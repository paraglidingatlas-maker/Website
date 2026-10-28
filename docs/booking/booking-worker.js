/**
 * Paragliding Atlas booking relay
 *
 * Receives a hold from prototypes/v4/book.html, keeps it under a reference,
 * takes the card payment through Stripe Checkout when a sum is due, and
 * hands the pilot to MailerLite so the booking confirmation and the welcome
 * kit go out from there. Same shape as enquiry-worker.js and
 * corrections-worker.js: one small Worker, one job, no framework and no SDK.
 *
 * DEPLOY THIS AS A SEPARATE WORKER. Not inside the enquiry or corrections
 * Workers and not inside the restless-king-e534 proxy.
 *
 * Routes
 *   POST /hold            the form. JSON back to the page's script, or a plain
 *                         HTML confirmation when the form posts without one.
 *   GET  /status?ref=     the hold's public state, for the page on the way
 *                         back from Stripe.
 *   POST /stripe-webhook  checkout.session.completed, signature verified.
 *
 * ---------------------------------------------------------------------------
 * SETUP, in order. docs/booking.md says the same at more length.
 *
 * 1. KV namespace. `wrangler kv namespace create BOOKINGS`, then bind it in
 *    wrangler.toml as BOOKINGS. Every hold is one key, hold:<reference>.
 *
 * 2. Secrets, each with `wrangler secret put <NAME>`:
 *      MAILERLITE_API_KEY     MailerLite > Integrations > API (a new token)
 *      STRIPE_SECRET_KEY      Stripe > Developers > API keys (sk_live_... or sk_test_...)
 *      STRIPE_WEBHOOK_SECRET  Stripe > Developers > Webhooks, after adding the
 *                             endpoint <worker-url>/stripe-webhook for the event
 *                             checkout.session.completed (whsec_...)
 *    Without STRIPE_SECRET_KEY the relay still holds places and books calls;
 *    the deposit button on the page is disabled for any departure whose sum
 *    due is not set below, and "deposit" posts are answered as a call hold.
 *
 * 3. Optional: a "Send email" binding named EMAIL (as in enquiry-worker.js) so
 *    every hold is also emailed to aninder@paraglidingatlas.com. Without it,
 *    nothing is emailed from here; MailerLite still sends the pilot's emails.
 *
 * 4. Vars in wrangler.toml: SITE = "https://paraglidingatlas.com" (where
 *    book.html lives; the prototype is served under /prototypes/v4/ until the
 *    switch, so set SITE to that while testing).
 *
 * 5. Deploy, copy the Worker URL into ENDPOINT in tools/v4_book.py, rebuild
 *    the page. Until then the page says the relay is not connected and offers
 *    the call.
 * ---------------------------------------------------------------------------
 */

import { EmailMessage } from "cloudflare:email";

/** Only these origins may post here. Kept identical to enquiry-worker.js. */
const ALLOWED_ORIGINS = [
  "https://paraglidingatlas-maker.github.io",
  "https://paraglidingatlas.com",
  "https://www.paraglidingatlas.com",
];

/** The departures, exactly as the trip pages state them; the page's list is
 *  built from the same facts (tools/v4_book.py). `due` is the sum payable
 *  when you book, in minor units, where the site states it: India's trip page
 *  says the full £1,100 is due when you book because both departures are
 *  within 120 days. Kenya's page says "Enquire for prices", so its due is
 *  null and no payment can be taken for it until the owner sets one. */
const DEPARTURES = {
  "india-1": { trip: "india", group: "India 2026 pilots", title: "India Tour 1", place: "Bir Billing",
    when: "21 to 30 October 2026", start: "2026-10-21", len: "10 days", currency: "gbp", due: 110000,
    due_text: "£1,100, the full price (the departure is within 120 days)" },
  "india-2": { trip: "india", group: "India 2026 pilots", title: "India Tour 2", place: "Bir Billing",
    when: "3 to 12 November 2026", start: "2026-11-03", len: "10 days", currency: "gbp", due: 110000,
    due_text: "£1,100, the full price (the departure is within 120 days)" },
  "kenya-1": { trip: "kenya", group: "Kenya 2027 pilots", title: "Kenya Tour 1", place: "Kerio Valley",
    when: "18 to 29 January 2027", start: "2027-01-18", len: "12 days", currency: null, due: null, due_text: null },
  "kenya-2": { trip: "kenya", group: "Kenya 2027 pilots", title: "Kenya Tour 2", place: "Kerio Valley",
    when: "1 to 12 February 2027", start: "2027-02-01", len: "12 days", currency: null, due: null, due_text: null },
};

/** MailerLite group ids, by the group name above (read from the account, 21 Oct 2026). */
const MAILERLITE_GROUPS = {
  "India 2026 pilots": "199795329387726060",
  "Kenya 2027 pilots": "201934341732828248",
};

const CALENDAR = "https://calendar.app.google/HaJMYuiomt5Db9eh8";
const OWNER = "aninder@paraglidingatlas.com";
const FROM = "bookings@send.paraglidingatlas.com";
const FROM_NAME = "Paragliding Atlas booking relay";

/** Field length caps, one per field the page sends. */
const LIMITS = {
  name: 120, email: 200, phone: 40, country: 120, rating: 120, total: 40, recent: 40, wing: 160,
  ice_name: 120, ice_phone: 40, heard: 60, departure: 20, mode: 10, page: 40,
};

/** Rate limit: this many posts per window, per IP, counted in KV. */
const RATE = { posts: 8, windowSeconds: 600 };

/** The terms, in one line each, for the plain confirmation. Quoted from terms.html. */
const TERMS_LINE = "The full balance is due 120 days before departure; your deposit is not refunded; a termination fee applies if you cancel, worked out as the Package Travel Act requires.";

function cors(origin) {
  const allow = ALLOWED_ORIGINS.includes(origin) ? origin : ALLOWED_ORIGINS[0];
  return {
    "Access-Control-Allow-Origin": allow,
    "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type, Accept",
    "Access-Control-Max-Age": "86400",
  };
}

function json(body, status, origin) {
  return new Response(JSON.stringify(body), {
    status,
    headers: { "Content-Type": "application/json", "Cache-Control": "no-store", ...cors(origin) },
  });
}

function html(body, status) {
  return new Response(body, { status, headers: { "Content-Type": "text/html; charset=utf-8", "Cache-Control": "no-store" } });
}

function esc(s) {
  return String(s || "").replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
}

/** Strip CR and LF from anything going into a header or a single-line field. */
function oneLine(s) {
  return String(s || "").replace(/[\r\n]+/g, " ").trim();
}

function encodeHeader(s) {
  const clean = oneLine(s);
  // eslint-disable-next-line no-control-regex
  if (/^[\x20-\x7E]*$/.test(clean)) return clean;
  const b64 = btoa(String.fromCharCode(...new TextEncoder().encode(clean)));
  return "=?UTF-8?B?" + b64 + "?=";
}

function buildMime({ subject, replyTo, text }) {
  const body = btoa(String.fromCharCode(...new TextEncoder().encode(text))).replace(/(.{76})/g, "$1\r\n");
  return [
    `From: ${encodeHeader(FROM_NAME)} <${FROM}>`,
    `To: <${OWNER}>`,
    replyTo ? `Reply-To: <${oneLine(replyTo)}>` : null,
    `Subject: ${encodeHeader(subject)}`,
    `Message-ID: <${crypto.randomUUID()}@paraglidingatlas.com>`,
    `Date: ${new Date().toUTCString()}`,
    "MIME-Version: 1.0",
    'Content-Type: text/plain; charset="utf-8"',
    "Content-Transfer-Encoding: base64",
    "",
    body,
  ].filter((l) => l !== null).join("\r\n");
}

/** A reference like PA-2026-7K3Q: the year, then four characters from an
 *  alphabet without 0/O, 1/I, so it survives being read out on a phone. */
function newRef() {
  const alphabet = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789";
  const bytes = crypto.getRandomValues(new Uint8Array(4));
  let s = "";
  for (const b of bytes) s += alphabet[b % alphabet.length];
  return `PA-${new Date().getUTCFullYear()}-${s}`;
}

/** The balance date, as the terms set it: 120 days before departure. If that
 *  day has passed, the balance is due with the booking, which is what the
 *  India page says of its departures. */
function balanceLine(dep) {
  const start = new Date(dep.start + "T00:00:00Z");
  const due = new Date(start.getTime() - 120 * 86400000);
  const now = new Date();
  const fmt = (d) => d.toLocaleDateString("en-GB", { day: "numeric", month: "long", year: "numeric", timeZone: "UTC" });
  if (due <= now) return `Due with the booking: the departure is within 120 days (the terms' balance date, ${fmt(due)}, has passed)`;
  return `${fmt(due)} (120 days before departure, as the booking terms set out)`;
}

function paymentLine(h) {
  if (h.status === "paid") return `Paid: ${h.dep.due_text}, by card, Stripe reference ${h.payment_ref || "pending"}`;
  if (h.mode === "deposit") return `Card payment started, not yet confirmed: ${h.dep.due_text}`;
  if (h.dep.due_text) return `Deposit pending, call booked. Due when you book: ${h.dep.due_text}`;
  return "Deposit pending, call booked. The deposit for this trip is [to supply]";
}

/* ----------------------------------------------------------------- Stripe */

function formEncode(obj, prefix) {
  const out = [];
  for (const [k, v] of Object.entries(obj)) {
    const key = prefix ? `${prefix}[${k}]` : k;
    if (v === null || v === undefined) continue;
    if (typeof v === "object") out.push(formEncode(v, key));
    else out.push(encodeURIComponent(key) + "=" + encodeURIComponent(String(v)));
  }
  return out.filter(Boolean).join("&");
}

async function stripeCheckout(env, h) {
  const site = env.SITE || "https://paraglidingatlas.com";
  const body = formEncode({
    mode: "payment",
    client_reference_id: h.ref,
    customer_email: h.email,
    success_url: `${site}/book.html?ref=${h.ref}&cs={CHECKOUT_SESSION_ID}`,
    cancel_url: `${site}/book.html?ref=${h.ref}&cancelled=1`,
    line_items: { 0: { quantity: 1, price_data: { currency: h.dep.currency, unit_amount: h.dep.due,
      product_data: { name: `${h.dep.title}, ${h.dep.when}: a place for one pilot`, description: `Paragliding Atlas, ${h.dep.place}. Reference ${h.ref}.` } } } },
    payment_intent_data: { description: `${h.ref} ${h.dep.title} ${h.dep.when}`, receipt_email: h.email, metadata: { ref: h.ref } },
    metadata: { ref: h.ref, departure: h.departure },
  });
  const r = await fetch("https://api.stripe.com/v1/checkout/sessions", {
    method: "POST",
    headers: { Authorization: `Bearer ${env.STRIPE_SECRET_KEY}`, "Content-Type": "application/x-www-form-urlencoded", "Idempotency-Key": `hold-${h.ref}` },
    body,
  });
  const data = await r.json();
  if (!r.ok || !data.url) throw new Error("stripe: " + (data.error && data.error.message));
  return data;
}

async function stripeSession(env, id) {
  const r = await fetch(`https://api.stripe.com/v1/checkout/sessions/${encodeURIComponent(id)}`, {
    headers: { Authorization: `Bearer ${env.STRIPE_SECRET_KEY}` },
  });
  if (!r.ok) return null;
  return r.json();
}

async function hmacHex(secret, msg) {
  const key = await crypto.subtle.importKey("raw", new TextEncoder().encode(secret), { name: "HMAC", hash: "SHA-256" }, false, ["sign"]);
  const sig = await crypto.subtle.sign("HMAC", key, new TextEncoder().encode(msg));
  return [...new Uint8Array(sig)].map((b) => b.toString(16).padStart(2, "0")).join("");
}

function sameString(a, b) {
  if (a.length !== b.length) return false;
  let out = 0;
  for (let i = 0; i < a.length; i++) out |= a.charCodeAt(i) ^ b.charCodeAt(i);
  return out === 0;
}

/** Stripe-Signature: t=<unix>,v1=<hex>[,v1=...]. Signed payload is `${t}.${body}`. */
async function verifyStripe(env, header, body) {
  if (!env.STRIPE_WEBHOOK_SECRET || !header) return false;
  const parts = Object.create(null);
  const v1 = [];
  for (const kv of header.split(",")) {
    const [k, v] = kv.split("=", 2);
    if (k === "t") parts.t = v;
    if (k === "v1") v1.push(v);
  }
  if (!parts.t || !v1.length) return false;
  if (Math.abs(Date.now() / 1000 - Number(parts.t)) > 300) return false;
  const expected = await hmacHex(env.STRIPE_WEBHOOK_SECRET, `${parts.t}.${body}`);
  return v1.some((s) => sameString(s, expected));
}

/* ------------------------------------------------------------- MailerLite */

/** Add or update the pilot (the subscribers endpoint upserts on email), with
 *  the booking fields, and put them in the trip's group, which starts the
 *  "Booking confirmation" automation and, for India, the welcome kit. */
async function mailerlite(env, h) {
  if (!env.MAILERLITE_API_KEY) return { skipped: "no MAILERLITE_API_KEY" };
  const groupId = MAILERLITE_GROUPS[h.dep.group];
  const body = {
    email: h.email,
    fields: {
      name: h.name,
      phone: h.phone,
      country: h.country,
      trip: `${h.dep.title}, ${h.dep.place}`,
      departure: h.dep.when,
      reference: h.ref,
      deposit_status: paymentLine(h),
      balance_due: h.status === "paid" ? "Nothing further is due: the full price was paid with the booking" : balanceLine(h.dep),
    },
    groups: groupId ? [groupId] : [],
    status: "active",
  };
  const r = await fetch("https://connect.mailerlite.com/api/subscribers", {
    method: "POST",
    headers: { Authorization: `Bearer ${env.MAILERLITE_API_KEY}`, "Content-Type": "application/json", Accept: "application/json" },
    body: JSON.stringify(body),
  });
  if (!r.ok) throw new Error("mailerlite " + r.status + " " + (await r.text()).slice(0, 200));
  return r.json();
}

/* ------------------------------------------------------------------- KV */

async function getHold(env, ref) {
  if (!/^PA-\d{4}-[A-Z0-9]{4}$/.test(ref)) return null;
  const raw = await env.BOOKINGS.get("hold:" + ref);
  return raw ? JSON.parse(raw) : null;
}

async function putHold(env, h) {
  await env.BOOKINGS.put("hold:" + h.ref, JSON.stringify(h));
}

async function rateLimited(env, ip) {
  const key = "rate:" + ip + ":" + Math.floor(Date.now() / 1000 / RATE.windowSeconds);
  const n = Number((await env.BOOKINGS.get(key)) || 0) + 1;
  await env.BOOKINGS.put(key, String(n), { expirationTtl: RATE.windowSeconds * 2 });
  return n > RATE.posts;
}

/** What the page may see of a hold. Never the phone numbers or the contact. */
function publicHold(h) {
  return {
    ok: true, ref: h.ref, mode: h.mode, status: h.status, departure_id: h.departure,
    trip_title: `${h.dep.title}, ${h.dep.place}`, when: h.dep.when, email: h.email,
    payment: paymentLine(h), balance: h.status === "paid" ? "Nothing further is due" : balanceLine(h.dep),
    calendar: CALENDAR,
  };
}

/** The plain confirmation, for a form that posted without JavaScript. The
 *  site's tokens, nothing else; book.html draws the full one. */
function plainConfirmation(h) {
  const p = publicHold(h);
  return `<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex"><title>Held: ${esc(p.ref)} | Paragliding Atlas</title>
<style>body{margin:0;background:#141519;color:#b4b4b4;font:16px/1.7 "DM Sans",system-ui,sans-serif;padding:2rem 1rem}main{max-width:40rem;margin:0 auto;background:#202127;padding:1.6rem 1.4rem}
.k{font-size:.72rem;font-weight:600;letter-spacing:.16em;text-transform:uppercase;color:#ff7517;margin:0}.r{font-family:"DM Mono",ui-monospace,monospace;font-size:2rem;color:#f6f4f4;margin:.2rem 0 1rem}
.s{color:#5fd08a;font-size:.72rem;font-weight:600;letter-spacing:.12em;text-transform:uppercase}dl{margin:0;border-top:1px solid #2b2c33;padding-top:.8rem}dt{font-size:.72rem;letter-spacing:.14em;text-transform:uppercase;color:#737373}dd{margin:0 0 .7rem;color:#f6f4f4;font-family:"DM Mono",ui-monospace,monospace;font-size:.95rem}
a{color:#ff7517}.b{display:inline-block;background:#ff7517;color:#141519;font-weight:700;padding:.8rem 1.4rem;text-decoration:none;margin:.6rem 0}ol{padding-left:1.3rem}</style></head><body><main>
<span class="s">Held</span><p class="k">Your reference</p><p class="r">${esc(p.ref)}</p>
<dl><dt>Trip</dt><dd>${esc(p.trip_title)}</dd><dt>Dates</dt><dd>${esc(p.when)}</dd><dt>Payment</dt><dd>${esc(p.payment)}</dd><dt>Balance</dt><dd>${esc(p.balance)}</dd><dt>Confirmation to</dt><dd>${esc(p.email)}</dd></dl>
<ol><li>A confirmation email is on its way with this reference, the dates and the terms in one line.</li>
${h.mode === "call" ? `<li>Book the call: <a class="b" href="${CALENDAR}">Book a free 30-minute call</a></li>` : "<li>Stripe sends the card receipt to the same address.</li>"}
<li>Two days after the confirmation, the welcome kit: the packing list, visa and insurance, and how the days run.</li></ol>
<p>Quote ${esc(p.ref)} in any message about this booking. ${esc(TERMS_LINE)}</p>
<p><a href="https://paraglidingatlas.com/">paraglidingatlas.com</a></p></main></body></html>`;
}

async function notifyOwner(env, h, what) {
  if (!env.EMAIL) return;
  const text = [
    `${what}: ${h.ref}`, "",
    `Trip:      ${h.dep.title}, ${h.dep.when}`,
    `Name:      ${h.name}`, `Email:     ${h.email}`, `Phone:     ${h.phone}`, `Based in:  ${h.country}`, "",
    `Licence:   ${h.rating}`, `Airtime:   ${h.total} total, ${h.recent} in the last 12 months`, `Wing:      ${h.wing}`, "",
    `Emergency: ${h.ice_name}, ${h.ice_phone}`, `Heard via: ${h.heard || "not given"}`, "",
    `Mode:      ${h.mode}`, `Status:    ${h.status}`, `Payment:   ${paymentLine(h)}`, `Balance:   ${balanceLine(h.dep)}`, "",
    `Held at:   ${h.created}`, `From IP country: ${h.ip_country}`,
  ].join("\n");
  try {
    await env.EMAIL.send(new EmailMessage(FROM, OWNER, buildMime({ subject: `${what}: ${h.ref} ${h.dep.title} ${h.name}`, replyTo: h.email, text })));
  } catch (err) {
    console.error("owner email failed", err && err.message);
  }
}

/** After a hold is settled (paid, or a call booked): MailerLite, then the owner. */
async function afterHold(env, h, what) {
  try {
    const ml = await mailerlite(env, h);
    h.mailerlite = ml && ml.data ? ml.data.id : (ml && ml.skipped) || "ok";
  } catch (err) {
    console.error("mailerlite failed", err && err.message);
    h.mailerlite = "failed: " + (err && err.message);
  }
  await putHold(env, h);
  await notifyOwner(env, h, what);
}

/* ------------------------------------------------------------------ routes */

async function postHold(request, env, ctx, origin) {
  const wantsJson = /application\/json/.test(request.headers.get("Accept") || "");
  const ip = request.headers.get("CF-Connecting-IP") || "0";
  if (await rateLimited(env, ip)) {
    return wantsJson ? json({ ok: false, error: "Too many attempts from this connection. Please try again in a few minutes." }, 429, origin)
      : html("<p>Too many attempts. Please try again in a few minutes.</p>", 429);
  }

  let form;
  try { form = await request.formData(); } catch { return json({ ok: false, error: "Could not read the form" }, 400, origin); }
  const get = (k) => oneLine(String(form.get(k) || "")).slice(0, LIMITS[k] || 200);

  /* Honeypot and time trap, as the other forms. */
  if (String(form.get("website") || "").trim() !== "") return json({ ok: true, ref: "PA-0000-0000" }, 200, origin);
  const started = Number(form.get("t") || 0);
  if (started && Date.now() - started < 3000) return json({ ok: true, ref: "PA-0000-0000" }, 200, origin);

  const dep = DEPARTURES[get("departure")];
  const fail = (m) => (wantsJson ? json({ ok: false, error: m }, 400, origin) : html(`<p>${esc(m)}</p>`, 400));
  if (!dep) return fail("Pick one of the four departures.");
  const h = {
    ref: newRef(), departure: get("departure"), dep, mode: get("mode") === "deposit" ? "deposit" : "call",
    name: get("name"), email: get("email").toLowerCase(), phone: get("phone"), country: get("country"),
    rating: get("rating"), total: get("total"), recent: get("recent"), wing: get("wing"),
    ice_name: get("ice_name"), ice_phone: get("ice_phone"), heard: get("heard"),
    status: "held", created: new Date().toISOString(), ip_country: request.headers.get("CF-IPCountry") || "unknown",
  };
  for (const k of ["name", "phone", "country", "rating", "total", "recent", "wing", "ice_name", "ice_phone"]) {
    if (!h[k]) return fail("Please fill in every field in step 2.");
  }
  if (!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(h.email)) return fail("That email address looks wrong.");
  if (!form.get("consent")) return fail("Please read the terms and tick the box.");

  /* A reference must be new. Four characters from 32 give a million; check anyway. */
  for (let i = 0; i < 5 && (await getHold(env, h.ref)); i++) h.ref = newRef();

  if (h.mode === "deposit" && dep.due && env.STRIPE_SECRET_KEY) {
    try {
      const session = await stripeCheckout(env, h);
      h.stripe_session = session.id;
      h.status = "awaiting_payment";
      await putHold(env, h);
      if (wantsJson) return json({ ...publicHold(h), checkout_url: session.url }, 200, origin);
      return Response.redirect(session.url, 303);
    } catch (err) {
      console.error("checkout failed", err && err.message);
      return wantsJson ? json({ ok: false, error: "The card payment could not be started. Please try the call instead, or email " + OWNER + "." }, 502, origin)
        : html("<p>The card payment could not be started. Please email " + OWNER + ".</p>", 502);
    }
  }

  /* A call hold, or a deposit asked for where none can be taken yet. */
  h.mode = "call";
  h.status = "held";
  await putHold(env, h);
  ctx.waitUntil(afterHold(env, h, "Place held, call to book"));
  return wantsJson ? json(publicHold(h), 200, origin) : html(plainConfirmation(h), 200);
}

async function getStatus(request, env, origin) {
  const url = new URL(request.url);
  const ref = (url.searchParams.get("ref") || "").toUpperCase();
  const h = await getHold(env, ref);
  if (!h) return json({ ok: false, error: "No such reference" }, 404, origin);
  /* Back from Stripe before the webhook landed: ask Stripe about the session. */
  if (h.status === "awaiting_payment" && h.stripe_session && env.STRIPE_SECRET_KEY) {
    const s = await stripeSession(env, h.stripe_session);
    if (s && s.payment_status === "paid") await markPaid(env, h, s);
  }
  return json(publicHold(h), 200, origin);
}

async function markPaid(env, h, session) {
  if (h.status === "paid") return;
  h.status = "paid";
  h.paid_at = new Date().toISOString();
  h.payment_ref = session.payment_intent || session.id;
  h.amount_paid = session.amount_total;
  await putHold(env, h);
  await afterHold(env, h, "Place held and paid");
}

async function stripeWebhook(request, env, ctx) {
  const body = await request.text();
  if (!(await verifyStripe(env, request.headers.get("Stripe-Signature"), body))) {
    return new Response("bad signature", { status: 400 });
  }
  let event;
  try { event = JSON.parse(body); } catch { return new Response("bad json", { status: 400 }); }
  if (event.type === "checkout.session.completed" || event.type === "checkout.session.async_payment_succeeded") {
    const session = event.data.object;
    const ref = (session.client_reference_id || (session.metadata && session.metadata.ref) || "").toUpperCase();
    const h = await getHold(env, ref);
    if (h && session.payment_status === "paid") ctx.waitUntil(markPaid(env, h, session));
  }
  return new Response("ok", { status: 200 });
}

export default {
  async fetch(request, env, ctx) {
    const origin = request.headers.get("Origin") || "";
    const url = new URL(request.url);

    if (request.method === "OPTIONS") return new Response(null, { status: 204, headers: cors(origin) });

    if (url.pathname === "/stripe-webhook") {
      if (request.method !== "POST") return new Response("POST only", { status: 405 });
      return stripeWebhook(request, env, ctx);
    }

    /* Everything else is for the site. A plain form post carries Origin too. */
    if (!ALLOWED_ORIGINS.includes(origin)) return json({ ok: false, error: "Origin not allowed" }, 403, origin);

    if (url.pathname === "/hold" && request.method === "POST") return postHold(request, env, ctx, origin);
    if (url.pathname === "/status" && request.method === "GET") return getStatus(request, env, origin);
    return json({ ok: false, error: "Not found" }, 404, origin);
  },
};

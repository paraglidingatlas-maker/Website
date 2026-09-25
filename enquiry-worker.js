/**
 * Paragliding Atlas trip enquiry form receiver
 *
 * Receives a POST from the enquiry page and emails it to Aninder using
 * Cloudflare's native send_email binding. Same approach as corrections-worker.js:
 * no third-party email provider, no API key, and it only ever sends to a
 * verified destination address on your own account.
 *
 * DEPLOY THIS AS A SEPARATE WORKER.
 * Not inside the corrections Worker and not inside the restless-king-e534
 * proxy. One form per Worker keeps each one small, and means a problem with
 * one form (or switching one off) never touches the other.
 *
 * ---------------------------------------------------------------------------
 * SETUP, in order. Steps 1 to 3 are in the Cloudflare dashboard.
 *
 * 1. Onboard `send.paraglidingatlas.com` under
 *    Compute > Email Service > Email Sending > Onboard Domain.
 *    SHARED WITH THE CORRECTIONS WORKER: if that is already done for
 *    corrections-worker.js, skip this step. One onboarded subdomain can send
 *    from any address on it, so enquiries@ and corrections@ both work.
 *    Choose the SUBDOMAIN, not the apex. Cloudflare writes its cf-bounce MX,
 *    SPF, DKIM and DMARC records onto that subdomain only, so the apex MX,
 *    which points at Google Workspace, is never touched and your email cannot
 *    break. See the notes at the foot of corrections-worker.js for why.
 *
 * 2. Verify your destination address:
 *    Compute > Email Service > Email Routing > Destination Addresses
 *    Add aninder@paraglidingatlas.com and click the link Cloudflare emails you.
 *    SHARED WITH THE CORRECTIONS WORKER: a destination is verified once per
 *    account, so if it already shows as Verified, skip this step.
 *    Until that link is clicked, nothing will send.
 *
 * 3. Create a new Worker (for example `enquiry-form`), paste this file in,
 *    then under Settings > Bindings add a "Send email" binding:
 *      Variable name : EMAIL
 *      Type          : Send email
 *      Destination   : aninder@paraglidingatlas.com   (restricted, not open)
 *    Restricting it means this Worker can only ever email you, so even if the
 *    endpoint is abused it cannot be turned into a spam relay.
 *
 * 4. FROM below is already set to an address on the sending subdomain. Check
 *    ALLOWED_ORIGINS covers wherever the site is served from at the time.
 *
 * 5. Deploy, copy the worker URL, and paste it into `var ENDPOINT = "";` in
 *    the enquiry page's form script. Until then the page keeps opening the
 *    visitor's own mail app, exactly as it does now.
 * ---------------------------------------------------------------------------
 */

import { EmailMessage } from "cloudflare:email";

/** Must be an address on the SENDING SUBDOMAIN, never on the apex. The apex
 *  SPF ends in `-all` (Google only), so anything sent as @paraglidingatlas.com
 *  from Cloudflare would hard fail. The full reasoning is in
 *  corrections-worker.js. It does not need to be a real mailbox: nobody
 *  replies to it, because Reply-To is set to the person enquiring. */
const FROM = "enquiries@send.paraglidingatlas.com";
const FROM_NAME = "Paragliding Atlas enquiry form";

/** Must match the verified destination address exactly. */
const TO = "aninder@paraglidingatlas.com";

/** Only these origins may post here. Add the custom domain when DNS moves.
 *  A wildcard would let any site on the internet post through your Worker.
 *  Kept identical to corrections-worker.js. */
const ALLOWED_ORIGINS = [
  "https://paraglidingatlas-maker.github.io",
  "https://paraglidingatlas.com",
  "https://www.paraglidingatlas.com",
];

/** Field length caps, one per field the enquiry form sends. A form post is
 *  small; anything larger is not a human. `trip` is a select, so its cap only
 *  matters if someone posts to the Worker directly. */
const LIMITS = {
  name: 120,
  email: 200,
  country: 120,
  trip: 80,
  when: 200,
  rating: 200,
  total: 100,
  recent: 100,
  wing: 200,
  xc: 1000,
  message: 5000,
};

function cors(origin) {
  const allow = ALLOWED_ORIGINS.includes(origin) ? origin : ALLOWED_ORIGINS[0];
  return {
    "Access-Control-Allow-Origin": allow,
    "Access-Control-Allow-Methods": "POST, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type",
    "Access-Control-Max-Age": "86400",
  };
}

function json(body, status, origin) {
  return new Response(JSON.stringify(body), {
    status,
    headers: { "Content-Type": "application/json", ...cors(origin) },
  });
}

/** Strip CR and LF from anything going into a header.
 *  Without this, a newline in the name field lets someone inject extra
 *  headers and add their own recipients. This is the one security check in
 *  here that is not optional. */
function headerSafe(s) {
  return String(s || "").replace(/[\r\n]+/g, " ").trim();
}

/** RFC 2047 encode, so a Norwegian or accented name survives the subject line. */
function encodeHeader(s) {
  const clean = headerSafe(s);
  // eslint-disable-next-line no-control-regex
  if (/^[\x20-\x7E]*$/.test(clean)) return clean;
  const b64 = btoa(String.fromCharCode(...new TextEncoder().encode(clean)));
  return "=?UTF-8?B?" + b64 + "?=";
}

function buildMime({ subject, replyTo, text }) {
  const body = btoa(String.fromCharCode(...new TextEncoder().encode(text)))
    .replace(/(.{76})/g, "$1\r\n");
  const lines = [
    `From: ${encodeHeader(FROM_NAME)} <${FROM}>`,
    `To: <${TO}>`,
    replyTo ? `Reply-To: <${headerSafe(replyTo)}>` : null,
    `Subject: ${encodeHeader(subject)}`,
    `Message-ID: <${crypto.randomUUID()}@paraglidingatlas.com>`,
    `Date: ${new Date().toUTCString()}`,
    "MIME-Version: 1.0",
    'Content-Type: text/plain; charset="utf-8"',
    "Content-Transfer-Encoding: base64",
    "",
    body,
  ].filter((l) => l !== null); // not filter(Boolean): that would also drop the
  // "" above, the blank line that separates headers from body, and the whole
  // base64 body would then be read as one broken header.
  return lines.join("\r\n");
}

export default {
  async fetch(request, env) {
    const origin = request.headers.get("Origin") || "";

    if (request.method === "OPTIONS") {
      return new Response(null, { status: 204, headers: cors(origin) });
    }
    if (request.method !== "POST") {
      return json({ ok: false, error: "POST only" }, 405, origin);
    }
    if (!ALLOWED_ORIGINS.includes(origin)) {
      return json({ ok: false, error: "Origin not allowed" }, 403, origin);
    }

    let form;
    try {
      form = await request.formData();
    } catch {
      return json({ ok: false, error: "Could not read the form" }, 400, origin);
    }

    const get = (k) => String(form.get(k) || "").trim().slice(0, LIMITS[k] || 500);
    /* Every field except message and xc is a single line on the page, so keep
       it one: a newline smuggled into the name should not become a fake line
       in the email, let alone a header. */
    const one = (k) => headerSafe(get(k));

    /* Honeypot. The form renders a field no human ever sees; a bot fills every
       field it finds. Return 200 rather than an error, so a bot cannot tell it
       was caught and retry with the field cleared. */
    if (String(form.get("website") || "").trim() !== "") {
      return json({ ok: true }, 200, origin);
    }

    /* Time trap. The form stamps when it was rendered. Nobody fills in this
       form in under three seconds; a bot posts instantly. */
    const started = Number(form.get("t") || 0);
    if (started && Date.now() - started < 3000) {
      return json({ ok: true }, 200, origin);
    }

    const name = one("name");
    const email = one("email");
    const message = get("message");
    const rating = one("rating");
    const total = one("total");
    const recent = one("recent");

    /* The page marks these required, so a real visitor never gets here with
       them empty. Checked again because the browser's word is not proof. */
    if (!name || !rating || !total || !recent) {
      return json({ ok: false, error: "Please fill in the required fields." }, 400, origin);
    }
    if (!email || !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email)) {
      return json({ ok: false, error: "That email address looks wrong." }, 400, origin);
    }
    if (message.length < 10) {
      return json({ ok: false, error: "Please write a little more in your message." }, 400, origin);
    }
    if (!form.get("consent")) {
      return json({ ok: false, error: "Please tick the consent box." }, 400, origin);
    }

    const trip = one("trip") || "not given";

    const text = [
      "A trip enquiry was submitted on paraglidingatlas.com",
      "",
      `Name:     ${name}`,
      `Email:    ${email}`,
      `Based in: ${one("country") || "not given"}`,
      `Country:  ${request.headers.get("CF-IPCountry") || "unknown"} (from IP)`,
      `Time:     ${new Date().toISOString()}`,
      "",
      `Trip:     ${trip}`,
      `Timing:   ${one("when") || "not given"}`,
      "",
      `Licence or rating:    ${rating}`,
      `Total airtime:        ${total}`,
      `Hours last 12 months: ${recent}`,
      `Wing:                 ${one("wing") || "not given"}`,
      `XC and SIV:           ${get("xc") || "not given"}`,
      "",
      "Message:",
      message,
      "",
      "Consent given to use these details to answer this enquiry.",
      "",
      "---",
      "Sent by the enquiry form. Reply directly to reach the sender.",
    ].join("\n");

    try {
      await env.EMAIL.send(
        new EmailMessage(
          FROM,
          TO,
          buildMime({
            subject: `Trip enquiry: ${trip} - ${name}`,
            replyTo: email,
            text,
          })
        )
      );
    } catch (err) {
      /* Do not leak the internal error to the page. Log it for the dashboard. */
      console.error("send failed", err && err.message);
      return json(
        { ok: false, error: "Could not send that. Please email aninder@paraglidingatlas.com instead." },
        502,
        origin
      );
    }

    return json({ ok: true }, 200, origin);
  },
};

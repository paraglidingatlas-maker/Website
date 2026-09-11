/**
 * Paragliding Atlas corrections form receiver
 *
 * Receives a POST from the corrections page and emails it to Aninder using
 * Cloudflare's native send_email binding. No third-party email provider, no API
 * key, no SPF or DKIM records needed, because it only ever sends to a verified
 * destination address on your own account, which Cloudflare allows free on any
 * plan and does not count against any quota.
 *
 * DEPLOY THIS AS A SEPARATE WORKER.
 * Do not add it to the existing restless-king-e534 proxy. That one is marked in
 * the handoff as confirmed-working and not to be modified casually, and mixing a
 * public CORS proxy with an email sender in one script is asking for trouble.
 *
 * ---------------------------------------------------------------------------
 * SETUP, in order. Steps 1 to 3 are in the Cloudflare dashboard.
 *
 * 1. Onboard `send.paraglidingatlas.com` under
 *    Compute > Email Service > Email Sending > Onboard Domain.
 *    Choose the SUBDOMAIN, not the apex. Cloudflare writes its cf-bounce MX,
 *    SPF, DKIM and DMARC records onto that subdomain only, so the apex MX,
 *    which points at Google Workspace, is never touched and your email cannot
 *    break. Verified in DNS 2026-09-11: apex MX is Google, apex SPF ends in
 *    `-all`, and `send.` is unused.
 *
 * 2. Verify your destination address:
 *    Compute > Email Service > Email Routing > Destination Addresses
 *    Add aninder@paraglidingatlas.com and click the link Cloudflare emails you.
 *    Until that link is clicked, nothing will send.
 *
 * 3. Create a new Worker, paste this file in, then under
 *    Settings > Bindings add a "Send email" binding:
 *      Variable name : EMAIL
 *      Type          : Send email
 *      Destination   : aninder@paraglidingatlas.com   (restricted, not open)
 *    Restricting it means this Worker can only ever email you, so even if the
 *    endpoint is abused it cannot be turned into a spam relay.
 *
 * 4. Set FROM below to an address on the routed domain, and ALLOWED_ORIGIN to
 *    wherever the site is served from at the time.
 *
 * 5. Deploy, then send me the worker URL and I will wire the form to it.
 * ---------------------------------------------------------------------------
 */

import { EmailMessage } from "cloudflare:email";

/** Must be an address on the SENDING SUBDOMAIN, never on the apex.
 *
 *  Two reasons, both checked in DNS rather than assumed:
 *  1. The apex SPF record is `v=spf1 include:_spf.google.com -all`. The `-all`
 *     is a hard fail, so anything sent as @paraglidingatlas.com from somewhere
 *     that is not Google gets rejected, quite possibly silently.
 *  2. Onboarding a SUBDOMAIN for sending puts Cloudflare's records on the
 *     subdomain and leaves the apex MX untouched, so Google Workspace mail
 *     keeps working exactly as it does now.
 *
 *  `mail.paraglidingatlas.com` is already in use, pointing at Cloudflare.
 *  `send.` was confirmed free. It does not need to be a real mailbox: nobody
 *  replies to it, because Reply-To is set to whoever submitted the form. */
const FROM = "corrections@send.paraglidingatlas.com";
const FROM_NAME = "Paragliding Atlas corrections form";

/** Must match the verified destination address exactly. The user uses one
 *  address for all communication, which is a deliberate choice on his part. */
const TO = "aninder@paraglidingatlas.com";

/** Only these origins may post here. Add the custom domain when DNS moves.
 *  A wildcard would let any site on the internet post through your Worker. */
const ALLOWED_ORIGINS = [
  "https://paraglidingatlas-maker.github.io",
  "https://paraglidingatlas.com",
  "https://www.paraglidingatlas.com",
];

/** Field length caps. A form post is small; anything larger is not a human. */
const LIMITS = { name: 120, email: 200, page: 300, message: 5000 };

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
  ].filter(Boolean);
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

    /* Honeypot. The form renders a field no human ever sees; a bot fills every
       field it finds. Return 200 rather than an error, so a bot cannot tell it
       was caught and retry with the field cleared. */
    if (String(form.get("website") || "").trim() !== "") {
      return json({ ok: true }, 200, origin);
    }

    /* Time trap. The form stamps when it was rendered. A human takes seconds to
       type a correction; a bot posts instantly. */
    const started = Number(form.get("t") || 0);
    if (started && Date.now() - started < 3000) {
      return json({ ok: true }, 200, origin);
    }

    const message = get("message");
    if (message.length < 10) {
      return json({ ok: false, error: "Please write a little more detail." }, 400, origin);
    }

    const name = get("name") || "not given";
    const email = get("email");
    const page = get("page") || "not given";

    if (email && !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email)) {
      return json({ ok: false, error: "That email address looks wrong." }, 400, origin);
    }

    const text = [
      "A correction was submitted on paraglidingatlas.com",
      "",
      `From:    ${name}`,
      `Email:   ${email || "not given"}`,
      `Page:    ${page}`,
      `Country: ${request.headers.get("CF-IPCountry") || "unknown"}`,
      `Time:    ${new Date().toISOString()}`,
      "",
      "Message:",
      message,
      "",
      "---",
      "Sent by the corrections form. Reply directly to reach the sender,",
      "if they left an address.",
    ].join("\n");

    try {
      await env.EMAIL.send(
        new EmailMessage(
          FROM,
          TO,
          buildMime({
            subject: `Correction: ${page}`,
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

/* ---------------------------------------------------------------------------
 * DMARC NOTE, FOR WHOEVER TIGHTENS THE POLICY LATER
 *
 * paraglidingatlas.com published a DMARC record on 2026-09-11:
 *   v=DMARC1; p=none; rua=mailto:aninder@paraglidingatlas.com; fo=1
 * There is no `sp=` tag, so that policy applies to subdomains too, including
 * send.paraglidingatlas.com. At p=none nothing is affected either way.
 *
 * **When the policy is tightened to quarantine or reject, this Worker's mail
 * must still align.** Cloudflare's Email Sending onboarding writes SPF and DKIM
 * onto the sending subdomain, which is what makes it align, so this should be
 * fine. But confirm it before tightening: send a test through the form, open it
 * in Gmail, Show original, and check DMARC passes. Tightening while this fails
 * would silently drop every correction anyone submits.
 * ---------------------------------------------------------------------------
 */

/* ---------------------------------------------------------------------------
 * WHY A SUBDOMAIN, AND WHAT WOULD GO WRONG WITHOUT ONE
 *
 * Enabling Email Routing on a domain sets Cloudflare's own MX records on it.
 * If aninder@paraglidingatlas.com currently receives mail through Google
 * Workspace, Microsoft 365, or your registrar's mail service, those MX records
 * will be replaced and INBOUND MAIL TO THAT DOMAIN WILL STOP.
 *
 * That is the single thing in this whole job that can break something you rely
 * on every day, so confirm where that mailbox actually lives first.
 *
 * If the domain's email is hosted elsewhere and you want to keep it there, the
 * sending domain does not have to be the same one. Email Routing can be enabled
 * on any other domain or subdomain in your Cloudflare account, and this Worker
 * can still deliver to aninder@paraglidingatlas.com, because the destination
 * only has to be verified, not routed.
 * ------------------------------------------------------------------------- */

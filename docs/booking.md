# The booking flow (21 Oct 2026)

> **Parked (28 Oct 2026, imported into the live repo by chat 15).** The site's rules keep the live tree
> untouched until the owner switches booking on, so `booking-worker.js` sits at `docs/booking/booking-worker.js`
> and the two email images at `docs/booking/email-assets/`. When booking is switched on, move them back to the
> repo root and `assets/email/` (the emails link `https://paraglidingatlas.com/assets/email/...`).


The owner's ask: "activate the Hold a place / Book now buttons by enabling a
high-end booking system matching the vibe of the site, then connect it with a
confirmation email (with the receipt) and a welcome-kit email, both prepared."

Built, not yet live. Nothing is deployed, nothing sends, no automation is
enabled: every switch is the owner's.

## What exists

| Piece | Where |
|---|---|
| The page | `prototypes/v4/book.html`, built by `tools/v4_book.py` on the enquiry page's shell. Prototype-only (`tools/v2_site.py`, `PROTO_ONLY`). |
| The relay | `booking-worker.js` at the repo root, a Cloudflare Worker in the shape of `enquiry-worker.js`. |
| The emails | MailerLite automations "Booking confirmation" (id 201934827617781573) and "Welcome kit: India 2026" (id 201934830701643442), both disabled. The same HTML is kept in `docs/emails/booking-confirmation-india.html`, `booking-confirmation-kenya.html` (see the section at the end) and `docs/emails/welcome-kit-india.html`. |
| MailerLite fields | `trip`, `departure`, `reference`, `deposit_status`, `balance_due` (text; ids 1938134 to 1938138). |
| MailerLite groups | "India 2026 pilots" (199795329387726060, existed) and "Kenya 2027 pilots" (201934341732828248, new). The existing "Kenya 2027 interest" group is left for the interest list. |

## How it works

1. A trip's **Hold a place** link opens `book.html?trip=india&when=21+to+30+October+2026`
   (the same query the links already pass to `enquire.html`). The page opens on
   that departure. Three steps on one page: pick a departure (the four the trip
   pages list), who you are (name, email, phone, country, licence, hours, wing,
   emergency contact, how they heard), hold the place.
2. **Hold with a deposit** posts the form to the relay's `POST /hold` with
   `mode=deposit`. The relay validates (honeypot, time trap, rate limit, every
   field), writes the hold to KV under a reference like `PA-2026-7K3Q`, creates
   a Stripe Checkout Session for the sum due and sends the pilot to Stripe's
   page. Stripe returns them to `book.html?ref=PA-2026-7K3Q&cs=...`; the page asks
   `GET /status?ref=` and draws the confirmation. Stripe's webhook
   (`POST /stripe-webhook`, signature verified) marks the hold paid; if the
   pilot is back before the webhook, `/status` asks Stripe directly.
3. **Book a free 30-minute call** posts `mode=call`. The relay records the hold as
   "deposit pending, call booked" and answers at once; the page draws the
   confirmation with the calendar link.
4. After a hold is settled (paid, or a call hold) the relay upserts the pilot
   in MailerLite with the booking fields and puts them in the trip's group.
   Joining the group starts "Booking confirmation" (at once) and, for India,
   "Welcome kit: India 2026" (two days later). With an `EMAIL` binding the relay
   also emails the owner the full hold (phone, contact, flying), which never
   goes to MailerLite.
5. Without JavaScript the form is a plain POST to the relay, which answers with
   its own plain confirmation page (or the Stripe redirect).

What the page may read back of a hold (`/status`): reference, trip, dates,
payment line, email. Never the phone numbers or the emergency contact.

## The sums, and where they come from

Nothing is invented. The terms (`terms.html`, section 3) say a deposit is due
with registration and the full balance 120 days before departure, and give no
deposit amount. The India trip page says: "Because both are less than 120 days
away, the full £1,100 is due when you book." So:

- India, both departures: the sum due now is **£1,100**, labelled as the full
  price. The deposit button is live once the relay and Stripe are configured.
- Kenya, both departures: the page says "Enquire for prices" and no deposit is
  stated anywhere, so the sum shows **[to supply]** and the deposit button is
  disabled with a note; the call route works. To take Kenya deposits, set
  `currency`, `due` (minor units) and `due_text` for `kenya-1` and `kenya-2` in
  `DEPARTURES` in `booking-worker.js`, and `due` in `DEPS` in `tools/v4_book.py`.

The balance line the relay writes is the terms' rule applied to the departure
date: 120 days before departure, or, if that day has passed (true of all four
departures today), "due with the booking".

## To configure, in order

1. **Stripe.** A Stripe account for Paragliding Atlas (or Touch The Sky With
   Glory, org. 937116934). From Developers > API keys, the secret key. Enable
   email receipts (Settings > Emails) so Stripe sends the card receipt; the
   relay sets `receipt_email` on every payment.
2. **The Worker.** In a folder with `booking-worker.js`:

   ```toml
   # wrangler.toml
   name = "booking-relay"
   main = "booking-worker.js"
   compatibility_date = "2026-10-01"

   [vars]
   SITE = "https://paraglidingatlas.com"   # where book.html lives; for the prototype, "https://paraglidingatlas.com/prototypes/v4"

   [[kv_namespaces]]
   binding = "BOOKINGS"
   id = "<from: wrangler kv namespace create BOOKINGS>"

   [[send_email]]                            # optional, as enquiry-worker.js
   name = "EMAIL"
   destination_address = "aninder@paraglidingatlas.com"
   ```

   Then the secrets, never in the repo:

   ```
   wrangler secret put MAILERLITE_API_KEY      # MailerLite > Integrations > API > new token
   wrangler secret put STRIPE_SECRET_KEY       # sk_test_... first, sk_live_... when ready
   wrangler secret put STRIPE_WEBHOOK_SECRET   # see step 3
   wrangler deploy
   ```

3. **The webhook.** Stripe > Developers > Webhooks > add endpoint
   `https://<worker-url>/stripe-webhook`, event `checkout.session.completed`
   (and `checkout.session.async_payment_succeeded`). Copy its signing secret
   into `STRIPE_WEBHOOK_SECRET`.
4. **The page.** Paste the Worker URL into `ENDPOINT` in `tools/v4_book.py`,
   run `python3 tools/v4_book.py`. The deposit button lights for India.
5. **MailerLite.** Open each automation, read the email, press Enable. Nothing
   sends until then. The sender address must be verified in MailerLite
   (Settings > Domains); the automations carry the account's default sender.
6. **Test in Stripe test mode** with card 4242 4242 4242 4242: hold a place on
   the prototype page, pay, come back, check the KV entry (`wrangler kv key
   list --binding BOOKINGS`), the MailerLite subscriber and that the
   confirmation arrived. Then switch the key to live.
7. **Switch-over.** `book.html` leaves `PROTO_ONLY`; the India and Kenya
   pages' Hold a place links change from `../enquire.html?trip=...&when=...` to
   `../book.html?trip=...&when=...` (same query, so nothing else moves); the
   menu's "Enquire Now" may become "Hold a Place" as on book.html.

## What only the owner can supply

- The Stripe account and its keys.
- The Kenya deposit amount (and whether India should take a deposit rather than
  the full £1,100 the trip page states).
- How long holds stay in KV. The relay keeps them until deleted; the privacy
  policy promises enquiries are kept up to 24 months, and says nothing yet
  about bookings: [to supply], then add an `expirationTtl` in `putHold`.
- A Kenya welcome kit. The India one is built from the India page and the
  packing PDF; the Kenya page's own packing and know-before-you-go content
  would need the same treatment (the Drive "Know before you go" doc is a
  Kenya draft with cycling-tour text still in it, so it was not used).
- Enabling the automations, after reading them.

## Privacy and security notes

- Card details never touch the relay or the site: Stripe's hosted page only.
- CORS and the Origin check allow only the site's own origins, as the other
  Workers. Rate limit: 8 posts per IP per 10 minutes, counted in KV.
- The Stripe webhook is verified with the signing secret (HMAC SHA-256,
  5-minute tolerance, constant-time compare).
- The MailerLite record carries name, email, phone, country and the booking
  fields; the flying details and the emergency contact stay in KV and the
  owner's email only.
- The consent line on the page says what the details are for; the privacy
  policy should gain a line on bookings (MailerLite as processor, Stripe as
  processor, retention): [to supply].

## The confirmation email (21 Oct, second design)

`tools/email_booking.py` writes `docs/emails/booking-confirmation-india.html` and
`booking-confirmation-kenya.html`, one per trip, in the site's own look: the
departure's photograph with the headline on it, a boarding card (pilot, reference,
departure, payment, balance), the relief map and terrain profile for India, the
owner's note, the next steps as a rail, three photographs from the trip page and
the terms in one line. `tools/email_graphics.py FONTDIR` draws the two India
graphics into `assets/email/` from the terrain data in `tools/data` (FONTDIR holds
DM Mono, Poppins and DM Sans TTFs; the generator does not fetch them).

The India body is loaded into the MailerLite automation "Booking confirmation"
(201934827617781573, trigger India 2026 pilots only) and the Kenya body into
"Booking confirmation: Kenya 2027" (201941373388064170, trigger Kenya 2027 pilots).
Both are disabled. The two `assets/email/` images are referenced at
paraglidingatlas.com and show in real mail only once that folder is pushed to main.

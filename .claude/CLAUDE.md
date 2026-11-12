# Paragliding Atlas: standing notes for every chat

- `assets/email/` holds the owner's email signature images (docs/email-signature.md). Never delete, rename or move
  it, and keep it in any host move: sent emails point at those addresses for good.
- The owner's map of every module and open question: https://claude.ai/artifact/CBTZTQhwDrP8AZswj5PFV5 (private).
  Read it when you start; before you end or hand over, update your box in its database collection "modules".
- Website chats are numbered (15, 16, 17 ...). When your job is done, or the chat has grown long, hand over without
  asking the owner: write the handover at the top of docs/v4-next-session.md, update the map, open the next numbered
  chat yourself with the session tools (create_session), and give the owner its link. Copy this rule into every
  handover so it carries on.
- Video play buttons (owner, 12 Nov 2026): never a round/circle play button on the site. Every video play button is
  the YouTube-style rounded rectangle the owner approved on the galleries (.gff-btn in v4-gallery.css; .md-play in
  v4-media.css matches it): about 16:11, radius ~14px, dark see-through at rest, YouTube red #f00 on hover. Audio
  players (episodes, live show) are not videos and keep their own controls.
- Share links (owner, 12 Nov 2026): every photo and film on the site has a Share button (prototypes/v4/v4-share.js
  and v4-share.css: <button type="button" data-share></button>, optional data-share-url / data-share-title). It
  opens the device's own share sheet, else a panel (Copy link, WhatsApp, Telegram, Email, Facebook, X). Any new
  media you add gets one. Photos share the site link (page#photo-name opens it); films share their YouTube link.

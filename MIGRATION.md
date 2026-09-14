# Moving to paraglidingatlas.com

**Status: prepared and TESTED, not activated. Do not flip anything until DNS is live.**

The switch has been run end to end in a dry run and reverted. First attempt moved
2,304 URLs and left **986 behind**, because canonical and og:url were written by
six generators and by hand in the static pages, not from config. That is fixed:
every generator now reads `site_config.BASE`, and the schema injector normalises
any absolute self-reference it still finds, including on noindex pages. The
second dry run moved **every URL in the site, sitemap.xml, robots.txt and
llms.txt, with zero left behind**, and reverted just as cleanly.

So "change one line and rebuild" is now literally true. It was not before it was
tested, which is the only reason this note exists.

## Why this matters more than anything else on the site

Two searches for this brand, one on the name and one on the exact domain, returned
Podbean, Apple Podcasts, Spotify, Amazon Music, Castbox, Castro, Podcast Republic
and YouTube. **The website appeared in neither.**

Meanwhile the brand's actual identity already lives on `paraglidingatlas.com`: the
email address in every episode description, the Patreon, the address people are
told to write to. The site sits somewhere else entirely, on a shared
`github.io` domain, in a subdirectory.

That split costs three things at once:

1. **Domain authority.** `github.io` is a shared domain. A subdirectory on it
   inherits almost nothing and builds almost nothing.
2. **Entity resolution.** An answer engine works out that a website, a YouTube
   channel and a podcast are one organisation by corroborating signals across
   them. Every external signal points at `paraglidingatlas.com`. The content
   points at `github.io`. The two halves of the brand do not resolve to one
   entity.
3. **Trust.** A visitor who reads an episode description, sees
   `aninder@paraglidingatlas.com`, then lands on `paraglidingatlas-maker.github.io`
   has a small moment of doubt. Those add up.

## What has already been done

- `site_config.py` holds the address in one place. Everything else reads from it.
- `CNAME.example` is ready to become `CNAME`.
- Every canonical, `og:url`, sitemap entry and `llms.txt` link is generated from
  `site_config.BASE`, so they all move together and none can be left behind.

## The switch, in order

**The order below is not the order this file gave before.** GitHub's own docs say
to add the domain in the repository settings BEFORE pointing DNS at it, because
configuring DNS first can let someone else claim a subdomain of it in the window
between. This file had DNS first. Corrected.

1. **Verify the domain first.** Repository (or account) **Settings → Pages →
   Add a domain**. GitHub gives you a `_github-pages-challenge-...` TXT record to
   add at the registrar. This is the step that prevents a takeover, and it is
   optional only in the sense that nothing stops you skipping it.
2. **Add the custom domain in Settings → Pages → Custom domain**, and Save. Do
   this before touching the A records.
3. **DNS at the registrar.** Four A records on the apex `paraglidingatlas.com`:
   `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`.
   Four AAAA records for IPv6: `2606:50c0:8000::153`, `2606:50c0:8001::153`,
   `2606:50c0:8002::153`, `2606:50c0:8003::153`. A CNAME for `www` pointing at
   `paraglidingatlas-maker.github.io`. Remove any default A record the registrar
   put there, and do not use a wildcard record.
4. **`git mv CNAME.example CNAME`** and commit. GitHub Pages reads this file.
   Note that setting the domain in Settings usually writes this file for you, so
   check before committing a second one.
5. **Wait for the certificate**, then tick **Enforce HTTPS**. Up to an hour, and
   occasionally longer. Do not proceed while it still says provisioning.
6. **In `site_config.py`**, set `DOMAIN = "paraglidingatlas.com"` and `PATH = "/"`.
   Those two lines are the whole change.
7. **`./build.sh`**. It fails loudly if sitemap.xml, robots.txt or llms.txt still
   carry a stale address.
8. **`python3 tools/audit.py --drift`** must pass before pushing. It reads the
   base from `site_config` now, so it validates against wherever you just
   pointed the site rather than against a hard-coded address.
9. **Google Search Console and Bing Webmaster Tools**: add the new property and
   submit `sitemap.xml`. Bing matters more than it used to, because ChatGPT
   search leans on its index.

## What the dry run actually found

The claim above that this is a one-line change was tested again, properly, and
it was not true. Flipping `site_config` and rebuilding produced:

- **3 FAILs from `tools/audit.py` itself**, which hard-coded the old address in
  three places including a literal `/Website/` in the sitemap check. The audit
  would have failed step 8 against a site that was entirely correct, and anyone
  following this file would have concluded the site was broken.
- **35 broken links and 2 missing preloads, all in `404.html`.** It uses
  root-absolute paths, correctly, because a 404 is served for any URL at any
  depth and a relative path would resolve differently depending how deep the
  missing URL was. But nothing rewrote them, so they all still said `/Website/`.
- **Five generators and two templates** still writing the old address into pages
  and being rescued only because the schema injector runs afterwards and
  normalises them. Fragile, and invisible until the injector missed one.

All fixed. `404.html` is now generated from `templates/404-template.html` by
`tools/generate_404.py`, the audit reads `site_config`, and the generators and
templates take the base from config. Re-run end to end after the fixes:
**0 FAIL, 0 occurrences of the old address, 0 root-absolute `/Website/` paths**,
and reverting is equally clean.

## The one thing that will go wrong if rushed

GitHub Pages serves the old `github.io/Website/` URLs as redirects after a custom
domain is set, which is fine for humans. It is less fine for AI retrieval
crawlers: several of them will drop a page from a generated answer rather than
follow an extra hop. So the canonical switch in step 4 is not optional tidying,
it is the step that makes the move actually work. Do steps 1 to 6 in one sitting.

## What not to do

Do not set the custom domain and leave `site_config.py` pointing at github.io.
The site would then advertise canonicals on a domain it no longer serves from,
which is worse than either address on its own.

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

1. **DNS.** Point the apex `paraglidingatlas.com` at GitHub Pages with four A
   records: `185.199.108.153`, `185.199.109.153`, `185.199.110.153`,
   `185.199.111.153`. Add a CNAME for `www` pointing at
   `paraglidingatlas-maker.github.io`. Verify propagation before continuing.
2. **`git mv CNAME.example CNAME`** and commit. GitHub Pages reads this file.
3. **Repository settings → Pages → Custom domain**, then tick **Enforce HTTPS**
   once the certificate has issued. This can take up to an hour. Do not proceed
   while it is still provisioning.
4. **In `site_config.py`**, set `DOMAIN = "paraglidingatlas.com"` and `PATH = "/"`.
   Those two lines are the whole change. Nothing else needs editing.
5. **`./build.sh`**. It fails loudly if sitemap.xml, robots.txt or llms.txt still
   carry a stale address, so a partial move cannot ship quietly.
6. **`python3 tools/audit.py --drift`** must pass before pushing.
7. **Google Search Console and Bing Webmaster Tools**: add the new property,
   submit `sitemap.xml`. Bing matters more than it used to, because ChatGPT
   search leans on its index.

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

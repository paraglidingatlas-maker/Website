#!/usr/bin/env python3
"""One place for the things every generator needs to agree on.

WHY THIS EXISTS
Five generators each hard-coded the base URL. That was survivable while the site
lived at one address. It stops being survivable the moment the site moves to
paraglidingatlas.com, which is the domain the brand already uses for email, for
Patreon and across every podcast directory. Moving is a one-line change here.

DO NOT flip BASE to the custom domain until the DNS is actually pointed and the
CNAME file is committed. Canonicals pointing at a domain that does not resolve
are far worse than canonicals pointing at a github.io subpath.
"""

# ---------------------------------------------------------------- address ----
# Switch these two together, and only when DNS is live. See MIGRATION.md.
DOMAIN = "paraglidingatlas-maker.github.io"
PATH = "/Website/"
BASE = "https://%s%s" % (DOMAIN, PATH)

# ----------------------------------------------------------------- entity ----
# Every place this brand demonstrably exists. These become sameAs, which is how
# an answer engine works out that the website, the YouTube channel and the Apple
# podcast are one organisation rather than three unrelated things. Without it a
# brand can be well known and still be unrecognised as an entity.
ORG_NAME = "Paragliding Atlas"
ORG_LEGAL = "Paragliding Atlas"
ORG_ID = BASE + "#organization"
SITE_ID = BASE + "#website"
ORG_NUMBER = "937116934"
ORG_EMAIL = "aninder@paraglidingatlas.com"
ORG_ADDRESS = {
    "streetAddress": "Olav Troviks Vei M 46",
    "addressLocality": "Oslo",
    "addressCountry": "NO",
}
FOUNDER = "Aninder Singh"

SAME_AS = [
    "https://www.youtube.com/@ParaglidingAtlas",
    "https://podcasts.apple.com/us/podcast/paragliding-atlas-by-aninder-singh/id1735782803",
    "https://open.spotify.com/show/16jBM3RfjVERukNHJrIRec",
    "https://www.patreon.com/cw/ParaglidingAtlas",
    "https://www.instagram.com/anindersingh13",
    "https://castbox.fm/channel/Paragliding-Atlas-by-Aninder-Singh-id6075445",
    "https://www.podbean.com/podcast-detail/tb6yq-2f5cd4/Paragliding-Atlas-by-Aninder-Singh-Podcast",
]

RSS = "https://anchor.fm/s/ed1344d8/podcast/rss"

DESCRIPTION = ("A talk show on the art and science of free flight. Honest conversations with "
               "designers, test pilots, instructors and record holders, published in full with "
               "transcripts, alongside small guided paragliding trips.")


def url(path=""):
    """Absolute URL for a repo-relative path."""
    return BASE + path.lstrip("/")


def organization():
    return {
        "@type": "Organization",
        "@id": ORG_ID,
        "name": ORG_NAME,
        "url": BASE,
        "description": DESCRIPTION,
        "email": ORG_EMAIL,
        "logo": {"@type": "ImageObject", "url": url("assets/logo/atlas-logo-white.png")},
        "founder": {"@type": "Person", "name": FOUNDER},
        "address": dict({"@type": "PostalAddress"}, **ORG_ADDRESS),
        "identifier": ORG_NUMBER,
        "sameAs": SAME_AS,
    }


def website():
    return {
        "@type": "WebSite",
        "@id": SITE_ID,
        "name": ORG_NAME,
        "url": BASE,
        "description": DESCRIPTION,
        "inLanguage": "en",
        "publisher": {"@id": ORG_ID},
    }

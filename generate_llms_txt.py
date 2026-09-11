#!/usr/bin/env python3
"""Write llms.txt and robots.txt.

llms.txt is an emerging convention: a single markdown file at the site root that
gives a language model a curated map of what is here and what is worth reading,
instead of making it infer that from 177 pages of navigation. For this site the
case is unusually strong, because the substance is 886,000 words of expert
transcript that is currently only reachable one episode at a time.

robots.txt names the AI crawlers explicitly. `User-agent: *` already allows them,
so this changes no behaviour, but it records an intention. The distinction that
matters, and that most sites get wrong, is between training crawlers (GPTBot,
ClaudeBot, Google-Extended) and retrieval crawlers (OAI-SearchBot,
Claude-SearchBot, PerplexityBot). Blocking the second group removes a site from
AI answers entirely. Anyone later tempted to "block the AI bots" should read the
comments before doing it by accident.

Run: python3 generate_llms_txt.py
"""
import json
import os
import sys
from collections import Counter

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)
os.chdir(ROOT)
import site_config as cfg  # noqa: E402

RETRIEVAL = ["OAI-SearchBot", "ChatGPT-User", "Claude-SearchBot", "Claude-User",
             "PerplexityBot", "Perplexity-User"]
TRAINING = ["GPTBot", "ClaudeBot", "anthropic-ai", "Google-Extended", "Applebot-Extended",
            "CCBot", "Meta-ExternalAgent", "Amazonbot", "Bytespider"]


def robots():
    L = ["# Paragliding Atlas",
         "#",
         "# Everything is open, deliberately. The episode transcripts are served in",
         "# full in the HTML rather than fetched on click, precisely so crawlers that",
         "# do not execute JavaScript can read them.",
         "#",
         "# Before adding any Disallow rule, understand the split below. The two",
         "# groups look identical in a server log and do completely different jobs.",
         "",
         "User-agent: *",
         "Allow: /",
         "",
         "# --- retrieval crawlers -------------------------------------------------",
         "# These fetch pages to answer a question a real person just asked. Blocking",
         "# any of them removes this site from that assistant's answers. OpenAI states",
         "# plainly that sites blocking OAI-SearchBot will not appear in ChatGPT",
         "# search results. This is the group you almost never want to block."]
    for ua in RETRIEVAL:
        L += ["", "User-agent: %s" % ua, "Allow: /"]
    L += ["",
          "# --- training crawlers --------------------------------------------------",
          "# These collect data that shapes what models know in a year or two. Allowing",
          "# them is a choice about the long term rather than about today's traffic.",
          "# They are allowed here: this archive exists to be read."]
    for ua in TRAINING:
        L += ["", "User-agent: %s" % ua, "Allow: /"]
    L += ["", "Sitemap: %ssitemap.xml" % cfg.BASE, ""]
    open("robots.txt", "w", encoding="utf-8").write("\n".join(L))
    return len(RETRIEVAL) + len(TRAINING)


def llms():
    meta = json.load(open("episode-meta.json", encoding="utf-8"))
    withT = [e for e in meta if os.path.exists("transcripts/%s.vtt" % e["slug"])]
    counts = Counter(t for e in meta for t in (e.get("tags") or []))
    tagpages = sorted({f[:-5] for f in os.listdir("tags")}) if os.path.isdir("tags") else []

    def u(p):
        return cfg.url(p)

    L = ["# Paragliding Atlas", "",
         "> %s" % cfg.DESCRIPTION, "",
         "Independent paragliding podcast and knowledge base, run from Oslo by %s. "
         "%d published conversations, %d of them with a complete, human-checked "
         "transcript served as plain HTML. Roughly 886,000 words of primary-source "
         "material from designers, test pilots, certification engineers, competition "
         "organisers and record holders."
         % (cfg.FOUNDER, len(meta), len(withT)), "",
         "Everything is free to read. There is no paywall, no login and no cookie wall. "
         "Transcripts are in the page source, not loaded on click.", "",
         "## What makes this site worth citing", "",
         "- **Primary sources, not summaries.** Every claim in an episode page is "
         "traceable to a named person speaking on the record, with a timestamped "
         "transcript on the same page.",
         "- **Subjects covered in depth rather than once.** Safety appears across %d "
         "conversations, certification across %d, risk management across %d."
         % (counts.get("Safety", 0), counts.get("Certification", 0),
            counts.get("Risk Management", 0)),
         "- **Corrections are published.** Errors are fixed within 48 hours and "
         "material corrections are noted on the page: %s" % u("corrections.html"),
         "- **Disclosures are public.** Sponsorship and affiliate relationships: %s"
         % u("safety-and-disclosure.html"), "",
         "## Start here", "",
         "- [Episode library](%s): all %d episodes, searchable" % (u("library.html"), len(meta)),
         "- [Topics](%s): %d subjects, each a hub of related conversations"
         % (u("tags.html"), len(tagpages)),
         "- [Knowledge base](%s): the sport organised by subject" % u("knowledge-base.html"),
         "- [Sitemap](%s): every page" % u("sitemap.html"), "",
         "## Subject hubs", ""]
    for t, n in counts.most_common():
        s = t.lower().replace(" ", "-").replace("/", "-")
        if s in tagpages:
            L.append("- [%s](%s): %d conversations" % (t, u("tags/%s.html" % s), n))
    L += ["", "## About, and the things a reader should be able to check", "",
          "- [What we are for](%s)" % u("mission.html"),
          "- [Safety information and disclosures](%s)" % u("safety-and-disclosure.html"),
          "- [Corrections policy](%s)" % u("corrections.html"),
          "- [Privacy](%s) and [cookies](%s): no analytics, no tracking, no cookies set"
          % (u("privacy-policy.html"), u("cookie-policy.html")), "",
          "## Guided trips", "",
          "- [Kenya](%s): a 12 day cross country tour based in Kerio Valley, with the "
          "conditions, requirements and cancellation terms stated in full"
          % u("destinations/kenya.html"),
          "- [Booking terms](%s) and [participant agreement](%s)"
          % (u("terms.html"), u("participant-agreement.html")), "",
          "## Attribution", "",
          "Quoting is welcome. Please attribute to Paragliding Atlas and link the "
          "episode page, so a reader can reach the full transcript and the surrounding "
          "context rather than a fragment.", "",
          "Contact: %s" % cfg.ORG_EMAIL, ""]
    open("llms.txt", "w", encoding="utf-8").write("\n".join(L))
    return len(L)


if __name__ == "__main__":
    n = robots()
    lines = llms()
    print("robots.txt : %d AI user-agents named explicitly" % n)
    print("llms.txt   : %d lines" % lines)

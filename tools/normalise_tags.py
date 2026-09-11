#!/usr/bin/env python3
"""Collapse the raw keyword lists into one controlled vocabulary.

The spreadsheet's keywords were written per episode, so the same idea arrives in
several spellings: two-liner, two-liners, two-line glider, two-liner wings,
two-liner gliders. Left alone that produces five tag pages each holding one
episode, which is worse than no tags at all: thin pages, split link equity, and
navigation that leads nowhere.

SYNONYMS below is the editorial part. Everything after it is mechanical.
Run: python3 tools/normalise_tags.py [--write]
"""
import json
import os
import re
import sys
from collections import Counter, defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# canonical display name -> every raw spelling that should fold into it
SYNONYMS = {
    "Two Liners": ["two-liner", "two-liners", "two liner", "two-line glider", "two line glider",
                   "two-liner wings", "two-liner gliders", "two-liner safety", "two-line gliders"],
    "Safety": ["safety", "paragliding safety", "flight safety", "flight incidents"],
    "Safety Training": ["safety training", "safety pilot coaching", "emergency procedures"],
    "Competition": ["competition", "competition flying", "competitive paragliding", "competition pilots",
                    "competitions", "racing", "comp"],
    "World Cup": ["world cup", "pwca", "super final", "fai"],
    "Certification": ["certification", "certification norms", "homologation", "en/dhv categories",
                      "en966", "wg6", "test house", "en ratings"],
    "Cross Country": ["cross-country", "cross country", "cross-country flying", "xc", "distance"],
    "Collapses": ["collapse", "collapses", "collapse behavior", "collapse prevention",
                  "collapse stability", "asymmetrics"],
    "Reserves": ["reserve", "reserves", "reserve parachute", "reserve deployment", "steerable reserve",
                 "round reserve"],
    "Harnesses": ["harness", "harnesses", "acro harness"],
    "SIV": ["siv", "siv training"],
    "Acro": ["acro", "acro flying", "acro paragliding"],
    "Hike and Fly": ["hike and fly", "hiking and flying", "hike & fly"],
    "X-Alps": ["x-alps", "xalps"],
    "Vol Biv": ["vol-biv", "vol biv", "bivvy flying"],
    "Risk Management": ["risk management", "risk vs reward", "risk-taking", "risk aversion", "risk"],
    "Wing Design": ["design", "paraglider design", "wing design", "aerodynamics", "profile design",
                    "arc", "winglets"],
    "Innovation": ["innovation", "innovation in aviation", "new technologies", "paragliding innovation",
                   "technology", "paragliding future"],
    "Weather": ["weather forecasting", "meteorology", "weather conditions", "models", "thermals",
                "wind shear", "dust devil"],
    "Mental Game": ["mental game", "mental clarity", "mindset", "mind", "psychology", "self-confidence",
                    "mental approach", "mental preparation", "flow state", "mindfulness"],
    "Fear": ["fear"],
    "Training": ["training", "progression", "instructor", "instruction", "instructor ethics",
                 "ground handling", "wing control", "maneuvers"],
    "Mentorship": ["mentorship", "mentors", "support system"],
    "Adventure": ["adventure", "adventure flying", "adventure travel", "expedition", "exploration"],
    "Storytelling": ["storytelling", "narrative", "filmmaking", "videography", "content creation",
                     "filming"],
    "Himalayas": ["himalayas", "karakorams", "karakoram", "bir", "bir billing", "8000ers"],
    "Equipment": ["paragliding equipment", "equipment maintenance", "equipment evolution", "gear"],
    "Materials": ["fabric technology", "lightweight fabrics", "line materials", "material fatigue",
                  "carabiners", "microscopic cracks", "corrosion", "dynamic loads"],
    "Impact Protection": ["koroyd", "orikami", "impact protection", "helmet safety", "helmet",
                          "full-face helmet", "visor"],
    "Governance": ["governance", "civl", "institution", "accountability", "standardization",
                   "licenses", "pilot advocacy", "resignation", "transparency", "proxy voting"],
    "Accidents": ["accident", "accidents", "mid-air collisions", "death", "close calls", "fatalities"],
    "Manufacturing": ["manufacturing", "r&d", "r & d", "brand partnerships", "manufacturer accountability"],
    "Physiology": ["physiology", "hypoxia", "oxygen", "hydration", "fatigue", "g-forces", "g-force",
                   "cortisol", "nutrition", "acclimatization", "altitude"],
    "Speed Flying": ["speed flying"],
    "Parakites": ["parakites", "kite risers", "dune rider", "flare system", "moustache wing"],
    "Kenya": ["kenya", "africa", "ethiopia"],
    "India": ["india", "panchgani"],
    "Community": ["community", "paragliding community", "community growth", "culture",
                  "paragliding culture", "social media"],
}

RAW_TO_CANON = {}
for canon, raws in SYNONYMS.items():
    for r in raws:
        RAW_TO_CANON[r] = canon


def titlecase(t):
    small = {"and", "or", "the", "of", "vs", "a", "in", "to"}
    words = re.split(r"[\s_]+", t.strip())
    out = []
    for i, w in enumerate(words):
        if w.lower() in small and i:
            out.append(w.lower())
        elif w.isupper() and len(w) <= 4:
            out.append(w)
        else:
            out.append(w[:1].upper() + w[1:])
    return " ".join(out)


def canonical(raw):
    r = re.sub(r"\s+", " ", raw.strip().lower())
    if not r:
        return None
    if r in RAW_TO_CANON:
        return RAW_TO_CANON[r]
    # simple plural fold so "wings" and "wing" do not both survive
    if r.endswith("s") and r[:-1] in RAW_TO_CANON:
        return RAW_TO_CANON[r[:-1]]
    return titlecase(r)


def slug(name):
    return re.sub(r"-+", "-", re.sub(r"[^a-z0-9]+", "-", name.lower())).strip("-")


def main():
    meta = json.load(open(os.path.join(ROOT, "episode-meta.json"), encoding="utf-8"))
    before = Counter(t.strip().lower() for e in meta for t in (e.get("tags") or []))
    counts = Counter()
    for e in meta:
        seen, out = set(), []
        for raw in (e.get("tags") or []):
            c = canonical(raw)
            if c and c.lower() not in seen:
                seen.add(c.lower())
                out.append(c)
        e["tags"] = out
        counts.update(out)
    print("raw distinct tags   : %d" % len(before))
    print("canonical tags      : %d" % len(counts))
    print("tags on 2+ episodes : %d   (these get a page)"
          % sum(1 for _, n in counts.items() if n >= 2))
    print("tags on 1 episode   : %d   (rendered as plain text)"
          % sum(1 for _, n in counts.items() if n == 1))
    print("\ntop 25:")
    for t, n in counts.most_common(25):
        print("   %-22s %3d   /tags/%s.html" % (t, n, slug(t)))
    if "--write" in sys.argv:
        json.dump(meta, open(os.path.join(ROOT, "episode-meta.json"), "w", encoding="utf-8"),
                  ensure_ascii=False, indent=2)
        print("\nwritten to episode-meta.json")


if __name__ == "__main__":
    main()

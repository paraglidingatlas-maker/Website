"""Fetch an SRS event's final tables (Sports, Female, Team) from api.airtribune.com and save them as JSON for the
comp gallery's podium and race chart (chat 25, 17 Nov 2026). Usage: python3 tools/srs_results.py MEET OUT.json
Tapalpa: meet 93 -> tools/data/tapalpa-results.json. Names stay exactly as SRS writes them (SURNAME in capitals);
the gallery turns them into display names."""
import html, json, re, sys, urllib.request

API = "https://api.airtribune.com/srs/scores/?meet=%s&type=%d"


def num(x):
    """a score; SRS writes "-" for a task not flown (0 points)"""
    try:
        return float(x)
    except ValueError:
        return 0.0


def rows(meet, t):
    s = urllib.request.urlopen(API % (meet, t), timeout=60).read().decode()
    for r in re.findall(r"<tr[^>]*>(.*?)</tr>", s, re.S):
        yield [html.unescape(re.sub("<[^>]*>", "", x)).strip() for x in re.findall(r"<t[dh][^>]*>(.*?)</t[dh]>", r, re.S)]


def pilots(meet, t):
    out, tasks = [], []
    for c in rows(meet, t):
        if c[:2] == ["Rank", "ID"]:
            tasks = c[6:-1]
        elif len(c) == 12 and c[0].isdigit():
            out.append(dict(rank=int(c[0]), name=c[2], nat=c[3], glider=c[4], scores=[num(x) for x in c[6:11]], total=num(c[11])))
    return tasks, out


def teams(meet):
    out = []
    for c in rows(meet, 61):
        if len(c) == 9 and c[0].isdigit():
            out.append(dict(rank=int(c[0]), name=c[2], scores=[num(x) for x in c[3:8]], total=num(c[8]), members=[]))
        elif len(c) == 12 and not c[0] and c[1] and out:
            out[-1]["members"].append(c[2])
    return out


if __name__ == "__main__":
    meet, dst = sys.argv[1], sys.argv[2]
    tasks, sports = pilots(meet, 56)
    _, female = pilots(meet, 57)
    json.dump(dict(source=API.split("?")[0] + "?meet=" + meet, tasks=tasks, overall=sports, women=female, teams=teams(meet)),
              open(dst, "w"), ensure_ascii=False, indent=0)
    print("wrote", dst, len(sports), "pilots,", len(female), "women,", "teams")

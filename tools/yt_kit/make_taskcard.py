"""The task card, from srs.live's announcement (chat 21, 9 Nov 2026).

    python3 make_taskcard.py N "Mon 9 Nov" "59.9 km" "Triangle in the flats" "Window 10:30" "Start 12:15"

Writes out/taskN/boards/TaskN_Card_Task.png (3840x2160, transparent) and a preview. Only what SRS announced.
"""
import asyncio, os, sys
import make_day as D


def body(n, date, dist, kind, *lines):
    s = "".join("<span>%s</span>" % D.E(x) for x in lines)
    return ('<div class="win"><div class="k">Tapalpa &middot; Task %d &middot; %s</div><div class="n">%s</div>'
            '<div class="s"><span><b>%s</b></span>%s</div></div>%s' % (n, D.E(date), D.E(dist), D.E(kind), s, D.LOCK))


if __name__ == "__main__":
    n = int(sys.argv[1])
    asyncio.run(D.render(n, {"Card_Task": body(n, *sys.argv[2:])}))

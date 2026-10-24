# contact sheet: python3 -I sheet.py SRC_DIR OUT_PREFIX [per_sheet]
import sys, os
from PIL import Image, ImageDraw, ImageOps
src, out = sys.argv[1], sys.argv[2]
n = int(sys.argv[3]) if len(sys.argv) > 3 else 12
fs = sorted(f for f in os.listdir(src) if f.lower().endswith(('.jpg','.jpeg','.png')))
W, H, C = 520, 360, 3
for s in range(0, len(fs), n):
    grp = fs[s:s+n]; rows = (len(grp)+C-1)//C
    sh = Image.new('RGB', (C*W, rows*(H+24)), 'white'); d = ImageDraw.Draw(sh)
    for i, f in enumerate(grp):
        im = ImageOps.exif_transpose(Image.open(os.path.join(src, f))).convert('RGB')
        sz = im.size; im.thumbnail((W-8, H-8))
        x, y = (i%C)*W, (i//C)*(H+24)
        sh.paste(im, (x+4+(W-8-im.width)//2, y+4+(H-8-im.height)//2))
        d.text((x+6, y+H+4), f"{f} {sz[0]}x{sz[1]}", fill='black')
    p = f"{out}-{s//n+1:02d}.jpg"; sh.save(p, quality=80); print(p)

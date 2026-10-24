# From the detected segments to the photo's own lineset: keep segments whose line runs through the risers,
# group them into lines, follow each from the risers to the wing, and take its brightness from the photo.
import os
import cv2, numpy as np, math, sys, json
S=os.environ['SCRATCH']+'/'
cfg=json.loads(sys.argv[1]); name=cfg['name']
g=cv2.imread(S+f'k3/{name}-graded.png'); m=cv2.imread(S+f'k3/{name}-mask.png',0)
H,W=m.shape
segs=json.load(open(S+f'k3/{name}-segs.json'))
lum=cv2.cvtColor(g,cv2.COLOR_BGR2GRAY).astype(np.float32)
kk=cfg.get('kern',7); k=cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(kk,kk))
br=lum-cv2.morphologyEx(lum,cv2.MORPH_OPEN,k)
if cfg.get('pol','bright')=='dark': br=cv2.morphologyEx(lum,cv2.MORPH_CLOSE,k)-lum
glid=(m>60)
C=np.array(cfg['C'],float)
lines=[]
for x1,y1,x2,y2 in segs:
    p=np.array([x1,y1],float); q=np.array([x2,y2],float); d=(q-p)/np.linalg.norm(q-p)
    perp=abs((C-p)[0]*d[1]-(C-p)[1]*d[0])
    if perp>cfg.get('perp',30): continue
    if np.linalg.norm(p-C)>np.linalg.norm(q-C): p,q=q,p
    # stop if the glider lies between the risers and this segment (it would be a line seen past the wing)
    n=int(np.linalg.norm(p-C)); blocked=False
    for t in range(cfg.get('rmin',150),n,4):
        u=C+(p-C)*t/n
        if glid[int(u[1]),int(u[0])]: blocked=True; break
    if blocked: continue
    ang=math.degrees(math.atan2(q[1]-C[1],q[0]-C[0]))
    lines.append((ang,p,q))
lines.sort(key=lambda a:a[0])
groups=[]
for a in lines:
    if groups and a[0]-groups[-1][-1][0]<cfg.get('merge',0.35): groups[-1].append(a)
    else: groups.append([a])
print(len(lines),'segments ->',len(groups),'lines')
geom=np.zeros((H,W),np.float32)
SC=4
big=np.zeros((H,W),np.uint8)
for gr in groups:
    pts=np.vstack([np.vstack([p,q]) for _,p,q in gr])
    vx,vy,x0,y0=cv2.fitLine(pts.astype(np.float32),cv2.DIST_L2,0,0.01,0.01).ravel()
    d=np.array([vx,vy]); o=np.array([x0,y0])
    if (o-C)@d<0: d=-d
    t0=(C-o)@d + cfg.get('start',60)     # just past the risers
    t=t0; last=None
    while True:
        u=o+d*t
        if not(0<=u[0]<W-1 and 0<=u[1]<H-1): break
        if glid[int(u[1]),int(u[0])] and t>t0+40: last=u; break
        t+=2
    if last is None: continue
    a=o+d*t0
    cv2.line(big,(int(a[0]*16),int(a[1]*16)),(int(last[0]*16),int(last[1]*16)),255,cfg.get("w",2),cv2.LINE_AA,shift=4)
geom=big.astype(np.float32)/255
alpha=geom*np.clip(cfg.get('floor',0.45)+br/cfg.get('k',14.0),0,1)
alpha[glid]=0
cv2.imwrite(S+f'k3/{name}-lines.png',np.clip(alpha*255,0,255).astype(np.uint8))
sel=(geom>0.5)&(br>cfg.get('thr',6))
col=np.median(g[sel],axis=0) if sel.sum()>20 else np.array([200,200,200])
print('line colour (bgr)',col)
json.dump(col.tolist(),open(S+f'k3/{name}-linecol.json','w'))
x0,y0,x1,y1=cfg['view']
c=g[y0:y1,x0:x1].astype(np.float32)*0.55
a=alpha[y0:y1,x0:x1,None]; c=c*(1-a)+np.array([60,60,255])*a
cv2.imwrite(S+f'look/{name}-lineset.jpg',cv2.resize(c,None,fx=cfg.get('vs',0.6),fy=cfg.get('vs',0.6),interpolation=cv2.INTER_AREA).astype(np.uint8),[cv2.IMWRITE_JPEG_QUALITY,88])

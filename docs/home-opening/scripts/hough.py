# Find the real lines as long straight segments that point back at the risers.
import os
import cv2, numpy as np, math, sys, json
S=os.environ['SCRATCH']+'/'
cfg=json.loads(sys.argv[1]); name=cfg['name']
g=cv2.imread(S+f'k3/{name}-graded.png'); m=cv2.imread(S+f'k3/{name}-mask.png',0)
lum=cv2.cvtColor(g,cv2.COLOR_BGR2GRAY).astype(np.float32)
kk=cfg.get('kern',7); k=cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(kk,kk))
br=lum-cv2.morphologyEx(lum,cv2.MORPH_OPEN,k)
dk=cv2.morphologyEx(lum,cv2.MORPH_CLOSE,k)-lum
resp=br if cfg.get('pol','bright')=='bright' else dk
x0,y0,x1,y1=cfg['view']
excl=cv2.dilate((m>40).astype(np.uint8),np.ones((9,9)))
sub=resp[y0:y1,x0:x1]
b=((sub>cfg.get('thr',5))&(excl[y0:y1,x0:x1]==0)).astype(np.uint8)*255
segs=cv2.HoughLinesP(b,1,np.pi/3600,cfg.get('votes',80),minLineLength=cfg.get('minlen',250),maxLineGap=cfg.get('gap',30))
keep=[]
C=np.array(cfg['C'],float)-[x0,y0]
for x1_,y1_,x2_,y2_ in (segs.reshape(-1,4) if segs is not None else []):
    mid=np.array([(x1_+x2_)/2,(y1_+y2_)/2]); d=np.array([x2_-x1_,y2_-y1_],float); r=mid-C
    if r[1]>0: continue
    am=math.degrees(math.atan2(r[1],r[0]))
    if not(cfg.get('amin',-180)<=am<=cfg.get('amax',0)): continue
    ang=abs(math.degrees(math.atan2(d[0]*r[1]-d[1]*r[0],d@r))); ang=min(ang,180-ang)
    if ang<cfg.get('tol',2.0): keep.append([int(x1_+x0),int(y1_+y0),int(x2_+x0),int(y2_+y0)])
print(0 if segs is None else len(segs),len(keep))
json.dump(keep,open(S+f'k3/{name}-segs.json','w'))
vis=np.clip(g[y0:y1,x0:x1].astype(np.float32)*1.6,0,255).astype(np.uint8)
for a,b_,c,d in keep: cv2.line(vis,(a-x0,b_-y0),(c-x0,d-y0),(0,0,255),2)
cv2.imwrite(S+f'look/{name}-segs.jpg',cv2.resize(vis,None,fx=cfg.get('vs',0.6),fy=cfg.get('vs',0.6),interpolation=cv2.INTER_AREA),[cv2.IMWRITE_JPEG_QUALITY,88])

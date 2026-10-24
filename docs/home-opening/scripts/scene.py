# One Kenya scene for F from a graded photo: the ground with the gliders taken out (filled from nearby
# ground of the same photo), the gliders cut out with their real lines, their soft shadow, and a depth map.
import os
import cv2, numpy as np, json, sys
import onnxruntime as ort
S=os.environ['SCRATCH']+'/'
cfg=json.loads(sys.argv[1]); name=cfg['name']; tag=cfg['tag']; out=S+'k3/out/'
import os; os.makedirs(out,exist_ok=True)
g=cv2.imread(S+f'k3/{name}-graded.png'); H,W=g.shape[:2]
m=cv2.imread(S+f'k3/{name}-mask.png',0).astype(np.float32)/255
la=cv2.imread(S+f'k3/{name}-lines.png',0)
la=np.zeros_like(m) if la is None or cfg.get('nolines') else la.astype(np.float32)/255
# ---- the gliders, with their lines ----
A=np.maximum(m,la)
ys,xs=np.nonzero(A>0.03); x0,x1,y0,y1=xs.min(),xs.max(),ys.min(),ys.max()
mg=int(0.02*max(x1-x0,y1-y0)); x0-=mg; y0-=mg; x1+=mg; y1+=mg
col=np.array(json.load(open(S+f'k3/{name}-linecol.json'))) if os.path.exists(S+f'k3/{name}-linecol.json') else np.array([200,200,200])
lc=np.array(cfg.get('linecol',col.tolist()),np.float32)
rgb=g.astype(np.float32).copy()
use_line=(la>m)
rgb[use_line]=lc
crop=np.dstack([rgb[y0:y1,x0:x1],A[y0:y1,x0:x1]*255])
cw=cfg.get('wingw',1000); s=cw/crop.shape[1]
wing=cv2.resize(crop,(cw,int(round(crop.shape[0]*s))),interpolation=cv2.INTER_AREA)
wing=np.clip(wing,0,255).astype(np.uint8)
cv2.imwrite(out+f'kenya-{tag}-wing.png',wing)
wh,ww=wing.shape[:2]
# ---- the shadow: the silhouette, padded, soft, at a third ----
pad=cfg.get('pad',0.06); pw,ph=int(ww*pad),int(wh*pad)
sh=np.zeros((wh+2*ph,ww+2*pw),np.float32); sh[ph:ph+wh,pw:pw+ww]=wing[...,3]/255.
sh=cv2.resize(sh,(sh.shape[1]//3,sh.shape[0]//3),interpolation=cv2.INTER_AREA)
sh=cv2.GaussianBlur(sh,(0,0),max(2,sh.shape[1]/90))
cv2.imwrite(out+f'kenya-{tag}-shadow.png',np.clip(sh/max(sh.max(),1e-3)*255,0,255).astype(np.uint8))
# ---- the ground: gliders out, filled from the same photo ----
GW=cfg.get('groundw',2000); gs=GW/W; GH=int(round(H*gs))
G=cv2.resize(g,(GW,GH),interpolation=cv2.INTER_AREA).astype(np.float32)
hole=cv2.resize((A>0.005).astype(np.uint8)*255,(GW,GH),interpolation=cv2.INTER_AREA)>0
hole=cv2.dilate(hole.astype(np.uint8),np.ones((15,15)))>0
n,lab,stats,_=cv2.connectedComponentsWithStats(hole.astype(np.uint8))
allhole=hole.copy()
# the light: a smooth fill of the hole (so the brightness runs on across it)
q=4; small=cv2.resize(G.astype(np.uint8),(GW//q,GH//q),interpolation=cv2.INTER_AREA)
hs=(cv2.resize(hole.astype(np.uint8),(GW//q,GH//q),interpolation=cv2.INTER_AREA)>0).astype(np.uint8)
L_=cfg.get('lfd',21); hs=cv2.dilate(hs,np.ones((L_,L_)))
lf=cv2.resize(cv2.inpaint(small,hs,9,cv2.INPAINT_TELEA),(GW,GH),interpolation=cv2.INTER_CUBIC).astype(np.float32)
lf=cv2.GaussianBlur(lf,(0,0),10)
def low(x): return cv2.GaussianBlur(x,(0,0),10)
# the texture: tile by tile, each from the clean ground nearby that looks most like its surroundings
T=64; st=32; win=np.outer(np.hanning(T),np.hanning(T)).astype(np.float32)+1e-3
acc=np.zeros_like(G); wsum=np.zeros((GH,GW),np.float32)
texall=G-low(G)
clean=~cv2.dilate(allhole.astype(np.uint8),np.ones((9,9))).astype(bool)
ys_,xs_=np.nonzero(allhole); hy0,hy1,hx0,hx1=ys_.min(),ys_.max(),xs_.min(),xs_.max()
nt=0
for ty in range(max(0,hy0-T//2),min(GH-T,hy1+T//2)+1,st):
    for tx in range(max(0,hx0-T//2),min(GW-T,hx1+T//2)+1,st):
        if not allhole[ty:ty+T,tx:tx+T].any(): continue
        y0_,y1_,x0_,x1_=max(0,ty-T),min(GH,ty+2*T),max(0,tx-T),min(GW,tx+2*T)
        nb=clean[y0_:y1_,x0_:x1_]
        if nb.sum()<50: nb=np.ones_like(nb)
        tgt=lf[ty:ty+T,tx:tx+T].reshape(-1,3).mean(0)
        tstd=texall[y0_:y1_,x0_:x1_][nb].std(0)
        best=None
        for r in (2,3,4,6,8):
            for k in range(16):
                an=k*np.pi/8; sx=int(tx+np.cos(an)*r*T); sy=int(ty+np.sin(an)*r*T)
                if not(0<=sx<=GW-T and 0<=sy<=GH-T): continue
                if not clean[sy:sy+T,sx:sx+T].all(): continue
                sp=G[sy:sy+T,sx:sx+T].reshape(-1,3)
                e=((sp.mean(0)-tgt)**2).sum()+3*((texall[sy:sy+T,sx:sx+T].reshape(-1,3).std(0)-tstd)**2).sum()+0.5*r
                if best is None or e<best[0]: best=(e,sx,sy)
            if best is not None and r>=4: break
        if best is None: continue
        _,sx,sy=best
        acc[ty:ty+T,tx:tx+T]+=(lf[ty:ty+T,tx:tx+T]+texall[sy:sy+T,sx:sx+T])*win[...,None]
        wsum[ty:ty+T,tx:tx+T]+=win; nt+=1
fill=np.where(wsum[...,None]>0,acc/np.maximum(wsum,1e-6)[...,None],lf)
wgt=cv2.GaussianBlur(cv2.dilate(allhole.astype(np.uint8),np.ones((9,9))).astype(np.float32),(0,0),4)
wgt=np.maximum(wgt,allhole.astype(np.float32))[...,None]
G=G*(1-wgt)+fill*wgt
print('filled with',nt,'tiles')
G=np.clip(G,0,255).astype(np.uint8)
cv2.imwrite(out+f'kenya-{tag}-ground.png',G)
# ---- the depth map (near is light) ----
sess=ort.InferenceSession(S+'models/depth_anything_v2_vits.onnx')
x=cv2.resize(cv2.cvtColor(G,cv2.COLOR_BGR2RGB),(518,518),interpolation=cv2.INTER_AREA).astype(np.float32)/255
x=(x-np.array([0.485,0.456,0.406]))/np.array([0.229,0.224,0.225])
d=sess.run(None,{'l_x_':x.transpose(2,0,1)[None].astype(np.float32)})[0][0]
d=(d-np.percentile(d,1))/(np.percentile(d,99)-np.percentile(d,1)); d=np.clip(d,0,1)
d=cv2.resize(d,(640,int(round(640*GH/GW))),interpolation=cv2.INTER_AREA)
d=cv2.GaussianBlur(d,(0,0),3)
cv2.imwrite(out+f'kenya-{tag}-depth.jpg',(d*255).astype(np.uint8),[cv2.IMWRITE_JPEG_QUALITY,90])
# where the gliders sat in the photo, as fractions of the ground (for placing them)
json.dump({'ws':[ww,wh],'gs':[GW,GH],'pad':[pw/ww,ph/wh],'box':[x0/W,y0/H,x1/W,y1/H]},open(out+f'kenya-{tag}.json','w'))
print('wing',ww,wh,'ground',GW,GH)

# v2 "sharp dark" treatment (after designer E's tarmac): nothing is blurred, so every line stays.
# The ground is crushed and tinted; the glider keeps its colour; the air between wing and pilot is crushed a little less,
# so the lines read. usage: python3 tx.py NAME   (run inside fx/; needs mask_NAME.png)
import sys,numpy as np,cv2
from PIL import Image
CFG={'66':dict(gam=1.9,mul=0.58,sat=0.42,tint=(0.90,1.03,0.97),vmin=0.34,vr=1.15),
     't345':dict(gam=1.75,mul=0.62,sat=0.55,tint=(1.04,1.0,0.90),vmin=0.36,vr=1.05),
     't454':dict(gam=1.8,mul=0.60,sat=0.60,tint=(0.98,1.0,1.04),vmin=0.34,vr=1.1)}
LUM=np.array([.299,.587,.114],np.float32)
def run(n):
    c=CFG[n]; rgb=np.asarray(Image.open(f'../cal/t6_{n}.jpg').convert('RGB')).astype(np.float32)/255; H,W=rgb.shape[:2]
    m=np.asarray(Image.open(f'mask_{n}.png').convert('L')).astype(np.float32)/255
    bg=rgb*rgb*(3-2*rgb)*0.5+rgb*0.5
    lum=(bg@LUM)[...,None]; bg=lum+(bg-lum)*c['sat']
    deep=np.clip(bg,0,1)**c['gam']*c['mul']; mild=np.clip(bg,0,1)**(c['gam']*0.72)*min(1,c['mul']*1.25)
    pts=cv2.findNonZero((m>0.5).astype(np.uint8)); hull=np.zeros((H,W),np.uint8); cv2.fillConvexPoly(hull,cv2.convexHull(pts),1)
    hz=cv2.GaussianBlur(hull.astype(np.float32),(0,0),45)[...,None]
    bg=(deep*(1-hz)+mild*hz)*np.array(c['tint'],np.float32)
    ys,xs=np.nonzero(m>0.5); cx,cy=xs.mean(),ys.mean()
    yy,xx=np.mgrid[0:H,0:W].astype(np.float32); r=np.sqrt(((xx-cx)/W)**2+((yy-cy)/H)**2)
    bg*=(np.clip(1.08-c['vr']*r**1.3,c['vmin'],1))[...,None]
    fg=np.clip((rgb-0.5)*1.12+0.5,0,1)**0.84; l2=(fg@LUM)[...,None]; fg=np.clip(l2+(fg-l2)*1.18,0,1)
    a=cv2.GaussianBlur(cv2.erode(m,np.ones((3,3),np.uint8)),(0,0),1.1)[...,None]
    out=np.clip(bg*(1-a)+fg*a+np.random.default_rng(7).normal(0,0.012,(H,W,1)).astype(np.float32),0,1)
    Image.fromarray((out*255+0.5).astype(np.uint8)).save(f'../cal/t6_{n}_sd.jpg',quality=94,subsampling=0)
    Image.fromarray((out*255+0.5).astype(np.uint8)).resize((900,H*900//W)).save(f'pv_{n}.jpg',quality=88); print(n,'done')
for n in sys.argv[1:]: run(n)

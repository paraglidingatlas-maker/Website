# designer E treatments. usage: python3 e_fx.py NAME   (run inside fx/, needs emask_NAME.png from e_mask.py)
#  tarmac: no blur. Ground kept sharp and crushed to near-black, subject the only colour (the top-down reference)
#  pan:    panning shot. Ground streaked along the line of flight but its colour kept in the streaks
import sys,numpy as np,cv2
from PIL import Image
CFG={'89':dict(mode='tarmac',gam=2.15,mul=0.50,sat=0.22,tint=(0.93,1.0,1.09),vmin=0.30,vr=1.25),
     't454':dict(mode='pan',ang=-3,L=170,gam=1.5,mul=0.66,sat=0.80,tint=(0.97,1.0,1.05),vmin=0.34,vr=1.0),
     '138':dict(mode='pan',ang=0,L=150,gam=1.9,mul=0.62,sat=0.32,tint=(0.90,1.0,1.10),vmin=0.22,vr=1.05)}
LUM=np.array([.299,.587,.114],np.float32)
def mblur(img,L,ang):
    k=np.zeros((L,L),np.float32); c=L//2
    cv2.line(k,(0,c),(L-1,c),1.0,1); M=cv2.getRotationMatrix2D((c,c),-ang,1); k=cv2.warpAffine(k,M,(L,L)); k/=k.sum()
    return cv2.filter2D(img,-1,k,borderType=cv2.BORDER_REFLECT)
def run(n):
    c=CFG[n]; rgb=np.asarray(Image.open(f'../cal/t6_{n}.jpg').convert('RGB')).astype(np.float32)/255; H,W=rgb.shape[:2]
    m=np.asarray(Image.open(f'emask_{n}.png')).astype(np.float32)/255
    if c['mode']=='pan':
        hole=cv2.dilate((m>0.05).astype(np.uint8),np.ones((41,41),np.uint8))
        sm=cv2.resize((rgb*255).astype(np.uint8),(W//4,H//4),interpolation=cv2.INTER_AREA)
        inp=cv2.inpaint(sm,cv2.resize(hole,(W//4,H//4),interpolation=cv2.INTER_NEAREST),9,cv2.INPAINT_TELEA)
        inp=cv2.resize(inp,(W,H),interpolation=cv2.INTER_CUBIC).astype(np.float32)/255
        hf=cv2.GaussianBlur(hole.astype(np.float32),(0,0),12)[...,None]; bg=rgb*(1-hf)+inp*hf
        bg=mblur(mblur(bg,c['L'],c['ang']),c['L']//2,c['ang'])
    else:
        bg=rgb.copy(); bg=bg*bg*(3-2*bg)*0.5+bg*0.5     # a little contrast before the crush, so the rows stay crisp
    lum=(bg@LUM)[...,None]; bg=lum+(bg-lum)*c['sat']
    bg=np.clip(bg,0,1)**c['gam']*c['mul']*np.array(c['tint'],np.float32)
    ys,xs=np.nonzero(m>0.5); cx,cy=xs.mean(),ys.mean()
    yy,xx=np.mgrid[0:H,0:W].astype(np.float32); r=np.sqrt(((xx-cx)/W)**2+((yy-cy)/H)**2)
    bg*=(np.clip(1.08-c['vr']*r**1.3,c['vmin'],1))[...,None]
    if c['mode']=='tarmac':   # the wing's own shadow under it: a soft drop along the light, so it sits in the air
        sh=cv2.GaussianBlur(np.roll(np.roll(m,26,0),-14,1),(0,0),18)[...,None]; bg*=1-0.45*sh
    fg=np.clip((rgb-0.5)*1.12+0.5,0,1)**0.84; l2=(fg@LUM)[...,None]; fg=np.clip(l2+(fg-l2)*1.18,0,1)
    a=cv2.GaussianBlur(cv2.erode(m,np.ones((3,3),np.uint8)),(0,0),1.1)[...,None]
    out=bg*(1-a)+fg*a
    out=np.clip(out+np.random.default_rng(7).normal(0,0.012,(H,W,1)).astype(np.float32),0,1)
    Image.fromarray((out*255+0.5).astype(np.uint8)).save(f'../cal/t6_{n}_e.jpg',quality=94,subsampling=0)
    cut=np.dstack([fg,a]); Image.fromarray((np.clip(cut,0,1)*255+.5).astype(np.uint8),'RGBA').save(f'../cal/t6_{n}_ecut.png')
    Image.fromarray((out*255+0.5).astype(np.uint8)).resize((1000,H*1000//W)).save(f'../tmp/pv_{n}.jpg',quality=88); print(n,'done')
for n in sys.argv[1:]: run(n)

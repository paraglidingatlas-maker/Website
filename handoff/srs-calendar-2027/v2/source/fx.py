import sys,numpy as np,cv2
from PIL import Image
from rembg import new_session,remove
S=new_session('isnet-general-use')
# per photo: blur angle (deg, direction of travel), extra crops to re-segment (pilot), blur length
CFG={'138':dict(ang=0,rois=[],L=150),
     '66':dict(ang=57,rois=[(1150,800,1650,1300)],L=130),
     '100':dict(ang=4,rois=[(1300,1050,1950,1420)],L=150),
     '89':dict(ang=82,rois=[(1380,930,1720,1270)],L=130),
     't454':dict(ang=-3,rois=[(480,1150,1020,1500)],L=150),
     't494':dict(ang=0,rois=[],L=170,minarea=1500),
     't345':dict(ang=-8,rois=[(700,1380,1300,1655)],L=190,sat=0.8,gam=1.35,mul=0.78,tint=(1.0,1.0,1.0),vmin=0.45)}
def seg(im): return np.asarray(remove(im,session=S,only_mask=True)).astype(np.float32)/255
def clean(m,minarea):
    b=(m>0.5).astype(np.uint8); n,lab,st,_=cv2.connectedComponentsWithStats(b,8)
    keep=np.zeros_like(b)
    for i in range(1,n):
        if st[i,cv2.CC_STAT_AREA]>=minarea: keep[lab==i]=1
    keep=cv2.dilate(keep,np.ones((5,5),np.uint8))
    return np.clip((m-0.3)/0.5,0,1)*keep
def mblur(img,L,ang):
    k=np.zeros((L,L),np.float32); c=L//2
    cv2.line(k,(0,c),(L-1,c),1.0,1); M=cv2.getRotationMatrix2D((c,c),-ang,1); k=cv2.warpAffine(k,M,(L,L)); k/=k.sum()
    return cv2.filter2D(img,-1,k,borderType=cv2.BORDER_REFLECT)
def run(n):
    c=CFG[n]; pil=Image.open(f'../cal/t6_{n}.jpg').convert('RGB'); rgb=np.asarray(pil).astype(np.float32)/255; H,W=rgb.shape[:2]
    m=clean(seg(pil),c.get('minarea',6000 if n!='138' else 2000))
    if n=='138': m=np.maximum(m,np.clip((seg(pil)-0.3)/0.5,0,1)*(cv2.dilate((m>0).astype(np.uint8),np.ones((1,1),np.uint8))|1)*(np.arange(H)[:,None]<900))  # keep thin lines
    for (x0,y0,x1,y1) in c['rois']:
        mm=clean(seg(pil.crop((x0,y0,x1,y1))),1500); m[y0:y1,x0:x1]=np.maximum(m[y0:y1,x0:x1],mm)
    Image.fromarray((m*255).astype(np.uint8)).save(f'mask_{n}.png')
    # background: remove subject, then streak
    hole=cv2.dilate((m>0.05).astype(np.uint8),np.ones((41,41),np.uint8))
    sm=cv2.resize((rgb*255).astype(np.uint8),(W//4,H//4),interpolation=cv2.INTER_AREA)
    inp=cv2.inpaint(sm,cv2.resize(hole,(W//4,H//4),interpolation=cv2.INTER_NEAREST),9,cv2.INPAINT_TELEA)
    inp=cv2.resize(inp,(W,H),interpolation=cv2.INTER_CUBIC).astype(np.float32)/255
    hf=cv2.GaussianBlur(hole.astype(np.float32),(0,0),12)[...,None]
    bg=rgb*(1-hf)+inp*hf
    if c.get('pad'):
        P=c['pad']; bg=cv2.copyMakeBorder(bg,0,P,0,0,cv2.BORDER_REFLECT_101)
        rgb=cv2.copyMakeBorder(rgb,0,P,0,0,cv2.BORDER_CONSTANT,value=0); m=cv2.copyMakeBorder(m,0,P,0,0,cv2.BORDER_CONSTANT,value=0); H+=P
        soft=cv2.GaussianBlur(bg,(0,0),45); w=np.clip((np.arange(H,dtype=np.float32)-(H-P-500))/600,0,1)[:,None,None]
        bg=bg*(1-w)+soft*w
    bg=mblur(mblur(bg,c['L'],c['ang']),c['L']//2,c['ang'])
    lum=(bg@np.array([.299,.587,.114],np.float32))[...,None]
    bg=lum+(bg-lum)*c.get('sat',0.32)                       # desaturate
    bg=np.clip(bg,0,1)**c.get('gam',1.9)*c.get('mul',0.62)               # crush + darken
    bg*=np.array(c.get('tint',(0.90,1.0,1.10)),np.float32)   # cool tint
    ys,xs=np.nonzero(m>0.5); cx,cy=xs.mean(),ys.mean()
    yy,xx=np.mgrid[0:H,0:W].astype(np.float32); r=np.sqrt(((xx-cx)/W)**2+((yy-cy)/H)**2)
    bg*=(np.clip(1.08-1.05*r**1.3,c.get('vmin',0.22),1))[...,None]   # light pool around the subject
    # subject: sharp, colour kept
    fg=np.clip((rgb-0.5)*1.12+0.5,0,1)**0.84; l2=(fg@np.array([.299,.587,.114],np.float32))[...,None]; fg=np.clip(l2+(fg-l2)*1.18,0,1)
    a=cv2.erode(m,np.ones((3,3),np.uint8)); a=cv2.GaussianBlur(a,(0,0),1.1)[...,None]
    out=bg*(1-a)+fg*a
    g=np.random.default_rng(7).normal(0,0.012,(H,W,1)).astype(np.float32); out=np.clip(out+g,0,1)
    Image.fromarray((out*255+0.5).astype(np.uint8)).save(f'../cal/t6_{n}_fx.jpg',quality=94,subsampling=0)
    Image.fromarray((out*255+0.5).astype(np.uint8)).resize((900,H*900//W)).save(f'pv_{n}.jpg',quality=88)
    print(n,'done mask %.3f'%m.mean())
for n in sys.argv[1:]: run(n)

# Designer D treatment: a pan that keeps its colour, and the wing keeps its lines.
# Run from inside fx/:  python3 fx2.py t454 138
#  1. subject mask (rembg, plus re-segmented crops for the pilot), cached in mask2_NAME.png
#  2. lines: found in the ORIGINAL photo, in polar space around the risers (a line is a constant angle),
#     then drawn back at their real angles from the risers to the wing
#  3. background: subject inpainted out, streaked along the direction of travel, colour kept, one grade
#  4. subject on top with a slightly eroded soft edge (no rim), the same grade, a little more light
import sys,os,numpy as np,cv2
from PIL import Image
CFG={
 't454':dict(ang=-3,L=170,rois=[(480,1150,1020,1500)],R=[(757,1243)],fan=(-100,5),rmax=1150,pol='light',
             sat=0.82,gam=1.4,mul=0.72,tint=(1.0,0.99,1.0),vmin=0.42,fgain=1.0,lcol=(0.86,0.88,0.90),lthr=2.6,nolines=True),
 '138': dict(ang=0,L=190,rois=[],R=[(1528,775),(1622,760)],fan=(-135,-45),rmax=1000,pol='dark',minarea=2000,
             sat=0.78,gam=1.75,mul=0.50,tint=(0.80,0.95,1.16),vmin=0.30,fgain=1.0,lcol=(0.74,0.80,0.90),lthr=2.2,direct=True,t0=0.016,t1=0.04,gate=0.022),
 '66':  dict(ang=57,L=140,rois=[(1150,800,1650,1300)],R=[(1330,1010)],fan=(-170,-10),rmax=900,pol='light',
             sat=0.80,gam=1.45,mul=0.66,tint=(0.97,1.0,1.03),vmin=0.36,fgain=1.0,lcol=(0.86,0.88,0.90),lthr=2.6,nolines=True),
}
LUM=np.array([.299,.587,.114],np.float32)
def seg(im,S):
    from rembg import remove
    return np.asarray(remove(im,session=S,only_mask=True)).astype(np.float32)/255
def clean(m,minarea):
    b=(m>0.5).astype(np.uint8); n,lab,st,_=cv2.connectedComponentsWithStats(b,8); keep=np.zeros_like(b)
    for i in range(1,n):
        if st[i,cv2.CC_STAT_AREA]>=minarea: keep[lab==i]=1
    return np.clip((m-0.3)/0.5,0,1)*cv2.dilate(keep,np.ones((5,5),np.uint8))
def mask(n,c,pil):
    f=f'mask2_{n}.png'
    if os.path.exists(f): return np.asarray(Image.open(f)).astype(np.float32)/255
    from rembg import new_session
    S=new_session('isnet-general-use'); m=clean(seg(pil,S),c.get('minarea',6000))
    for (x0,y0,x1,y1) in c['rois']:
        mm=clean(seg(pil.crop((x0,y0,x1,y1)),S),1500); m[y0:y1,x0:x1]=np.maximum(m[y0:y1,x0:x1],mm)
    Image.fromarray((m*255).astype(np.uint8)).save(f); return m
def mblur(img,L,ang):
    k=np.zeros((L,L),np.float32); c=L//2
    cv2.line(k,(0,c),(L-1,c),1.0,1); M=cv2.getRotationMatrix2D((c,c),-ang,1); k=cv2.warpAffine(k,M,(L,L)); k/=k.sum()
    return cv2.filter2D(img,-1,k,borderType=cv2.BORDER_REFLECT)
def lines(n,c,rgb,m):
    """alpha map of the wing's lines, at full size"""
    H,W=m.shape; lum=(rgb@LUM).astype(np.float32); out=np.zeros((H,W),np.float32)
    subj=cv2.dilate((m>0.3).astype(np.uint8),np.ones((7,7),np.uint8))
    if c.get('direct'):
        # smooth sky: the lines are simply the thin dark (or light) detail above the pilot
        k=cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(9,9))
        r=cv2.morphologyEx(lum,cv2.MORPH_BLACKHAT if c['pol']=='dark' else cv2.MORPH_TOPHAT,k)
        # keep only what holds a direction: the response averaged along a short line, best of all angles
        best=np.zeros_like(r)
        for t in range(-48,49,3):
            Lk=41; kk=np.zeros((Lk,Lk),np.float32); cc=Lk//2
            cv2.line(kk,(cc,0),(cc,Lk-1),1.0,1); kk=cv2.warpAffine(kk,cv2.getRotationMatrix2D((cc,cc),t,1),(Lk,Lk)); kk/=kk.sum()
            best=np.maximum(best,cv2.filter2D(r,-1,kk))
        near=np.zeros((H,W),np.uint8)
        for (rx,ry) in c['R']: cv2.circle(near,(rx,ry),260,1,-1)          # close to the risers the lines bunch up: no gate there
        a=np.clip((r-c.get('t0',0.035))/c.get('t1',0.07),0,1)**0.55*((best>c.get('gate',0.03))|(near==1))
        cone=np.zeros((H,W),np.uint8)
        for (rx,ry) in c['R']:
            pts=[(rx,ry)]+[(int(rx+c['rmax']*2*np.cos(np.radians(t))),int(ry+c['rmax']*2*np.sin(np.radians(t)))) for t in np.linspace(c['fan'][0],c['fan'][1],30)]
            cv2.fillPoly(cone,[np.array(pts,np.int32)],1)
        a*=cone*(1-subj)
        # drop specks: keep only long thin components
        b=cv2.dilate((a>0.2).astype(np.uint8),np.ones((3,3),np.uint8)); k2,lab,st,_=cv2.connectedComponentsWithStats(b,8); keep=np.zeros_like(b)
        for i in range(1,k2):
            if st[i,cv2.CC_STAT_HEIGHT]>=90 or (st[i,cv2.CC_STAT_HEIGHT]>=14 and near[lab==i].any()): keep[lab==i]=1
        a=a*cv2.dilate(keep,np.ones((3,3),np.uint8)); return np.clip(cv2.GaussianBlur(a,(0,0),0.7)*1.12,0,0.84)
    NA=5760
    for (rx,ry) in c['R']:
        RM=c['rmax']
        pol=cv2.warpPolar(lum,(RM,NA),(rx,ry),RM,cv2.INTER_LINEAR|cv2.WARP_POLAR_LINEAR)       # rows: angle, cols: radius
        pm=cv2.warpPolar(subj.astype(np.float32),(RM,NA),(rx,ry),RM,cv2.INTER_NEAREST|cv2.WARP_POLAR_LINEAR)
        # thin ridge across the angle axis; the kernel is about 9 px of arc at every radius
        resp=np.zeros_like(pol)
        for r0 in range(40,RM,40):
            kk=max(3,int(round(9/(r0+20)*NA/(2*np.pi)))|1); band=pol[:,r0:r0+40]
            op=cv2.MORPH_TOPHAT if c['pol']=='light' else cv2.MORPH_BLACKHAT
            resp[:,r0:r0+40]=cv2.morphologyEx(band,op,np.ones((kk,1),np.uint8))
        resp=cv2.blur(resp,(90,1))                                    # a line holds its angle; texture does not
        a0,a1=c['fan']; rows=np.arange(NA)*360.0/NA; rows=np.where(rows>180,rows-360,rows)
        infan=((rows>=a0)&(rows<=a1))
        # for each angle: where the ray meets the wing (first subject pixel beyond 120 px)
        hit=np.full(NA,-1,int)
        far=pm[:,120:]>0.5; anyhit=far.any(1); hit[anyhit]=far[anyhit].argmax(1)+120
        ev=np.zeros(NA,np.float32)
        for i in np.nonzero(infan&(hit>200))[0]:
            seg_=resp[i,60:hit[i]-6]; ok=pm[i,60:hit[i]-6]<0.5
            if ok.sum()>80: ev[i]=np.percentile(seg_[ok],70)
        base=cv2.blur(ev.reshape(-1,1),(1,301)).ravel(); sd=ev[infan&(hit>200)].std()+1e-6
        z=(ev-base)/sd
        # peaks, at least 0.5 degree apart
        idx=[i for i in range(2,NA-2) if z[i]>c['lthr'] and z[i]==z[max(0,i-8):i+9].max()]
        print(n,'riser',(rx,ry),'lines found',len(idx))
        big=4; canvas=np.zeros((H*big,W*big),np.float32)
        for i in idx:
            t=np.radians(rows[i]); r1=hit[i]+4; al=float(np.clip(0.45+0.12*z[i],0.5,0.95))
            p0=(int((rx+14*np.cos(t))*big),int((ry+14*np.sin(t))*big)); p1=(int((rx+r1*np.cos(t))*big),int((ry+r1*np.sin(t))*big))
            cv2.line(canvas,p0,p1,al,5,cv2.LINE_AA)
        out=np.maximum(out,cv2.resize(canvas,(W,H),interpolation=cv2.INTER_AREA))
    return out*(1-subj)
def run(n):
    c=CFG[n]; pil=Image.open(f'../cal/t6_{n}.jpg').convert('RGB'); rgb=np.asarray(pil).astype(np.float32)/255; H,W=rgb.shape[:2]
    m=mask(n,c,pil); la=np.zeros(m.shape,np.float32) if c.get('nolines') else lines(n,c,rgb,m)
    Image.fromarray((la*255).astype(np.uint8)).save(f'lines_{n}.png')
    hole=cv2.dilate((m>0.05).astype(np.uint8),np.ones((41,41),np.uint8))
    sm=cv2.resize((rgb*255).astype(np.uint8),(W//4,H//4),interpolation=cv2.INTER_AREA)
    inp=cv2.inpaint(sm,cv2.resize(hole,(W//4,H//4),interpolation=cv2.INTER_NEAREST),9,cv2.INPAINT_TELEA)
    inp=cv2.resize(inp,(W,H),interpolation=cv2.INTER_CUBIC).astype(np.float32)/255
    hf=cv2.GaussianBlur(hole.astype(np.float32),(0,0),12)[...,None]
    bg=rgb*(1-hf)+inp*hf
    bg=mblur(mblur(bg,c['L'],c['ang']),c['L']//2,c['ang'])
    def grade(x,sat,gam,mul):
        l=(x@LUM)[...,None]; x=l+(x-l)*sat
        return np.clip(x,0,1)**gam*mul*np.array(c['tint'],np.float32)
    bg=grade(bg,c['sat'],c['gam'],c['mul'])
    ys,xs=np.nonzero(m>0.5); cx,cy=xs.mean(),ys.mean()
    yy,xx=np.mgrid[0:H,0:W].astype(np.float32); r=np.sqrt(((xx-cx)/W)**2+((yy-cy)/H)**2)
    bg*=(np.clip(1.06-0.95*r**1.3,c['vmin'],1))[...,None]            # the light falls where the pilot is
    fg=np.clip((rgb-0.5)*1.08+0.5,0,1)**0.92; l2=(fg@LUM)[...,None]; fg=np.clip(l2+(fg-l2)*1.12,0,1)*c['fgain']
    fg=fg*np.array([1-(1-t)*0.35 for t in c['tint']],np.float32)      # a third of the place's tint on the subject
    out=bg*(1-la[...,None])+np.array(c['lcol'],np.float32)*la[...,None]
    a=cv2.erode(m,np.ones((5,5),np.uint8)); a=cv2.GaussianBlur(a,(0,0),1.3)[...,None]
    out=out*(1-a)+fg*a
    g=np.random.default_rng(7).normal(0,0.011,(H,W,1)).astype(np.float32); out=np.clip(out+g,0,1)
    Image.fromarray((out*255+0.5).astype(np.uint8)).save(f'../cal/t6_{n}_d.jpg',quality=94,subsampling=0)
    Image.fromarray((out*255+0.5).astype(np.uint8)).resize((1300,H*1300//W),Image.LANCZOS).save(f'../pv/d_{n}.jpg',quality=88)
    print(n,'done')
for n in sys.argv[1:]: run(n)

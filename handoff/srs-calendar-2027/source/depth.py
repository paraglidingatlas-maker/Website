# "depth" treatment: landscape kept sharp, sky pulled down with a graduated filter; also writes the subject as a cut-out
import sys,numpy as np,cv2
from PIL import Image
from rembg import new_session,remove
n=sys.argv[1]; rois=[tuple(map(int,a.split(','))) for a in sys.argv[2:]]
S=new_session('isnet-general-use')
pil=Image.open(f'../cal/t6_{n}.jpg').convert('RGB'); rgb=np.asarray(pil).astype(np.float32)/255; H,W=rgb.shape[:2]
seg=lambda im: np.asarray(remove(im,session=S,only_mask=True)).astype(np.float32)/255
m=np.clip((seg(pil)-0.3)/0.5,0,1)
for (x0,y0,x1,y1) in rois: m[y0:y1,x0:x1]=np.maximum(m[y0:y1,x0:x1],np.clip((seg(pil.crop((x0,y0,x1,y1)))-0.3)/0.5,0,1))
b=(m>0.5).astype(np.uint8); k,lab,st,_=cv2.connectedComponentsWithStats(b,8); keep=np.zeros_like(b)
for i in range(1,k):
    if st[i,cv2.CC_STAT_AREA]>=1500: keep[lab==i]=1
m*=cv2.dilate(keep,np.ones((5,5),np.uint8))
x=np.clip(rgb,0,1); x=x*x*(3-2*x)*0.5+x*0.5
lum=(x@np.array([.299,.587,.114],np.float32))[...,None]; x=lum+(x-lum)*1.08
yy=np.arange(H,dtype=np.float32)[:,None,None]/H
nd=np.clip(0.42+0.58*np.clip((yy-0.05)/0.5,0,1)**0.8,0,1)       # graduated filter: sky down, land untouched
bg=x*nd*np.array([0.94,0.99,1.06],np.float32)*0.92
fg=np.clip(x*1.03,0,1)
a=cv2.GaussianBlur(cv2.erode(m,np.ones((3,3),np.uint8)),(0,0),1.0)[...,None]
out=np.clip(bg*(1-a)+fg*a,0,1)
Image.fromarray((out*255+.5).astype(np.uint8)).save(f'../cal/t6_{n}_depth.jpg',quality=94,subsampling=0)
cut=np.dstack([fg,a]); Image.fromarray((np.clip(cut,0,1)*255+.5).astype(np.uint8),'RGBA').save(f'../cal/t6_{n}_cut.png')
print('mask %.3f'%m.mean())

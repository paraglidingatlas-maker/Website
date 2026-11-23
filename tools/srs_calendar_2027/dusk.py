# "dusk" treatment: no blur; everything sinks into blue haze except the saturated wings
import sys,numpy as np,cv2
from PIL import Image
n=sys.argv[1]; rgb=np.asarray(Image.open(f'../cal/t6_{n}.jpg').convert('RGB')).astype(np.float32)/255; H,W=rgb.shape[:2]
mx=rgb.max(2); mn=rgb.min(2); sat=(mx-mn)/(mx+1e-4)
w=np.clip((sat-0.30)/0.14,0,1)*np.clip((mx-0.40)/0.14,0,1)
w=cv2.GaussianBlur(cv2.dilate(w,np.ones((3,3),np.uint8)),(0,0),1.0)[...,None]
lum=(rgb@np.array([.299,.587,.114],np.float32))[...,None]
bg=lum+(rgb-lum)*0.5; bg=np.clip(bg,0,1)**1.55*0.72*np.array([0.82,0.98,1.16],np.float32)
fg=np.clip(lum+(rgb-lum)*1.25,0,1)
x=bg*(1-w)+fg*w
yy,xx=np.mgrid[0:H,0:W].astype(np.float32); r=np.sqrt(((xx-W*0.55)/W)**2+((yy-H*0.5)/H)**2)
x*=np.clip(1.1-0.8*r**1.6,0.5,1)[...,None]
x=np.clip(x+np.random.default_rng(5).normal(0,0.010,(H,W,1)).astype(np.float32),0,1)
Image.fromarray((x*255+.5).astype(np.uint8)).save(f'../cal/t6_{n}_dusk.jpg',quality=94,subsampling=0)

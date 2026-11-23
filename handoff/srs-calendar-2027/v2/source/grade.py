# "natural" treatment: no blur, rich colour kept, cinematic curve + vignette
import sys,numpy as np,cv2
from PIL import Image
n=sys.argv[1]; rgb=np.asarray(Image.open(f'../cal/t6_{n}.jpg').convert('RGB')).astype(np.float32)/255; H,W=rgb.shape[:2]
x=np.clip(rgb,0,1); x=x*x*(3-2*x)*0.55+x*0.45          # gentle S curve
lum=(x@np.array([.299,.587,.114],np.float32))[...,None]
x=lum+(x-lum)*0.92; x=x*np.array([0.96,1.0,1.03],np.float32)*1.0
hi=np.clip((lum-0.55)/0.3,0,1); x=x*(1-hi)+np.clip(rgb*1.04,0,1)*hi   # keep the wings bright and clean
yy,xx=np.mgrid[0:H,0:W].astype(np.float32); r=np.sqrt(((xx-W*0.42)/W)**2+((yy-H*0.55)/H)**2)
x*=np.clip(1.12-0.8*r**1.5,0.55,1)[...,None]
x=np.clip(x+np.random.default_rng(3).normal(0,0.010,(H,W,1)).astype(np.float32),0,1)
Image.fromarray((x*255+.5).astype(np.uint8)).save(f'../cal/t6_{n}_nat.jpg',quality=94,subsampling=0)

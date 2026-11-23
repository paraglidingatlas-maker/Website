# "night" treatment (designer F): like dusk, but the haze is smoothed before it is darkened, so JPEG blocks do not
# show, and the wings are keyed with a soft edge so they carry no halo. Writes ../cal/t6_NAME_night.jpg
import sys,numpy as np,cv2
from PIL import Image
n=sys.argv[1]; src=np.asarray(Image.open(f'../cal/t6_{n}.jpg').convert('RGB')); H,W=src.shape[:2]
rgb=src.astype(np.float32)/255
mx=rgb.max(2); mn=rgb.min(2); sat=(mx-mn)/(mx+1e-4)
w=np.clip((sat-0.34)/0.22,0,1)*np.clip((mx-0.38)/0.2,0,1)          # the wings: saturated and bright
w=cv2.GaussianBlur(w,(0,0),1.6)
w=np.clip(w*1.25,0,1)[...,None]
# background: denoise (kills 8x8 blocks in the haze), keep the ridge lines
den=cv2.bilateralFilter(src,9,28,7); den=cv2.bilateralFilter(den,9,20,9).astype(np.float32)/255
den=cv2.GaussianBlur(den,(0,0),1.2)
lum=(den@np.array([.299,.587,.114],np.float32))[...,None]
bg=lum+(den-lum)*0.45
bg=np.clip(bg,0,1)**1.7*0.62*np.array([0.78,0.95,1.20],np.float32)   # crush into navy
l0=(rgb@np.array([.299,.587,.114],np.float32))[...,None]
fg=np.clip(l0+(rgb-l0)*1.22,0,1)*0.96
x=bg*(1-w)+fg*w
yy,xx=np.mgrid[0:H,0:W].astype(np.float32); r=np.sqrt(((xx-W*0.55)/W)**2+((yy-H*0.45)/H)**2)
x*=np.clip(1.12-0.75*r**1.6,0.55,1)[...,None]
x=np.clip(x+np.random.default_rng(5).normal(0,0.011,(H,W,1)).astype(np.float32),0,1)   # fine grain hides banding
Image.fromarray((x*255+.5).astype(np.uint8)).save(f'../cal/t6_{n}_night.jpg',quality=95,subsampling=0)

# The site's grade for the new Kenya photos: haze cut, deeper blacks, a little warmer and richer, soft vignette.
import os
import cv2, numpy as np, sys
S=os.environ['SCRATCH']+'/'
def grade(bgr, haze=0.5, warm=1.0):
    f=bgr.astype(np.float32)/255
    # black point per channel (cuts the blue haze), white point overall
    lo=np.percentile(f.reshape(-1,3),0.4,axis=0)*haze*1.6
    hi=np.percentile(f,99.7)
    f=np.clip((f-lo)/(hi-lo),0,1)
    lab=cv2.cvtColor(f,cv2.COLOR_BGR2LAB)
    L=lab[...,0]/100
    cl=cv2.createCLAHE(clipLimit=1.6,tileGridSize=(8,8)).apply((L*65535).astype(np.uint16)).astype(np.float32)/65535
    L=0.55*L+0.45*cl
    L=np.clip(L,0,1)**1.12                       # deeper mid-tones
    L=L+0.22*(L*L*(3-2*L)-L)                     # a gentle S-curve
    lab[...,0]=L*100
    lab[...,1:]*=1.2                              # a little richer
    lab[...,1]+=1.0*warm; lab[...,2]+=3.5*warm    # warmer (late light)
    f=cv2.cvtColor(lab,cv2.COLOR_LAB2BGR)
    h,w=f.shape[:2]; y,x=np.ogrid[-1:1:h*1j,-1:1:w*1j]
    v=1-0.30*np.clip(np.sqrt((x*0.9)**2+(y*1.1)**2)-0.35,0,1)**1.6
    f*=v[...,None]
    return np.clip(f*255,0,255).astype(np.uint8)
if __name__=='__main__':
    for n in sys.argv[1:]:
        o=cv2.imread(S+f'orig/{n}.JPG'); g=grade(o)
        cv2.imwrite(S+f'k3/{n}-graded.png',g)
        a=cv2.resize(o,(900,600),interpolation=cv2.INTER_AREA); b=cv2.resize(g,(900,600),interpolation=cv2.INTER_AREA)
        cv2.imwrite(S+f'look/{n}-ba.jpg',np.hstack([a,b]),[cv2.IMWRITE_JPEG_QUALITY,85])

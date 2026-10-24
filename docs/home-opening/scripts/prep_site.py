# The site's own India photos: a lighter version of the same grade (they are already edited once).
import os
import cv2, numpy as np, sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from grade import grade
S=os.environ['SCRATCH']+'/'
src,name,warm=sys.argv[1],sys.argv[2],float(sys.argv[3])
o=cv2.imread(src); g=grade(o,haze=0.2,warm=warm)
g=cv2.addWeighted(o,0.45,g,0.55,0)          # half way: keep the photo's own edit
cv2.imwrite(S+f'k3/{name}-graded.png',g)
cv2.imwrite(S+f'look/{name}-ba.jpg',np.hstack([cv2.resize(o,(700,int(700*o.shape[0]/o.shape[1]))),cv2.resize(g,(700,int(700*o.shape[0]/o.shape[1])))]),[cv2.IMWRITE_JPEG_QUALITY,85])
print(g.shape)

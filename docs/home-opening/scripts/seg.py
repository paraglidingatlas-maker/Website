# Cut the gliders out with rembg (birefnet-general-lite), one crop per glider, at full size.
import os
import sys, numpy as np, cv2
from PIL import Image
from rembg import new_session, remove
S=os.environ['SCRATCH']+'/'
sess=new_session('birefnet-general-lite')
name=sys.argv[1]; boxes=[tuple(map(int,b.split(','))) for b in sys.argv[2:]]
g=cv2.imread(S+f'k3/{name}-graded.png')
A=np.zeros(g.shape[:2],np.uint8)
for (x0,y0,x1,y1) in boxes:
    crop=Image.fromarray(cv2.cvtColor(g[y0:y1,x0:x1],cv2.COLOR_BGR2RGB))
    m=remove(crop,session=sess,only_mask=True)
    A[y0:y1,x0:x1]=np.maximum(A[y0:y1,x0:x1],np.asarray(m))
cv2.imwrite(S+f'k3/{name}-mask.png',A)
print(A.mean())

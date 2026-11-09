"""Turn the pasted sprites into x-<name>.jpg for make_atlas.py: sharpen the edited region to the
photo's detail level (edits come out softer) and colour-match mouth skin to the base.
Usage: python3 finish_sprites.py <dir>   (needs s-closed.jpg plus s-slight/ah/oo/ee and s-blink/lookL/lookR[/lookUp].jpg)"""
import cv2, numpy as np, sys, os
sys.path.insert(0, os.path.dirname(__file__)); from face import face_box, region_mask
D = sys.argv[1]; base = cv2.imread(f'{D}/s-closed.jpg').astype(np.float32); box = face_box(base); x, y, w, h = box
MM = region_mask(base.shape, box, 'mouth'); ME = region_mask(base.shape, box, 'eyes')
mr = (slice(y+int(h*.65), y+int(h*.98)), slice(x+int(w*.25), x+int(w*.75)))
lap = lambda im: cv2.Laplacian(cv2.cvtColor(np.clip(im,0,255).astype(np.uint8), cv2.COLOR_BGR2GRAY)[mr], cv2.CV_64F).var()
target = lap(base)
for k in ['closed','slight','ah','oo','ee','blink','lookL','lookR','lookUp']:
    p = f'{D}/s-{k}.jpg'
    if not os.path.exists(p): continue
    s = cv2.imread(p).astype(np.float32); M = ME if k in ('blink','lookL','lookR','lookUp') else MM
    for amt in (0.8, 1.4, 2.0, 2.8):
        sh = s + amt*(s - cv2.GaussianBlur(s, (0,0), 1.0))
        if lap(sh) >= target*0.4: break
    cv2.imwrite(f'{D}/x-{k}.jpg', np.clip(sh*M + base*(1-M), 0, 255).astype(np.uint8), [cv2.IMWRITE_JPEG_QUALITY, 95])
print('wrote x-*.jpg in', D)

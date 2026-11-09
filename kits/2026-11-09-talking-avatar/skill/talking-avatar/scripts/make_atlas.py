"""Pre-render a talking-avatar atlas for the browser: a base still plus small cut-outs.

mouth/<shape>-<1..5>.png  in-between mouth frames (optical-flow warp from closed toward the shape)
eyes/<blink|lookL|lookR|lookUp>-<1..3>.png  eyelid / gaze steps (level 3 of blink = the real closed-eye still)
Each cut-out carries a feathered alpha, so the player just draws it over base.jpg at manifest x,y.
Usage: python3 make_atlas.py <dir with x-*.jpg from finish_sprites.py> <out-dir>
"""
import cv2, numpy as np, json, os, sys
SRC, OUT = sys.argv[1], sys.argv[2]
os.makedirs(f'{OUT}/mouth', exist_ok=True); os.makedirs(f'{OUT}/eyes', exist_ok=True)
img = lambda k: cv2.imread(f'{SRC}/x-{k}.jpg').astype(np.float32)
base = img('closed'); H, W = base.shape[:2]
g = cv2.cvtColor(base.astype(np.uint8), cv2.COLOR_BGR2GRAY)
fc = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
x, y, fw, fh = max(fc.detectMultiScale(g, 1.1, 5, minSize=(80, 80)), key=lambda f: f[2])
def ell(box, soft):
    x0,y0,x1,y1=int(x+fw*box[0]),int(y+fh*box[1]),int(x+fw*box[2]),int(y+fh*box[3]); m=np.zeros((H,W),np.float32)
    cv2.ellipse(m,((x0+x1)//2,(y0+y1)//2),((x1-x0)//2,(y1-y0)//2),0,0,360,1,-1)
    return np.clip(cv2.GaussianBlur(m,(0,0),(x1-x0)/soft)*1.8,0,1), (max(0,x0-30),max(0,y0-30),min(W,x1+30),min(H,y1+30))
MM, mbox = ell((0.18,0.58,0.82,1.0),7); ME, ebox = ell((0.04,0.18,0.96,0.54),7)
dis = cv2.DISOpticalFlow_create(cv2.DISOPTICAL_FLOW_PRESET_MEDIUM); dis.setFinestScale(0); dis.setPatchSize(12); dis.setVariationalRefinementIterations(10)
gray = lambda im: cv2.cvtColor(np.clip(im,0,255).astype(np.uint8), cv2.COLOR_BGR2GRAY)
gx, gy = np.meshgrid(np.arange(W, dtype=np.float32), np.arange(H, dtype=np.float32))
def pair(k):
    t = img(k); return t, dis.calc(gray(base), gray(t), None), dis.calc(gray(t), gray(base), None)
def morph(t, f01, f10, s, blend=True):
    wb = cv2.remap(base, gx+s*f10[...,0], gy+s*f10[...,1], cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
    if not blend: return wb
    wt = cv2.remap(t, gx+(1-s)*f01[...,0], gy+(1-s)*f01[...,1], cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
    b = float(np.clip((s-0.2)/0.45,0,1)); b = b*b*(3-2*b); return wb*(1-b)+wt*b
def cut(im, m, box, path):
    x0,y0,x1,y1 = box; rgba = np.dstack([np.clip(im[y0:y1,x0:x1],0,255), (m[y0:y1,x0:x1]*255)]).astype(np.uint8)
    cv2.imwrite(path, rgba, [cv2.IMWRITE_PNG_COMPRESSION, 9])
man = {'width': W, 'height': H, 'mouth': {'x': mbox[0], 'y': mbox[1], 'levels': 5, 'shapes': []},
       'eyes': {'x': ebox[0], 'y': ebox[1], 'levels': 3, 'kinds': []}}
for k in ['slight','ah','oo','ee']:
    P = pair(k)
    for lv in range(1, 6): cut(morph(*P, lv/5), MM, mbox, f'{OUT}/mouth/{k}-{lv}.png')
    man['mouth']['shapes'].append(k)
for k in ['blink','lookL','lookR','lookUp']:
    if not os.path.exists(f'{SRC}/x-{k}.jpg'): continue
    P = pair(k)
    for lv in range(1, 4):
        im = P[0] if (k=='blink' and lv==3) else morph(*P, lv/3, blend=(k!='blink'))
        cut(im, ME, ebox, f'{OUT}/eyes/{k}-{lv}.png')
    man['eyes']['kinds'].append(k)
cv2.imwrite(f'{OUT}/base.jpg', np.clip(base,0,255).astype(np.uint8), [cv2.IMWRITE_JPEG_QUALITY, 88])
json.dump(man, open(f'{OUT}/manifest.json','w'), indent=1); print(json.dumps(man))

"""Shared helpers: face box and feathered region masks (mouth, eyes) for a portrait."""
import cv2, numpy as np
def face_box(img):
    g = cv2.cvtColor(img.astype(np.uint8), cv2.COLOR_BGR2GRAY)
    fc = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    faces = fc.detectMultiScale(g, 1.1, 5, minSize=(80, 80))
    if len(faces) == 0: raise SystemExit('no face found: use a front-facing portrait')
    return max(faces, key=lambda f: f[2])
REGIONS = {'mouth': (0.18, 0.58, 0.82, 1.0), 'eyes': (0.04, 0.18, 0.96, 0.54)}
def region_mask(shape, box, region, soft=7):
    x, y, w, h = box; r = REGIONS[region]
    x0, y0, x1, y1 = int(x+w*r[0]), int(y+h*r[1]), int(x+w*r[2]), int(y+h*r[3])
    m = np.zeros(shape[:2], np.float32)
    cv2.ellipse(m, ((x0+x1)//2, (y0+y1)//2), ((x1-x0)//2, (y1-y0)//2), 0, 0, 360, 1, -1)
    return np.clip(cv2.GaussianBlur(m, (0, 0), (x1-x0)/soft)*1.8, 0, 1)[..., None]

"""Align an image edit to the base portrait and keep ONLY the mouth or eye region from it.
Image editors redraw the whole picture slightly; pasting just the region keeps the head identical.
Usage: python3 paste.py <base.jpg> <edit.jpg> <mouth|eyes> <out.jpg>"""
import cv2, numpy as np, sys, os
sys.path.insert(0, os.path.dirname(__file__)); from face import face_box, region_mask
b = cv2.imread(sys.argv[1]); e = cv2.imread(sys.argv[2]); reg = sys.argv[3]
g = cv2.cvtColor(b, cv2.COLOR_BGR2GRAY); orb = cv2.ORB_create(5000); kb, db = orb.detectAndCompute(g, None)
e = cv2.resize(e, (b.shape[1], b.shape[0])); ke, de = orb.detectAndCompute(cv2.cvtColor(e, cv2.COLOR_BGR2GRAY), None)
m = sorted(cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True).match(de, db), key=lambda m: m.distance)[:600]
M, _ = cv2.estimateAffinePartial2D(np.float32([ke[i.queryIdx].pt for i in m]), np.float32([kb[i.trainIdx].pt for i in m]), method=cv2.RANSAC)
e = cv2.warpAffine(e, M, (b.shape[1], b.shape[0]), borderMode=cv2.BORDER_REPLICATE)
mask = region_mask(b.shape, face_box(b), reg)
cv2.imwrite(sys.argv[4], (e*mask + b*(1-mask)).clip(0, 255).astype(np.uint8), [cv2.IMWRITE_JPEG_QUALITY, 93])

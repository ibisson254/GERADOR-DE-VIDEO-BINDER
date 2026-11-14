"""Máscara de desgaste da tinta (falhas e grão) usada por compor.CSS: python3 -I desgaste.py saida.png"""
import sys, numpy as np, cv2
r = np.random.default_rng(7); n = 520
a = cv2.GaussianBlur(r.random((n, n)).astype(np.float32), (0, 0), 1.2)
b = cv2.GaussianBlur(r.random((n, n)).astype(np.float32), (0, 0), 6)
a = (a - a.min()) / (a.max() - a.min()); b = (b - b.min()) / (b.max() - b.min())
m = np.where((a * .55 + b * .45) < .28, 0, 255).astype(np.uint8)
alpha = cv2.GaussianBlur(m, (0, 0), .6)
out = np.dstack([np.zeros_like(m)] * 3 + [alpha])
cv2.imwrite(sys.argv[1], out)

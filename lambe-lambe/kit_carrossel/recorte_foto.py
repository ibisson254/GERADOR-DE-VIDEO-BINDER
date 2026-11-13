"""Foto do artista em recorte P&B com borda de papel rasgado (referência «Jhon Avon» do fundador).
recorte(base, foto_bgr, mascara, cx, topo, altura, ang) -> base com a foto colada"""
import cv2, numpy as np
from compor import colar
def recorte(base, f, m, cx, topo, alt, ang=0, borda=18, seed=4):
    s = alt/f.shape[0]; f = cv2.resize(f,None,fx=s,fy=s,interpolation=cv2.INTER_CUBIC); m = cv2.resize(m,None,fx=s,fy=s)
    h,w = m.shape
    # P&B de jornal: contraste forte, grão
    g = cv2.cvtColor(f,cv2.COLOR_BGR2GRAY).astype(np.float32)
    g = cv2.createCLAHE(2.0,(4,4)).apply(g.astype(np.uint8)).astype(np.float32)
    g = np.clip((g-118)*1.35+122,0,255)
    rng = np.random.default_rng(seed); g = np.clip(g+rng.normal(0,9,g.shape),0,255)
    papel = cv2.resize(cv2.imread('kit_papel.png'),(w,h)).astype(np.float32)
    papel = papel*0.45+np.array([228,230,232],np.float32)*0.55; foto = np.clip(papel*(g[...,None]/235.0),0,255).astype(np.uint8)
    # corte de baixo rasgado
    yy,xx = np.mgrid[0:h,0:w]; base_y = h-8-np.cumsum(rng.normal(0,1.2,w)).clip(-10,10)
    corte = (yy < base_y[None,:]).astype(np.uint8)*255
    m = cv2.min(m, corte)
    # borda de papel branco irregular
    pad = borda+12; M = cv2.copyMakeBorder(m,pad,pad,pad,pad,cv2.BORDER_CONSTANT,0)
    F = cv2.copyMakeBorder(foto,pad,pad,pad,pad,cv2.BORDER_CONSTANT,0)
    nz = cv2.GaussianBlur(rng.random(M.shape).astype(np.float32),(0,0),3); nz=(nz-nz.min())/(nz.max()-nz.min())
    dist = cv2.distanceTransform((M<128).astype(np.uint8),cv2.DIST_L2,5)
    lim = borda*(0.55+0.7*nz)
    B = ((dist<lim)|(M>127)).astype(np.uint8)*255
    B = cv2.morphologyEx(B,cv2.MORPH_OPEN,np.ones((3,3),np.uint8))
    hb,wb = B.shape
    branco = (cv2.resize(cv2.imread('kit_papel.png'),(wb,hb)).astype(np.float32)*0.35+np.array([238,240,242])*0.65).astype(np.uint8)
    base = colar(base, branco, B, cx, topo+hb/2-pad, ang)
    base = colar(base, F, cv2.GaussianBlur(M,(0,0),.8), cx, topo+hb/2-pad, ang, sombra=False)
    return base

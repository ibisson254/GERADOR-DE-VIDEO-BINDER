import numpy as np, cv2
def grabcut(im, pr_box, fg_box, bg_boxes=(), it=6):
    H,W=im.shape[:2]; m=np.full((H,W),cv2.GC_BGD,np.uint8)
    x0,y0,x1,y1=pr_box; m[y0:y1,x0:x1]=cv2.GC_PR_FGD
    x0,y0,x1,y1=fg_box; m[y0:y1,x0:x1]=cv2.GC_FGD
    for x0,y0,x1,y1 in bg_boxes: m[y0:y1,x0:x1]=cv2.GC_BGD
    a=np.zeros((1,65)); b=np.zeros((1,65)); cv2.grabCut(im,m,None,a,b,it,cv2.GC_INIT_WITH_MASK)
    pm=np.where((m==1)|(m==3),255,0).astype(np.uint8)
    pm=cv2.morphologyEx(pm,cv2.MORPH_OPEN,np.ones((5,5),np.uint8))
    n,lab,st,_=cv2.connectedComponentsWithStats(pm); k=1+np.argmax(st[1:,4])
    pm=np.where(lab==k,255,0).astype(np.uint8)
    return cv2.morphologyEx(pm,cv2.MORPH_CLOSE,np.ones((9,9),np.uint8))
def limpar(im, box, sel, dil=5, raio=7, proteger=None, seed=1):
    """apaga texto dentro de box: inpaint em baixa resolução + grão sintético com o desvio do papel à volta"""
    x0,y0,x1,y1=box; roi=im[y0:y1,x0:x1].copy()
    m=(sel(roi)).astype(np.uint8)*255
    if proteger is not None: m[proteger[y0:y1,x0:x1]>0]=0
    m=cv2.dilate(m,np.ones((dil,dil),np.uint8))
    fill=cv2.inpaint(roi,m,raio,cv2.INPAINT_TELEA)
    lp=cv2.GaussianBlur(fill.astype(np.float32),(0,0),6)
    # grão: desvio padrão local do papel fora do texto
    f=roi.astype(np.float32); hp=f-cv2.GaussianBlur(f,(0,0),3)
    fora=(m==0); sd=hp[fora].std(0) if fora.sum()>500 else np.array([10,10,10],np.float32)
    rng=np.random.default_rng(seed); n=rng.normal(0,1,roi.shape[:2]).astype(np.float32)
    n=cv2.GaussianBlur(n,(0,0),0.9); n=n/n.std()
    n2=cv2.GaussianBlur(rng.normal(0,1,roi.shape[:2]).astype(np.float32),(0,0),2.5); n2=n2/n2.std()
    g1=(n*0.55+n2*0.35)[...,None]*sd.mean(); tex=lp+g1
    mm=np.clip(cv2.GaussianBlur(m,(0,0),5)/255.0*1.6,0,1)[...,None]
    out=roi.astype(np.float32)*(1-mm)+tex*mm
    im[y0:y1,x0:x1]=np.clip(out,0,255).astype(np.uint8)
    return im
def transferir_textura(arte, velha, mask, k=1.0):
    """arte nova com a pincelada (alta frequência) da pintura velha"""
    v=velha.astype(np.float32).mean(2); hp=v-cv2.GaussianBlur(v,(0,0),1.6)
    hp=np.clip(hp,-14,14)[...,None]
    return np.clip(arte.astype(np.float32)+hp*k,0,255).astype(np.uint8)
def cobrir(arte_path, W, H, foco=(0.5,0.5)):
    a=cv2.imread(arte_path); ah,aw=a.shape[:2]; s=max(W/aw,H/ah)
    a=cv2.resize(a,(int(aw*s+1),int(ah*s+1)),interpolation=cv2.INTER_LANCZOS4)
    ox=int((a.shape[1]-W)*foco[0]); oy=int((a.shape[0]-H)*foco[1])
    return a[oy:oy+H,ox:ox+W]

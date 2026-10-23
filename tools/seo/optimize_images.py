"""Make WebP copies (max 1600px, q80) of heavy images, point <img> at them, add width/height, lazy-load.
Run from repo root. SKIP env: comma list of html files not to touch."""
import re,os,glob
from PIL import Image
SKIP=set(os.environ.get('SKIP','product__spine-mt-core.html').split(','))
def webp(src):
    if not re.search(r'\.(png|jpe?g)$',src,re.I) or not os.path.exists(src) or os.path.getsize(src)<40_000: return src
    out=re.sub(r'\.(png|jpe?g)$','.webp',src,flags=re.I)
    if not os.path.exists(out):
        im=Image.open(src); im=im.convert('RGBA' if im.mode in('RGBA','LA','P') else 'RGB')
        if im.width>1600: im=im.resize((1600,round(im.height*1600/im.width)),Image.LANCZOS)
        im.save(out,'WEBP',quality=80,method=6)
    return out if os.path.getsize(out)<os.path.getsize(src) else src
for f in glob.glob('*.html'):
    if f in SKIP: continue
    h=open(f,encoding='utf-8').read(); n=[0]
    def fix(m):
        t=m.group(0); s=re.search(r'\bsrc="([^"]+)"',t)
        if not s or s.group(1).startswith(('http','data:')): return t
        new=webp(s.group(1)); t=t.replace(s.group(0),f'src="{new}"')
        if os.path.exists(new) and 'width=' not in t:
            try:
                w,hh=Image.open(new).size; t=t.replace('<img',f'<img width="{w}" height="{hh}"',1)
            except Exception: pass
        n[0]+=1
        if n[0]>3 and 'loading=' not in t: t=t.replace('<img','<img loading="lazy" decoding="async"',1)
        return t
    h=re.sub(r'<img\b[^>]*>',fix,h)
    open(f,'w',encoding='utf-8').write(h)
print('ok')

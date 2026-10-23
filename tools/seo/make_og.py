"""Generate 1200x630 OG images into og/. Run from repo root: python3 tools/seo/make_og.py"""
import json
from PIL import Image, ImageDraw, ImageFont, features
assert features.check('raqm'), 'needs libraqm for Hebrew RTL'
F='/usr/share/fonts/truetype/sand-box/google/Rubik/Rubik-VariableFont_wght.ttf'
LOGO='assets/img/78c8016e_065b79d68_I-GroupNewLogo2.png'
NAVY=(0,52,113); BLUE=(11,94,215)
def font(sz):
    f=ImageFont.truetype(F,sz)
    try: f.set_variation_by_name('Bold')
    except Exception: pass
    return f
def fit(img,box):
    img=img.convert('RGBA'); img.thumbnail(box,Image.LANCZOS); return img
def base():
    im=Image.new('RGB',(1200,630),(255,255,255)); dr=ImageDraw.Draw(im)
    for y in range(630):  # soft gradient
        c=int(255-y*20/630); dr.line([(0,y),(1200,y)],fill=(c-8,c-2,255))
    dr.rectangle([0,600,1200,630],fill=NAVY); dr.rectangle([0,594,1200,600],fill=BLUE)
    return im,dr
def text_rtl(dr,xy,s,sz,fill,maxw):
    while sz>28 and dr.textlength(s,font=font(sz),direction='rtl')>maxw: sz-=2
    dr.text(xy,s,font=font(sz),fill=fill,anchor='ra',direction='rtl',language='he')
def product(name,sub,src,out):
    im,dr=base()
    card=Image.new('RGBA',(520,500),(255,255,255,255)); im.paste(card,(50,50),card)
    p=fit(Image.open(src),(480,460)); im.paste(p,(50+(520-p.width)//2,50+(500-p.height)//2),p)
    lg=fit(Image.open(LOGO),(260,110)); im.paste(lg,(1150-lg.width,50),lg)
    text_rtl(dr,(1150,220),name,64,NAVY,540)
    text_rtl(dr,(1150,320),sub,34,BLUE,540)
    text_rtl(dr,(1150,500),'I-Group Medical Tech | i-group.co.il',26,(90,100,120),540)
    im.save(out,'JPEG',quality=88)
def generic(title,out):
    im,dr=base()
    lg=fit(Image.open(LOGO),(560,260)); im.paste(lg,((1200-lg.width)//2,90),lg)
    dr.text((600,420),title,font=font(46),fill=NAVY,anchor='ma',direction='rtl',language='he')
    dr.text((600,500),'I-Group Medical Tech | i-group.co.il',font=font(28),fill=BLUE,anchor='ma')
    im.save(out,'JPEG',quality=88)
if __name__=='__main__':
    d=json.load(open('tools/seo/pages.json'))
    generic('טכנולוגיות רפואיות מתקדמות לשיקום וכאב','og/default.jpg')
    for f,v in d.items():
        slug=f[:-5].replace('__','-')
        if v.get('img'):
            product(v['name'],v['t'].split(' – ')[0].split(' | ')[0],v['img'],f'og/{slug}.jpg'); v['og']=f'og/{slug}.jpg'
        else: v['og']='og/default.jpg'
    json.dump(d,open('tools/seo/pages.json','w'),ensure_ascii=False,indent=1)

# -*- coding: utf-8 -*-
"""Idempotent on-page SEO: FAQ (+FAQPage JSON-LD), related links, Hebrew alts, H1 subtitles, footer links, stub redirects.
Run from repo root after new_pages.py; then make_og.py and apply_seo.py. Never touches files in SKIP."""
import json,re,glob,os,html as H
from content_data import *
import new_pages
SKIP=set(os.environ.get('SKIP','product__spine-mt-core.html').split(','))
d=json.load(open('tools/seo/pages.json'))
FAQ['gen']=new_pages.GEN
T='style="color: rgb(11, 94, 215);"'
def block(name,inner): return f'<!-- {name}:start -->{inner}<!-- {name}:end -->'
def strip(h,name): return re.sub(rf'<!-- {name}:start -->.*?<!-- {name}:end -->','',h,flags=re.S)
def faq_html(key):
    qa=FAQ[key]
    items=''.join(f'<details class="bg-card rounded-2xl border border-border/50 p-5 mb-3"><summary class="font-semibold cursor-pointer" {T}>{H.escape(q)}</summary><p class="text-sm text-muted-foreground leading-relaxed mt-3">{H.escape(a)}</p></details>' for q,a in qa)
    ld={"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in qa]}
    return (f'<section class="py-12" id="faq"><div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8"><h2 class="text-2xl md:text-3xl font-bold mb-6 text-center" {T}>שאלות נפוצות</h2>{items}'
            f'<p class="text-xs text-muted-foreground mt-4">{DISC}</p></div></section>'
            '<script type="application/ld+json">'+json.dumps(ld,ensure_ascii=False)+'</script>')
def related_html(f):
    rel=[]
    for g in GROUPS:
        if f in g: rel+= [x for x in g if x!=f and x not in rel]
    if not rel: return ''
    if f!='clinic-equipment.html' and 'clinic-equipment.html' not in rel: rel.append('clinic-equipment.html')
    links=''.join(f'<a href="{x}" class="inline-block rounded-full border border-border/60 px-4 py-2 text-sm hover:bg-primary/10" {T}>{LINKS[x]}</a>' for x in rel)
    return f'<section class="py-10 bg-secondary/30"><div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8"><h2 class="text-xl md:text-2xl font-bold mb-4 text-center" {T}>מוצרים ונושאים קשורים</h2><nav aria-label="מוצרים קשורים" class="flex flex-wrap gap-3 justify-center">{links}</nav></div></section>'
FOOT=['shockwave-therapy.html','spinal-decompression.html','magnetotherapy.html','clinic-equipment.html','product__ultrawave-lgt-2620.html','product__powershocker-lgt-2500s-plus.html']
FOOTLBL={'product__ultrawave-lgt-2620.html':'Ultrawave LGT-2620 גלי הלם','product__powershocker-lgt-2500s-plus.html':'PowerShocker גלי הלם רדיאליים'}
def has_heb(s): return re.search('[\u0590-\u05FF]',s)
def fix_alts(f,h,name,kw):
    def rep(m):
        t=m.group(0); src=(re.search(r'src="([^"]*)"',t) or [None,''])[1]
        a=re.search(r'\balt="([^"]*)"',t); alt=a.group(1) if a else None
        if '71165688_tr' in src or src.endswith('.html'): new=''   # tracking pixel / iframe stub: decorative
        elif 'I-GroupNewLogo' in src: new='לוגו איי גרופ – I-Group Medical Tech'
        elif alt in (None,'','[object Object]'):
            nxt=re.sub('<[^>]+>','',(re.search(r'<h[2-4][^>]*>(.*?)</h[2-4]>',h[m.end():m.end()+3000],re.S) or [None,''])[1]).strip()
            new=(nxt+' – ' if nxt else '')+(name or 'איי גרופ')
            if 'magnetoter' in src or 'images' in src: new=f'מגנטותרפיה Biomag – {nxt or name}'
        elif re.search('[\u0600-\u06FF\u0400-\u04FF]',alt) or alt.startswith(('סרטון','ספיין','הכרות')):
            new=f'תמונה ממוזערת לסרטון על {name}' + (f' – {alt}' if has_heb(alt) and not re.search('[\u0600-\u06FF]',alt) else '')
        elif not has_heb(alt): new=f'{alt} – {kw or name}'
        elif len(alt)<16 and name and name not in alt: new=f'{alt} – {name}'
        else: return t
        new=H.escape(H.unescape(new),quote=True)
        return t.replace(a.group(0),f'alt="{new}"') if a else t.replace('<img',f'<img alt="{new}"',1)
    return re.sub(r'<img\b[^>]*>',rep,h)
n=dict(faq=0,rel=0,alt=0,h1=0,foot=0)
for f in sorted(glob.glob('*.html')):
    if f in SKIP: continue
    h=open(f,encoding='utf-8').read(); o=h
    if f in STUBS:
        to=STUBS[f]; d[f]['nf']=1; d[f]['canon']=to
        h=re.sub(r'<body.*</body>',f'<body><meta http-equiv="refresh" content="0; url={to}"><p style="font-family:sans-serif;text-align:center;margin-top:20vh">העמוד עבר. <a href="{to}">המשך לעמוד החדש</a></p></body>',h,flags=re.S)
        open(f,'w',encoding='utf-8').write(h); continue
    for k in ('faq','related','footlinks','h1sub'): h=strip(h,k)
    name=d.get(f,{}).get('name') or re.sub('<[^>]+>','',(re.search(r'<h1[^>]*>(.*?)</h1>',h,re.S) or [None,''])[1]).strip()
    key,kw=PAGES.get(f,(d.get(f,{}).get('faq'),None))
    # H1 keyword subtitle
    if kw: h=re.sub(r'(<h1\b[^>]*>)(.*?)(</h1>)',lambda m:m.group(1)+m.group(2)+block('h1sub',f'<span style="display:block;font-size:.55em;font-weight:600;margin-top:.25em">{kw}</span>')+m.group(3),h,count=1,flags=re.S); n['h1']+=1
    tail=''
    if key: tail+=faq_html(key); n['faq']+=1
    r=related_html(f)
    if r: tail+=r; n['rel']+=1
    if tail: h=h.replace('<footer',block('related' if not key else 'faq',tail)+'<footer',1)
    # footer links
    lis=''.join(f'<li><a class="text-sm text-background/50 hover:text-primary transition-colors" href="{x}">{FOOTLBL.get(x,LINKS[x])}</a></li>' for x in FOOT)
    h2=re.sub(r'(href="product__lgt-2410s.html">[^<]*</a></li>)',lambda m:m.group(1)+block('footlinks',lis),h,count=1)
    if h2!=h: n['foot']+=1; h=h2
    before=h; h=fix_alts(f,h,name,kw); n['alt']+=sum(1 for a,b in zip(re.findall(r'alt="[^"]*"',before),re.findall(r'alt="[^"]*"',h)) if a!=b)
    if h!=o: open(f,'w',encoding='utf-8').write(h)
json.dump(d,open('tools/seo/pages.json','w'),ensure_ascii=False,indent=1)
print(n)

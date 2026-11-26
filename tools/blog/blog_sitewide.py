"""Add /blog/ to nav, footer and sitemap (idempotent). Run from repo root, then rebuild blog."""
import glob,re
NAVCLS='px-4 py-2 text-sm font-medium rounded-lg transition-all duration-300 text-white/70 hover:text-white hover:bg-white/10'
FL='<li><a class="text-sm text-background/50 hover:text-primary transition-colors" href="/blog/">בלוג – מדריכים ומאמרים</a></li>'
n=0
for f in glob.glob('*.html')+glob.glob('product/*.html')+glob.glob('kin/product/*.html'):
    h=open(f,encoding='utf-8').read(); o=h
    if 'העמוד עבר' in h: continue
    if 'href="/blog/" class="'+NAVCLS not in h:
        h=h.replace(f'>כירופרקטיקה</a>',f'>כירופרקטיקה</a><a href="/blog/" class="{NAVCLS}">בלוג</a>',1)
    if '<!-- footlinks:end -->' in h and 'href="/blog/">' not in h:
        h=h.replace('<!-- footlinks:end -->',FL+'<!-- footlinks:end -->',1)
    if h!=o: open(f,'w',encoding='utf-8').write(h); n+=1
sm=open('sitemap.xml',encoding='utf-8').read()
import json
urls=['/blog/']+['/blog/'+a['slug'] for a in json.load(open('tools/blog/articles.json'))]
for u in urls:
    if f'<loc>https://i-group.co.il{u}</loc>' not in sm:
        sm=sm.replace('</urlset>',f'  <url><loc>https://i-group.co.il{u}</loc><lastmod>2026-11-26</lastmod></url>\n</urlset>')
open('sitemap.xml','w',encoding='utf-8').write(sm); print(n,'pages updated')

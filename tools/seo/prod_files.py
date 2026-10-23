"""Write production sitemap.xml / robots.txt / redirects.csv into /workspace/seo (NOT into the preview site)."""
import json,datetime,csv,subprocess
SITE='https://i-group.co.il'
d=json.load(open('tools/seo/pages.json'))
route=lambda f:'/' if f=='index.html' else '/'+f[:-5].replace('__','/')
EX=('thank-you','consultations','privacy','terms','accessibility','cancellation')
today=datetime.date.today().isoformat()
urls=[]
for f,v in d.items():
    if v.get('nf') or f.startswith(EX): continue
    try: lm=subprocess.check_output(['git','log','-1','--format=%cs','--',f],text=True).strip() or today
    except Exception: lm=today
    urls.append(f'  <url><loc>{SITE}{route(f)}</loc><lastmod>{lm}</lastmod></url>')
open('/workspace/seo/sitemap.xml','w').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+'\n'.join(urls)+'\n</urlset>\n')
open('/workspace/seo/robots.txt','w').write(f'User-agent: *\nAllow: /\nDisallow: /consultations\nDisallow: /thank-you/\n\nSitemap: {SITE}/sitemap.xml\n')
live=['/','/product/biomag-lumina','/cryotherapy','/vet','/kin','/privacy','/terms','/accessibility','/address','/cancellation','/phone-consultation','/consultations','/thank-you/demo','/thank-you/contact','/thank-you/newsletter','/thank-you/consultation']
rows=[]
for f,v in d.items():
    r=route(f)
    if v.get('canon'): rows.append((r,route(v['canon']),'301','old product URL renders "product not found" on Base44; merge into replacement'))
    else: rows.append((r,r,'200 (same path)','served by '+f+(' – in live sitemap' if r in live else ' – found via site links')))
for r in ['/index','/home']: rows.append((r,'/','301','common legacy alias'))
for r in ['/product/focuswave-lgt-2620','/shockwave','/decompression']: rows.append((r,{'/product/focuswave-lgt-2620':'/product/ultrawave-lgt-2620','/shockwave':'/shockwave-therapy','/decompression':'/spinal-decompression'}[r],'301','defensive alias (optional)'))
for r in ['/shock','/back','/sport','/lazer','/ultra','/brain','/women','/wond','/manual','/3age','/oxygen','/yoga','/trial','/testimonials','/book','/consult-booking','/consult-instrumentation','/docs']:
    rows.append((r,'','REVIEW','route found only in base44_backup_20261001.zip app.js – that bundle looks like a different Base44 app (clinic booking); not on live i-group sitemap. Confirm before adding a 301'))
with open('/workspace/seo/redirects.csv','w',newline='') as fh:
    w=csv.writer(fh); w.writerow(['old_path','new_path','status','note']); w.writerows(rows)
print(len(urls),'urls;',len(rows),'redirect rows')

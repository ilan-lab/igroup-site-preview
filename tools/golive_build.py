"""Go-live restructure for GitHub Pages at domain root (https://i-group.co.il/).
- flat a__b__c.html -> a/b/c.html (GitHub Pages serves /a/b/c from a/b/c.html, 200, no trailing-slash redirect)
- every internal href/src -> root-relative
- 301 rows of redirects.csv -> static stubs; /consultations -> noindex stub to home
- production robots.txt + sitemap.xml at root. Run from repo root, once (idempotent-ish)."""
import re,glob,os,csv,subprocess,shutil,html as H
SITE='https://i-group.co.il'
def route(f): return '/' if f=='index.html' else '/'+f[:-5].replace('__','/')
def target(f): return f.replace('__','/')
flat=sorted(glob.glob('*.html'))
def rew(h):
    def href(m):
        a,v=m.group(1),m.group(2)
        if re.match(r'(https?:|mailto:|tel:|#|/|data:|javascript:)',v): return m.group(0)
        mm=re.match(r'([\w.-]+)\.html(#.*)?$',v)
        if mm and mm.group(1)+'.html' in flat: return f'{a}="{route(mm.group(1)+".html")}{mm.group(2) or ""}"'
        if v.startswith(('assets/','og/')): return f'{a}="/{v}"'
        return m.group(0)
    return re.sub(r'\b(href|src|poster)="([^"]*)"',href,h)
for f in flat:
    h=rew(open(f,encoding='utf-8').read())
    t=target(f); os.makedirs(os.path.dirname(t) or '.',exist_ok=True)
    if t!=f: subprocess.run(['git','mv','-f',f,t],check=True)
    open(t,'w',encoding='utf-8').write(h)
# /kin also as kin/index.html fallback in case Pages prefers the directory
shutil.copy('kin.html','kin/index.html')
def stub(path,to,noindex=False):
    url=SITE+to; f=path.strip('/')+'.html'
    os.makedirs(os.path.dirname(f) or '.',exist_ok=True)
    rob='<meta name="robots" content="noindex,nofollow">' if noindex else ''
    open(f,'w',encoding='utf-8').write(f'''<!DOCTYPE html><html lang="he" dir="rtl"><head><meta charset="utf-8"><title>העמוד עבר | איי גרופ</title>{rob}
<link rel="canonical" href="{url}"><meta http-equiv="refresh" content="0; url={to}">
<script>location.replace("{to}"+location.hash)</script></head>
<body><p style="font-family:sans-serif;text-align:center;margin-top:20vh">העמוד עבר. <a href="{to}">המשך לעמוד החדש</a></p></body></html>
''')
    return f
made=[]
for r in csv.DictReader(open('tools/seo/production/redirects.csv',encoding='utf-8')):
    if r['status'].strip()=='301' and r['old_path'] not in ('/index',):
        made.append(stub(r['old_path'],r['new_path']))
made.append(stub('/consultations','/',noindex=True))
for x in ('robots.txt','sitemap.xml'): shutil.copy('tools/seo/production/'+x,x)
open('.nojekyll','w').close()
print('stubs:',made)

"""Page weight = HTML + <img> + linked css/js (local files). Usage: python3 tools/seo/weight.py page.html ..."""
import re,os,sys
for f in sys.argv[1:]:
    h=open(f,encoding='utf-8').read(); tot=len(h.encode()); imgs=0; seen=set()
    for s in re.findall(r'<img\b[^>]*\bsrc="([^"]+)"',h)+re.findall(r'(?:href|src)="(assets/[^"]+\.(?:css|js))"',h):
        if s in seen or not os.path.exists(s): continue
        seen.add(s); n=os.path.getsize(s); tot+=n; imgs+=n if not s.endswith(('.css','.js')) else 0
    print(f"{f}: total {tot/1024:.0f} KB (images {imgs/1024:.0f} KB)")

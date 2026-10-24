"""Idempotent post-process: turn dead React <button>s into real <a> links, fix tel button,
add floating WhatsApp button. Usage: python3 fix_nav.py [root_dir]"""
import re, os, sys
ROOT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
NAV = {'דף הבית': '/', 'טכנולוגיות': '/#products', 'קריותרפיה': '/cryotherapy', 'קינסיותרפיה': '/kin',
       'וטרינריה': '/vet', 'שירותים': '/#services', 'צור קשר': '/#contact', 'צור קשר להדגמה': '/#contact',
       'גלה את הטכנולוגיות שלנו': '/#products', 'חומר מחקרי': '/#clinical-research', 'חזרה לעמוד הבית': '/'}
HOME_ANCHOR = {'/#products': '#products', '/#services': '#services', '/#contact': '#contact', '/#clinical-research': '#clinical-research'}
WA = ('<a id="wa-float" href="https://wa.me/972549007723?text=%D7%A4%D7%A0%D7%99%D7%99%D7%94%20%D7%9E%D7%94%D7%90%D7%AA%D7%A8" '
      'target="_blank" rel="noopener" aria-label="WhatsApp" style="position:fixed;left:16px;bottom:calc(16px + env(safe-area-inset-bottom));'
      'z-index:2147483000;width:56px;height:56px;border-radius:50%;background:#25D366;display:flex;align-items:center;justify-content:center;'
      'box-shadow:0 4px 14px rgba(0,0,0,.3)"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" width="30" height="30" fill="#fff" aria-hidden="true">'
      '<path d="M16.04 3C8.86 3 3.02 8.83 3.02 16c0 2.29.6 4.53 1.74 6.5L3 29l6.68-1.75A13 13 0 0 0 16.04 29C23.2 29 29 23.17 29 16S23.2 3 16.04 3zm0 23.8c-2 0-3.96-.54-5.67-1.55l-.4-.24-3.97 1.04 1.06-3.86-.26-.4A10.77 10.77 0 0 1 5.25 16c0-5.95 4.84-10.8 10.8-10.8 5.94 0 10.77 4.85 10.77 10.8 0 5.95-4.84 10.8-10.78 10.8zm5.92-8.08c-.32-.16-1.92-.95-2.22-1.06-.3-.1-.51-.16-.73.16-.21.33-.83 1.06-1.02 1.28-.19.21-.37.24-.7.08-.32-.16-1.36-.5-2.6-1.6-.96-.86-1.6-1.91-1.8-2.23-.18-.33-.02-.5.15-.66.14-.15.32-.38.49-.57.16-.19.21-.33.32-.54.1-.22.05-.4-.03-.57-.08-.16-.72-1.74-.99-2.38-.26-.63-.53-.54-.73-.55h-.62c-.21 0-.56.08-.86.4-.3.33-1.13 1.1-1.13 2.69 0 1.58 1.16 3.11 1.32 3.33.16.21 2.28 3.48 5.52 4.88.77.33 1.37.53 1.84.68.77.25 1.48.21 2.03.13.62-.1 1.92-.79 2.19-1.55.27-.76.27-1.41.19-1.55-.08-.13-.3-.21-.62-.37z"/></svg></a>')

def fix(h, is_home):
    def btn(m):
        attrs, inner = m.group(1), m.group(2)
        label = re.sub(r'<[^>]+>', '', inner).strip()
        if label not in NAV: return m.group(0)
        url = NAV[label]
        if is_home: url = HOME_ANCHOR.get(url, url)
        return f'<a href="{url}"{attrs}>{inner}</a>'
    # tel: <a href="tel:..." ...><button CLS>X</button></a>  ->  <a href="tel:..." CLS>X</a>
    h = re.sub(r'<a href="tel:0549007723"([^>]*)><button([^>]*)>(.*?)</button></a>',
               lambda m: f'<a href="tel:0549007723"{m.group(2)}{" data-wrap" if False else ""}>{m.group(3)}</a>'.replace(
                   'class="', 'class="' + (re.search(r'class="([^"]*)"', m.group(1)).group(1) + ' ' if re.search(r'class="([^"]*)"', m.group(1)) else ''), 1),
               h, flags=re.S)
    h = re.sub(r'<button([^>]*)>((?:(?!</?button).)*?)</button>', btn, h, flags=re.S)
    if 'id="wa-float"' not in h and '</body>' in h:
        h = h.replace('</body>', WA + '</body>', 1)
    return h

n = 0
for d, _, fs in os.walk(ROOT):
    if '/.git' in d or '/tools' in d: continue
    for f in fs:
        if not f.endswith('.html'): continue
        p = os.path.join(d, f); h = open(p, encoding='utf-8').read()
        if 'http-equiv="refresh"' in h: continue  # redirect stubs
        rel = os.path.relpath(p, ROOT)
        nh = fix(h, rel == 'index.html')
        if nh != h: open(p, 'w', encoding='utf-8').write(nh); n += 1
print('fix_nav: updated', n, 'files')

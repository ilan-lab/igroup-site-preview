"""Embed the focused-vs-radial YouTube film on every shockwave page.
Idempotent. Run from repo root: python3 tools/seo/embed_shockwave_video.py
"""
import re, sys
from pathlib import Path
sys.path.insert(0, 'tools/seo')
from youtube_video import video_ld_script, video_section, video_blog_block, TOC_LI, MARK

ROOT = Path('.')

PRODUCT_AND_TOPIC = [
    # (path, use alt background on the new section)
    ('shockwave-devices.html', True),
    ('shockwave-therapy.html', True),
    ('product/ultrawave-lgt-2620.html', False),
    ('product/powershocker-lgt-2500s-plus.html', False),
]

BLOG = [
    # (path, insert after this unique snippet)
    (
        'blog/focused-vs-radial-shockwave.html',
        'רק מה שחשוב כדי לקבל החלטה טובה.</p>',
        'start',  # TOC position: start of ol
    ),
    (
        'blog/what-is-shockwave-therapy.html',
        'href="/blog/focused-vs-radial-shockwave">גלי הלם ממוקדים מול רדיאליים – מה לבחור לקליניקה</a>.</p>',
        'after-s2',
    ),
]

def strip_existing(html):
    html = re.sub(rf'<!-- {MARK}:start -->.*?<!-- {MARK}:end -->', '', html, flags=re.S)
    html = re.sub(rf'<!-- {MARK}-ld:start -->.*?<!-- {MARK}-ld:end -->', '', html, flags=re.S)
    # also remove a leftover TOC li if re-running
    html = html.replace(TOC_LI, '')
    return html

def insert_ld(html):
    if f'<!-- {MARK}-ld:start -->' in html:
        return html
    if '<!-- seo:end -->' not in html:
        raise SystemExit('missing <!-- seo:end -->')
    return html.replace('<!-- seo:end -->', video_ld_script() + '\n<!-- seo:end -->', 1)

def insert_after_hero(html, alt):
    # first </section> after the visible h1 (color style) — the hero
    m = re.search(r'<h1 class="text-3xl md:text-4xl font-bold mb-2".*?</section>', html, re.S)
    if not m:
        raise SystemExit('could not find hero section after h1')
    return html[:m.end()] + video_section(alt=alt) + html[m.end():]

def insert_blog(html, after, toc_mode):
    idx = html.find(after)
    if idx < 0:
        raise SystemExit(f'anchor not found: {after[:60]}')
    at = idx + len(after)
    html = html[:at] + video_blog_block() + html[at:]
    # TOC
    if toc_mode == 'start':
        html = html.replace('<ol>', '<ol>' + TOC_LI, 1)
    elif toc_mode == 'after-s2':
        needle = '<li><a href="#s2">שני סוגים עיקריים: ממוקדים ורדיאליים</a></li>'
        if needle not in html:
            raise SystemExit('s2 TOC item not found')
        html = html.replace(needle, needle + TOC_LI, 1)
    return html

def patch(path, fn):
    p = ROOT / path
    html = p.read_text(encoding='utf-8')
    original_title = re.search(r'<title>(.*?)</title>', html, re.S).group(1)
    original_desc = re.search(r'<meta name="description" content="([^"]*)">', html).group(1)
    original_og = re.search(r'<meta property="og:image" content="([^"]*)">', html).group(1)
    html = strip_existing(html)
    html = insert_ld(html)
    html = fn(html)
    # invariants
    assert re.search(r'<title>(.*?)</title>', html, re.S).group(1) == original_title
    assert re.search(r'<meta name="description" content="([^"]*)">', html).group(1) == original_desc
    assert re.search(r'<meta property="og:image" content="([^"]*)">', html).group(1) == original_og
    assert 'youtube-nocookie.com/embed/iB6AslQP-DE' in html
    assert '"@type": "VideoObject"' in html or '"@type":"VideoObject"' in html
    assert html.count('<title>') == 1
    p.write_text(html, encoding='utf-8')
    print('patched', path, 'title_len', len(original_title), 'desc_len', len(original_desc))

def main():
    for path, alt in PRODUCT_AND_TOPIC:
        patch(path, lambda h, alt=alt: insert_after_hero(h, alt))
    for path, after, toc in BLOG:
        patch(path, lambda h, after=after, toc=toc: insert_blog(h, after, toc))

if __name__ == '__main__':
    main()

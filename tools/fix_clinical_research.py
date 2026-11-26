#!/usr/bin/env python3
"""Restore the clinical-research accordion panels lost in the static React snapshot.

The closed institution headers were exported, but the original links (from the
Base44/React KM data: two published articles and the YouTube clinical videos)
were not. This is idempotent: if the panels already contain the source URLs, it
leaves the file alone.

Usage: python3 tools/fix_clinical_research.py [root_dir]
"""
import os, re, sys

ROOT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')

# Original KM data from the React bundle (igroup_crawl/js/index.js, const KM).
# Do not invent studies; these are the targets the live React app already used.
ITEMS = [
    {
        "name": "New York Medical Group",
        "links": [
            {"title": "Chiropractic Management of Symptomatic Pedicle Hemangioma",
             "url": "https://www.researchgate.net/publication/361733422_Chiropractic_Management_of_Symptomatic_Pedicle_Hemangioma_a_Case_Report",
             "type": "research"},
            {"title": "Clinical Research Article — NCBI",
             "url": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10008232/",
             "type": "research"},
        ],
    },
    {
        "name": "Korea National Hospital",
        "links": [
            {"title": "Clinical Demonstration",
             "url": "https://www.youtube.com/watch?v=jHxR2Hys1io",
             "type": "video"},
        ],
    },
    {
        "name": "Lokmanya Hospital",
        "links": [
            {"title": "Clinical Case Presentation",
             "url": "https://www.youtube.com/watch?v=5I4EJqELNb8",
             "type": "video"},
        ],
    },
    {
        "name": "American Spine Center",
        "links": [
            {"title": "Treatment Results",
             "url": "https://www.youtube.com/watch?v=SR04Ug73Jvs&t=327s",
             "type": "video"},
            {"title": "Clinical Case Study",
             "url": "https://www.youtube.com/watch?v=SR04Ug73Jvs",
             "type": "video"},
        ],
    },
    {
        "name": "Clinical Research Institute",
        "links": [
            {"title": "Case Presentation",
             "url": "https://www.youtube.com/watch?v=5I4EJqELNb8",
             "type": "video"},
        ],
    },
    {
        "name": "International Medical Center",
        "links": [
            {"title": "Clinical Demonstration",
             "url": "https://www.youtube.com/watch?v=jHxR2Hys1io",
             "type": "video"},
        ],
    },
]

LABEL = {"research": "מאמר מחקרי", "video": "סרטון קליני"}

ICON_FILE = (
    '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" '
    'stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" '
    'class="lucide lucide-file-text w-4 h-4 text-blue-700" aria-hidden="true">'
    '<path d="M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7Z"></path>'
    '<path d="M14 2v4a2 2 0 0 0 2 2h4"></path>'
    '<path d="M10 9H8"></path><path d="M16 13H8"></path><path d="M16 17H8"></path></svg>'
)
ICON_PLAY = (
    '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="currentColor" '
    'class="lucide lucide-play w-4 h-4 text-red-600 fill-red-600" aria-hidden="true">'
    '<polygon points="6 3 20 12 6 21 6 3"></polygon></svg>'
)
ICON_EXT = (
    '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" '
    'stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" '
    'class="lucide lucide-external-link w-3.5 h-3.5 text-muted-foreground group-hover:text-primary '
    'transition-colors shrink-0" aria-hidden="true">'
    '<path d="M15 3h6v6"></path><path d="M10 14 21 3"></path>'
    '<path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path></svg>'
)

STYLE = (
    '<style>'
    '#clinical-research details > summary{list-style:none;cursor:pointer}'
    '#clinical-research details > summary::-webkit-details-marker{display:none}'
    '#clinical-research details[open] summary .lucide-chevron-down{transform:rotate(180deg)}'
    '</style>'
)
SCRIPT = (
    '<script>'
    '(function(){var s=document.getElementById("clinical-research");if(!s)return;'
    's.querySelectorAll("details").forEach(function(d){'
    'd.addEventListener("toggle",function(){'
    'if(!d.open)return;'
    's.querySelectorAll("details").forEach(function(o){if(o!==d)o.open=false});'
    '});});})();'
    '</script>'
)


def panel_html(item):
    rows = []
    for link in item["links"]:
        is_video = link["type"] == "video"
        icon_wrap = "bg-red-50" if is_video else "bg-blue-50"
        icon = ICON_PLAY if is_video else ICON_FILE
        rows.append(
            f'<a href="{link["url"]}" target="_blank" rel="noopener noreferrer" '
            f'class="flex items-center gap-3 p-3.5 rounded-lg bg-white border border-border '
            f'hover:border-primary/40 hover:shadow-sm transition-all group">'
            f'<div class="w-9 h-9 rounded-lg flex items-center justify-center shrink-0 {icon_wrap}">'
            f'{icon}</div>'
            f'<div class="flex-1 min-w-0">'
            f'<p class="font-medium text-sm truncate group-hover:text-primary transition-colors" '
            f'style="color: rgb(11, 94, 215);">{link["title"]}</p>'
            f'<p class="text-xs text-muted-foreground mt-0.5">{LABEL[link["type"]]}</p>'
            f'</div>{ICON_EXT}</a>'
        )
    return (
        '<div class="overflow-hidden">'
        '<div class="px-6 pb-5 pt-1 space-y-2 bg-secondary/20">'
        + "".join(rows) +
        '</div></div>'
    )


ITEM_RE = re.compile(
    r'<div style="">'
    r'(<button class="w-full px-6 py-5 hover:bg-secondary/40 transition-colors '
    r'flex items-center justify-between gap-4 text-start">)'
    r'(.*?)'
    r'</button></div>',
    re.S,
)


INJECT_RE = re.compile(
    r'<style>#clinical-research details.*?</style>|'
    r'<script>\(function\(\)\{var s=document\.getElementById\("clinical-research".*?</script>',
    re.S,
)

def strip_injects(html):
    return INJECT_RE.sub('', html)

def with_inject(section_html):
    section_html = strip_injects(section_html).strip()
    if not section_html.startswith('<section id="clinical-research"'):
        raise SystemExit('expected section start after stripping injects')
    if not section_html.endswith('</section>'):
        raise SystemExit('expected section end after stripping injects')
    # Style before the section; script at the end so the details exist when it runs.
    return STYLE + section_html[:-len('</section>')] + SCRIPT + '</section>'

def fix_section(sec):
    if 'pmc/articles/PMC10008232' in sec and '<details' in sec:
        new_sec = with_inject(sec)
        return new_sec, new_sec != sec

    # Drop a previously injected style/script so re-runs stay clean
    sec = strip_injects(sec)

    found = []

    def repl(m, found=found):
        open_btn, inner = m.group(1), m.group(2)
        name = None
        for item in ITEMS:
            if item["name"] in inner:
                name = item["name"]
                item_data = item
                break
        if not name:
            return m.group(0)
        found.append(name)
        summary_open = open_btn.replace("<button ", "<summary ", 1)
        return (
            f'<details>'
            f'{summary_open}{inner}</summary>'
            f'{panel_html(item_data)}'
            f'</details>'
        )

    new_sec, n = ITEM_RE.subn(repl, sec)
    expected = [i["name"] for i in ITEMS]
    if found != expected:
        raise SystemExit(f'clinical-research rewrite mismatch: found {found}, expected {expected}')
    if n != 6:
        raise SystemExit(f'clinical-research expected 6 items, replaced {n}')

    return with_inject(new_sec), True


SEC_RE = re.compile(
    r'(?:<style>#clinical-research details.*?</style>|'
    r'<script>\(function\(\)\{var s=document\.getElementById\("clinical-research".*?</script>)*'
    r'<section id="clinical-research"[^>]*>.*?</section>',
    re.S,
)


def fix_html(html):
    m = SEC_RE.search(html)
    if not m:
        return html, False
    new_sec, changed = fix_section(m.group(0))
    if not changed:
        return html, False
    return html[:m.start()] + new_sec + html[m.end():], True


def main():
    updated = 0
    scanned = 0
    for d, _, fs in os.walk(ROOT):
        if "/.git" in d or "/tools" in d:
            continue
        for f in fs:
            if not f.endswith(".html"):
                continue
            path = os.path.join(d, f)
            html = open(path, encoding="utf-8").read()
            if 'id="clinical-research"' not in html:
                continue
            scanned += 1
            new_html, changed = fix_html(html)
            if changed:
                open(path, "w", encoding="utf-8").write(new_html)
                updated += 1
                print("updated", os.path.relpath(path, ROOT))
            else:
                print("already fixed", os.path.relpath(path, ROOT))
    print(f"fix_clinical_research: scanned {scanned}, updated {updated}")


if __name__ == "__main__":
    main()

"""Shared YouTube embed + VideoObject for the focused-vs-radial film (fJ9p71K2Vc0)."""
import json

VIDEO_ID = 'fJ9p71K2Vc0'
VIDEO_NAME = 'מה ההבדל בין גלי הלם ממוקדים לרדיאליים'
VIDEO_HEADING = 'צפו: ההבדל בין גלי הלם ממוקדים לרדיאליים'
VIDEO_DESC = (
    'הסבר מקצועי על ההבדל בין גלי הלם ממוקדים (אלקטרומגנטיים) לגלי הלם רדיאליים '
    '(פנאומטיים): איך כל סוג עובד, למי הוא מתאים בקליניקת פיזיותרפיה, אורתופדיה או '
    'רפואת ספורט, ומה כדאי לבדוק לפני בחירת מכשיר.'
)
THUMB = f'https://i.ytimg.com/vi/{VIDEO_ID}/maxresdefault.jpg'
WATCH = f'https://www.youtube.com/watch?v={VIDEO_ID}'
EMBED = f'https://www.youtube.com/embed/{VIDEO_ID}'
EMBED_PRIVACY = f'https://www.youtube-nocookie.com/embed/{VIDEO_ID}'
UPLOAD_DATE = '2026-11-27'
DURATION = 'PT8M25S'
MARK = 'yt-focused-vs-radial'

def video_ld():
    return {
        '@context': 'https://schema.org',
        '@type': 'VideoObject',
        'name': VIDEO_NAME,
        'description': VIDEO_DESC,
        'thumbnailUrl': THUMB,
        'uploadDate': UPLOAD_DATE,
        'duration': DURATION,
        'embedUrl': EMBED,
        'contentUrl': WATCH,
    }

def video_ld_script():
    return (
        f'<!-- {MARK}-ld:start -->'
        f'<script type="application/ld+json">{json.dumps(video_ld(), ensure_ascii=False)}</script>'
        f'<!-- {MARK}-ld:end -->'
    )

def video_iframe():
    return (
        '<div class="yt-embed rounded-2xl overflow-hidden border border-border/50 shadow-lg" '
        'style="position:relative;width:100%;aspect-ratio:16/9;background:#0b1a2b;">'
        f'<iframe src="{EMBED_PRIVACY}" title="{VIDEO_NAME}" loading="lazy" '
        'allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" '
        'allowfullscreen referrerpolicy="strict-origin-when-cross-origin" '
        'style="position:absolute;inset:0;width:100%;height:100%;border:0;"></iframe>'
        '</div>'
    )

def video_section(alt=False):
    bg = ' bg-secondary/30' if alt else ''
    return (
        f'<!-- {MARK}:start -->'
        f'<section class="py-12{bg}" aria-labelledby="yt-focused-vs-radial-h" id="video-focused-vs-radial">'
        '<div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">'
        f'<h2 id="yt-focused-vs-radial-h" class="text-2xl md:text-3xl font-bold mb-6 text-center" '
        f'style="color: rgb(11, 94, 215);">{VIDEO_HEADING}</h2>'
        f'{video_iframe()}'
        '</div></section>'
        f'<!-- {MARK}:end -->'
    )

def video_blog_block():
    return (
        f'<!-- {MARK}:start -->'
        '<div class="not-prose yt-video" id="video-focused-vs-radial" style="margin:1.75rem 0 2.25rem;">'
        f'<h2 id="yt-focused-vs-radial-h" class="text-2xl md:text-3xl font-bold mb-6 text-center" '
        f'style="color: rgb(11, 94, 215);">{VIDEO_HEADING}</h2>'
        f'{video_iframe()}'
        '</div>'
        f'<!-- {MARK}:end -->'
    )

TOC_LI = f'<li><a href="#video-focused-vs-radial">{VIDEO_HEADING}</a></li>'

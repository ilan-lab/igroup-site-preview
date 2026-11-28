"""Build /blog/ index + 5 articles from tools/blog/a*.md. Run from repo root: python3 tools/blog/build_blog.py"""
import re, json, html, sys, math
sys.path.insert(0,'tools/seo')
from nov26_pages import HEAD, FOOT, seo as _seo, crumbs, faqld, C, esc
from youtube_video import video_ld, video_blog_block, TOC_LI, VIDEO_HEADING
from make_og import product as og_product, generic as og_generic
BASE='https://i-group.co.il'; DATE='2026-11-26'; DATE_HE='26.11.2026'
LOGO_URL=BASE+'/assets/img/78c8016e_065b79d68_I-GroupNewLogo2.png'
ORG={"@type":"Organization","name":"איי גרופ – I-Group Medical Tech","url":BASE+"/","logo":{"@type":"ImageObject","url":LOGO_URL},
     "telephone":"+972-54-900-7723","address":{"@type":"PostalAddress","streetAddress":"מאיר אריאל 6","addressLocality":"נתניה","addressCountry":"IL"}}
A=[
 dict(n=1,slug='what-is-shockwave-therapy',aud='למטופלים',kw='טיפול בגלי הלם',
  title='מה זה טיפול בגלי הלם ולמי הוא מתאים? המדריך המלא | איי גרופ',
  desc='מה זה טיפול בגלי הלם (ESWT), איך הוא מרגיש, כמה טיפולים צריך, למי הוא מתאים – דורבן, אכילס, כתף ומרפק – ומתי לא מטפלים. מדריך מבוסס, ברור ופשוט.',
  h1='מה זה טיפול בגלי הלם ולמי הוא מתאים?',og_name='מה זה טיפול בגלי הלם?',og_sub='ולמי הוא מתאים | מדריך',
  img='/assets/img/feedc697_3075a8a23_Screenshot_20260608_234511_Chrome.webp',og_src='tools/seo/src/3075a8a23_Screenshot_20260608_234511_Chrome.jpg',
  faq=[('האם טיפול בגלי הלם כואב?','רוב המטופלים מתארים אי נוחות או כאב מסוים במהלך הטיפול, במיוחד באזורים רגישים. העוצמה מותאמת לסף הסבילות של המטופל, ובדרך כלל מתחילים בעוצמה נמוכה ומעלים בהדרגה.'),
       ('כמה טיפולים בגלי הלם צריך?','פרוטוקולים מקובלים כוללים לרוב 3 עד 5 מפגשים במרווח של כשבוע, ובמקרים מסוימים יותר. מספר המפגשים תלוי במצב ובתגובת המטופל, ואין הבטחה לתוצאה.'),
       ('האם גלי הלם מתאימים לטיפול בדורבן?','דורבן ופלנטר פסיאיטיס הם מההתוויות המוכרות ביותר לטיפול בגלי הלם בספרות המקצועית. ההחלטה אם לטפל ובאיזה פרוטוקול מתקבלת על ידי איש מקצוע לאחר אבחון, ולרוב בשילוב תרגול וניהול עומסים.'),
       ('מתי אסור לטפל בגלי הלם?','נגד-התוויות מקובלות כוללות היריון, הפרעות קרישה או טיפול נוגד קרישה, גידול באזור הטיפול, לוחות גדילה פתוחים, טיפול מעל ריאות, כלי דם ועצבים מרכזיים, וזיהום חריף באזור. הרשימה המלאה מופיעה בהוראות היצרן.'),
       ('מה ההבדל בין גלי הלם ממוקדים לרדיאליים?','בגלי הלם רדיאליים האנרגיה חזקה בנקודת המגע ומתפזרת, ולכן הם מתאימים למבנים שטחיים יחסית. בגלי הלם ממוקדים האנרגיה מתכנסת לנקודת מוקד בעומק שנבחר, לטיפול מדויק במבנים עמוקים יותר.')]),
 dict(n=2,slug='spinal-decompression-how-it-works',aud='למטופלים',kw='דיקומפרסיה / דקומפרסיה לגב',
  title='דיקומפרסיה לגב – איך דקומפרסיה עובדת ולמי מתאימה | איי גרופ',
  desc='דקומפרסיה (דיקומפרסיה) לגב: איך עובד טיפול ממוחשב בעמוד השדרה, במה הוא שונה ממתיחה רגילה, למי הוא נשקל בבלט ופריצת דיסק ומתי לא עושים אותו בכלל.',
  h1='דקומפרסיה לגב (דיקומפרסיה) – איך זה עובד?',og_name='דיקומפרסיה לגב',og_sub='איך זה עובד ולמי זה מתאים',
  img='/assets/img/67d6fe3d_00a2e304c_1200px900px4on3.webp',og_src='tools/seo/src/00a2e304c_1200px900px4on3.png',
  faq=[('מה ההבדל בין דקומפרסיה לדיקומפרסיה?','אין הבדל. אלה שני כתיבים של אותו טיפול – הפחתת לחץ מבוקרת על עמוד השדרה באמצעות מערכת ממוחשבת. שני הכתיבים נפוצים בעברית.'),
       ('כמה מפגשי דקומפרסיה צריך?','מפגש נמשך בדרך כלל כ-20 עד 45 דקות, והטיפול ניתן כסדרה של מפגשים, לרוב 15 עד 20, לפי פרוטוקול שהמטפל קובע. מומלץ לשלב תרגילי ייצוב.'),
       ('האם דקומפרסיה כואבת?','רוב המטופלים מתארים תחושת משיכה ומתיחה ולא כאב. מתחילים בכוח נמוך ומעלים בהדרגה. כאב חד או החמרה בכאב המקרין מחייבים לעצור ולעדכן את המטפל.'),
       ('למי אסור לעשות דקומפרסיה?','נגד-התוויות מקובלות: היריון, שבר, גידול או זיהום בעמוד השדרה, אוסטאופורוזיס משמעותית, אי-יציבות של עמוד השדרה, קיבוע ניתוחי או שתלים (לפי שיקול רופא) ומפרצת בטנית.'),
       ('האם דקומפרסיה מחליפה ניתוח?','לא בהכרח. זהו טיפול שמרני שנשקל לעיתים לפני טיפולים פולשניים. ההחלטה על מסלול הטיפול היא של הרופא, ואין הבטחה לתוצאה.')]),
 dict(n=3,slug='focused-vs-radial-shockwave',aud='לבעלי קליניקות',kw='גלי הלם ממוקדים מול רדיאליים · מכשיר גלי הלם לקליניקה',
  title='גלי הלם ממוקדים מול רדיאליים – מה לבחור לקליניקה? | איי גרופ',
  desc='גלי הלם ממוקדים או רדיאליים? השוואה מקצועית לבעלי קליניקות: איך כל סוג עובד, למי הוא מתאים, עמידות ראש הטיפול, שירות ושאלות שחובה לשאול לפני רכישה.',
  h1='גלי הלם ממוקדים מול רדיאליים – מה לבחור לקליניקה?',og_name='ממוקדים מול רדיאליים',og_sub='איזה מכשיר גלי הלם לקליניקה?',
  img='/assets/img/cb09d943_professional-shockwave-therapy-machine-lgt-2500s.webp',og_src='tools/seo/src/professional-shockwave-therapy-machine-lgt-2500s.jpg',
  faq=[('איזה מכשיר גלי הלם מתאים לקליניקת פיזיותרפיה כללית?','קליניקה עם עומס גבוה של פציעות גידים, נקודות טריגר ואזורים רחבים מוצאת לרוב מענה רחב במכשיר רדיאלי. קליניקות שמטפלות במבנים עמוקים ורוצות דיוק בנקודה נוטות למכשיר ממוקד.'),
       ('אפשר לשלב מכשיר ממוקד ומכשיר רדיאלי באותה קליניקה?','כן. קליניקות ומרכזי שיקום רבים משלבים את שני הסוגים, כדי להתאים את סוג הגל לאבחנה ולאזור הטיפול.'),
       ('למה חשובה עמידות ראש הטיפול?','ראש הטיפול הוא חלק מתכלה. העמידות שלו בפולסים, עלות ההחלפה וזמינות החלפים משפיעות על עלות התפעול לאורך זמן. לדוגמה, ראש הטיפול של PowerShocker LGT-2500S PLUS מדורג ל-2,000,000 פולסים.'),
       ('כמה עולה מכשיר גלי הלם לקליניקה?','המחיר תלוי בדגם (ממוקד או רדיאלי), בתצורה ובאביזרים. לקבלת הצעת מחיר מותאמת לקליניקה התקשרו לעמירם 050-917-6111 או לאינה 054-936-9742.'),
       ('אפשר לקבל הדגמה לפני רכישה?','כן. ניתן לתאם שיחת ייעוץ והדגמה עם צוות איי גרופ. פרטי התצורה, ההדרכה, האחריות והשירות מפורטים בהצעת המחיר.')]),
 dict(n=4,slug='choosing-decompression-device',aud='לבעלי קליניקות',kw='מכשיר דקומפרסיה לקליניקה · מכשיר דיקומפרסיה',
  title='איך בוחרים מכשיר דקומפרסיה לקליניקה – המדריך | איי גרופ',
  desc='מדריך לבחירת מכשיר דקומפרסיה (דיקומפרסיה) לקליניקה: סוגי מערכות, שליטה בכוח ובזווית, ניטור, מקום, הדרכה ושירות, וצ׳קליסט מסודר לפני שמחליטים.',
  h1='איך בוחרים מכשיר דקומפרסיה לקליניקה?',og_name='מכשיר דקומפרסיה לקליניקה',og_sub='איך בוחרים נכון | מדריך',
  img='/assets/img/0c492d45_70bc55ed2_2222.jpg',og_src='assets/img/0c492d45_70bc55ed2_2222.jpg',
  faq=[('מה ההבדל בין Spine-MT ל-Spine MT Core?','Spine-MT היא מערכת דקומפרסיה ממוחשבת לעמוד השדרה. Spine MT Core משלבת בנוסף לדקומפרסיה גם חימום, הנעה ותיקון מנח במכשיר אחד.'),
       ('כמה מקום צריך למכשיר דקומפרסיה?','זה תלוי בדגם. כדאי לבקש מהספק את מידות המערכת ולמדוד את החדר מראש, כולל מרחב לכניסה ויציאה של המטופל, לרתימה ולתנועה של המטפל.'),
       ('האם צריך הדרכה מיוחדת כדי להפעיל מכשיר דקומפרסיה?','כן. ההדרכה צריכה לכלול לא רק הפעלה טכנית אלא גם בחירת מטופלים, נגד-התוויות ופרוטוקולים, כדי שכל הצוות יעבוד בצורה אחידה ובטוחה.'),
       ('יש לי שולחן מתיחה. האם כדאי לעבור לדקומפרסיה ממוחשבת?','שדרוג שווה בחינה כשמספר מטופלי הדיסק גדל, כשרופאים מפנים אליכם מטופלים לדקומפרסיה, או כשאתם רוצים פרוטוקולים מתועדים ואחידים. בשיחת ייעוץ נעזור להעריך את ההתאמה.'),
       ('כמה עולה מכשיר דקומפרסיה?','המחיר תלוי בדגם, בתצורה ובאביזרים. לקבלת הצעת מחיר מפורטת, כולל הדרכה, אחריות ושירות, התקשרו לעמירם 050-917-6111 או לאינה 054-936-9742.')]),
 dict(n=5,slug='chiropractic-table-guide',aud='לבעלי קליניקות',kw='מיטה כירופרקטית · מיטה כירופרקטית לקליניקה',
  title='מיטה כירופרקטית לשיקום הגב – מדריך לבעלי קליניקות | איי גרופ',
  desc='מיטה כירופרקטית לשיקום הגב: מה מבדיל אותה ממיטת טיפול רגילה, טכניקות דרופ, פלקסיה ומתיחה, מה לבדוק לפני רכישה והשוואה בין Raphael 707 ל-606.',
  h1='מיטה כירופרקטית לשיקום הגב – מדריך לבעלי קליניקות',og_name='מיטה כירופרקטית',og_sub='לשיקום הגב | מדריך לקליניקות',
  img='/assets/img/raphael-707-chiropractic-table.webp',og_src='tools/seo/src/raphael-707.png',
  faq=[('מה ההבדל בין מיטה כירופרקטית למיטת טיפול רגילה?','מיטה כירופרקטית בנויה ממקטעים נפרדים שיכולים לרדת, להתכופף או לנטות הצידה, ובכך מאפשרת טכניקות כמו דרופ ופלקסיה-דיסטרקציה. מיטה רגילה היא משטח יציב בלבד.'),
       ('מה ההבדל בין דרופ מוטורי לדרופ פנאומטי?','דרופ פנאומטי מופעל באמצעות מדחס אוויר. דרופ מוטורי פועל ללא מדחס, ולכן העבודה שקטה יותר והנחיתה רכה. זה המנגנון ב-Raphael 707.'),
       ('מה ההבדל בין Raphael 707 ל-Raphael 606?','Raphael 707 היא מערכת משולבת עם דרופ מוטורי, פלקסיה אוטומטית, מתיחה צירית עד 10 ס"מ ומסך מגע. Raphael 606 מתמקדת בפלקסיה-דיסטרקציה בשיטת Leander, עם דרופ אוטומטי ב-3 מקטעים וכיפוף צידי עד 20°.'),
       ('כמה מקום צריך למיטה כירופרקטית?','לפי היצרן של מיטות Raphael, מומלץ חלל של כ-3 עד 3.5 מטר אורך ו-1.2 עד 1.5 מטר רוחב סביב המיטה, כדי לאפשר תנועה חופשית של המטפל.'),
       ('כמה עולה מיטה כירופרקטית?','המחיר תלוי בדגם, בצבע ובאביזרים. לקבלת הצעת מחיר מותאמת התקשרו לעמירם 050-917-6111 או לאינה 054-936-9742.')]),
]
REL_LINKS={1:[('מכשירי גלי הלם לקליניקה','/shockwave-devices'),('טיפול בגלי הלם (ESWT)','/shockwave-therapy'),('Ultrawave LGT-2620','/product/ultrawave-lgt-2620'),('PowerShocker LGT-2500S PLUS','/product/powershocker-lgt-2500s-plus'),('קריותרפיה רפואית','/cryotherapy')],
 2:[('דקומפרסיה לעמוד השדרה','/spinal-decompression'),('Spine-MT','/product/spine-mt'),('Spine MT Core','/product/spine-mt-core'),('מיטה כירופרקטית Raphael','/chiropractic-beds'),('מכשירים לקליניקות','/clinic-equipment')],
 3:[('מכשירי גלי הלם לקליניקה – השוואה','/shockwave-devices'),('Ultrawave LGT-2620','/product/ultrawave-lgt-2620'),('PowerShocker LGT-2500S PLUS','/product/powershocker-lgt-2500s-plus'),('טיפול בגלי הלם (ESWT)','/shockwave-therapy'),('מכשירים לקליניקות','/clinic-equipment')],
 4:[('Spine-MT','/product/spine-mt'),('Spine MT Core','/product/spine-mt-core'),('Therapy Master','/product/tera-master'),('מיטה רובוטית טיפולית','/product/robotic-bed'),('דקומפרסיה לעמוד השדרה','/spinal-decompression')],
 5:[('מיטה כירופרקטית Raphael','/chiropractic-beds'),('דקומפרסיה לעמוד השדרה','/spinal-decompression'),('Spine-MT','/product/spine-mt'),('מיטה רובוטית טיפולית','/product/robotic-bed'),('מכשירי גלי הלם לקליניקה','/shockwave-devices')]}
RELATED={1:[3,2,5],2:[4,1,5],3:[1,4,5],4:[2,5,3],5:[4,2,3]}
def inline(t):
    t=html.escape(t,quote=False)
    t=re.sub(r'\*\*(.+?)\*\*',r'<strong>\1</strong>',t)
    t=re.sub(r'\[([^\]]+)\]\(([^)]+)\)',r'<a href="\2">\1</a>',t)
    return t
def md2html(md):
    out=[];toc=[];lst=None;tbl=[];para=[];n=0
    def flush():
        nonlocal lst,tbl,para
        if para: out.append('<p>'+inline(' '.join(para))+'</p>'); para=[]
        if lst: out.append(f'<{lst[0]}>'+''.join(f'<li>{inline(x)}</li>' for x in lst[1])+f'</{lst[0]}>'); lst=None
        if tbl:
            rows=[[c.strip() for c in r.strip().strip('|').split('|')] for r in tbl if not re.match(r'^\|[\s\-|]+\|$',r.strip())]
            h=''.join(f'<th>{inline(c)}</th>' for c in rows[0]); b=''.join('<tr>'+''.join(f'<td>{inline(c)}</td>' for c in r)+'</tr>' for r in rows[1:])
            out.append(f'<div class="blog-table"><table><thead><tr>{h}</tr></thead><tbody>{b}</tbody></table></div>'); tbl=[]
    for line in md.splitlines():
        s=line.rstrip()
        if not s.strip(): flush(); continue
        if s.startswith('## '):
            flush(); n+=1; t=s[3:]; toc.append((f's{n}',t)); out.append(f'<h2 id="s{n}">{inline(t)}</h2>'); continue
        if s.startswith('### '): flush(); out.append(f'<h3>{inline(s[4:])}</h3>'); continue
        if s.startswith('|'):
            if para or lst: flush()
            tbl.append(s); continue
        m=re.match(r'^(\d+)\. (.*)',s)
        if s.startswith('- ') or m:
            kind='ol' if m else 'ul'; item=m.group(2) if m else s[2:]
            if para or tbl: flush()
            if lst and lst[0]!=kind: flush()
            if not lst: lst=(kind,[])
            lst[1].append(item); continue
        if lst or tbl: flush()
        para.append(s.strip())
    flush(); return out,toc
W='<div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">'
BTN1='<a href="tel:0509176111" class="inline-flex items-center justify-center rounded-md text-sm font-medium bg-primary text-primary-foreground shadow hover:bg-primary/90 h-9 px-4 py-2">עמירם: 050-917-6111</a><a href="tel:0549369742" class="inline-flex items-center justify-center rounded-md text-sm font-medium bg-primary text-primary-foreground shadow hover:bg-primary/90 h-9 px-4 py-2">אינה: 054-936-9742</a>'
BTN2='<a href="/phone-consultation" class="inline-flex items-center justify-center rounded-md text-sm font-medium border border-border h-9 px-4 py-2 bg-white">קביעת שיחת ייעוץ</a>'
def cta(a):
    if a['aud']=='לבעלי קליניקות':
        t,b='רוצים להתאים את המכשיר לקליניקה שלכם?','צוות איי גרופ ישמח לעזור בהשוואה בין הדגמים, לתאם הדגמה ולהכין הצעת מחיר מפורטת עם הדרכה, אחריות ושירות.'
    else:
        t,b='שאלות על הטיפול או על הציוד?','איי גרופ מייבאת ומפיצה מכשור לקליניקות בישראל. אנחנו לא נותנים ייעוץ רפואי, אבל נשמח לענות על שאלות על הטכנולוגיה ולחבר אתכם למידע הנכון.'
    return f'<aside class="blog-cta"><p class="blog-cta-t">{t}</p><p>{b}</p><div class="flex flex-wrap gap-3">{BTN1}{BTN2}</div></aside>'
def card(a):
    return (f'<a href="/blog/{a["slug"]}" class="blog-card"><img loading="lazy" decoding="async" src="{a["img"]}" alt="{esc(a["h1"])}">'
            f'<div class="blog-card-b"><span class="blog-chip">{a["aud"]}</span><h3>{esc(a["h1"])}</h3><p>{esc(a["desc"])}</p><span class="blog-meta">{a["rt"]} דקות קריאה</span></div></a>')
def page(path,file,title,desc,og,ogalt,ld,body,ogtype='article'):
    h=HEAD; a=h.find('<!-- seo:start -->'); b=h.find('<!-- seo:end -->')+len('<!-- seo:end -->')
    s=_seo(title,desc,path,og,ogalt,ld).replace('<meta property="og:type" content="website">',f'<meta property="og:type" content="{ogtype}">')
    if ogtype=='article': s=s.replace('<!-- seo:end -->',f'<meta property="article:published_time" content="{DATE}">\n<meta property="article:modified_time" content="{DATE}">\n<!-- seo:end -->')
    open(file,'w',encoding='utf-8').write(h[:a]+s+h[b:]+body+FOOT); print('wrote',file,len(title),len(desc))
import os; os.makedirs('blog',exist_ok=True)
for a in A:
    md=open(f'tools/blog/a{a["n"]}.md',encoding='utf-8').read()
    a['words']=len(md.split())+sum(len((q+' '+x).split()) for q,x in a['faq']); a['rt']=max(4,math.ceil(a['words']/200))
for a in A:
    md=open(f'tools/blog/a{a["n"]}.md',encoding='utf-8').read()
    blocks,toc=md2html(md)
    if a['slug']=='focused-vs-radial-shockwave':
        # after the two intro paragraphs, before the first h2
        idx0=next(i for i,b in enumerate(blocks) if b.startswith('<h2'))
        blocks.insert(idx0, video_blog_block())
        toc.insert(0, ('video-focused-vs-radial', VIDEO_HEADING))
    elif a['slug']=='what-is-shockwave-therapy':
        # after section s2 (focused vs radial), before s3
        idx=[i for i,b in enumerate(blocks) if b.startswith('<h2')]
        # s3 is the 3rd h2 (0-index 2)
        blocks.insert(idx[2], video_blog_block())
        toc.insert(2, ('video-focused-vs-radial', VIDEO_HEADING))
    # mid-article CTA after 3rd h2 section
    idx=[i for i,b in enumerate(blocks) if b.startswith('<h2')]
    if len(idx)>3: blocks.insert(idx[3],cta(a))
    path=f'/blog/{a["slug"]}'; og=f'og/blog-{a["slug"]}.jpg'
    og_product(a['og_name'],a['og_sub'],a['og_src'],og)
    faqh=''.join(f'<details class="bg-card rounded-xl border border-border/50 p-4"><summary class="font-semibold cursor-pointer" {C}>{q}</summary><p class="text-sm text-muted-foreground leading-relaxed mt-3">{x}</p></details>' for q,x in a['faq'])
    tochtml=''.join(f'<li><a href="#{i}">{inline(t)}</a></li>' for i,t in toc)
    rel=''.join(f'<a href="{u}" class="inline-block rounded-full border border-border/60 px-4 py-2 text-sm hover:bg-primary/10" {C}>{t}</a>' for t,u in REL_LINKS[a['n']])
    body=(f'<section class="relative pt-24 pb-8 overflow-hidden blog-hero">{W}'
      f'<nav aria-label="פירורי לחם" class="blog-bc"><a href="/">דף הבית</a> › <a href="/blog/">בלוג</a> › <span>{esc(a["h1"])}</span></nav>'
      f'<div class="blog-hero-grid"><div><span class="blog-chip">{a["aud"]}</span>'
      f'<h1 class="text-3xl md:text-4xl font-bold mb-4 mt-3" {C}>{esc(a["h1"])}</h1><p class="blog-lead">{esc(a["desc"])}</p>'
      f'<p class="blog-meta">צוות איי גרופ · {DATE_HE} · {a["rt"]} דקות קריאה</p></div>'
      f'<div class="blog-hero-img"><img src="{a["img"]}" alt="{esc(a["h1"])}"></div></div></div></section>'
      f'<section class="pb-12">{W}<div class="blog-layout"><article class="blog-prose">{"".join(blocks)}'
      f'<h2 id="faq">שאלות נפוצות</h2><div class="space-y-3 not-prose">{faqh}</div>{cta(a)}'
      '<p class="blog-disc">המידע במאמר הוא כללי ואינו מחליף ייעוץ רפואי. ההתאמה לטיפול, ההתוויות ונגד-ההתוויות נקבעות על ידי איש מקצוע מוסמך ובהתאם להוראות היצרן.</p></article>'
      f'<aside class="blog-aside"><div class="blog-toc"><p class="blog-toc-t">בכתבה</p><ol>{tochtml}<li><a href="#faq">שאלות נפוצות</a></li></ol></div>'
      f'<div class="blog-side-cta"><p class="blog-cta-t">ייעוץ ללא התחייבות</p><p>מאיר אריאל 6, נתניה</p>{BTN1}{BTN2}</div></aside></div></div></section>'
      f'<section class="py-12 bg-secondary/30">{W}<h2 class="text-2xl md:text-3xl font-bold mb-6 text-center" {C}>מאמרים נוספים</h2><div class="blog-grid">{"".join(card(A[i-1]) for i in RELATED[a["n"]])}</div></div></section>'
      f'<section class="py-10">{W}<h2 class="text-xl md:text-2xl font-bold mb-4 text-center" {C}>מוצרים ונושאים קשורים</h2><nav aria-label="מוצרים קשורים" class="flex flex-wrap gap-3 justify-center">{rel}</nav></div></section>')
    art={"@context":"https://schema.org","@type":"Article","headline":a['h1'],"description":a['desc'],"image":[BASE+'/'+og],"datePublished":DATE,"dateModified":DATE,
         "inLanguage":"he-IL","author":ORG,"publisher":ORG,"mainEntityOfPage":{"@type":"WebPage","@id":BASE+path},"keywords":a['kw'].replace(' · ',', '),"wordCount":a['words']}
    bc={"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"דף הבית","item":BASE+"/"},{"@type":"ListItem","position":2,"name":"בלוג","item":BASE+"/blog/"},{"@type":"ListItem","position":3,"name":a['h1'],"item":BASE+path}]}
    ld=[art,bc,faqld(a['faq'])]
    if a['slug'] in ('focused-vs-radial-shockwave','what-is-shockwave-therapy'):
        ld.append(video_ld())
    page(path,f'blog/{a["slug"]}.html',a['title'],a['desc'],og,a['h1']+' – איי גרופ',ld,body)
# ---- index ----
og_generic('בלוג איי גרופ – מדריכים לטיפול ולקליניקות','og/blog.jpg')
grp=lambda aud:''.join(card(a) for a in A if a['aud']==aud)
body=(f'<section class="relative pt-24 pb-10 overflow-hidden blog-hero">{W}<nav aria-label="פירורי לחם" class="blog-bc"><a href="/">דף הבית</a> › <span>בלוג</span></nav>'
  f'<h1 class="text-3xl md:text-4xl font-bold mb-3 mt-3" {C}>בלוג איי גרופ</h1><p class="blog-lead">מדריכים מקצועיים על גלי הלם, דקומפרסיה לעמוד השדרה ומיטות כירופרקטיות – למטופלים שרוצים להבין את הטיפול, ולבעלי קליניקות שבוחרים ציוד.</p>'
  f'<div class="flex flex-wrap gap-3 mt-5">{BTN1}{BTN2}</div></div></section>'
  f'<section class="py-10 bg-secondary/30">{W}<h2 class="text-2xl md:text-3xl font-bold mb-6" {C}>לבעלי קליניקות</h2><div class="blog-grid">{grp("לבעלי קליניקות")}</div></div></section>'
  f'<section class="py-10">{W}<h2 class="text-2xl md:text-3xl font-bold mb-6" {C}>למטופלים</h2><div class="blog-grid">{grp("למטופלים")}</div></div></section>'
  f'<section class="py-10 bg-secondary/30">{W}<h2 class="text-xl md:text-2xl font-bold mb-4 text-center" {C}>עמודי מידע ומוצרים</h2><nav aria-label="מוצרים קשורים" class="flex flex-wrap gap-3 justify-center">'
  +''.join(f'<a href="{u}" class="inline-block rounded-full border border-border/60 px-4 py-2 text-sm hover:bg-primary/10" {C}>{t}</a>' for t,u in [('מכשירי גלי הלם לקליניקה','/shockwave-devices'),('טיפול בגלי הלם','/shockwave-therapy'),('דקומפרסיה לעמוד השדרה','/spinal-decompression'),('מיטה כירופרקטית Raphael','/chiropractic-beds'),('מגנטותרפיה','/magnetotherapy'),('מכשירים לקליניקות','/clinic-equipment')])+'</nav></div></section>')
blog={"@context":"https://schema.org","@type":"Blog","name":"בלוג איי גרופ","url":BASE+"/blog/","inLanguage":"he-IL","publisher":ORG,
      "blogPost":[{"@type":"BlogPosting","headline":a['h1'],"url":BASE+'/blog/'+a['slug'],"datePublished":DATE,"image":BASE+'/og/blog-'+a['slug']+'.jpg'} for a in A]}
bc={"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"דף הבית","item":BASE+"/"},{"@type":"ListItem","position":2,"name":"בלוג","item":BASE+"/blog/"}]}
page('/blog/','blog/index.html','בלוג איי גרופ – מדריכים לגלי הלם, דקומפרסיה וקליניקות',
     'בלוג איי גרופ: מדריכים מקצועיים בעברית על טיפול בגלי הלם, דקומפרסיה (דיקומפרסיה) לעמוד השדרה ומיטות כירופרקטיות – למטופלים ולבעלי קליניקות בישראל.',
     'og/blog.jpg','בלוג איי גרופ',[blog,bc],body,ogtype='website')
json.dump([{k:a[k] for k in ('slug','title','h1','kw','aud','words')} for a in A],open('tools/blog/articles.json','w'),ensure_ascii=False,indent=1)

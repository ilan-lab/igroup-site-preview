"""Nov 26 2026 site-wide SEO pass (idempotent). Run after nov26_pages.py from repo root."""
import glob, re, os, sys
sys.path.insert(0,'tools/seo')
from nov26_pages import sec,p,ul,card,grid,small,table,C
TODAY='2026-11-26'
changed=set()
def rd(f): return open(f,encoding='utf-8').read()
def wr(f,s,old):
    if s!=old: open(f,'w',encoding='utf-8').write(s); changed.add(f)
pages=[f for f in glob.glob('*.html')+glob.glob('product/*.html')+glob.glob('kin/product/*.html')]
STUB_MARK='העמוד עבר'
NAVCLS='px-4 py-2 text-sm font-medium rounded-lg transition-all duration-300 text-white/70 hover:text-white hover:bg-white/10'
NEWNAV=f'<a href="/shockwave-devices" class="{NAVCLS}">גלי הלם</a><a href="/chiropractic-beds" class="{NAVCLS}">כירופרקטיקה</a>'
FL='<li><a class="text-sm text-background/50 hover:text-primary transition-colors" href="{u}">{t}</a></li>'
NEWFL=FL.format(u='/shockwave-devices',t='מכשירי גלי הלם לקליניקה')+FL.format(u='/chiropractic-beds',t='מיטה כירופרקטית Raphael')
REL='<a href="{u}" class="inline-block rounded-full border border-border/60 px-4 py-2 text-sm hover:bg-primary/10" '+C+'>{t}</a>'
RELADD={
 'product/ultrawave-lgt-2620.html':[('/shockwave-devices','מכשירי גלי הלם לקליניקה – השוואה')],
 'product/powershocker-lgt-2500s-plus.html':[('/shockwave-devices','מכשירי גלי הלם לקליניקה – השוואה')],
 'product/lgt-2410s.html':[('/shockwave-devices','מכשירי גלי הלם לקליניקה')],
 'cryotherapy.html':[('/shockwave-devices','מכשירי גלי הלם לקליניקה')],
 'shockwave-therapy.html':[('/shockwave-devices','מכשירי גלי הלם לקליניקה – השוואה')],
 'product/robotic-bed.html':[('/chiropractic-beds','מיטה כירופרקטית Raphael')],
 'product/spine-mt.html':[('/chiropractic-beds','מיטה כירופרקטית Raphael')],
 'product/spine-mt-core.html':[('/chiropractic-beds','מיטה כירופרקטית Raphael')],
 'product/tera-master.html':[('/chiropractic-beds','מיטה כירופרקטית Raphael')],
 'spinal-decompression.html':[('/chiropractic-beds','מיטה כירופרקטית Raphael')],
 'product/ultrasound.html':[('/shockwave-devices','מכשירי גלי הלם לקליניקה')],
 'product/rehamoto-5100p.html':[('/spinal-decompression','דקומפרסיה לעמוד השדרה')],
 'magnetotherapy.html':[('/shockwave-devices','מכשירי גלי הלם לקליניקה')],
 'product/biomag-lumina.html':[('/shockwave-devices','מכשירי גלי הלם לקליניקה')],
}
def before_faq(h,block,marker):
    if marker in h: return h
    i=h.find('שאלות נפוצות</h2>')
    if i<0: i=h.find('<footer')
    s=h.rfind('<section',0,i)
    return h[:s]+block+h[s:]
L=lambda u,t: f'<a href="{u}" class="underline" {C}>{t}</a>'
TOPIC={
'product/ultrawave-lgt-2620.html':('id="uw-fit"',
  sec('למי מתאים Ultrawave LGT-2620?',
   ul(['<strong>אורתופדיה ורפואת ספורט</strong> – טיפול מדויק בנקודה ובמבנים עמוקים, כמו מקומות חיבור של גידים לעצם.',
       '<strong>קליניקות פיזיותרפיה</strong> שכבר עובדות עם מכשיר רדיאלי ורוצות להוסיף יכולת טיפול ממוקדת בעומק.',
       '<strong>מרכזי שיקום ומכוני כאב</strong> שבונים פרוטוקול של סדרת טיפולים (בדרך כלל 3–5) ורוצים להתאים את סוג הגל לאבחנה.']),id_='uw-fit')+
  sec('Ultrawave LGT-2620 מול PowerShocker LGT-2500S PLUS',
   table(['','Ultrawave LGT-2620','PowerShocker LGT-2500S PLUS'],[
    ['סוג גל','ממוקד','רדיאלי'],['מחולל','אלקטרומגנטי','פנאומטי, דו-ערוצי'],
    ['פיזור האנרגיה','מתכנסת לנקודת מוקד בעומק הרקמה','חזקה בנקודת המגע ומתפזרת לשטח רחב'],
    ['מתאים במיוחד ל','מבנים עמוקים וטיפול מדויק בנקודה','מבנים שטחיים, אזורים רחבים ונקודות טריגר']])+
   p('רבות מהקליניקות משלבות את שני הסוגים. השוואה מלאה, כולל דגם LGT-2520GP הממוקד החדש (4 מיליון פולסים ממוקדים), בעמוד '+L('/shockwave-devices','מכשירי גלי הלם לקליניקה')+'.'),alt=True)+
  sec('איך משלבים את Ultrawave בעבודת הקליניקה',
   p('הטיפול ניתן בקליניקה, ללא הרדמה וללא זמן החלמה. המטפל מאתר את אזור הכאב, מתאים את עומק המוקד והאנרגיה לאבחנה, ומתעד את הפרמטרים לקראת המפגש הבא. מידע מקצועי על ההתוויות, נגד-ההתוויות ומבנה הסדרה – במדריך '+L('/shockwave-therapy','טיפול בגלי הלם (ESWT)')+'.'))),
'shockwave-therapy.html':('id="sw-choose"',
  sec('איך בוחרים מכשיר גלי הלם לקליניקה?',
   p('הבחירה מתחילה מסוג המטופלים: מבנים עמוקים וטיפול מדויק בנקודה מתאימים למכשיר ממוקד אלקטרומגנטי, ופציעות גידים שטחיות, נקודות טריגר ואזורים נרחבים מתאימים למכשיר רדיאלי. שאלות שכדאי לשאול לפני רכישה:')+
   ul(['אילו התוויות חוזרות הכי הרבה בקליניקה – דורבן, אכילס, כתף, מרפק או ברך?',
       'האם נדרש מכשיר ממוקד, רדיאלי או שילוב של שניהם?',
       'מה עמידות ראש הטיפול? למשל, ראש הטיפול של PowerShocker מדורג ל-2,000,000 פולסים, ו-LGT-2520GP מדגיש 4 מיליון פולסים ממוקדים.',
       'אילו הדרכה, שירות ואחריות כלולים בהצעת המחיר?'])+
   p('השוואה מלאה בין הדגמים – בעמוד '+L('/shockwave-devices','מכשירי גלי הלם לקליניקה – ממוקדים ורדיאליים')+'.'),alt=True,id_='sw-choose')),
'spinal-decompression.html':('id="dc-compare"',
  sec('דקומפרסיה, מתיחה ומיטה כירופרקטית – מה ההבדל?',
   grid([card('דקומפרסיה ממוחשבת',small('מחשב מפעיל כוח מדורג במחזורים של משיכה והרפיה, בזווית שנבחרת לפי המקטע, ומנטר את התנגדות הגוף. מערכות: Spine-MT ו-Spine MT Core.'),'/product/spine-mt'),
         card('מתיחה רגילה (טרקשן)',small('כוח משיכה קבוע לאורך הטיפול. השרירים סביב עמוד השדרה עלולים להגיב בכיווץ, ולכן ההשפעה על הדיסק שונה.')),
         card('מיטה כירופרקטית',small('טיפול ידני בטכניקות דרופ ופלקסיה-דיסטרקציה. בדגם Raphael 707 יש גם מתיחה צירית מוטורית עד 10 ס"מ.'),'/chiropractic-beds')])+
   p('דקומפרסיה (נכתב לעיתים גם "דיקומפרסיה") לעמוד השדרה משתלבת לעיתים קרובות בתוכנית שיקום רחבה יותר, לצד תרגול ייצוב וטיפול ידני. '+L('/chiropractic-beds','מיטה כירופרקטית Raphael')+' מאפשרת למטפל לעבור בין טכניקות באותו מפגש.'),alt=True,id_='dc-compare')+
  sec('איך משלבים דקומפרסיה בקליניקה',
   ul(['<strong>אבחון</strong> – הטיפול נשקל לאחר אבחון רפואי, ולרוב לאחר הדמיה.',
       '<strong>התאמה</strong> – בחירת המקטע (מותני או צווארי), הזווית והכוח לפי המטופל.',
       '<strong>סדרה</strong> – מפגשים של כ-20 עד 45 דקות, לרוב 15 עד 20 מפגשים, לפי הפרוטוקול שהמטפל קובע.',
       '<strong>שילוב</strong> – תרגול ייצוב ומעקב אחרי ההתקדמות לאורך הסדרה.']))),
'clinic-equipment.html':('id="ce-bytype"',
  sec('חדש באיי גרופ',grid([
    card('מכשירי גלי הלם לקליניקה – השוואה',small('Ultrawave LGT-2620 הממוקד, LGT-2520GP החדש ו-PowerShocker LGT-2500S PLUS הרדיאלי, בטבלת השוואה אחת.'),'/shockwave-devices'),
    card('מיטה כירופרקטית Raphael – לשיקום הגב',small('Raphael 707 עם דרופ חשמלי, פלקסיה ומתיחה צירית, ו-Raphael 606 בטכניקת Leander.'),'/chiropractic-beds')],n=2),id_='ce-bytype')+
  sec('איזה מכשור מתאים לאיזו קליניקה?',
   table(['סוג הקליניקה','מכשור מומלץ לבדיקה'],[
    ['קליניקת פיזיותרפיה',L('/shockwave-devices','גלי הלם')+', '+L('/product/ultrasound','אולטרסאונד טיפולי')+', '+L('/magnetotherapy','מגנטותרפיה')+', '+L('/kin','RehaMoto')],
    ['אורתופדיה ורפואת ספורט',L('/product/ultrawave-lgt-2620','גלי הלם ממוקדים')+', '+L('/cryotherapy','קריותרפיה ממוקדת LGT-2410S')],
    ['מכון כאב ומרכז עמוד שדרה',L('/spinal-decompression','דקומפרסיה')+' (Spine-MT, Spine MT Core), '+L('/chiropractic-beds','מיטה כירופרקטית')+', '+L('/product/robotic-bed','מיטה רובוטית')],
    ['מרכז שיקום וגריאטריה',L('/kin','RehaMoto')+', '+L('/product/tera-master','Therapy Master')+', '+L('/product/biomag-lumina','Biomag')],
    ['מרפאה וטרינרית',L('/vet','Biomag וטרינריה')]])+
   p('לפני רכישה כדאי לבדוק כמה דברים: אילו מצבים חוזרים הכי הרבה אצל המטופלים, כמה מקום פנוי יש בחדר הטיפול, האם המכשיר מאפשר לטפל בכמה מטופלים במקביל, ואילו הדרכה, שירות ואחריות כלולים בהצעת המחיר. בשיחת ייעוץ בטלפון 054-900-7723 נעזור להשוות בין המכשירים.'),alt=True)),
'magnetotherapy.html':('id="mg-clinic"',
  sec('איך משלבים מגנטותרפיה בקליניקה',
   p('מגנטותרפיה פולסטית (PEMF, נקראת גם "טיפול מגנטי") משתלבת בקליניקה כטיפול שקט שאינו דורש נוכחות רציפה של המטפל:')+
   ul(['<strong>טיפול במקביל</strong> – ב-Biomag Lumina 3D-e הקליני יש עד 4 ערוצים, כך שאפשר להפעיל כמה אפליקטורים ותוכניות בו-זמנית.',
       '<strong>מטופלים רגישים</strong> – המטופל כמעט אינו מרגיש דבר, ולכן הטיפול מתאים גם למטופלים מבוגרים או כאובים.',
       '<strong>המשכיות בבית</strong> – הסדרה מיועדת גם לשימוש ביתי עם תוכניות מוכנות, לאחר התייעצות עם הרופא המטפל.',
       '<strong>חלק מתוכנית שיקום</strong> – לצד '+L('/shockwave-devices','גלי הלם')+', '+L('/cryotherapy','קריותרפיה')+' ו'+L('/kin','שיקום תנועה')+'.']),alt=True,id_='mg-clinic')),
}
for f in pages:
    h=rd(f); o=h
    if STUB_MARK in h:
        if 'name="robots"' not in h:
            h=h.replace('<link rel="canonical"','<meta name="robots" content="noindex,follow"><link rel="canonical"',1)
        wr(f,h,o); continue
    # nav
    if '/shockwave-devices" class="'+NAVCLS not in h:
        h=re.sub(r'(<a href="/?#products" class="[^"]*">טכנולוגיות</a>)',lambda m:m.group(1)+NEWNAV,h,count=1)
    # footlinks
    if '<!-- footlinks:start -->' in h and 'href="/shockwave-devices">' not in h[h.find('<!-- footlinks:start -->'):h.find('<!-- footlinks:end -->')]:
        h=h.replace('<!-- footlinks:start -->','<!-- footlinks:start -->'+NEWFL,1)
    # related
    for u,t in RELADD.get(f,[]):
        a=h.find('aria-label="מוצרים קשורים"'); b=h.find('</nav>',a)
        if a>0 and f'href="{u}"' not in h[a:b]:
            s=h.find('>',a)+1; h=h[:s]+REL.format(u=u,t=t)+h[s:]
    if f in TOPIC:
        m,blk=TOPIC[f]; h=before_faq(h,blk,m)
    wr(f,h,o)
# new redirect stubs for old WordPress URLs
TPL='''<!DOCTYPE html><html lang="he" dir="rtl"><head><meta charset="utf-8"><title>העמוד עבר | איי גרופ</title><meta name="robots" content="noindex,follow">
<link rel="canonical" href="{url}"><meta http-equiv="refresh" content="0; url={to}">
<script>location.replace("{to}"+location.hash)</script></head>
<body><p style="font-family:sans-serif;text-align:center;margin-top:20vh">העמוד עבר. <a href="{to}">המשך לעמוד החדש</a></p></body></html>
'''
STUBS={'product/rehamoto-5100d-config2.html':'/kin/product/5100d-config-ii','product/morenova.html':'/clinic-equipment',
 'kinesiotherapy.html':'/kin','KinesiotherapyProduct.html':'/kin',
 'product/בלון-גז-ברזל-18-קג.html':'/cryotherapy','product/מילוי-גליל-פחמן-דו־חמצני-co₂.html':'/cryotherapy'}
for f,to in STUBS.items():
    s=TPL.format(url='https://i-group.co.il'+to,to=to)
    if not os.path.exists(f) or rd(f)!=s: open(f,'w',encoding='utf-8').write(s); changed.add(f)
# sitemap
sm=rd('sitemap.xml'); o=sm
for path in ['/shockwave-devices','/chiropractic-beds']:
    if f'<loc>https://i-group.co.il{path}</loc>' not in sm:
        sm=sm.replace('</urlset>',f'  <url><loc>https://i-group.co.il{path}</loc><lastmod>{TODAY}</lastmod></url>\n</urlset>')
for f in list(changed)+['shockwave-devices.html','chiropractic-beds.html']:
    if f in STUBS: continue
    path='/' if f=='index.html' else '/'+f[:-5]
    sm=re.sub(r'(<loc>https://i-group\.co\.il'+re.escape(path)+r'</loc><lastmod>)[^<]+',r'\g<1>'+TODAY,sm)
wr('sitemap.xml',sm,o)
print('\n'.join(sorted(changed))); print(len(changed),'files')

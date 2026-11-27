"""Nov 26 2026: build /shockwave-devices and /chiropractic-beds from the Ultrawave page template.
Run from repo root: python3 tools/seo/nov26_pages.py"""
import json, re, html, sys
sys.path.insert(0,'tools/seo')
from make_og import product as og_product
from youtube_video import video_ld, video_section
BASE='https://i-group.co.il'
C='style="color: rgb(11, 94, 215);"'
tpl=open('product/ultrawave-lgt-2620.html',encoding='utf-8').read()
nav_end=tpl.find('</nav>')+6
HEAD=tpl[:nav_end]
FOOT=tpl[tpl.find('<footer'):]
def esc(s): return html.escape(s,quote=True)
def seo(title,desc,path,og,ogalt,ld):
    url=BASE+path; ogu=BASE+'/'+og
    m=[f'<title>{esc(title)}</title>',f'<meta name="description" content="{esc(desc)}">',
       f'<link rel="canonical" href="{url}">','<meta name="robots" content="index,follow">',
       '<meta property="og:type" content="website">',f'<meta property="og:title" content="{esc(title)}">',
       f'<meta property="og:description" content="{esc(desc)}">',f'<meta property="og:url" content="{url}">',
       '<meta property="og:site_name" content="I-Group Medical Tech">','<meta property="og:locale" content="he_IL">',
       f'<meta property="og:image" content="{ogu}">','<meta property="og:image:width" content="1200">',
       '<meta property="og:image:height" content="630">',f'<meta property="og:image:alt" content="{esc(ogalt)}">',
       '<meta name="twitter:card" content="summary_large_image">',f'<meta name="twitter:title" content="{esc(title)}">',
       f'<meta name="twitter:description" content="{esc(desc)}">',f'<meta name="twitter:image" content="{ogu}">']
    for o in ld: m.append('<script type="application/ld+json">'+json.dumps(o,ensure_ascii=False)+'</script>')
    return '<!-- seo:start -->\n'+'\n'.join(m)+'\n<!-- seo:end -->'
def crumbs(name,path):
    return {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
        {"@type":"ListItem","position":1,"name":"דף הבית","item":BASE+"/"},
        {"@type":"ListItem","position":2,"name":name,"item":BASE+path}]}
def faqld(faq):
    return {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[
        {"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in faq]}
def itemlist(items):
    return {"@context":"https://schema.org","@type":"ItemList","itemListElement":[
        {"@type":"ListItem","position":i+1,"name":n,"url":BASE+u} for i,(n,u) in enumerate(items)]}
# ---- html helpers (same classes as existing topic pages) ----
W='<div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">'
def sec(title,inner,alt=False,id_=None):
    i=f' id="{id_}"' if id_ else ''
    return (f'<section{i} class="py-12{" bg-secondary/30" if alt else ""}">{W}'
            f'<h2 class="text-2xl md:text-3xl font-bold mb-6 text-center" {C}>{title}</h2>{inner}</div></section>')
def p(t): return f'<p class="text-sm md:text-base text-muted-foreground leading-relaxed mb-4 max-w-4xl mx-auto">{t}</p>'
def ul(items): return '<ul class="list-disc pr-6 space-y-2 text-sm md:text-base text-muted-foreground leading-relaxed max-w-4xl mx-auto mb-4">'+''.join(f'<li>{x}</li>' for x in items)+'</ul>'
def card(title,body,href=None,img=None,alt=''):
    im=f'<img loading="lazy" decoding="async" src="{img}" alt="{esc(alt)}" class="w-full aspect-[4/3] object-contain mb-4">' if img else ''
    tag,attr=('a',f' href="{href}"') if href else ('div','')
    hov=' block hover:shadow-lg transition-shadow' if href else ''
    return f'<{tag}{attr} class="bg-card rounded-2xl border border-border/50 p-6{hov}">{im}<h3 class="text-base font-bold mb-2" {C}>{title}</h3>{body}</{tag}>'
def grid(cards,n=3): return f'<div class="grid md:grid-cols-{n} gap-6">'+''.join(cards)+'</div>'
def small(t): return f'<p class="text-sm text-muted-foreground leading-relaxed">{t}</p>'
def table(head,rows):
    th=''.join(f'<th class="p-3 text-right font-bold" {C}>{h}</th>' for h in head)
    tr=''.join('<tr class="border-t border-border/50">'+''.join(f'<td class="p-3 align-top">{c}</td>' for c in r)+'</tr>' for r in rows)
    return ('<div class="overflow-x-auto max-w-5xl mx-auto bg-card rounded-2xl border border-border/50">'
            f'<table class="w-full text-sm text-muted-foreground"><thead><tr class="bg-secondary/40">{th}</tr></thead><tbody>{tr}</tbody></table></div>')
def hero(h1,sub,lead,img,alt):
    return (f'<section class="relative pt-24 pb-12 overflow-hidden">{W}<div class="grid lg:grid-cols-2 gap-8 lg:gap-12 items-center">'
            f'<div class="relative rounded-2xl overflow-hidden border border-border/50 shadow-lg" style="background-color: rgb(232, 238, 245);"><img src="{img}" alt="{esc(alt)}" class="w-full aspect-[4/3] object-contain"></div>'
            f'<div><h1 class="text-3xl md:text-4xl font-bold mb-2" {C}>{h1}</h1><p class="text-lg font-medium mb-4" {C}>{sub}</p>'
            f'<p class="text-sm md:text-base text-muted-foreground leading-relaxed mb-6">{lead}</p><div class="flex flex-wrap gap-3">'
            '<a href="tel:0549007723" class="inline-flex items-center justify-center rounded-md text-sm font-medium bg-primary text-primary-foreground shadow hover:bg-primary/90 h-9 px-4 py-2">חייג לייעוץ: 054-900-7723</a>'
            '<a href="/phone-consultation" class="inline-flex items-center justify-center rounded-md text-sm font-medium border border-border h-9 px-4 py-2">קביעת שיחת ייעוץ</a></div></div></div></div></section>')
def faqsec(faq):
    items=''.join(f'<details class="bg-card rounded-xl border border-border/50 p-4"><summary class="font-semibold cursor-pointer" {C}>{q}</summary><p class="text-sm text-muted-foreground leading-relaxed mt-3">{a}</p></details>' for q,a in faq)
    return sec('שאלות נפוצות',f'<div class="max-w-4xl mx-auto space-y-3">{items}</div>',alt=True)
def related(links):
    a=''.join(f'<a href="{u}" class="inline-block rounded-full border border-border/60 px-4 py-2 text-sm hover:bg-primary/10" {C}>{t}</a>' for t,u in links)
    return (f'<section class="py-10">{W}<h2 class="text-xl md:text-2xl font-bold mb-4 text-center" {C}>מוצרים ונושאים קשורים</h2>'
            f'<nav aria-label="מוצרים קשורים" class="flex flex-wrap gap-3 justify-center">{a}</nav></div></section>')
def disclaimer(t): return f'<section class="py-6">{W}<p class="text-xs text-muted-foreground text-center max-w-4xl mx-auto">{t}</p></div></section>'
def build(path,file,title,desc,og,ogalt,ld,body):
    h=HEAD
    a=h.find('<!-- seo:start -->'); b=h.find('<!-- seo:end -->')+len('<!-- seo:end -->')
    h=h[:a]+seo(title,desc,path,og,ogalt,ld)+h[b:]
    out=h+body+FOOT
    open(file,'w',encoding='utf-8').write(out)
    print('wrote',file,len(title),len(desc))

IMG_UW='/assets/img/feedc697_3075a8a23_Screenshot_20260608_234511_Chrome.webp'
IMG_PS='/assets/img/cb09d943_professional-shockwave-therapy-machine-lgt-2500s.webp'
IMG_GP='/assets/img/lgt-2520gp-card.webp'
IMG_707='/assets/img/raphael-707-chiropractic-table.webp'
IMG_606='/assets/img/raphael-606-chiropractic-table.webp'

def main():
    # ================= 1. shockwave-devices =================
    path='/shockwave-devices'
    title='מכשירי גלי הלם לקליניקה – ממוקדים ורדיאליים | איי גרופ'
    desc='מכשירי גלי הלם לקליניקה: השוואה בין Ultrawave LGT-2620 הממוקד, LGT-2520GP החדש ו-PowerShocker LGT-2500S PLUS הרדיאלי – סוג גל, התוויות ובחירה נכונה.'
    faq=[('מה ההבדל בין מכשיר גלי הלם ממוקד למכשיר רדיאלי?','במכשיר ממוקד (כמו Ultrawave LGT-2620 ו-LGT-2520GP) מחולל אלקטרומגנטי מרכז את האנרגיה בנקודת מוקד בעומק הרקמה. במכשיר רדיאלי (כמו PowerShocker LGT-2500S PLUS) גל לחץ פנאומטי מתפזר מהמוליך אל שטח רחב יותר, ולכן הוא מתאים במיוחד למבנים שטחיים ולאזורים נרחבים.'),
         ('איזה מכשיר גלי הלם מתאים לקליניקה שלי?','זה תלוי בסוג המטופלים: קליניקות שמטפלות בעיקר במבנים עמוקים ובנקודות מדויקות נוטות למכשיר ממוקד, וקליניקות עם עומס גבוה של פציעות גידים שטחיות, נקודות טריגר ואזורים רחבים נוטות למכשיר רדיאלי. רבות משלבות את שני הסוגים. צוות איי גרופ ישמח לעזור בהתאמה בשיחת ייעוץ.'),
         ('באילו מצבים משתמשים בגלי הלם בקליניקה?','בין ההתוויות המקובלות: דורבן (פלנטר פסיאיטיס), דלקת בגיד אכילס, טנדיניטיס בכתף ובגיד הסופרספינטוס, הסתיידות בכתף, מרפק טניס ומרפק גולף, טנדיניטיס פטלרי, תסמונת ה-IT band ונקודות טריגר. ההחלטה על טיפול מתקבלת על ידי איש מקצוע מוסמך.'),
         ('כמה טיפולים כוללת סדרה ומה משך הטיפול?','בדרך כלל סדרה של 3–5 טיפולים, וטיפול נמשך כ-5–15 דקות לאזור, בהתאם לאבחנה ולפרוטוקול שקבע המטפל.'),
         ('כמה עולה מכשיר גלי הלם לקליניקה?','המחיר תלוי בדגם (ממוקד או רדיאלי), בתצורה ובאביזרים. לקבלת הצעת מחיר מותאמת לקליניקה התקשרו ל-054-900-7723.'),
         ('אפשר לקבל הדגמה לפני רכישה?','כן. ניתן לתאם שיחת ייעוץ והדגמה עם צוות איי גרופ. פרטי התצורה, ההדרכה, האחריות והשירות מפורטים בהצעת המחיר.')]
    items=[('Ultrawave LGT-2620','/product/ultrawave-lgt-2620'),('LGT-2520GP','https://focused.i-group.co.il/'),('PowerShocker LGT-2500S PLUS','/product/powershocker-lgt-2500s-plus')]
    il=itemlist([(n,u) for n,u in items if u.startswith('/')])
    il['itemListElement'].insert(1,{"@type":"ListItem","position":2,"name":"LGT-2520GP","url":"https://focused.i-group.co.il/"})
    for i,e in enumerate(il['itemListElement']): e['position']=i+1
    body=hero('מכשירי גלי הלם לקליניקה','ממוקדים ורדיאליים – השוואה ובחירה',
      'איי גרופ מייבאת ומפיצה בישראל מכשירי גלי הלם (ESWT) מסדרת LGT של היצרן Longest – גם מכשירי גלי הלם ממוקדים אלקטרומגנטיים וגם מכשיר גלי הלם רדיאלי פנאומטי. בעמוד זה תמצאו השוואה בין הדגמים, למי מתאים כל אחד, ומה כדאי לבדוק לפני שבוחרים מכשיר גלי הלם לקליניקת פיזיותרפיה, אורתופדיה או רפואת ספורט.',
      IMG_UW,'מכשירי גלי הלם לקליניקה – Ultrawave, LGT-2520GP ו-PowerShocker')
    body+=video_section(alt=True)
    body+=sec('הדגמים שלנו',grid([
      card('Ultrawave LGT-2620 – גלי הלם ממוקדים',small('מחולל אלקטרומגנטי שמרכז את האנרגיה בנקודת מוקד בעומק הרקמה – לאזורים עמוקים ולטיפול מדויק בנקודה.'),'/product/ultrawave-lgt-2620',IMG_UW,'Ultrawave LGT-2620 מכשיר גלי הלם ממוקדים'),
      card('LGT-2520GP – גלי הלם ממוקדים (חדש)',small('גלי הלם אלקטרומגנטיים ממוקדים לטיפול מדויק בעומק הרקמה, עם דגש על עמידות: 4 מיליון פולסים ממוקדים.'),'https://focused.i-group.co.il/',IMG_GP,'LGT-2520GP מכשיר גלי הלם ממוקדים'),
      card('PowerShocker LGT-2500S PLUS – גלי הלם רדיאליים',small('מכשיר פנאומטי דו-ערוצי, לחץ 1.0–5.0 בר ותדר 1–22 הרץ, מסך מגע 7 אינץ׳ – למבנים שטחיים ולאזורים רחבים.'),'/product/powershocker-lgt-2500s-plus',IMG_PS,'PowerShocker LGT-2500S PLUS מכשיר גלי הלם רדיאלי')]))
    body+=sec('השוואה בין מכשירי גלי הלם',table(['','Ultrawave LGT-2620','LGT-2520GP','PowerShocker LGT-2500S PLUS'],[
      ['סוג גל','ממוקד','ממוקד','רדיאלי'],
      ['מחולל','אלקטרומגנטי','אלקטרומגנטי','פנאומטי (לחץ אוויר)'],
      ['פיזור האנרגיה','מרוכזת בנקודת מוקד בעומק הרקמה','מרוכזת בנקודת מוקד בעומק הרקמה','מתפזרת מהמוליך אל שטח רחב'],
      ['מתאים במיוחד ל','מבנים עמוקים וטיפול מדויק בנקודה','טיפול מדויק בעומק הרקמה, קליניקות עם נפח טיפולים גבוה','מבנים שטחיים, אזורים רחבים ונקודות טריגר'],
      ['נתונים בולטים','גלי הלם אלקטרומגנטיים ממוקדים','4 מיליון פולסים ממוקדים','2 ערוצים, 1.0–5.0 בר, 1–22 הרץ, מסך 7 אינץ׳, ראש טיפול ל-2,000,000 פולסים, מוליך ויברציה'],
      ['מפרט מלא','בעמוד המוצר ובהצעת המחיר','באתר LGT-2520GP','בעמוד המוצר']])+
      p('הנתונים בטבלה לקוחים מעמודי המוצרים באתר. מפרט טכני מלא, תצורות ואביזרים נמסרים עם הצעת המחיר.'),alt=True)
    body+=sec('ממוקד או רדיאלי – איך בוחרים?',
      p('ההבדל המרכזי הוא באופן שבו האנרגיה מגיעה לרקמה. במכשיר גלי הלם ממוקד האנרגיה מתכנסת לנקודת מוקד בעומק שנקבע, ולכן הוא מתאים לטיפול מדויק במבנים עמוקים. במכשיר רדיאלי גל הלחץ חזק ביותר בנקודת המגע ומתפזר משם, ולכן הוא מתאים לטיפול באזורים רחבים ובמבנים שטחיים.')+
      ul(['<strong>קליניקת פיזיותרפיה כללית</strong> – מכשיר רדיאלי נותן מענה רחב לפציעות גידים, נקודות טריגר ואזורים נרחבים.',
          '<strong>אורתופדיה ורפואת ספורט</strong> – מכשיר ממוקד מאפשר טיפול מדויק בנקודה ובמבנים עמוקים.',
          '<strong>מרכז שיקום עם נפח טיפולים גבוה</strong> – שילוב של ממוקד ורדיאלי מכסה את רוב ההתוויות, ועמידות ראש הטיפול חשובה במיוחד.',
          '<strong>לפני רכישה</strong> – כדאי לבדוק הדרכה, שירות ואחריות, זמינות חלקים ועלות החלפת ראש טיפול. הפרטים מופיעים בהצעת המחיר.']))
    body+=sec('התוויות נפוצות לטיפול בגלי הלם',
      grid([card('כף רגל ועקב',small('דורבן (פלנטר פסיאיטיס) ודלקת בגיד אכילס.')),
            card('כתף ומרפק',small('טנדיניטיס בגיד הסופרספינטוס, הסתיידות בכתף, מרפק טניס ומרפק גולף.')),
            card('ברך, ירך ושרירים',small('טנדיניטיס פטלרי, תסמונת ה-IT band ונקודות טריגר בשרירים.'))])+
      p('סדרת טיפולים כוללת בדרך כלל 3–5 טיפולים של כ-5–15 דקות לאזור. מידע מקצועי מפורט על הטיפול עצמו, נגד-התוויות ומבנה הסדרה – בעמוד <a href="/shockwave-therapy" class="underline" '+C+'>טיפול בגלי הלם (ESWT)</a>.'),alt=True)
    body+=faqsec(faq)
    body+=disclaimer('המידע בעמוד מיועד לאנשי מקצוע בתחום הבריאות ואינו מהווה ייעוץ רפואי. ההחלטה על טיפול ועל פרוטוקול הטיפול היא באחריות המטפל המוסמך.')
    body+=related([('טיפול בגלי הלם – מדריך לקליניקות','/shockwave-therapy'),('Ultrawave LGT-2620','/product/ultrawave-lgt-2620'),('PowerShocker LGT-2500S PLUS','/product/powershocker-lgt-2500s-plus'),('קריותרפיה רפואית','/cryotherapy'),('מכשירים לקליניקות','/clinic-equipment'),('מיטה כירופרקטית Raphael','/chiropractic-beds')])
    og_product('מכשירי גלי הלם לקליניקה','ממוקדים ורדיאליים | Ultrawave · PowerShocker','tools/seo/src/'+[x for x in __import__('os').listdir('tools/seo/src') if '3075a8a23' in x][0],'og/shockwave-devices.jpg')
    build(path,'shockwave-devices.html',title,desc,'og/shockwave-devices.jpg','מכשירי גלי הלם לקליניקה – איי גרופ',[crumbs('מכשירי גלי הלם לקליניקה',path),il,faqld(faq),video_ld()],body)

    # ================= 2. chiropractic-beds =================
    path='/chiropractic-beds'
    title='מיטה כירופרקטית Raphael 707 ו-606 – לשיקום הגב | איי גרופ'
    desc='מיטה כירופרקטית Raphael לשיקום הגב: דגם 707 עם דרופ חשמלי, פלקסיה ומתיחה צירית, ודגם 606 בטכניקת Leander. מפרט מלא, השוואה וייעוץ לקליניקות בישראל.'
    faq=[('מה ההבדל בין Raphael 707 ל-Raphael 606?','Raphael 707 היא מערכת משולבת: דרופ מוטורי, פלקסיה אוטומטית עד 22.4°, מתיחה צירית עד 10 ס"מ, כיפוף צידי, גובה חשמלי ומסך מגע 10 אינץ׳. Raphael 606 מתמקדת בטכניקת פלקסיה-דיסטרקציה בשיטת Leander, עם דרופ אוטומטי ב-3 מקטעים, פלקסיה אוטומטית עם זיכרון, כיפוף צידי עד 20° ומקטע חזה נשמט עד 15°.'),
         ('האם אפשר לבצע מתיחה ודקומפרסיה על המיטה?','בדגם Raphael 707 יש מתיחה צירית מוטורית עד 10 ס"מ ב-16 רמות, שאפשר לשלב עם פלקסיה וכיפוף צידי. דגם 606 מבצע פלקסיה-דיסטרקציה בשיטת Leander. למערכת דקומפרסיה ממוחשבת ייעודית ראו את עמוד הדקומפרסיה של עמוד השדרה.'),
         ('כמה מקום צריך בקליניקה?','לפי היצרן, מומלץ חלל של כ-3–3.5 מטר אורך ו-1.2–1.5 מטר רוחב סביב המיטה, כדי לאפשר תנועה חופשית של המטפל.'),
         ('האם המיטה מתאימה למטפל שמתחיל לעבוד בטכניקות דרופ ופלקסיה?','היצרן מציין שהדרופ החשמלי ב-707 מייצר כוח ותזמון קבועים ומפחית את התלות בכוח הידיים של המטפל. הדרכה על המיטה ניתנת עם ההתקנה.'),
         ('מי היצרן?','המיטות מיוצרות על ידי Young Il M (01M) מקוריאה, יצרנית ציוד לטיפול בעמוד השדרה. לפי היצרן, Raphael 707 רשומה ב-FDA ובעלת אישור CE, ו-Raphael 606 רשומה ב-FDA.'),
         ('כמה עולה מיטה כירופרקטית?','המחיר תלוי בדגם, בצבע ובאביזרים הנלווים. לקבלת הצעת מחיר מותאמת התקשרו ל-054-900-7723.')]
    body=hero('מיטה כירופרקטית Raphael','לשיקום הגב',
      'מיטות כירופרקטיות מסדרת Raphael של היצרן הקוריאני Young Il M (01M), לטיפול ידני בעמוד השדרה בקליניקות פיזיותרפיה, כירופרקטיקה, אורתופדיה ומרפאות כאב. שני דגמים: <strong>Raphael 707</strong> – מערכת משולבת של דרופ חשמלי, פלקסיה אוטומטית, מתיחה צירית וגובה חשמלי עם מסך מגע; ו-<strong>Raphael 606</strong> – מיטה בטכניקת פלקסיה-דיסטרקציה בשיטת Leander עם דרופ אוטומטי ב-3 מקטעים.',
      IMG_707,'מיטה כירופרקטית Raphael 707 לשיקום הגב')
    body+=sec('שני דגמים, שתי גישות טיפול',grid([
      card('Raphael 707 – מערכת משולבת',small('דרופ · פלקסיה · פלקסיה אוטומטית · מתיחה צירית · כיפוף צידי · גובה חשמלי – הכול במיטה אחת, עם מסך מגע וזיכרון פרוטוקולים.'),'#raphael-707',IMG_707,'Raphael 707 מיטה כירופרקטית עם מסך מגע'),
      card('Raphael 606 – פלקסיה-דיסטרקציה (Leander)',small('מיטה שנבנתה ברישיון Leander, עם דרופ אוטומטי ב-3 מקטעים, פלקסיה אוטומטית עם זיכרון וכיפוף צידי.'),'#raphael-606',IMG_606,'Raphael 606 מיטה כירופרקטית Leander')],n=2))
    body+=sec('Raphael 707',
      p('Raphael 707 (גרסת 707-K) נועדה לרכז במיטה אחת טכניקות שבדרך כלל דורשות כמה מיטות: דרופ בשיטת Thompson, פלקסיה בשיטות Cox ו-Leander, ומתיחה צירית לדקומפרסיה. הדרופ מופעל במנוע עם חיישן, ללא מדחס אוויר – ולכן העבודה שקטה והנחיתה רכה.')+
      table(['מאפיין','Raphael 707'],[
       ['דרופ','מוטורי ומוגן בפטנט, ללא מדחס; מקטעים: צוואר, חזה/מותן ואגן; מעבר מהיר בין אוטומטי לחצי-אוטומטי'],
       ['פלקסיה אוטומטית','עד 22.4° ב-8 רמות; עד 30 חזרות'],
       ['מתיחה צירית','מוטורית, עד 10 ס"מ ב-16 רמות; מתיחה לסירוגין'],
       ['שילובים','מתיחה + פלקסיה + כיפוף צידי במקביל'],
       ['הפעלה','מסך מגע 10 אינץ׳ על מעמד; זיכרון ל-3 פרוטוקולים'],
       ['גובה','הגבהה חשמלית 59–89 ס"מ'],
       ['מידות ומשקל','רוחב 67 ס"מ, אורך 176–228 ס"מ, משקל 135 ק"ג'],
       ['אביזרים כלולים','חגורת COX, חגורת COX צווארית, מוט פלקסיה ידני, כרית Dutchman Roll, כרית ברכיים משולשת'],
       ['אופציות','חגורת סקוליוזיס, ערסל צוואר, סט חגורות מתיחה'],
       ['אישורים (לפי היצרן)','רישום FDA ואישור CE']]),alt=True,id_='raphael-707')
    body+=sec('Raphael 606',
      p('Raphael 606 נבנתה ברישיון Leander ומתמקדת בטכניקת פלקסיה-דיסטרקציה. הדרופ האוטומטי בשלושה מקטעים פועל בתנועה אנכית ממורכזת, וניתן לעבור בין מצב אוטומטי, חצי-אוטומטי וידני.')+
      table(['מאפיין','Raphael 606'],[
       ['דרופ','אוטומטי ב-3 מקטעים (צוואר, חזה, אגן); אוטומטי / חצי-אוטומטי / ידני'],
       ['פלקסיה אוטומטית','10 רמות מהירות, עד 30 דקות, זיכרון והשהיה של 3 שניות'],
       ['כיפוף צידי','עד 20°'],
       ['מקטע חזה נשמט','עד 15°'],
       ['הפעלה','לוח בקרה אלקטרוני מובנה; הגבהה חשמלית'],
       ['מידות','רוחב 64 ס"מ, אורך 186–226 ס"מ, גובה 58.5–73.5 ס"מ'],
       ['משקל ועומס','142 ק"ג; עומס בטוח 150 ק"ג; 220V'],
       ['אופציות','חגורת COX, חגורת סקוליוזיס'],
       ['אישורים (לפי היצרן)','רישום FDA']]),id_='raphael-606')
    body+=sec('Raphael 707 מול Raphael 606',table(['','Raphael 707','Raphael 606'],[
      ['גישה מרכזית','מערכת משולבת: דרופ, פלקסיה ומתיחה','פלקסיה-דיסטרקציה בשיטת Leander'],
      ['מתיחה צירית','כן, עד 10 ס"מ','לא'],
      ['פלקסיה אוטומטית','עד 22.4°, 8 רמות','10 רמות מהירות, עד 30 דקות'],
      ['כיפוף צידי','כן, בשילוב עם מתיחה ופלקסיה','עד 20°'],
      ['ממשק','מסך מגע 10 אינץ׳','לוח בקרה מובנה'],
      ['טווח גובה','59–89 ס"מ','58.5–73.5 ס"מ']]),alt=True)
    body+=sec('למי מתאימה מיטה כירופרקטית?',
      ul(['פיזיותרפיסטים וכירופרקטורים שמשלבים טכניקות דרופ ופלקסיה בטיפול בגב ובצוואר.',
          'מרפאות כאב, אורתופדיה ורפואה משקמת שמפעילות תוכנית שמרנית לעמוד השדרה.',
          'מטפלים שרוצים להפחית עומס על פרקי הידיים והכתפיים בטיפול ידני חוזר.',
          'מרכזי עמוד שדרה שמעוניינים בפרוטוקולים אחידים שניתנים לשחזור בין מטפלים.'])+
      p('המיטה הכירופרקטית משתלבת היטב עם מערכות נוספות לשיקום הגב: <a href="/spinal-decompression" class="underline" '+C+'>דקומפרסיה של עמוד השדרה</a> ממוחשבת (Spine-MT), <a href="/product/robotic-bed" class="underline" '+C+'>מיטה רובוטית טיפולית</a> ו<a href="/shockwave-devices" class="underline" '+C+'>מכשירי גלי הלם</a> לטיפול ברקמות רכות.'))
    body+=faqsec(faq)
    body+=disclaimer('הנתונים הטכניים בעמוד לקוחים מפרסומי היצרן Young Il M (01M) ועשויים להשתנות. המידע מיועד לאנשי מקצוע ואינו מהווה ייעוץ רפואי.')
    body+=related([('דקומפרסיה של עמוד השדרה','/spinal-decompression'),('Spine-MT','/product/spine-mt'),('Spine MT Core','/product/spine-mt-core'),('מיטה רובוטית טיפולית','/product/robotic-bed'),('מכשירי גלי הלם לקליניקה','/shockwave-devices'),('מכשירים לקליניקות','/clinic-equipment')])
    og_product('מיטה כירופרקטית Raphael','לשיקום הגב | דגמים 707 ו-606','tools/seo/src/raphael-707.png','og/chiropractic-beds.jpg')
    build(path,'chiropractic-beds.html',title,desc,'og/chiropractic-beds.jpg','מיטה כירופרקטית Raphael – איי גרופ',[crumbs('מיטה כירופרקטית Raphael',path),faqld(faq)],body)

if __name__=='__main__':
    main()

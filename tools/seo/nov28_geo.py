"""Nov 28 2026 GEO pass (idempotent). Run from repo root AFTER nov26_pages.py and nov26_sitewide.py:
    python3 tools/seo/nov26_pages.py && python3 tools/seo/nov26_sitewide.py && python3 tools/seo/nov28_geo.py
What it does
 1. Official-importer / importer+distributor first paragraph (data-geo-importer="2") on every product page.
    'יבואנית רשמית ובלעדית' only where the site already states exclusive importer (Longest products);
    everything else keeps the 'יבואנית ומפיצה' wording.
 2. Short English summary (lang="en") under it (data-geo-en="1").
 3. New dedicated page /product/raphael-707 (Raphael 707 only) + FAQ/Product JSON-LD + OG image,
    internal links from home, clinic-equipment, blog, chiropractic-beds, related chips, footer.
 4. Strengthens /chiropractic-beds (buying guide section, 707 link, 3 extra FAQs + FAQPage JSON-LD).
 5. sitemap.xml + llms.txt entries.
"""
import re, json, glob, html, sys, os
sys.path.insert(0,'tools/seo')
from nov26_pages import (sec,p,ul,card,grid,small,table,faqsec,related,disclaimer,seo,crumbs,faqld,C,W,esc,BASE)
from make_og import product as og_product
TODAY='2026-11-28'
changed=set()
def rd(f): return open(f,encoding='utf-8').read()
def wr(f,s,old):
    if s!=old: open(f,'w',encoding='utf-8').write(s); changed.add(f)
PHONE='054-900-7723'
ADDR_HE='המשרד במאיר אריאל 6, נתניה, טלפון '+PHONE+'.'
ADDR_EN='We are based at Meir Ariel 6, Netanya; call or WhatsApp '+PHONE+'.'
def he(kind,dev):
    if kind=='official':
        return f'איי גרופ (I-Group Medical Tech) היא היבואנית הרשמית והבלעדית של Longest בישראל ומשווקת את {dev} לקליניקות, עם אחריות, שירות ותמיכה מקומיים. {ADDR_HE}'
    return f'איי גרופ (I-Group Medical Tech) היא יבואנית ומפיצה של {dev} בישראל, עם אחריות ושירות מקומיים. {ADDR_HE}'
def en(kind,what):
    if kind=='official':
        return f'{what}. I-Group Medical Tech is the official and exclusive importer of Longest in Israel, providing local warranty and service. {ADDR_EN}'
    return f'{what}. I-Group Medical Tech imports and distributes it in Israel, with local warranty and service. {ADDR_EN}'
# page -> (kind, hebrew device phrase, english "what is it" sentence start, anchor)
PAGES={
 'product/ultrawave-lgt-2620.html':('official','מכשיר גלי ההלם הממוקדים Ultrawave LGT-2620','The Ultrawave LGT-2620 is an electromagnetic focused shockwave therapy device for physiotherapy, orthopedic and pain clinics','sub'),
 'product/powershocker-lgt-2500s-plus.html':('official','מכשיר גלי ההלם הרדיאליים PowerShocker LGT-2500S PLUS','The PowerShocker LGT-2500S PLUS is a radial shockwave therapy device for physiotherapy, sports and pain clinics','sub'),
 'product/lgt-2410s.html':('official','מערכת הקריותרפיה הממוקדת LGT-2410S','The LGT-2410S is a focused CO2 cryotherapy system for clinics','sub'),
 'product/rehamoto-5100p.html':('official','מאמן הגפיים האקטיבי-פסיבי RehaMoto LGT-5100P','The RehaMoto LGT-5100P is an active-passive rehabilitation trainer for the upper and lower limbs','sub'),
 'kin/product/5100p.html':('official','מאמן הגפיים האקטיבי-פסיבי RehaMoto LGT-5100P','The RehaMoto LGT-5100P is an active-passive rehabilitation trainer for the upper and lower limbs','h1'),
 'kin/product/5100d.html':('official','מאמן הגפיים האקטיבי-פסיבי RehaMoto LGT-5100D','The RehaMoto LGT-5100D is a motorized active-passive rehabilitation trainer for the upper and lower limbs','h1'),
 'kin/product/5100d-config-ii.html':('official','מאמן הגפיים האקטיבי-פסיבי RehaMoto LGT-5100D Config II','The RehaMoto LGT-5100D Config II is a motorized active-passive rehabilitation trainer for the upper and lower limbs','h1'),
 'product/spine-mt.html':('dist','מכשיר הדקומפרסיה הממוחשבת Spine-MT','Spine-MT is a computerized spinal decompression system for clinics','sub'),
 'product/spine-mt-core.html':('dist','מכשיר Spine MT Core לשיקום עמוד השדרה','Spine MT Core is a spinal rehabilitation and decompression system for clinics','sub'),
 'product/tera-master.html':('dist','מערכת Therapy Master (THERA MASTER)','Therapy Master is a combined spinal decompression and therapy system for clinics','sub'),
 'product/biomag-lumina.html':('dist','מכשירי המגנטותרפיה Biomag, כולל Lumina 3D-e','Biomag Lumina 3D-e is a 3D pulsed electromagnetic field (PEMF) therapy device for clinics and home use','sub'),
 'product/robotic-bed.html':('dist','המיטה הרובוטית הטיפולית','The robotic therapy bed is a rehabilitation bed that performs controlled, repeatable treatment movements set by the therapist','sub'),
 'product/ultrasound.html':('dist','מערכת האולטרסאונד הטיפולי SonNext','SonNext is a non-thermal therapeutic ultrasound system for physiotherapy and rehabilitation clinics','sub'),
 'chiropractic-beds.html':('dist','מיטות Raphael הכירופרקטיות, כולל הדגמים 707 ו-606','Raphael chiropractic tables, including the 707 and 606 models, are spinal treatment tables for back rehabilitation clinics','sub'),
 'product/raphael-707.html':('dist','מיטה כירופרקטית Raphael 707','The Raphael 707 is a chiropractic table for back rehabilitation that combines a motorized drop, automatic flexion, axial traction and electric height adjustment with a 10-inch touch screen','sub'),
}
EN_CLS='text-sm text-muted-foreground leading-relaxed mb-4'
def importer_blocks(kind,dev,what,cls):
    a=f'<p class="{cls}" data-geo-importer="2">{he(kind,dev)}</p>'
    b=f'<p lang="en" dir="ltr" class="{EN_CLS}" style="text-align:left" data-geo-en="1">{html.escape(en(kind,what),quote=False)}</p>'
    return a+b
def patch_importer(f):
    kind,dev,what,anchor=PAGES[f]
    o=h=rd(f)
    h=re.sub(r'<p lang="en"[^>]*data-geo-en="1">.*?</p>','',h,flags=re.S)
    m=re.search(r'<p class="([^"]*)" data-geo-importer="\d">.*?</p>',h,flags=re.S)
    if m:
        h=h[:m.start()]+importer_blocks(kind,dev,what,m.group(1))+h[m.end():]
    else:
        cls='text-sm md:text-base text-foreground leading-relaxed mb-4' if anchor=='sub' else 'text-base text-foreground leading-relaxed mb-3'
        blk=importer_blocks(kind,dev,what,cls)
        i=h.find('</h1>'); assert i>0,f
        if anchor=='sub':
            mm=re.compile(r'<p class="text-lg[^"]*"[^>]*>.*?</p>',re.S).match(h,i+5)
            assert mm,f
            pos=mm.end()
        else: pos=i+5
        h=h[:pos]+blk+h[pos:]
    wr(f,h,o)
# ---------------- Raphael 707 dedicated page ----------------
IMG_707='/assets/img/raphael-707-chiropractic-table.webp'
RLINK='/product/raphael-707'
L=lambda u,t: f'<a href="{u}" class="underline" {C}>{t}</a>'
FAQ707=[
 ('מהי מיטה כירופרקטית Raphael 707?','Raphael 707 (גרסת 707-K) היא מיטה כירופרקטית לשיקום הגב של היצרן הקוריאני Young Il M (01M). היא מרכזת במיטה אחת דרופ מוטורי, פלקסיה אוטומטית, מתיחה צירית וכיפוף צידי, עם הגבהה חשמלית ומסך מגע 10 אינץ׳, לשימוש בקליניקות פיזיותרפיה, כירופרקטיקה, אורתופדיה ומרפאות כאב.'),
 ('אילו טכניקות אפשר לבצע על Raphael 707?','לפי היצרן, המיטה נועדה לרכז טכניקות שבדרך כלל דורשות כמה מיטות: דרופ בשיטת Thompson, פלקסיה-דיסטרקציה בשיטות Cox ו-Leander, מתיחה צירית לדקומפרסיה וכיפוף צידי. הבחירה בטכניקה ובפרוטוקול נתונה לשיקול דעתו של המטפל.'),
 ('במה שונה דרופ מוטורי מדרופ פנאומטי?','הדרופ ב-Raphael 707 מופעל במנוע עם חיישן ומוגן בפטנט, ללא מדחס אוויר. לפי היצרן, המשמעות היא עבודה שקטה, נחיתה רכה וכוח ותזמון קבועים שמפחיתים את התלות בכוח הידיים של המטפל.'),
 ('האם יש במיטה מתיחה צירית ודקומפרסיה?','כן. ב-Raphael 707 יש מתיחה צירית מוטורית עד 10 ס"מ ב-16 רמות, כולל מתיחה לסירוגין, ואפשר לשלב מתיחה, פלקסיה וכיפוף צידי במקביל. למערכת דקומפרסיה ממוחשבת ייעודית ראו את עמוד ה-Spine-MT.'),
 ('מה המידות, המשקל והחלל הנדרש בקליניקה?','רוחב 67 ס"מ, אורך 176–228 ס"מ, גובה בהגבהה חשמלית 59–89 ס"מ ומשקל 135 ק"ג. לפי היצרן מומלץ חלל של כ-3–3.5 מטר אורך ו-1.2–1.5 מטר רוחב סביב המיטה.'),
 ('אילו אביזרים כלולים במיטה?','חגורת COX, חגורת COX צווארית, מוט פלקסיה ידני, כרית Dutchman Roll וכרית ברכיים משולשת. אופציות: חגורת סקוליוזיס, ערסל צוואר וסט חגורות מתיחה.'),
 ('האם Raphael 707 מאושרת?','לפי היצרן, Raphael 707 רשומה ב-FDA ובעלת אישור CE. נשמח לשלוח את פרטי האישורים יחד עם הצעת המחיר.'),
 ('מי מייבא את Raphael 707 לישראל ואיך מקבלים שירות?','איי גרופ (I-Group Medical Tech) היא יבואנית ומפיצה של מיטות Raphael בישראל, עם אחריות ושירות מקומיים. המשרד במאיר אריאל 6, נתניה, טלפון 054-900-7723. הדרכה על המיטה ניתנת עם ההתקנה, ופרטי האחריות והשירות מפורטים בהצעת המחיר.'),
 ('כמה עולה Raphael 707 ואפשר לקבל הדגמה?','המחיר תלוי בצבע ובאביזרים הנלווים. לקבלת הצעת מחיר מותאמת ולתיאום שיחת ייעוץ והדגמה התקשרו לעמירם 050-917-6111 או לאינה 054-936-9742.'),
]
SPEC707=[
 ['דרופ','מוטורי ומוגן בפטנט, ללא מדחס; מקטעים: צוואר, חזה/מותן ואגן; מעבר מהיר בין אוטומטי לחצי-אוטומטי'],
 ['פלקסיה אוטומטית','עד 22.4° ב-8 רמות; עד 30 חזרות'],
 ['מתיחה צירית','מוטורית, עד 10 ס"מ ב-16 רמות; מתיחה לסירוגין'],
 ['שילובים','מתיחה + פלקסיה + כיפוף צידי במקביל'],
 ['הפעלה','מסך מגע 10 אינץ׳ על מעמד; זיכרון ל-3 פרוטוקולים'],
 ['גובה','הגבהה חשמלית 59–89 ס"מ'],
 ['מידות ומשקל','רוחב 67 ס"מ, אורך 176–228 ס"מ, משקל 135 ק"ג'],
 ['אביזרים כלולים','חגורת COX, חגורת COX צווארית, מוט פלקסיה ידני, כרית Dutchman Roll, כרית ברכיים משולשת'],
 ['אופציות','חגורת סקוליוזיס, ערסל צוואר, סט חגורות מתיחה'],
 ['אישורים (לפי היצרן)','רישום FDA ואישור CE'],
 ['יצרן','Young Il M (01M), קוריאה']]
def build707():
    base=rd('chiropractic-beds.html')
    head=base[:base.find('</nav>')+6]; foot=base[base.find('<footer'):]
    kind,dev,what,_=PAGES['product/raphael-707.html']
    path=RLINK
    title='מיטה כירופרקטית Raphael 707 – לשיקום הגב | איי גרופ'
    desc='מיטה כירופרקטית Raphael 707 לשיקום הגב: דרופ מוטורי, פלקסיה אוטומטית, מתיחה צירית ומסך מגע. מפרט מלא, שאלות נפוצות והדגמה בישראל עם איי גרופ, נתניה.'
    hero_h=('<section class="relative pt-24 pb-12 overflow-hidden">'+W+'<div class="grid lg:grid-cols-2 gap-8 lg:gap-12 items-center">'
      '<div class="relative rounded-2xl overflow-hidden border border-border/50 shadow-lg" style="background-color: rgb(232, 238, 245);"><img src="'+IMG_707+'" alt="מיטה כירופרקטית Raphael 707 לשיקום הגב – מסך מגע ודרופ מוטורי" class="w-full aspect-[4/3] object-contain"></div>'
      '<div><h1 class="text-3xl md:text-4xl font-bold mb-2" '+C+'>מיטה כירופרקטית Raphael 707</h1><p class="text-lg font-medium mb-4" '+C+'>לשיקום הגב</p>'
      +importer_blocks(kind,dev,what,'text-sm md:text-base text-foreground leading-relaxed mb-4')+
      '<p class="text-sm md:text-base text-muted-foreground leading-relaxed mb-6">Raphael 707 (גרסת 707-K) של היצרן הקוריאני Young Il M (01M) מרכזת במיטה אחת דרופ מוטורי, פלקסיה אוטומטית, מתיחה צירית וכיפוף צידי, עם הגבהה חשמלית ומסך מגע 10 אינץ׳ – לקליניקות פיזיותרפיה, כירופרקטיקה, אורתופדיה ומרפאות כאב.</p>'
      '<div class="flex flex-wrap gap-3"><a href="tel:0509176111" class="inline-flex items-center justify-center rounded-md text-sm font-medium bg-primary text-primary-foreground shadow hover:bg-primary/90 h-9 px-4 py-2">עמירם: 050-917-6111</a><a href="tel:0549369742" class="inline-flex items-center justify-center rounded-md text-sm font-medium bg-primary text-primary-foreground shadow hover:bg-primary/90 h-9 px-4 py-2">אינה: 054-936-9742</a>'
      '<a href="/phone-consultation" class="inline-flex items-center justify-center rounded-md text-sm font-medium border border-border h-9 px-4 py-2">קביעת שיחת ייעוץ</a></div></div></div></div></section>')
    body=hero_h
    body+=sec('מה מייחד את Raphael 707',grid([
      card('דרופ מוטורי ושקט',small('הדרופ מופעל במנוע עם חיישן ומוגן בפטנט, ללא מדחס אוויר, ולכן העבודה שקטה והנחיתה רכה. מקטעים: צוואר, חזה/מותן ואגן, עם מעבר מהיר בין מצב אוטומטי לחצי-אוטומטי.')),
      card('פלקסיה אוטומטית',small('פלקסיה אוטומטית עד 22.4° ב-8 רמות ועד 30 חזרות, לעבודה חוזרת בכוח ובתזמון קבועים.')),
      card('מתיחה צירית',small('מתיחה צירית מוטורית עד 10 ס"מ ב-16 רמות, כולל מתיחה לסירוגין, עם אפשרות לשלב פלקסיה וכיפוף צידי במקביל.')),
      card('מסך מגע וזיכרון',small('מסך מגע 10 אינץ׳ על מעמד, זיכרון ל-3 פרוטוקולים והגבהה חשמלית 59–89 ס"מ להתאמה לגובה המטפל והמטופל.'))],n=2))
    body+=sec('טכניקות שאפשר לבצע על המיטה',
      p('לפי היצרן, Raphael 707 נועדה לרכז במיטה אחת טכניקות שבדרך כלל דורשות כמה מיטות. הבחירה בטכניקה ובפרוטוקול נתונה תמיד לשיקול דעתו של המטפל.')+
      ul(['<strong>דרופ בשיטת Thompson</strong> – נחיתה רכה בעזרת הדרופ המוטורי, בלי מדחס אוויר.',
          '<strong>פלקסיה-דיסטרקציה בשיטות Cox ו-Leander</strong> – פלקסיה אוטומטית עד 22.4° בשילוב מתיחה.',
          '<strong>מתיחה צירית לדקומפרסיה</strong> – מתיחה מוטורית עד 10 ס"מ ב-16 רמות.',
          '<strong>כיפוף צידי</strong> – ניתן לשלב עם מתיחה ופלקסיה באותו טיפול.']),alt=True,id_='techniques')
    body+=sec('מפרט טכני – Raphael 707',table(['מאפיין','Raphael 707'],SPEC707),id_='specs')
    body+=sec('למה קליניקות בוחרות מיטה כירופרקטית משולבת?',
      ul(['<strong>מיטה אחת במקום כמה</strong> – דרופ, פלקסיה ומתיחה באותה מערכת, וחיסכון בשטח הקליניקה.',
          '<strong>פחות עומס על המטפל</strong> – הדרופ המוטורי מפחית את התלות בכוח הידיים ומקל על פרקי הידיים והכתפיים בטיפול ידני חוזר.',
          '<strong>פרוטוקולים אחידים</strong> – זיכרון לשלושה פרוטוקולים ובקרה במסך מגע מאפשרים עבודה שניתנת לשחזור בין מטפלים.',
          '<strong>עבודה שקטה</strong> – ללא מדחס אוויר, לחוויית טיפול רגועה יותר.'])+
      p('המיטה הכירופרקטית משתלבת עם מערכות נוספות לשיקום הגב: '+L('/spinal-decompression','דקומפרסיה של עמוד השדרה')+' ממוחשבת ('+L('/product/spine-mt','Spine-MT')+'), '+L('/product/robotic-bed','מיטה רובוטית טיפולית')+' ו'+L('/shockwave-devices','מכשירי גלי הלם')+' לטיפול ברקמות רכות.'),alt=True)
    body+=sec('Raphael 707 לעומת פתרונות נוספים לעמוד השדרה',table(['','מיטה כירופרקטית Raphael 707','דקומפרסיה ממוחשבת (Spine-MT)','מיטה רובוטית טיפולית'],[
      ['עיקרון','מיטה לטיפול ידני של המטפל, עם דרופ, פלקסיה ומתיחה מוטוריים','מערכת דקומפרסיה ממוחשבת עם שליטה דיגיטלית בזוויות ובכוחות','תנועות טיפוליות מדויקות לפי פרמטרים שהוגדרו על ידי המטפל'],
      ['מי מפעיל','המטפל, בשילוב טכניקות הדרופ והפלקסיה','המטפל מגדיר את הפרוטוקול והמערכת מבצעת','המטפל מגדיר פרמטרים, והמערכת מנטרת את תגובת הגוף'],
      ['עמוד המוצר','זהו העמוד',L('/product/spine-mt','Spine-MT'),L('/product/robotic-bed','מיטה רובוטית')]]))
    body+=sec('איך זה עובד עם איי גרופ',
      p('איי גרופ (I-Group Medical Tech) היא יבואנית ומפיצה של מיטות Raphael בישראל, עם אחריות ושירות מקומיים. המשרד במאיר אריאל 6, נתניה, פתוח א׳–ה׳ 09:00–18:00.')+
      ul(['שיחת ייעוץ והדגמה עם עמירם או אינה – '+L('/phone-consultation','קביעת שיחה')+'.',
          'הצעת מחיר מותאמת לפי צבע ואביזרים.',
          'התקנה והדרכה על המיטה (ההדרכה ניתנת עם ההתקנה).',
          'אחריות ושירות מקומיים – הפרטים מפורטים בהצעת המחיר.']),alt=True,id_='process')
    body+=faqsec(FAQ707)
    body+=sec('עוד על מיטות כירופרקטיות',
      p('לסקירה כללית של הסדרה ראו את עמוד '+L('/chiropractic-beds','מיטה כירופרקטית Raphael – לשיקום הגב')+', ולמדריך לבחירת מיטה כירופרקטית לקליניקה קראו את '+L('/blog/chiropractic-table-guide','המדריך בבלוג')+'. סקירה של כל המכשור לקליניקה: '+L('/clinic-equipment','מכשירים לקליניקות')+'.'))
    body+=disclaimer('הנתונים הטכניים בעמוד לקוחים מפרסומי היצרן Young Il M (01M) ועשויים להשתנות. המידע מיועד לאנשי מקצוע ואינו מהווה ייעוץ רפואי.')
    body+=related([('מיטה כירופרקטית Raphael – לשיקום הגב','/chiropractic-beds'),('מדריך: מיטה כירופרקטית לקליניקה','/blog/chiropractic-table-guide'),('דקומפרסיה של עמוד השדרה','/spinal-decompression'),('Spine-MT','/product/spine-mt'),('מיטה רובוטית טיפולית','/product/robotic-bed'),('מכשירים לקליניקות','/clinic-equipment')])
    og_product('מיטה כירופרקטית Raphael 707','לשיקום הגב','tools/seo/src/raphael-707.png','og/product-raphael-707.jpg')
    prod={"@context":"https://schema.org","@type":["Product","MedicalDevice"],"@id":BASE+RLINK+"#product",
      "name":"מיטה כירופרקטית Raphael 707","alternateName":["Raphael 707","Raphael 707-K chiropractic table"],"model":"707",
      "description":"מיטה כירופרקטית Raphael 707 לשיקום הגב של היצרן הקוריאני Young Il M (01M): דרופ מוטורי ללא מדחס, פלקסיה אוטומטית עד 22.4°, מתיחה צירית עד 10 ס\"מ, כיפוף צידי, הגבהה חשמלית 59–89 ס\"מ ומסך מגע 10 אינץ׳.",
      "url":BASE+RLINK,"brand":{"@type":"Brand","name":"Raphael"},"category":"Medical Devices > Chiropractic Tables",
      "manufacturer":{"@type":"Organization","name":"Young Il M (01M)"},
      "image":[BASE+"/og/product-raphael-707.jpg",BASE+IMG_707],
      "additionalProperty":[{"@type":"PropertyValue","name":n,"value":v} for n,v in [("פלקסיה אוטומטית","עד 22.4° ב-8 רמות"),("מתיחה צירית","עד 10 ס\"מ ב-16 רמות"),("מסך","מסך מגע 10 אינץ׳"),("גובה","59–89 ס\"מ, חשמלי"),("משקל","135 ק\"ג"),("אישורים (לפי היצרן)","FDA, CE")]],
      "seller":{"@type":"Organization","name":"I-Group Medical Tech","url":BASE+"/","telephone":"+972-54-900-7723",
                "address":{"@type":"PostalAddress","streetAddress":"מאיר אריאל 6","addressLocality":"נתניה","addressCountry":"IL"}}}
    bc={"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
        {"@type":"ListItem","position":1,"name":"דף הבית","item":BASE+"/"},
        {"@type":"ListItem","position":2,"name":"מיטה כירופרקטית Raphael","item":BASE+"/chiropractic-beds"},
        {"@type":"ListItem","position":3,"name":"Raphael 707","item":BASE+RLINK}]}
    h=head
    a=h.find('<!-- seo:start -->'); b=h.find('<!-- seo:end -->')+len('<!-- seo:end -->')
    h=h[:a]+seo(title,desc,path,'og/product-raphael-707.jpg','מיטה כירופרקטית Raphael 707 – איי גרופ',[bc,faqld(FAQ707),prod])+h[b:]
    out=h+body+foot
    f='product/raphael-707.html'
    if not os.path.exists(f) or rd(f)!=out:
        open(f,'w',encoding='utf-8').write(out); changed.add(f)
# ---------------- links ----------------
REL='<a href="{u}" class="inline-block rounded-full border border-border/60 px-4 py-2 text-sm hover:bg-primary/10" '+C+'>{t}</a>'
R707=('/product/raphael-707','מיטה כירופרקטית Raphael 707')
def add_chip(h):
    a=h.find('aria-label="מוצרים קשורים"')
    if a<0: return h
    b=h.find('</nav>',a)
    if 'href="/product/raphael-707"' in h[a:b]: return h
    s=h.find('>',a)+1
    return h[:s]+REL.format(u=R707[0],t=R707[1])+h[s:]
FL='<li><a class="text-sm text-background/50 hover:text-primary transition-colors" href="{u}">{t}</a></li>'
def add_footer(h):
    if 'footlinks:start' not in h or 'href="/product/raphael-707">' in h[h.find('<footer'):]: return h
    chiro=FL.format(u='/chiropractic-beds',t='מיטה כירופרקטית Raphael')
    if chiro not in h: return h
    return h.replace(chiro,chiro+FL.format(u=R707[0],t='Raphael 707 – מיטה כירופרקטית'),1)
def patch_chiro():
    f='chiropractic-beds.html'; o=h=rd(f)
    # a) dedicated page section before the 707 section
    if 'id="r707-page"' not in h:
        blk=('<section id="r707-page" class="py-8">'+W+'<div class="max-w-4xl mx-auto bg-card rounded-2xl border border-border/50 p-6">'
             '<h2 class="text-xl md:text-2xl font-bold mb-3" '+C+'>Raphael 707 – עמוד מוצר ייעודי</h2>'
             '<p class="text-sm md:text-base text-muted-foreground leading-relaxed mb-3">כל הפרטים על הדגם המשולב – טכניקות, מפרט מלא, אביזרים, שאלות נפוצות ותהליך ההדגמה וההתקנה – בעמוד '
             +L(RLINK,'מיטה כירופרקטית Raphael 707 – לשיקום הגב')+'.</p></div></div></section>')
        i=h.find('<section id="raphael-707"'); h=h[:i]+blk+h[i:]
    # b) buying guide before FAQ
    if 'id="chiro-choose"' not in h:
        blk=sec('איך בוחרים מיטה כירופרקטית לקליניקה?',
          p('הבחירה מתחילה בטכניקות שהצוות עובד איתן ובנפח המטופלים. כמה שאלות שכדאי לשאול לפני רכישה:')+
          ul(['אילו טכניקות הצוות מבצע בפועל – דרופ, פלקסיה-דיסטרקציה, מתיחה צירית או שילוב ביניהן?',
              'האם נדרשת מיטה משולבת עם מתיחה צירית וכיפוף צידי (Raphael 707), או מיטה שממוקדת בפלקסיה-דיסטרקציה בשיטת Leander (Raphael 606)?',
              'כמה מקום פנוי יש בחדר הטיפולים? היצרן ממליץ על כ-3–3.5 מטר אורך ו-1.2–1.5 מטר רוחב סביב המיטה.',
              'אילו הדרכה, אחריות ושירות מקומי כלולים בהצעת המחיר, ומי נותן אותם בישראל?'])+
          p('למדריך מלא קראו את '+L('/blog/chiropractic-table-guide','מיטה כירופרקטית לשיקום הגב – מדריך לקליניקות')+', ולפרטי הדגם המשולב ראו את '+L(RLINK,'עמוד Raphael 707')+'.'),id_='chiro-choose')
        i=h.find('שאלות נפוצות</h2>'); s=h.rfind('<section',0,i); h=h[:s]+blk+h[s:]
    # c) extra FAQs (html + JSON-LD)
    extra=[('מי היבואן של מיטות Raphael בישראל ומה כולל השירות?','איי גרופ (I-Group Medical Tech) היא יבואנית ומפיצה של מיטות Raphael בישראל, עם אחריות ושירות מקומיים. הדרכה על המיטה ניתנת עם ההתקנה, ופרטי האחריות והשירות מפורטים בהצעת המחיר. המשרד במאיר אריאל 6, נתניה, טלפון 054-900-7723.'),
           ('אפשר לראות את Raphael 707 לפני רכישה?','כן. ניתן לתאם שיחת ייעוץ והדגמה עם עמירם (050-917-6111) או אינה (054-936-9742). פרטים נוספים בעמוד Raphael 707.'),
           ('אילו אביזרים כלולים ב-Raphael 707?','חגורת COX, חגורת COX צווארית, מוט פלקסיה ידני, כרית Dutchman Roll וכרית ברכיים משולשת. אופציות: חגורת סקוליוזיס, ערסל צוואר וסט חגורות מתיחה.')]
    if extra[0][0] not in h:
        det=''.join(f'<details class="bg-card rounded-xl border border-border/50 p-4"><summary class="font-semibold cursor-pointer" {C}>{q}</summary><p class="text-sm text-muted-foreground leading-relaxed mt-3">{a}</p></details>' for q,a in extra)
        i=h.find('שאלות נפוצות</h2>'); j=h.find('</div></section>',i)
        h=h[:j]+det+h[j:]
        def fix(m):
            d=json.loads(m.group(1))
            if d.get('@type')!='FAQPage': return m.group(0)
            d['mainEntity']+=[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in extra]
            return '<script type="application/ld+json">'+json.dumps(d,ensure_ascii=False)+'</script>'
        h=re.sub(r'<script type="application/ld\+json">(.*?)</script>',fix,h,flags=re.S)
    wr(f,h,o)
def patch_misc():
    # home: link in audience table
    f='index.html'; o=h=rd(f)
    old=L('/chiropractic-beds','מיטה כירופרקטית')+', '+L('/product/robotic-bed','מיטה רובוטית')
    if old in h and 'href="/product/raphael-707"' not in h.split('<footer')[0]:
        h=h.replace(old,L('/chiropractic-beds','מיטה כירופרקטית')+' ('+L(RLINK,'Raphael 707')+'), '+L('/product/robotic-bed','מיטה רובוטית'),1)
    wr(f,h,o)
    # clinic-equipment: card
    f='clinic-equipment.html'; o=h=rd(f)
    if 'href="/product/raphael-707"' not in h.split('<footer')[0]:
        k=h.find('Raphael 707 עם דרופ חשמלי, פלקסיה ומתיחה צירית, ו-Raphael 606 בטכניקת Leander.</p></a>')
        assert k>0
        e=k+len('Raphael 707 עם דרופ חשמלי, פלקסיה ומתיחה צירית, ו-Raphael 606 בטכניקת Leander.</p></a>')
        h=h[:e]+('<a href="'+RLINK+'" class="bg-card rounded-2xl border border-border/50 p-6 block hover:shadow-lg transition-shadow"><h3 class="text-base font-bold mb-2" '+C+'>מיטה כירופרקטית Raphael 707 – לשיקום הגב</h3><p class="text-sm text-muted-foreground leading-relaxed">דרופ מוטורי, פלקסיה אוטומטית, מתיחה צירית ומסך מגע 10 אינץ׳ – כל הפרטים והשאלות הנפוצות בעמוד אחד.</p></a>')+h[e:]
    wr(f,h,o)
    # blog guide: inline paragraph before related section
    f='blog/chiropractic-table-guide.html'; o=h=rd(f)
    if 'id="r707-link"' not in h:
        i=h.find('aria-label="מוצרים קשורים"'); s=h.rfind('<section',0,i)
        blk=('<section id="r707-link" class="py-6">'+W+p('לפרטים על הדגם המשולב עם דרופ מוטורי, פלקסיה אוטומטית ומתיחה צירית ראו את '+L(RLINK,'עמוד מיטה כירופרקטית Raphael 707')+'.')+'</div></section>')
        h=h[:s]+blk+h[s:]
    wr(f,h,o)
CHIPS=['chiropractic-beds.html','product/robotic-bed.html','product/spine-mt.html','product/spine-mt-core.html','product/tera-master.html','spinal-decompression.html']+glob.glob('blog/*.html')
def main():
    for f in PAGES:
        if f=='product/raphael-707.html': continue
        patch_importer(f)
    build707()
    patch_importer('product/raphael-707.html')   # no-op safety (already built with blocks)
    patch_chiro(); patch_misc()
    for f in CHIPS:
        o=h=rd(f); wr(f,add_chip(h),o)
    for f in glob.glob('*.html')+glob.glob('product/*.html')+glob.glob('kin/product/*.html')+glob.glob('blog/*.html')+glob.glob('kin/*.html'):
        if 'העמוד עבר' in rd(f)[:600]: continue
        o=h=rd(f); wr(f,add_footer(h),o)
    # sitemap
    sm=rd('sitemap.xml'); o=sm
    if '/product/raphael-707</loc>' not in sm:
        sm=sm.replace('</urlset>',f'  <url><loc>{BASE}/product/raphael-707</loc><lastmod>{TODAY}</lastmod></url>\n</urlset>')
    for f in changed:
        path='/' if f=='index.html' else ('/blog/' if f=='blog/index.html' else '/kin' if f=='kin/index.html' else '/'+f[:-5])
        sm=re.sub(r'(<loc>https://i-group\.co\.il'+re.escape(path)+r'</loc><lastmod>)[^<]+',r'\g<1>'+TODAY,sm)
    wr('sitemap.xml',sm,o)
    # llms.txt
    t=rd('llms.txt'); o=t
    t=t.replace('- Raphael 707 / 606 — מיטה כירופרקטית לשיקום הגב: https://i-group.co.il/chiropractic-beds',
                '- Raphael 707 — מיטה כירופרקטית לשיקום הגב (דרופ מוטורי, פלקסיה אוטומטית, מתיחה צירית, מסך מגע): https://i-group.co.il/product/raphael-707\n- Raphael 707 / 606 — סדרת מיטות כירופרקטיות Raphael: https://i-group.co.il/chiropractic-beds')
    if 'raphael-707' not in t.split('## עמודים חשובים')[1]:
        t=t.replace('- ציוד לקליניקה: https://i-group.co.il/clinic-equipment','- מיטה כירופרקטית Raphael 707: https://i-group.co.il/product/raphael-707\n- ציוד לקליניקה: https://i-group.co.il/clinic-equipment')
    if 'Official importer status' not in t:
        t=t.replace('## עברית','''Official importer status (per I-Group site content): I-Group Medical Tech is the official and exclusive importer of Longest in Israel (shockwave devices Ultrawave LGT-2620, LGT-2520GP, PowerShocker LGT-2500S PLUS; LGT-2410S cryotherapy; RehaMoto LGT-5100D / 5100P), with local warranty and service. For Spine-MT, Spine MT Core, Therapy Master, Biomag, Raphael chiropractic tables (model 707), the robotic therapy bed and SonNext ultrasound, I-Group is the importer and distributor in Israel, with local warranty and service.
Raphael 707: a chiropractic table for back rehabilitation (motorized drop, automatic flexion up to 22.4 degrees, axial traction up to 10 cm, lateral flexion, electric height 59-89 cm, 10-inch touch screen), made by Young Il M (01M), Korea. Page: https://i-group.co.il/product/raphael-707

## עברית''',1)
        t=t.replace('איי גרופ היא היבואנית הבלעדית של Longest בישראל (מכשירי גלי הלם, קריותרפיה וקינסיותרפיה RehaMoto).','איי גרופ היא היבואנית הרשמית והבלעדית של Longest בישראל (מכשירי גלי הלם, קריותרפיה וקינסיותרפיה RehaMoto), עם אחריות ושירות מקומיים.')
    wr('llms.txt',t,o)
    print('\n'.join(sorted(changed))); print(len(changed),'files')
if __name__=='__main__': main()

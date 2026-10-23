# -*- coding: utf-8 -*-
"""Build treatment/landing pages from the site template (nav+footer of the Ultrawave page). Run from repo root."""
import json,os,re,html as H
d=json.load(open('tools/seo/pages.json'))
def img(f):
    FB={'cryotherapy.html':'assets/img/5e8c0cd2_cryotherapy-device-LGT-2410S.webp','vet.html':'assets/img/c9042b7b_ab09e6b7c_images1.jpg','kin.html':'assets/img/59294b5d_ac13c611c_Kin.webp','shockwave-therapy.html':'assets/img/f72dc8e7_professional-shockwave-therapy-machine-4.webp','spinal-decompression.html':'assets/img/c1533d39_cd4a8a2e1_4on3aspectratio.webp','clinic-equipment.html':'assets/img/238c5257_professional-shockwave-therapy-machine-3.webp'}
    FB['product__spine-mt-core.html']='assets/img/0c492d45_70bc55ed2_2222.jpg'
    s=d.get(f,{}).get('img') or FB[f]
    if not s.startswith('assets/'):
        import glob; stem=os.path.splitext(os.path.basename(s))[0]; c=sorted(glob.glob(f'assets/img/*{stem}.*'),key=lambda x:not x.endswith('.webp')); s=c[0] if c else FB.get(f,s)
    w=re.sub(r'\.(png|jpe?g)$','.webp',s)
    return w if os.path.exists(w) else s
tpl=open('product__ultrawave-lgt-2620.html',encoding='utf-8').read()
head=tpl[:tpl.find('<section',tpl.find('</nav>'))]; foot=tpl[tpl.find('<footer'):]
T='style="color: rgb(11, 94, 215);"'
def card(f,title,text):
    return (f'<a href="{f}" class="bg-card rounded-2xl border border-border/50 p-6 block hover:shadow-lg transition-shadow">'
            f'<img loading="lazy" decoding="async" src="{img(f)}" alt="{H.escape(title)}" class="w-full aspect-[4/3] object-contain mb-4">'
            f'<h3 class="text-base font-bold mb-2" {T}>{title}</h3><p class="text-sm text-muted-foreground leading-relaxed">{text}</p></a>')
def sec(h2,body,alt=False):
    return (f'<section class="py-12{" bg-secondary/30" if alt else ""}"><div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">'
            f'<h2 class="text-2xl md:text-3xl font-bold mb-6 text-center" {T}>{h2}</h2>{body}</div></section>')
def p(*xs): return ''.join(f'<p class="text-sm md:text-base text-muted-foreground leading-relaxed mb-4 max-w-4xl mx-auto">{x}</p>' for x in xs)
def ul(*xs): return '<ul class="max-w-4xl mx-auto list-disc pr-6 space-y-2 text-sm md:text-base text-muted-foreground">'+''.join(f'<li>{x}</li>' for x in xs)+'</ul>'
def grid(*cards): return '<div class="grid md:grid-cols-3 gap-6">'+''.join(cards)+'</div>'
def hero(h1,sub,lead,im,alt):
    return (f'<section class="relative pt-24 pb-12 overflow-hidden"><div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8"><div class="grid lg:grid-cols-2 gap-8 lg:gap-12 items-center">'
            f'<div class="relative rounded-2xl overflow-hidden border border-border/50 shadow-lg" style="background-color: rgb(232, 238, 245);"><img src="{im}" alt="{alt}" class="w-full aspect-[4/3] object-contain"></div>'
            f'<div><h1 class="text-3xl md:text-4xl font-bold mb-2" {T}>{h1}</h1><p class="text-lg font-medium mb-4" {T}>{sub}</p>'
            f'<p class="text-sm md:text-base text-muted-foreground leading-relaxed mb-6">{lead}</p>'
            '<div class="flex flex-wrap gap-3"><a href="tel:0549007723" class="inline-flex items-center justify-center rounded-md text-sm font-medium bg-primary text-primary-foreground shadow hover:bg-primary/90 h-9 px-4 py-2">חייג לייעוץ: 054-900-7723</a>'
            '<a href="phone-consultation.html" class="inline-flex items-center justify-center rounded-md text-sm font-medium border border-border h-9 px-4 py-2">קביעת שיחת ייעוץ</a></div></div></div></div></section>')
U=lambda f:img(f)
PAGES={
'shockwave-therapy.html':dict(faq='shock',
 t='טיפול בגלי הלם – מכשירים, התוויות ופרוטוקולים לקליניקה | איי גרופ',
 d='מדריך לטיפול בגלי הלם לקליניקות: ממוקדים מול רדיאליים, דורבן, הסתיידות בכתף, מרפק טניס, מספר טיפולים ונגד-התוויות. מכשירי Ultrawave ו-PowerShocker.',
 name='טיפול בגלי הלם', img='product__ultrawave-lgt-2620.html',
 body=lambda:hero('טיפול בגלי הלם (ESWT)','מידע מקצועי לקליניקות ולמטפלים','טיפול בגלי הלם חוץ-גופיים (ESWT) הוא טיפול לא פולשני, שבו גלים אקוסטיים מועברים לרקמה דרך העור. בעמוד זה ריכזנו את ההבדלים בין סוגי המכשירים, ההתוויות המקובלות, מבנה סדרת טיפולים ונגד-ההתוויות – כדי לעזור לכם לבחור מכשיר גלי הלם לקליניקה.',U('product__ultrawave-lgt-2620.html'),'מכשיר גלי הלם ממוקדים Ultrawave LGT-2620 לקליניקה')
 +sec('מה זה טיפול בגלי הלם?',p('בטיפול בגלי הלם מוחדרים לרקמה פולסים אקוסטיים קצרים בעלי אנרגיה גבוהה. בספרות המקצועית מתואר שימוש בהם לטיפול בכאב שרירי-שלדי כרוני, במיוחד בגידים ובמקומות חיבור גידים לעצם. הטיפול ניתן בקליניקה, ללא הרדמה וללא זמן החלמה, ונמשך בדרך כלל דקות ספורות לאזור.'))
 +sec('גלי הלם ממוקדים מול גלי הלם רדיאליים',grid(card('product__ultrawave-lgt-2620.html','Ultrawave LGT-2620 – גלי הלם ממוקדים','מחולל אלקטרומגנטי שמרכז את האנרגיה בנקודת מוקד בעומק הרקמה – לאזורים עמוקים ולטיפול מדויק בנקודה.'),card('product__powershocker-lgt-2500s-plus.html','PowerShocker LGT-2500S PLUS – גלי הלם רדיאליים','מכשיר פנאומטי דו-ערוצי, לחץ 1–5 בר ותדר 1–22 הרץ, למבנים שטחיים יחסית: גידים, רצועות ונקודות טריגר.'),card('cryotherapy.html','קריותרפיה ממוקדת LGT-2410S','טכנולוגיה משלימה בקליניקה: קירור CO₂ מהיר ומבוקר לטיפול בנפיחות וכאב מפציעות חריפות.')),True)
 +sec('התוויות מקובלות לטיפול בגלי הלם',ul('דורבן ופאשיאיטיס פלנטרית','טנדינופתיה בגיד אכילס','הסתיידות בגידי הכתף (Calcific tendinopathy)','מרפק טניס ומרפק גולף','ברך קופץ (טנדינופתיה פטלרית)','נקודות טריגר מיופסציאליות')+p('ההחלטה על טיפול ועל הפרוטוקול נעשית על ידי איש מקצוע לאחר אבחון.'))
 +sec('איך נראית סדרת טיפולים?',p('פרוטוקולים מקובלים כוללים לרוב 3 עד 5 מפגשים במרווח של כשבוע. במהלך הטיפול המטופל חש לחץ או דקירות, והעוצמה מותאמת לסף הסבילות. שיפור, כשהוא מתרחש, מופיע בדרך כלל בהדרגה לאורך כמה שבועות.'),True)),
'spinal-decompression.html':dict(faq='spine',
 t='דקומפרסיה לעמוד השדרה – טיפול שמרני בפריצת דיסק | איי גרופ',
 d='דקומפרסיה ממוחשבת לעמוד השדרה: איך היא שונה ממתיחה, למי היא מתאימה, משך סדרת טיפולים ונגד-התוויות. מערכות Spine-MT, Spine MT Core ו-Therapy Master לקליניקות.',
 name='דקומפרסיה לעמוד השדרה', img='product__spine-mt.html',
 body=lambda:hero('דקומפרסיה לעמוד השדרה','טיפול שמרני בפריצת דיסק ובכאבי גב – מידע לקליניקות','דקומפרסיה ממוחשבת היא טיפול לא פולשני שבו מערכת ממוחשבת מפעילה כוח מתיחה מדורג ומבוקר על עמוד השדרה המותני או הצווארי. כאן תמצאו הסבר על השיטה, למי היא מתאימה, ואת מערכות הדקומפרסיה שאיי גרופ מביאה לקליניקות בישראל.',U('product__spine-mt.html'),'מכשיר דקומפרסיה לעמוד השדרה Spine-MT')
 +sec('איך עובדת דקומפרסיה ממוחשבת?',p('המטופל שוכב על מיטת הטיפול ונרתם ברתמות אגן וחזה. המחשב מפעיל כוח במחזורים של משיכה והרפיה, בזווית שנבחרת לפי המקטע המטופל, ומנטר את התנגדות הגוף לאורך הטיפול. המטרה היא להפחית את הלחץ על הדיסק ועל שורשי העצבים, בשונה ממתיחה בכוח קבוע.'))
 +sec('מערכות הדקומפרסיה שלנו',grid(card('product__spine-mt.html','Spine-MT','מערכת דקומפרסיה ממוחשבת עם שליטה דיגיטלית בזוויות ובכוחות והתאמה אישית לכל מטופל.'),card('product__spine-mt-core.html','Spine MT Core','דקומפרסיה, חימום, הנעה ותיקון מנח במכשיר שיקום רב-תכליתי אחד.'),card('product__tera-master.html','Therapy Master','מערכת תרפיה משולבת לקליניקות המחפשות פתרון בעלות משתלמת.'),card('product__robotic-bed.html','מיטה רובוטית טיפולית','תנועות טיפוליות מדויקות ועקביות על בסיס פרמטרים שהמטפל מגדיר.')),True)
 +sec('למי מתאים טיפול בדקומפרסיה?',ul('כאבי גב תחתון או צוואר מתמשכים','בלט דיסק או פריצת דיסק','כאב מקרין לרגל (סיאטיקה) או ליד','ניוון דיסק')+p('הטיפול נשקל לאחר אבחון רפואי, ולרוב לאחר הדמיה. הוא אינו מתאים לכל כאב גב, ויש נגד-התוויות ברורות – ראו בשאלות הנפוצות.'))),
'magnetotherapy.html':dict(faq='bio',
 t='מגנטותרפיה פולסטית PEMF – מכשירי Biomag לקליניקה ולבית | איי גרופ',
 d='מגנטותרפיה פולסטית (PEMF): איך היא עובדת, טכנולוגיית ה-3D של Biomag, שימוש בקליניקה, בבית ובווטרינריה, ונגד-התוויות. Biomag Lumina 3D-e מיובא על ידי איי גרופ.',
 name='מגנטותרפיה פולסטית', img='product__biomag-lumina.html',
 body=lambda:hero('מגנטותרפיה פולסטית (PEMF)','מכשירי Biomag 3D לקליניקות, לבית ולבעלי חיים','מגנטותרפיה פולסטית היא טיפול בשדה מגנטי משתנה בעוצמה נמוכה, המועבר דרך אפליקטור שמונח על הגוף. איי גרופ מייבאת לישראל את מכשירי Biomag הצ\'כיים, עם טכנולוגיית שדה תלת-ממדי רשומה כפטנט.',U('product__biomag-lumina.html'),'מכשיר מגנטותרפיה פולסטית Biomag Lumina 3D-e')
 +sec('איך עובדת מגנטותרפיה?',p('אפליקטור – משטח, גליל או אפליקטור מקומי – מונח על אזור הטיפול ומשדר שדה מגנטי פולסטי. המטופל כמעט אינו מרגיש דבר, ולכן הטיפול מתאים גם למטופלים מבוגרים או כאובים. בקליניקה אפשר להפעיל כמה ערוצים במקביל בזמן שהמטפל פנוי למטופל אחר.'))
 +sec('המכשירים',grid(card('product__biomag-lumina.html','Biomag Lumina 3D-e','4 ערוצים, מעל 200 תוכניות ופרמטרים לפי היצרן, לקליניקה ולשימוש ביתי.'),card('vet.html','Biomag וטרינריה','ערכות מגנטותרפיה לסוסים, לכלבים ולחתולים.'),card('clinic-equipment.html','כל המכשירים לקליניקות','גלי הלם, דקומפרסיה, קריותרפיה ושיקום תנועה.')),True)),
'clinic-equipment.html':dict(faq='gen',
 t='מכשור רפואי לקליניקות פיזיותרפיה, שיקום וכאב | איי גרופ',
 d='כל המכשירים של איי גרופ לקליניקות בישראל: גלי הלם, דקומפרסיה לעמוד השדרה, מגנטותרפיה, קריותרפיה, אולטרסאונד טיפולי ומאמני שיקום. ייעוץ, הדגמה והצעת מחיר.',
 name='מכשירים לקליניקות', img='product__powershocker-lgt-2500s-plus.html',
 body=lambda:hero('מכשור רפואי לקליניקות','פיזיותרפיה, אורתופדיה, רפואת ספורט ומכוני כאב','איי גרופ (I-GROUP MEDICAL TEC LTD) משווקת, מייבאת ומפיצה טכנולוגיות רפואיות מתקדמות למרפאות ולמכוני שיקום ברחבי ישראל. כאן תמצאו את כל קווי המוצרים במקום אחד.',U('product__powershocker-lgt-2500s-plus.html'),'מכשור רפואי לקליניקות – מכשיר גלי הלם PowerShocker')
 +sec('גלי הלם',grid(card('product__ultrawave-lgt-2620.html','Ultrawave LGT-2620','גלי הלם אלקטרומגנטיים ממוקדים.'),card('product__powershocker-lgt-2500s-plus.html','PowerShocker LGT-2500S PLUS','גלי הלם רדיאליים דו-ערוציים.'),card('shockwave-therapy.html','מדריך: טיפול בגלי הלם','התוויות, פרוטוקולים ובחירת מכשיר.')))
 +sec('עמוד שדרה ודקומפרסיה',grid(card('product__spine-mt.html','Spine-MT','דקומפרסיה ממוחשבת.'),card('product__spine-mt-core.html','Spine MT Core','דקומפרסיה, חימום, הנעה ותיקון.'),card('product__tera-master.html','Therapy Master','תרפיה משולבת.'),card('product__robotic-bed.html','מיטה רובוטית טיפולית','טיפול רובוטי מדויק ועקבי.'),card('spinal-decompression.html','מדריך: דקומפרסיה','איך זה עובד ולמי מתאים.')),True)
 +sec('מגנטותרפיה, קריותרפיה ושיקום',grid(card('product__biomag-lumina.html','Biomag Lumina 3D-e','מגנטותרפיה פולסטית 3D.'),card('cryotherapy.html','LGT-2410S','קריותרפיה ממוקדת CO₂.'),card('kin.html','RehaMoto','מאמני אקטיבי-פסיבי לשיקום גפיים.'),card('product__ultrasound.html','אולטרסאונד טיפולי','חימום רקמתי בפיזיותרפיה.'),card('vet.html','Biomag וטרינריה','מגנטותרפיה לבעלי חיים.')))),
}
GEN=[('מה איי גרופ עושה?','איי גרופ (I-GROUP MEDICAL TEC LTD, ח.פ. 517296117) משווקת, מייבאת ומפיצה טכנולוגיות רפואיות מתקדמות לקליניקות, למרפאות ולמכוני שיקום בישראל.'),
('למי מיועדים המכשירים?','לפיזיותרפיסטים, אורתופדים, רופאי ספורט, כירופרקטורים, מכוני כאב ומרכזי שיקום. חלק מהמכשירים, כמו Biomag, מתאימים גם לשימוש ביתי.'),
('אפשר לקבל הדגמה?','כן. ניתן לתאם שיחת ייעוץ והדגמה בטלפון 054-900-7723 או בעמוד קביעת שיחת הייעוץ.'),
('איך בוחרים מכשיר לקליניקה?','כדאי להתחיל מסוג המטופלים והמצבים הנפוצים בקליניקה, מהמקום הפנוי ומהתקציב. בשיחת ייעוץ נעזור להשוות בין המכשירים הרלוונטיים.'),
('איפה נמצאים המשרדים?','משרדי איי גרופ נמצאים ברחוב מאיר אריאל 6, נתניה. הוראות הגעה מלאות מופיעות בעמוד ההגעה.')]
if __name__=='__main__':
    for f,v in PAGES.items():
        open(f,'w',encoding='utf-8').write(head+v['body']()+foot)
        d[f]={'t':v['t'],'d':v['d'],'name':v['name'],'img':d[v['img']]['img'],'og':'og/'+f[:-5]+'.jpg','faq':v['faq']}
    json.dump(d,open('tools/seo/pages.json','w'),ensure_ascii=False,indent=1)
    print('built',list(PAGES))

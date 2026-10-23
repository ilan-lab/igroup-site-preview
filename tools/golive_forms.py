"""Wire every lead form to FormSubmit.co (ilan@i-group.co.il) + WhatsApp fallback. Idempotent."""
import re,glob
from bs4 import BeautifulSoup
EP='https://formsubmit.co/ilan@i-group.co.il'
SITE='https://i-group.co.il'
WA='https://wa.me/972549007723'
def hidden(soup,form,subject,nxt):
    for k,v in [('_subject',subject),('_next',SITE+nxt),('_template','table'),('_language','he')]:
        t=soup.new_tag('input',type='hidden',attrs={'name':k,'value':v}); form.insert(0,t)
    hp=soup.new_tag('input',type='text',attrs={'name':'_honey','style':'display:none','tabindex':'-1','autocomplete':'off'}); form.insert(0,hp)
def wa_note(soup,text):
    p=soup.new_tag('p',attrs={'class':'text-xs text-center mt-2','style':'opacity:.8','data-wa-fallback':''})
    p.append('מעדיפים וואטסאפ? ')
    a=soup.new_tag('a',href=WA+'?text='+text,target='_blank',rel='noopener noreferrer',style='text-decoration:underline'); a.string='שלחו לנו הודעה ב-WhatsApp: 054-900-7723'
    p.append(a); return p
def process(f):
    h=open(f,encoding='utf-8').read(); o=h
    h=h.replace("document.querySelectorAll('form').forEach(function(f){f.addEventListener('submit',function(e){e.preventDefault();alert('טופס הדגמה בלבד (קלון סטטי)');});});","")
    for m in list(re.finditer(r'<form\b.*?</form>',h,re.S)):
        src=m.group(0)
        if 'formsubmit.co' in src: continue
        soup=BeautifulSoup(src,'html.parser'); form=soup.form
        form['action']=EP; form['method']='POST'; form['accept-charset']='UTF-8'
        for el in form.find_all(['input','textarea']):
            if not el.get('name'):
                el['name']=el.get('id') or {'email':'email','tel':'phone','text':'name'}.get(el.get('type','text'),'field')
        txt=form.get_text()
        if 'הרשמה' in txt and 'message' not in src:
            hidden(soup,form,'הרשמה לניוזלטר – אתר איי גרופ','/thank-you/newsletter'); note='הרשמה לניוזלטר'
        elif 'מועד מועדף' in txt:
            hidden(soup,form,'בקשת שיחת ייעוץ טלפונית – אתר איי גרופ','/thank-you/consultation'); note='אשמח לתאם שיחת ייעוץ'
            lab=[l for l in form.find_all('label') if 'מועד מועדף' in l.get_text()][0]
            cal=lab.find_next_sibling('div')
            new=BeautifulSoup('<div class="grid grid-cols-2 gap-3"><input type="date" name="preferred_date" required class="flex w-full rounded-md border border-input bg-transparent px-3 py-1 text-base shadow-sm h-11"><select name="preferred_time" class="flex w-full rounded-md border border-input bg-transparent px-3 py-1 text-base shadow-sm h-11"><option value="בוקר (09:00-12:00)">בוקר (09:00-12:00)</option><option value="צהריים (12:00-15:00)">צהריים (12:00-15:00)</option><option value="אחה&quot;צ (15:00-18:00)">אחה"צ (15:00-18:00)</option></select></div>','html.parser')
            cal.replace_with(new)
            for b in form.find_all('button',type='button'):
                v=b.get_text(strip=True); lbl=soup.new_tag('label',attrs={'class':b.get('class') and ' '.join(b['class']) or '','style':'cursor:pointer;display:inline-flex;gap:6px;align-items:center'})
                cb=soup.new_tag('input',type='checkbox',attrs={'name':'interests[]','value':v}); lbl.append(cb); lbl.append(v); b.replace_with(lbl)
            sb=form.find('button',type='submit')
            if sb.has_attr('disabled'): del sb['disabled']
            for s in sb.find_all(string=True):
                if 'קוד אימות' in s: s.replace_with('שלח בקשה')
        else:
            hidden(soup,form,'פנייה חדשה מאתר איי גרופ','/thank-you/contact'); note='פנייה מהאתר'
            for i in ('name','phone'):
                el=form.find(id=i)
                if el: el['required']=''
        form.append(wa_note(soup,note))
        h=h.replace(src,str(soup),1)
    if h!=o: open(f,'w',encoding='utf-8').write(h); print('updated',f)
for f in sorted(glob.glob('*.html')): process(f)

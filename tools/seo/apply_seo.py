"""Inject SEO/OG/Twitter/JSON-LD into every page. Run from repo root: python3 tools/seo/apply_seo.py
Single switch: set INDEXABLE=True (or env INDEXABLE=1) when going live to drop noindex."""
import json,re,os,html
INDEXABLE=os.environ.get('INDEXABLE')=='1' or False
SITE='https://i-group.co.il'
IMAGE_BASE=os.environ.get('IMAGE_BASE','https://ilan-lab.github.io/igroup-site-preview')  # where /og/ is hosted
PHONE_DISPLAY='054-900-7723'; PHONE_INTL='+972-54-900-7723'
d=json.load(open('tools/seo/pages.json'))
e=lambda s:html.escape(s,quote=True)
for f,v in d.items():
    h=open(f,encoding='utf-8').read()
    h=re.sub(r'<!-- seo:start -->.*?<!-- seo:end -->\n?','',h,flags=re.S)
    h=re.sub(r'<title>.*?</title>','',h,flags=re.S)
    h=re.sub(r'<meta\b[^>]*\b(?:name|property)="(?:description|robots|og:[^"]+|twitter:[^"]+)"[^>]*>\n?','',h)
    h=re.sub(r'<link\b[^>]*\brel="canonical"[^>]*>\n?','',h)
    h=h.replace('Biomog','Biomag').replace('054-502-0506',PHONE_DISPLAY).replace('0545020506','0549007723')
    route='/' if f=='index.html' else '/'+f[:-5].replace('__','/')
    url=SITE+route; img=IMAGE_BASE+'/'+v['og']; prod=v.get('p')
    alt=(v.get('name') or 'I-Group Medical Tech')+' – איי גרופ'
    robots='index,follow' if INDEXABLE and not v.get('nf') and f!='consultations.html' else 'noindex,nofollow'
    m=[f'<title>{e(v["t"])}</title>',f'<meta name="description" content="{e(v["d"])}">',
       f'<link rel="canonical" href="{url}">',f'<meta name="robots" content="{robots}">',
       f'<meta property="og:type" content="{"product" if prod else "website"}">',
       f'<meta property="og:title" content="{e(v["t"])}">',f'<meta property="og:description" content="{e(v["d"])}">',
       f'<meta property="og:url" content="{url}">','<meta property="og:site_name" content="I-Group Medical Tech">',
       '<meta property="og:locale" content="he_IL">',f'<meta property="og:image" content="{img}">',
       '<meta property="og:image:width" content="1200">','<meta property="og:image:height" content="630">',
       f'<meta property="og:image:alt" content="{e(alt)}">','<meta name="twitter:card" content="summary_large_image">',
       f'<meta name="twitter:title" content="{e(v["t"])}">',f'<meta name="twitter:description" content="{e(v["d"])}">',
       f'<meta name="twitter:image" content="{img}">']
    if prod:
        ld={"@context":"https://schema.org","@type":"Product","name":v['name'],"description":v['d'],"image":img,"url":url,
            "brand":{"@type":"Brand","name":v['name'].split()[0]},
            "offers":{"@type":"Offer","url":url,"availability":"https://schema.org/InStock","priceCurrency":"ILS",
                      "seller":{"@type":"Organization","name":"I-Group Medical Tech","telephone":PHONE_INTL,"url":SITE}}}
        m.append('<script type="application/ld+json">'+json.dumps(ld,ensure_ascii=False)+'</script>')
    h=h.replace('</head>','<!-- seo:start -->\n'+'\n'.join(m)+'\n<!-- seo:end -->\n</head>',1)
    open(f,'w',encoding='utf-8').write(h)
print('done; INDEXABLE =',INDEXABLE)

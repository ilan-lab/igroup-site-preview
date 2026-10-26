/* improve.js — tiny a11y helpers: skip link, main landmark id, accessible names for icon-only controls. */
(function () {
  var root = document.getElementById('root');
  if (root && !document.getElementById('main-content')) {
    var target = root.querySelector('section') || root.firstElementChild;
    if (target) { target.id = target.id || 'main-content'; target.setAttribute('tabindex', '-1'); }
  }
  var skip = document.createElement('a');
  skip.className = 'imp-skip';
  skip.href = '#' + ((root && root.querySelector('section') && root.querySelector('section').id) || 'main-content');
  skip.textContent = 'דלג לתוכן הראשי';
  document.body.insertBefore(skip, document.body.firstChild);

  document.querySelectorAll('button').forEach(function (b) {
    if (!b.textContent.trim() && !b.getAttribute('aria-label') && b.querySelector('svg')) {
      if (b.closest('nav') && /md:hidden/.test(b.className)) b.setAttribute('aria-label', 'תפריט');
    }
  });
  document.querySelectorAll('a[target="_blank"]').forEach(function (a) {
    if (!/noopener/.test(a.rel)) a.rel = (a.rel + ' noopener noreferrer').trim();
  });
})();

/* Language switcher (he/en/ru/ar) — the static snapshot lost the React i18n, so the flag button was dead.
   Restores the same flag dropdown and translates the page with Google Website Translator (cookie googtrans). */
(function () {
  var FLAGS = { he: '🇮🇱', en: '🇬🇧', ru: '🇷🇺', ar: '🇸🇦' };
  var NAMES = { he: 'עברית', en: 'English', ru: 'Русский', ar: 'العربية' };
  function getLang() {
    var m = document.cookie.match(/(?:^|;\s*)googtrans=\/[a-z]+\/([a-zA-Z-]+)/);
    return m && FLAGS[m[1]] ? m[1] : 'he';
  }
  function setCookie(v, del) {
    var exp = del ? '; expires=Thu, 01 Jan 1970 00:00:00 GMT' : '; max-age=31536000';
    var host = location.hostname, parts = host.split('.');
    document.cookie = 'googtrans=' + v + '; path=/' + exp;
    for (var i = 0; i < parts.length - 1; i++) {
      document.cookie = 'googtrans=' + v + '; path=/; domain=.' + parts.slice(i).join('.') + exp;
    }
  }
  function choose(code) {
    if (code === getLang()) return;
    if (code === 'he') setCookie('', true); else setCookie('/he/' + code);
    location.reload();
  }
  var lang = getLang();
  var html = document.documentElement;
  if (lang !== 'he') {
    var w = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT), n, hits = [];
    while ((n = w.nextNode())) if (/איי גרופ/.test(n.nodeValue)) hits.push(n);
    hits.forEach(function (n) {
      var parts = n.nodeValue.split('איי גרופ'), frag = document.createDocumentFragment();
      parts.forEach(function (t, k) {
        if (k) { var sp = document.createElement('span'); sp.className = 'notranslate'; sp.textContent = 'I-Group'; frag.appendChild(sp); }
        if (t) frag.appendChild(document.createTextNode(t));
      });
      n.parentNode.replaceChild(frag, n);
    });
    html.setAttribute('dir', lang === 'ar' ? 'rtl' : 'ltr');
    var c = document.createElement('div'); c.id = 'google_translate_element'; c.style.display = 'none';
    document.body.appendChild(c);
    window.googleTranslateElementInit = function () {
      new google.translate.TranslateElement({ pageLanguage: 'he', includedLanguages: 'en,ru,ar', autoDisplay: false }, 'google_translate_element');
      var tries = 0, t = setInterval(function () {
        var sel = document.querySelector('select.goog-te-combo');
        if (sel && sel.options.length > 1) {
          if (sel.value !== lang) { sel.value = lang; sel.dispatchEvent(new Event('change')); }
          clearInterval(t);
        } else if (++tries > 100) clearInterval(t);
      }, 100);
    };
    var s = document.createElement('script');
    s.src = 'https://translate.google.com/translate_a/element.js?cb=googleTranslateElementInit';
    document.body.appendChild(s);
  }
  document.querySelectorAll('button[title="he"],button[data-lang-switch]').forEach(function (btn) {
    btn.setAttribute('data-lang-switch', '');
    btn.setAttribute('title', NAMES[lang]);
    btn.setAttribute('aria-label', 'שפה / Language: ' + NAMES[lang]);
    btn.setAttribute('aria-haspopup', 'true');
    btn.setAttribute('aria-expanded', 'false');
    btn.classList.add('notranslate');
    btn.textContent = FLAGS[lang];
    var wrap = btn.parentElement;
    var menu = document.createElement('div');
    menu.className = 'imp-lang-menu notranslate';
    menu.setAttribute('role', 'menu');
    menu.hidden = true;
    Object.keys(FLAGS).forEach(function (code) {
      if (code === lang) return;
      var b = document.createElement('button');
      b.type = 'button'; b.setAttribute('role', 'menuitem'); b.title = NAMES[code];
      b.setAttribute('aria-label', NAMES[code]); b.setAttribute('data-lang', code);
      b.textContent = FLAGS[code];
      b.addEventListener('click', function () { choose(code); });
      menu.appendChild(b);
    });
    wrap.appendChild(menu);
    btn.addEventListener('click', function (e) {
      e.stopPropagation(); menu.hidden = !menu.hidden; btn.setAttribute('aria-expanded', String(!menu.hidden));
    });
    document.addEventListener('mousedown', function (e) { if (!wrap.contains(e.target)) { menu.hidden = true; btn.setAttribute('aria-expanded', 'false'); } });
  });
})();

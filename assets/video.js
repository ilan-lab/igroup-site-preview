/* video.js — cinematic "theater" player, matching the Base44 site's video presentation
   (dark blurred backdrop, large rounded 16:9 frame, soft scale-in, title under the video).
   Handles YouTube, Google Drive previews and direct MP4; vertical clips via data-video-aspect. */
(function () {
  var css = '' +
    '.ig-vp{position:fixed;inset:0;z-index:99999;display:flex;flex-direction:column;align-items:center;justify-content:center;' +
    'padding:max(56px,env(safe-area-inset-top)) 16px max(24px,env(safe-area-inset-bottom));background:rgba(3,10,24,.92);' +
    '-webkit-backdrop-filter:blur(10px);backdrop-filter:blur(10px);opacity:0;transition:opacity .28s ease}' +
    '.ig-vp.ig-in{opacity:1}' +
    '.ig-vp-frame{position:relative;background:#000;border-radius:16px;overflow:hidden;' +
    'box-shadow:0 30px 80px rgba(0,0,0,.6),0 0 0 1px rgba(255,255,255,.06);transform:scale(.94) translateY(12px);' +
    'transition:transform .38s cubic-bezier(.2,.8,.2,1)}' +
    '.ig-vp.ig-in .ig-vp-frame{transform:none}' +
    '.ig-vp-frame iframe,.ig-vp-frame video{position:absolute;inset:0;width:100%;height:100%;border:0;display:block;background:#000}' +
    '.ig-vp-title{color:#fff;font-weight:700;font-size:18px;margin-top:16px;text-align:center;max-width:min(900px,92vw);' +
    'line-height:1.4;opacity:.92;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}' +
    '.ig-vp-close{position:absolute;top:max(12px,env(safe-area-inset-top));right:16px;width:44px;height:44px;border-radius:50%;' +
    'border:0;background:rgba(255,255,255,.12);color:#fff;font-size:28px;line-height:44px;cursor:pointer;transition:background .2s}' +
    '.ig-vp-close:hover,.ig-vp-close:focus-visible{background:rgba(255,255,255,.25);outline:none}' +
    '.ig-vp-spin{position:absolute;inset:0;margin:auto;width:42px;height:42px;border:3px solid rgba(255,255,255,.2);' +
    'border-top-color:#fff;border-radius:50%;animation:igspin .8s linear infinite}@keyframes igspin{to{transform:rotate(360deg)}}' +
    'html.ig-vp-lock,html.ig-vp-lock body{overflow:hidden}' +
    '@media (max-width:640px){.ig-vp{padding-left:0;padding-right:0}.ig-vp-frame{border-radius:0}.ig-vp-frame.ig-vert{border-radius:12px}.ig-vp-title{font-size:15px;padding:0 16px}}' +
    '@media (prefers-reduced-motion:reduce){.ig-vp,.ig-vp-frame{transition:none}}';
  var st = document.createElement('style'); st.textContent = css; document.head.appendChild(st);

  function source(u) {
    var m = u.match(/(?:youtube(?:-nocookie)?\.com\/(?:embed\/|watch\?v=|shorts\/)|youtu\.be\/)([\w-]{11})/);
    if (m) return { kind: 'iframe', src: 'https://www.youtube-nocookie.com/embed/' + m[1] + '?autoplay=1&rel=0&modestbranding=1&playsinline=1', vert: /shorts\//.test(u) };
    var d = u.match(/drive\.google\.com\/file\/d\/([^/?#]+)/);
    if (d) return { kind: 'iframe', src: 'https://drive.google.com/file/d/' + d[1] + '/preview?autoplay=1' };
    if (/\.(mp4|webm|mov|m4v)(\?|#|$)/i.test(u)) return { kind: 'video', src: u };
    return { kind: 'iframe', src: u };
  }
  function ratio(a) { var p = String(a || '16/9').split('/'); var r = (+p[0]) / (+p[1]); return r > 0 ? r : 16 / 9; }

  /* ---- video card grids: exactly 1 per row, large, centered (max 900px) ---- */
  var gcss = '.ig-vgrid{display:grid!important;grid-template-columns:1fr!important;gap:32px!important;max-width:900px;margin-inline:auto}' +
    '@media (max-width:640px){.ig-vgrid{gap:20px!important}}' +
    '.ig-vgrid>*{min-width:0}.ig-vgrid [data-video-src]{display:flex;flex-direction:column;width:100%}' +
    '.ig-vgrid .ig-vthumb,.ig-vgrid [data-video-src].aspect-video{position:relative;aspect-ratio:16/9!important;overflow:hidden;background:#0b1624!important}' +
    '.ig-vgrid [data-video-src].aspect-video>img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}.ig-vthumb>img{position:relative;z-index:1;width:100%;height:100%;object-fit:cover}' +
    '.ig-vgrid .ig-vthumb.ig-vert{aspect-ratio:auto!important;height:min(80vh,calc(min(900px,100vw - 32px) * 16 / 9))}' +
    '.ig-vthumb.ig-vert>img,.ig-vthumb.ig-sq>img{object-fit:contain}' +
    '.ig-vthumb.ig-vert::before,.ig-vthumb.ig-sq::before{content:"";position:absolute;inset:-20px;background:var(--ig-bg) center/cover;filter:blur(18px) brightness(.55);transform:scale(1.1)}' +
    '.ig-vthumb>div{z-index:2}.ig-vgrid [data-video-src] p{font-size:16px}' +
    '.ig-vgrid .w-14.h-14{width:72px;height:72px;opacity:.95!important}';
  var gs = document.createElement('style'); gs.textContent = gcss; document.head.appendChild(gs);
  function grids() {
    document.querySelectorAll('[data-video-src]').forEach(function (b) {
      var g = b.closest('.grid'); if (g) g.classList.add('ig-vgrid');
      var img = b.querySelector('img'), th = img && img.parentElement;
      if (th && th !== b) {
        th.classList.add('ig-vthumb');
        var rr = ratio(b.getAttribute('data-video-aspect')); if (rr < 1.3) { th.classList.add(rr < 1 ? 'ig-vert' : 'ig-sq'); th.style.setProperty('--ig-bg', 'url("' + img.getAttribute('src') + '")'); }
      }
    });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', grids); else grids();

  var cur = null;
  function open(btn) {
    if (cur) cur.close();
    var u = btn.getAttribute('data-video-src'), s = source(u);
    var r = s.vert ? 9 / 16 : ratio(btn.getAttribute('data-video-aspect'));
    var card = btn.closest('.rounded-2xl,.rounded-xl') || btn;
    var tEl = card.querySelector('p,h3,h4');
    var title = btn.getAttribute('data-video-title') || (tEl && tEl.textContent.trim()) || '';
    var o = document.createElement('div');
    o.className = 'ig-vp'; o.setAttribute('role', 'dialog'); o.setAttribute('aria-modal', 'true');
    o.setAttribute('aria-label', title || 'סרטון');
    var f = document.createElement('div'); f.className = 'ig-vp-frame' + (r < 1 ? ' ig-vert' : '');
    function size() {
      var mob = innerWidth <= 640, maxW = mob ? innerWidth : Math.min(innerWidth - 32, 1280);
      var maxH = innerHeight - (title ? 140 : 100);
      var w = Math.min(maxW, maxH * r); if (r < 1 && mob) w = Math.min(w, innerWidth - 32);
      f.style.width = Math.round(w) + 'px'; f.style.height = Math.round(w / r) + 'px';
    }
    size();
    f.innerHTML = '<div class="ig-vp-spin"></div>';
    var m;
    if (s.kind === 'video') {
      m = document.createElement('video'); m.src = s.src; m.controls = true; m.autoplay = true; m.playsInline = true;
      m.setAttribute('playsinline', ''); m.preload = 'auto';
      m.addEventListener('loadedmetadata', function () { if (m.videoWidth && m.videoHeight) { r = m.videoWidth / m.videoHeight; f.classList.toggle('ig-vert', r < 1); size(); } });
    } else {
      m = document.createElement('iframe'); m.src = s.src; m.title = title || 'סרטון';
      m.allow = 'autoplay; encrypted-media; picture-in-picture; fullscreen; accelerometer; gyroscope';
      m.setAttribute('allowfullscreen', ''); m.referrerPolicy = 'strict-origin-when-cross-origin';
    }
    m.addEventListener(s.kind === 'video' ? 'loadeddata' : 'load', function () { var sp = f.querySelector('.ig-vp-spin'); if (sp) sp.remove(); });
    f.appendChild(m);
    var c = document.createElement('button'); c.type = 'button'; c.className = 'ig-vp-close'; c.setAttribute('aria-label', 'סגור'); c.innerHTML = '&times;';
    o.appendChild(c); o.appendChild(f);
    if (title) { var t = document.createElement('div'); t.className = 'ig-vp-title'; t.textContent = title; o.appendChild(t); }
    function close() {
      document.removeEventListener('keydown', key); removeEventListener('resize', size);
      o.classList.remove('ig-in'); document.documentElement.classList.remove('ig-vp-lock');
      setTimeout(function () { o.remove(); }, 280); cur = null; try { btn.focus({ preventScroll: true }); } catch (e) {}
    }
    function key(e) { if (e.key === 'Escape') close(); else if (e.key === 'Tab') { e.preventDefault(); c.focus(); } }
    o.addEventListener('click', function (e) { if (!f.contains(e.target)) close(); });
    document.addEventListener('keydown', key); addEventListener('resize', size);
    document.documentElement.classList.add('ig-vp-lock');
    document.body.appendChild(o);
    requestAnimationFrame(function () { requestAnimationFrame(function () { o.classList.add('ig-in'); }); });
    c.focus({ preventScroll: true });
    cur = { close: close };
  }
  document.addEventListener('click', function (e) {
    var b = e.target.closest('[data-video-src]');
    if (b) { e.preventDefault(); open(b); }
  });
})();

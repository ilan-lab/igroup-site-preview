/* video.js — restores the video lightbox that Base44's React app provided (stripped in the static clone). */
(function () {
  function embed(u) {
    var m = u.match(/(?:youtube\.com\/(?:embed\/|watch\?v=)|youtu\.be\/)([\w-]{11})/);
    if (m) return 'https://www.youtube-nocookie.com/embed/' + m[1] + '?autoplay=1&rel=0&playsinline=1';
    return u;
  }
  function open(u) {
    var o = document.createElement('div');
    o.setAttribute('role', 'dialog'); o.setAttribute('aria-modal', 'true');
    o.style.cssText = 'position:fixed;inset:0;z-index:99999;background:rgba(0,0,0,.85);display:flex;align-items:center;justify-content:center;padding:16px';
    o.innerHTML = '<div style="position:relative;width:min(960px,100%);aspect-ratio:16/9">' +
      '<button type="button" aria-label="סגור" style="position:absolute;top:-44px;left:0;font-size:32px;color:#fff;background:none;border:0;cursor:pointer">&times;</button>' +
      '<iframe src="' + embed(u) + '" style="width:100%;height:100%;border:0;border-radius:12px;background:#000" allow="autoplay; encrypted-media; picture-in-picture; fullscreen" allowfullscreen referrerpolicy="strict-origin-when-cross-origin"></iframe></div>';
    function close() { o.remove(); document.removeEventListener('keydown', esc); }
    function esc(e) { if (e.key === 'Escape') close(); }
    o.addEventListener('click', function (e) { if (e.target === o || e.target.closest('button')) close(); });
    document.addEventListener('keydown', esc);
    document.body.appendChild(o);
    o.querySelector('button').focus();
  }
  document.addEventListener('click', function (e) {
    var b = e.target.closest('[data-video-src]');
    if (b) { e.preventDefault(); open(b.getAttribute('data-video-src')); }
  });
})();

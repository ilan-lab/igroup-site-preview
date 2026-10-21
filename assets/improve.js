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

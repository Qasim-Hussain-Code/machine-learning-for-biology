// Light and dark toggle. The choice is remembered for the whole book.
// On a phone the contents list starts closed, so the chapter is the first thing on the screen.
(function () {
  var r = document.documentElement, k = 'mlb-theme';
  function label() {
    var next = r.dataset.theme === 'dark' ? 'light' : 'dark';
    document.querySelectorAll('.modebtn').forEach(function (b) {
      b.innerHTML = (next === 'light' ? 'Light' : 'Dark') + '<span class="wide"> mode</span>';
      b.setAttribute('aria-label', 'Switch to ' + next + ' mode');
    });
  }
  label();
  document.addEventListener('click', function (e) {
    var b = e.target.closest('.modebtn');
    if (!b) return;
    r.dataset.theme = r.dataset.theme === 'dark' ? 'light' : 'dark';
    try { localStorage.setItem(k, r.dataset.theme); } catch (x) {}
    label();
  });
  var d = document.querySelector('.tocd');
  if (d) {
    var phone = window.matchMedia('(max-width: 820px)');
    var fit = function () { if (phone.matches) d.removeAttribute('open'); else d.setAttribute('open', ''); };
    fit();
    if (phone.addEventListener) phone.addEventListener('change', fit);
    // on a wide screen the list is always open, so its heading is not a control
    d.querySelector('summary').addEventListener('click', function (e) { if (!phone.matches) e.preventDefault(); });
  }
})();

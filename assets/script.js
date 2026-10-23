const toggle = document.querySelector('.mobile-toggle');
const nav = document.querySelector('.nav');
const chinese = document.documentElement.lang.startsWith('zh');
const labels = chinese
  ? { open: '打开导航', close: '关闭导航' }
  : { open: 'Open navigation', close: 'Close navigation' };

function setNavigation(open) {
  nav.classList.toggle('open', open);
  toggle.setAttribute('aria-expanded', String(open));
  toggle.setAttribute('aria-label', open ? labels.close : labels.open);
}

if (toggle && nav) {
  toggle.addEventListener('click', () => setNavigation(!nav.classList.contains('open')));
  nav.querySelectorAll('a').forEach(link => {
    link.addEventListener('click', () => setNavigation(false));
  });
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape' && nav.classList.contains('open')) {
      setNavigation(false);
      toggle.focus();
    }
  });
}

// Keep the same section when switching languages; plain links also work without JS.
const languageSwitch = document.querySelector('.language-switch');
if (languageSwitch) {
  const destination = new URL(languageSwitch.getAttribute('href'), window.location.href);
  function updateLanguageLink() {
    destination.hash = window.location.hash;
    languageSwitch.href = destination.href;
  }
  updateLanguageLink();
  window.addEventListener('hashchange', updateLanguageLink);
}

document.querySelectorAll('[data-year]').forEach(element => {
  element.textContent = new Date().getFullYear();
});

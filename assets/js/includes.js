// includes.js — loads header and footer partials

async function loadPartial(id, url) {
  try {
    const res = await fetch(url);
    if (!res.ok) return;
    const html = await res.text();
    const el = document.getElementById(id);
    if (el) el.outerHTML = html;
  } catch(e) {}
}

document.addEventListener('DOMContentLoaded', () => {
  loadPartial('header-placeholder', '/_header.html').then(() => {
    // Mobile nav toggle
    const toggle = document.querySelector('.nav-toggle');
    const links  = document.querySelector('.nav-links');
    if (toggle && links) {
      toggle.addEventListener('click', () => links.classList.toggle('open'));
    }
    // Active nav link
    const current = window.location.pathname;
    document.querySelectorAll('.nav-links a').forEach(a => {
      if (a.getAttribute('href') === current) a.classList.add('active');
    });
  });
  loadPartial('footer-placeholder', '/_footer.html');
});

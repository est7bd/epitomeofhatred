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

/* ── EASTER EGG — type "corrupt" ── */
(function () {
  const TARGET = 'corrupt';
  let buffer = '';
  document.addEventListener('keydown', (e) => {
    if (['INPUT','TEXTAREA','SELECT'].includes(document.activeElement.tagName)) return;
    if (e.key.length !== 1) return;
    buffer = (buffer + e.key.toLowerCase()).slice(-TARGET.length);
    if (buffer === TARGET) { buffer = ''; triggerCorrupt(); }
  });
  function triggerCorrupt() {
    const o = document.createElement('div');
    o.style.cssText = 'position:fixed;inset:0;z-index:99999;background:#0a0a0a;display:flex;flex-direction:column;align-items:center;justify-content:center;cursor:pointer;animation:cFade 0.4s ease both;';
    o.innerHTML = `
      <style>
        @keyframes cFade{from{opacity:0;transform:translateY(10px)}to{opacity:1;transform:translateY(0)}}
        @keyframes cBlink{0%,100%{opacity:1}50%{opacity:0.2}}
        .c-label{font-family:var(--font-mono,'JetBrains Mono',monospace);font-size:0.65rem;letter-spacing:0.3em;text-transform:uppercase;color:#cc2222;animation:cBlink 1.5s ease infinite;margin-bottom:1.5rem;}
        .c-title{font-family:var(--font-display,'Bebas Neue',sans-serif);font-size:clamp(4rem,14vw,10rem);color:#f0f0f0;line-height:0.88;text-align:center;letter-spacing:0.02em;}
        .c-title span{color:#cc2222;}
        .c-sub{font-family:var(--font-mono,'JetBrains Mono',monospace);font-size:0.7rem;letter-spacing:0.15em;color:rgba(204,34,34,0.4);margin-top:1rem;text-transform:uppercase;}
        .c-msg{font-family:var(--font-body,'Crimson Pro',Georgia,serif);font-size:1.05rem;color:rgba(220,200,200,0.5);margin-top:1.5rem;text-align:center;max-width:420px;line-height:1.75;font-style:italic;}
        .c-dismiss{font-family:var(--font-mono,'JetBrains Mono',monospace);margin-top:2.5rem;font-size:0.58rem;color:rgba(204,34,34,0.2);letter-spacing:0.2em;text-transform:uppercase;}
      </style>
      <div class="c-label">▸ Epitome of Hatred</div>
      <div class="c-title">No<br><span>Filter.</span></div>
      <div class="c-sub">No Apologies. Never.</div>
      <p class="c-msg">You typed "corrupt." Bold of you to name it.<br>This site has been doing exactly that since day one.</p>
      <div class="c-dismiss">click or esc to close</div>
    `;
    document.body.appendChild(o);
    document.body.style.overflow = 'hidden';
    const close = () => { o.remove(); document.body.style.overflow = ''; };
    o.addEventListener('click', close);
    document.addEventListener('keydown', function esc(e) {
      if (e.key === 'Escape') { close(); document.removeEventListener('keydown', esc); }
    });
  }
})();

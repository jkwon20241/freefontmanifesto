(() => {
  /* ---------- glyph fields: scroll-linked ink wave + tap to press ---------- */
  const BAND = 0.3; // share of the field (top→bottom) inked at once
  const fields = [...document.querySelectorAll('svg.field')].map(svg => {
    const H = svg.viewBox.baseVal.height;
    const items = [...svg.querySelectorAll('.g, .a')].map((el, i) => {
      const b = el.getBBox();
      return { el, isA: el.classList.contains('a'), yn: (b.y + b.height / 2) / H, i };
    });
    return { svg, items, mode: svg.classList.contains('cover') ? 'cover' : 'end' };
  });

  function progress(f) {
    const r = f.svg.getBoundingClientRect(), vh = innerHeight;
    if (!r.height) return null; // hidden at this breakpoint
    if (f.mode === 'cover') {
      // 0 at the top of the page, 1 once the cover has scrolled away
      return Math.max(0, Math.min(1, -r.top / (r.height * 0.85)));
    }
    // back cover: 0 when it enters the screen, 1 at the very bottom of the page
    const maxScroll = document.documentElement.scrollHeight - vh;
    const topAtEnd = r.top + (scrollY - maxScroll); // its top when fully scrolled
    const span = vh - topAtEnd;
    if (span <= 0) return 1;
    return Math.max(0, Math.min(1, (vh - r.top) / span));
  }

  function paint() {
    for (const f of fields) {
      const p = progress(f);
      if (p === null) continue;
      const q = f.mode === 'cover' ? p * (1 + BAND) : p; // the cover's wave passes fully; the back cover ends inked
      for (const it of f.items) {
        const on = it.yn <= q && it.yn > q - BAND;
        if (it.isA) {
          it.el.style.setProperty('--r', `${Math.round(p * 360 + it.i * 15 + (it.el._spin || 0))}deg`);
        } else {
          it.el.classList.toggle('on', on);
        }
      }
    }
  }
  let ticking = false;
  const onScroll = () => { if (!ticking) { ticking = true; requestAnimationFrame(() => { ticking = false; paint(); updateNav(); }); } };
  addEventListener('scroll', onScroll, { passive: true });
  addEventListener('resize', onScroll);

  for (const f of fields) {
    f.svg.addEventListener('click', e => {
      const t = e.target.closest('.g, .a');
      if (!t) return;
      if (t.classList.contains('a')) { t._spin = (t._spin || 0) + 90; paint(); }
      else t.classList.toggle('pressed');
    });
  }

  /* ---------- contents: current section + reading progress ---------- */
  const ids = ['intro', 'q1', 'specimens', 'q2', 'q3', 'q4', 'conclusion', 'colophon'];
  const sections = ids.map(id => document.getElementById(id));
  const links = [...document.querySelectorAll('.contents a')];
  const dots = [...document.querySelectorAll('.progress .dots span')];
  const questionOrder = ['q1', 'q2', 'q3', 'q4'];
  function updateNav() {
    let current = null;
    for (const s of sections) if (s.getBoundingClientRect().top <= innerHeight * 0.35) current = s.id;
    links.forEach(a => a.setAttribute('aria-current', a.hash === '#' + current ? 'true' : 'false'));
    const reached = questionOrder.filter(id => document.getElementById(id).getBoundingClientRect().top <= innerHeight * 0.35).length;
    dots.forEach((d, i) => d.classList.toggle('on', i < reached));
  }

  /* ---------- mobile index menu ---------- */
  const menu = document.getElementById('index-menu');
  const openBtn = document.querySelector('.index-btn');
  const closeBtn = menu.querySelector('.close-btn');
  const open = () => { menu.hidden = false; openBtn.setAttribute('aria-expanded', 'true'); document.body.style.overflow = 'hidden'; closeBtn.focus(); };
  const close = (focusBtn = true) => { menu.hidden = true; openBtn.setAttribute('aria-expanded', 'false'); document.body.style.overflow = ''; if (focusBtn) openBtn.focus(); };
  openBtn.addEventListener('click', open);
  closeBtn.addEventListener('click', () => close());
  menu.addEventListener('click', e => { if (e.target.closest('a')) close(false); });
  addEventListener('keydown', e => { if (e.key === 'Escape' && !menu.hidden) close(); });

  paint(); updateNav();
})();

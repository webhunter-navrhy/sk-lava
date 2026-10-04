(() => {
  const $ = (s, c = document) => c.querySelector(s), $$ = (s, c = document) => [...c.querySelectorAll(s)];
  const calm = matchMedia('(prefers-reduced-motion: reduce)').matches;

  // hero – slová postupne
  const h1 = $('[data-words]');
  if (h1) {
    let i = 0;
    const wrap = node => [...node.childNodes].forEach(n => {
      if (n.nodeType === 3) {
        const frag = document.createDocumentFragment();
        n.textContent.split(/([ \t\n]+)/).forEach(t => {
          if (!t) return;
          if (/^[ \t\n]+$/.test(t)) { frag.append(' '); return; }
          const w = document.createElement('span'); w.className = 'w';
          const s = document.createElement('span'); s.textContent = t; s.style.animationDelay = (0.25 + i++ * 0.08) + 's';
          w.append(s); frag.append(w);
        });
        n.replaceWith(frag);
      } else if (n.nodeType === 1 && n.tagName !== 'BR') wrap(n);
    });
    wrap(h1);
  }

  // hero – pás zámkovej dlažby sa „pokladá“ zľava doprava (farby ako ich šachovnica)
  const pv = $('#pavers');
  if (pv) {
    const C = ['#c8141b', '#a3161a', '#2a292c', '#2a292c', '#333135', '#333135', '#3d3b3f', '#4a4744', '#8d877d', '#b38c5c'];
    const build = () => {
      const pw = parseFloat(getComputedStyle(pv).getPropertyValue('--pw')) || pv.offsetHeight;
      const n = Math.ceil(innerWidth / (pw + 3)) + 2;
      let seed = 7;
      const rnd = () => (seed = (seed * 9301 + 49297) % 233280) / 233280;
      pv.innerHTML = [0, 1, 2].map(r => '<div class="row">' + Array.from({ length: n }, (_, k) =>
        `<i style="--c:${C[Math.floor(rnd() * C.length)]};--d:${(1.1 + k * 0.03 + r * 0.1 + rnd() * 0.08).toFixed(2)}s"></i>`).join('') + '</div>').join('');
    };
    build();
    let rw = innerWidth;
    addEventListener('resize', () => { if (Math.abs(innerWidth - rw) > 80) { rw = innerWidth; build(); $$('i', pv).forEach(i => i.style.animationDelay = '0s'); } });
  }

  // navigácia
  const nav = $('#nav');
  const onScroll = () => nav.classList.toggle('is-solid', scrollY > 40);
  addEventListener('scroll', onScroll, { passive: true }); onScroll();
  const burger = $('#burger');
  const close = () => { nav.classList.remove('is-open'); burger.setAttribute('aria-expanded', false); document.body.style.overflow = ''; };
  burger.addEventListener('click', () => {
    const open = nav.classList.toggle('is-open');
    burger.setAttribute('aria-expanded', open); document.body.style.overflow = open ? 'hidden' : '';
  });
  $$('#menu a').forEach(a => a.addEventListener('click', close));

  // odhalenie pri skrolovaní
  const io = new IntersectionObserver(es => es.forEach(e => {
    if (e.isIntersecting) { e.target.classList.add('is-in'); io.unobserve(e.target); }
  }), { rootMargin: '0px 0px -8% 0px' });
  $$('.rv').forEach(el => {
    const sib = [...el.parentElement.children].filter(c => c.classList.contains('rv'));
    const idx = sib.indexOf(el); if (idx > 0) el.style.transitionDelay = Math.min(idx, 6) * 0.07 + 's';
    io.observe(el);
  });

  // čísla
  const cio = new IntersectionObserver(es => es.forEach(e => {
    if (!e.isIntersecting) return; cio.unobserve(e.target);
    const el = e.target, to = +el.dataset.count;
    if (calm) return;
    const from = to > 1000 ? to - 22 : 0, t0 = performance.now(), dur = 1500;
    const tick = t => { const k = Math.min(1, (t - t0) / dur); el.textContent = Math.round(from + (to - from) * (1 - Math.pow(1 - k, 4))); if (k < 1) requestAnimationFrame(tick); };
    el.textContent = from; requestAnimationFrame(tick);
  }), { threshold: .6 });
  $$('[data-count]').forEach(el => cio.observe(el));

  // služby – vždy otvorená len jedna
  const det = $$('.svc__i');
  det.forEach(d => d.addEventListener('toggle', () => { if (d.open) det.forEach(o => { if (o !== d) o.open = false; }); }));

  // postup – rez spevnenou plochou sa skladá po krokoch
  const steps = $$('.step'), groups = $$('#rez .k'), fn = $('#flowN'), ft = $('#flowT');
  const names = steps.map(s => $('h3', s).textContent);
  let cur = -2;
  const setStep = i => {
    if (i === cur) return; cur = i;
    steps.forEach((s, k) => s.classList.toggle('is-on', k === i));
    groups.forEach(g => {
      const k = +g.dataset.k, u = g.dataset.until === undefined ? 99 : +g.dataset.until;
      g.classList.toggle('on', i >= k && i < u);
    });
    fn.textContent = String(i + 1).padStart(2, '0') + ' / ' + String(steps.length).padStart(2, '0');
    ft.textContent = i < 0 ? 'Pôvodný terén' : names[i];
  };
  let tk = false;
  const checkSteps = () => {
    tk = false;
    const line = innerHeight * (innerWidth <= 960 ? .8 : .6);
    let i = -1; steps.forEach((s, k) => { if (s.getBoundingClientRect().top < line) i = k; });
    setStep(i);
  };
  addEventListener('scroll', () => { if (!tk) { tk = true; requestAnimationFrame(checkSteps); } }, { passive: true });
  addEventListener('resize', checkSteps); checkSteps();

  // referencie – filter, mapa, „zobraziť všetky“
  const cards = $$('.card'), wrapC = $('#cards'), pins = $$('.pin'), note = $('#mapNote'), noteTxt = note.textContent;
  const more = $('#more');
  let kat = '*', obec = null;
  const apply = () => {
    const all = kat !== '*' || obec;
    cards.forEach(c => {
      const ok = (kat === '*' || c.dataset.k === kat) && (!obec || c.dataset.obce.split('|').includes(obec));
      c.classList.toggle('is-out', !ok);
      if (all) c.classList.remove('is-more');
    });
    if (all) more.parentElement.hidden = true;
    pins.forEach(p => {
      const has = cards.some(c => !c.classList.contains('is-out') && c.dataset.obce.split('|').includes(p.dataset.obec));
      p.style.opacity = has ? '' : .3;
      p.classList.toggle('is-sel', p.dataset.obec === obec);
    });
    if (obec) {
      const n = cards.filter(c => !c.classList.contains('is-out')).length;
      note.innerHTML = `${obec} · ${n} ${n === 1 ? 'stavba' : n < 5 ? 'stavby' : 'stavieb'} <button type="button">Zrušiť výber obce</button>`;
      $('button', note).addEventListener('click', () => { obec = null; apply(); });
    } else note.textContent = noteTxt;
  };
  more.addEventListener('click', () => { cards.forEach(c => c.classList.remove('is-more')); more.parentElement.hidden = true; });
  $$('.filters button').forEach(b => b.addEventListener('click', () => {
    $$('.filters button').forEach(x => x.classList.toggle('is-on', x === b));
    kat = b.dataset.f; apply();
  }));
  const hot = (o, on) => {
    wrapC.classList.toggle('is-hl', on);
    cards.forEach(c => c.classList.toggle('is-hot', on && c.dataset.obce.split('|').includes(o)));
    pins.forEach(p => p.classList.toggle('is-hot', on && p.dataset.obec === o));
  };
  pins.forEach(p => {
    const o = p.dataset.obec;
    p.addEventListener('pointerenter', () => hot(o, true));
    p.addEventListener('pointerleave', () => hot(o, false));
    const pick = () => {
      obec = obec === o ? null : o; apply(); hot(o, false);
      if (obec && innerWidth <= 960) $('.refs__col').scrollIntoView({ behavior: calm ? 'auto' : 'smooth', block: 'start' });
    };
    p.addEventListener('click', pick);
    p.addEventListener('keydown', e => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); pick(); } });
  });
  cards.forEach(c => {
    c.addEventListener('pointerenter', () => { if (matchMedia('(hover: hover)').matches) c.dataset.obce.split('|').forEach(o => pins.forEach(p => { if (p.dataset.obec === o) p.classList.add('is-hot'); })); });
    c.addEventListener('pointerleave', () => pins.forEach(p => p.classList.remove('is-hot')));
  });

  // lightbox – všetky fotky jednej stavby
  const lb = $('#lb'), lbI = $('#lbI'), lbC = $('#lbC');
  let li = 0, list = [], cap = '', last = null;
  const show = i => { li = (i + list.length) % list.length; lbI.src = list[li]; lbI.alt = cap; lbC.textContent = `${cap} · ${li + 1} / ${list.length}`; };
  const lbClose = () => { lb.hidden = true; document.body.style.overflow = ''; if (last) last.focus(); };
  const open = c => {
    last = c; list = c.dataset.fotos.split(','); cap = c.dataset.cap;
    show(0); lb.hidden = false; document.body.style.overflow = 'hidden'; $('#lbX').focus();
    list.slice(1, 3).forEach(s => { const im = new Image(); im.src = s; });
  };
  cards.forEach(c => {
    c.addEventListener('click', () => open(c));
    c.addEventListener('keydown', e => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); open(c); } });
  });
  $('#lbX').addEventListener('click', lbClose);
  $('#lbP').addEventListener('click', () => show(li - 1));
  $('#lbN').addEventListener('click', () => show(li + 1));
  lb.addEventListener('click', e => { if (e.target === lb || e.target.tagName === 'FIGURE') lbClose(); });
  addEventListener('keydown', e => {
    if (lb.hidden) return;
    if (e.key === 'Escape') lbClose(); else if (e.key === 'ArrowLeft') show(li - 1); else if (e.key === 'ArrowRight') show(li + 1);
  });
  let sx = 0;
  lb.addEventListener('touchstart', e => { sx = e.touches[0].clientX; }, { passive: true });
  lb.addEventListener('touchend', e => { const dx = e.changedTouches[0].clientX - sx; if (Math.abs(dx) > 50) show(li + (dx < 0 ? 1 : -1)); });

  // formulár – v náhľade neodosiela
  $('#form').addEventListener('submit', e => { e.preventDefault(); $('#formNote').hidden = false; });
})();

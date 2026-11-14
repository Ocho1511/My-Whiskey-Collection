// ---- Glas-Info: eigene Zeichnungen (lizenzfrei, offline) + kurze Erklaerung ----
// glassId() ist bewusst eine reine Funktion ohne Verweis auf spaeter definierte Konstanten (wird schon beim ersten Rendern genutzt)
function glassId(name) {
  const n = String(name || '').toLowerCase();
  if (/glencairn|nosing|tulpe|tulip/.test(n)) return 'glencairn';
  if (/highball|longdrink|collins/.test(n)) return 'highball';
  if (/coupe|schale|martini/.test(n)) return 'coupe';
  if (/julep|becher|cup/.test(n) && !/kaffee|coffee/.test(n)) return 'julep';
  if (/henkel|irish|coffee|kaffee/.test(n)) return 'irishcoffee';
  if (/tumbler|rocks|old.?fashioned|whisky.?glas|whiskey.?glas|whisky glass/.test(n)) return 'tumbler';
  return null;
}
function glassClick(a, ev) {
  ev.stopPropagation();
  const name = a.getAttribute('data-glass') || '';
  if (glassId(name)) { ev.preventDefault(); showGlass(name); return false; }
  return true;   // unbekanntes Glas: normale Bildersuche
}
const GLASS_DRAW = {
  glencairn: '<path d="M31 18C29 30 20 44 22 62c1 10 8 14 10 18v4q18 6 36 0v-4c2-4 9-8 10-18 2-18-7-32-9-44z" fill="url(#gg)"/><path d="M23.4 56C23 64 28 70 32 76l36 0c4-6 9-12 8.6-20z" fill="url(#gl)"/><path d="M27 32c-3 10-4 18-2 26" stroke="#fff" stroke-opacity=".7" stroke-width="2.4" fill="none" stroke-linecap="round"/><ellipse cx="50" cy="90" rx="22" ry="2.6" fill="#000" opacity=".25"/>',
  tumbler: '<path d="M25 26h50l-4 58q-.4 5-5 5H34q-4.6 0-5-5z" fill="url(#gg)"/><path d="M27.4 54h45.2l-1.6 30q-.4 4-5 4H34q-4.6 0-5-4z" fill="url(#gl)"/><rect x="33" y="34" width="20" height="22" rx="4" fill="#fff" fill-opacity=".55" transform="rotate(-9 43 45)"/><rect x="50" y="40" width="18" height="19" rx="4" fill="#fff" fill-opacity=".45" transform="rotate(10 59 49)"/><path d="M30 34l2.6 44" stroke="#fff" stroke-opacity=".7" stroke-width="2.4" fill="none" stroke-linecap="round"/><ellipse cx="50" cy="91" rx="24" ry="2.6" fill="#000" opacity=".25"/>',
  highball: '<path d="M35 8h30l-2.4 80q-.2 5-5 5H42.4q-4.8 0-5-5z" fill="url(#gg)"/><path d="M36.4 34h27.2l-1.6 54q-.2 4-4.6 4H42.6q-4.4 0-4.6-4z" fill="url(#gl)"/><rect x="40" y="22" width="14" height="16" rx="3" fill="#fff" fill-opacity=".55" transform="rotate(-8 47 30)"/><rect x="48" y="40" width="13" height="15" rx="3" fill="#fff" fill-opacity=".45" transform="rotate(9 54 47)"/><circle cx="46" cy="64" r="1.6" fill="#fff" fill-opacity=".7"/><circle cx="54" cy="72" r="1.2" fill="#fff" fill-opacity=".7"/><circle cx="49" cy="80" r="1.5" fill="#fff" fill-opacity=".7"/><path d="M40 14l1.8 70" stroke="#fff" stroke-opacity=".7" stroke-width="2.2" fill="none" stroke-linecap="round"/><ellipse cx="50" cy="94" rx="17" ry="2.2" fill="#000" opacity=".25"/>',
  coupe: '<path d="M18 28q0 28 32 28t32-28z" fill="url(#gg)"/><path d="M22 36q2 18 28 18t28-18z" fill="url(#gl)"/><rect x="47.6" y="55" width="4.8" height="28" rx="1.4" fill="url(#gg)"/><ellipse cx="50" cy="86" rx="16" ry="3.6" fill="url(#gg)"/><path d="M24 32c1 8 5 14 11 17" stroke="#fff" stroke-opacity=".7" stroke-width="2.2" fill="none" stroke-linecap="round"/><circle cx="62" cy="42" r="3.4" fill="#b3202e"/><path d="M62 38.8q2-4 5-4.6" stroke="#4d6b2f" stroke-width="1.2" fill="none"/>',
  julep: '<path d="M27 30h46l-5 54q-.4 4.6-5 4.6H37q-4.6 0-5-4.6z" fill="url(#gs)"/><path d="M33 44h34M32 58h36M33 72h34" stroke="#fff" stroke-opacity=".35" stroke-width="1.4"/><path d="M26 30q24-9 48 0" fill="none" stroke="#e8edf2" stroke-width="3" stroke-linecap="round"/><g fill="#5faa5a"><ellipse cx="38" cy="22" rx="7" ry="3.6" transform="rotate(-30 38 22)"/><ellipse cx="50" cy="18" rx="7" ry="3.6" transform="rotate(-85 50 18)"/><ellipse cx="62" cy="22" rx="7" ry="3.6" transform="rotate(25 62 22)"/><ellipse cx="50" cy="26" rx="6" ry="3.2"/></g><circle cx="34" cy="31" r="2.6" fill="#fff" fill-opacity=".8"/><circle cx="44" cy="32" r="2.6" fill="#fff" fill-opacity=".8"/><circle cx="55" cy="31" r="2.6" fill="#fff" fill-opacity=".8"/><circle cx="65" cy="32" r="2.6" fill="#fff" fill-opacity=".8"/><ellipse cx="50" cy="92" rx="22" ry="2.4" fill="#000" opacity=".25"/>',
  irishcoffee: '<path d="M28 20h44l-4 44q-.6 8-9 8H41q-8.4 0-9-8z" fill="url(#gg)"/><path d="M31.4 46h37.2l-1 18q-.6 7-8.4 7h-18.4q-7.8 0-8.4-7z" fill="#4a2a14"/><path d="M29.6 28h40.8l-1 10H30.6z" fill="#f6efe2"/><path d="M72 28c18 0 18 26-4 28" fill="none" stroke="url(#gg)" stroke-width="5" stroke-linecap="round"/><rect x="46.6" y="72" width="6.8" height="10" rx="1.4" fill="url(#gg)"/><ellipse cx="50" cy="86" rx="14" ry="3.4" fill="url(#gg)"/><path d="M33 26c-1 8 0 18 3 30" stroke="#fff" stroke-opacity=".7" stroke-width="2.2" fill="none" stroke-linecap="round"/>'
};
const GLASS_TXT = {
  glencairn: {
    de: ['Glencairn-Glas', 'Das Standardglas für Whisky-Verkostungen. Der bauchige Körper lässt den Whisky atmen, die schmale Öffnung bündelt das Aroma zur Nase. Man trinkt Whisky pur oder mit wenigen Tropfen Wasser daraus.'],
    en: ['Glencairn glass', 'The standard tasting glass for whisky. The bulbous body lets the whisky breathe and the narrow rim funnels the aroma to your nose. Used for whisky neat or with a few drops of water.']
  },
  tumbler: {
    de: ['Tumbler (Rocks-Glas)', 'Ein kurzes, breites Glas mit schwerem Boden, auch Old-Fashioned-Glas genannt. Ideal für Whiskey auf Eis und für Cocktails wie Old Fashioned, Boulevardier oder Rusty Nail.'],
    en: ['Tumbler (rocks glass)', 'A short, wide glass with a heavy base, also called an old fashioned glass. Ideal for whiskey on the rocks and for cocktails such as the Old Fashioned, Boulevardier or Rusty Nail.']
  },
  highball: {
    de: ['Highball-Glas', 'Hoch und schmal. Es hält Eis und Kohlensäure lange kühl und spritzig, perfekt für Whisky mit Soda oder Ginger Ale.'],
    en: ['Highball glass', 'Tall and narrow. It keeps ice and fizz cold and lively for a long time, perfect for whisky with soda or ginger ale.']
  },
  coupe: {
    de: ['Coupe', 'Eine flache Schale auf Stiel für Cocktails ohne Eis, etwa Manhattan, Rob Roy oder Whisky Sour. Am Stiel gehalten, wärmt die Hand das Getränk nicht.'],
    en: ['Coupe', 'A shallow bowl on a stem for cocktails served without ice, such as the Manhattan, Rob Roy or whisky sour. Held by the stem, your hand does not warm the drink.']
  },
  julep: {
    de: ['Julep-Becher', 'Ein Metallbecher, meist aus Silber oder Zinn. Er beschlägt mit Crushed Ice und hält den Mint Julep eiskalt, dazu ein Bund frische Minze.'],
    en: ['Julep cup', 'A metal cup, usually silver or pewter. It frosts over with crushed ice and keeps the mint julep ice cold, topped with a bunch of fresh mint.']
  },
  irishcoffee: {
    de: ['Irish-Coffee-Glas', 'Ein hitzebeständiges Henkelglas mit Stiel, damit man den heißen Kaffee mit Whiskey und kalter Sahnehaube gut halten kann.'],
    en: ['Irish coffee glass', 'A heat-resistant glass with a handle and stem, so you can comfortably hold the hot coffee with whiskey and a cold cream top.']
  }
};
function showGlass(name) {
  const id = glassId(name);
  if (!id) return;
  const lang = serveLang() === 'de' ? 'de' : 'en';
  const [title, text] = GLASS_TXT[id][lang];
  const more = lang === 'de' ? 'Mehr Bilder ansehen ↗' : 'See more pictures ↗';
  const close = lang === 'de' ? 'Schließen' : 'Close';
  const old = document.getElementById('glass-overlay'); if (old) old.remove();
  const o = document.createElement('div');
  o.id = 'glass-overlay'; o.className = 'glass-overlay';
  o.innerHTML = `<div class="glass-card" role="dialog" aria-label="${esc(title)}">
    <svg viewBox="0 0 100 100" width="150" height="150" aria-hidden="true"><defs>
      <linearGradient id="gg" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#bcd4e0"/><stop offset=".3" stop-color="#f4fafc"/><stop offset=".7" stop-color="#d3e5ee"/><stop offset="1" stop-color="#9fbacb"/></linearGradient>
      <linearGradient id="gl" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f0b455"/><stop offset="1" stop-color="#b9731f"/></linearGradient>
      <linearGradient id="gs" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#9aa6b3"/><stop offset=".35" stop-color="#f1f4f7"/><stop offset=".7" stop-color="#c3ccd6"/><stop offset="1" stop-color="#8b97a4"/></linearGradient>
    </defs>${GLASS_DRAW[id]}</svg>
    <div class="glass-title">${esc(title)}</div>
    <p>${esc(text)}</p>
    <a class="glass-link" href="${glassUrl(name)}" target="_blank" rel="noopener">${more}</a>
    <button type="button" class="wine-btn primary" id="glass-close">${close}</button>
  </div>`;
  o.addEventListener('click', e => { if (e.target === o) o.remove(); });
  document.body.appendChild(o);
  document.getElementById('glass-close').onclick = () => o.remove();
}

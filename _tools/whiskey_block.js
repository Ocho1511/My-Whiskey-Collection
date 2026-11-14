/* ═══════════════════════════════════════
   PERFECT SERVE · REZEPTE · ZUTATENREGAL (Whiskey)
   Texte in diesem Block: Deutsch und Englisch (andere Sprachen zeigen Englisch)
═══════════════════════════════════════ */
const SX = {
  de: {
    need_name: 'Bitte erst den Namen eintragen', busy: '⏳ Empfehlung wird gesucht…', none: 'Keine Empfehlung gefunden', applied: 'Empfehlung übernommen ✓',
    fav_set: 'Als Favorit gesetzt ✓', wish_added: 'Auf die Wunschliste gesetzt ✓',
    glass_glencairn: 'Glencairn-Glas', glass_tumbler: 'Tumbler', glass_highball: 'Highball-Glas',
    ice_none: 'ohne Eis', ice_big: 'große Kugel oder Würfel', ice_cubes: 'Eiswürfel',
    water_drops: '2–3 Tropfen Wasser', mix_soda: '1:3 mit Soda oder Ginger Ale', mix_cocktail: 'nach Rezept',
    rec_title: 'Rezepte', rec_sub: 'Klassiker und Cocktails', rec_all: 'Alle', rec_fav: '⭐ Favoriten', rec_own: 'Eigene', rec_mine: '🥃 Passt zu meiner Bar',
    rec_fits: 'Passt zu', rec_none: 'Keine Rezepte für diese Auswahl.', rec_ing: 'Zutaten', rec_steps: 'Zubereitung', rec_glass: 'Glas',
    rec_ai_title: 'Rezept für einen Whisky (KI)', rec_ai_btn: '🤖 Rezept erstellen', rec_pick: 'Whisky wählen…', rec_save: 'Als eigenes Rezept speichern', rec_saved: 'Rezept gespeichert ✓',
    rec_add_title: 'Eigenes Rezept anlegen', rec_name: 'Name', rec_ing_ph: 'Zutaten, eine pro Zeile', rec_steps_ph: 'Zubereitung', rec_add_btn: 'Rezept speichern',
    rec_del: 'Dieses Rezept löschen?', rec_busy: '⏳ Rezept wird erstellt…', rec_fail: 'Das hat nicht geklappt', rec_name_req: 'Bitte einen Namen eingeben',
    shelf_title: 'Mein Zutatenregal (Mixer, Garnitur, Zutaten)', shelf_hint: 'Tippe an, was du zu Hause hast. Die Empfehlungen zeigen dann ✓ (vorhanden) oder 🛒 (fehlt).',
    shelf_missing: '🛒 Fehlendes auf die Wunschliste', shelf_nothing: 'Für deine Whiskys fehlt nichts.', shelf_done: '{n} auf die Wunschliste gesetzt ✓', shelf_wish_note: 'Zutat/Garnitur'
  },
  en: {
    need_name: 'Please enter the name first', busy: '⏳ Looking for a recommendation…', none: 'No recommendation found', applied: 'Recommendation applied ✓',
    fav_set: 'Set as favourite ✓', wish_added: 'Added to the wish list ✓',
    glass_glencairn: 'Glencairn glass', glass_tumbler: 'Tumbler', glass_highball: 'Highball glass',
    ice_none: 'no ice', ice_big: 'large sphere or cube', ice_cubes: 'ice cubes',
    water_drops: '2–3 drops of water', mix_soda: '1:3 with soda or ginger ale', mix_cocktail: 'per recipe',
    rec_title: 'Recipes', rec_sub: 'Classics and cocktails', rec_all: 'All', rec_fav: '⭐ Favourites', rec_own: 'Mine', rec_mine: '🥃 Fits my bar',
    rec_fits: 'Fits', rec_none: 'No recipes for this selection.', rec_ing: 'Ingredients', rec_steps: 'Method', rec_glass: 'Glass',
    rec_ai_title: 'Recipe for a whisky (AI)', rec_ai_btn: '🤖 Create recipe', rec_pick: 'Choose a whisky…', rec_save: 'Save as my recipe', rec_saved: 'Recipe saved ✓',
    rec_add_title: 'Add your own recipe', rec_name: 'Name', rec_ing_ph: 'Ingredients, one per line', rec_steps_ph: 'Method', rec_add_btn: 'Save recipe',
    rec_del: 'Delete this recipe?', rec_busy: '⏳ Creating recipe…', rec_fail: 'That did not work', rec_name_req: 'Please enter a name',
    shelf_title: 'My ingredient shelf (mixers, garnish, ingredients)', shelf_hint: 'Tap what you have at home. Recommendations then show ✓ (have) or 🛒 (missing).',
    shelf_missing: '🛒 Add missing items to the wish list', shelf_nothing: 'Nothing is missing for your whiskies.', shelf_done: '{n} added to the wish list ✓', shelf_wish_note: 'Ingredient/garnish'
  }
};
function serveLang() { return baseLang() === 'de' ? 'de' : 'en'; }
function sx(k, vars) {
  let s = (SX[serveLang()][k] ?? SX.en[k] ?? k);
  if (vars) Object.entries(vars).forEach(([a, b]) => { s = s.split('{' + a + '}').join(b); });
  return s;
}
const sxPick = (pair) => pair[serveLang() === 'de' ? 0 : 1];

// ---- Katalog: Mixer, Garnitur, Zutaten (id: [de, en]) ----
const SERVE_ING = {
  orange: ['Orangenzeste', 'Orange peel'], lemon: ['Zitronenzeste', 'Lemon peel'], cherry: ['Kirsche (Amarena)', 'Cherry (amarena)'], mint: ['Minze', 'Mint'],
  ginger: ['Ingwer', 'Ginger'], cinnamon: ['Zimtstange', 'Cinnamon stick'], sugar: ['Zuckersirup', 'Sugar syrup'], honey: ['Honig', 'Honey'],
  gingerale: ['Ginger Ale', 'Ginger ale'], soda: ['Sodawasser', 'Soda water'], bitters: ['Angostura Bitters', 'Angostura bitters'],
  vermsweet: ['Süßer Wermut', 'Sweet vermouth'], vermdry: ['Trockener Wermut', 'Dry vermouth'], lemonjuice: ['Zitronensaft', 'Lemon juice']
};
// ---- Genussarten ----
const SERVE_WAY = {
  neat: { n: ['Pur', 'Neat'], why: ['Zeigt das volle Aroma ohne Verdünnung', 'Shows the full aroma without dilution'] },
  water: { n: ['Pur mit ein paar Tropfen Wasser', 'Neat with a few drops of water'], why: ['Wasser öffnet die Aromen und mildert den Alkohol', 'Water opens the aromas and softens the alcohol'] },
  rocks: { n: ['Auf Eis (on the rocks)', 'On the rocks'], why: ['Kühlt und rundet ab, angenehm bei Wärme', 'Chills and rounds off, pleasant in warm weather'] },
  highball: { n: ['Highball mit Soda oder Ginger Ale', 'Highball with soda or ginger ale'], why: ['Leicht und erfrischend, gut für Blends', 'Light and refreshing, good for blends'] },
  oldfashioned: { n: ['Old Fashioned', 'Old fashioned'], why: ['Süße und Bitters runden kräftige Whiskys ab', 'Sweetness and bitters round off bold whiskies'] }
};
const SERVE_FOOD = {
  peat: [['Blauschimmelkäse', 'Geräucherter Lachs', 'Dunkle Schokolade'], ['Blue cheese', 'Smoked salmon', 'Dark chocolate']],
  sherry: [['Trockenfrüchte', 'Nüsse', 'Dunkle Schokolade'], ['Dried fruit', 'Nuts', 'Dark chocolate']],
  bourbon: [['BBQ', 'Pekannuss', 'Karamell'], ['BBQ', 'Pecan', 'Caramel']],
  blend: [['Hartkäse', 'Nüsse'], ['Hard cheese', 'Nuts']],
  world: [['Käse', 'Schokolade'], ['Cheese', 'Chocolate']],
  malt: [['Reifer Käse', 'Dunkle Schokolade'], ['Aged cheese', 'Dark chocolate']]
};
// ---- Regeln: Stichwort in Name/Destillerie/Fass/Region -> Genussarten, Garnitur, Speisen ----
const SERVE_RULES = [
  [/torf|peat|rauch|smok|islay|laphroaig|ardbeg|lagavulin|caol ila|bowmore|talisker/i, { w: ['water', 'neat'], g: [], f: 'peat' }],
  [/sherry|oloroso|pedro|ximenez|\bpx\b|macallan|glendronach/i, { w: ['water', 'neat'], g: ['orange'], f: 'sherry' }],
  [/bourbon|\brye\b|tennessee|maker'?s|buffalo|jim beam|jack daniel|four roses|wild turkey|woodford/i, { w: ['rocks', 'oldfashioned', 'highball'], g: ['orange', 'cherry'], f: 'bourbon' }],
  [/irish|jameson|redbreast|bushmills|teeling/i, { w: ['neat', 'highball'], g: ['lemon', 'ginger'], f: 'blend' }]
];
function serveByRules(g) {
  const text = [g.name, g.grape, g.cask, g.region].filter(Boolean).join(' ');
  const ways = [], garn = [];
  let food = null;
  SERVE_RULES.forEach(([re, eff]) => {
    if (re.test(text)) {
      eff.w.forEach(x => { if (!ways.includes(x)) ways.push(x); });
      eff.g.forEach(x => { if (!garn.includes(x)) garn.push(x); });
      if (!food) food = eff.f;
    }
  });
  if (g.type === 'weiß') {        // Bourbon/Rye
    ['rocks', 'oldfashioned', 'highball'].forEach(x => { if (!ways.includes(x)) ways.push(x); });
    ['orange', 'cherry'].forEach(x => { if (!garn.includes(x)) garn.push(x); });
    if (!food) food = 'bourbon';
  } else if (g.type === 'rosé') { // Blended
    ['highball', 'rocks'].forEach(x => { if (!ways.includes(x)) ways.push(x); });
    if (!garn.includes('lemon')) garn.push('lemon');
    if (!food) food = 'blend';
  } else if (g.type === 'sekt') { // World
    ['neat', 'rocks'].forEach(x => { if (!ways.includes(x)) ways.push(x); });
    if (!food) food = 'world';
  } else {                        // Single Malt und Sonstiges
    ['water', 'neat'].forEach(x => { if (!ways.includes(x)) ways.push(x); });
    if (!food) food = 'malt';
  }
  const top = ways.slice(0, 3);
  const first = top[0];
  const glass = (first === 'neat' || first === 'water') ? sx('glass_glencairn') : first === 'highball' ? sx('glass_highball') : sx('glass_tumbler');
  const ice = (first === 'neat' || first === 'water') ? sx('ice_none') : first === 'highball' ? sx('ice_cubes') : sx('ice_big');
  const ratio = first === 'water' ? sx('water_drops') : first === 'highball' ? sx('mix_soda') : first === 'oldfashioned' ? sx('mix_cocktail') : '';
  return {
    tips: top.map(id => ({ n: sxPick(SERVE_WAY[id].n), why: sxPick(SERVE_WAY[id].why) })),
    garnish: garn.slice(0, 4).map(id => sxPick(SERVE_ING[id])), ratio, glass, ice,
    food: sxPick(SERVE_FOOD[food]).join(', ')
  };
}
async function aiServe(g) {
  const lang = serveLang() === 'de' ? 'Deutsch' : 'Englisch';
  const resp = await aiFetch(AI_PROXY_URL, {
    method: 'POST', headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      model: 'claude-sonnet-4-6', max_tokens: 800,
      system: 'Du bist ein Whisky-Experte. Gib für den genannten Whisky die perfekte Art zu genießen. Antworte NUR mit einem JSON-Objekt ohne Markdown: {"tips":[{"name":"Genussart","why":"höchstens 12 Wörter"}],"garnish":["Mixer oder Garnitur"],"ratio":"Wasser oder Mischung, z. B. 2–3 Tropfen Wasser","glass":"...","ice":"...","food":["passende Speise"]}. tips: genau 3 Genussarten (pur, mit Wasser, auf Eis, Highball, Cocktail) in sinnvoller Reihenfolge; garnish: bis zu 4 Mixer/Garnituren (leer, wenn pur empfohlen); food: bis zu 3 passende Speisen. Alle Texte auf ' + lang + '.',
      messages: [{ role: 'user', content: `Whisky: ${g.name}${g.type ? ' (Stil: ' + (TYPE_LABELS[g.type] || g.type) + ')' : ''}${g.grape ? ', Destillerie: ' + g.grape : ''}${g.region ? ', Region: ' + g.region : ''}${g.age ? ', ' + g.age + ' Jahre' : ''}${g.abv ? ', ' + g.abv + ' % vol.' : ''}${g.cask ? ', Fass: ' + g.cask : ''}.` }]
    })
  });
  const data = await resp.json();
  if (data.type === 'error' || !data.content) return null;
  const text = (data.content || []).filter(b => b.type === 'text').map(b => b.text).join('\n');
  const m = text.match(/\{[\s\S]*\}/);
  if (!m) return null;
  try {
    const j = JSON.parse(m[0]);
    const tips = (Array.isArray(j.tips) ? j.tips : []).slice(0, 3).map(x => ({ n: String((x && x.name) || '').trim().slice(0, 120), why: String((x && x.why) || '').slice(0, 160) })).filter(x => x.n);
    const garnish = (Array.isArray(j.garnish) ? j.garnish : []).map(x => String(x).trim()).filter(Boolean).slice(0, 6);
    const food = (Array.isArray(j.food) ? j.food : []).map(x => String(x).trim()).filter(Boolean).slice(0, 4).join(', ');
    if (!tips.length && !garnish.length && !food) return null;
    return { tips, garnish, ratio: String(j.ratio || '').slice(0, 40), glass: String(j.glass || '').slice(0, 60), ice: String(j.ice || '').slice(0, 60), food: food.slice(0, 200) };
  } catch { return null; }
}

// ---- Formular: Perfect Serve ----
let serveTips = [], serveSrc = '', serveFav = '';
const sv = (id) => document.getElementById(id);
function serveItemFromForm() {
  const v = id => (sv(id) ? sv(id).value.trim() : '');
  return { name: v('f-name'), type: v('f-type'), grape: v('f-grape'), region: v('f-region'), age: v('f-age'), abv: v('f-abv'), cask: v('f-cask') };
}
function cleanServe(s) {
  if (!s || typeof s !== 'object') return null;
  const tips = (Array.isArray(s.tips) ? s.tips : []).slice(0, 4).map(x => ({ n: cleanStr(x && x.n, 120).trim(), why: cleanStr(x && x.why, 160).trim() })).filter(x => x.n);
  const o = { garnish: cleanText(s.garnish, 240), ratio: cleanText(s.ratio, 40), glass: cleanText(s.glass, 60), ice: cleanText(s.ice, 60), food: cleanText(s.food, 240), fav: cleanText(s.fav, 120), tips, src: ['rules', 'ai', 'own'].includes(s.src) ? s.src : null };
  return (o.garnish || o.ratio || o.glass || o.ice || o.food || o.fav || tips.length) ? o : null;
}
function serveReadForm() {
  const v = id => (sv(id) ? sv(id).value.trim() : '');
  return cleanServe({ garnish: v('f-serve-garnish'), ratio: v('f-serve-ratio'), glass: v('f-serve-glass'), ice: v('f-serve-ice'), food: v('f-serve-food'), fav: serveFav, tips: serveTips, src: serveSrc || 'own' });
}
function serveWriteForm(s) {
  s = s || {};
  if (sv('f-serve-garnish')) sv('f-serve-garnish').value = s.garnish || '';
  if (sv('f-serve-ratio')) sv('f-serve-ratio').value = s.ratio || '';
  if (sv('f-serve-glass')) sv('f-serve-glass').value = s.glass || '';
  if (sv('f-serve-ice')) sv('f-serve-ice').value = s.ice || '';
  if (sv('f-serve-food')) sv('f-serve-food').value = s.food || '';
  serveTips = Array.isArray(s.tips) ? s.tips.slice() : [];
  serveSrc = s.src || '';
  serveFav = s.fav || '';
  serveRenderReco();
}
function serveIngId(name) {
  const n = String(name || '').trim().toLowerCase();
  if (!n) return null;
  return Object.keys(SERVE_ING).find(id => SERVE_ING[id].some(x => x.toLowerCase() === n || n.includes(x.toLowerCase()) || x.toLowerCase().includes(n))) || null;
}
function serveRenderReco() {
  const box = sv('serve-reco');
  if (!box) return;
  let html = serveTips.map((x, i) => `<div class="serve-tip">
      <button type="button" class="filter-chip ${serveFav && x.n.toLowerCase() === serveFav.toLowerCase() ? 'active' : ''}" onclick="serveSetFav(${i})">🥃 ${esc(x.n)}</button>
      <span class="serve-why">${esc(x.why)}</span>
    </div>`).join('');
  const shelf = settings.herbs || [];
  const items = (sv('f-serve-garnish') ? sv('f-serve-garnish').value : '').split(',').map(x => x.trim()).filter(Boolean);
  if (shelf.length && items.length) {
    html += '<div class="serve-shelf">' + items.map(it => { const id = serveIngId(it); return id ? (shelf.includes(id) ? '✓ ' : '🛒 ') + esc(it) : esc(it); }).join(' · ') + '</div>';
  }
  box.innerHTML = html;
}
function serveApply(r, src) {
  if (sv('f-serve-garnish')) sv('f-serve-garnish').value = (r.garnish || []).join(', ');
  if (sv('f-serve-ratio')) sv('f-serve-ratio').value = r.ratio || '';
  if (sv('f-serve-glass')) sv('f-serve-glass').value = r.glass || '';
  if (sv('f-serve-ice')) sv('f-serve-ice').value = r.ice || '';
  if (sv('f-serve-food')) sv('f-serve-food').value = r.food || '';
  serveTips = r.tips || [];
  serveFav = serveTips[0] ? serveTips[0].n : '';
  serveSrc = src;
  serveRenderReco();
  showToast(sx('applied'));
}
async function serveFill(mode) {
  const g = serveItemFromForm();
  if (!g.name) { showToast(sx('need_name')); return; }
  if (mode === 'ai') {
    showToast(sx('busy'));
    let r = null;
    try { r = await aiServe(g); } catch (e) { if (e && (e.noCredits || e.noConsent)) return; }
    if (!r) { showToast(sx('none')); return; }
    serveApply(r, 'ai');
  } else {
    serveApply(serveByRules(g), 'rules');
  }
}
function serveSetFav(i) {
  const x = serveTips[i];
  if (!x) return;
  serveFav = x.n;
  serveRenderReco();
  showToast(sx('fav_set'));
}
// Anzeige auf der Karte: Favorit-Genussart, Garnitur, Speisen
function serveCardLine(w) {
  const s = w.serve;
  if (!s) return '';
  const a = [s.fav, s.garnish].filter(Boolean).join(' · ');
  const b = s.food ? `<div class="wine-region" style="margin-top:2px">🍽 ${esc(s.food)}</div>` : '';
  return (a ? `<div class="wine-region" style="margin-top:4px">🥃 ${esc(a)}${s.ratio ? ' (' + esc(s.ratio) + ')' : ''}</div>` : '') + b;
}

// ---- Zutatenregal (in den Einstellungen gespeichert, wird mit dem Cloud-Stand synchronisiert) ----
function toggleHerb(id) {
  if (!SERVE_ING[id]) return;
  const a = settings.herbs || [];
  settings.herbs = a.includes(id) ? a.filter(x => x !== id) : a.concat(id);
  saveRecipesData();
  renderRecipes();
}
function shelfMissingToWish() {
  const have = new Set(settings.herbs || []);
  const need = new Set();
  wines.forEach(w => {
    if (!w.serve || !w.serve.garnish) return;
    w.serve.garnish.split(',').forEach(x => { const id = serveIngId(x); if (id && !have.has(id)) need.add(id); });
  });
  if (!need.size) { showToast(sx('shelf_nothing')); return; }
  let n = 0;
  need.forEach(id => {
    const nm = sxPick(SERVE_ING[id]);
    if (!wishes.some(w => (w.name || '').toLowerCase() === nm.toLowerCase())) {
      wishes.push({ id: Date.now().toString() + id, name: nm, year: null, type: 'other', region: null, country: null, grape: null, note: sx('shelf_wish_note'), done: false });
      n++;
    }
  });
  saveWishes();
  showToast(sx('shelf_done', { n }));
}

// ---- Rezepte (styles = Typ-Schlüssel: rot Single Malt, weiß Bourbon/Rye, rosé Blended, sekt World) ----
const RECIPES = [
  { id: 'oldfashioned', n: ['Old Fashioned', 'Old fashioned'], styles: ['weiß'], glass: { de: 'Tumbler', en: 'Tumbler' },
    ing: { de: ['6 cl Bourbon oder Rye', '1 Zuckerwürfel oder 1 cl Zuckersirup', '2 Dashes Angostura Bitters', 'Orangenzeste'], en: ['6 cl bourbon or rye', '1 sugar cube or 1 cl sugar syrup', '2 dashes Angostura bitters', 'Orange peel'] },
    steps: { de: 'Zucker mit Bitters im Glas verrühren, Whiskey und ein großes Eisstück zugeben, kaltrühren und die Orangenzeste darüber ausdrücken.', en: 'Stir sugar and bitters in the glass, add whiskey and one large ice cube, stir until cold and express an orange peel over it.' } },
  { id: 'manhattan', n: ['Manhattan', 'Manhattan'], styles: ['weiß', 'rosé'], glass: { de: 'Coupe', en: 'Coupe' },
    ing: { de: ['5 cl Rye oder Bourbon', '2 cl süßer Wermut', '2 Dashes Angostura Bitters', 'Amarena-Kirsche'], en: ['5 cl rye or bourbon', '2 cl sweet vermouth', '2 dashes Angostura bitters', 'Amarena cherry'] },
    steps: { de: 'Mit Eis kaltrühren, in die gekühlte Coupe abseihen, Kirsche dazugeben.', en: 'Stir with ice, strain into a chilled coupe, add the cherry.' } },
  { id: 'whiskysour', n: ['Whisky Sour', 'Whiskey sour'], styles: ['weiß', 'rosé'], glass: { de: 'Tumbler', en: 'Tumbler' },
    ing: { de: ['5 cl Bourbon', '3 cl Zitronensaft', '2 cl Zuckersirup', 'Optional: Eiweiß'], en: ['5 cl bourbon', '3 cl lemon juice', '2 cl sugar syrup', 'Optional: egg white'] },
    steps: { de: 'Alle Zutaten erst ohne Eis, dann mit Eis kräftig shaken und auf frisches Eis abseihen.', en: 'Shake all ingredients first without ice, then with ice, and strain over fresh ice.' } },
  { id: 'highball', n: ['Whisky Highball', 'Whisky highball'], styles: ['rosé', 'rot', 'sekt'], glass: { de: 'Highball-Glas', en: 'Highball glass' },
    ing: { de: ['4 cl Whisky', '12 cl Sodawasser oder Ginger Ale', 'Viel Eis', 'Zitronenzeste'], en: ['4 cl whisky', '12 cl soda water or ginger ale', 'Lots of ice', 'Lemon peel'] },
    steps: { de: 'Glas mit Eis füllen, Whisky zugeben, vorsichtig mit Soda auffüllen und einmal umrühren.', en: 'Fill the glass with ice, add the whisky, top gently with soda and stir once.' } },
  { id: 'julep', n: ['Mint Julep', 'Mint julep'], styles: ['weiß'], glass: { de: 'Becher oder Tumbler', en: 'Julep cup or tumbler' },
    ing: { de: ['6 cl Bourbon', '1,5 cl Zuckersirup', 'Viele Minzblätter', 'Crushed Ice'], en: ['6 cl bourbon', '1.5 cl sugar syrup', 'Plenty of mint leaves', 'Crushed ice'] },
    steps: { de: 'Minze mit Sirup leicht andrücken, Bourbon und Crushed Ice zugeben, verrühren und mit einem Minzzweig garnieren.', en: 'Lightly muddle the mint with the syrup, add bourbon and crushed ice, stir and garnish with a mint sprig.' } },
  { id: 'penicillin', n: ['Penicillin', 'Penicillin'], styles: ['rosé', 'rot'], glass: { de: 'Tumbler', en: 'Tumbler' },
    ing: { de: ['5 cl Blended Scotch', '2 cl Zitronensaft', '2 cl Honig-Ingwer-Sirup', '1 cl rauchiger Islay-Whisky zum Schwimmen'], en: ['5 cl blended Scotch', '2 cl lemon juice', '2 cl honey-ginger syrup', '1 cl smoky Islay whisky to float'] },
    steps: { de: 'Blend, Saft und Sirup mit Eis shaken, auf großes Eis abseihen, den Islay darüber schwimmen lassen.', en: 'Shake blend, juice and syrup with ice, strain over large ice, float the Islay on top.' } },
  { id: 'robroy', n: ['Rob Roy', 'Rob Roy'], styles: ['rosé', 'rot'], glass: { de: 'Coupe', en: 'Coupe' },
    ing: { de: ['5 cl Scotch', '2 cl süßer Wermut', '2 Dashes Angostura Bitters', 'Kirsche oder Zitronenzeste'], en: ['5 cl Scotch', '2 cl sweet vermouth', '2 dashes Angostura bitters', 'Cherry or lemon peel'] },
    steps: { de: 'Wie ein Manhattan: mit Eis kaltrühren und in die gekühlte Coupe abseihen.', en: 'Like a Manhattan: stir with ice and strain into a chilled coupe.' } },
  { id: 'boulevardier', n: ['Boulevardier', 'Boulevardier'], styles: ['weiß'], glass: { de: 'Tumbler', en: 'Tumbler' },
    ing: { de: ['4,5 cl Bourbon', '3 cl Campari', '3 cl süßer Wermut', 'Orangenzeste'], en: ['4.5 cl bourbon', '3 cl Campari', '3 cl sweet vermouth', 'Orange peel'] },
    steps: { de: 'Mit Eis kaltrühren, auf frisches Eis abseihen, Orangenzeste ausdrücken.', en: 'Stir with ice, strain over fresh ice, express an orange peel.' } },
  { id: 'irishcoffee', n: ['Irish Coffee', 'Irish coffee'], styles: ['sekt'], glass: { de: 'Henkelglas', en: 'Irish coffee glass' },
    ing: { de: ['4 cl Irish Whiskey', '12 cl heißer Kaffee', '2 TL brauner Zucker', 'Geschlagene Sahne'], en: ['4 cl Irish whiskey', '12 cl hot coffee', '2 tsp brown sugar', 'Lightly whipped cream'] },
    steps: { de: 'Zucker im heißen Kaffee auflösen, Whiskey zugeben und die Sahne vorsichtig über einen Löffel obenauf geben.', en: 'Dissolve the sugar in the hot coffee, add the whiskey and float the cream over a spoon.' } },
  { id: 'rustynail', n: ['Rusty Nail', 'Rusty Nail'], styles: ['rot', 'rosé'], glass: { de: 'Tumbler', en: 'Tumbler' },
    ing: { de: ['5 cl Scotch', '2,5 cl Drambuie', 'Zitronenzeste'], en: ['5 cl Scotch', '2.5 cl Drambuie', 'Lemon peel'] },
    steps: { de: 'Auf Eis im Glas verrühren, Zitronenzeste ausdrücken.', en: 'Stir over ice in the glass, express a lemon peel.' } },
  { id: 'paperplane', n: ['Paper Plane', 'Paper Plane'], styles: ['weiß'], glass: { de: 'Coupe', en: 'Coupe' },
    ing: { de: ['2,5 cl Bourbon', '2,5 cl Aperol', '2,5 cl Amaro Nonino', '2,5 cl Zitronensaft'], en: ['2.5 cl bourbon', '2.5 cl Aperol', '2.5 cl Amaro Nonino', '2.5 cl lemon juice'] },
    steps: { de: 'Alle Zutaten mit Eis shaken und in die gekühlte Coupe abseihen.', en: 'Shake all ingredients with ice and strain into a chilled coupe.' } },
  { id: 'goldrush', n: ['Gold Rush', 'Gold rush'], styles: ['weiß'], glass: { de: 'Tumbler', en: 'Tumbler' },
    ing: { de: ['6 cl Bourbon', '2 cl Zitronensaft', '2 cl Honigsirup'], en: ['6 cl bourbon', '2 cl lemon juice', '2 cl honey syrup'] },
    steps: { de: 'Mit Eis shaken und auf großes Eis abseihen.', en: 'Shake with ice and strain over large ice.' } }
];
function cleanRecipes(a) {
  if (!Array.isArray(a)) return [];
  return a.slice(0, 200).map(r => ({
    id: cleanStr(r && r.id, 40).trim() || ('r' + Date.now() + Math.floor(Math.random() * 1000)),
    name: cleanStr(r && r.name, 120).trim(), ing: cleanStr(r && r.ing, 2000), steps: cleanStr(r && r.steps, 4000), gin: cleanStr(r && r.gin, 120)
  })).filter(r => r.name);
}
function cleanIdList(a) { return Array.isArray(a) ? Array.from(new Set(a.map(x => cleanStr(x, 40).trim()).filter(Boolean))).slice(0, 300) : []; }
function saveRecipesData() { saveSettings(); touchData(); }
let recFilter = 'all', recMine = false, aiRecipe = null, recAiBusy = false;
function setRecFilter(f) { recFilter = f; renderRecipes(); }
function toggleRecMine() { recMine = !recMine; renderRecipes(); }
function toggleRecFav(id) {
  const a = settings.favRecipes || [];
  settings.favRecipes = a.includes(id) ? a.filter(x => x !== id) : a.concat(id);
  saveRecipesData(); renderRecipes();
}
function saveOwnRecipe() {
  const name = sv('rec-n').value.trim();
  if (!name) { showToast(sx('rec_name_req')); return; }
  settings.recipes = (settings.recipes || []).concat({ id: 'r' + Date.now(), name: name.slice(0, 120), ing: sv('rec-i').value.slice(0, 2000), steps: sv('rec-s').value.slice(0, 4000), gin: '' });
  saveRecipesData();
  showToast(sx('rec_saved'));
  renderRecipes();
}
function deleteOwnRecipe(id) {
  if (!confirm(sx('rec_del'))) return;
  settings.recipes = (settings.recipes || []).filter(r => r.id !== id);
  settings.favRecipes = (settings.favRecipes || []).filter(x => x !== id);
  saveRecipesData(); renderRecipes();
}
async function createAiRecipe() {
  if (recAiBusy) return;
  const id = sv('rec-ai-gin') ? sv('rec-ai-gin').value : '';
  const w = wines.find(x => x.id === id);
  if (!w) return;
  recAiBusy = true;
  showToast(sx('rec_busy'));
  try {
    const lang = serveLang() === 'de' ? 'Deutsch' : 'Englisch';
    const resp = await aiFetch(AI_PROXY_URL, {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        model: 'claude-sonnet-4-6', max_tokens: 900,
        system: 'Du bist ein Barkeeper. Erstelle ein gutes Rezept (Cocktail oder besonderer Highball), das den genannten Whisky in Szene setzt. Antworte NUR mit einem JSON-Objekt ohne Markdown: {"name":"...","ingredients":["Menge Zutat", "..."],"steps":["..."],"glass":"..."}. Alle Texte auf ' + lang + '.',
        messages: [{ role: 'user', content: `Whisky: ${w.name}${w.type ? ' (Stil: ' + (TYPE_LABELS[w.type] || w.type) + ')' : ''}${w.grape ? ', Destillerie: ' + w.grape : ''}${w.age ? ', ' + w.age + ' Jahre' : ''}${w.abv ? ', ' + w.abv + ' % vol.' : ''}${w.cask ? ', Fass: ' + w.cask : ''}.` }]
      })
    });
    const data = await resp.json();
    const text = (data.content || []).filter(b => b.type === 'text').map(b => b.text).join('\n');
    const m = text.match(/\{[\s\S]*\}/);
    const j = m ? JSON.parse(m[0]) : null;
    if (!j || !j.name || !Array.isArray(j.ingredients)) { showToast(sx('rec_fail')); }
    else { aiRecipe = { name: String(j.name).slice(0, 120), ing: j.ingredients.map(String).join('\n').slice(0, 2000), steps: (Array.isArray(j.steps) ? j.steps.map(String).join(' ') : String(j.steps || '')).slice(0, 4000), gin: w.name }; }
  } catch (e) { if (!(e && (e.noCredits || e.noConsent))) showToast(sx('rec_fail')); }
  recAiBusy = false;
  renderRecipes();
}
function saveAiRecipe() {
  if (!aiRecipe) return;
  settings.recipes = (settings.recipes || []).concat(Object.assign({ id: 'r' + Date.now() }, aiRecipe));
  aiRecipe = null;
  saveRecipesData(); showToast(sx('rec_saved')); renderRecipes();
}
function renderRecipes() {
  const el = sv('recipes-content');
  if (!el) return;
  const lang = serveLang();
  const favs = new Set(settings.favRecipes || []);
  const items = wines.slice();
  const types = new Set(items.map(w => w.type));
  const all = RECIPES.map(r => ({ id: r.id, name: sxPick(r.n), ing: r.ing[lang], steps: r.steps[lang], glass: r.glass[lang], styles: r.styles, own: false }))
    .concat((settings.recipes || []).map(r => ({ id: r.id, name: r.name, ing: String(r.ing || '').split('\n').filter(Boolean), steps: r.steps, glass: '', styles: [], own: true, gin: r.gin })));
  let list = all.filter(r => recFilter === 'all' || (recFilter === 'fav' && favs.has(r.id)) || (recFilter === 'own' && r.own));
  if (recMine) list = list.filter(r => r.own || r.styles.some(s => types.has(s)));
  const chip = (id, label) => `<button class="filter-chip ${recFilter === id ? 'active' : ''}" onclick="setRecFilter('${id}')">${label}</button>`;
  const cards = list.map(r => {
    const fits = items.filter(w => r.styles.includes(w.type)).slice(0, 5).map(w => w.name);
    return `<details class="rec-card"><summary><span class="rec-name">${esc(r.name)}</span>
        <button type="button" class="rec-fav" onclick="event.preventDefault();toggleRecFav('${esc(r.id)}')" aria-label="fav">${favs.has(r.id) ? '⭐' : '☆'}</button></summary>
      ${fits.length ? `<div class="wine-region">🥃 ${esc(sx('rec_fits'))}: ${esc(fits.join(', '))}</div>` : ''}
      ${r.gin ? `<div class="wine-region">🥃 ${esc(r.gin)}</div>` : ''}
      <div class="rec-h">${esc(sx('rec_ing'))}</div><ul>${r.ing.map(x => `<li>${esc(x)}</li>`).join('')}</ul>
      <div class="rec-h">${esc(sx('rec_steps'))}</div><p>${esc(r.steps || '')}</p>
      ${r.glass ? `<div class="wine-region">🥃 ${esc(sx('rec_glass'))}: ${esc(r.glass)}</div>` : ''}
      ${r.own ? `<button type="button" class="wine-btn danger" onclick="deleteOwnRecipe('${esc(r.id)}')">🗑</button>` : ''}
    </details>`;
  }).join('');
  const herbs = settings.herbs || [];
  const shelf = Object.keys(SERVE_ING).map(id => `<button class="filter-chip ${herbs.includes(id) ? 'active' : ''}" onclick="toggleHerb('${id}')">${esc(sxPick(SERVE_ING[id]))}</button>`).join('');
  el.innerHTML = `
    <div class="filter-scroll">${chip('all', esc(sx('rec_all')))}${chip('fav', esc(sx('rec_fav')))}${chip('own', esc(sx('rec_own')))}
      <button class="filter-chip ${recMine ? 'active' : ''}" onclick="toggleRecMine()">${esc(sx('rec_mine'))}</button></div>
    <div class="rec-list">${cards || `<div class="empty-state">${esc(sx('rec_none'))}</div>`}</div>
    <div class="rec-box"><div class="stats-title">${esc(sx('rec_ai_title'))}</div>
      <select id="rec-ai-gin"><option value="">${esc(sx('rec_pick'))}</option>${items.map(w => `<option value="${esc(w.id)}">${esc(w.name)}</option>`).join('')}</select>
      <button class="scan-btn" style="margin-top:8px" onclick="createAiRecipe()">${esc(sx('rec_ai_btn'))}</button>
      ${aiRecipe ? `<div class="rec-card open"><div class="rec-name">${esc(aiRecipe.name)}</div><ul>${aiRecipe.ing.split('\n').map(x => `<li>${esc(x)}</li>`).join('')}</ul><p>${esc(aiRecipe.steps)}</p>
        <button class="wine-btn primary" onclick="saveAiRecipe()">${esc(sx('rec_save'))}</button></div>` : ''}</div>
    <div class="rec-box"><div class="stats-title">${esc(sx('rec_add_title'))}</div>
      <input id="rec-n" placeholder="${esc(sx('rec_name'))}">
      <textarea id="rec-i" rows="4" placeholder="${esc(sx('rec_ing_ph'))}"></textarea>
      <textarea id="rec-s" rows="3" placeholder="${esc(sx('rec_steps_ph'))}"></textarea>
      <button class="scan-btn" onclick="saveOwnRecipe()">${esc(sx('rec_add_btn'))}</button></div>
    <div class="rec-box"><div class="stats-title">${esc(sx('shelf_title'))}</div>
      <div class="legend-text">${esc(sx('shelf_hint'))}</div>
      <div class="shelf-chips">${shelf}</div>
      <button class="scan-btn" style="margin-top:8px" onclick="shelfMissingToWish()">${esc(sx('shelf_missing'))}</button></div>`;
}

"""Whiskey-App: Perfect-Serve-/Rezept-/Glas-Texte vom Zwei-Sprachen-Block (SX u. a.) auf das normale t()-System umstellen,
Wein-Reste in KI-Anfragen/HTML korrigieren. Voraussetzung: merge_i18n.py wurde bereits ausgefuehrt."""
import re, sys, subprocess, json, html as htmllib
sys.stdout.reconfigure(encoding='utf-8')
P = 'C:/wk/My-Whiskey-Collection/index.html'
s = open(P, encoding='utf-8').read()
size0 = len(s.encode('utf-8'))


def rep(a, b, count=1):
    global s
    c = s.count(a)
    assert c == count, (c, a[:100])
    s = s.replace(a, b)


def rx(pattern, repl, count=1, flags=re.S):
    global s
    s, n = re.subn(pattern, repl, s, flags=flags)
    assert n == count, (n, pattern[:100])


# ---------- 0) Rezept-Ids/-Stile aus der alten Tabelle merken ----------
rec = re.findall(r"\{ id: '([a-z]+)', n: \[[^\]]*\], styles: (\[[^\]]*\])", s)
assert len(rec) == 12, len(rec)
recipe_fn = "function recipeList() {\n  return [\n" + ",\n".join("    { id: '%s', styles: %s }" % (i, st) for i, st in rec) + "\n  ];\n}\n"
recipe_glass = {'oldfashioned': 'tumbler', 'manhattan': 'coupe', 'whiskysour': 'tumbler', 'highball': 'highball', 'julep': 'julep', 'penicillin': 'tumbler',
                'robroy': 'coupe', 'boulevardier': 'tumbler', 'irishcoffee': 'irishcoffee', 'rustynail': 'tumbler', 'paperplane': 'coupe', 'goldrush': 'tumbler'}
assert set(recipe_glass) == {i for i, _ in rec}, (set(recipe_glass) ^ {i for i, _ in rec})
ing_ids = re.findall(r"([a-z]+): \['[^']*', '[^']*'\]", re.search(r"const SERVE_ING = \{(.*?)\n\};", s, re.S).group(1))
assert len(ing_ids) == 14, ing_ids

# ---------- 1) Aufrufstellen umstellen ----------
n_sx = len(re.findall(r"\bsx\('", s))
s = re.sub(r"\bsx\('([A-Za-z_]+)'", r"t('sx_\1'", s)
print('sx() ->', n_sx, 'Aufrufe auf t(sx_*)')
assert len(re.findall(r"\bsx\(", s)) == 1   # nur die Definition function sx(k, vars) bleibt bis zum AST-Entfernen
rep("tips: top.map(id => ({ n: sxPick(SERVE_WAY[id].n), why: sxPick(SERVE_WAY[id].why) })),", "tips: top.map(id => ({ n: t('way_' + id + '_n'), why: t('way_' + id + '_why') })),")
rep("garnish: garn.slice(0, 4).map(id => sxPick(SERVE_ING[id])), ratio, glass, ice,", "garnish: garn.slice(0, 4).map(id => ingName(id)), ratio, glass, ice,")
rep("food: sxPick(SERVE_FOOD[food]).join(', ')", "food: t('food_' + food)")
rep("  const lang = serveLang() === 'de' ? 'Deutsch' : 'Englisch';\n  const resp = await aiFetch(AI_PROXY_URL, {\n    method: 'POST', headers: { 'Content-Type': 'application/json' },\n    body: JSON.stringify({\n      model: 'claude-sonnet-4-6', max_tokens: 800,",
    "  const lang = aiLangName();\n  const resp = await aiFetch(AI_PROXY_URL, {\n    method: 'POST', headers: { 'Content-Type': 'application/json' },\n    body: JSON.stringify({\n      model: 'claude-sonnet-4-6', max_tokens: 800,")
rep("    const lang = serveLang() === 'de' ? 'Deutsch' : 'Englisch';\n    const resp = await aiFetch(AI_PROXY_URL, {", "    const lang = aiLangName();\n    const resp = await aiFetch(AI_PROXY_URL, {")
rep("  if (!SERVE_ING[id]) return;", "  if (!serveIngIds().includes(id)) return;")
rep("    const nm = sxPick(SERVE_ING[id]);", "    const nm = ingName(id);")
rep("Object.keys(SERVE_ING).map(id => `<button class=\"filter-chip ${herbs.includes(id) ? 'active' : ''}\" onclick=\"toggleHerb('${id}')\">${esc(sxPick(SERVE_ING[id]))}</button>`).join('')",
    "serveIngIds().map(id => `<button class=\"filter-chip ${herbs.includes(id) ? 'active' : ''}\" onclick=\"toggleHerb('${id}')\">${esc(ingName(id))}</button>`).join('')")
rep("  const lang = serveLang();\n  const favs = new Set(settings.favRecipes || []);\n  const items = wines.slice();", "  const favs = new Set(settings.favRecipes || []);\n  const items = wines.slice();")
rep("const all = RECIPES.map(r => ({ id: r.id, name: sxPick(r.n), ing: r.ing[lang], steps: r.steps[lang], glass: r.glass[lang], styles: r.styles, own: false }))",
    "const all = recipeList().map(r => ({ id: r.id, name: t('rec_' + r.id + '_n'), ing: t('rec_' + r.id + '_ing').split('\\n').filter(Boolean), steps: t('rec_' + r.id + '_steps'), glass: t('rec_' + r.id + '_glass'), styles: r.styles, own: false }))")
# Glas-Karte
rep("  const lang = serveLang() === 'de' ? 'de' : 'en';\n  const [title, text] = GLASS_TXT[id][lang];\n  const more = lang === 'de' ? 'Mehr Bilder ansehen ↗' : 'See more pictures ↗';\n  const close = lang === 'de' ? 'Schließen' : 'Close';\n",
    "  const title = t('glass_' + id + '_title'), text = t('glass_' + id + '_text'), more = t('glass_more'), close = t('glass_close');\n")
rep("  const q = String(name || '').trim() + (serveLang() === 'de' ? ' Whisky Glas' : ' whisky glass');", "  const q = String(name || '').trim() + ' ' + t('glass_query');")
# alte Definitionen gleich mit entfernen lassen (AST) - Texte in eingefuegtem Block
NEW = '''// ---- Texte: normales t()-System (Schluessel sx_*, ing_*, way_*, food_*, rec_<id>_*, glass_<id>_*). Alles Funktionen, damit schon beim ersten Rendern nutzbar (keine TDZ-Falle) ----
function serveLang() { return baseLang(); }
// Sprachname (deutsch) fuer die KI-Anfragen: "Alle Texte auf <Sprache>"
function aiLangName() {
  const m = { de: 'Deutsch', en: 'Englisch', es: 'Spanisch', sv: 'Schwedisch', da: 'Dänisch', fi: 'Finnisch', ru: 'Russisch', it: 'Italienisch', fr: 'Französisch', pl: 'Polnisch', hu: 'Ungarisch', cs: 'Tschechisch', sk: 'Slowakisch', ro: 'Rumänisch', hr: 'Kroatisch', pt: 'Portugiesisch', no: 'Norwegisch', nl: 'Niederländisch', el: 'Griechisch', uk: 'Ukrainisch', ja: 'Japanisch', ko: 'Koreanisch', zh: 'Chinesisch', hi: 'Hindi' };
  return m[baseLang()] || 'Englisch';
}
function serveIngIds() { return %s; }
function ingName(id) { return t('ing_' + id); }
%s// Glas-Name -> Zeichnung. Zuerst Stichwoerter (de/en), dann die Namen aus allen Sprachbloecken, damit auch z. B. japanische Glasnamen erkannt werden
var _glassNameMap = null;
function glassId(name) {
  const n = String(name || '').toLowerCase();
  if (/glencairn|nosing|tulpe|tulip/.test(n)) return 'glencairn';
  if (/highball|longdrink|collins/.test(n)) return 'highball';
  if (/coupe|schale|martini/.test(n)) return 'coupe';
  if (/julep|becher|cup/.test(n) && !/kaffee|coffee/.test(n)) return 'julep';
  if (/henkel|irish|coffee|kaffee/.test(n)) return 'irishcoffee';
  if (/tumbler|rocks|old.?fashioned|whisky.?glas|whiskey.?glas|whisky glass/.test(n)) return 'tumbler';
  if (n.length < 2) return null;
  if (!_glassNameMap) {
    _glassNameMap = new Map();
    const recGlass = %s;
    const ids = ['glencairn', 'tumbler', 'highball', 'coupe', 'julep', 'irishcoffee'];
    Object.keys(I18N).forEach(l => {
      const b = I18N[l] || {};
      ids.forEach(id => { [b['glass_' + id + '_title'], b['sx_glass_' + id]].forEach(v => { const x = String(v || '').trim().toLowerCase(); if (x) _glassNameMap.set(x, id); }); });
      Object.keys(recGlass).forEach(r => { const x = String(b['rec_' + r + '_glass'] || '').trim().toLowerCase(); if (x && !_glassNameMap.has(x)) _glassNameMap.set(x, recGlass[r]); });
    });
  }
  if (_glassNameMap.has(n)) return _glassNameMap.get(n);
  for (const [x, id] of _glassNameMap) { if (x.length >= 3 && (n.includes(x) || (n.length >= 3 && x.includes(n)))) return id; }
  return null;
}
function glassViewText() { return t('sx_glass_view'); }
''' % (json.dumps(ing_ids), recipe_fn, json.dumps(recipe_glass))
# Einfuegen vor der Regel-Tabelle
anchor = "// ---- Regeln: Stichwort in Name/Destillerie/Fass/Region -> Genussarten, Garnitur, Speisen ----\n"
rep(anchor, NEW + anchor)
# serveIngId ueber alle Sprachen
rx(r"function serveIngId\(name\) \{.*?\n\}\n", "function serveIngId(name) {   // Name -> Id ueber die Namen aller Sprachen (Garnitur kann in einer anderen Sprache gespeichert worden sein)\n"
   "  const n = String(name || '').trim().toLowerCase();\n  if (!n) return null;\n  const langs = Object.keys(I18N);\n"
   "  return serveIngIds().find(id => langs.some(l => { const x = String((I18N[l] && I18N[l]['ing_' + id]) || '').toLowerCase(); return x && (x === n || n.includes(x) || x.includes(n)); })) || null;\n}\n")
open(P, 'w', encoding='utf-8', newline='').write(s)

# ---------- 2) alte Zwei-Sprachen-Tabellen und Hilfen per AST entfernen ----------
NAMES = 'SX,sx,sxPick,serveLang,SERVE_ING,SERVE_WAY,SERVE_FOOD,RECIPES,GLASS_TXT,glassViewText,glassId'
# serveLang/glassId/glassViewText gibt es jetzt doppelt (alt + neu): nur die ALTEN entfernen -> alte zuerst umbenennen
s = open(P, encoding='utf-8').read()
s = s.replace("function serveLang() { return baseLang() === 'de' ? 'de' : 'en'; }", "function serveLang__old() {}")
assert "function serveLang__old()" in s
# alte glassViewText / glassId: die neuen stehen im eingefuegten Block, die alten kommen spaeter im Text -> alte per Marker umbenennen
cnt_g = s.count("function glassViewText()")
assert cnt_g == 2, cnt_g
i_first = s.index("function glassViewText()")
i_second = s.index("function glassViewText()", i_first + 10)
s = s[:i_second] + "function glassViewText__old()" + s[i_second + len("function glassViewText()"):]
cnt_i = s.count("function glassId(name)")
assert cnt_i == 2, cnt_i
j_first = s.index("function glassId(name)")
j_second = s.index("function glassId(name)", j_first + 10)
s = s[:j_second] + "function glassId__old(name)" + s[j_second + len("function glassId(name)"):]
open(P, 'w', encoding='utf-8', newline='').write(s)
NAMES = 'SX,sx,sxPick,serveLang__old,SERVE_ING,SERVE_WAY,SERVE_FOOD,RECIPES,GLASS_TXT,glassViewText__old,glassId__old'
r = subprocess.run(['node', 'C:/wk/My-Whiskey-Collection/_tools/ast_tool.mjs', P, 'remove', NAMES], capture_output=True, text=True, encoding='utf-8')
print('AST-Entfernen:', r.stdout.strip(), r.stderr.strip())
s = open(P, encoding='utf-8').read()

# ---------- 3) Wein-Reste in KI-Anfragen / Texten ----------
rep("land (Herkunftsland auf Deutsch oder null)", "land (Herkunftsland auf ${aiLangName()} oder null)")
rep("bevorzugt Wikipedia, die Seite des Weinguts oder ein Wein-Shop/Vivino;", "bevorzugt Wikipedia, die Seite der Destillerie oder ein Whisky-Shop;")
rep("`Wein: ${name}${year ? ' (Jahrgang ' + year + ')' : ''}. Nenne Typ, Region, Land, Hauptrebsorte, den aktuellen Durchschnittspreis",
    "`Whisky: ${name}${year ? ' (Abfüllung/Jahr ' + year + ')' : ''}. Nenne Typ, Region, Land, Destillerie, Alter, Alkoholgehalt, Fass, den aktuellen Durchschnittspreis")
rx(r"land \(Herkunftsland auf Deutsch, z\.B\. Schottland, oder null\)", "land (Herkunftsland auf ' + aiLangName() + ', z.B. Schottland, oder null)", count=2)
rx(r"passend zu Weinart und Rebsorte, oder null\)", "passend zu Whisky-Stil und Destillerie, oder null)", count=1)
rep("'Welcher Wein ist auf diesem Etikett zu sehen?'", "'Welcher Whisky ist auf diesem Etikett zu sehen?'")
rep("Stimmt der Jahrgang nicht oder ist der Preis nur für Kartons/Magnums, das kurz in \"note\" schreiben (z. B. \"Jahrgang 2019\", \"zzgl. Versand\")",
    "Stimmt Abfüllung oder Alter nicht oder ist der Preis nur für Kartons/Sets, das kurz in \"note\" schreiben (z. B. \"12 Jahre\", \"zzgl. Versand\")")
rep("`Wein: ${w.name}${w.year && !w.name.includes(String(w.year)) ? ' ' + w.year : ''}", "`Whisky: ${w.name}${w.year && !w.name.includes(String(w.year)) ? ' ' + w.year : ''}")
rep("The number is still saved with the wine so the bottle is recognized next time.", "The number is still saved with the whisky so the bottle is recognized next time.")
# ---------- 4) HTML: tote Reste + statische Texte an den de-Block angleichen ----------
rep('<option value="ripeness" hidden disabled data-i18n="sort_ripeness">↕ Trinkreife (dringendste zuerst)</option>\n', "") if '<option value="ripeness" hidden disabled' in s else None
rx(r"<!-- ═+\n\s*TRINKREIFE TAB\n═+ -->\n", "", count=1) if re.search(r"TRINKREIFE TAB", s) else None
i0 = s.index('const I18N = {')
j0 = s.index('\n};', s.index('\nzh:', i0))
m_de = re.search(r'\nde: \{\n(.*?)\n\},\n', s[i0:j0 + 5], re.S)
de_vals = {}
for line in m_de.group(1).split('\n'):
    mm = re.match(r'^\s+([A-Za-z_0-9]+): (".*"),?$', line)
    if mm:
        try:
            de_vals[mm.group(1)] = json.loads(mm.group(2))
        except Exception:
            pass
msc = re.search(r'<script(?![^>]*src)[^>]*>', s)
head_html, rest_html = s[:msc.start()], s[msc.start():]
changed = []


def sync_text(m):
    attrs, key, inner = m.group(2), m.group(3), m.group(4)
    v = de_vals.get(key)
    if v is None or '<' in inner or '{' in inner:
        return m.group(0)
    if htmllib.unescape(inner).strip() == v.strip():
        return m.group(0)
    if '<' in v or '\n' in v:
        return m.group(0)
    changed.append((key, inner.strip()[:40], v[:40]))
    return '<%s%s>%s</%s>' % (m.group(1), attrs, htmllib.escape(v, quote=False), m.group(1)) if False else m.group(0).replace('>' + inner + '</', '>' + htmllib.escape(v, quote=False) + '</', 1)


head_html = re.sub(r'<(button|label|div|span|summary|h1|h2|h3|p|option|b|strong|a)\b([^>]*\bdata-i18n="([A-Za-z_0-9]+)"[^>]*)>([^<>]*)</\1>', sync_text, head_html)


def sync_ph(m):
    tag = m.group(0)
    key = re.search(r'data-i18n-ph="([A-Za-z_0-9]+)"', tag).group(1)
    v = de_vals.get(key)
    pm = re.search(r'placeholder="([^"]*)"', tag)
    if v is None or not pm or htmllib.unescape(pm.group(1)) == v:
        return tag
    changed.append((key, pm.group(1)[:40], v[:40]))
    return tag.replace(pm.group(0), 'placeholder="%s"' % htmllib.escape(v, quote=True))


head_html = re.sub(r'<(?:input|textarea)\b[^>]*data-i18n-ph="[A-Za-z_0-9]+"[^>]*>', sync_ph, head_html)
s = head_html + rest_html
print('HTML-Defaulttexte an de-Block angeglichen:', len(changed))
for c in changed[:40]:
    print('  ', c)
open(P, 'w', encoding='utf-8', newline='').write(s)
c = re.findall(r'<script(?![^>]*src)[^>]*>(.*?)</script>', s, flags=re.S)[0]
open('C:/Users/tknec/AppData/Local/Temp/chk.js', 'w', encoding='utf-8').write(c)
rr = subprocess.run(['node', '--check', 'C:/Users/tknec/AppData/Local/Temp/chk.js'], capture_output=True, text=True)
print('syntax', rr.returncode, rr.stderr[:400])
print('Bytes', size0, '->', len(s.encode('utf-8')))

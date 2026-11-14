"""Stufe 1: toten Code der Whiskey-App entfernen (Trinkreife-Reiter, Trinkfenster, Regal-Blinken, Vivino-Zweig).
Beibehalten: Serviertemperatur (auf den Karten sichtbar), lvlDrink (wird per onclick-Zeichenkette genutzt), alles zu Trinken/Historie."""
import re, sys, subprocess, json
sys.stdout.reconfigure(encoding='utf-8')
P = 'C:/wk/My-Whiskey-Collection/index.html'
s = open(P, encoding='utf-8').read()
size0 = len(s.encode('utf-8')); lines0 = s.count('\n') + 1


def rep(a, b, count=1):
    global s
    c = s.count(a)
    assert c == count, (c, a[:100])
    s = s.replace(a, b)


def rx(pattern, repl, count=1, flags=re.S):
    global s
    s, n = re.subn(pattern, repl, s, flags=flags)
    assert n == count, (n, pattern[:100])


# ---------- Verweise in behaltenem Code ----------
rep("  else if (a.id === 'tab-trinkreife') renderTrinkreife();\n", "")
rep("    if (active.id === 'tab-trinkreife') renderTrinkreife();\n", "")
rep("(name === 'keller' || name === 'trinkreife') ? 'flex' : 'none'", "name === 'keller' ? 'flex' : 'none'")
rep("  if (name === 'trinkreife') renderTrinkreife();\n", "")
rep("  if (active && active.id === 'tab-trinkreife') renderTrinkreife();\n  else if (active && active.id === 'tab-racks')", "  if (active && active.id === 'tab-racks')")
# cleanWine
rep("  const dw = fixDrinkWindow(yearV, w.type, w.grape, cleanInt(w.drinkFrom, 1000, 2300), cleanInt(w.drinkTo, 1000, 2300));\n", "")
rep("    drinkFrom: dw.from, drinkTo: dw.to,\n", "")
# Lookup: ruleFrom/drinkYearOk
rep("    const y = parseInt(year);\n    if (info && drinkYearOk(y)) info.drinkFrom = ruleFrom(y, info.drinkFrom);\n", "")
# Lookup-/Auto-Lookup-Felder (kommt zweimal vor)
rep("    setIfEmpty('f-drink-from', info.drinkFrom);\n    setIfEmpty('f-drink-to', info.drinkTo);\n    fixFormDrinkWindow();\n", "", count=2)
rep("info.grape || info.drinkFrom || info.drinkTo || info.tempFrom != null", "info.grape || info.tempFrom != null")
rep("function onVintageInput() { autoFillDrinkWindow(); maybeAutoLookup(); }", "function onVintageInput() { maybeAutoLookup(); }")
rep("document.getElementById('f-grape').addEventListener('change', autoFillDrinkWindow);\n", "")
rep("document.getElementById('f-type').addEventListener('change', autoFillDrinkWindow);\n", "")
# Enrich
rep("!w.grape || !w.drinkFrom || !w.drinkTo || w.tempFrom == null || !w.price", "!w.grape || w.tempFrom == null || !w.price", count=2)
rx(r"            if \(!w\.drinkFrom && info\.drinkFrom\) \{[^\n]*\n            if \(!w\.drinkTo && info\.drinkTo\) \{[^\n]*\n            \{ const fx = fixDrinkWindow\([^\n]*\n", "")
rep("await resolveWineImage(info, wineCriteria(w), { noVivino: true })", "await resolveWineImage(info, wineCriteria(w))")
rep("            // Falls Vivino kein Bild hatte: KI-Direktbild / og:image als Rückfall (mit jetzt ggf. ergänzten Kriterien)\n", "            // KI-Direktbild / og:image (mit jetzt ggf. ergänzten Kriterien)\n")
# Bildaufloesung ohne Vivino
rx(r"  const viv = \(meta && meta\.noVivino\) \? null : await vivinoImageFor\(crit, meta\);\n  if \(viv\) \{[^\n]*\n", "")
# Formular laden/leeren/speichern
rep("  document.getElementById('f-drink-from').value = w.drinkFrom||'';\n  document.getElementById('f-drink-to').value = w.drinkTo||'';\n", "")
rep("  autoDrink = { from: null, to: null };\n", "")
rep("'f-note','f-drink-from','f-drink-to',", "'f-note',")
rep("    drinkFrom: parseInt(document.getElementById('f-drink-from').value)||null,\n    drinkTo: parseInt(document.getElementById('f-drink-to').value)||null,\n", "")
rep("'locPlatz','drinkFrom','drinkTo','tempFrom'", "'locPlatz','tempFrom'")
# Etikett-Scan
rep("    { const yy = parseInt(document.getElementById('f-year').value); const df = ruleFrom(yy, info.drinkFrom); if (df) document.getElementById('f-drink-from').value = df; }\n    if (info.drinkTo) document.getElementById('f-drink-to').value = info.drinkTo;\n    fixFormDrinkWindow();\n", "")
rep("showToast(info.drinkFrom || info.drinkTo ? t('toast_label_ripe') : t('toast_label'));", "showToast(t('toast_label'));")
# Import
rep("    drinkFrom: col('trinken ab'), drinkTo: col('trinken bis'), note: col('notiz')", "    note: col('notiz')")
rep("      drinkFrom: get(cols, 'drinkFrom'), drinkTo: get(cols, 'drinkTo'), note: get(cols, 'note')", "      note: get(cols, 'note')")
# KI-Anfragen: Trinkfenster-Felder entfallen
rep("drinkFrom (Jahr als Zahl oder null), drinkTo (Jahr als Zahl oder null), ", "")
rep(", ein geschätztes Trinkfenster,", ",")
rx(r"drinkFrom \(Jahr als Zahl, ab dem der Wein.*?oder null\), (tempFrom und tempTo \(.*?oder null\)\.) drinkFrom/drinkTo sind.*?nach drinkFrom\. ", r"\1 ")
# Einstellungen: Blinken
rep("blinkUrgent:false, blinkOver:false, blinkPeak:false, blinkOptimal:false, ", "")
rep("'tempUnit', 'blinkUrgent', 'blinkOver', 'blinkPeak', 'blinkOptimal']", "'tempUnit']")
rep("  ['blinkUrgent', 'blinkOver', 'blinkPeak', 'blinkOptimal'].forEach(k => { if (typeof p[k] === 'boolean') o[k] = p[k]; });\n", "")
rx(r"(settings\.racks = cleanRacks\(settings\.racks\);\n)", r"\1['blinkUrgent', 'blinkOver', 'blinkPeak', 'blinkOptimal'].forEach(k => { delete settings[k]; });   // frühere Blink-Einstellungen aus gespeicherten Daten entfernen\n")
# renderKeller: Sortierung 'ripeness', Reife-Balken
rx(r"  else if \(sortMode === 'ripeness'\) \{\n    const rmap = new Map.*?\n    \}\);\n  \}\n", "")
rep("    const ripe = getRipenessInfo(w);\n", "")
rx(r"      \$\{ripe \? `\n      <div class=\"wine-ripeness\">\n        <div class=\"wine-ripeness-bar \$\{ripe\.cls\}\" style=\"width:\$\{ripe\.pct\}%\"></div>\n      </div>` : ''\}\n", "")
# Statistik
rep("    ${statsRipeHtml()}\n", "")
# Regal: Blink-Schalter, Ripeness-Punkte, Legende
rx(r"  // Trinkreife-Punkt an jeder Flasche; auf Wunsch blinken Weine nach Trinkreife \(jede Gruppe einzeln wählbar\)\n  const BLINKS = .*?  const sw = rackStoreFilter", "  const sw = rackStoreFilter")
rx(r"<div class=\"rack-toolbar\"><span class=\"rack-toolbar-lbl\">\$\{t\('rack_blink_lbl'\)\}</span>`\n    \+ BLINKS\.map\(.*?\.join\(''\)\n    \+ `</div>`\n    \+ \(blinkOn\.Urgent \? [^\n]*\n    \+ `<div class=\"rack-box\$\{blink \? ' blink-on' : ''\}\">", "`\n    + `<div class=\"rack-box\">")
rx(r"        let topKey = null, urgent = false;[^\n]*\n        entries\.forEach\(x => \{ const ri = ripeInfo[^\n]*\n        const dot = topKey [^\n]*\n", "")
rep("${urgent ? ' blinking' : ''}", "")
rep("${badge}${dot}</div>", "${badge}</div>")
rx(r"  html \+= `<div class=\"rack-legend\">`[^\n]*\n", "")
rep(".rack-slot.moving > :not(.rack-ripe):not(.rack-slot-count) { opacity: .55; }", ".rack-slot.moving > :not(.rack-slot-count) { opacity: .55; }")
# ---------- HTML ----------
rx(r"<div class=\"tab\" id=\"tab-trinkreife\">.*?<div id=\"trinkreife-list\"></div>\n</div>\n\n", "")
rx(r"      <div class=\"export-card\" id=\"drinkrule-btn\".*?      </div>\n      </div>\n(?=      <div id=\"enrich-progress\")", "")
rx(r"    <div class=\"form-row\" style=\"display:none\">\n      <div class=\"form-group\">\n        <label data-i18n=\"l_from\">.*?<input id=\"f-drink-to\" placeholder=\"\" type=\"number\">\n      </div>\n    </div>\n", "")
open(P, 'w', encoding='utf-8', newline='').write(s)
print('Stufe 1 Text/HTML fertig')

# ---------- Funktionen/Konstanten per AST entfernen ----------
NAMES = ('renderTrinkreife,setRipeFilterType,setRipeFilterStatus,setRipeFilterCountry,ripeStatusKey,ripeOverdue,ripeInfo,getRipenessInfo,goToRipeStatus,statsRipeHtml,'
         'fixDrinkWindow,maturationOffset,MATURATION_GRAPE,MATURATION_GRAPE_WINE,MATURATION_TYPE,autoDrink,recalcDrinkWindows,fixFormDrinkWindow,autoFillDrinkWindow,'
         'drinkYearOk,ruleFrom,toggleRackBlink,RIPE_PRIO,RIPE_CLASS,ripeFilterType,ripeFilterStatus,ripeFilterCountry,vivinoImageFor,wineNameMatches,NAME_STOP,NAME_GRAPES')
r = subprocess.run(['node', 'C:/wk/My-Whiskey-Collection/_tools/ast_tool.mjs', P, 'remove', NAMES], capture_output=True, text=True, encoding='utf-8')
print(r.stdout.strip(), r.stderr.strip())
s2 = open(P, encoding='utf-8').read()
print('Zeilen', lines0, '->', s2.count('\n') + 1, '| Bytes', size0, '->', len(s2.encode('utf-8')))

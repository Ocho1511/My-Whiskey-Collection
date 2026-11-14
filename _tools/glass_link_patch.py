import re, sys, subprocess
sys.stdout.reconfigure(encoding='utf-8')
P = 'C:/wk/My-Whiskey-Collection/index.html'
s = open(P, encoding='utf-8').read()


def rep(a, b, count=1):
    global s
    c = s.count(a)
    assert c == count, (c, a[:90])
    s = s.replace(a, b)


# 1) Formular: Link unter den Feldern + oninput am Glas-Feld
rep('<input id="f-serve-glass" type="text">', '<input id="f-serve-glass" type="text" oninput="serveGlassLink()">')
rep('<div class="form-group"><label data-i18n="serve_ice">Eis</label><input id="f-serve-ice" type="text"></div>\n      </div>',
    '<div class="form-group"><label data-i18n="serve_ice">Eis</label><input id="f-serve-ice" type="text"></div>\n      </div>\n'
    '      <a id="serve-glass-link" class="glass-link" href="#" target="_blank" rel="noopener" style="display:none"></a>')

# 2) Link nach dem Setzen des Glas-Felds aktualisieren (Laden eines Whiskys und Empfehlung uebernehmen)
rep("  if (sv('f-serve-glass')) sv('f-serve-glass').value = s.glass || '';", "  if (sv('f-serve-glass')) sv('f-serve-glass').value = s.glass || '';\n  serveGlassLink();")
rep("  if (sv('f-serve-glass')) sv('f-serve-glass').value = r.glass || '';", "  if (sv('f-serve-glass')) sv('f-serve-glass').value = r.glass || '';\n  serveGlassLink();")

# 3) Karte: Glas als Link
rep("  return (a ? `<div class=\"wine-region\" style=\"margin-top:4px\">🥃 ${esc(a)}${s.ratio ? ' (' + esc(s.ratio) + ')' : ''}</div>` : '') + b;\n}",
    "  const g = s.glass ? `<div class=\"wine-region\" style=\"margin-top:2px\">🥃 ${glassLinkHtml(s.glass)}</div>` : '';\n"
    "  return (a ? `<div class=\"wine-region\" style=\"margin-top:4px\">🥃 ${esc(a)}${s.ratio ? ' (' + esc(s.ratio) + ')' : ''}</div>` : '') + g + b;\n}\n"
    "// Glas ansehen: Bildersuche zum Glas (die meisten wissen nicht, wie z. B. ein Glencairn-Glas aussieht)\n"
    "function glassUrl(name) {\n"
    "  const q = String(name || '').trim() + (serveLang() === 'de' ? ' Whisky Glas' : ' whisky glass');\n"
    "  return 'https://www.google.com/search?tbm=isch&q=' + encodeURIComponent(q);\n"
    "}\n"
    "function glassLinkHtml(name) {\n"
    "  return `<a class=\"glass-link\" href=\"${glassUrl(name)}\" target=\"_blank\" rel=\"noopener\" onclick=\"event.stopPropagation()\">${esc(name)} · ${esc(sx('glass_view'))} ↗</a>`;\n"
    "}\n"
    "function serveGlassLink() {\n"
    "  const a = sv('serve-glass-link'), v = sv('f-serve-glass') ? sv('f-serve-glass').value.trim() : '';\n"
    "  if (!a) return;\n"
    "  if (!v) { a.style.display = 'none'; return; }\n"
    "  a.href = glassUrl(v); a.textContent = '🔍 ' + sx('glass_view') + ': ' + v + ' ↗'; a.style.display = 'inline-block';\n"
    "}")

# 4) Rezepte: Glas als Link
rep("${r.glass ? `<div class=\"wine-region\">🥃 ${esc(sx('rec_glass'))}: ${esc(r.glass)}</div>` : ''}",
    "${r.glass ? `<div class=\"wine-region\">🥃 ${esc(sx('rec_glass'))}: ${glassLinkHtml(r.glass)}</div>` : ''}")

# 5) Texte (SX de/en) + CSS
rep("    glass_glencairn: 'Glencairn-Glas',", "    glass_view: 'Glas ansehen',\n    glass_glencairn: 'Glencairn-Glas',")
rep("    glass_glencairn: 'Glencairn glass',", "    glass_view: 'See the glass',\n    glass_glencairn: 'Glencairn glass',")
s = s.replace('</style>', '.glass-link { color: var(--gold); font-size: 13px; font-weight: 600; text-decoration: underline; text-underline-offset: 3px; margin: 2px 0 8px; }\n</style>', 1)
open(P, 'w', encoding='utf-8', newline='').write(s)
c = re.findall(r'<script(?![^>]*src)[^>]*>(.*?)</script>', s, flags=re.S)[0]
open('C:/Users/tknec/AppData/Local/Temp/chk.js', 'w', encoding='utf-8').write(c)
print('syntax', subprocess.run(['node', '--check', 'C:/Users/tknec/AppData/Local/Temp/chk.js'], capture_output=True, text=True).returncode)

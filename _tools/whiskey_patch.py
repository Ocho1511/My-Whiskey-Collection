import re, json, sys, subprocess
sys.stdout.reconfigure(encoding='utf-8')
P = 'C:/wk/My-Whiskey-Collection/index.html'
s = open(P, encoding='utf-8').read()


def rep(a, b, count=1):
    global s
    c = s.count(a)
    assert c == count, (c, a[:90])
    s = s.replace(a, b)


block = open('C:/wk/My-Whiskey-Collection/_tools/whiskey_block.js', encoding='utf-8').read()

# 1) code block before splashInit()
rep('\nsplashInit();', '\n' + block + '\nsplashInit();')

# 2) data model + settings + sync
rep("email:'', font:'inter'}, safeParse(SETTINGS_KEY, {}));",
    "email:'', font:'inter', recipes:[], favRecipes:[], herbs:[]}, safeParse(SETTINGS_KEY, {}));\nsettings.recipes = cleanRecipes(settings.recipes); settings.favRecipes = cleanIdList(settings.favRecipes); settings.herbs = cleanIdList(settings.herbs);")
rep("  return { dv: 3, wines, wishes, drunkWines, racks: settings.racks || [], cellars: settings.cellars || [], owner: settings.owner || '', prefs: collectPrefs() };",
    "  return { dv: 3, wines, wishes, drunkWines, racks: settings.racks || [], cellars: settings.cellars || [], owner: settings.owner || '', prefs: collectPrefs(), recipes: settings.recipes || [], favRecipes: settings.favRecipes || [], herbs: settings.herbs || [] };")
rep("  settings.owner = cleanStr(d.owner, 60);\n  persistAll();\n  adoptPrefs(d.prefs);",
    "  settings.owner = cleanStr(d.owner, 60);\n  settings.recipes = cleanRecipes(d.recipes); settings.favRecipes = cleanIdList(d.favRecipes); settings.herbs = cleanIdList(d.herbs);\n  persistAll();\n  adoptPrefs(d.prefs);")
rep("  if (!settings.owner && d.owner) settings.owner = cleanStr(d.owner, 60);\n  persistAll();\n}",
    "  if (!settings.owner && d.owner) settings.owner = cleanStr(d.owner, 60);\n  settings.recipes = mergeById(settings.recipes || [], cleanRecipes(d.recipes));\n  settings.favRecipes = cleanIdList((settings.favRecipes || []).concat(d.favRecipes || []));\n  settings.herbs = cleanIdList((settings.herbs || []).concat(d.herbs || []));\n  persistAll();\n}")
rep("    ...cleanTemps(w),\n", "    ...cleanTemps(w),\n    serve: cleanServe(w.serve),\n")

# 3) form HTML: Perfect Serve group before the storage-location group
rep('''    <div class="form-group">
      <label data-i18n="l_location">''', '''    <div class="form-group" id="serve-group">
      <label data-i18n="serve_title">Perfect Serve (Genuss, Mixer, Speisen)</label>
      <div class="serve-btns">
        <button type="button" class="wine-btn" onclick="serveFill('rules')" data-i18n="serve_rules_btn">🥃 Regel-Empfehlung</button>
        <button type="button" class="wine-btn primary" onclick="serveFill('ai')" data-i18n="serve_ai_btn">🤖 KI-Empfehlung</button>
      </div>
      <div id="serve-reco"></div>
      <input id="f-serve-garnish" type="text" oninput="serveRenderReco()" data-i18n-ph="serve_garnish_ph" placeholder="Mixer und Garnitur, mit Komma getrennt">
      <div class="form-row" style="margin-top:8px">
        <div class="form-group"><label data-i18n="serve_ratio">Wasser / Mischung</label><input id="f-serve-ratio" type="text"></div>
        <div class="form-group"><label data-i18n="serve_glass">Glas</label><input id="f-serve-glass" type="text"></div>
        <div class="form-group"><label data-i18n="serve_ice">Eis</label><input id="f-serve-ice" type="text"></div>
      </div>
      <label data-i18n="serve_food">Passende Speisen</label>
      <input id="f-serve-food" type="text">
    </div>
    <div class="form-group">
      <label data-i18n="l_location">''')

# 4) form load / clear / save / merge
rep("  document.getElementById('f-cask').value = w.cask||'';\n", "  document.getElementById('f-cask').value = w.cask||'';\n  serveWriteForm(w.serve);\n")
rep("'f-photo'].forEach(id => document.getElementById(id).value = '');", "'f-photo'].forEach(id => document.getElementById(id).value = '');\n  serveWriteForm(null);")
rep("    cask: document.getElementById('f-cask').value.trim()||null,\n", "    cask: document.getElementById('f-cask').value.trim()||null,\n    serve: serveReadForm(),\n")
rep("['region','country','grape','age','abv','cask',", "['region','country','grape','age','abv','cask','serve',")

# 5) card line
rep("<div class=\"wine-year\">${w.year||''} ${w.grape?'· '+esc(w.grape):''}</div>", "<div class=\"wine-year\">${w.year||''} ${w.grape?'· '+esc(w.grape):''}</div>${serveCardLine(w)}")

# 6) navigation: the hidden Trinkreife button becomes Rezepte
m = re.search(r'<button class="nav-btn" onclick="showTab\(\'trinkreife\',this\)" style="display:none" hidden>\s*<span class="nav-icon">[^<]*</span><span data-i18n="nav_ripe">[^<]*</span>', s)
assert m, 'nav'
s = s.replace(m.group(0), '<button class="nav-btn" onclick="showTab(\'rezepte\',this)">\n    <span class="nav-icon">🍹</span><span data-i18n="nav_recipes">Rezepte</span>')
rep('<div class="tab" id="tab-trinkreife">', '''<div class="tab" id="tab-rezepte">
  <div class="page-header">
    <h1 data-i18n="nav_recipes">Rezepte</h1>
    <div class="subtitle" data-i18n="rec_subtitle">Klassiker und Cocktails</div>
  </div>
  <div id="recipes-content"></div>
</div>

<div class="tab" id="tab-trinkreife">''')
rep("  if (name === 'trinkreife') renderTrinkreife();\n", "  if (name === 'trinkreife') renderTrinkreife();\n  if (name === 'rezepte') renderRecipes();\n")
rep("  else if (a.id === 'tab-trinkreife') renderTrinkreife();\n", "  else if (a.id === 'tab-trinkreife') renderTrinkreife();\n  else if (a.id === 'tab-rezepte') renderRecipes();\n")

# 7) CSS (first </style> only)
s = s.replace('</style>', '''.serve-btns { display: flex; gap: 8px; margin-bottom: 8px; flex-wrap: wrap; }
.serve-btns .wine-btn { flex: 1; width: auto; }
.serve-tip { display: flex; align-items: center; gap: 8px; flex-wrap: wrap; margin: 6px 0; }
.serve-why { font-size: 12px; color: var(--text-muted); flex: 1; min-width: 120px; }
.serve-shelf { font-size: 12px; color: var(--text-muted); margin: 6px 0; }
.rec-list { padding: 0 16px; display: flex; flex-direction: column; gap: 10px; }
.rec-card { background: var(--card); border: 1px solid var(--border); border-radius: 14px; padding: 12px 14px; }
.rec-card summary { cursor: pointer; display: flex; justify-content: space-between; align-items: center; gap: 8px; list-style: none; }
.rec-card summary::-webkit-details-marker { display: none; }
.rec-name { font-family: var(--heading-font, 'Playfair Display', serif); font-size: 16px; }
.rec-fav { background: none; border: none; font-size: 20px; cursor: pointer; color: var(--gold); }
.rec-h { font-weight: 700; font-size: 12px; margin-top: 10px; color: var(--text-muted); text-transform: uppercase; letter-spacing: .5px; }
.rec-card ul { margin: 4px 0 4px 18px; padding: 0; font-size: 14px; }
.rec-card p { font-size: 14px; margin: 4px 0; }
.rec-box { margin: 16px; padding: 14px; background: var(--card); border: 1px solid var(--border); border-radius: 14px; }
.rec-box input, .rec-box textarea, .rec-box select { width: 100%; margin-top: 8px; box-sizing: border-box; }
.shelf-chips { display: flex; flex-wrap: wrap; gap: 6px; margin-top: 6px; }
.legend-text { font-size: 12px; color: var(--text-muted); }
</style>''', 1)

# 8) i18n (de + en; all other languages fall back to en)
DE = {'nav_recipes': 'Rezepte', 'rec_subtitle': 'Klassiker und Cocktails', 'serve_title': 'Perfect Serve (Genuss, Mixer, Speisen)',
      'serve_rules_btn': '🥃 Regel-Empfehlung', 'serve_ai_btn': '🤖 KI-Empfehlung', 'serve_garnish_ph': 'Mixer und Garnitur, mit Komma getrennt',
      'serve_ratio': 'Wasser / Mischung', 'serve_glass': 'Glas', 'serve_ice': 'Eis', 'serve_food': 'Passende Speisen'}
EN = {'nav_recipes': 'Recipes', 'rec_subtitle': 'Classics and cocktails', 'serve_title': 'Perfect serve (way to enjoy, mixers, food)',
      'serve_rules_btn': '🥃 Rule-based tip', 'serve_ai_btn': '🤖 AI recommendation', 'serve_garnish_ph': 'Mixers and garnish, comma separated',
      'serve_ratio': 'Water / ratio', 'serve_glass': 'Glass', 'serve_ice': 'Ice', 'serve_food': 'Food pairing'}
out = []
for l in s.split('\n'):
    out.append(l)
    if l == 'de: {':
        out += ['  %s: %s,' % (k, json.dumps(v, ensure_ascii=False)) for k, v in DE.items()]
    elif l == 'en: {':
        out += ['  %s: %s,' % (k, json.dumps(v, ensure_ascii=False)) for k, v in EN.items()]
s = '\n'.join(out)
open(P, 'w', encoding='utf-8', newline='').write(s)

c = re.findall(r'<script(?![^>]*src)[^>]*>(.*?)</script>', s, flags=re.S)[0]
open('C:/Users/tknec/AppData/Local/Temp/w2_s0.js', 'w', encoding='utf-8').write(c)
r = subprocess.run(['node', '--check', 'C:/Users/tknec/AppData/Local/Temp/w2_s0.js'], capture_output=True, text=True, encoding='utf-8')
print('syntax', r.returncode, r.stderr[:500])

"""Stufe 2: CSS der entfernten Funktionen, verwaiste Sprachschluessel, 'Last Build'."""
import re, sys, subprocess, json
sys.stdout.reconfigure(encoding='utf-8')
P = 'C:/wk/My-Whiskey-Collection/index.html'
s = open(P, encoding='utf-8').read()
size0 = len(s.encode('utf-8'))


def rep(a, b, count=1):
    global s
    c = s.count(a)
    assert c == count, (c, a[:100])
    s = s.replace(a, b)


# --- Rest-Satz in der KI-Anfrage + TEMP_GRAPE ---
rep(" Das Trinkfenster beginnt nie vor dem Jahrgang, und drinkTo liegt immer nach drinkFrom.", "")
open(P, 'w', encoding='utf-8', newline='').write(s)
r = subprocess.run(['node', 'C:/wk/My-Whiskey-Collection/_tools/ast_tool.mjs', P, 'remove', 'TEMP_GRAPE'], capture_output=True, text=True, encoding='utf-8')
print('TEMP_GRAPE:', r.stdout.strip(), r.stderr.strip())
s = open(P, encoding='utf-8').read()

# --- CSS ---
FEATURE = re.compile(r'ripe|ripeness|seg-|blink|rt-dot|rack-toggle|rack-legend|rack-toolbar|trinkreife|drinkrule|wine-ripeness|rackDot|rackBlink')
style_blocks = list(re.finditer(r'(<style[^>]*>)(.*?)(</style>)', s, re.S))
css_all = '\n'.join(m.group(2) for m in style_blocks)
text_wo_css = s
for m in style_blocks:
    text_wo_css = text_wo_css.replace(m.group(2), '')


def used_elsewhere(name):
    return re.search(r'(?<![A-Za-z0-9_-])' + re.escape(name) + r'(?![A-Za-z0-9_-])', text_wo_css) is not None


css_no_comments = re.sub(r'/\*.*?\*/', '', css_all, flags=re.S)
classes = set(re.findall(r'\.([A-Za-z][A-Za-z0-9_-]*)', css_no_comments))
ids = set(re.findall(r'#([A-Za-z][A-Za-z0-9_-]*)(?=[\s\.\{:,>\[+~)])', css_no_comments))
dead = {c for c in classes if FEATURE.search(c) and not used_elsewhere(c)} | {i for i in ids if FEATURE.search(i) and not used_elsewhere(i)}
all_dead_generic = sorted(c for c in classes if not used_elsewhere(c) and not c.startswith(('show', 'active')))
print('tote Feature-Klassen/IDs:', sorted(dead))


def split_top(sel, sep=','):
    parts, depth, cur = [], 0, ''
    for ch in sel:
        if ch in '([': depth += 1
        elif ch in ')]': depth -= 1
        if ch == sep and depth == 0: parts.append(cur); cur = ''
        else: cur += ch
    parts.append(cur)
    return parts


def selector_dead(sel):
    outside = re.sub(r':not\([^)]*\)', '', sel)
    for c in re.findall(r'\.([A-Za-z][A-Za-z0-9_-]*)', outside):
        if c in dead: return True
    for i in re.findall(r'#([A-Za-z][A-Za-z0-9_-]*)', outside):
        if i in dead: return True
    return False


removed_sel = []


def parse_rules(text):
    """Zerlegt CSS in Tokens: ('comment'|'rule'|'at', prelude, body-or-None)."""
    toks, i, n = [], 0, len(text)
    while i < n:
        if text[i].isspace():
            j = i
            while j < n and text[j].isspace(): j += 1
            toks.append(('ws', text[i:j], None)); i = j; continue
        if text.startswith('/*', i):
            j = text.index('*/', i) + 2
            toks.append(('comment', text[i:j], None)); i = j; continue
        j = i
        while j < n and text[j] != '{' and text[j] != ';': j += 1
        if j >= n: toks.append(('ws', text[i:], None)); break
        if text[j] == ';':
            toks.append(('stmt', text[i:j + 1], None)); i = j + 1; continue
        prelude = text[i:j]
        depth, k = 0, j
        while k < n:
            if text[k] == '{': depth += 1
            elif text[k] == '}':
                depth -= 1
                if depth == 0: break
            k += 1
        body = text[j + 1:k]
        kind = 'at' if prelude.strip().startswith('@') else 'rule'
        toks.append((kind, prelude, body)); i = k + 1
    return toks


def clean(text):
    toks = parse_rules(text)
    out = []
    for kind, a, b in toks:
        if kind == 'rule':
            sels = split_top(a.strip())
            keep = [x for x in sels if not selector_dead(x.strip())]
            if len(keep) == len(sels):
                out.append(('rule', a + '{' + b + '}'))
            elif keep:
                removed_sel.extend(x.strip() for x in sels if selector_dead(x.strip()))
                out.append(('rule', ', '.join(x.strip() for x in keep) + ' {' + b + '}'))
            else:
                removed_sel.append(a.strip()[:80]); out.append(('removed', ''))
        elif kind == 'at':
            name = a.strip().split()[0]
            if name in ('@media', '@supports'):
                inner = clean(b)
                if inner.strip(): out.append(('rule', a + '{' + inner + '}'))
                else: removed_sel.append(a.strip()[:80]); out.append(('removed', ''))
            else:
                out.append(('rule', a + '{' + b + '}'))
        else:
            out.append((kind, a))
    # Kommentare unmittelbar vor entfernten Regeln mit entfernen
    res = []
    for idx, (k, v) in enumerate(out):
        if k == 'comment':
            nxt = next((o for o in out[idx + 1:] if o[0] != 'ws'), None)
            if nxt and nxt[0] == 'removed': continue
        if k == 'ws' and res and res[-1][0] == 'ws': continue
        res.append((k, v))
    txt = ''.join(v for k, v in res if k != 'removed')
    return re.sub(r'\n[ \t]*\n[ \t]*\n+', '\n\n', txt)


new_blocks = []
for m in style_blocks:
    new_blocks.append(clean(m.group(2)))
# Keyframes, die nirgends mehr verwendet werden
def drop_unused_keyframes(css):
    for kf in re.findall(r'@keyframes\s+([A-Za-z0-9_-]+)', css):
        uses = len(re.findall(r'(?<![A-Za-z0-9_-])' + re.escape(kf) + r'(?![A-Za-z0-9_-])', css + text_wo_css))
        if uses <= 1:
            css = re.sub(r'@keyframes\s+' + re.escape(kf) + r'\s*\{(?:[^{}]|\{[^{}]*\})*\}\s*', '', css)
            removed_sel.append('@keyframes ' + kf)
    return css
new_blocks = [drop_unused_keyframes(b) for b in new_blocks]
for m, nb in reversed(list(zip(style_blocks, new_blocks))):
    s = s[:m.start(2)] + nb + s[m.end(2):]
print('CSS-Regeln/Selektoren entfernt:', len(removed_sel))
print(json.dumps(removed_sel[:60], ensure_ascii=False))

# --- Sprachschluessel ---
i0 = s.index('const I18N = {'); j0 = s.index('\n};', s.index('\nzh:', i0))
rest = s[:i0] + s[j0:]
de_start = s.index('\nde: {', i0)
de_end = s.index('\n},', de_start)
keys = re.findall(r'^\s+([a-z_0-9]+): ', s[de_start:de_end], re.M)
STEMS = re.compile(r'^(ripe_|seg_|st_|s_over_warn|drinkrule_|l_from$|l_to$|rack_blink|sort_ripeness|nav_ripe$|toast_label_ripe|ripe-|rack_ripe)')
unused = []
for k in keys:
    if not re.search(r'(?<![A-Za-z0-9_])' + re.escape(k) + r'(?![A-Za-z0-9_])', rest):
        unused.append(k)
cand = [k for k in unused if STEMS.search(k)]
other_unused = [k for k in unused if k not in cand]
print('verwaiste Schluessel (Feature):', cand)
print('weitere unreferenzierte Schluessel (NICHT entfernt, evtl. dynamisch):', len(other_unused), other_unused[:40])
removed_keys = 0
lines = s.split('\n'); out = []; in_i = False
cs = set(cand)
for l in lines:
    if l.startswith('const I18N = {'): in_i = True
    m = re.match(r'^\s+([a-z_0-9]+): ', l)
    if in_i and m and m.group(1) in cs and (l.rstrip().endswith(',') or l.rstrip().endswith('"') or l.rstrip().endswith("'")):
        removed_keys += 1; continue
    out.append(l)
s = '\n'.join(out)
print('entfernte Sprachzeilen:', removed_keys)

# --- Last Build ---
rep('        <div class="contact-copyright">© 2026 Thomas Knecht. All rights reserved.</div>\n',
    '        <div class="contact-copyright">© 2026 Thomas Knecht. All rights reserved.</div>\n        <div class="contact-build" id="last-build"></div>\n')
m = re.search(r"const APP_VERSION = [^\n]*\n", s)
assert m
s = s[:m.end()] + "const BUILD_DATE = '2026-11-15';   // bei jedem Build auf das aktuelle Datum setzen (Anzeige: Kontakt → Last Build)\n" + s[m.end():]
rep("function applyVersion() {\n  const el = document.getElementById('app-version');\n  if (el) el.textContent = t('setup_version') + ' ' + APP_VERSION;\n}",
    "function applyVersion() {\n  const el = document.getElementById('app-version');\n  if (el) el.textContent = t('setup_version') + ' ' + APP_VERSION;\n  const lb = document.getElementById('last-build');\n  if (lb) { let d = BUILD_DATE; try { d = new Date(BUILD_DATE + 'T12:00:00').toLocaleDateString(dateLocale(), { day: '2-digit', month: '2-digit', year: 'numeric' }); } catch (e) {} lb.textContent = 'Last Build: ' + d; }\n}")
s = s.replace('</style>', '.contact-build { font-size: 11px; color: var(--text-muted); margin-top: 6px; text-align: center; opacity: .85; }\n</style>', 1)
open(P, 'w', encoding='utf-8', newline='').write(s)
c = re.findall(r'<script(?![^>]*src)[^>]*>(.*?)</script>', s, flags=re.S)[0]
open('C:/Users/tknec/AppData/Local/Temp/chk.js', 'w', encoding='utf-8').write(c)
rr = subprocess.run(['node', '--check', 'C:/Users/tknec/AppData/Local/Temp/chk.js'], capture_output=True, text=True)
print('syntax', rr.returncode, rr.stderr[:300])
print('Bytes', size0, '->', len(s.encode('utf-8')))

"""Traegt die Schluessel aus whiskey_source.json (+ tr_whiskey_<code>.json) und extras_whiskey_source.json (+ tr_extras_whiskey_<code>.json)
in JEDEN Sprachblock von const I18N der Whiskey-App ein. Vorhandene Schluessel werden ersetzt (keine Doppelten).
Aufruf: python merge_i18n.py [--check]"""
import re, sys, json, os
sys.stdout.reconfigure(encoding='utf-8')
P = 'C:/wk/My-Whiskey-Collection/index.html'
D = 'C:/wk/Gin-Factory/_tools/i18n/'
CODES = 'es sv da fi ru it fr pl hu cs sk ro hr pt no nl el uk ja ko zh hi'.split()


def load(name):
    p = D + name
    return json.load(open(p, encoding='utf-8')) if os.path.exists(p) else None


src = load('whiskey_source.json')
ext = load('extras_whiskey_source.json') or {'de': {}, 'en': {}}
data = {'de': dict(src['de'], **ext['de']), 'en': dict(src['en'], **ext['en'])}
core_keys = list(src['de'].keys())
ext_keys = list(ext['de'].keys())
missing_tr = []
for c in CODES:
    d = dict(load('tr_whiskey_%s.json' % c) or {})
    if not d:
        missing_tr.append('tr_whiskey_' + c)
    e = load('tr_extras_whiskey_%s.json' % c)
    if e:
        d.update(e)
    else:
        missing_tr.append('tr_extras_whiskey_' + c)
    data[c] = d
# Korrekturen (Wein-Reste in einzelnen Uebersetzungen), die ein erneutes Zusammenfuehren nicht zuruecksetzen soll
ov_path = 'C:/wk/My-Whiskey-Collection/_tools/i18n_overrides_whiskey.json'
if os.path.exists(ov_path):
    for c, kv in json.load(open(ov_path, encoding='utf-8')).items():
        data.setdefault(c, {}).update(kv)
REMOVE_KEYS = ['sort_ripeness']   # verwaiste Schluessel (Funktion entfernt)
s = open(P, encoding='utf-8').read()
i0 = s.index('const I18N = {')
j0 = s.index('\n};', s.index('\nzh:', i0))
head, block, tail = s[:i0], s[i0:j0], s[j0:]
lines = block.split('\n')
# Sprachbloecke finden
starts = [(i, m.group(1)) for i, l in enumerate(lines) for m in [re.match(r'^([a-z]{2}): \{$', l)] if m]
codes_in = [c for _, c in starts]
print('Sprachbloecke:', len(codes_in), codes_in)
if '--check' not in sys.argv:
    out = []
    n_ins = n_rep = 0
    for idx, l in enumerate(lines):
        out.append(l)
    # Block fuer Block bearbeiten (von hinten, damit Indizes stabil bleiben)
    for k in range(len(starts) - 1, -1, -1):
        i, code = starts[k]
        end = starts[k + 1][0] if k + 1 < len(starts) else len(lines)
        vals = data.get(code)
        if vals is None:
            continue
        blk = lines[i + 1:end]
        # vorhandene Schluessel dieses Blocks entfernen, die ersetzt werden (verhindert Doppelte)
        keep = []
        for l in blk:
            m = re.match(r'^\s+([A-Za-z_0-9]+): ', l)
            if m and m.group(1) in REMOVE_KEYS:
                continue
            if m and m.group(1) in vals:
                n_rep += 1
                continue
            keep.append(l)
        new = ['  %s: %s,' % (key, json.dumps(v, ensure_ascii=False)) for key, v in vals.items()]
        n_ins += len(new)
        lines[i + 1:end] = new + keep
    block = '\n'.join(lines)
    s = head + block + tail
    open(P, 'w', encoding='utf-8', newline='').write(s)
    print('eingetragen:', n_ins, 'ersetzte vorhandene Zeilen:', n_rep)
    if missing_tr:
        print('Hinweis: fehlende Dateien (Sprache faellt auf en zurueck):', len(missing_tr), 'z. B.', missing_tr[:3])
# Pruefung: jeder Block hat jeden Kernschluessel
s2 = open(P, encoding='utf-8').read()
i0 = s2.index('const I18N = {')
j0 = s2.index('\n};', s2.index('\nzh:', i0))
blk_all = s2[i0:j0].split('\n')
starts = [(i, m.group(1)) for i, l in enumerate(blk_all) for m in [re.match(r'^([a-z]{2}): \{$', l)] if m]
bad = {}
dups = {}
for k, (i, code) in enumerate(starts):
    end = starts[k + 1][0] if k + 1 < len(starts) else len(blk_all)
    keys = [re.match(r'^\s+([A-Za-z_0-9]+): ', l).group(1) for l in blk_all[i + 1:end] if re.match(r'^\s+([A-Za-z_0-9]+): ', l)]
    ks = set(keys)
    miss = [x for x in core_keys if x not in ks]
    if miss:
        bad[code] = miss
    if len(keys) != len(ks):
        dups[code] = len(keys) - len(ks)
print('Bloecke ohne alle Kernschluessel:', {c: len(m) for c, m in bad.items()} or 'keiner')
print('Doppelte Schluessel je Block:', dups or 'keine')

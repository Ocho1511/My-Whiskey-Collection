import re, sys, json
sys.stdout.reconfigure(encoding='utf-8')
s = open('C:/wk/My-Whiskey-Collection/index.html', encoding='utf-8').read()
i0 = s.index('const I18N = {')
j0 = s.index('\n};', s.index('\nzh:', i0))
blk = s[i0:j0].split('\n')
starts = [(i, m.group(1)) for i, l in enumerate(blk) for m in [re.match(r'^([a-z]{2}): \{$', l)] if m]
# Wein-Woerter je Sprache (Wortanfang, ohne Wortgrenze am Ende)
W = {
 'de': r'\b(wein|weine|weine?n|weingut|rebsort|jahrgang|trinkreife|trinkfenster|vivino|winzer|rotwein|weißwein|sekt\b|champagner|kellerei)',
 'en': r'\b(wine|wines|winery|grape|vintage|vivino|sparkling|champagne|cellar\b)',
 'es': r'\b(vino|vinos|bodega|uva\b|cosecha|vivino)', 'sv': r'\b(vin\b|viner|vinet|druva|årgång|vivino)', 'da': r'\b(vin\b|vine\b|vinen|drue|årgang|vivino)',
 'fi': r'\b(viini|viinit|viinin|rypäle|vuosikerta|vivino)', 'ru': r'(вин[оау]\b|вина\b|вин\b|сорт винограда|урожай|vivino|шампанск)', 'it': r'\b(vino|vini|vigneto|uva\b|annata|vivino)',
 'fr': r'\b(vin\b|vins\b|domaine|cépage|millésime|vivino)', 'pl': r'\b(wino|wina\b|win\b|szczep|rocznik|vivino)', 'hu': r'\b(bor\b|borok|szőlőfajta|évjárat|pincészet|vivino)',
 'cs': r'\b(víno|vína|vín\b|odrůda|ročník|vivino)', 'sk': r'\b(víno|vína|vín\b|odroda|ročník|vivino)', 'ro': r'\b(vin\b|vinuri|struguri|recoltă|vivino)',
 'hr': r'\b(vino|vina\b|sorta grož|berba|vivino)', 'pt': r'\b(vinho|vinhos|uva\b|colheita|vivino)', 'no': r'\b(vin\b|viner|vinen|drue|årgang|vivino)',
 'nl': r'\b(wijn|wijnen|druif|jaargang|vivino)', 'el': r'(κρασ|οινοπ|ποικιλία σταφυλ|vivino)', 'uk': r'(вин[оау]\b|вина\b|вин\b|сорт винограду|врожай|vivino)',
 'ja': r'(ワイン|ブドウ品種|ヴィンテージ|ヴィヴィーノ|vivino)', 'ko': r'(와인|포도 품종|빈티지|vivino)', 'zh': r'(葡萄酒|红酒|葡萄品种|年份|酒庄|vivino)', 'hi': r'(वाइन|अंगूर की किस्म|विंटेज|vivino)',
}
found = {}
for k, (i, code) in enumerate(starts):
    end = starts[k + 1][0] if k + 1 < len(starts) else len(blk)
    pat = re.compile(W[code], re.I)
    for l in blk[i + 1:end]:
        m = re.match(r'^\s+([A-Za-z_0-9]+): (".*"),?$', l)
        if not m:
            continue
        key, val = m.group(1), m.group(2)
        if pat.search(val):
            found.setdefault(key, {})[code] = pat.search(val).group(0)
print('Schluessel mit Wein-Woertern:', len(found))
for key, langs in sorted(found.items()):
    print(' ', key, '->', ', '.join('%s(%s)' % (c, w) for c, w in langs.items()))

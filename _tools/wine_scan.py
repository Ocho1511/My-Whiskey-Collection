import re, sys
sys.stdout.reconfigure(encoding='utf-8')
s = open('C:/wk/My-Whiskey-Collection/index.html', encoding='utf-8').read()
m = re.search(r'<script(?![^>]*src)[^>]*>(.*?)</script>', s, re.S)
js = m.group(1)
html = s[:m.start()] + s[m.end():]
i0 = js.index('const I18N = {')
j0 = js.index('\n};', js.index('\nzh:', i0))
code = js[:i0] + js[j0:]
PAT = re.compile(r'\b(Wein(e|en|es|gut\w*|händler\w*|shop\w*|region\w*|karte|typ|art|etikett\w*)?|wine\w*|Rebsort\w*|Rebe\w*|grape\w*|Jahrgang|vintage|Trinkreife|Trinkfenster|Vivino|Winzer\w*|Weinkeller|Keller|Rotwein|Weißwein|Sekt|Champagne\w*)\b', re.I)
LIT = re.compile(r"""'(?:[^'\\\n]|\\.)*'|"(?:[^"\\\n]|\\.)*"|`(?:[^`\\]|\\.)*`""")
print('=== JS-Zeichenketten mit Wein-Woertern ===')
for n, l in enumerate(code.split('\n'), 1):
    if l.strip().startswith('//'):
        continue
    for sm in LIT.finditer(l):
        lit = sm.group(0)
        if PAT.search(lit) and re.search(r'[A-Za-zÄÖÜäöü]{4,} [A-Za-zÄÖÜäöü]{3,}', lit):
            print(n, '|', lit[:200])
print('=== HTML ===')
for n, l in enumerate(html.split('\n'), 1):
    if PAT.search(l) and not l.strip().startswith(('<!--', '/*', '//', '.', '#', '@')):
        print(n, '|', l.strip()[:170])

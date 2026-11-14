import re, sys
sys.stdout.reconfigure(encoding='utf-8')
P = 'C:/wk/My-Whiskey-Collection/index.html'

# Rezeptbuch mit Whisky-Tumbler (Bernstein, Eiswuerfel) auf dem Einband, flach mit Verlaeufen
ICON = ('<svg viewBox="0 0 24 24" width="1em" height="1em" aria-hidden="true" style="display:block;margin:0 auto">'
        '<defs>'
        '<linearGradient id="rcA" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8a5a2e"/><stop offset="1" stop-color="#4a2e16"/></linearGradient>'
        '<linearGradient id="rcB" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f0b455"/><stop offset="1" stop-color="#b9731f"/></linearGradient>'
        '</defs>'
        '<rect x="4.2" y="2" width="15.6" height="20" rx="1.8" fill="url(#rcA)" stroke="#e9c46a" stroke-width=".7"/>'
        '<rect x="4.2" y="2" width="2.6" height="20" rx="1.2" fill="#3a2410"/>'
        '<path d="M9 8.6h8.4l-.9 8.6a1.4 1.4 0 0 1-1.4 1.2h-3.8a1.4 1.4 0 0 1-1.4-1.2z" fill="rgba(255,255,255,.22)"/>'
        '<path d="M9.4 11.4h7.6l-.6 5.8a1.2 1.2 0 0 1-1.2 1.1h-4a1.2 1.2 0 0 1-1.2-1.1z" fill="url(#rcB)"/>'
        '<rect x="10.9" y="12.2" width="2.7" height="2.7" rx=".5" fill="rgba(255,255,255,.55)" transform="rotate(-8 12.2 13.5)"/>'
        '<rect x="13.6" y="13.6" width="2.3" height="2.3" rx=".5" fill="rgba(255,255,255,.4)" transform="rotate(10 14.7 14.8)"/>'
        '<path d="M9.8 9.4l.5 6" stroke="#fff" stroke-opacity=".6" stroke-width=".6" stroke-linecap="round"/>'
        '</svg>')

s = open(P, encoding='utf-8').read()
pat = re.compile(r'(<span class="nav-icon">)🍹(</span><span data-i18n="nav_recipes">)')
s, n = pat.subn(lambda m: m.group(1) + ICON + m.group(2), s)
assert n == 1, n
open(P, 'w', encoding='utf-8', newline='').write(s)
print('ok')

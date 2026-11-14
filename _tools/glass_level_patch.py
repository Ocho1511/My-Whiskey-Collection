import re, sys
sys.stdout.reconfigure(encoding='utf-8')


def rep(s, a, b, count=1):
    c = s.count(a)
    assert c == count, (c, a[:80])
    return s.replace(a, b)


# --- Logo (logo.svg + Splash + Kopf in index.html): Pegel niedriger, Eiswuerfel ragen heraus ---
OLD_LIQ = '<path d="M19.8 29 Q36 31.6 52.2 29 L49.5 50.5 L22.5 50.5 Z"'
NEW_LIQ = '<path d="M21.1 40.2 Q36 42.6 50.9 40.2 L49.5 50.5 L22.5 50.5 Z"'
OLD_CUBES = ('<rect x="25.5" y="32" width="11" height="11" rx="2.2" transform="rotate(-13 31 37.5)"/>\n'
             '            <rect x="36.5" y="36" width="10" height="10" rx="2.2" transform="rotate(12 41.5 41)"/>\n'
             '            <rect x="29" y="42.5" width="8" height="6" rx="1.6" transform="rotate(-6 33 45.5)" fill="rgba(255,255,255,.22)"/>')
NEW_CUBES = ('<rect x="29" y="43.6" width="8" height="5.4" rx="1.5" transform="rotate(-6 33 46.3)" fill="rgba(255,255,255,.2)"/>\n'
             '            <rect x="25.6" y="32.4" width="11.6" height="12.4" rx="2.3" transform="rotate(-13 31.4 38.6)"/>\n'
             '            <rect x="37" y="35.4" width="10.4" height="10.6" rx="2.2" transform="rotate(12 42.2 40.7)"/>')

for path in ('C:/wk/My-Whiskey-Collection/logo.svg', 'C:/wk/My-Whiskey-Collection/index.html'):
    s = open(path, encoding='utf-8').read()
    n = s.count(OLD_LIQ)
    assert n >= 1, path
    s = s.replace(OLD_LIQ, NEW_LIQ)
    # Wuerfel-Block: in logo.svg ist die Einrueckung identisch (12 Leerzeichen); sonst per Regex
    s2, k = re.subn(r'<rect x="25\.5" y="32" width="11" height="11" rx="2\.2" transform="rotate\(-13 31 37\.5\)"/>\s*'
                    r'<rect x="36\.5" y="36" width="10" height="10" rx="2\.2" transform="rotate\(12 41\.5 41\)"/>\s*'
                    r'<rect x="29" y="42\.5" width="8" height="6" rx="1\.6" transform="rotate\(-6 33 45\.5\)" fill="rgba\(255,255,255,\.22\)"/>',
                    NEW_CUBES, s)
    assert k == n, (path, k, n)
    open(path, 'w', encoding='utf-8', newline='').write(s2)
    print('logo updated', path, n)

# --- kleines Tumbler-Symbol im Rezepte-Tab: weniger Whisky, Eis ragt heraus ---
P = 'C:/wk/My-Whiskey-Collection/index.html'
s = open(P, encoding='utf-8').read()
s = rep(s, '<path d="M9.4 11.4h7.6l-.6 5.8a1.2 1.2 0 0 1-1.2 1.1h-4a1.2 1.2 0 0 1-1.2-1.1z" fill="url(#rcB)"/>',
        '<path d="M9.75 14.4h6.9l-.35 2.8a1.2 1.2 0 0 1-1.2 1.1h-3.8a1.2 1.2 0 0 1-1.2-1.1z" fill="url(#rcB)"/>')
s = rep(s, '<rect x="10.9" y="12.2" width="2.7" height="2.7" rx=".5" fill="rgba(255,255,255,.55)" transform="rotate(-8 12.2 13.5)"/>',
        '<rect x="10.7" y="10.9" width="3" height="3.9" rx=".6" fill="rgba(255,255,255,.7)" transform="rotate(-8 12.2 12.8)"/>')
s = rep(s, '<rect x="13.6" y="13.6" width="2.3" height="2.3" rx=".5" fill="rgba(255,255,255,.4)" transform="rotate(10 14.7 14.8)"/>',
        '<rect x="13.9" y="12.3" width="2.5" height="3.2" rx=".5" fill="rgba(255,255,255,.55)" transform="rotate(10 15.1 13.9)"/>')
open(P, 'w', encoding='utf-8', newline='').write(s)
print('recipes icon updated')

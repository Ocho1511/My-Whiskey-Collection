import re, sys
sys.stdout.reconfigure(encoding='utf-8')


def bottle(uid, style):
    return (f'<svg viewBox="0 0 32 32" width="1em" height="1em" aria-hidden="true" style="{style}">'
            '<defs>'
            f'<linearGradient id="wg{uid}" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#9a5a17"/><stop offset=".3" stop-color="#e9a447"/><stop offset=".65" stop-color="#c47a22"/><stop offset="1" stop-color="#7a4210"/></linearGradient>'
            f'<linearGradient id="wl{uid}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f3dfb0"/><stop offset="1" stop-color="#d9bf84"/></linearGradient>'
            f'<linearGradient id="wc{uid}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#5b3a22"/><stop offset="1" stop-color="#2e1b0e"/></linearGradient>'
            '</defs>'
            '<ellipse cx="16" cy="30.7" rx="8.6" ry="1" fill="#000" opacity=".28"/>'
            f'<path d="M13.5 6h5v4.6c0 1.4 5.6 2.2 5.6 6.4v9.8a3 3 0 0 1-3 3H10.9a3 3 0 0 1-3-3V17c0-4.2 5.6-5 5.6-6.4z" fill="url(#wg{uid})"/>'
            f'<rect x="7.9" y="16.6" width="16.2" height="9.4" fill="url(#wl{uid})"/>'
            '<rect x="7.9" y="16.6" width="16.2" height="1.6" fill="#3a2410"/>'
            '<rect x="7.9" y="24.4" width="16.2" height="1.6" fill="#3a2410"/>'
            '<rect x="11" y="20" width="10" height="1.1" rx=".5" fill="#6a4420"/>'
            '<rect x="12.6" y="22" width="6.8" height=".9" rx=".45" fill="#8a5a2e"/>'
            f'<rect x="12.6" y="1.8" width="6.8" height="4.8" rx="1.3" fill="url(#wc{uid})"/>'
            '<rect x="13.2" y="5.6" width="5.6" height="1.3" rx=".4" fill="#e9c46a"/>'
            '<path d="M10.6 19v7" stroke="#fff" stroke-opacity=".5" stroke-width="1" stroke-linecap="round"/>'
            '<path d="M14.5 8.4v2.4" stroke="#fff" stroke-opacity=".5" stroke-width=".8" stroke-linecap="round"/>'
            '</svg>')


if __name__ == '__main__':
    P = 'C:/wk/My-Whiskey-Collection/index.html'
    s = open(P, encoding='utf-8').read()
    nav = bottle('N', 'display:block;margin:0 auto')
    pat = re.compile(r'(<span class="nav-icon">)(?:🥃|<svg viewBox="0 0 32 32" width="1em".*?</svg>)(</span><span data-i18n="nav_keller">)', re.S)
    s, n = pat.subn(lambda m: m.group(1) + nav + m.group(2), s, count=1)
    assert n == 1, n
    open(P, 'w', encoding='utf-8', newline='').write(s)
    print('ok')

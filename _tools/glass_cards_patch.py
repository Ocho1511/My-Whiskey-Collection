import re, sys, subprocess
sys.stdout.reconfigure(encoding='utf-8')
P = 'C:/wk/My-Whiskey-Collection/index.html'
s = open(P, encoding='utf-8').read()
block = open('C:/wk/My-Whiskey-Collection/_tools/glass_cards_block.js', encoding='utf-8').read()


def rep(a, b, count=1):
    global s
    c = s.count(a)
    assert c == count, (c, a[:90])
    s = s.replace(a, b)


rep('target="_blank" rel="noopener" onclick="event.stopPropagation()">${esc(name)} · ${esc(glassViewText())} ↗</a>`;',
    'target="_blank" rel="noopener" data-glass="${esc(name)}" onclick="return glassClick(this,event)">${esc(name)} · ${esc(glassViewText())} ↗</a>`;')
rep('<a id="serve-glass-link" class="glass-link" href="#" target="_blank" rel="noopener" style="display:none"></a>',
    '<a id="serve-glass-link" class="glass-link" href="#" target="_blank" rel="noopener" style="display:none" onclick="return glassClick(this,event)"></a>')
rep("  a.href = glassUrl(v); a.textContent = '🔍 '", "  a.href = glassUrl(v); a.setAttribute('data-glass', v); a.textContent = '🔍 '")
rep('function serveGlassLink() {', block + '\nfunction serveGlassLink() {')
css = ('.glass-overlay { position: fixed; inset: 0; background: rgba(0,0,0,.65); z-index: 10000; display: flex; align-items: center; justify-content: center; padding: 20px; }\n'
       '.glass-card { background: var(--card); border: 1px solid var(--border); border-radius: 18px; padding: 20px 18px; max-width: 340px; width: 100%; text-align: center; box-shadow: 0 10px 40px rgba(0,0,0,.5); }\n'
       '.glass-card svg { display: block; margin: 0 auto 6px; }\n'
       '.glass-card .glass-title { font-family: var(--heading-font, "Playfair Display", serif); font-size: 20px; margin: 4px 0 8px; }\n'
       '.glass-card p { font-size: 14px; line-height: 1.5; color: var(--text-muted); margin: 0 0 12px; }\n'
       '.glass-card .glass-link { display: inline-block; margin: 0 0 14px; }\n'
       '.glass-card .wine-btn { width: 100%; }\n')
s = s.replace('</style>', css + '</style>', 1)
open(P, 'w', encoding='utf-8', newline='').write(s)
c = re.findall(r'<script(?![^>]*src)[^>]*>(.*?)</script>', s, flags=re.S)[0]
open('C:/Users/tknec/AppData/Local/Temp/chk.js', 'w', encoding='utf-8').write(c)
print('syntax', subprocess.run(['node', '--check', 'C:/Users/tknec/AppData/Local/Temp/chk.js'], capture_output=True, text=True).returncode)

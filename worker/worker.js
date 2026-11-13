// Cloudflare Worker "whiskey-scan-proxy" for My Whiskey Collection.
// Endpoints (all POST, JSON):
//   /            Anthropic Messages proxy (label scan, lookup, price search). Key stays in the secret ANTHROPIC_API_KEY.
//   /sync        cloud sync by sync code (KV): ops "pull" and "push"
//   /barcode     EAN lookup via Open Food Facts
//   /whiskeyimg  bottle picture by name via Open Food Facts, fallback Wikipedia thumbnail (returns { image, match })
//   /ogimage     og:image of a web page
//   /rates       ECB euro reference rates
//   /acct/status, /acct/unlock   optional per-install AI credits (only if env.GATED = "1")
// Bindings / settings (see wrangler.toml): KV namespace WK (optional but needed for sync + credits + rate limit),
// secret ANTHROPIC_API_KEY, optional secret UNLOCK_CODE, vars ALLOWED_ORIGINS, FREE_CREDITS, GATED.

const UA = 'MyWhiskeyCollection/1.0 (bottle lookup)';
const JSON_H = { 'Content-Type': 'application/json' };
const MAX_BODY = 12 * 1024 * 1024;       // photos are sent as base64
const MAX_SYNC = 5 * 1024 * 1024;
const AI_FIELDS = ['model', 'max_tokens', 'system', 'messages', 'tools', 'temperature', 'stop_sequences'];

function origins(env) {
  return String(env.ALLOWED_ORIGINS || '').split(',').map(s => s.trim()).filter(Boolean);
}
function corsFor(request, env) {
  const o = request.headers.get('Origin') || '';
  const list = origins(env);
  const ok = !o || list.includes('*') || list.includes(o) || /^https?:\/\/(localhost|127\.0\.0\.1)(:\d+)?$/.test(o) || o === 'capacitor://localhost' || o === 'ionic://localhost';
  return {
    ok,
    headers: {
      'Access-Control-Allow-Origin': ok && o ? o : (list[0] || 'null'),
      'Access-Control-Allow-Methods': 'POST, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type, X-Install-Id',
      'Access-Control-Expose-Headers': 'X-Credits-Left',
      'Vary': 'Origin'
    }
  };
}
const reply = (obj, status, cors, extra) => new Response(JSON.stringify(obj), { status: status || 200, headers: Object.assign({}, JSON_H, cors, extra || {}) });

async function rateLimit(request, env, limit) {
  if (!env.WK) return true;
  const ip = request.headers.get('CF-Connecting-IP') || 'x';
  const key = 'rl:' + ip + ':' + Math.floor(Date.now() / 60000);
  const n = parseInt(await env.WK.get(key) || '0', 10) + 1;
  if (n > limit) return false;
  await env.WK.put(key, String(n), { expirationTtl: 120 });
  return true;
}

// ── optional credits (native store app) ──
const idOk = (id) => /^[A-Za-z0-9-]{8,80}$/.test(id || '');
async function getCredits(env, id) {
  const raw = await env.WK.get('acct:' + id, 'json');
  if (raw) return raw;
  return { credits: parseInt(env.FREE_CREDITS || '50', 10), unlimited: false };
}
const putCredits = (env, id, a) => env.WK.put('acct:' + id, JSON.stringify(a));

// ── AI proxy ──
async function aiProxy(request, env, cors) {
  if (!env.ANTHROPIC_API_KEY) return reply({ error: 'not_configured' }, 500, cors.headers);
  const len = parseInt(request.headers.get('Content-Length') || '0', 10);
  if (len > MAX_BODY) return reply({ error: 'too_large' }, 413, cors.headers);
  let body; try { body = await request.json(); } catch { return reply({ error: 'bad_json' }, 400, cors.headers); }
  const out = {}; for (const k of AI_FIELDS) if (body[k] !== undefined) out[k] = body[k];
  if (!out.model || !Array.isArray(out.messages)) return reply({ error: 'bad_request' }, 400, cors.headers);
  if (!(out.max_tokens > 0)) out.max_tokens = 1024;
  out.max_tokens = Math.min(out.max_tokens, 4096);
  if (!(await rateLimit(request, env, 30))) return reply({ error: 'rate_limited' }, 429, cors.headers);
  const extra = {};
  const gated = env.GATED === '1' && env.WK;
  const id = request.headers.get('X-Install-Id') || '';
  let acct = null;
  if (gated) {
    if (!idOk(id)) return reply({ error: 'install_id' }, 400, cors.headers);
    acct = await getCredits(env, id);
    if (!acct.unlimited && acct.credits <= 0) return reply({ error: 'no_credits' }, 402, cors.headers, { 'X-Credits-Left': '0' });
  }
  const r = await fetch('https://api.anthropic.com/v1/messages', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', 'x-api-key': env.ANTHROPIC_API_KEY, 'anthropic-version': '2023-06-01' },
    body: JSON.stringify(out)
  });
  const text = await r.text();
  if (gated && r.ok && !acct.unlimited) { acct.credits -= 1; await putCredits(env, id, acct); }
  if (gated) extra['X-Credits-Left'] = acct.unlimited ? 'unlimited' : String(Math.max(0, acct.credits));
  return new Response(text, { status: r.status, headers: Object.assign({}, JSON_H, cors.headers, extra) });
}

// ── sync ──
async function sync(request, env, cors) {
  if (!env.WK) return reply({ error: 'no_kv' }, 501, cors.headers);
  if (!(await rateLimit(request, env, 120))) return reply({ error: 'rate_limited' }, 429, cors.headers);
  let b; try { b = await request.json(); } catch { return reply({ error: 'bad_json' }, 400, cors.headers); }
  const code = String(b.code || '');
  if (!/^[A-Za-z0-9_-]{8,64}$/.test(code)) return reply({ error: 'bad_code' }, 400, cors.headers);
  const key = 'sync:' + code;
  const cur = await env.WK.get(key, 'json');
  if (b.op === 'pull') {
    return reply(cur ? { exists: true, updatedAt: cur.updatedAt || 0, data: cur.data } : { exists: false }, 200, cors.headers);
  }
  if (b.op === 'push') {
    const at = Number(b.updatedAt) || 0;
    if (!b.data || typeof b.data !== 'object') return reply({ error: 'bad_data' }, 400, cors.headers);
    const s = JSON.stringify({ updatedAt: at, data: b.data });
    if (s.length > MAX_SYNC) return reply({ error: 'too_large' }, 413, cors.headers);
    if (cur && (cur.updatedAt || 0) > at) return reply({ stored: false, newer: true, updatedAt: cur.updatedAt, data: cur.data }, 200, cors.headers);
    await env.WK.put(key, s);
    return reply({ stored: true, updatedAt: at }, 200, cors.headers);
  }
  return reply({ error: 'bad_op' }, 400, cors.headers);
}

// ── Open Food Facts helpers ──
const WHISKY_RE = /whisk|bourbon|scotch|single-malt|malt-whisk|rye/i;
function whiskeyType(text) {
  const t = String(text || '').toLowerCase();
  if (/bourbon|rye|tennessee|american/.test(t)) return 'weiß';
  if (/blended|blend|johnnie walker|chivas|ballantine|dewar|famous grouse|monkey shoulder|j&b/.test(t)) return 'rosé';
  if (/single malt|single-malt|islay|speyside|highland|lowland|campbeltown/.test(t)) return 'rot';
  if (/irish|japan|nikka|suntory|indian|taiwan|canadian|world/.test(t)) return 'sekt';
  return '';
}
async function barcode(request, env, cors) {
  let b; try { b = await request.json(); } catch { return reply({ error: 'bad_json' }, 400, cors.headers); }
  const ean = String(b.ean || '');
  if (!/^\d{8,14}$/.test(ean)) return reply({ error: 'bad_ean' }, 400, cors.headers);
  if (!(await rateLimit(request, env, 60))) return reply({ error: 'rate_limited' }, 429, cors.headers);
  const r = await fetch('https://world.openfoodfacts.org/api/v2/product/' + ean + '.json?fields=product_name,brands,categories_tags,quantity', { headers: { 'User-Agent': UA } });
  if (!r.ok && r.status !== 404) return reply({ error: 'upstream' }, 502, cors.headers);
  const j = await r.json().catch(() => null);
  if (!j || j.status !== 1 || !j.product) return reply({ found: false }, 200, cors.headers);
  const p = j.product, cats = (p.categories_tags || []).join(' ');
  const name = p.product_name || '', brand = (p.brands || '').split(',')[0].trim();
  const spirit = WHISKY_RE.test(cats + ' ' + name) || /spirit|liquor|distilled/.test(cats);
  const alcohol = /alcohol|spirit|beverage/.test(cats);
  return reply({ found: true, name, brand, type: whiskeyType(cats + ' ' + name + ' ' + brand), notWine: alcohol && !spirit ? true : (!alcohol && cats ? true : false) }, 200, cors.headers);
}
async function whiskeyImg(request, env, cors) {
  let b; try { b = await request.json(); } catch { return reply({ error: 'bad_json' }, 400, cors.headers); }
  const name = String(b.name || '').trim().slice(0, 120);
  if (name.length < 2) return reply({ image: null }, 200, cors.headers);
  if (!(await rateLimit(request, env, 60))) return reply({ error: 'rate_limited' }, 429, cors.headers);
  const q = [name, b.grape && !name.toLowerCase().includes(String(b.grape).toLowerCase()) ? b.grape : ''].filter(Boolean).join(' ').slice(0, 160);
  try {
    const u = 'https://world.openfoodfacts.org/cgi/search.pl?action=process&json=1&page_size=10&search_simple=1&fields=product_name,brands,image_front_url,categories_tags&search_terms=' + encodeURIComponent(q);
    const r = await fetch(u, { headers: { 'User-Agent': UA } });
    if (!r.ok) throw new Error('off ' + r.status);
    const j = await r.json();
    const hit = (j.products || []).find(p => p.image_front_url && WHISKY_RE.test((p.categories_tags || []).join(' ') + ' ' + (p.product_name || '')))
      || (j.products || []).find(p => p.image_front_url && (p.categories_tags || []).some(c => /spirit|liquor|distilled/.test(c)));
    if (hit) return reply({ image: hit.image_front_url, match: [hit.brands, hit.product_name].filter(Boolean).join(' '), source: 'openfoodfacts' }, 200, cors.headers);
  } catch (e) { /* fall through to Wikipedia */ }
  try {
    const u = 'https://en.wikipedia.org/w/api.php?action=query&format=json&generator=search&gsrlimit=1&prop=pageimages&piprop=thumbnail&pithumbsize=500&gsrsearch=' + encodeURIComponent(q + ' whisky');
    const r = await fetch(u, { headers: { 'User-Agent': UA } });
    if (!r.ok) throw new Error('wp ' + r.status);
    const j = await r.json();
    const page = j.query && j.query.pages ? Object.values(j.query.pages)[0] : null;
    if (page && page.thumbnail && page.thumbnail.source) return reply({ image: page.thumbnail.source, match: page.title || '', source: 'wikipedia' }, 200, cors.headers);
  } catch (e) { return reply({ error: 'upstream' }, 502, cors.headers); }
  return reply({ image: null }, 200, cors.headers);
}
async function ogImage(request, env, cors) {
  let b; try { b = await request.json(); } catch { return reply({ error: 'bad_json' }, 400, cors.headers); }
  let u; try { u = new URL(String(b.url || '')); } catch { return reply({ image: null }, 200, cors.headers); }
  const h = u.hostname.toLowerCase();
  if (!/^https?:$/.test(u.protocol) || h === 'localhost' || /^[\d.]+$/.test(h) || h.includes(':') || h.endsWith('.local') || h.endsWith('.internal') || !h.includes('.'))
    return reply({ image: null }, 200, cors.headers);
  if (!(await rateLimit(request, env, 60))) return reply({ error: 'rate_limited' }, 429, cors.headers);
  try {
    const r = await fetch(u.toString(), { headers: { 'User-Agent': UA, 'Accept': 'text/html' }, redirect: 'follow' });
    const html = (await r.text()).slice(0, 250000);
    const m = /<meta[^>]+property=["']og:image["'][^>]*content=["']([^"']+)["']/i.exec(html) || /<meta[^>]+content=["']([^"']+)["'][^>]*property=["']og:image["']/i.exec(html);
    if (!m) return reply({ image: null }, 200, cors.headers);
    const img = new URL(m[1].replace(/&amp;/g, '&'), u).toString();
    return reply({ image: /^https:\/\//.test(img) ? img : null }, 200, cors.headers);
  } catch { return reply({ image: null }, 200, cors.headers); }
}
async function rates(request, env, cors) {
  const r = await fetch('https://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml', { cf: { cacheTtl: 3600, cacheEverything: true } });
  if (!r.ok) return reply({ error: 'upstream' }, 502, cors.headers);
  const xml = await r.text();
  const out = { EUR: 1 };
  for (const m of xml.matchAll(/currency=['"]([A-Z]{3})['"]\s+rate=['"]([\d.]+)['"]/g)) out[m[1]] = parseFloat(m[2]);
  return reply({ rates: out, base: 'EUR' }, 200, cors.headers);
}
async function acct(path, request, env, cors) {
  if (env.GATED !== '1' || !env.WK) return reply({ gated: false }, 200, cors.headers);
  const id = request.headers.get('X-Install-Id') || '';
  if (!idOk(id)) return reply({ error: 'install_id' }, 400, cors.headers);
  const a = await getCredits(env, id);
  if (path === '/acct/unlock') {
    let b; try { b = await request.json(); } catch { b = {}; }
    if (!env.UNLOCK_CODE || String(b.code || '') !== env.UNLOCK_CODE) return reply({ error: 'bad_code' }, 403, cors.headers);
    a.unlimited = true; await putCredits(env, id, a);
    return reply({ unlimited: true }, 200, cors.headers);
  }
  return reply({ gated: true, credits: a.credits, unlimited: !!a.unlimited }, 200, cors.headers);
}

export default {
  async fetch(request, env) {
    const cors = corsFor(request, env);
    if (request.method === 'OPTIONS') return new Response(null, { headers: cors.headers });
    if (!cors.ok) return reply({ error: 'origin' }, 403, cors.headers);
    if (request.method !== 'POST') return reply({ error: 'method' }, 405, cors.headers);
    const path = new URL(request.url).pathname.replace(/\/+$/, '') || '/';
    try {
      if (path === '/') return await aiProxy(request, env, cors);
      if (path === '/sync') return await sync(request, env, cors);
      if (path === '/barcode') return await barcode(request, env, cors);
      if (path === '/whiskeyimg') return await whiskeyImg(request, env, cors);
      if (path === '/ogimage') return await ogImage(request, env, cors);
      if (path === '/rates') return await rates(request, env, cors);
      if (path === '/acct/status' || path === '/acct/unlock') return await acct(path, request, env, cors);
      return reply({ error: 'not_found' }, 404, cors.headers);   // /credits/* and /admin/* are not part of this worker
    } catch (e) {
      return reply({ error: 'server' }, 500, cors.headers);
    }
  }
};

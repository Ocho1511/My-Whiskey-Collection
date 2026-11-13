# whiskey-scan-proxy

Cloudflare Worker for My Whiskey Collection (AI proxy, cloud sync, barcode, bottle image search, ECB rates).

```
cd worker
npx wrangler login
npx wrangler kv namespace create WK        # paste the id into wrangler.toml
npx wrangler secret put ANTHROPIC_API_KEY
npx wrangler deploy
```
Then put the printed workers.dev URL into `SCAN_PROXY_URL` in `index.html` (currently https://whiskey-scan-proxy.ocho1511.workers.dev).
Not included: Apple in-app purchase (`/credits/*`) and the admin statistics (`/admin/stats`).

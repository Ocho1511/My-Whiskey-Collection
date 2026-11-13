# My Whiskey Collection

Personal whiskey collection app (PWA): stock, storage racks with QR labels, wish list, statistics, history, cloud sync, AI label scan.

- `index.html` – the app (single file, 24 languages)
- `anleitung*.html`, `support.html`, `datenschutz.html` – guide, support and privacy pages
- `worker/` – Cloudflare Worker (AI proxy, sync, barcode, bottle images, rates), see `worker/README.md`

Derived from the Weinkeller app but independent: own storage keys, own worker, own pages.

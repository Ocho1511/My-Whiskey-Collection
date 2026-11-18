# My Whiskey Collection

Personal whiskey collection app (PWA): stock, storage racks with QR labels, wish list, statistics, history, cloud sync, AI label scan.

- `index.html` – the app (single file, 24 languages)
- `anleitung*.html`, `support.html`, `datenschutz.html` – guide, support and privacy pages
- Backend: shared Cloudflare workers (sync, barcode, page image via the Gin-Factory repo `scan-proxy/`; AI proxy and exchange rates via the Weinkeller worker), no worker code lives in this repo

Derived from the Weinkeller app but independent: own storage keys and own pages (the backend workers are shared with the other apps).

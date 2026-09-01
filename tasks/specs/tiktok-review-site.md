# TikTok review site

## Goal

Publish a small, public, zero-cost website that accurately describes Clipping
Publisher and supplies the legal and visual assets required by TikTok's app
review form.

## Done means

- `index.html`, `privacy.html`, and `terms.html` contain accurate public copy.
- Every local link resolves and every HTML file passes a local HTTP smoke test.
- `app-icon.png` is a 1024x1024 PNG under 5 MB.
- No credentials, personal addresses, analytics, trackers, or third-party scripts
  are present.
- A fresh read-only critic returns PASS against this spec.
- Changes are proposed through a focused pull request.

## Verification

```sh
python3 scripts/verify_site.py
python3 -m http.server 8765
curl --fail http://127.0.0.1:8765/
curl --fail http://127.0.0.1:8765/privacy.html
curl --fail http://127.0.0.1:8765/terms.html
git diff --check
```

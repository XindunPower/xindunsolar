# xindunsolar automation workspace

Cloud Automation repo for daily English→Spanish news translation/publish and published-article image fixes.

| Path | Purpose |
|------|---------|
| `progress.json` | Current news list page to process (daily publish agent only) |
| `scripts/duomi_image.py` | Duomi gpt-image-2 (cloud replacement for local `/image`) |
| `duomi_image.py` | Same helper at repo root (compat) |
| `AUTOMATION_INSTRUCTIONS.md` | Paste into Cursor Automation instructions |
| `requirements.txt` | Pillow for ≤100KB compress |
| `.env.example` | Document `DUOMI_API_KEY` (use Cloud secrets; do not commit `.env`) |

## Required secrets

- `DUOMI_API_KEY` — raw key (no `Bearer`)
- `WP_USER` / `WP_APP_PASSWORD` — WordPress login for cookie + REST nonce

## Duomi command (must use `python3`)

```bash
pip install -r requirements.txt
export DUOMI_API_KEY="..."

python3 scripts/duomi_image.py \
  --image-url "https://www.xindun-power.com/uploadfile/example.jpg" \
  --prompt "Edit this exact image. Keep layout/products/background/aspect ratio unchanged. Only translate English marketing/diagram overlay text to Spanish. Do NOT change product casing text, logos, model numbers, certificates, Chinese exhibition signs, or wall company names (Xindun / Xindun GREEN POWER / XINDUN POWER)." \
  --output-name "nombre-en-espanol-desde-alt" \
  --max-kb 100 \
  --print-json
```

After Duomi: resize to original WxH, JPEG ≤100KB. If aspect differs >5% or layout/products changed, discard and fall back to OCR (or compress-only when there is no English overlay).

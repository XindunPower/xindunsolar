# xindunsolar automation workspace

Cloud Automation repo for daily English→Spanish news translation/publish.

| Path | Purpose |
|------|---------|
| `progress.json` | Current news list page to process |
| `scripts/duomi_image.py` | Duomi gpt-image-2 (cloud replacement for local `/image`) |
| `docs/AUTOMATION_INSTRUCTIONS.md` | Paste into Cursor Automation instructions |
| `requirements.txt` | Pillow for ≤100KB compress |
| `.env.example` | Document `DUOMI_API_KEY` (use Cloud secrets; do not commit `.env`) |

## Quick test

```bash
export DUOMI_API_KEY="..."
python scripts/duomi_image.py --dry-run \
  --image-url "https://www.xindun-power.com/uploadfile/example.jpg" \
  --prompt "Translate overlay text to Spanish; keep product casing text" \
  --size "3:2"
```

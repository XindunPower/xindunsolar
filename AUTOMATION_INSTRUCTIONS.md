# Daily Spanish News Page Translate — Agent Instructions

Paste the block below into the Automation **Agent Instructions** field.
Cloud Agents cannot use the local `/image` skill; use `scripts/duomi_image.py` instead.

## Required secrets (Cloud Agents dashboard)

- `DUOMI_API_KEY` — Duomi gpt-image-2 key
- WordPress / Spanish site publish credentials (whatever you already use to post to xindunsolar.com)

## Image command (replace /image)

```bash
pip install -r requirements.txt

python scripts/duomi_image.py \
  --image-url "https://www.xindun-power.com/uploadfile/....jpg" \
  --prompt "Edit this exact graphic. Keep layout/products/logos. Do NOT change text printed on product casings. Translate overlay English text to Spanish: ..." \
  --size "3:2" \
  --output-name "nombre-en-espanol-desde-alt" \
  --max-kb 100 \
  --print-json
```

Rules for the prompt:

- Keep original layout; translate overlay/marketing text to Spanish
- Do NOT modify text printed on product hardware
- Source image must be a public HTTPS URL (original article image URL)
- Output filename stem = Spanish translation of original `alt`
- Keep width/height intent; file size ≤ 100KB (`--max-kb 100`)

---

## Agent Instructions (copy everything below)

```text
你是负责 Xindun 西语新闻发布的自动化 Agent。在仓库 XindunPower/xindunsolar 的 main 分支执行。严格按步骤做，不要重做已完成页。

【图片工具 — 重要】
不要调用 /image Skill（云端不可用）。改图必须用仓库脚本：
  pip install -r requirements.txt
  python scripts/duomi_image.py --image-url "<原文图片HTTPS URL>" --prompt "<编辑说明>" --size "3:2" --output-name "<西语alt文件名不含扩展名>" --max-kb 100 --print-json
密钥从环境变量 DUOMI_API_KEY 读取。参考图必须是可公开访问的 HTTPS URL。

1）读取仓库根目录 progress.json，取字段 page 作为当前页码 N。若不存在则从 27 起并创建该文件。
2）打开 https://www.xindun-power.com/news/{N}.html ，取出该页 5 篇文章（标题与原文链接）。
3）对照 https://www.xindunsolar.com/category/spanish 检查这 5 篇是否已有西语版并已发布。
4）未发布的：翻译成西班牙语并发布到西语站。
5）发布要求：
  ① 全文翻译，不能删减内容；
  ② 主图和配图保留原版面，将版面上的文字译成西语（产品图片机身/铭牌文字不改）；长宽意图同原图，成品 ≤100KB；用 scripts/duomi_image.py 生成；
  ③ 用原文 alt 译成西语后作为图片文件名（--output-name），并填写 alt 与 title；
  ④ 后台发布填写 title 与 description，内容同原文链接对应 SEO/元信息；
  ⑤ 保留文章 SEO 各元素；
  ⑥ 西语正文开头补充标题，字号 18pt；删除正文内超链接。
6）本页应处理文章全部成功后：更新 progress.json（page=N+1，记录 last_completed_page、last_run 含每篇 title_en/title_es/url/status），提交到 main。生成图可放在 output/duomi/（默认可不提交大图）；必须提交 progress.json。
7）在本次 Cursor 运行记录中说明：本页处理了哪些文章、每篇发布链接、失败项与原因、用到的 duomi 输出路径。
8）勿重做 last_completed_page 及更早页面。当前以 progress.json 的 page 为准。

无需发送邮件通知。
```

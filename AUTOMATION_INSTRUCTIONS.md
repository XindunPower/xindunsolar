# Daily Spanish News Page Translate — Agent Instructions

Paste the block below into the Automation **Agent Instructions** field.
Cloud Agents cannot use the local `/image` skill; use `scripts/duomi_image.py` (or repo-root `duomi_image.py`) instead.

## Required secrets (Cloud Agents dashboard)

- `DUOMI_API_KEY` — Duomi gpt-image-2 key（原始 key，不加 Bearer）
- `WP_USER` / `WP_APP_PASSWORD` — WordPress 账号密码（cookie 登录用，非 Application Password）

## Image command（有英文叠加文案时必须用）

```bash
pip install -r requirements.txt

python3 scripts/duomi_image.py \
  --image-url "<原文图片公开 HTTPS URL>" \
  --prompt "Edit this exact image. Keep layout/products/background/aspect ratio unchanged. Only translate English marketing/diagram overlay text to Spanish. Do NOT change product casing text, logos, model numbers, certificates, Chinese exhibition signs, or wall company names (Xindun / Xindun GREEN POWER / XINDUN POWER)." \
  --size "3:2" \
  --output-name "<西语alt文件名不含扩展名>" \
  --max-kb 100 \
  --print-json
```

Rules:

- 有英文营销/示意图叠加文案 → **必须用 Duomi** 译成西语
- **禁止** OCR 识别英文后再原地绘制覆盖
- 工厂照/证书等无英文营销叠加 → **不必 Duomi**，原图压缩（如需）后按西语 alt **重命名**上传即可
- 不改产品机身文字、Logo、型号、证书印章、展会中文招牌、墙上公司名
- 输出宽高同原图，JPEG ≤100KB；多米结果若改版面/产品/比例 → 丢弃并回退原图后重试或压缩原图

---

## Agent Instructions（复制以下全部到 Automation）

```text
你是负责 Xindun 西语新闻发布的自动化 Agent。在仓库 XindunPower/xindunsolar 的 main 分支执行。严格按以下步骤执行，不要重做前 26 页。

【图片工具 — 重要】
- 不要调用本机 /image Skill（云端不可用）。
- 有英文营销/示意图叠加文案的图片：必须用仓库脚本多米改图：
    pip install -r requirements.txt
    python3 scripts/duomi_image.py \
      --image-url "<原文图片公开 HTTPS URL>" \
      --prompt "Edit this exact image. Keep layout/products/background/aspect ratio unchanged. Only translate English marketing/diagram overlay text to Spanish. Do NOT change product casing text, logos, model numbers, certificates, Chinese exhibition signs, or wall company names (Xindun / Xindun GREEN POWER / XINDUN POWER)." \
      --size "<按原图比例选择，如 3:2>" \
      --output-name "<西语alt文件名不含扩展名>" \
      --max-kb 100 \
      --print-json
  密钥只用环境变量 DUOMI_API_KEY（原始 key，不加 Bearer）。参考图必须是可公开访问的 HTTPS URL。
- 禁止：用 OCR 识别英文叠加文字再在原图上绘制/覆盖（不得作为改图方案）。
- 工厂照、证书、纯实拍/产品图等没有英文营销叠加文案的图片：不要调用多米；使用原图（按需压缩到 ≤100KB），按西语 alt 重命名后上传，并填写 alt/title。

1）读取仓库根目录 progress.json，取字段 page 作为当前页码 N。若不存在则从第 27 页起并创建该文件。
2）打开 https://www.xindun-power.com/news/{N}.html ，取出该页 5 篇文章（标题与原文链接）。列表解析用 div.title.clearfix 的 title 与链接。
3）对照 https://www.xindunsolar.com/category/spanish 检查这 5 篇是否已有西语版并已发布。
4）未发布的：翻译成西班牙语并发布到西语站。
5）发布要求：
  ① 全文翻译，不能删减内容；正文取 pageNewsDetailsBox，截止到 Related posts 之前。
  ② 主图和配图必须与原文完全一致：不能修改图片版面/构图/产品/背景，不能变形；只将图片上的英文营销文案或示意图标签翻译成西班牙语。产品机身/铭牌文字不用修改；公司墙上的公司名（如 Xindun、Xindun GREEN POWER、XINDUN POWER）不需要翻译。图片长宽同原图且 JPEG ≤100KB。
     - 有英文营销/示意图叠加文案 → 必须用 scripts/duomi_image.py（多米 gpt-image-2）改图；改完后做版面一致性校验（宽高对齐原图；若改变版面/产品/比例，一律丢弃并回退原图后重试或改用压缩原图策略中允许的路径，但仍不得改用 OCR 绘制）。
     - 无英文营销叠加的工厂照/证书/实拍图 → 不调用多米，原图压缩后按西语文件名上传即可。
     - 禁止把会“重新设计海报”的生图结果直接上线。
  ③ 用原文 alt 译成西语后作为图片文件名（--output-name / 上传文件名），并填写 alt 与 title。
  ④ 后台发布填写 title 和 description，内容同原文链接对应 SEO/元信息的西语翻译。
  ⑤ 文章的 SEO 各元素要保留。
  ⑥ 西语正文开头补充标题，字号 18pt；删除正文内超链接。
  ⑦ 正文翻译后若出现 Google Translate 的 Error 500/Server Error 字符串，必须重试修复后才能发布。
6）本页应处理文章全部成功后：更新 progress.json（page=N+1，记录 last_completed_page、last_run 含每篇 title_en/title_es/url/status），提交并推送到 main。生成图可放在 output/duomi/（大图默认可不提交）；必须提交 progress.json。
7）在本次 Cursor 运行记录中说明：本页处理了哪些文章、每篇发布链接、失败项与原因、每张图用了 duomi 还是仅重命名/压缩、duomi 输出路径。
8）前 26 页已完成，勿重做。当前以 progress.json 的 page 为准；勿重做 last_completed_page 及更早页面。

实现细节（必须遵循）：
- WordPress：cookie 登录 wp-login.php + 管理后台 wpApiSettings 的 X-WP-Nonce 调用 REST；不要依赖 Basic Auth / Application Password。
- 媒体与文章：cookie+nonce 下 POST /wp-json/wp/v2/media 与 /wp-json/wp/v2/posts；西语分类 id=89。
- Yoast SEO：创建/发布后，通过 /wp-admin/post.php 提交（须带上完整 content，避免正文被清空），并带 yoast_free_metabox_nonce，写入 yoast_wpseo_title、yoast_wpseo_metadesc，以及 OG/Twitter 图片字段；然后用 REST 再设置 featured_media。
- 仅当本页 5 篇全部成功后才把 progress.json 的 page 更新为 N+1 并推送到 main。

无需发送邮件通知。
```

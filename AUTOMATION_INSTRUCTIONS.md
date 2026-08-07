# Xindun Spanish Automation — Agent Instructions

Paste the relevant block below into the Automation **Agent Instructions** field.
Cloud Agents cannot use the local `/image` skill; use `scripts/duomi_image.py` (Duomi gpt-image-2).

## Required secrets (Cloud Agents dashboard)

- `DUOMI_API_KEY` — Duomi gpt-image-2 key（原始 key，不加 Bearer）
- `WP_USER` / `WP_APP_PASSWORD` — 西语站 WordPress 登录密码（cookie 登录用）

## 多米 gpt-image-2 必跑命令（替换 /image）

本环境用 **`python3`**（不要写 `python`，云端常找不到）。

```bash
pip install -r requirements.txt

python3 scripts/duomi_image.py \
  --image-url "<原文图片公开 HTTPS URL>" \
  --prompt "Edit this exact image. Keep layout/products/background/aspect ratio unchanged. Only translate English marketing/diagram overlay text to Spanish. Do NOT change product casing text, logos, model numbers, certificates, Chinese exhibition signs, or wall company names (Xindun / Xindun GREEN POWER / XINDUN POWER)." \
  --output-name "<西语alt文件名不含扩展名>" \
  --max-kb 100 \
  --print-json
```

### 强制规则

1. **有英文营销/图解叠加文案的配图：必须先调用上述多米命令**，不可只做 OCR 就跳过。
2. 密钥只用环境变量 `DUOMI_API_KEY`（原始 key，不加 `Bearer`）。
3. `--image-url` 必须是可公开访问的原文 HTTPS URL（不可传本地路径）。
4. `--output-name` = 原文 `alt` 的西语翻译（文件名 stem，无扩展名）。
5. 成品要求：宽高与原图一致、JPEG ≤100KB。
6. 多米默认常输出约 `2048x1360`（3:2）。出图后若分辨率/比例与原图不同：
   - 先缩放到原图 **WxH**，再 JPEG 压缩到 ≤100KB；
   - 若宽高比相对原图偏差 **>5%**，或版面/产品被改写 → **丢弃多米结果**，回退 OCR 原地替换（或无英文叠加时仅压缩原图）。
7. 脚本 `--max-kb` 若因超大 PNG 报 `Could not compress ... under 100KB`：保留原始多米出图，自行 Pillow 缩放到原图尺寸后再压 JPEG，**不要**因此跳过「已调用多米」这一步。
8. 无英文叠加文案的实拍/产品照：不调用多米，原图压缩后上传即可。
9. 勿改：机身/铭牌文字、logo、型号、证书章、中文展板、墙面公司名（Xindun / Xindun GREEN POWER / XINDUN POWER）。

---

## A) 每日西语新闻发布 Agent（copy everything below）

```text
你是负责 Xindun 西语新闻发布的自动化 Agent。在仓库 XindunPower/xindunsolar 的 main 分支执行。严格按步骤做，不要重做已完成页。

【图片工具 — 重要｜必须调用多米】
不要调用 /image Skill（云端不可用）。凡正文主图/配图带英文营销或图解叠加文案的，必须先跑多米：
  pip install -r requirements.txt
  python3 scripts/duomi_image.py \
    --image-url "<原文图片公开 HTTPS URL>" \
    --prompt "Edit this exact image. Keep layout/products/background/aspect ratio unchanged. Only translate English marketing/diagram overlay text to Spanish. Do NOT change product casing text, logos, model numbers, certificates, Chinese exhibition signs, or wall company names (Xindun / Xindun GREEN POWER / XINDUN POWER)." \
    --output-name "<西语alt文件名不含扩展名>" \
    --max-kb 100 \
    --print-json
密钥只用 DUOMI_API_KEY（原始 key，不加 Bearer）。参考图必须是可公开访问的 HTTPS URL。
多米后处理：缩放到原图 WxH，JPEG≤100KB；若比例相对原图偏差>5%或改版面/产品 → 丢弃并回退 OCR 原地替换。无英文叠加则仅压缩原图，不调多米。
汇报里必须写清每张图是否调用了 duomi_image.py、输出路径、采用/丢弃原因。

1）读取仓库根目录 progress.json，取字段 page 作为当前页码 N。若不存在则从 27 起并创建该文件。
2）打开 https://www.xindun-power.com/news/{N}.html ，取出该页 5 篇文章（标题与原文链接）。
3）对照 https://www.xindunsolar.com/category/spanish 检查这 5 篇是否已有西语版并已发布。
4）未发布的：翻译成西班牙语并发布到西语站。
5）发布要求：
  ① 全文翻译，不能删减内容；
  ② 主图和配图：有英文叠加则必须先 duomi_image.py；保留原版面，机身/铭牌文字不改；长宽同原图，成品 ≤100KB；
  ③ 用原文 alt 译成西语后作为图片文件名（--output-name），并填写 alt 与 title；
  ④ 后台发布填写 title 与 description，内容同原文链接对应 SEO/元信息；
  ⑤ 保留文章 SEO 各元素；
  ⑥ 西语正文开头补充标题，字号 18pt；删除正文内超链接。
6）本页应处理文章全部成功后：更新 progress.json（page=N+1，记录 last_completed_page、last_run 含每篇 title_en/title_es/url/status），提交到 main。生成图可放在 output/duomi/（默认可不提交大图）；必须提交 progress.json。
7）在本次 Cursor 运行记录中说明：本页处理了哪些文章、每篇发布链接、失败项与原因、每张图是否调用多米及采用/回退路径。
8）勿重做 last_completed_page 及更早页面。当前以 progress.json 的 page 为准。

无需发送邮件通知。
```

---

## B) 已发布文章配图修复 Agent（copy everything below）

```text
你是 Xindun 西语站「已发布文章配图修复」Agent。仓库：XindunPower/xindunsolar，分支 main。
本次只修复已发布文章的配图，不要新翻译整页新闻，不要推进 progress.json 的 page。

【图片工具】
- 不要调用本机 /image Skill。
- 有英文营销/图解叠加文案的配图：必须调用多米 gpt-image-2（不可只 OCR 就交差）：
  pip install -r requirements.txt
  python3 scripts/duomi_image.py \
    --image-url "<原文图片公开 HTTPS URL>" \
    --prompt "Edit this exact image. Keep layout/products/background/aspect ratio unchanged. Only translate English marketing/diagram overlay text to Spanish. Do NOT change product casing text, logos, model numbers, certificates, Chinese exhibition signs, or wall company names (Xindun / Xindun GREEN POWER / XINDUN POWER)." \
    --output-name "<西语alt文件名不含扩展名>" \
    --max-kb 100 \
    --print-json
- 密钥只用环境变量 DUOMI_API_KEY（原始 key，不加 Bearer）。
- 多米后处理：缩放到原图 WxH 并 JPEG≤100KB；若 --max-kb 因超大 PNG 失败，保留出图后自行压缩，仍算已调用多米。
- 多米结果若改版面/产品/比例（相对原图宽高比偏差>5%）→ 丢弃并回退 OCR 原地替换；无英文叠加文案则原图压缩后重传。
- 汇报必须逐图写明：调用了 duomi_image.py / OCR / 仅压缩，以及采用或丢弃原因。

【对每篇文章】
1) 打开西语已发布页，列出当前配图（含特色图）的 media URL / attachment id（能拿到就记）。
2) 找到对应英文原文页，取出同序主图/配图的原图 HTTPS URL 与原文 alt。
3) 按图片规则生成替换图：宽高同原图，JPEG≤100KB；alt/title 用原文 alt 的西语翻译；文件名用西语 alt。
4) WordPress：cookie 登录 wp-login.php + wpApiSettings 的 X-WP-Nonce；
   - POST /wp-json/wp/v2/media 上传新图；
   - 更新 posts：替换正文 img，并设置 featured_media（如需）；分类保持西语 id=89，不要改标题正文（除非你只为修图必须改 img HTML）。
5) 若 Yoast/OG 用到旧图，一并更新相关图片字段（post.php + yoast_free_metabox_nonce；保存后再 REST 确认 featured_media）。
6) 发布后打开前台核对：西语文案是否正确、版面是否与原文一致、图片是否≤100KB。

【完成汇报】
逐篇列出：西语 URL、替换了几张图、新旧媒体链接、用了 OCR / duomi_image.py / 仅压缩、失败项与原因。
不要修改 progress.json。
```

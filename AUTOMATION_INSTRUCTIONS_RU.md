# 俄语新闻发布 — 自动化说明

把下面「Agent Instructions」整段贴进自动化 **Xindun 俄语新闻翻译发布** 的 Agent Instructions。

https://cursor.com/automations/e1c15e4c-e189-11f1-8120-06b44be262b7

云端虚拟机从快照启动，工作区里的 `progress_ru.json` 经常落后于 main。开工前必须先 `git fetch origin main`，只认远端页码。

## Agent Instructions

```text
你是负责 Xindun 俄语新闻发布的自动化 Agent。在仓库 XindunPower/xindunsolar 的 main 分支执行。严格按以下步骤执行。西语与法语任务已结束，本任务只做俄语，不与其他语言任务并行。

0）先同步进度，再做任何翻译、改图或发布。云端快照里的 progress_ru.json 经常是旧的。
   git fetch origin main
   git show origin/main:progress_ru.json
   以 origin/main 里的 page 作为当前页码 N。
   若本地 progress_ru.json 的 page 小于 origin/main，这是旧快照：立刻停止。不要翻译，不要调用多米，不要登录 WordPress，不要重做已完成页。
   也可以运行 python3 scripts/sync_news_progress.py progress_ru.json。退出码 3 表示本地进度已落后并被 origin/main 覆盖，同样立刻停止并改读更新后的 page。退出码 0 才可以继续。
   fetch 失败时也不要开工。不要读取或改动西语 progress.json、法语 progress_fr.json。

【图片工具 — 重要】
- 不要调用本机 /image Skill（云端不可用）。
- 有英文营销/示意图叠加文案的图片：必须用仓库脚本多米改图：
    pip install -r requirements.txt
    python3 scripts/duomi_image.py \
      --image-url "<原文图片公开 HTTPS URL>" \
      --prompt "Edit this exact image. Keep layout/products/background/aspect ratio unchanged. Only translate English marketing/diagram overlay text to Russian. Do NOT change product casing text, logos, model numbers, certificates, Chinese exhibition signs, or wall company names (Xindun / Xindun GREEN POWER / XINDUN POWER)." \
      --size "<按原图比例选择，如 3:2>" \
      --output-name "<俄语 alt 文件名不含扩展名>" \
      --max-kb 100 \
      --print-json
  密钥只用环境变量 DUOMI_API_KEY（原始 key，不加 Bearer）。参考图必须是可公开访问的 HTTPS URL。
  俄语改图在扣积分前会再核对 origin/main。进度落后时脚本会拒绝请求，不要改用别的方式绕过。
- 禁止：用 OCR 识别英文叠加文字再在原图上绘制/覆盖（不得作为改图方案）。
- 工厂照、证书、纯实拍/产品图等没有英文营销叠加文案的图片：不要调用多米；使用原图（按需压缩到 ≤100KB），按俄语 alt 重命名后上传，并填写 alt/title。

1）在第 0 步确认 origin/main 的 progress_ru.json 之后，取其 page 作为当前页码 N。若不存在则从第 1 页起并创建该文件（page=1）。
2）打开 https://www.xindun-power.com/news/{N}.html ，取出该页 5 篇文章（标题与原文链接）。列表解析用 div.title.clearfix 的 title 与链接。第 1 页是 https://www.xindun-power.com/news/index.html（news/1.html 返回 404）。
3）不要检查是否已有俄语页面或已发布俄语版（俄语新闻尚未发布过）。本页 5 篇全部翻译成俄语并发布。同一原文链接已经记在 progress_ru.json 里的，不要再发第二篇。
4）发布要求：
  ① 按原文前台阅读体验翻译，不要按 HTML 碎片翻译。先打开原文页面，按读者看到的标题、段落、列表、图表说明、图注来理解整篇，再写成通顺俄语；禁止把源码拆成标签/短句逐段机翻后拼回去。保留等效版式（标题层级、段落、列表、表格、图片位置），但翻译对象是可读正文，不是 HTML 节点。
  ② 全文翻译，不能删减内容；正文取 pageNewsDetailsBox，截止到 Related posts 之前。
  ③ 主图和配图必须与原文完全一致：不能修改图片版面/构图/产品/背景，不能变形；只将图片上的英文营销文案或示意图标签翻译成俄语。产品机身/铭牌文字不用修改；公司墙上的公司名（如 Xindun、Xindun GREEN POWER、XINDUN POWER）不需要翻译。图片长宽同原图且 JPEG ≤100KB。
     - 有英文营销/示意图叠加文案 → 必须用 scripts/duomi_image.py（多米 gpt-image-2）改图；改完后做版面一致性校验（宽高对齐原图；若改变版面/产品/比例，一律丢弃并回退原图后重试；仍不得改用 OCR 绘制）。
     - 无英文营销叠加的工厂照/证书/实拍图 → 不调用多米，原图压缩后按俄语文件名上传即可。
     - 禁止把会“重新设计海报”的生图结果直接上线。
  ④ 用原文 alt 译成俄语后作为图片文件名（--output-name / 上传文件名），并填写 alt 与 title。
  ⑤ 后台发布填写 title 和 description，内容同原文链接对应 SEO/元信息的俄语翻译。
  ⑥ 文章的 SEO 各元素要保留。
  ⑦ WordPress 文章标题已经是页面 H1。不要在正文开头再补一条 18pt 标题。删除正文内超链接。特色图只设 featured_media，不要再插入正文。
  ⑧ 正文翻译后若出现 Google Translate 的 Error 500/Server Error 字符串，必须重试修复后才能发布。
  ⑨ 每篇俄语文章必须加上标签 Русский（名称必须完全一致）。分类必须设置为 Русский（id=125，slug=russian）；创建/发布时传 categories: [125]。不要使用西语分类 id=89、法语分类，或其他语言分类。
5）本页 5 篇全部成功后：更新 progress_ru.json（page=N+1，记录 last_completed_page、last_run 含每篇 title_en/title_ru/url/status/published_url），提交并推送到 main。推送前再 git fetch origin main；若远端 page 已经大于本地，不要用旧进度覆盖 main。下一轮任务必须以更新后的 page 为准，自动处理下一页，勿重做本页。生成图可放在 output/duomi/（大图默认可不提交）；必须提交 progress_ru.json。任一篇失败则不要推进页码。
6）在本次 Cursor 运行记录中说明：本页处理了哪些文章、每篇发布链接、是否已打上 Русский 标签并归入 Русский 分类、失败项与原因、每张图用了 duomi 还是仅重命名/压缩、duomi 输出路径。
7）俄语从第 1 页开始。当前以 origin/main 上 progress_ru.json 的 page 为准；勿重做 last_completed_page 及更早页面。

实现细节（必须遵循）：
- 翻译方法：以原文前台阅读体验为准，不要按 HTML 碎片翻译。不要按标签、class、内联样式或被拆开的短节点逐条翻译；先按页面呈现理解全文，再输出俄语正文。
- WordPress：cookie 登录 wp-login.php + 管理后台 wpApiSettings 的 X-WP-Nonce 调用 REST；不要依赖 Basic Auth / Application Password。
- 媒体与文章：cookie+nonce 下 POST /wp-json/wp/v2/media 与 /wp-json/wp/v2/posts。
- 分类 Русский：固定使用 categories: [125]（slug=russian）。不要传空分类，不要使用 Uncategorized。
- 标签 Русский：先 GET /wp-json/wp/v2/tags?search=Русский（或按 name/slug 精确匹配）。若无同名标签，则 POST /wp-json/wp/v2/tags 创建 name=Русский（建议 slug=russkiy）。创建/发布文章时传 tags: [<该 tag id>] 且 categories: [125]。不要误用现有标签 RUS（id=69）。
- Yoast SEO：创建/发布后，通过 /wp-admin/post.php 提交（须带上完整 content，避免正文被清空），并带 yoast_free_metabox_nonce，写入 yoast_wpseo_title、yoast_wpseo_metadesc，以及 OG/Twitter 图片字段；然后用 REST 再设置 featured_media。
- 仅当本页 5 篇全部成功后才把 progress_ru.json 的 page 更新为 N+1 并推送到 main，供下一轮任务自动接下一页。

无需发送邮件通知。
```

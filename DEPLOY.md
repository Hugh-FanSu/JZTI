# JZTI · 鸡贼人格自测 —— 部署到 Vercel

> 目标：拿到一个公开网址（如 `https://jzti.vercel.app`），手机/微信打开即测，可分享、可病毒传播。
> 你这台机器没装 Node/Homebrew，所以下面 **路线 A（全程网页操作，零本地安装）** 最省事。

---

## 路线 A：GitHub 网页上传 + Vercel 导入（推荐，零安装）

### 1. 建一个 GitHub 仓库并上传 index.html
1. 打开 https://github.com/new ，仓库名随意（如 `jzti`），选 **Public**，点 **Create repository**。
2. 在新仓库页点 **uploading an existing file**（或 Add file → Upload files）。
3. 把本目录下的 **`index.html`** 和 **`vercel.json`** 拖进去上传，点 **Commit changes**。
   - 只需这两个文件；`app.py` / `scale_data.py` 是 Streamlit 版，部署静态页用不到。

### 2. 用 Vercel 导入
1. 打开 https://vercel.com ，用 GitHub 账号登录（Continue with GitHub）。
2. 点 **Add New… → Project**，找到刚建的 `jzti` 仓库，点 **Import**。
3. Framework Preset 选 **Other**（它会自动识别为静态站点），其它默认，点 **Deploy**。
4. 等十几秒，拿到网址 `https://jzti-xxx.vercel.app` —— 直接能用、自带 HTTPS。

### 3. （可选）自定义域名 / 短网址
- Vercel 项目 → **Settings → Domains** 可绑自己的域名。
- 之后改内容：在 GitHub 仓库里重新上传 `index.html`，Vercel 会自动重新部署。

---

## 路线 B：本地 Vercel CLI（需先装 Node）

适合你以后想本地一条命令部署。先装 Node（任选其一）：
- 官网装：https://nodejs.org 下载 LTS 版 `.pkg` 安装；
- 或装 Homebrew 后 `brew install node`。

装好后，在本目录执行：
```bash
cd ~/Downloads/鸡贼量表
npx vercel            # 首次会让你登录 + 几个回车，生成预览网址
npx vercel --prod     # 正式发布，拿到生产网址
```
`.vercelignore` 已配置好，只发布 `index.html`，自动排除 Python 文件。

---

## 🇨🇳 部署到阿里云 OSS（境内可访问 · 域名 jzti-test.icu 已备案）

> 单页静态站，OSS 几乎免费。只需上传一个 `index.html`。

1. **建 Bucket**：阿里云控制台 → 对象存储 OSS → 创建 Bucket。
   - 地域：选离用户近的（如华东 1·杭州）；读写权限：**公共读**。
2. **传文件**：把本目录的 **`index.html`** 上传到 Bucket 根目录（其它 `.py`/`vercel.*` 不用传）。
3. **开静态网站**：Bucket → 基础设置 → **静态页面** → 默认首页与默认 404 页都填 `index.html` → 保存。
4. **绑域名**：Bucket → 传输管理 → **域名管理** → 绑定自定义域名 `jzti-test.icu`
   （备案已过，可绑）→ 按提示去你的域名 DNS 加一条 **CNAME** 指向 Bucket 的外网域名。
5. **开 HTTPS**：阿里云「数字证书管理服务」申请免费 DV 证书（绑 `jzti-test.icu`）→ 回到 OSS 域名管理给该域名**上传/绑定证书并开启 HTTPS**。
   （站内 `SITE_URL` 已用 `https://`，所以务必开 HTTPS，二维码才对得上。）
6. **（可选）加 CDN**：阿里云 CDN 添加加速域名 `jzti-test.icu`，源站选该 OSS Bucket，配 HTTPS —— 访问更快更稳。

**更新内容**：以后改完 `index.html`，重新上传覆盖即可（CDN 记得刷新该文件缓存）。

### 统计（境内可用）
Vercel 统计在 OSS 上失效，已移除。注册 **51.la** 或 **百度统计** 后，把它给你的 `<script>` 代码贴到
`index.html` 里 `ANALYTICS_PLACEHOLDER` 那一行即可（数据只在你后台可见）。

---

## 传播小贴士
- **微信内打开**：Vercel 域名在国内多数可直连；若个别网络打不开，可在路线 A 第 3 步绑一个自己的域名，或换国内静态托管（对象存储 / 备案空间）。
- **朋友圈/群**：结果页有「🔗 分享给朋友」按钮，手机会调起系统分享并带上成绩文案；「📸 生成分享卡」可保存名片图，配图转发更易传播。
- **链接预览**：`index.html` 里已写好 `og:title` / `og:description`，发到支持预览的平台会显示标题和文案。

---

作者：公众号「人类行为研究室」 · 改造自公众号「铁围山」（鸡贼行为倾向量表 Chengdu Cunning Scale）

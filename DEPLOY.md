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

## 传播小贴士
- **微信内打开**：Vercel 域名在国内多数可直连；若个别网络打不开，可在路线 A 第 3 步绑一个自己的域名，或换国内静态托管（对象存储 / 备案空间）。
- **朋友圈/群**：结果页有「🔗 分享给朋友」按钮，手机会调起系统分享并带上成绩文案；「📸 生成分享卡」可保存名片图，配图转发更易传播。
- **链接预览**：`index.html` 里已写好 `og:title` / `og:description`，发到支持预览的平台会显示标题和文案。

---

作者：公众号「人类行为研究室」 · 改造自公众号「铁围山」（鸡贼行为倾向量表 Chengdu Cunning Scale）

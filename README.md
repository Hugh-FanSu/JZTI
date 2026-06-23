# JZTI · 鸡贼人格类型指标

> JīZéi Type Indicator —— 一个披着学术外衣的搞怪自测：20 题测出你的「鸡贼型号」。
> **本量表纯属娱乐，信效度为 0。**

测完会得到：4 字母 SBTI 式代号（如 `ADBL`）+ 名号（如「华尔街之狼」）、四维雷达图、鸡贼指数与段位、口头禅、天敌 / 绝配，以及一张可分享的「鸡贼名片」。

## 在线体验

👉 **https://jzti-test.icu/**（阿里云 OSS · 已备案，境内可访问）

## 文件说明

| 文件 | 用途 |
| --- | --- |
| `index.html` | ⭐ 纯静态单页（零依赖），**部署上线就靠它** |
| `vercel.json` | Vercel 部署配置 |
| `.vercelignore` | 部署时排除 Python 文件 |
| `app.py` / `scale_data.py` | Streamlit 版（本地 `streamlit run app.py`，可选） |
| `DEPLOY.md` | 部署步骤 |

## 本地预览

直接双击 `index.html` 即可，无需任何环境。

## 部署

见 [`DEPLOY.md`](./DEPLOY.md)。最省事：把 `index.html` + `vercel.json` 传到 GitHub 仓库，再到 vercel.com 导入即可。

---

作者：公众号「人类行为研究室」 · 改造自公众号「铁围山」（鸡贼行为倾向量表 Chengdu Cunning Scale）

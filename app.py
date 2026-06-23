# -*- coding: utf-8 -*-
"""JZTI · 鸡贼人格类型指标 —— Streamlit 自测应用。

运行：streamlit run app.py
"""
import io

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
import numpy as np
import streamlit as st

from scale_data import (
    AXES, ANCHORS, TYPES, TIERS, DIM_MID,
    dim_raw, dim_display, jindex, total_raw, raw_score, type_code, tier_of,
)

# ---------------------------------------------------------------------------
# 中文字体（matplotlib 画雷达图/分享卡用）
# ---------------------------------------------------------------------------
def _setup_cjk_font():
    candidates = [
        "PingFang SC", "Heiti SC", "Hiragino Sans GB", "STHeiti",
        "Songti SC", "Arial Unicode MS", "Microsoft YaHei", "SimHei",
        "Noto Sans CJK SC", "WenQuanYi Zen Hei",
    ]
    available = {f.name for f in font_manager.fontManager.ttflist}
    for name in candidates:
        if name in available:
            plt.rcParams["font.sans-serif"] = [name]
            break
    plt.rcParams["axes.unicode_minus"] = False


_setup_cjk_font()

st.set_page_config(page_title="JZTI · 鸡贼人格自测", page_icon="🦊", layout="centered")

ACCENT = "#E8743B"   # 主题橙
INK = "#2b2b2b"

# ---------------------------------------------------------------------------
# 样式
# ---------------------------------------------------------------------------
st.markdown(
    f"""
    <style>
      .block-container {{ max-width: 760px; }}
      .sbti-hero h1 {{ margin-bottom: .1rem; }}
      .sbti-sub {{ color:#888; font-size:.92rem; line-height:1.5; }}
      .dim-card {{
        background:#FFF7F2; border:1px solid #F3D9C8; border-radius:14px;
        padding:14px 18px 4px; margin:18px 0 8px;
      }}
      .dim-title {{ font-weight:700; color:{ACCENT}; font-size:1.05rem; }}
      .dim-sub {{ color:#a98; font-size:.82rem; margin-bottom:.2rem; }}
      .result-code {{
        font-size:3.2rem; font-weight:800; letter-spacing:.35rem;
        color:{ACCENT}; text-align:center; margin:.2rem 0;
      }}
      .result-title {{ text-align:center; font-size:1.9rem; font-weight:800; color:{INK}; }}
      .result-tag {{ text-align:center; color:#777; font-style:italic; margin-bottom:1rem; }}
      .quote-box {{
        border-left:4px solid {ACCENT}; background:#FBFBFB; padding:10px 16px;
        border-radius:0 10px 10px 0; color:#444; font-size:1.02rem; margin:8px 0;
      }}
      .pair-box {{ background:#F7F7F9; border-radius:12px; padding:12px 16px; margin:6px 0; }}
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# 顶部
# ---------------------------------------------------------------------------
st.markdown(
    """
    <div class="sbti-hero">
      <h1>🦊 JZTI · 鸡贼人格类型指标</h1>
      <div class="sbti-sub">
        JīZéi Type Indicator&nbsp;|&nbsp;基于「四维鸡贼行为模型」(4D-JBM)的非临床自评工具<br>
        共 20 题，约 2 分钟。请凭<b>第一反应</b>作答——关键不是“我有没有做过”，而是“我是不是经常这样想”。
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)
st.caption("⚠️ 特别声明：本量表纯属胡编，信效度为 0，结果仅供娱乐与自嘲。")
st.caption("作者：公众号「人类行为研究室」 · 改造自公众号「铁围山」（鸡贼行为倾向量表 Chengdu Cunning Scale）")

# ---------------------------------------------------------------------------
# 答题
# ---------------------------------------------------------------------------
RADIO_OPTS = list(range(len(ANCHORS)))  # 0..3（4 选项）

with st.form("sbti"):
    answers = {}
    for ax in AXES:
        st.markdown(
            f'<div class="dim-card"><div class="dim-title">{ax["dim"]}</div>'
            f'<div class="dim-sub">{ax["subtitle"]}</div></div>',
            unsafe_allow_html=True,
        )
        for item_id, text, _rev in ax["items"]:
            choice = st.radio(
                f"**{item_id}.** {text}",
                options=RADIO_OPTS,
                format_func=lambda i: ANCHORS[i],
                index=None,  # 强制选边，不预选
                horizontal=True,
                key=f"q{item_id}",
            )
            answers[item_id] = choice
    submitted = st.form_submit_button("🔮 出结果", use_container_width=True)

if submitted and any(v is None for v in answers.values()):
    st.warning("还有题没答完哦，请把 24 题都选上再出结果。")
    submitted = False


# ---------------------------------------------------------------------------
# 画图：雷达图 + 分享卡
# ---------------------------------------------------------------------------
def radar_figure(sums):
    """四维雷达图，返回 matplotlib Figure。sums: 4 个 5–25 的分数。"""
    labels = [ax["high"]["name"] for ax in AXES]  # 精算/闪躲/双标/薅毛
    vals = [dim_display(s) for s in sums]
    N = len(labels)
    angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
    vals_c = vals + vals[:1]
    angles_c = angles + angles[:1]

    fig, ax = plt.subplots(figsize=(4.6, 4.6), subplot_kw=dict(polar=True))
    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)
    ax.set_ylim(0, 100)
    ax.set_yticks([25, 50, 75, 100])
    ax.set_yticklabels(["", "", "", ""])
    ax.set_xticks(angles)
    ax.set_xticklabels(labels, fontsize=13)
    ax.plot(angles_c, vals_c, color=ACCENT, linewidth=2)
    ax.fill(angles_c, vals_c, color=ACCENT, alpha=0.25)
    ax.grid(color="#ddd")
    ax.spines["polar"].set_color("#ddd")
    fig.tight_layout()
    return fig


def share_card(code, info, tier_name, score, pct, sums):
    """生成一张可截图分享的结果卡（含小雷达图）。返回 PNG bytes。"""
    fig = plt.figure(figsize=(6.4, 8.4), dpi=160)
    fig.patch.set_facecolor("#FFFFFF")

    # 顶部色带
    fig.text(0.5, 0.955, "JZTI · 鸡贼人格类型指标", ha="center", fontsize=13, color="#999")
    fig.text(0.5, 0.905, code, ha="center", fontsize=46, fontweight="bold",
             color=ACCENT, fontfamily=plt.rcParams["font.sans-serif"][0])
    fig.text(0.5, 0.845, info["title"], ha="center", fontsize=26, fontweight="bold", color=INK)
    fig.text(0.5, 0.808, info["tagline"], ha="center", fontsize=12.5, color="#888", style="italic")

    # 雷达图嵌入
    labels = [ax["high"]["name"] for ax in AXES]
    vals = [dim_display(s) for s in sums]
    N = len(labels)
    angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
    rad = fig.add_axes([0.27, 0.40, 0.46, 0.32], polar=True)
    rad.set_theta_offset(np.pi / 2)
    rad.set_theta_direction(-1)
    rad.set_ylim(0, 100)
    rad.set_yticklabels([])
    rad.set_xticks(angles)
    rad.set_xticklabels(labels, fontsize=11)
    rad.plot(angles + angles[:1], vals + vals[:1], color=ACCENT, linewidth=2)
    rad.fill(angles + angles[:1], vals + vals[:1], color=ACCENT, alpha=0.25)
    rad.grid(color="#e3e3e3")

    fig.text(0.5, 0.345, f"段位：{tier_name}　|　鸡贼指数 {score}/100　|　也许击败 {pct}%",
             ha="center", fontsize=14, fontweight="bold", color=ACCENT)

    # 语录
    fig.text(0.5, 0.275, f"「{info['quote']}」", ha="center", fontsize=13,
             color="#444", wrap=True)

    # 天敌 / 绝配
    nem = TYPES[info["nemesis"]]["title"]
    mat = TYPES[info["match"]]["title"]
    fig.text(0.5, 0.185, f"天敌：{nem}（{info['nemesis']}）", ha="center", fontsize=12, color="#666")
    fig.text(0.5, 0.150, f"绝配：{mat}（{info['match']}）", ha="center", fontsize=12, color="#666")

    fig.text(0.5, 0.06, "测一测你的鸡贼型号 · JZTI", ha="center", fontsize=11, color="#bbb")
    fig.text(0.5, 0.038, "本量表纯属娱乐，信效度为 0", ha="center", fontsize=9, color="#ccc")
    fig.text(0.5, 0.018, "作者 公众号「人类行为研究室」 · 改造自公众号「铁围山」",
             ha="center", fontsize=8, color="#ccc")

    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight", facecolor="#FFFFFF")
    plt.close(fig)
    buf.seek(0)
    return buf.getvalue()


# ---------------------------------------------------------------------------
# 结果
# ---------------------------------------------------------------------------
if submitted:
    code, sums = type_code(answers)
    total = total_raw(answers)
    score = raw_score(total)   # 鸡贼指数（绝对分）
    pct = jindex(total)        # 百分位（相对排名）
    info = TYPES[code]
    tier_name, tier_en, tier_desc = tier_of(pct)

    st.markdown("---")
    st.markdown(f'<div class="result-code">{code}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="result-title">{info["title"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="result-tag">{info["tagline"]}</div>', unsafe_allow_html=True)

    c1, c2 = st.columns([1, 1])
    with c1:
        st.pyplot(radar_figure(sums))
    with c2:
        st.metric("鸡贼指数", f"{score} / 100")
        st.caption(f"🏆 鸡贼程度也许击败了 {pct}% 的用户")
        st.markdown(f"**段位　{tier_name}**  \n<span style='color:#999'>{tier_en}</span>",
                    unsafe_allow_html=True)
        st.progress(min(score, 100) / 100)
        # 各维度小条
        for ax, s in zip(AXES, sums):
            pole = ax["high"]["name"] if s >= DIM_MID else ax["low"]["name"]
            st.caption(f"{ax['dim'].split('·')[1].strip()}：{s}/30 → **{pole}**")

    st.markdown(f"#### 🧬 关于「{info['title']}」")
    st.write(info["desc"])
    st.markdown(f'<div class="quote-box">口头禅：「{info["quote"]}」</div>', unsafe_allow_html=True)

    nem, mat = TYPES[info["nemesis"]], TYPES[info["match"]]
    p1, p2 = st.columns(2)
    with p1:
        st.markdown(
            f'<div class="pair-box">☠️ <b>天敌</b><br>{nem["title"]}'
            f'<br><span style="color:#999">{info["nemesis"]}</span></div>',
            unsafe_allow_html=True)
    with p2:
        st.markdown(
            f'<div class="pair-box">💞 <b>绝配</b><br>{mat["title"]}'
            f'<br><span style="color:#999">{info["match"]}</span></div>',
            unsafe_allow_html=True)

    st.markdown(f"#### 🏅 段位解读 · {tier_name}")
    st.write(tier_desc)

    # 分享卡
    st.markdown("#### 📸 一键生成分享卡")
    card = share_card(code, info, tier_name, score, pct, sums)
    st.image(card, caption="长按/右键保存，或点下方按钮下载，发群里炫一下。", use_container_width=True)
    st.download_button("⬇️ 下载分享卡 (PNG)", data=card,
                       file_name=f"JZTI_{code}.png", mime="image/png",
                       use_container_width=True)

    st.caption("再读一遍声明：纯属娱乐，信效度为 0。算得越准，越说明我俩都挺闲。")
else:
    st.info("👆 答完 20 题，点「出结果」，揭晓你的鸡贼型号。")

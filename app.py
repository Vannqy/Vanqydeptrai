# -*- coding: utf-8 -*-
"""Vẽ đường tròn lượng giác & đồ thị sin, cos (nền đen) bằng matplotlib."""
import math
from fractions import Fraction

import matplotlib
matplotlib.use("Agg")  # không cần cửa sổ, dùng được trên server
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle

BG, FG = "#000000", "#f2f2f2"
AXIS, MUTED, GRID = "#9aa0a6", "#8a8f94", "#2a2a2a"
COS_C, SIN_C = "#00e5ff", "#ffb300"
ANGLE_C, TAN_C = "#69f0ae", "#d0a2ff"

plt.rcParams.update({
    "figure.facecolor": BG, "axes.facecolor": BG, "savefig.facecolor": BG,
    "text.color": FG, "axes.labelcolor": FG,
    "xtick.color": AXIS, "ytick.color": AXIS,
    "font.family": "DejaVu Sans",
})

SPECIAL = sorted({k * 30 for k in range(13)} | {45, 135, 225, 315})

EXACT = [(0.0, "0"), (0.5, "1/2"), (math.sqrt(2) / 2, "√2/2"),
         (math.sqrt(3) / 2, "√3/2"), (1.0, "1")]
EXACT_TAN = [(0.0, "0"), (1 / math.sqrt(3), "√3/3"), (1.0, "1"),
             (math.sqrt(3), "√3")]


# ---------------------------------------------------------------- định dạng
def fmt_deg(d):
    return f"{int(round(d))}°" if abs(d - round(d)) < 1e-6 else f"{d:.1f}°"


def fmt_rad(d):
    """Độ -> radian dạng phân số của π (nếu là số nguyên độ)."""
    if abs(d - round(d)) > 1e-6:
        return f"{math.radians(d):.3f}"
    f = Fraction(int(round(d)), 180)
    if f == 0:
        return "0"
    n, m = f.numerator, f.denominator
    top = "π" if n == 1 else f"{n}π"
    return top if m == 1 else f"{top}/{m}"


def val_str(v, table):
    sign = "−" if v < -1e-12 else ""
    a = abs(v)
    approx = f"{sign}{a:.4f}"
    for t, s in table:
        if abs(a - t) < 1e-9:
            exact = f"{sign}{s}"
            return exact if s in ("0", "1") else f"{exact} ≈ {approx}"
    return approx


def _clean(x):
    return 0.0 if abs(x) < 1e-12 else x


def values(deg):
    rad = math.radians(deg)
    return rad, _clean(math.cos(rad)), _clean(math.sin(rad))


def info(deg):
    """Chuỗi hiển thị cho các giá trị lượng giác tại góc deg."""
    rad, c, s = values(deg)
    if abs(c) < 1e-9:
        tan_txt = "không xác định"
    else:
        tv = s / c
        tan_txt = "rất lớn" if abs(tv) >= 1000 else val_str(tv, EXACT_TAN)
    return {
        "theta": f"{fmt_deg(deg)} = {fmt_rad(deg)} rad",
        "cos": val_str(c, EXACT),
        "sin": val_str(s, EXACT),
        "tan": tan_txt,
        "identity": f"cos²θ + sin²θ = {c * c:.3f} + {s * s:.3f} = 1",
    }


# ------------------------------------------------------------ đường tròn
def draw_circle(deg):
    rad, c, s = values(deg)
    fig = plt.figure(figsize=(6, 6), dpi=110, facecolor=BG)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(-1.6, 1.6)
    ax.set_ylim(-1.6, 1.6)
    ax.set_aspect("equal")
    ax.axis("off")

    # lưới mờ
    for t in np.arange(-1.5, 1.51, 0.5):
        ax.plot([t, t], [-1.5, 1.5], color=GRID, lw=0.7, zorder=0)
        ax.plot([-1.5, 1.5], [t, t], color=GRID, lw=0.7, zorder=0)

    # tia, vạch chia và nhãn các góc đặc biệt
    for d in SPECIAL[:-1]:
        r = math.radians(d)
        ax.plot([0, math.cos(r)], [0, math.sin(r)], color="#1c1c1c", lw=0.8, zorder=1)
        ax.plot([0.96 * math.cos(r), 1.04 * math.cos(r)],
                [0.96 * math.sin(r), 1.04 * math.sin(r)], color=AXIS, lw=1.2, zorder=2)
        label = "0" if d == 0 else f"{fmt_rad(d)}\n{d}°"
        ax.text(1.31 * math.cos(r), 1.31 * math.sin(r), label, ha="center",
                va="center", fontsize=9, color=MUTED, linespacing=1.1, zorder=3,
                bbox=dict(boxstyle="square,pad=0.12", fc=BG, ec="none"))

    ax.add_patch(Circle((0, 0), 1, fill=False, ec=FG, lw=1.8, zorder=2))

    # hai trục toạ độ
    arrow = dict(arrowstyle="-|>", color=AXIS, lw=1.3, shrinkA=0, shrinkB=0,
                 mutation_scale=14)
    ax.annotate("", xy=(1.58, 0), xytext=(-1.58, 0), arrowprops=arrow, zorder=2)
    ax.annotate("", xy=(0, 1.58), xytext=(0, -1.58), arrowprops=arrow, zorder=2)
    ax.text(1.57, -0.16, "trục cos", ha="right", va="center", fontsize=10,
            color=COS_C, style="italic")
    ax.text(0.07, 1.50, "trục sin", ha="left", va="center", fontsize=10,
            color=SIN_C, style="italic")
    ax.text(-0.06, -0.07, "O", ha="right", va="top", fontsize=12, color=FG)
    for v, txt in ((1, "1"), (-1, "−1")):
        ax.text(v, -0.09, txt, ha="center", va="top", fontsize=10, color=AXIS)
        ax.text(-0.06, v, txt, ha="right", va="center", fontsize=10, color=AXIS)
    for x, y, txt in ((1.38, 1.38, "I"), (-1.38, 1.38, "II"),
                      (-1.38, -1.38, "III"), (1.38, -1.38, "IV")):
        ax.text(x, y, txt, ha="center", va="center", fontsize=13,
                color="#4a4a4a", fontweight="bold")

    # ---- phần động theo góc ----
    tt = np.linspace(0, rad, max(2, int(deg) + 2))
    ax.plot(np.cos(tt), np.sin(tt), color=ANGLE_C, lw=4, alpha=0.9,
            solid_capstyle="round", zorder=3)
    ax.plot(0.25 * np.cos(tt), 0.25 * np.sin(tt), color=ANGLE_C, lw=2, zorder=3)
    if 20 < deg < 340:
        ax.text(0.42 * math.cos(rad / 2), 0.42 * math.sin(rad / 2), "θ",
                color=ANGLE_C, fontsize=14, ha="center", va="center", zorder=7,
                bbox=dict(boxstyle="square,pad=0.1", fc=BG, ec="none"))

    dash = (0, (4, 3))
    ax.plot([c, c], [s, 0], color=SIN_C, lw=1.6, ls=dash, alpha=0.85, zorder=3)
    ax.plot([c, 0], [s, s], color=COS_C, lw=1.6, ls=dash, alpha=0.85, zorder=3)
    ax.plot([0, c], [0, 0], color=COS_C, lw=5, solid_capstyle="round", zorder=4)
    ax.plot([0, 0], [0, s], color=SIN_C, lw=5, solid_capstyle="round", zorder=4)
    ax.plot([0, c], [0, s], color=FG, lw=2.2, zorder=5)
    ax.plot([c], [0], "o", color=COS_C, ms=7, zorder=6)
    ax.plot([0], [s], "o", color=SIN_C, ms=7, zorder=6)
    ax.plot([c], [s], "o", color=FG, ms=12, mec=ANGLE_C, mew=2.5, zorder=8)

    ax.text(1.16 * c, 1.16 * s, "M", color=FG, fontsize=14, fontweight="bold",
            ha="center", va="center", zorder=8)
    if abs(c) > 0.25:
        ax.text(c / 2, -0.15 if s >= 0 else 0.15, "cos θ", color=COS_C,
                fontsize=13, fontweight="bold", ha="center", va="center", zorder=7)
    if abs(s) > 0.2:
        ax.text(-0.17 if c >= 0 else 0.17, s / 2, "sin θ", color=SIN_C,
                fontsize=13, fontweight="bold", ha="center", va="center", zorder=7)
    return fig


# ---------------------------------------------------------------- đồ thị
def draw_graphs(deg):
    rad = math.radians(deg)
    fig, axes = plt.subplots(2, 1, figsize=(6, 6), dpi=110, facecolor=BG)
    fig.subplots_adjust(left=0.13, right=0.97, top=0.92, bottom=0.09, hspace=0.45)
    t = np.linspace(0, 2 * np.pi, 721)

    for ax, func, color, title in ((axes[0], np.sin, SIN_C, "y = sin θ"),
                                   (axes[1], np.cos, COS_C, "y = cos θ")):
        tr = t[t <= rad + 1e-9]
        y = float(func(rad))
        ax.axhline(0, color=AXIS, lw=1.0, zorder=1)
        ax.plot(t, func(t), color=color, lw=1.6, alpha=0.35, zorder=2)
        ax.plot(tr, func(tr), color=color, lw=3.2, zorder=3)
        ax.plot([rad, rad], [0, y], color=color, lw=1.3, ls="--", alpha=0.9, zorder=3)
        ax.plot([rad], [y], "o", color=color, ms=10, mec=FG, mew=1.6, zorder=5)

        ax.set_xlim(-0.2, 2 * np.pi + 0.2)
        ax.set_ylim(-1.3, 1.3)
        ax.set_xticks(np.arange(0, 2 * np.pi + 1e-9, np.pi / 2))
        ax.set_xticklabels(["0", "π/2", "π", "3π/2", "2π"], fontsize=10)
        ax.set_xticks(np.arange(0, 2 * np.pi + 1e-9, np.pi / 6), minor=True)
        ax.set_yticks([-1, -0.5, 0, 0.5, 1])
        ax.set_yticklabels(["−1", "−0,5", "0", "0,5", "1"], fontsize=10)
        ax.tick_params(which="minor", length=0)
        ax.grid(which="major", color="#333333", lw=0.8)
        ax.grid(which="minor", color="#1a1a1a", lw=0.6)
        ax.set_axisbelow(True)
        for sp in ax.spines.values():
            sp.set_color("#555555")
        ax.set_title(title, loc="left", color=color, fontsize=14,
                     fontweight="bold", pad=8)
    axes[1].set_xlabel("θ (radian)", fontsize=10, color=MUTED)
    return fig


import streamlit as st  # noqa: E402


st.set_page_config(page_title="Đường tròn lượng giác", page_icon="📐",
                   layout="wide")

st.session_state.setdefault("deg", 30)
st.session_state.setdefault("playing", False)
st.session_state.setdefault("speed", 2)
st.session_state.setdefault("jump", None)


# ------------------------------------------------------------- callback
def change(delta):
    st.session_state.deg = (st.session_state.deg + delta) % 360


def jump_to_special():
    v = st.session_state.jump
    if v is not None:
        st.session_state.deg = int(v)
        st.session_state.jump = None


def chip(label, value, color):
    return (
        f'<div style="flex:1;min-width:150px;padding:10px 14px;border-radius:10px;'
        f'background:#111;border:1px solid {color}55">'
        f'<div style="font-size:0.8rem;color:#8a8f94">{label}</div>'
        f'<div style="font-size:1.15rem;font-weight:700;color:{color}">{value}</div>'
        f'</div>'
    )


# ---------------------------------------------------------------- giao diện
st.title("📐 Đường tròn lượng giác")
st.caption("Kéo thanh trượt để quay điểm M trên đường tròn đơn vị và quan sát "
           "sin θ, cos θ thay đổi.")

c1, c2 = st.columns([1, 2])
with c1:
    st.toggle("▶ Tự quay", key="playing")
with c2:
    st.select_slider("Tốc độ quay", options=[1, 2, 3, 5, 8], key="speed",
                     disabled=not st.session_state.playing)


def view():
    # Khi đang tự quay, tăng góc TRƯỚC khi vẽ thanh trượt
    if st.session_state.playing:
        change(st.session_state.speed)

    st.slider("Góc θ (độ)", 0, 360, step=1, key="deg")
    deg = st.session_state.deg

    b1, b2, b3, b4 = st.columns(4)
    b1.button("−15°", on_click=change, args=(-15,), use_container_width=True)
    b2.button("−1°", on_click=change, args=(-1,), use_container_width=True)
    b3.button("+1°", on_click=change, args=(1,), use_container_width=True)
    b4.button("+15°", on_click=change, args=(15,), use_container_width=True)

    st.selectbox("Chọn nhanh góc đặc biệt", SPECIAL, index=None,
                 key="jump", on_change=jump_to_special,
                 format_func=lambda d: f"{d}° = {fmt_rad(d)} rad",
                 placeholder="Chọn một góc đặc biệt…")

    v = info(deg)
    st.markdown(
        '<div style="display:flex;flex-wrap:wrap;gap:10px;margin:8px 0 14px">'
        + chip("Góc θ", v["theta"], ANGLE_C)
        + chip("cos θ  (hoành độ M)", v["cos"], COS_C)
        + chip("sin θ  (tung độ M)", v["sin"], SIN_C)
        + chip("tan θ", v["tan"], TAN_C)
        + "</div>",
        unsafe_allow_html=True,
    )

    left, right = st.columns(2)
    with left:
        fig = draw_circle(deg)
        st.pyplot(fig)
        plt.close(fig)
    with right:
        fig = draw_graphs(deg)
        st.pyplot(fig)
        plt.close(fig)

    st.caption(f"Hệ thức cơ bản:  {v['identity']}")


# Chỉ tự làm mới theo chu kỳ khi bật "Tự quay"
st.fragment(view, run_every=0.3 if st.session_state.playing else None)()

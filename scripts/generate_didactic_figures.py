"""Figures for the 14-slide didactic presentation."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyBboxPatch
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "slides" / "figures_didatica"
OUT.mkdir(parents=True, exist_ok=True)

BLUE = "#0071A4"
ORANGE = "#EF6C00"
BROWN = "#3D3528"
RED = "#D32F2F"
SKY = "#1E88E5"


def _style() -> None:
    plt.rcParams.update(
        {
            "font.family": "Arial",
            "axes.edgecolor": BROWN,
            "axes.labelcolor": BROWN,
            "xtick.color": BROWN,
            "ytick.color": BROWN,
            "text.color": BROWN,
            "axes.titlecolor": BROWN,
            "figure.facecolor": "white",
            "axes.facecolor": "white",
            "axes.spines.top": False,
            "axes.spines.right": False,
        }
    )


def fig_voltage_cloud() -> None:
    rng = np.random.default_rng(7)
    x = rng.normal(5.00, 0.04, 280)
    y = rng.normal(0.0, 0.12, 280)
    fig, ax = plt.subplots(figsize=(6.2, 5.4), dpi=180)
    ax.scatter(x, y, s=18, c=SKY, alpha=0.55, linewidths=0, zorder=2)
    ax.axvline(5.00, color=ORANGE, lw=2.2, zorder=3)
    ax.scatter([5.00], [0], s=90, c=ORANGE, zorder=4)
    ax.text(5.00, 0.42, "5,00 V", ha="center", fontsize=14, color=ORANGE, fontweight="bold")
    ax.set_xlim(4.82, 5.18)
    ax.set_ylim(-0.55, 0.55)
    ax.set_yticks([])
    ax.set_xlabel("Tensão possível (V)")
    ax.set_title("Indicação ≠ valor conhecido sem incerteza", fontsize=12)
    fig.tight_layout()
    fig.savefig(OUT / "01_indicacao_5V.png", bbox_inches="tight")
    plt.close()


def fig_pipeline() -> None:
    fig, ax = plt.subplots(figsize=(10.5, 2.4), dpi=180)
    ax.set_xlim(0, 10.5)
    ax.set_ylim(0, 2.4)
    ax.axis("off")
    labels = [
        "Entradas\nincertas",
        "Amostragem\naleatória",
        "Modelo\nmatemático",
        "Resultados\nsimulados",
        "Análise\nestatística",
    ]
    xs = [0.25, 2.35, 4.45, 6.55, 8.65]
    for x, lab in zip(xs, labels):
        box = FancyBboxPatch(
            (x, 0.45),
            1.7,
            1.45,
            boxstyle="round,pad=0.04,rounding_size=0.12",
            facecolor="#E8F4F8",
            edgecolor=BLUE,
            linewidth=1.6,
        )
        ax.add_patch(box)
        ax.text(x + 0.85, 1.18, lab, ha="center", va="center", fontsize=10, color=BROWN)
    for x in xs[:-1]:
        ax.annotate(
            "",
            xy=(x + 2.05, 1.18),
            xytext=(x + 1.78, 1.18),
            arrowprops=dict(arrowstyle="->", color=ORANGE, lw=1.8),
        )
    fig.tight_layout()
    fig.savefig(OUT / "02_pipeline.png", bbox_inches="tight")
    plt.close()


def fig_gaussian() -> None:
    x = np.linspace(-4.2, 4.2, 600)
    y = (1 / np.sqrt(2 * np.pi)) * np.exp(-0.5 * x**2)
    fig, ax = plt.subplots(figsize=(6.4, 5.2), dpi=180)
    ax.plot(x, y, color=BLUE, lw=2.4)
    for a, b, c, lab in [
        (-1, 1, "#90CAF9", "68%  ·  μ ± σ"),
        (-2, 2, "#BBDEFB", "95%  ·  μ ± 2σ"),
        (-3, 3, "#E3F2FD", "99,7%  ·  μ ± 3σ"),
    ]:
        xs = np.linspace(a, b, 200)
        ys = (1 / np.sqrt(2 * np.pi)) * np.exp(-0.5 * xs**2)
        ax.fill_between(xs, ys, color=c, zorder=1)
    ax.plot(x, y, color=BLUE, lw=2.4, zorder=3)
    ax.set_xticks([-3, -2, -1, 0, 1, 2, 3], ["μ−3σ", "μ−2σ", "μ−σ", "μ", "μ+σ", "μ+2σ", "μ+3σ"])
    ax.set_yticks([])
    ax.set_xlim(-4.2, 4.2)
    ax.set_ylim(0, 0.45)
    ax.set_title("Gaussiana: faixas clássicas", fontsize=12)
    ax.text(0, 0.22, "68%", ha="center", color=BLUE, fontsize=11)
    fig.tight_layout()
    fig.savefig(OUT / "03_gaussiana.png", bbox_inches="tight")
    plt.close()


def fig_resistance_hist() -> None:
    rng = np.random.default_rng(42)
    n = 80_000
    v = rng.normal(5.00, 0.05, n)
    i = rng.normal(0.100, 0.002, n)
    r = v / i
    uc = float(r.std(ddof=1))
    fig, ax = plt.subplots(figsize=(6.4, 5.2), dpi=180)
    ax.hist(r, bins=70, color=SKY, alpha=0.85, density=True, edgecolor="none")
    ax.axvline(50.0, color=ORANGE, lw=2.0, label="50,0 Ω")
    ax.axvline(r.mean(), color=RED, lw=1.4, ls="--", label=f"média {r.mean():.2f} Ω")
    ax.set_xlabel("Resistência R = V / I  (Ω)")
    ax.set_ylabel("Densidade")
    ax.set_title(f"Monte Carlo:  u(R) ≈ {uc:.2f} Ω   (GUM ≈ 1,12 Ω)", fontsize=11)
    ax.legend(frameon=False, fontsize=9)
    fig.tight_layout()
    fig.savefig(OUT / "04_histograma_R.png", bbox_inches="tight")
    plt.close()
    print(f"R mean={r.mean():.4f}  u={uc:.4f}")


def fig_calibration_mc() -> None:
    """Voltmeter calibration y = a x + b, then Monte Carlo on a, b and V_corr."""
    rng = np.random.default_rng(21)
    x_ref = np.array([1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0])
    a_true, b_true = 1.008, -0.015
    u_ref, u_ind = 0.002, 0.008
    y_obs = a_true * x_ref + b_true + rng.normal(0.0, u_ind, size=x_ref.size)

    n = 30_000
    a_s = np.empty(n)
    b_s = np.empty(n)
    ones = np.ones_like(x_ref)
    for k in range(n):
        x_k = x_ref + rng.normal(0.0, u_ref, size=x_ref.size)
        y_k = y_obs + rng.normal(0.0, u_ind, size=x_ref.size)
        a_s[k], b_s[k] = np.polyfit(x_k, y_k, 1)

    y_star = 5.00
    v_corr = (y_star - b_s) / a_s
    rho = float(np.corrcoef(a_s, b_s)[0, 1])
    a_hat, b_hat = float(a_s.mean()), float(b_s.mean())
    v_mean, v_u = float(v_corr.mean()), float(v_corr.std(ddof=1))

    fig, axes = plt.subplots(2, 1, figsize=(5.4, 6.4), dpi=180, gridspec_kw={"hspace": 0.38})
    ax0, ax1 = axes

    ax0.scatter(a_s[::6], b_s[::6], s=10, c=SKY, alpha=0.28, linewidths=0)
    ax0.scatter([a_hat], [b_hat], s=55, c=ORANGE, zorder=3)
    ax0.set_xlabel("inclinação  a")
    ax0.set_ylabel("intercepto  b  (V)")
    ax0.set_title(f"a e b correlacionados  (ρ ≈ {rho:.2f})", fontsize=11)

    ax1.hist(v_corr, bins=55, color=SKY, alpha=0.88, density=True, edgecolor="none")
    ax1.axvline(v_mean, color=ORANGE, lw=2.0, label=f"média {v_mean:.4f} V")
    ax1.set_xlabel("Tensão corrigida em 5,00 V  (V)")
    ax1.set_ylabel("Densidade")
    ax1.set_title(f"u(V_corr) ≈ {v_u*1e3:.1f} mV", fontsize=11)
    ax1.legend(frameon=False, fontsize=9)

    fig.tight_layout()
    fig.savefig(OUT / "05_calibracao_MC.png", bbox_inches="tight")
    plt.close()
    print(
        f"calib a={a_hat:.5f} b={b_hat:.5f} V  rho={rho:.3f}  "
        f"Vcorr={v_mean:.5f} u={v_u:.5f} V"
    )


def copy_gif() -> None:
    src = ROOT / "Pi_monte_carlo_all.gif"
    dest = OUT / "pi_quarto_circulo.gif"
    dest.write_bytes(src.read_bytes())
    im = Image.open(src)
    im.seek(im.n_frames - 1)
    frame = im.convert("RGB")
    frame.save(OUT / "pi_quarto_circulo_final.png")


if __name__ == "__main__":
    _style()
    fig_voltage_cloud()
    fig_pipeline()
    fig_gaussian()
    fig_resistance_hist()
    fig_calibration_mc()
    copy_gif()
    print("wrote", OUT)

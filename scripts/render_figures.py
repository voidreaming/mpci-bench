#!/usr/bin/env python3
"""Render the site's scientific figures from paper Tables 4 and 5.

Requires Python 3 and matplotlib (``python -m pip install matplotlib``).
Run from any directory: ``python scripts/render_figures.py``.
No data is fetched at render time; exact values and provenance are in figure-data.json.
"""

import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.ticker import PercentFormatter


ROOT = Path(__file__).resolve().parents[1]
DATA = json.loads((ROOT / "scripts/figure-data.json").read_text())
OUT = ROOT / "dist/assets/results"
OUT.mkdir(parents=True, exist_ok=True)

BLUE = "#2878b5"
ORANGE = "#d87831"
INK = "#343a40"
GRAY = "#737d88"
GRID = "#e5e9ec"

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 13,
    "text.color": INK,
    "axes.labelcolor": INK,
    "xtick.color": GRAY,
    "ytick.color": INK,
    "axes.edgecolor": "#c5cdd3",
    "axes.linewidth": .7,
    "svg.fonttype": "none",
    "svg.hashsalt": "mpci-bench-figures-v1",
    "figure.facecolor": "white",
    "axes.facecolor": "white",
    "savefig.facecolor": "white",
})


def save(fig, name, title, description):
    """Keep SVG deterministic; provide a high-resolution PNG download as well."""
    fig.savefig(OUT / f"{name}.svg", metadata={
        "Date": None,
        "Title": title,
        "Description": description,
        "Creator": "MPCI-Bench; Matplotlib",
    })
    svg = OUT / f"{name}.svg"
    svg.write_text("\n".join(line.rstrip() for line in svg.read_text().splitlines()) + "\n")
    fig.savefig(OUT / f"{name}.png", dpi=180, metadata={
        "Title": title,
        "Description": description,
    })
    plt.close(fig)


def modality_leakage():
    rows = DATA["action_results"]
    fig, ax = plt.subplots(figsize=(12, 7.1), dpi=100)
    fig.subplots_adjust(left=.235, right=.965, bottom=.13, top=.815)
    fig.text(.235, .949, "Images leak more often than text", fontsize=19, weight="bold")
    fig.text(.235, .906, "Negative cases: sharing would violate the privacy norm", fontsize=12.5, color=GRAY)

    for i, row in enumerate(rows):
        if i % 2 == 0:
            ax.axhspan(i-.47, i+.47, color="#f7f9fa", zorder=0)
        text_lr, image_lr = row["text_leakage"], row["visual_leakage"]
        ax.plot([text_lr, image_lr], [i, i], color="#d1d7dc", lw=2.4, zorder=2)
        for value, color, marker in ((text_lr, BLUE, "o"), (image_lr, ORANGE, "s")):
            ax.scatter([value], [i], s=65, color=color, marker=marker, zorder=4,
                       edgecolors="white", linewidths=.8)
            # Keep labels outside each connector, within the 0–100% plotting range.
            align, dx = ("right", -1.9) if color == BLUE else ("left", 1.9)
            ax.text(value+dx, i, f"{value:.1f}", ha=align, va="center", fontsize=12,
                    color=color, bbox={"facecolor": "white", "edgecolor": "none", "pad": .6}, zorder=5)

    ax.set_yticks(range(len(rows)), [row["model"] for row in rows], fontsize=12.5)
    ax.set_ylim(len(rows)-.5, -.65)
    ax.set_xlim(0, 100)
    ax.set_xticks(range(0, 101, 20))
    ax.xaxis.set_major_formatter(PercentFormatter(xmax=100, decimals=0))
    ax.set_xlabel("Leakage rate (%) · lower is better", labelpad=12, fontsize=13)
    ax.grid(axis="x", color=GRID, linewidth=.7)
    ax.set_axisbelow(True)
    ax.tick_params(axis="y", length=0, pad=13)
    ax.tick_params(axis="x", length=0, pad=8)
    for side in ("top", "left", "right"):
        ax.spines[side].set_visible(False)
    ax.legend(handles=[
        Line2D([], [], color=BLUE, marker="o", lw=0, markersize=7, label="Text leakage"),
        Line2D([], [], color=ORANGE, marker="s", lw=0, markersize=7, label="Visual leakage"),
    ], loc="lower left", bbox_to_anchor=(-.013, 1.005), ncol=2, frameon=False,
        fontsize=12.5, handletextpad=.55, columnspacing=1.8, borderaxespad=0)
    fig.text(.235, .025, "Source: MPCI-Bench, arXiv v3, Table 4. All 11 evaluated models.", fontsize=10.5, color=GRAY)
    save(fig, "modality-leakage", "Text and visual leakage across eleven models",
         "Table 4, arXiv:2601.08235v3. Visual leakage exceeds textual leakage for all eleven evaluated models. "
         "Visual leakage ranges from 56.9% to 91.6%; text leakage ranges from 20.2% to 45.2%. "
         "Rates are on negative cases where disclosure violates the privacy norm. Lower is better.")


def mitigation_tradeoff():
    fig, axes = plt.subplots(1, 2, figsize=(12, 7.6), dpi=100)
    fig.subplots_adjust(left=.085, right=.97, bottom=.185, top=.77, wspace=.25)
    fig.text(.085, .95, "Can prompting reduce leakage without losing utility?", fontsize=18.5, weight="bold")
    fig.text(.085, .907, "A useful safeguard moves toward the upper left: less leakage, more useful sharing.",
             fontsize=12.5, color=GRAY)

    # Explicit label coordinates keep dense high-utility results readable.
    labels = {
        "Mistral-Large-3": {
            "Default": (84, 78, "center"),
            "CI Filter": (24, 76, "center"),
            "Image Review": (44, 54, "center"),
            "Explicit Refuse": (75, 64, "center"),
            "CoT": (23, 24, "center"),
        },
        "Qwen3-VL-8B": {
            "Default": (87, 76, "center"),
            "CI Filter": (17, 75, "center"),
            "Image Review": (80, 42, "center"),
            "Explicit Refuse": (40, 57, "center"),
            "CoT": (64, 66, "center"),
        },
    }
    styles = {
        "Default": (ORANGE, "o"),
        "CI Filter": (BLUE, "o"),
        "Image Review": (GRAY, "s"),
        "Explicit Refuse": (GRAY, "D"),
        "CoT": (GRAY, "^"),
    }
    for ax, model in zip(axes, ("Mistral-Large-3", "Qwen3-VL-8B")):
        ax.set_title(model, loc="left", fontsize=15.5, fontweight="bold", pad=16)
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)
        ax.set_xticks(range(0, 101, 20))
        ax.set_yticks(range(0, 101, 20))
        ax.xaxis.set_major_formatter(PercentFormatter(xmax=100, decimals=0))
        ax.yaxis.set_major_formatter(PercentFormatter(xmax=100, decimals=0))
        ax.grid(color=GRID, linewidth=.7)
        ax.set_axisbelow(True)
        ax.tick_params(length=0, pad=8, labelsize=11)
        ax.set_xlabel("Visual leakage · lower is better", labelpad=12, fontsize=12)
        for side in ("top", "right"):
            ax.spines[side].set_visible(False)
        ax.scatter([0], [100], marker="*", s=160, color=INK, zorder=6, clip_on=False)
        ax.text(3, 98, "Ideal", va="top", fontsize=10.5, color=GRAY)

        rows = [row for row in DATA["mitigation_results"] if row["model"] == model]
        for row in rows:
            method = row["method"]
            x, y = row["visual_leakage"], row["visual_utility"]
            color, marker = styles[method]
            ax.scatter([x], [y], s=95 if method in ("CI Filter", "Default") else 65,
                       color=color, marker=marker, edgecolor="white", linewidth=.8, zorder=5)
            tx, ty, align = labels[model][method]
            label = method
            if method == "CI Filter":
                label += f"\n{x:.1f}% / {y:.1f}%"
            ax.annotate(label, xy=(x, y), xytext=(tx, ty), textcoords="data",
                        fontsize=11.5, ha=align, va="center", color=color,
                        fontweight="bold" if method == "CI Filter" else "normal",
                        bbox={"facecolor": "white", "edgecolor": "none", "pad": 1.7},
                        arrowprops={"arrowstyle": "-", "color": color, "lw": .8,
                                    "shrinkA": 4, "shrinkB": 6}, zorder=6)

    axes[0].set_ylabel("Visual utility · higher is better", labelpad=12, fontsize=12)
    fig.text(.085, .075, "Leakage: negative cases (sharing is inappropriate). Utility: positive cases (sharing is expected).",
             fontsize=10.5, color=GRAY)
    fig.text(.085, .042, "Source: MPCI-Bench, arXiv v3, Table 5. CI Filter labels show leakage / utility. CoT = chain-of-thought.",
             fontsize=10.5, color=GRAY)
    save(fig, "mitigation-tradeoff", "Privacy and utility under five prompting methods",
         "Table 5, arXiv:2601.08235v3. Two panels compare Default, CI Filter, Image Review, Explicit Refuse and CoT prompts "
         "for Mistral-Large-3 and Qwen3-VL-8B. The upper left is ideal. CI Filter yields 29.6% visual leakage and 92.0% "
         "visual utility for Mistral, and 13.1% leakage and 90.4% utility for Qwen. Mistral CoT has lower leakage "
         "at 8.6% but utility drops to 13.4%.")


def modality_leakage_panel():
    """A 468px-wide panel for a chart/table pair in a 960px content column."""
    rows = DATA["action_results"]
    fig, ax = plt.subplots(figsize=(6.5, 7.8), dpi=100)
    fig.subplots_adjust(left=.34, right=.97, bottom=.12, top=.795)
    fig.text(.03, .955, "Text vs. visual leakage", fontsize=16, weight="bold")
    fig.text(.03, .913, "Negative cases · lower is better", fontsize=12, color=GRAY)
    for i, row in enumerate(rows):
        if i % 2 == 0:
            ax.axhspan(i-.47, i+.47, color="#f7f9fa", zorder=0)
        text_lr, visual_lr = row["text_leakage"], row["visual_leakage"]
        ax.plot([text_lr, visual_lr], [i, i], color="#d1d7dc", lw=2, zorder=2)
        for value, color, marker in ((text_lr, BLUE, "o"), (visual_lr, ORANGE, "s")):
            ax.scatter([value], [i], s=47, color=color, marker=marker, zorder=4,
                       edgecolors="white", linewidths=.6)
            align, dx = ("left", 4) if color == BLUE else ("right", -4)
            ax.text(value+dx, i, f"{value:.1f}", ha=align, va="center", fontsize=12,
                    color=color, bbox={"facecolor": "white", "edgecolor": "none", "pad": .7}, zorder=5)

    ax.set_yticks(range(len(rows)), [row["model"] for row in rows], fontsize=12)
    ax.set_ylim(len(rows)-.5, -.65)
    ax.set_xlim(0, 100)
    ax.set_xticks([0, 50, 100])
    ax.xaxis.set_major_formatter(PercentFormatter(xmax=100, decimals=0))
    ax.get_xticklabels()[-1].set_horizontalalignment("right")
    ax.set_xlabel("Leakage rate", labelpad=9, fontsize=12)
    ax.grid(axis="x", color=GRID, linewidth=.65)
    ax.set_axisbelow(True)
    ax.tick_params(axis="y", length=0, pad=9)
    ax.tick_params(axis="x", length=0, pad=8, labelsize=12)
    for side in ("top", "left", "right"):
        ax.spines[side].set_visible(False)
    fig.legend(handles=[
        Line2D([], [], color=BLUE, marker="o", lw=0, markersize=6, label="Text"),
        Line2D([], [], color=ORANGE, marker="s", lw=0, markersize=6, label="Visual"),
    ], loc="lower left", bbox_to_anchor=(.018, .84), ncol=2, frameon=False,
        fontsize=12, handletextpad=.4, columnspacing=1.7, borderaxespad=0)
    fig.text(.03, .025, "Source: arXiv v3, Table 4 · all 11 models", fontsize=11.5, color=GRAY)
    save(fig, "modality-leakage-panel", "Text and visual leakage across eleven models",
         "Compact panel layout of Table 4, arXiv:2601.08235v3. Same values as the full-width chart. "
         "Visual leakage exceeds text leakage for every evaluated model. Lower leakage is better.")


def modality_leakage_mobile():
    """A narrow, stacked-row layout with readable text at 320–390 CSS pixels."""
    rows = DATA["action_results"]
    fig, ax = plt.subplots(figsize=(4.5, 9.3), dpi=100)
    fig.subplots_adjust(left=.065, right=.96, bottom=.082, top=.855)
    fig.text(.065, .962, "Text vs. image leakage", fontsize=15, weight="bold")
    fig.text(.065, .933, "Negative cases · lower is better", fontsize=11.5, color=GRAY)
    for i, row in enumerate(rows):
        if i % 2 == 0:
            ax.axhspan(i-.49, i+.48, color="#f7f9fa", zorder=0)
        ax.text(0, i-.28, row["model"], fontsize=11.7, va="center",
                bbox={"facecolor": "white" if i % 2 else "#f7f9fa", "edgecolor": "none", "pad": .6}, zorder=4)
        text_lr, image_lr = row["text_leakage"], row["visual_leakage"]
        ax.plot([text_lr, image_lr], [i+.14, i+.14], color="#d1d7dc", lw=2, zorder=2)
        for value, color, marker in ((text_lr, BLUE, "o"), (image_lr, ORANGE, "s")):
            ax.scatter([value], [i+.14], s=46, color=color, marker=marker, zorder=4,
                       edgecolors="white", linewidths=.6)
            align, dx = ("left", 3.7) if color == BLUE else ("right", -3.7)
            ax.text(value+dx, i+.14, f"{value:.1f}", ha=align, va="center", fontsize=11.5,
                    color=color, bbox={"facecolor": "white", "edgecolor": "none", "pad": .8}, zorder=5)

    ax.set_yticks([])
    ax.set_ylim(len(rows)-.5, -.5)
    ax.set_xlim(0, 100)
    ax.set_xticks([0, 50, 100])
    ax.xaxis.set_major_formatter(PercentFormatter(xmax=100, decimals=0))
    ax.get_xticklabels()[-1].set_horizontalalignment("right")
    ax.set_xlabel("Leakage rate", labelpad=8, fontsize=11.7)
    ax.grid(axis="x", color=GRID, linewidth=.65)
    ax.set_axisbelow(True)
    ax.tick_params(axis="x", length=0, pad=7, labelsize=11.5)
    for side in ("top", "left", "right"):
        ax.spines[side].set_visible(False)
    ax.legend(handles=[
        Line2D([], [], color=BLUE, marker="o", lw=0, markersize=6, label="Text"),
        Line2D([], [], color=ORANGE, marker="s", lw=0, markersize=6, label="Image"),
    ], loc="lower left", bbox_to_anchor=(-.02, 1.014), ncol=2, frameon=False,
        fontsize=11.7, handletextpad=.35, columnspacing=1.3, borderaxespad=0)
    fig.text(.065, .012, "Source: arXiv v3, Table 4 · all 11 models", fontsize=9.7, color=GRAY)
    save(fig, "modality-leakage-mobile", "Text and visual leakage across eleven models",
         "Mobile layout of Table 4, arXiv:2601.08235v3. Same values as the desktop chart. "
         "Visual leakage exceeds text leakage for every model. Lower leakage is better.")


def mitigation_tradeoff_mobile():
    """Stack the two model panels; short direct labels preserve all five methods."""
    fig = plt.figure(figsize=(4.5, 10.6), dpi=100)
    axes = [fig.add_axes([.20, .56, .76, .325]), fig.add_axes([.20, .125, .76, .325])]
    fig.text(.07, .975, "Less leakage. Useful sharing.", fontsize=14.5, weight="bold")
    fig.text(.07, .946, "Upper left is better", fontsize=11.5, color=GRAY)
    labels = {
        "Mistral-Large-3": {
            "Default": (84, 78),
            "CI Filter": (24, 72),
            "Image Review": (38, 47),
            "Explicit Refuse": (73, 54),
            "CoT": (25, 25),
        },
        "Qwen3-VL-8B": {
            "Default": (85, 74),
            "CI Filter": (16, 71),
            "Image Review": (78, 36),
            "Explicit Refuse": (39, 49),
            "CoT": (64, 62),
        },
    }
    styles = {
        "Default": (ORANGE, "o"),
        "CI Filter": (BLUE, "o"),
        "Image Review": (GRAY, "s"),
        "Explicit Refuse": (GRAY, "D"),
        "CoT": (GRAY, "^"),
    }
    for ax, model in zip(axes, ("Mistral-Large-3", "Qwen3-VL-8B")):
        ax.set_title(model, loc="left", fontsize=13.5, fontweight="bold", pad=16)
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)
        ax.set_xticks([0, 50, 100])
        ax.set_yticks([0, 50, 100])
        ax.xaxis.set_major_formatter(PercentFormatter(xmax=100, decimals=0))
        ax.yaxis.set_major_formatter(PercentFormatter(xmax=100, decimals=0))
        ax.get_xticklabels()[-1].set_horizontalalignment("right")
        ax.grid(color=GRID, linewidth=.7)
        ax.set_axisbelow(True)
        ax.tick_params(length=0, pad=6, labelsize=11)
        ax.set_xlabel("Visual leakage ↓", labelpad=8, fontsize=11.7)
        ax.set_ylabel("Visual utility ↑", labelpad=5, fontsize=11.7)
        for side in ("top", "right"):
            ax.spines[side].set_visible(False)
        ax.scatter([0], [100], marker="*", s=110, color=INK, zorder=6, clip_on=False)
        ax.text(4, 98, "Ideal", va="top", fontsize=10.5, color=GRAY)
        for row in (row for row in DATA["mitigation_results"] if row["model"] == model):
            method = row["method"]
            x, y = row["visual_leakage"], row["visual_utility"]
            color, marker = styles[method]
            ax.scatter([x], [y], s=65 if method in ("CI Filter", "Default") else 50,
                       color=color, marker=marker, edgecolor="white", linewidth=.6, zorder=5)
            label = method.replace("Image Review", "Image\nReview").replace("Explicit Refuse", "Explicit\nRefuse")
            ax.annotate(label, xy=(x, y), xytext=labels[model][method], textcoords="data",
                        fontsize=11.5, ha="center", va="center", color=color,
                        fontweight="bold" if method == "CI Filter" else "normal",
                        bbox={"facecolor": "white", "edgecolor": "none", "pad": 1.2},
                        arrowprops={"arrowstyle": "-", "color": color, "lw": .75,
                                    "shrinkA": 3, "shrinkB": 5}, zorder=6)
    fig.text(.07, .048, "CoT = chain-of-thought", fontsize=10.5, color=GRAY)
    fig.text(.07, .022, "Source: arXiv v3, Table 5", fontsize=10.5, color=GRAY)
    save(fig, "mitigation-tradeoff-mobile", "Privacy and utility under five prompting methods",
         "Mobile layout of Table 5, arXiv:2601.08235v3. Same values as the desktop chart. "
         "Mistral-Large-3 and Qwen3-VL-8B panels compare five methods. "
         "Upper left means low negative-case image leakage and high positive-case visual utility.")


if __name__ == "__main__":
    modality_leakage()
    modality_leakage_panel()
    mitigation_tradeoff()
    modality_leakage_mobile()
    mitigation_tradeoff_mobile()
    print(f"Rendered 2 figures in desktop/mobile layouts and a compact leakage panel (SVG and PNG) in {OUT}")

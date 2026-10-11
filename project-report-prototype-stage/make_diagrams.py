from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, FancyArrowPatch, FancyBboxPatch


OUT = Path(__file__).parent / "assets"
OUT.mkdir(exist_ok=True)
NAVY = "#16324f"
TEAL = "#087e82"
PALE = "#eef5f8"
GREEN = "#eaf5ed"
AMBER = "#fff4df"
GREY = "#566773"


def setup(title, width=12, height=6):
    fig, ax = plt.subplots(figsize=(width, height))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 7)
    ax.axis("off")
    ax.text(6, 6.67, title, ha="center", va="center", fontsize=16,
            fontweight="bold", color=NAVY)
    return fig, ax


def node(ax, xy, size, label, *, ellipse=False, color=PALE, font_size=12):
    x, y = xy
    width, height = size
    if ellipse:
        patch = Ellipse((x + width / 2, y + height / 2), width, height,
                        facecolor=color, edgecolor=TEAL, linewidth=1.8)
    else:
        patch = FancyBboxPatch(
            xy, width, height, boxstyle="round,pad=0.04,rounding_size=0.1",
            facecolor=color, edgecolor=NAVY, linewidth=1.8
        )
    ax.add_patch(patch)
    ax.text(x + width / 2, y + height / 2, label, ha="center", va="center",
            fontsize=font_size, color="#17202a", linespacing=1.4)


def flow(ax, start, end, label, *, curve=0, label_offset=(0, 0)):
    ax.add_patch(FancyArrowPatch(
        start, end, arrowstyle="-|>", mutation_scale=14, linewidth=1.5,
        color=GREY, connectionstyle=f"arc3,rad={curve}"
    ))
    mid_x = (start[0] + end[0]) / 2 + label_offset[0]
    mid_y = (start[1] + end[1]) / 2 + label_offset[1]
    ax.text(mid_x, mid_y, label, ha="center", va="center", fontsize=9,
            color="#34495e", bbox={"facecolor": "white", "edgecolor": "none", "pad": 2})


def architecture():
    fig, ax = setup("Prototype Architecture — Implemented Components")
    node(ax, (0.4, 3.0), (2.45, 1.55),
         "React + Vite Frontend\nPrompt • response\nFive scores • explanations\nLoading • errors")
    node(ax, (4.05, 3.0), (3.0, 1.55),
         "FastAPI Backend\nPOST /api/generate\nPOST /api/analyze • GET /api/health\nNo key + DEMO_MODE=true\n→ labelled demo sample",
         color=GREEN)
    node(ax, (8.75, 4.65), (2.8, 1.15),
         "Google Gemini API\nLive text generation", color=AMBER)
    node(ax, (8.75, 2.55), (2.8, 1.15),
         "Shared Heuristic Analyzer\nKeyword • sentence • length\ncoverage • format")
    flow(ax, (2.9, 4.1), (4.0, 4.1), "requests", label_offset=(0, .22))
    flow(ax, (4.0, 3.45), (2.9, 3.45), "response + scores",
         label_offset=(0, -.22))
    flow(ax, (7.1, 4.05), (8.7, 5.0), "prompt + server-side key",
         label_offset=(.2, .38))
    flow(ax, (8.7, 4.75), (7.1, 3.65), "generated response",
         curve=.16, label_offset=(.15, -.02))
    flow(ax, (7.1, 3.35), (8.7, 3.2), "prompt + response",
         label_offset=(0, .24))
    flow(ax, (8.7, 2.85), (7.1, 3.2), "scores + explanations",
         curve=.14, label_offset=(0, -.25))
    fig.tight_layout()
    fig.savefig(OUT / "architecture.png", dpi=180, bbox_inches="tight")
    plt.close(fig)


def dfd_level0():
    fig, ax = setup("DFD Level 0 — System Context")
    node(ax, (0.5, 3.0), (2.0, 1.3), "User", color=AMBER)
    node(ax, (4.35, 2.75), (3.2, 1.8),
         "0. Response Analysis\nPlatform\nGenerate • analyze • present",
         ellipse=True, font_size=12)
    node(ax, (9.45, 3.0), (2.0, 1.3),
         "External AI Provider\n(Google Gemini)", color=GREEN)
    flow(ax, (2.55, 4.0), (4.3, 4.0), "prompt", label_offset=(0, .22))
    flow(ax, (4.3, 3.0), (2.55, 3.0), "response + five scores",
         label_offset=(0, -.24))
    flow(ax, (7.6, 4.0), (9.4, 4.0), "generation request", label_offset=(0, .22))
    flow(ax, (9.4, 3.0), (7.6, 3.0), "generated text / error",
         label_offset=(0, -.24))
    fig.tight_layout()
    fig.savefig(OUT / "dfd_level0.png", dpi=180, bbox_inches="tight")
    plt.close(fig)


def dfd_level1():
    fig, ax = setup("DFD Level 1 — Prompt to Analysis Results")
    node(ax, (0.35, 4.45), (1.55, 1.0), "User", color=AMBER)
    node(ax, (2.55, 4.35), (2.15, 1.2), "1.0 Receive and\nvalidate prompt",
         ellipse=True)
    node(ax, (5.25, 4.35), (2.2, 1.2), "2.0 Generate response",
         ellipse=True, color=GREEN)
    node(ax, (9.7, 4.45), (1.95, 1.0), "Google Gemini API", color=AMBER)
    node(ax, (5.25, 1.65), (2.2, 1.2), "3.0 Analyze prompt\nand response",
         ellipse=True)
    node(ax, (9.0, 1.65), (2.35, 1.2), "4.0 Return response,\nscores and notes",
         ellipse=True, color=GREEN)
    flow(ax, (1.92, 4.95), (2.5, 4.95), "prompt", label_offset=(0, .2))
    flow(ax, (4.72, 4.95), (5.2, 4.95), "valid prompt", label_offset=(0, .2))
    flow(ax, (7.47, 5.05), (9.65, 5.05), "provider request", label_offset=(0, .2))
    flow(ax, (9.65, 4.65), (7.47, 4.65), "generated text / error",
         curve=.16, label_offset=(0, -.24))
    flow(ax, (6.35, 4.3), (6.35, 2.9), "prompt + generated response",
         label_offset=(.85, 0))
    flow(ax, (7.5, 2.25), (8.95, 2.25), "five 0–100 scores + explanations",
         label_offset=(0, .8))
    ax.plot([10.15, 10.15, 1.15], [1.65, 0.55, 0.55],
            color=GREY, linewidth=1.5)
    ax.add_patch(FancyArrowPatch(
        (1.15, 0.55), (1.15, 4.4), arrowstyle="-|>",
        mutation_scale=14, linewidth=1.5, color=GREY
    ))
    ax.text(5.6, 0.8, "response + scores returned to the browser",
            ha="center", va="center", fontsize=8, color="#34495e",
            bbox={"facecolor": "white", "edgecolor": "none", "pad": 2})
    ax.text(6, .2, "DEMO_MODE uses labelled sample output; no persistence or history store is implemented.",
            ha="center", va="center", fontsize=8, color=GREY)
    fig.tight_layout()
    fig.savefig(OUT / "dfd_level1.png", dpi=180, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    architecture()
    dfd_level0()
    dfd_level1()
    print(f"Created prototype diagrams in {OUT}")

"""Desenha assets/info-card.svg (estilo neofetch). Edite ROWS para mudar o texto."""
from html import escape
from pathlib import Path

from term import TITLE_BAR, window

ROWS = [
    ("Nome", "Israel Barros"),
    ("Agora", "Gestor de IA"),
    ("Local", "Brasil"),
    ("Stack", "TypeScript · JavaScript · Python · HTML/CSS"),
    ("Foco", "automações · gateway de pagamento"),
]
COLORS = ["#ff5f56", "#ffbd2e", "#27c93f", "#58a6ff", "#bc8cff", "#39c5cf", "#c9d1d9", "#8b949e"]
W, X, VX, STEP = 490, 28, 100, 26
Y0 = TITLE_BAR + 40

els = [
    f'<text class="g" x="{X}" y="{Y0}">xunaty@github</text>',
    f'<text class="dim" x="{X}" y="{Y0 + 16}">{"-" * 13}</text>',
]
for i, (k, v) in enumerate(ROWS):
    y = Y0 + 16 + STEP * (i + 1)
    els.append(f'<text x="{X}" y="{y}"><tspan class="k">{escape(k)}</tspan><tspan x="{VX}">{escape(v)}</tspan></text>')
bar_y = Y0 + 16 + STEP * len(ROWS) + 24
els.append("<g>" + "".join(f'<rect x="{X + i * 28}" y="{bar_y}" width="28" height="14" fill="{c}"/>' for i, c in enumerate(COLORS)) + "</g>")

body = "\n".join(f'<g class="r" style="animation-delay:{i * .12:.2f}s">{e}</g>' for i, e in enumerate(els))
css = ".g{fill:#27c93f;font-weight:bold;font-size:15px}.k{fill:#58a6ff;font-weight:bold}" \
      ".r{animation:in .5s ease-out both}@keyframes in{from{opacity:0;transform:translateX(-8px)}}"
out = Path(__file__).parent.parent / "assets/info-card.svg"
out.parent.mkdir(exist_ok=True)
out.write_text(window(W, bar_y + 14 + 24, "xunaty@github: ~", css, body))
print(out)

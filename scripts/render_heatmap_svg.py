"""Desenha assets/heatmap.svg a partir de data/contributions.json."""
import json
from datetime import date
from pathlib import Path

from term import TITLE_BAR, window

root = Path(__file__).parent.parent
data = json.loads((root / "data/contributions.json").read_text())

MESES = "jan fev mar abr mai jun jul ago set out nov dez".split()
LEVELS = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353"]
W, X0, Y0, CELL, PITCH = 860, 44, TITLE_BAR + 34, 12, 15
RIGHT = W - 24

first = date.fromisoformat(data["days"][0]["date"])  # sempre um domingo
body, prev_month, last_col = [], None, -9
for d in data["days"]:
    day = date.fromisoformat(d["date"])
    col, row = (day - first).days // 7, (day.weekday() + 1) % 7
    if row == 0 and day.month != prev_month and col - last_col >= 3:
        body.append(f'<text class="dim" x="{X0 + col * PITCH}" y="{Y0 - 8}" style="font-size:10px">{MESES[day.month - 1]}</text>')
        prev_month, last_col = day.month, col
    body.append(
        f'<rect class="c" x="{X0 + col * PITCH}" y="{Y0 + row * PITCH}" width="{CELL}" height="{CELL}" rx="2"'
        f' fill="{LEVELS[d["level"]]}" style="animation-delay:{(col + row) * .015:.2f}s"/>'
    )

for row, nome in ((1, "seg"), (3, "qua"), (5, "sex")):
    body.append(f'<text class="dim" x="{X0 - 8}" y="{Y0 + row * PITCH + 10}" text-anchor="end" style="font-size:10px">{nome}</text>')

legend_y = Y0 + 7 * PITCH + 8
sq_x = RIGHT - 24 - 6 - 5 * PITCH + 3
body.append(f'<text class="dim" x="{sq_x - 6}" y="{legend_y + 10}" text-anchor="end" style="font-size:10px">menos</text>')
body.append("".join(f'<rect x="{sq_x + i * PITCH}" y="{legend_y}" width="{CELL}" height="{CELL}" rx="2" fill="{c}"/>' for i, c in enumerate(LEVELS)))
body.append(f'<text class="dim" x="{RIGHT - 24}" y="{legend_y + 10}" style="font-size:10px">mais</text>')

best = data["best"]
bd = date.fromisoformat(best["date"])
stats_y = legend_y + 34
body.append(
    f'<text x="24" y="{stats_y}">{data["total"]} contribuições <tspan class="dim">·</tspan> sequência atual {data["current"]}d'
    f' <tspan class="dim">·</tspan> maior {data["longest"]}d <tspan class="dim">·</tspan>'
    f' melhor dia {best["count"]} ({bd.day} {MESES[bd.month - 1]})</text>'
)

css = ".c{animation:pop .4s ease-out both}@keyframes pop{from{opacity:0}}"
out = root / "assets/heatmap.svg"
out.parent.mkdir(exist_ok=True)
out.write_text(window(W, stats_y + 20, f'{data["user"].lower()}@github: ~/contribuicoes', css, "\n".join(body)))
print(out)

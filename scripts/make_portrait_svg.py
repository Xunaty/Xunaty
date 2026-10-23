"""Foto -> assets/portrait.svg (ASCII que "digita" uma vez e para).

Só roda local, quando a foto muda: pip install numpy opencv-python
Uso: python scripts/make_portrait_svg.py foto.jpg [x,y,largura,altura]
  x,y,largura,altura = recorte da foto, em pixels. O retrato atual usa a foto de 960x720 com 200,0,545,470.
shortcut: o fundo some só por ser escuro (funciona com pessoa bem iluminada em fundo escuro);
  com fundo claro ou cheio de detalhes, troque por cv2.grabCut ou rembg.
"""
import sys
from html import escape
from pathlib import Path

import cv2
import numpy as np

from term import TITLE_BAR, window

COLS, CW, ROW_H, PAD = 100, 3.5, 7, 10
RAMP = " .,:;irsXA253hMHGS#9B&@"  # do mais vazio ao mais denso
STAGGER, WIPE = 0.045, 0.5  # segundos entre linhas / duração da varredura de cada linha

img = cv2.imread(sys.argv[1])
if img is None:
    sys.exit(f"não consegui abrir {sys.argv[1]}")
h, w = img.shape[:2]
box = sys.argv[2] if len(sys.argv) > 2 else f"{w // 20},{h // 20},{w * 9 // 10},{h * 9 // 10}"
x, y, bw, bh = map(int, box.split(","))
bw, bh = min(bw, w - x), min(bh, h - y)

gray = cv2.createCLAHE(clipLimit=2, tileGridSize=(4, 4)).apply(cv2.cvtColor(img[y:y + bh, x:x + bw], cv2.COLOR_BGR2GRAY))

rows = round(COLS * bh / bw * CW / ROW_H)
g = cv2.resize(gray, (COLS, rows), interpolation=cv2.INTER_AREA).astype(float)

# fundo escuro: os 45% mais escuros viram espaço; gama 1.5 apaga a camisa e deixa rosto e mãos em destaque.
lo, hi = np.percentile(g, (45, 99.5))
t = np.clip((g - lo) / (hi - lo), 0, 1) ** 1.5
idx = (t * (len(RAMP) - 1)).round().astype(int)
lines = ["".join(RAMP[i] for i in row).rstrip() for row in idx]

W, top, full = round(COLS * CW) + 2 * PAD, TITLE_BAR + PAD, COLS * CW
total = (rows - 1) * STAGGER + WIPE
body = []
for i, line in enumerate(lines):
    if not line:
        continue
    ry = top + i * ROW_H
    a, b = i * STAGGER / total, (i * STAGGER + WIPE) / total
    kt = f'keyTimes="0;{a:.4f};{b:.4f};1" dur="{total:.2f}s" fill="freeze"'
    # sem SMIL o estado padrão (largura cheia) mostra tudo; com SMIL a linha começa recortada em 0.
    body.append(
        f'<clipPath id="c{i}"><rect x="{PAD}" y="{ry}" width="{full}" height="{ROW_H}">'
        f'<animate attributeName="width" values="0;0;{full};{full}" {kt}/></rect></clipPath>'
        f'<text class="a" x="{PAD}" y="{ry + ROW_H - 1.5}" textLength="{len(line) * CW}" lengthAdjust="spacing"'
        f' xml:space="preserve" clip-path="url(#c{i})">{escape(line)}</text>'
        f'<rect x="{PAD}" y="{ry}" width="{CW}" height="{ROW_H - 1}" fill="#c9d1d9" opacity="0">'
        f'<animate attributeName="x" values="{PAD};{PAD};{PAD + full};{PAD + full}" {kt}/>'
        f'<animate attributeName="opacity" calcMode="discrete" values="0;1;0" keyTimes="0;{a:.4f};{b:.4f}" dur="{total:.2f}s" fill="freeze"/></rect>'
    )

out = Path(__file__).parent.parent / "assets/portrait.svg"
out.parent.mkdir(exist_ok=True)
out.write_text(window(W, top + rows * ROW_H + PAD, "xunaty@github: ~/foto", f".a{{font-size:{CW / .6:.2f}px}}", "\n".join(body)))
print(f"{out}: {COLS}x{rows} caracteres")

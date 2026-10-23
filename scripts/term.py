"""Moldura de janela de terminal compartilhada pelos SVGs."""

FONT = "ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"
TITLE_BAR = 34


def window(w, h, title, css, body):
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{title}">
<style>
text{{font-family:{FONT};font-size:13px;fill:#c9d1d9}}
.dim{{fill:#8b949e}}
@media (prefers-reduced-motion:reduce){{*{{animation:none!important}}}}
{css}
</style>
<rect x=".5" y=".5" width="{w - 1}" height="{h - 1}" rx="10" fill="#0d1117" stroke="#30363d"/>
<path d="M.5 {TITLE_BAR}H{w - .5}" stroke="#30363d"/>
<circle cx="20" cy="17" r="5" fill="#ff5f56"/><circle cx="38" cy="17" r="5" fill="#ffbd2e"/><circle cx="56" cy="17" r="5" fill="#27c93f"/>
<text x="76" y="21" class="dim" style="font-size:12px">{title}</text>
{body}
</svg>
"""

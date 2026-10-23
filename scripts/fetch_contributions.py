"""Baixa o calendário público de contribuições (sem token) e grava data/contributions.json.

Uso: python scripts/fetch_contributions.py <usuario>
"""
import json
import re
import sys
import urllib.request
from pathlib import Path

user = sys.argv[1]
html = urllib.request.urlopen(f"https://github.com/users/{user}/contributions", timeout=30).read().decode()

# shortcut: regex presa à ordem dos atributos do HTML do GitHub; troque por html.parser se quebrar.
counts = {i: int(n or 0) for i, n in re.findall(r'for="(contribution-day-component-\d+-\d+)"[^>]*>(?:No|(\d+)) contribution', html)}
days = [
    {"date": d, "level": int(lv), "count": counts[i]}
    for d, i, lv in re.findall(r'data-date="([\d-]+)" id="([^"]+)" data-level="(\d)"', html)
]
if not days or len(days) != len(counts):
    sys.exit("HTML do GitHub mudou: não achei o calendário de contribuições")

days.sort(key=lambda d: d["date"])

run = longest = 0
for d in days:
    run = run + 1 if d["count"] else 0
    longest = max(longest, run)

current = 0
for d in reversed(days):
    if d["count"]:
        current += 1
    elif d is not days[-1]:  # hoje ainda sem contribuição não zera a sequência
        break

out = Path(__file__).parent.parent / "data/contributions.json"
out.parent.mkdir(exist_ok=True)
out.write_text(json.dumps({
    "user": user,
    "total": sum(d["count"] for d in days),
    "current": current,
    "longest": longest,
    "best": max(days, key=lambda d: d["count"]),
    "days": days,
}, indent=1))
print(f"{out}: {len(days)} dias, {sum(d['count'] for d in days)} contribuições")

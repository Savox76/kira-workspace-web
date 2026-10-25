"""Baut die Webseite aus src/seite.html: index.html (Deutsch) und en/index.html (Englisch).

Im Text steht jede Übersetzung als {{deutsch||english}} direkt nebeneinander, {{R}} ist der Weg zur Wurzel.
Aufruf: python3 build.py
"""
import pathlib
import re

ROOT = pathlib.Path(__file__).parent
SRC = (ROOT / "src" / "seite.html").read_text(encoding="utf-8")
PAIR = re.compile(r"\{\{((?:(?!\{\{|\}\}).)*?)\|\|((?:(?!\{\{|\}\}).)*?)\}\}", re.S)


def render(lang: str, root: str) -> str:
    out = SRC.replace("{{R}}", root)
    out = PAIR.sub(lambda m: m.group(1) if lang == "de" else m.group(2), out)
    left = re.findall(r"\{\{.*?\}\}", out)
    if left:
        raise SystemExit(f"Unvollständige Platzhalter ({lang}): {left[:3]}")
    return out


(ROOT / "index.html").write_text(render("de", ""), encoding="utf-8")
(ROOT / "en").mkdir(exist_ok=True)
(ROOT / "en" / "index.html").write_text(render("en", "../"), encoding="utf-8")
print("index.html, en/index.html")

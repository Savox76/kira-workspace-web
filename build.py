"""Baut die Webseite aus src/: Startseite, Impressum und Datenschutz – jeweils Deutsch und Englisch.

Schreibweise in den Vorlagen:
  {{deutsch||english}}   Übersetzung direkt nebeneinander (darf verschachtelt sein)
  {{R}}                  Weg zur Wurzel ("" bzw. "../")
  {{TEIL:fuss}}          fügt src/teile/fuss.html ein
  {{F:name}}             Feld aus daten/impressum.json,  {{F?telefon:…}} nur wenn das Feld gefüllt ist
  {{NEUIGKEITEN}}        Abschnitt „Neu in Kira“ aus daten/kira.json (schreibt der Release-Workflow von Kira)

Impressum und Datenschutz entstehen erst, wenn name, strasse, ort und email in daten/impressum.json stehen.
Aufruf: python3 build.py
"""
import datetime as dt
import html
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).parent
SRC = ROOT / "src"
PAIR = re.compile(r"\{\{((?:(?!\{\{|\}\}).)*?)\|\|((?:(?!\{\{|\}\}).)*?)\}\}", re.S)
PFLICHT = ("name", "strasse", "ort", "email")
MONATE = ["Januar", "Februar", "März", "April", "Mai", "Juni", "Juli", "August", "September", "Oktober", "November", "Dezember"]
STAND = ("Oktober 2026", "October 2026")   # bei Änderungen an src/datenschutz.html anpassen
MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

# Seiten je Sprache: (Datei, Weg zur Wurzel)
PAGES = {
    "de": {"start": ("index.html", ""), "impressum": ("impressum.html", ""), "datenschutz": ("datenschutz.html", "")},
    "en": {"start": ("en/index.html", "../"), "impressum": ("en/legal-notice.html", "../"), "datenschutz": ("en/privacy.html", "../")},
}


def load_json(name: str) -> dict:
    p = ROOT / "daten" / name
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}


KIRA = load_json("kira.json")
IMP = {k: str(v).strip() for k, v in load_json("impressum.json").items() if not k.startswith("_")}
LEGAL = all(IMP.get(k) for k in PFLICHT)


def rel(lang: str, page: str, from_root: str) -> str:
    return from_root + PAGES[lang][page][0]


def datum(iso: str, lang: str) -> str:
    try:
        d = dt.date.fromisoformat(iso)
    except ValueError:
        return ""
    return f"{d.day}. {MONATE[d.month - 1]} {d.year}" if lang == "de" else f"{MONTHS[d.month - 1]} {d.day}, {d.year}"


def news(lang: str) -> str:
    items = KIRA.get("neuigkeiten") or []
    if not items:
        return ""
    rows = "\n".join(
        f'        <li><span class="news-v">{html.escape(i["version"])}</span>'
        f'<time datetime="{html.escape(i.get("datum", ""))}">{datum(i.get("datum", ""), lang)}</time>'
        f'<span class="news-t">{html.escape(i["de"] if lang == "de" else i["en"])}</span></li>' for i in items)
    head = "Neu in Kira" if lang == "de" else "What’s new in Kira"
    lead = (f"Kira wird laufend weiterentwickelt. Aktuell ist Version {KIRA.get('version', '')}." if lang == "de"
            else f"Kira is under active development. The current version is {KIRA.get('version', '')}.")
    return (f'  <section id="neu" aria-labelledby="neu-h">\n    <div class="wrap news">\n      <div class="intro"><h2 id="neu-h">{head}</h2>'
            f'<p>{lead}</p></div>\n      <ol class="news-list">\n{rows}\n      </ol>\n    </div>\n  </section>')


def legal_links(lang: str, root: str) -> str:
    if not LEGAL:
        return ""
    a = (f'<a href="{rel(lang, "impressum", root)}">{"Impressum" if lang == "de" else "Legal notice"}</a>'
         f'<a href="{rel(lang, "datenschutz", root)}">{"Datenschutz" if lang == "de" else "Privacy"}</a>')
    return a


def render(text: str, lang: str, page: str) -> str:
    root = PAGES[lang][page][1]
    other = "en" if lang == "de" else "de"
    text = re.sub(r"\{\{TEIL:(\w+)\}\}", lambda m: (SRC / "teile" / f"{m.group(1)}.html").read_text(encoding="utf-8"), text)
    stand = STAND[0] if lang == "de" else STAND[1]
    values = {
        "R": root, "START": rel(lang, "start", root), "DATENSCHUTZ": rel(lang, "datenschutz", root),
        "GEGENSTUECK": rel(other, page, root), "NEUIGKEITEN": news(lang), "RECHTLICHES": legal_links(lang, root),
        "TITEL": {"impressum": "{{Impressum||Legal notice}}", "datenschutz": "{{Datenschutz||Privacy}}"}.get(page, "Kira"),
    }
    for k, v in values.items():
        text = text.replace("{{" + k + "}}", v)
    fields = {**IMP, "stand": stand}
    text = re.sub(r"\{\{F:(\w+)\}\}", lambda m: html.escape(fields.get(m.group(1), "")), text)
    while True:
        new = PAIR.sub(lambda m: m.group(1) if lang == "de" else m.group(2), text)
        if new == text:
            break
        text = new
    text = re.sub(r"\{\{F\?(\w+):((?:(?!\{\{|\}\}).)*?)\}\}", lambda m: m.group(2) if fields.get(m.group(1)) else "", text, flags=re.S)
    left = re.findall(r"\{\{.*?\}\}", text)
    if left:
        raise SystemExit(f"Unvollständige Platzhalter ({lang}/{page}): {left[:3]}")
    return text


def write(path: str, content: str) -> None:
    p = ROOT / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")
    print(path)


main = (SRC / "seite.html").read_text(encoding="utf-8")
frame = (SRC / "rechtliches.html").read_text(encoding="utf-8")
for lang in ("de", "en"):
    write(PAGES[lang]["start"][0], render(main, lang, "start"))
    for page in ("impressum", "datenschutz"):
        target = ROOT / PAGES[lang][page][0]
        if LEGAL:
            body = (SRC / f"{page}.html").read_text(encoding="utf-8")
            write(PAGES[lang][page][0], render(frame.replace("{{INHALT}}", body), lang, page))
        elif target.exists():
            target.unlink()   # ohne vollständige Angaben keine halbe Rechtsseite veröffentlichen
if not LEGAL:
    print("Hinweis: Impressum und Datenschutz fehlen noch – bitte daten/impressum.json ausfüllen.")

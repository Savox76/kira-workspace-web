# Kira · Hermes Workspace – Webseite

Die öffentliche Seite über Kira (GitHub Pages). Deutsch unter `/`, Englisch unter `/en/`.

## Bearbeiten

Text und Aufbau stehen in `src/seite.html`. Jede Übersetzung steht direkt nebeneinander als `{{Deutsch||English}}`,
`{{R}}` ist der Weg zur Wurzel. Danach bauen:

```bash
python3 build.py      # schreibt index.html und en/index.html
```

`index.html` und `en/index.html` werden mit eingecheckt – GitHub Pages liefert sie direkt aus (Branch `main`, Ordner `/`).

- Gestaltung: `assets/site.css` (Farben und Schriften wie in der App: Nachtblau & Messing, Bricolage Grotesque, IBM Plex Sans – lokal eingebunden, keine fremden Server)
- Bilder: `assets/img/` – Bildschirmfotos von Kira mit Testdaten, als WebP

Downloads und Update-Kanal kommen später dazu.

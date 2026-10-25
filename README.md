# Kira · Hermes Workspace – Webseite

Die öffentliche Seite über Kira (GitHub Pages). Deutsch unter `/`, Englisch unter `/en/`.

## Bearbeiten

Text und Aufbau stehen in `src/seite.html`. Jede Übersetzung steht direkt nebeneinander als `{{Deutsch||English}}`,
`{{R}}` ist der Weg zur Wurzel. Danach bauen:

```bash
python3 build.py      # schreibt index.html und en/index.html
```

Die fertigen Seiten werden mit eingecheckt – GitHub Pages liefert sie direkt aus (Branch `main`, Ordner `/`). Der Workflow „Seiten bauen“ baut sie bei jeder Änderung an `src/`, `daten/` oder `assets/` automatisch neu.

## Daten

- `daten/impressum.json` – Angaben für Impressum und Datenschutz (Name, Anschrift, E-Mail). Erst wenn sie vollständig sind, erscheinen beide Seiten und die Links im Fuß.
- `daten/kira.json` – Version und „Neu in Kira“. Schreibt der Release-Workflow von Kira (Secret `KIRA_WEB_TOKEN` im Repo `hermes_workspace`).

- Gestaltung: `assets/site.css` (Farben und Schriften wie in der App: Nachtblau & Messing, Bricolage Grotesque, IBM Plex Sans – lokal eingebunden, keine fremden Server)
- Bilder: `assets/img/` – Bildschirmfotos von Kira mit Testdaten, als WebP

Downloads und Update-Kanal kommen später dazu.

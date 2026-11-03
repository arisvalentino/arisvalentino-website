# Quellcode – arisvalentino.com

Dieser Branch (`quellcode`) enthält den Quellcode der Website. Der Branch `main` ist die fertige, live ausgelieferte Seite (GitHub Pages, Domain arisvalentino.com über Strato-DNS: A 185.199.108.153, www CNAME arisvalentino.github.io).

## Aufbau
- `site/index.html` – Hauptseite (Fans), Quelle der Wahrheit, direkt bearbeiten
- `site/booking.html` – Booking-Seite (Veranstalter), direkt bearbeiten
- `site/lifeline/index.html` – LIFELINE-Albumseite (/lifeline/), eigenständig, Songs in `TRACKS` (src + status "single"), Audio in `site/lifeline/audio/` (AAC .m4a)
- `site/img`, `site/vid2`, `site/audio`, `site/fonts`, `site/downloads` – Medien
- Englische Texte stehen als `data-en`-Attribute in denselben Dateien; `build_site.py` rendert DE (/) und EN (/en/) vor.
- `build_site.py` – baut `dist/` (SEO, JSON-LD, Sitemap, Impressum, Datenschutz, 404). Impressum: nur „Aris Valentino“ (Künstlername im Ausweis eingetragen, bewusst so gewünscht).
- `make_github.py` – macht aus `dist/` die GitHub-Pages-Version `github/` (CNAME, .nojekyll, Weiterleitungsseiten für alte WordPress-URLs).
- `build_years.py` – Hilfsskript für das Show-Archiv.

## Veröffentlichen
```
python3 -W ignore -I build_site.py "$PWD"
python3 -I make_github.py "$PWD"
```
Dann den Inhalt von `github/` in den Branch `main` kopieren, committen, pushen.
Hero-Foto tauschen: `site/img/hero-wide.jpg` ersetzen (wird zu `img/aris-valentino-pop-rock-saenger.jpg`).

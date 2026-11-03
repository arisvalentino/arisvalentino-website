"""Turn dist/ (Netlify build) into github/ for GitHub Pages: no _redirects/_headers,
CNAME + .nojekyll, and small forwarding pages for the old WordPress URLs."""
import os, shutil, sys

base = sys.argv[1]
src, out = os.path.join(base, 'dist'), os.path.join(base, 'github')
if os.path.exists(out):
    shutil.rmtree(out)
shutil.copytree(src, out, ignore=shutil.ignore_patterns('_redirects', '_headers'))
open(os.path.join(out, 'CNAME'), 'w').write('arisvalentino.com\n')
open(os.path.join(out, '.nojekyll'), 'w').write('')

OLD = {'bewerbung': '/booking', 'epk': '/booking', 'songwriting': '/', 'imprint': '/impressum',
       'privacy-policy': '/datenschutz', 'cookie-richtlinie-eu': '/datenschutz'}
for path, target in OLD.items():
    d = os.path.join(out, path)
    os.makedirs(d, exist_ok=True)
    url = 'https://arisvalentino.com' + target
    open(os.path.join(d, 'index.html'), 'w', encoding='utf-8').write(
        f'<!doctype html><html lang="de"><head><meta charset="utf-8"><title>Aris Valentino</title>'
        f'<meta name="robots" content="noindex"><link rel="canonical" href="{url}">'
        f'<meta http-equiv="refresh" content="0; url={target}">'
        f'<script>location.replace("{target}")</script>'
        f'<style>body{{background:#000;color:#fff;font-family:sans-serif}}a{{color:#fff}}</style></head>'
        f'<body><p><a href="{target}">Weiter zu Aris Valentino</a></p></body></html>\n')
print(sum(len(f) for _, _, f in os.walk(out)), 'files')

"""Builds the deployable site (dist/) and the artifact preview (artifact/) from site/.
DE is the main language (/), EN lives under /en/. Run with: python3 -I build_site.py <scratchpad>"""
import re, sys, os, shutil, json
from bs4 import BeautifulSoup

ROOT = sys.argv[1]
SRC = os.path.join(ROOT, 'site')
DIST = os.path.join(ROOT, 'dist')
ART = os.path.join(ROOT, 'artifact')
DOMAIN = 'https://arisvalentino.com'
SPOTIFY = 'https://open.spotify.com/intl-de/artist/7dVIsUVDF1mmZ0CbGANwhK'
INSTA = 'https://www.instagram.com/arisvalentino1/'
TIKTOK = 'https://www.tiktok.com/@arisvalentino1'
FACEBOOK = 'https://www.facebook.com/officialarisvalentino'

# ---------- images: SEO file names + alt texts (de, en) ----------
IMAGES = {
    'img/hero-wide.jpg': ('img/aris-valentino-pop-rock-saenger.jpg', 'Aris Valentino, Pop-Rock-Sänger und Songwriter, in brauner Lederjacke vor blauem Himmel', 'Aris Valentino, pop rock singer and songwriter, in a brown leather jacket against a blue sky'),
    'img/about-close.jpg': ('img/aris-valentino-portrait-lederjacke.jpg', 'Aris Valentino in Lederjacke mit Gitarre, Schwarz-Weiß-Porträt', 'Aris Valentino in a leather jacket with a guitar, black and white portrait'),
    'img/about.jpg': ('img/aris-valentino-portrait-lederjacke-gitarre.jpg', 'Aris Valentino in Lederjacke mit weißer E-Gitarre, Schwarz-Weiß-Porträt', 'Aris Valentino in a leather jacket with a white electric guitar, black and white portrait'),
    'img/cover.jpg': ('img/aris-valentino-single-cover.jpg', '', ''),
    'img/og.jpg': ('img/aris-valentino-og.jpg', '', ''),
    'img/strip-bg.jpg': ('img/aris-valentino-collage.jpg', '', ''),
    'img/g/leather-guitar-bw.jpg': ('img/aris-valentino-portrait-gitarre-schwarz-weiss.jpg', 'Aris Valentino mit Gitarre im Studio, Schwarz-Weiß-Porträt', 'Aris Valentino with a guitar in the studio, black and white portrait'),
    'img/g/stage-red.jpg': ('img/aris-valentino-live-konzert-rote-buehne.jpg', 'Aris Valentino live auf der Bühne im roten Licht, Arm in die Luft', 'Aris Valentino live on stage in red light, arm raised'),
    'img/g/band-stage.jpg': ('img/aris-valentino-band-live-konzert.jpg', 'Aris Valentino und Band live vor dem Namensbanner, Publikum im Vordergrund', 'Aris Valentino and band live in front of the name banner, crowd in the foreground'),
    'img/g/acoustic-bw.jpg': ('img/aris-valentino-live-akustikgitarre.jpg', 'Aris Valentino singt live mit Akustikgitarre, Blick durch das Publikum', 'Aris Valentino singing live with acoustic guitar, seen through the crowd'),
    'img/g/crowd-white.jpg': ('img/aris-valentino-live-publikum-klatscht.jpg', 'Aris Valentino singt vor klatschendem Publikum', 'Aris Valentino singing to a clapping crowd'),
    'img/g/portrait-bw.jpg': ('img/aris-valentino-portrait-studio.jpg', 'Aris Valentino im weißen Studio, Schwarz-Weiß-Porträt', 'Aris Valentino in a white studio, black and white portrait'),
    'img/g/stage-blue.jpg': ('img/aris-valentino-live-gitarre-band.jpg', 'Aris Valentino mit Gitarre auf der Bühne, Band im Hintergrund', 'Aris Valentino with guitar on stage, band behind him'),
    'img/g/mustang.jpg': ('img/aris-valentino-portrait-oldtimer-nacht.jpg', 'Aris Valentino bei Nacht vor einem roten Oldtimer', 'Aris Valentino at night in front of a red classic car'),
    'img/g/band-bw.jpg': ('img/aris-valentino-band-gitarrist-live.jpg', 'Aris Valentino und Gitarrist rocken auf der Bühne', 'Aris Valentino and guitarist rocking out on stage'),
    'img/g/singing-bw.jpg': ('img/aris-valentino-gesang-mikrofon-live.jpg', 'Aris Valentino singt am Mikrofon mit Gitarre', 'Aris Valentino singing at the microphone with guitar'),
    'img/g/party.jpg': ('img/aris-valentino-nach-dem-konzert.jpg', 'Aris Valentino mit Freunden nach einem Konzert', 'Aris Valentino with friends after a show'),
    'img/g/crowd-1.jpg': ('img/aris-valentino-band-mit-fans.jpg', 'Aris Valentino und Band mit dem Publikum nach einer Show', 'Aris Valentino and band with the audience after a show'),
    'img/g/live-hands.jpg': ('img/aris-valentino-live-konzert-crowd-haende.jpg', 'Aris Valentino live mit Akustikgitarre und Band, Hände der Crowd in der Luft', 'Aris Valentino live with acoustic guitar and band, crowd hands in the air'),
}

FONT_CSS = '''@font-face{font-family:"Archivo";font-style:normal;font-display:swap;font-weight:100 900;font-stretch:62% 125%;src:url(fonts/archivo-latin-wdth-normal.woff2) format("woff2-variations"),url(fonts/archivo-latin-wdth-normal.woff2) format("woff2");unicode-range:U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+0304,U+0308,U+0329,U+2000-206F,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD}
@font-face{font-family:"Archivo";font-style:normal;font-display:swap;font-weight:100 900;font-stretch:62% 125%;src:url(fonts/archivo-latin-ext-wdth-normal.woff2) format("woff2-variations"),url(fonts/archivo-latin-ext-wdth-normal.woff2) format("woff2");unicode-range:U+0100-02BA,U+02BD-02C5,U+02C7-02CC,U+02CE-02D7,U+02DD-02FF,U+0304,U+0308,U+0329,U+1D00-1DBF,U+1E00-1E9F,U+1EF2-1EFF,U+2020,U+20A0-20AB,U+20AD-20C0,U+2113,U+2C60-2C7F,U+A720-A7FF}
@font-face{font-family:"Caveat";font-style:normal;font-display:swap;font-weight:700;src:url(fonts/caveat-latin-700-normal.woff2) format("woff2");unicode-range:U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+0304,U+0308,U+0329,U+2000-206F,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD}
@font-face{font-family:"Caveat";font-style:normal;font-display:swap;font-weight:700;src:url(fonts/caveat-latin-ext-700-normal.woff2) format("woff2");unicode-range:U+0100-02BA,U+02BD-02C5,U+02C7-02CC,U+02CE-02D7,U+02DD-02FF,U+0304,U+0308,U+0329,U+1D00-1DBF,U+1E00-1E9F,U+1EF2-1EFF,U+2020,U+20A0-20AB,U+20AD-20C0,U+2113,U+2C60-2C7F,U+A720-A7FF}
'''
LANG_CSS = '\n.lang a{text-decoration:none;padding:4px 6px;color:var(--muted)}\n.lang a:hover{color:var(--fg)}\n.lang a[aria-current]{color:var(--fg);text-decoration:underline;text-underline-offset:4px}\n'

META = {
    ('index', 'de'): ('Aris Valentino – Sänger & Songwriter | Pop mit Rock-’n’-Roll-Seele',
                      'Aris Valentino: Pop mit Rock-’n’-Roll-Seele, große Stimme und energiegeladene Live-Show mit Band. Neue Musik, Live-Termine, Videos, Fotos und Booking.'),
    ('index', 'en'): ('Aris Valentino – Singer & Songwriter | Pop with a rock ’n’ roll soul',
                      'Aris Valentino: pop with a rock ’n’ roll soul, a big voice and a high-energy live show with band. New music, live dates, videos, photos and booking.'),
    ('booking', 'de'): ('Booking – Aris Valentino & Band | Festivals & Live-Shows',
                        'Aris Valentino & Band buchen: 50+ Shows seit 2022, 3 ausverkaufte Headliner-Shows, Bochum Total, Zeltfestival Ruhr. Festivaltauglich mit eigenem In-Ear-Setup.'),
    ('booking', 'en'): ('Booking – Aris Valentino & Band | Festivals & live shows',
                        'Book Aris Valentino & Band: 50+ shows since 2022, 3 sold-out headline shows, Bochum Total, Zeltfestival Ruhr. Festival-ready with own in-ear setup.'),
}
URLS = {('index', 'de'): '/', ('index', 'en'): '/en/', ('booking', 'de'): '/booking', ('booking', 'en'): '/en/booking'}


def jsonld(page, lang):
    artist = {
        '@type': 'MusicGroup', '@id': DOMAIN + '/#artist', 'name': 'Aris Valentino',
        'url': DOMAIN + '/', 'image': DOMAIN + '/img/aris-valentino-pop-rock-saenger.jpg',
        'genre': ['Pop', 'Pop-Rock'],
        'foundingLocation': {'@type': 'Place', 'name': 'Köln', 'address': {'@type': 'PostalAddress', 'addressLocality': 'Köln', 'addressCountry': 'DE'}},
        'sameAs': [SPOTIFY, INSTA, TIKTOK, FACEBOOK],
        'member': [{'@type': 'Person', 'name': n} for n in ['Aris Valentino', 'Niklas Bischop', 'Felix Martin', 'Samuel Bojko', 'Simon Finzel']],
        'email': 'mail@arisvalentino.com',
        'telephone': '+49 173 9760402',
    }
    event = {'@type': 'MusicEvent', 'name': 'Aris Valentino live · Let Me Introduce', 'startDate': '2026-11-21',
             'eventStatus': 'https://schema.org/EventScheduled', 'eventAttendanceMode': 'https://schema.org/OfflineEventAttendanceMode',
             'location': {'@type': 'Place', 'name': 'Cafe No. 5', 'address': {'@type': 'PostalAddress', 'addressLocality': 'Köln', 'addressCountry': 'DE'}},
             'performer': {'@id': DOMAIN + '/#artist'}}
    graph = [artist, event,
             {'@type': 'WebPage', 'url': DOMAIN + URLS[(page, lang)], 'name': META[(page, lang)][0], 'inLanguage': lang, 'about': {'@id': DOMAIN + '/#artist'}}]
    return '<script type="application/ld+json">' + json.dumps({'@context': 'https://schema.org', '@graph': graph}, ensure_ascii=False) + '</script>'


def head_meta(page, lang):
    t, d = META[(page, lang)]
    u = DOMAIN + URLS[(page, lang)]
    alt = {l: DOMAIN + URLS[(page, l)] for l in ('de', 'en')}
    return f'''<title>{t}</title>
<meta name="description" content="{d}">
<link rel="canonical" href="{u}">
<link rel="alternate" hreflang="de" href="{alt['de']}">
<link rel="alternate" hreflang="en" href="{alt['en']}">
<link rel="alternate" hreflang="x-default" href="{alt['de']}">
<meta property="og:type" content="{'profile' if page == 'index' else 'website'}">
<meta property="og:site_name" content="Aris Valentino">
<meta property="og:title" content="{t}">
<meta property="og:description" content="{d}">
<meta property="og:url" content="{u}">
<meta property="og:image" content="{DOMAIN}/img/aris-valentino-og.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:locale" content="{'de_DE' if lang == 'de' else 'en_US'}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' fill='%23000'/%3E%3Ctext x='50%25' y='56%25' fill='%23fff' font-family='Arial Black,Arial' font-weight='900' font-size='30' text-anchor='middle' dominant-baseline='middle'%3EAV%3C/text%3E%3C/svg%3E">
{jsonld(page, lang)}'''


def split_source(name):
    raw = open(os.path.join(SRC, name + '.html'), encoding='utf-8').read()
    style = re.search(r'<style>\n?(.*?)</style>', raw, re.S).group(1)
    if '<body>' in raw:
        body = raw[raw.index('<body>') + 6: raw.rindex('</body>')]
    else:
        body = raw[raw.index('</style>') + 8:]
    return style, body


def prerender(body, lang):
    soup = BeautifulSoup(body, 'html.parser')
    key = 'data-' + lang
    for el in soup.find_all(attrs={key: True}):
        if el.find(True) is None:
            el.string = el[key]
        else:
            print('  skip (has children):', el.name, el.get('class'))
    for el in soup.find_all(attrs={'data-en': True}):
        del el['data-en']
        if el.has_attr('data-de'):
            del el['data-de']
    for el in soup.find_all(attrs={'data-de': True}):
        del el['data-de']
    for img in soup.find_all('img'):
        src = img.get('src', '')
        if src in IMAGES:
            new, de, en = IMAGES[src]
            img['src'] = new
            if img.get('alt', None) not in (None, ''):
                img['alt'] = de if lang == 'de' else en
    if lang == 'de':
        for b in soup.select('#tracks .play'):
            b['aria-label'] = b['aria-label'].replace('Play ', 'Abspielen: ')
        for el in soup.find_all(attrs={'aria-label': 'Live clips'}):
            el['aria-label'] = 'Live-Clips'
    return str(soup)


def lang_switch(page, lang):
    other = 'en' if lang == 'de' else 'de'
    here = 'index.html' if page == 'index' else 'booking.html'
    to_other = ('en/' + here) if lang == 'de' else ('../' + here)
    a_de = f'<a href="{here if lang == "de" else to_other}" hreflang="de"{" aria-current=\"page\"" if lang == "de" else ""}>DE</a>'
    a_en = f'<a href="{here if lang == "en" else to_other}" hreflang="en"{" aria-current=\"page\"" if lang == "en" else ""}>EN</a>'
    return f'<div class="lang" aria-label="Sprache / Language">{a_de}{a_en}</div>'


def build_page(page, lang, style, body):
    body = re.sub(r'<div class="lang" role="group" aria-label="Language">.*?</div>', lambda m: lang_switch(page, lang), body, count=1, flags=re.S)
    body = re.sub(r"  function setLang\(l\)\{.*?(?=  var hdr = document\.querySelector\('header'\);)", '', body, count=1, flags=re.S)
    body = body.replace('<a href="#top">Impressum</a>', '<a href="impressum.html">Impressum</a>')
    body = re.sub(r'<a href="#top" data-en="Privacy" data-de="Datenschutz">Privacy</a>', '<a href="datenschutz.html" data-en="Privacy" data-de="Datenschutz">Privacy</a>', body)
    body = prerender(body, lang)
    css = FONT_CSS + style.replace('url("img/strip-bg.jpg")', 'url("img/aris-valentino-collage.jpg")') + LANG_CSS
    html = f'''<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
{head_meta(page, lang)}
<link rel="preload" href="fonts/archivo-latin-wdth-normal.woff2" as="font" type="font/woff2" crossorigin>
<style>
html,body{{margin:0}}
:root{{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}}
img{{max-width:100%}}
[hidden]{{display:none!important}}
{css}
</style>
</head>
<body>
{body.strip()}
</body>
</html>
'''
    html = html.replace("v.poster = c.poster;", "v.poster = c.poster;")
    if lang == 'en':
        html = re.sub(r'((?:src|href|poster|data-audio)=")(img|vid2|vid|fonts|audio|downloads)/', r'\1../\2/', html)
        html = re.sub(r"(['(\"])(vid2|img/g)/", r'\1../\2/', html)
        html = html.replace('url(fonts/', 'url(../fonts/').replace('url("img/', 'url("../img/')
        html = html.replace('href="impressum.html"', 'href="../impressum.html"').replace('href="datenschutz.html"', 'href="../datenschutz.html"')
    return html


LEGAL_BODY = {
'impressum': ('Impressum', '''
<h1 class="legal-h">Impressum</h1>
<h2>Angaben gemäß § 5 DDG</h2>
<p>Aris Valentino<br>Schwalbacher Straße 6<br>50969 Köln<br>Deutschland</p>
<h2>Kontakt</h2>
<p>E-Mail: <span class="mail-ob">mail<span class="at">at</span>arisvalentino.com</span></p>
<h2>Verantwortlich für den Inhalt nach § 18 Abs. 2 MStV</h2>
<p>Aris Valentino, Anschrift wie oben</p>
<h2>Haftung für Links</h2>
<p>Diese Website enthält Links zu externen Websites Dritter, zum Beispiel Spotify und Instagram. Auf deren Inhalte habe ich keinen Einfluss. Für die Inhalte der verlinkten Seiten ist stets der jeweilige Anbieter verantwortlich. Bei Bekanntwerden von Rechtsverletzungen entferne ich entsprechende Links umgehend.</p>
<h2>Urheberrecht</h2>
<p>Alle Inhalte dieser Website, insbesondere Texte, Fotos, Videos und Musik, sind urheberrechtlich geschützt. Eine Verwendung außerhalb der Grenzen des Urheberrechts bedarf der vorherigen Zustimmung. Pressefotos stelle ich auf Anfrage zur Verfügung.</p>
'''),
'datenschutz': ('Datenschutz', '''
<h1 class="legal-h">Datenschutz&shy;erklärung</h1>
<p>Stand: November 2026</p>
<h2>1. Verantwortlicher</h2>
<p>Aris Valentino<br>Schwalbacher Straße 6<br>50969 Köln<br>E-Mail: <span class="mail-ob">mail<span class="at">at</span>arisvalentino.com</span></p>
<h2>2. Das Wichtigste in Kürze</h2>
<p>Diese Website setzt keine Cookies, nutzt keine Analyse- oder Tracking-Tools und bindet keine Inhalte von Drittanbietern ein. Schriften, Fotos und Videos werden direkt von dieser Website geladen. Personenbezogene Daten fallen nur an, wenn du die Website aufrufst (technisch notwendige Server-Logfiles) oder mir eine E-Mail schreibst.</p>
<h2>3. Hosting und Server-Logfiles</h2>
<p>Diese Website wird über GitHub Pages bereitgestellt, einen Dienst der GitHub, Inc., 88 Colin P. Kelly Jr. Street, San Francisco, CA 94107, USA. Beim Aufruf der Website verarbeitet GitHub automatisch Informationen, die dein Browser übermittelt, insbesondere deine IP-Adresse, Datum und Uhrzeit des Zugriffs und die aufgerufene Seite. Diese Daten sind technisch notwendig, um die Website auszuliefern und ihre Sicherheit und Stabilität zu gewährleisten. Rechtsgrundlage ist Art. 6 Abs. 1 lit. f DSGVO; mein berechtigtes Interesse liegt im sicheren und fehlerfreien Betrieb der Website. Da GitHub seinen Sitz in den USA hat, kann eine Übermittlung in die USA stattfinden. Diese erfolgt auf Grundlage des EU-US Data Privacy Framework bzw. der Standardvertragsklauseln der EU-Kommission (Art. 44 ff. DSGVO). Weitere Informationen findest du in der Datenschutzerklärung von GitHub: <a href="https://docs.github.com/de/site-policy/privacy-policies/github-general-privacy-statement" rel="noopener">docs.github.com</a>.</p>
<h2>4. Kontakt per E-Mail</h2>
<p>Wenn du mir eine E-Mail schreibst, verarbeite ich deine Angaben (zum Beispiel Name, E-Mail-Adresse und den Inhalt deiner Nachricht), um deine Anfrage zu beantworten. Rechtsgrundlage ist Art. 6 Abs. 1 lit. b DSGVO, sofern deine Anfrage auf einen Vertrag wie ein Booking zielt, im Übrigen Art. 6 Abs. 1 lit. f DSGVO. Die Daten lösche ich, sobald sie für die Bearbeitung nicht mehr erforderlich sind und keine gesetzlichen Aufbewahrungspflichten entgegenstehen.</p>
<h2>5. Links zu anderen Plattformen</h2>
<p>Auf dieser Website verlinke ich auf Spotify, Instagram, TikTok und Facebook. Es handelt sich um einfache Links: Erst wenn du darauf klickst, wirst du zur jeweiligen Plattform weitergeleitet. Dort gelten deren Datenschutzbestimmungen.</p>
<h2>6. Deine Rechte</h2>
<p>Du hast das Recht auf Auskunft (Art. 15 DSGVO), Berichtigung (Art. 16), Löschung (Art. 17), Einschränkung der Verarbeitung (Art. 18), Datenübertragbarkeit (Art. 20) und Widerspruch gegen Verarbeitungen auf Grundlage von Art. 6 Abs. 1 lit. f DSGVO (Art. 21). Schreib mir dafür einfach eine E-Mail.</p>
<p>Außerdem hast du das Recht, dich bei einer Datenschutz-Aufsichtsbehörde zu beschweren, zum Beispiel bei der Landesbeauftragten für Datenschutz und Informationsfreiheit Nordrhein-Westfalen.</p>
'''),
}
LEGAL_CSS = '''
.legal{padding-block:clamp(48px,7vw,96px) 0}
.legal > *{max-width:760px}
.legal-h{margin:0 0 clamp(24px,3vw,40px);font-family:var(--f-display);font-weight:800;font-stretch:125%;text-transform:uppercase;font-size:clamp(32px,5vw,64px);line-height:1;letter-spacing:-.01em;overflow-wrap:anywhere;hyphens:manual}
.legal h2{margin:36px 0 10px;font-family:var(--f-mono);font-weight:600;font-stretch:112%;font-size:13px;letter-spacing:.14em;text-transform:uppercase;color:var(--fg)}
.legal p{margin:0 0 14px;color:var(--muted);line-height:1.7;max-width:68ch}
.legal .mail-ob{display:inline;margin:0;font-family:var(--f-body);font-weight:500;font-stretch:100%;font-size:inherit;line-height:inherit;color:var(--fg)}
.legal .mail-ob .at{display:inline-block;margin:0 .3em;padding:.08em .3em .1em;border:1px solid var(--fg);font-size:.72em;letter-spacing:.1em;text-transform:uppercase;line-height:1}
'''


def build_legal(key, style):
    title, content = LEGAL_BODY[key]
    css = FONT_CSS + style.replace('url("img/strip-bg.jpg")', 'url("img/aris-valentino-collage.jpg")') + LANG_CSS + LEGAL_CSS
    return f'''<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title} – Aris Valentino</title>
<meta name="robots" content="noindex, follow">
<link rel="canonical" href="{DOMAIN}/{key}">
<style>
html,body{{margin:0}}
:root{{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}}
[hidden]{{display:none!important}}
{css}
header{{background:color-mix(in srgb,var(--bg) 82%,transparent);backdrop-filter:blur(12px)}}
</style>
</head>
<body>
<header>
  <div class="wrap">
    <a class="logo" href="index.html">ARIS VALENTINO</a>
    <nav aria-label="Hauptmenü"><a href="index.html">Startseite</a><a href="booking.html">Booking</a></nav>
  </div>
</header>
<main class="wrap legal">
{content}
</main>
<footer>
  <div class="wrap">
    <span>© 2026 Aris Valentino</span>
    <div class="links"><a href="index.html">Startseite</a><a href="booking.html">Booking</a><a href="impressum.html">Impressum</a><a href="datenschutz.html">Datenschutz</a></div>
  </div>
</footer>
</body>
</html>
'''


def main():
    if os.path.exists(DIST):
        shutil.rmtree(DIST)
    os.makedirs(DIST + '/en')
    pages = {}
    for page in ('index', 'booking'):
        style, body = split_source(page)
        for lang in ('de', 'en'):
            html = build_page(page, lang, style, body)
            out = os.path.join(DIST, ('' if lang == 'de' else 'en/') + page + '.html')
            open(out, 'w', encoding='utf-8').write(html)
            pages[(page, lang)] = html
            print('wrote', out, len(html))
    style_b, _ = split_source('booking')
    for key in LEGAL_BODY:
        open(os.path.join(DIST, key + '.html'), 'w', encoding='utf-8').write(build_legal(key, style_b))
    # assets
    for old, (new, _, _) in IMAGES.items():
        os.makedirs(os.path.dirname(os.path.join(DIST, new)), exist_ok=True)
        shutil.copy(os.path.join(SRC, old), os.path.join(DIST, new))
    shutil.copytree(os.path.join(SRC, 'fonts'), os.path.join(DIST, 'fonts'))
    shutil.copytree(os.path.join(SRC, 'vid2'), os.path.join(DIST, 'vid2'))
    shutil.copytree(os.path.join(SRC, 'audio'), os.path.join(DIST, 'audio'))
    shutil.copytree(os.path.join(SRC, 'downloads'), os.path.join(DIST, 'downloads'))
    # 404
    nf = build_legal('impressum', style_b).replace('<title>Impressum – Aris Valentino</title>', '<title>Seite nicht gefunden – Aris Valentino</title>')
    nf = re.sub(r'<main class="wrap legal">.*?</main>', '<main class="wrap legal"><h1 class="legal-h">404</h1><p>Diese Seite gibt es nicht (mehr).</p><p><a class="btn" href="/">Zur Startseite</a> &nbsp; <a class="btn ghost" href="/booking">Booking</a></p></main>', nf, flags=re.S)
    nf = nf.replace('href="index.html"', 'href="/"').replace('href="booking.html"', 'href="/booking"').replace('href="impressum.html"', 'href="/impressum"').replace('href="datenschutz.html"', 'href="/datenschutz"').replace('url(fonts/', 'url(/fonts/')
    open(os.path.join(DIST, '404.html'), 'w', encoding='utf-8').write(nf)
    # sitemap, robots, redirects, headers
    sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">']
    for page in ('index', 'booking'):
        for lang in ('de', 'en'):
            sm.append('  <url>')
            sm.append(f'    <loc>{DOMAIN}{URLS[(page, lang)]}</loc>')
            for l in ('de', 'en'):
                sm.append(f'    <xhtml:link rel="alternate" hreflang="{l}" href="{DOMAIN}{URLS[(page, l)]}"/>')
            if lang == 'de':
                for src in sorted(set(re.findall(r'src="(img/aris-valentino-[^"]+\.jpg)"', pages[(page, lang)]))):
                    sm.append(f'    <image:image><image:loc>{DOMAIN}/{src}</image:loc></image:image>')
            sm.append('    <changefreq>weekly</changefreq>')
            sm.append('  </url>')
    sm.append('</urlset>')
    open(os.path.join(DIST, 'sitemap.xml'), 'w').write('\n'.join(sm) + '\n')
    open(os.path.join(DIST, 'robots.txt'), 'w').write(f'User-agent: *\nAllow: /\n\nSitemap: {DOMAIN}/sitemap.xml\n')
    redirects = '''# old WordPress URLs -> new pages
/bewerbung            /booking       301
/bewerbung/*          /booking       301
/epk                  /booking       301
/epk/*                /booking       301
/songwriting          /              301
/songwriting/*        /              301
/imprint              /impressum     301
/imprint/*            /impressum     301
/privacy-policy       /datenschutz   301
/privacy-policy/*     /datenschutz   301
/cookie-richtlinie-eu /datenschutz   301
/cookie-richtlinie-eu/* /datenschutz 301
/index.html           /              301
/booking.html         /booking       301
/impressum.html       /impressum     301
/datenschutz.html     /datenschutz   301
/en/index.html        /en/           301
/en/booking.html      /en/booking    301
/booking              /booking.html      200
/impressum            /impressum.html    200
/datenschutz          /datenschutz.html  200
/en/booking           /en/booking.html   200
'''
    open(os.path.join(DIST, '_redirects'), 'w').write(redirects)
    open(os.path.join(DIST, '_headers'), 'w').write('/fonts/*\n  Cache-Control: public, max-age=31536000, immutable\n/img/*\n  Cache-Control: public, max-age=604800\n/vid2/*\n  Cache-Control: public, max-age=604800\n/*\n  X-Content-Type-Options: nosniff\n  Referrer-Policy: strict-origin-when-cross-origin\n')

    # artifact preview: same files; main page must be a fragment (the host wraps it)
    if os.path.exists(ART):
        shutil.rmtree(ART)
    shutil.copytree(DIST, ART)
    de = pages[('index', 'de')]
    head = de[de.index('<head>') + 6: de.index('</head>')]
    head = re.sub(r'<meta charset="utf-8">\n<meta name="viewport"[^>]*>\n', '', head)
    head = re.sub(r'<title>.*?</title>', '<title>Aris Valentino</title>\n<meta name="claude:viewport-fit-sides" content="cover">', head, count=1)
    head = re.sub(r'html,body\{margin:0\}\n:root\{padding-top[^\n]*\nimg\{max-width:100%\}\n\[hidden\]\{display:none!important\}\n', '', head)
    bodyfrag = de[de.index('<body>') + 6: de.rindex('</body>')]
    open(os.path.join(ART, 'index.html'), 'w', encoding='utf-8').write(head.strip() + '\n' + bodyfrag.strip() + '\n<script>document.documentElement.lang="de"</script>\n')
    clean_urls()
    print('done')


def clean_urls():
    # live site only (artifact keeps relative .html links): /, /booking, /en/, /en/booking, /impressum, /datenschutz
    import glob
    for f in glob.glob(os.path.join(DIST, '*.html')) + glob.glob(os.path.join(DIST, 'en', '*.html')):
        h = open(f, encoding='utf-8').read()
        en = os.sep + 'en' + os.sep in f
        pre = '/en' if en else ''
        rep = [
            ('href="../index.html', 'href="/'), ('href="../booking.html', 'href="/booking'),
            ('href="en/index.html', 'href="/en/'), ('href="en/booking.html', 'href="/en/booking'),
            ('href="../impressum.html"', 'href="/impressum"'), ('href="../datenschutz.html"', 'href="/datenschutz"'),
            ('href="impressum.html"', 'href="/impressum"'), ('href="datenschutz.html"', 'href="/datenschutz"'),
            ('href="index.html', 'href="' + (pre + '/' if en else '/')), ('href="booking.html', 'href="' + pre + '/booking'),
        ]
        for a, b in rep:
            h = h.replace(a, b)
        h = re.sub(r'((?:src|href|poster|data-audio)=")(?:\.\./)?(img|vid2|fonts|audio|downloads)/', r'\1/\2/', h)
        h = re.sub(r"(['(\"])(?:\.\./)?(vid2|img/g)/", r'\1/\2/', h)
        h = h.replace('url(../fonts/', 'url(/fonts/').replace('url(fonts/', 'url(/fonts/').replace('url("../img/', 'url("/img/').replace('url("img/', 'url("/img/')
        def ext(m):
            tag = m.group(0)
            if 'target=' not in tag:
                tag = tag[:-1] + ' target="_blank">'
            if 'rel=' not in tag:
                tag = tag[:-1] + ' rel="noopener">'
            return tag
        # external links + PDFs open in a new tab
        h = re.sub(r'<a\s[^>]*href="(?:https?://|/downloads/)[^"]*"[^>]*>', ext, h)
        open(f, 'w', encoding='utf-8').write(h)


main()

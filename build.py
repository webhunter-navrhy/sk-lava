"""Zostaví index.html + style.css s cache bustingom (?v=hash).
Obsah z lava-laco.sk (data.py), fotky pripravuje spracuj_foto.py (foto.json), logo = potrace z hlavičky ich webu."""
import hashlib, json, math, re
from pathlib import Path
from PIL import Image
from data import KAT, REFERENCIE, OBCE, PIN, SLUZBY, DALSIE, CINNOST, KROKY, TYPY

D = Path(__file__).parent
F = json.load(open(D / 'foto.json'))
R, G = F['rozmery'], F['galerie']
wh = lambda k: f'width="{R[k][0]}" height="{R[k][1]}"'
hs = lambda b: hashlib.md5(b).hexdigest()[:8]
esc = lambda s: s.replace('&', '&amp;').replace('"', '&quot;').replace('<', '&lt;')

# ---------- logo (červené, orezané na obsah) ----------
src = (D / 'podklady' / 'logo_trace.svg').read_text()
paths = re.search(r'(<g transform=.*?</g>)', src, re.S).group(1).replace('fill="#000000"', 'fill="#c8141b"')
logo_svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 52 1508 534">{paths}</svg>'
(D / 'img' / 'logo.svg').write_text(logo_svg)
LOGO = '<img class="logo" src="img/logo.svg?v=' + hs(logo_svg.encode()) + '" alt="LaVa" width="113" height="40">'
# favicon = schodíky z loga
fav = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32"><rect width="32" height="32" rx="6" fill="#161618"/>'
       '<g fill="#c8141b"><path d="M14 7h9l-1 3h-9z"/><path d="M11 12h12l-1 3H10z"/><path d="M8 17h15l-1 3H7z"/><path d="M5 22h18l-1 4H4z"/></g></svg>')
(D / 'img' / 'favicon.svg').write_text(fav)

# ---------- hero: výrez na výšku z g10-04 ----------
im = Image.open(D / 'img' / 'g10-04.jpg')
w, h = im.size
cw = round(h * 0.8)
x0 = round(w * 0.06)
im.crop((x0, 0, x0 + cw, h)).save(D / 'img' / 'hero.jpg', quality=84, optimize=True, progressive=True)

# ---------- marquee ----------
marquee = ''.join(f'<span>{c}</span><b aria-hidden="true"></b>' for c in CINNOST)
marquee = marquee + marquee.replace('<span>', '<span aria-hidden="true">')

# ---------- služby ----------
def svc(i, t, p, items, foto):
    k = f'g{foto[0]}-{foto[1]}'
    li = ''.join(f'<li>{x}</li>' for x in items)
    return (f'\n      <details class="svc__i rv"{" open" if i == 1 else ""}><summary><span class="svc__n">{i:02d}</span><h3>{t}</h3>'
            f'<span class="svc__x" aria-hidden="true"></span></summary>'
            f'<div class="svc__body"><div class="svc__t"><p>{p}</p><ul class="ticks">{li}</ul></div>'
            f'<figure class="svc__img"><img src="img/{k}.jpg" alt="{esc(t)} – realizácia LaVa" loading="lazy" {wh(k)}></figure></div></details>')
sluzby = ''.join(svc(i, *s) for i, s in enumerate(SLUZBY, 1)) + '\n    '
dalsie = ''.join(f'<li>{x}</li>' for x in DALSIE)

# ---------- postup: kroky + rez spevnenou plochou ----------
kroky = '\n' + '\n'.join(
    f'      <li class="step" data-i="{i}"><b>{i + 1:02d}</b><h3>{t}</h3><p>{p}</p></li>' for i, (t, p) in enumerate(KROKY)) + '\n    '

pav = ''.join(f'<rect class="pv" style="--d:{j * 0.06:.2f}s" x="{137 + j * 48}" y="200" width="46" height="34" rx="2"/>' for j in range(11))
pal = ''.join(f'<rect x="{24 + (j % 3) * 22}" y="{186 - (j // 3) * 12}" width="20" height="10" rx="1"/>' for j in range(9))
REZ = f'''<svg class="rez" id="rez" viewBox="0 36 800 404" role="img" aria-label="Rez spevnenou plochou">
<defs>
 <pattern id="pSoil" width="14" height="14" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><line x1="0" y1="0" x2="0" y2="14" class="hatch"/></pattern>
 <pattern id="pGravel" width="18" height="14" patternUnits="userSpaceOnUse"><circle cx="4" cy="4" r="2.4" class="gr"/><circle cx="13" cy="10" r="1.8" class="gr"/><circle cx="10" cy="3" r="1.1" class="gr"/></pattern>
 <pattern id="pSand" width="7" height="6" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r=".8" class="sd"/><circle cx="5.5" cy="4.5" r=".7" class="sd"/></pattern>
 <pattern id="pConc" width="10" height="10" patternUnits="userSpaceOnUse"><path d="M2 3l2 1-1 2zM7 7l2-1v2z" class="cc"/></pattern>
</defs>
<rect class="soil" x="0" y="200" width="800" height="240"/>
<line class="ground" x1="0" y1="200" x2="800" y2="200"/>
<g class="k" data-k="-1" data-until="0"><path class="grass" d="{''.join(f'M{x} 200l3-9 2 9M{x + 6} 200l4-12 1 12M{x + 12} 200l2-7 3 7' for x in range(6, 800, 26))}"/><text class="lbl" x="400" y="180" text-anchor="middle">pôvodný terén s trávou</text></g>
<g class="k" data-k="0" data-until="2"><path class="grass grass--off" d="{''.join(f'M{x} 200l3-9 2 9' for x in range(110, 690, 26))}"/><text class="lbl lbl--red" x="400" y="180" text-anchor="middle">odstránenie vegetácie</text></g>
<g class="k" data-k="1" data-until="6"><g class="pal">{pal}<rect x="20" y="196" width="70" height="4" class="palb"/></g><text class="lbl" x="55" y="140" text-anchor="middle">materiál</text></g>
<g class="k" data-k="1" data-until="4"><path class="pile" d="M712 200 Q752 150 792 200Z"/><text class="lbl" x="752" y="140" text-anchor="middle">kamenivo</text></g>
<g class="k" data-k="2"><rect class="cut" x="110" y="200" width="580" height="130"/><path class="cutline" d="M110 200V330H690V200"/></g>
<g class="k" data-k="2" data-until="5"><line class="stake" x1="100" y1="120" x2="100" y2="204"/><line class="stake" x1="700" y1="120" x2="700" y2="204"/><line class="string" x1="100" y1="132" x2="700" y2="132"/><text class="lbl lbl--red" x="400" y="122" text-anchor="middle">zameranie</text></g>
<g class="k" data-k="2"><text class="lbl" x="770" y="420" text-anchor="end">rastlý terén</text></g>
<g class="k grow" data-k="3"><rect class="gravel" x="110" y="255" width="580" height="75"/><line class="ln" x1="690" y1="292" x2="740" y2="292"/><text class="lbl" x="746" y="296">zhutnený</text><text class="lbl" x="746" y="310">podklad</text></g>
<g class="k" data-k="3" data-until="4"><g class="tamp">{''.join(f'<path d="M{x} 214v24m-7-8 7 8 7-8"/>' for x in (200, 320, 440, 560))}</g></g>
<g class="k" data-k="4"><path class="conc" d="M148 304H98V252l14-12v46h36z"/><path class="conc" d="M652 304h50V252l-14-12v46h-36z"/><rect class="curb" x="112" y="192" width="22" height="94" rx="2"/><rect class="curb" x="666" y="192" width="22" height="94" rx="2"/><line class="ln" x1="98" y1="298" x2="56" y2="340"/><text class="lbl" x="34" y="356">obrubník</text><text class="lbl" x="34" y="370">v betóne</text></g>
<g class="k" data-k="5"><rect class="sand" x="134" y="234" width="532" height="21"/><line class="ln" x1="300" y1="246" x2="300" y2="380"/><text class="lbl" x="306" y="384">lôžko</text></g>
<g class="k" data-k="5"><g class="pvs">{pav}</g><line class="ln" x1="420" y1="200" x2="420" y2="70"/><text class="lbl lbl--red" x="426" y="80">zámková dlažba</text><text class="lbl" x="426" y="96">zavibrovaná a zaspárovaná</text></g>
<g class="k" data-k="6"><rect class="conc" x="728" y="200" width="28" height="56"/><rect class="post" x="736" y="64" width="12" height="136"/><path class="board" d="M748 80h46M748 104h46M748 128h46M748 152h46M748 176h46"/><text class="lbl lbl--red" x="742" y="50" text-anchor="middle">plot</text></g>
</svg>'''

# ---------- mapa referencií ----------
LON0, LAT0, LON1, LAT1 = 17.975, 48.445, 18.505, 48.125
KX = math.cos(math.radians(48.28)) * 111.32
KY = 110.57
S = 16  # px na km
proj = lambda lat, lon: ((lon - LON0) * KX * S, (LAT0 - lat) * KY * S)
MW, MH = (LON1 - LON0) * KX * S, (LAT0 - LAT1) * KY * S
rivers = json.load(open(D / 'podklady' / 'rivers.json'))['elements']
rv = ''
for e in rivers:
    pts = [proj(p['lat'], p['lon']) for p in e['geometry']]
    cls = 'riv riv--s' if e['tags'].get('name') == 'Malá Nitra' else 'riv'
    rv += f'<polyline class="{cls}" points="' + ' '.join(f'{x:.1f},{y:.1f}' for x, y in pts[::2] + [pts[-1]]) + '"/>'
vx, vy = proj(*OBCE['Vráble'])
rings = ''.join(f'<circle class="ring" cx="{vx:.1f}" cy="{vy:.1f}" r="{r * S}"/><text class="ringl" x="{vx:.1f}" y="{vy - r * S - 4 if r == 15 else vy + r * S + 13:.1f}" text-anchor="middle">{r} km</text>' for r in (5, 10, 15))
pocty = {}
for n, ob in PIN.items():
    for o in ob:
        pocty[o] = pocty.get(o, 0) + 1
LBL = {  # posun popisu (dx, dy, kotva)
    'Vráble': (-14, 5, 'end'), 'Nová Ves nad Žitavou': (14, 4, 'start'), 'Golianovo': (0, -16, 'middle'),
    'Chrášťany': (14, 4, 'start'), 'Šurianky': (14, 4, 'start'), 'Nitra': (0, -16, 'middle'),
    'Lúčnica nad Žitavou': (-14, 13, 'end'), 'Veľký Cetín': (0, -16, 'middle'), 'Melek': (14, 16, 'start'),
    'Horný Ohaj': (14, 4, 'start'), 'Horný Pial': (0, 24, 'middle'),
}
pins = ''
for o, (lat, lon) in OBCE.items():
    x, y = proj(lat, lon)
    dx, dy, an = LBL[o]
    nm = 'Nitra (Klokočina a okolie)' if o == 'Nitra' else o
    sid = ' pin--home' if o == 'Vráble' else ''
    pins += (f'<g class="pin{sid}" data-obec="{o}" tabindex="0" role="button" aria-label="{nm}: {pocty[o]} referencií">'
             f'<circle class="pin__h" cx="{x:.1f}" cy="{y:.1f}" r="16"/><circle class="pin__c" cx="{x:.1f}" cy="{y:.1f}" r="10"/>'
             f'<text class="pin__n" x="{x:.1f}" y="{y + 3.6:.1f}" text-anchor="middle">{pocty[o]}</text>'
             f'<text class="pin__l" x="{x + dx:.1f}" y="{y + dy:.1f}" text-anchor="{an}">{nm}</text></g>')
# mierka 5 km + sever
sb = f'<g class="scale"><line x1="24" y1="{MH - 26:.0f}" x2="{24 + 5 * S}" y2="{MH - 26:.0f}"/><line x1="24" y1="{MH - 31:.0f}" x2="24" y2="{MH - 21:.0f}"/><line x1="{24 + 5 * S}" y1="{MH - 31:.0f}" x2="{24 + 5 * S}" y2="{MH - 21:.0f}"/><text x="24" y="{MH - 36:.0f}">5 km</text></g>'
north = f'<g class="north" transform="translate({MW - 34:.0f},40)"><path d="M0-18 7 6 0 1-7 6z"/><text y="22" text-anchor="middle">S</text></g>'
riv_l = ''
for name, lat, lon, rot in (('Žitava', 48.33, 18.352, 70), ('Nitra', 48.37, 18.098, 62)):
    x, y = proj(lat, lon)
    riv_l += f'<text class="rivl" transform="translate({x:.0f},{y:.0f}) rotate({rot})">{name}</text>'
mapa = (f'<svg class="mapsvg" viewBox="0 0 {MW:.0f} {MH:.0f}" role="img" aria-label="Mapa referencií v okolí Vrábľov">'
        f'<defs><clipPath id="mc"><rect width="{MW:.0f}" height="{MH:.0f}"/></clipPath>'
        f'<pattern id="mgrid" width="{S * 5}" height="{S * 5}" patternUnits="userSpaceOnUse"><path d="M{S * 5} 0H0V{S * 5}" class="mg"/></pattern></defs>'
        f'<g clip-path="url(#mc)"><rect width="{MW:.0f}" height="{MH:.0f}" fill="url(#mgrid)"/>{rv}{riv_l}{rings}</g>{pins}{sb}{north}</svg>')

# ---------- karty referencií ----------
n_fotiek = sum(len(v) for v in G.values())
VIDNO = 8
karty = ''
for idx, (n, typ, miesto, cin, kat, cover) in enumerate(REFERENCIE):
    k = f'g{n:02d}-{cover}'
    fotos = G[str(n)]
    full = ','.join(f'img/{f}.jpg' for f in [k] + [f for f in fotos if f != k])
    more = ' is-more' if idx >= VIDNO else ''
    karty += (f'\n          <article class="card{more}" data-k="{kat}" data-obce="{"|".join(PIN[n])}" data-fotos="{full}" '
              f'data-cap="{esc(typ)} · {esc(miesto)}" tabindex="0" role="button" aria-label="{esc(typ)}, {esc(miesto)} – {len(fotos)} fotiek">'
              f'<div class="card__img"><img src="img/{k}.jpg" alt="{esc(typ)}, {esc(miesto)} – {esc(cin)}" loading="lazy" {wh(k)}>'
              f'<span class="card__tag">{KAT[kat]}</span><span class="card__cnt">{len(fotos)} fotiek</span></div>'
              f'<p class="card__place">{miesto}</p><h3>{typ}</h3><p class="card__what">{cin}</p></article>')
karty += f'\n          <div class="cards__more"><button class="btn btn--line" id="more">Zobraziť všetkých 20 referencií</button></div>\n        '
pocet = {k: sum(1 for r in REFERENCIE if r[4] == k) for k in KAT}
filtre = '<button class="is-on" data-f="*">Všetky <sup>20</sup></button>' + ''.join(
    f'<button data-f="{k}">{v} <sup>{pocet[k]}</sup></button>' for k, v in KAT.items())

chip = lambda v: f'<label class="chip"><input type="checkbox" name="typ" value="{v}"><span>{v}</span></label>'
typy = ''.join(chip(t) for t in TYPY)

# ---------- zostavenie ----------
css = (D / 'fonts' / 'fonts.css').read_text() + '\n' + (D / 'style.src.css').read_text()
(D / 'style.css').write_text(css)
html = (D / 'src.html').read_text()
for k in R:
    html = html.replace('{{w_' + k + '}}', str(R[k][0])).replace('{{h_' + k + '}}', str(R[k][1]))
for k, v in dict(logo=LOGO, marquee=marquee, sluzby=sluzby, dalsie=dalsie, kroky=kroky, rez=REZ, mapa=mapa,
                 karty=karty, filtre=filtre, typy=typy, n_fotiek=str(n_fotiek),
                 hero=hs((D / 'img' / 'hero.jpg').read_bytes())).items():
    html = html.replace('{{' + k + '}}', v)
html = html.replace('{{css}}', hs(css.encode())).replace('{{js}}', hs((D / 'main.js').read_bytes()))
assert '{{' not in html, re.findall(r'\{\{\w+', html)
(D / 'index.html').write_text(html)
(D / 'robots.txt').write_text('User-agent: *\nDisallow: /\n')
print('ok', n_fotiek, 'fotiek,', len(html) // 1024, 'kB html')

"""Obsah náhľadu – všetko z lava-laco.sk (podklady/*.html): referencie zo stránky Referencie,
fotky z galérií foto01–foto20 (podklady/web/galeriaNN), polohy obcí z OpenStreetMap (podklady/geo.json)."""

# kategórie pre filter referencií
KAT = {
    'dlazby': 'Dlažby a terasy',
    'fasady': 'Fasády a zateplenie',
    'interier': 'Kúpeľne a byty',
    'stavby': 'Strechy a stavby',
}

# (galéria, typ stavby, miesto, činnosť – ako na webe, kategória, titulná fotka)
REFERENCIE = [
    (1, 'Rodinný dom na Sládkovičovej', 'Nová Ves nad Žitavou', 'Vybudovanie spevnených plôch (pokládka zámkovej dlažby)', 'dlazby', '03'),
    (2, 'Rodinný dom s dostavbou', 'Golianovo', 'Vybudovanie spevnených plôch (pokládka zámkovej dlažby)', 'dlazby', '04'),
    (3, 'Zrekonštruovaný rodinný dom', 'Chrášťany', 'Vybudovanie spevnených plôch (pokládka zámkovej dlažby)', 'dlazby', '07'),
    (4, '4-bytový dom', 'Šurianky', 'Zateplenie, rekonštrukcia bytovky', 'fasady', '06'),
    (5, 'Panelový byt', 'Nitra – Klokočina', 'Renovácia hygienických priestorov, prestavba bytového jadra', 'interier', '02'),
    (6, 'Starý mlyn', 'Lúčnica nad Žitavou', 'Rekonštrukcia starého mlyna', 'stavby', '03'),
    (7, 'Rodinné domy', 'Vráble, Nová Ves nad Žitavou', 'Vymurovanie novej fasády so zateplením', 'fasady', '02'),
    (8, 'Panelové byty', 'okolie Nitry', 'Renovovanie hygienických častí bytovky (obkladačské práce), rekonštrukcie bytových jadier', 'interier', '14'),
    (9, 'Rodinný dom – novostavba', 'Veľký Cetín', 'Terénne práce, pokládka dlažby chodníkov', 'dlazby', '02'),
    (10, 'Rodinný dom – novostavba', 'Lúčnica nad Žitavou', 'Vybudovanie prístupových ciest a terasy (pokládka zámkovej dlažby)', 'dlazby', '02'),
    (11, 'Zrekonštruovaný rodinný dom', 'Melek', 'Rekonštrukcia sedlovej strechy (nový krov, strešná krytina)', 'stavby', '01'),
    (12, 'Výškový rodinný dom', 'Vráble, Levická', 'Vybudovanie novej fasády so zateplením', 'fasady', '04'),
    (13, 'Rodinný dom – novostavba', 'Veľký Cetín', 'Vybudovanie spevnených plôch, úprava vonkajšieho terénu (pokládka zámkovej dlažby)', 'dlazby', '03'),
    (14, 'Rodinný dom s prístavbou', 'Horný Ohaj', 'Zatepľovacie práce na fasáde', 'fasady', '05'),
    (15, 'Rodinný dvojdom', 'Lúčnica nad Žitavou', 'Vybudovanie spevnených plôch (pokládka zámkovej dlažby)', 'dlazby', '04'),
    (16, 'Rodinný dom – novostavba', 'Vráble', 'Vybudovanie spevnených plôch (pokládka zámkovej dlažby)', 'dlazby', '03'),
    (17, 'Rodinný dom – novostavba', 'Horný Pial', 'Vybudovanie chodníkov (pokládka zámkovej dlažby)', 'dlazby', '04'),
    (18, 'Rodinný dom – bungalov', 'Vráble, Dukelská', 'Obkladačské práce, renovácia hygienických priestorov', 'interier', '05'),
    (19, 'Rodinný dom, záhrada', 'Nová Ves nad Žitavou', 'Vybudovanie spevnených plôch, úprava terénu a záhrady (pokládka zámkovej dlažby)', 'dlazby', '04'),
    (20, 'Zrekonštruovaný rodinný dom', 'Vráble', 'Vybudovanie terasy, obkladanie prístupových častí a plotu', 'dlazby', '04'),
]

# obec na mape → (lat, lon) z OpenStreetMap (Nominatim); kľúč = miesto pre pin
OBCE = {
    'Vráble': (48.2443, 18.3061),
    'Nová Ves nad Žitavou': (48.2849, 18.3272),
    'Golianovo': (48.2695, 18.1908),
    'Chrášťany': (48.3356, 18.3060),
    'Šurianky': (48.4215, 18.0219),
    'Nitra': (48.3010, 18.0700),
    'Lúčnica nad Žitavou': (48.2108, 18.2838),
    'Veľký Cetín': (48.2190, 18.1970),
    'Melek': (48.2008, 18.3283),
    'Horný Ohaj': (48.2640, 18.3240),
    'Horný Pial': (48.1550, 18.4485),
}
# referencia → obce, kde je pin
PIN = {1: ['Nová Ves nad Žitavou'], 2: ['Golianovo'], 3: ['Chrášťany'], 4: ['Šurianky'], 5: ['Nitra'], 6: ['Lúčnica nad Žitavou'],
       7: ['Vráble', 'Nová Ves nad Žitavou'], 8: ['Nitra'], 9: ['Veľký Cetín'], 10: ['Lúčnica nad Žitavou'], 11: ['Melek'],
       12: ['Vráble'], 13: ['Veľký Cetín'], 14: ['Horný Ohaj'], 15: ['Lúčnica nad Žitavou'], 16: ['Vráble'], 17: ['Horný Pial'],
       18: ['Vráble'], 19: ['Nová Ves nad Žitavou'], 20: ['Vráble']}

# zo stránky Naše služby (texty skrátené, zoznamy doslovne)
SLUZBY = [
    ('Zámkové dlažby, ploty a terénne úpravy',
     'Kompletná pokládka zámkovej dlažby, od poradenstva priamo u Vás (materiály a postup prác) cez realizáciu až po dokončovacie práce. '
     'Robíme aj opravy a rekonštrukcie už položených plôch. Ak nemáte vlastný materiál, zabezpečíme dlažbu, obrubníky, palisády aj podkladový materiál od renomovaných výrobcov.',
     ['úprava terénu, odstránenie vegetácie', 'dodávka materiálu', 'výkopové a zameriavacie práce', 'podkladové vrstvy, zhutňovanie',
      'obrubníky (záhonové, cestné, palisády)', 'pokládka, vibrovanie a zaspárovanie dlažby', 'výstavba plotov'],
     ('13', '04')),
    ('Keramické dlažby a obklady',
     'Lepenie keramickej dlažby a obkladov, opäť od poradenstva u Vás doma (materiály a postup prác) až po dokončovacie práce.',
     ['dodanie kompletného materiálu', 'úprava, príprava a vyčistenie podkladu', 'lepenie dlažby a obkladov',
      'dokončovacie práce, dorezávanie', 'spárovanie a čistenie'],
     ('18', '05')),
    ('Zatepľovanie, maliarske a fasádne práce',
     'Kompletná rekonštrukcia a zatepľovanie rodinných a bytových domov aj priemyselných budov: obvodové plášte, strešné konštrukcie a súvisiace úpravy. '
     'Systém volíme podľa podkladu, potrebnej hrúbky izolácie a požiarnej bezpečnosti, najčastejšie z minerálnej vlny alebo polystyrénu.',
     ['zateplenie obvodového plášťa', 'zateplenie strešných konštrukcií', 'výmena a oprava okien, dverí, balkónov',
      'fasádne práce a omietky', 'maľovky a dokončovacie práce'],
     ('07', '02')),
    ('Strechy a tesárske práce',
     'Rekonštrukcie a opravy sedlových striech, balkónových a terasových prístreškov aj altánkov.',
     ['demontáž starej krytiny', 'výmena a oprava krovu a latovania', 'rekonštrukcie komínových telies',
      'nová krytina, strešné časti a doplnky', 'klampiarske práce, odkvapové žľaby', 'kontrola strechy proti zatekaniu'],
     ('11', '02')),
    ('Rekonštrukcia bytu',
     'Kompletná rekonštrukcia bytového jadra a ostatných priestorov bytu, všetko od jednej firmy.',
     ['nosné murivá a priečky', 'obklady, keramické dlažby, obklady z kameňa', 'povrchové úpravy stien, maľovanie, stierkovanie',
      'drevené a plávajúce podlahy, opravy a izolácia podláh', 'drobné sadrokartónové práce', 'sanita, elektroinštalácia a vodoinštalácia'],
     ('08', '11')),
]

# ďalšie činnosti z úvodnej stránky (Naša činnosť), ktoré nemajú vlastný blok
DALSIE = ['Rekonštrukcie domov', 'Stavby menšieho rozsahu', 'Stavebno-montážne práce', 'Demolačné a búracie práce',
          'Murárske práce a stierky', 'Sadrokartón', 'Plastové okná a dvere', 'Projekcia a navrhovanie terénnych úprav',
          'Výroba a prenájom stavebného lešenia']

# všetkých 13 činností z úvodnej stránky (marquee)
CINNOST = ['Rekonštrukcie domov, bytov', 'Stavby menšieho rozsahu', 'Stavebno-montážne práce', 'Demolačné, búracie práce',
           'Murárske práce, stierky, fasády', 'Podlahy, sanita, sadrokartón', 'Strechy, výstavba a rekonštrukcia',
           'Maliarske, tesárske práce', 'Zámkové dlažby, ploty', 'Zatepľovanie domov, budov', 'Plastové okná, dvere',
           'Projekcia, navrhovanie terénnych úprav', 'Výroba stavebného lešenia, prenájom']

# postup spevnenej plochy = zoznam „Vybudovanie spevnených plôch zahŕňa“ zo stránky Naše služby
KROKY = [
    ('Úprava terénu', 'Odstránime vegetáciu a pripravíme terén. Ešte predtým Vám u Vás poradíme s materiálom a postupom prác.'),
    ('Dodávka materiálu', 'Dlažbu, obrubníky, palisády aj podkladový materiál zabezpečíme od renomovaných výrobcov. Ak máte vlastný materiál, použijeme ho.'),
    ('Výkop a zameranie', 'Plochu zameriame a vykopeme do potrebnej hĺbky.'),
    ('Podklad a zhutnenie', 'Navezieme a vyrovnáme podkladové vrstvy a každú poriadne zhutníme. Na podklade záleží, či dlažba o pár rokov nepoklesne.'),
    ('Obrubníky', 'Osadíme obrubníky do betónu: záhonové, cestné alebo palisády, rovno aj do oblúka.'),
    ('Pokládka a spárovanie', 'Položíme dlažbu podľa zvoleného vzoru, zavibrujeme ju a zaspárujeme.'),
    ('Plot', 'Ak treba, postavíme aj plot, aby bol pozemok hotový celý.'),
]

TYPY = ['Zámková dlažba', 'Obklady a dlažby', 'Zateplenie a fasáda', 'Strecha', 'Rekonštrukcia bytu', 'Rekonštrukcia domu', 'Lešenie', 'Iné']

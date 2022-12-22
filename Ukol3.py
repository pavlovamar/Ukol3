# Pro zvolenou množínu adresních bodů a množinu kontejnerů na tříděný odpad zjistěte průměrnou a maximální vzdálenost 
# k nejbližšímu veřejnému kontejneru na tříděný odpad. Pro každý adresní bod tedy určete nejbližší veřejný kontejner 
# na tříděný odpad a následně z těchto vzdáleností spočtěte průměr a maximum. Průměr a maximum vypište, pro maximum vypište i adresu, 
# která má nejbližší veřejný kontejner nejdále.

import json
from pyproj import Transformer
from pprint import pprint 

wgs2jtsk = Transformer.from_crs(4326,5514, always_xy = True)

try:
    with open("adresy.geojson", encoding = "utf-8") as f, \
        open("kontejnery.json", encoding = "utf-8") as h:
        data_adresy = json.load(f)
        data_kontejnery = json.load(h)
        adresy = data_adresy['features']
        features = data_kontejnery['features']
        for e in features:
            properties = e['properties']
            pristup = properties['PRISTUP']
            pristupne = 'nevim'
            if pristup == "volně":
                pristupne = 'ano'
            print(pristupne)

        for budova in adresy:
            zemepisna_sirka = budova['geometry']['coordinates'][0]
            zemepisna_delka = budova['geometry']['coordinates'][1]
            jtsk = wgs2jtsk.transform(zemepisna_sirka,zemepisna_delka)
            zemepisna_sirka_jtsk = jtsk[0]
            zemepisna_delka_jtsk = jtsk[1]






except FileNotFoundError:
    print("Soubor nebyl nalezen!")


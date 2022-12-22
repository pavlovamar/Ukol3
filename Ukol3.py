# Pro zvolenou množínu adresních bodů a množinu kontejnerů na tříděný odpad zjistěte průměrnou a maximální vzdálenost 
# k nejbližšímu veřejnému kontejneru na tříděný odpad. Pro každý adresní bod tedy určete nejbližší veřejný kontejner 
# na tříděný odpad a následně z těchto vzdáleností spočtěte průměr a maximum. Průměr a maximum vypište, pro maximum vypište i adresu, 
# která má nejbližší veřejný kontejner nejdále.

import json
from pyproj import Transformer
from pprint import pprint 
from math import sqrt

wgs2jtsk = Transformer.from_crs(4326,5514, always_xy = True)

try:
    with open("adresy.geojson", encoding = "utf-8") as f, \
        open("kontejnery.json", encoding = "utf-8") as h:
        data_adresy = json.load(f)
        data_kontejnery = json.load(h)
        for kontejner in data_kontejnery['features']:
            pristup = kontejner['properties']['PRISTUP']
            if pristup == "volně":
                zemepisna_sirka_kontejner = kontejner['geometry']['coordinates'][0]
                zemepisna_delka_kontejner = kontejner['geometry']['coordinates'][1]


        for adresa in data_adresy['features']:
            zemepisna_sirka = adresa['geometry']['coordinates'][0]
            zemepisna_delka = adresa['geometry']['coordinates'][1]
            jtsk = wgs2jtsk.transform(zemepisna_sirka,zemepisna_delka)
            zemepisna_sirka_jtsk = jtsk[0]
            zemepisna_delka_jtsk = jtsk[1]

        vzdalenost = sqrt((zemepisna_sirka_kontejner-zemepisna_sirka_jtsk)**2 + (zemepisna_delka_kontejner-zemepisna_delka_jtsk)**2)
        print(vzdalenost)





except FileNotFoundError:
    print("Soubor nebyl nalezen!")


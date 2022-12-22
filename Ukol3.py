# Pro zvolenou množínu adresních bodů a množinu kontejnerů na tříděný odpad zjistěte průměrnou a maximální vzdálenost 
# k nejbližšímu veřejnému kontejneru na tříděný odpad. Pro každý adresní bod tedy určete nejbližší veřejný kontejner 
# na tříděný odpad a následně z těchto vzdáleností spočtěte průměr a maximum. Průměr a maximum vypište, pro maximum vypište i adresu, 
# která má nejbližší veřejný kontejner nejdále.

import json
from pyproj import Transformer
from pprint import pprint 
from math import sqrt, inf

wgs2jtsk = Transformer.from_crs(4326,5514, always_xy = True)
vzdalesnot = 0
nejkratsi_vzadelnost = inf
try:
    with open("adresy.geojson", encoding = "utf-8") as f, \
        open("kontejnery.geojson", encoding = "utf-8") as h:
        data_adresy = json.load(f)
        data_kontejnery = json.load(h)
        for adresa in data_adresy['features']:
            zem_sirka = adresa['geometry']['coordinates'][0]
            zem_delka = adresa['geometry']['coordinates'][1]
            jtsk = wgs2jtsk.transform(zem_sirka,zem_delka)
            zem_sirka_adresa = jtsk[0]
            zem_delka_adresa = jtsk[1]
            ulice = adresa['properties']['addr:street']
            cislo_domu = adresa['properties']['addr:housenumber']
            soucasna_adresa = ulice, cislo_domu 
            for kontejner in data_kontejnery['features']:
                soucasny_kontejner = kontejner['properties']['ID']
                pristup = kontejner['properties']['PRISTUP']
                if pristup == "volně":
                    zem_sirka_kontejner = kontejner['geometry']['coordinates'][0]
                    zem_delka_kontejner = kontejner['geometry']['coordinates'][1]
                    vzdalenost = sqrt((zem_sirka_kontejner-zem_sirka_adresa)**2 + (zem_delka_kontejner-zem_delka_adresa)**2)
                    if vzdalenost < nejkratsi_vzadelnost:
                        nejkratsi_vzadelnost = vzdalenost
                        nejblizsi_kontejner = soucasny_kontejner
                        print(nejkratsi_vzadelnost)
                


         



except FileNotFoundError:
    print("Soubor nebyl nalezen!")


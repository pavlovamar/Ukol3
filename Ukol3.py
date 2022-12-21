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
        adresy = json.load(f)
        kontejnery = json.load(h)
        budovy = adresy['features']


        for b in budovy:
            geometrie = b['geometry']
            souradnice = geometrie['coordinates']
            wgs2jtsk.transform(souradnice)
            print(souradnice)
except FileNotFoundError:
    print("Soubor nebyl nalezen!")


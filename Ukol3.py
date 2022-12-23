# Pro zvolenou množínu adresních bodů a množinu kontejnerů na tříděný odpad zjistěte průměrnou a maximální vzdálenost 
# k nejbližšímu veřejnému kontejneru na tříděný odpad. Pro každý adresní bod tedy určete nejbližší veřejný kontejner 
# na tříděný odpad a následně z těchto vzdáleností spočtěte průměr a maximum. Průměr a maximum vypište, pro maximum vypište i adresu, 
# která má nejbližší veřejný kontejner nejdále.

import json
from pyproj import Transformer
from pprint import pprint 
from math import sqrt, inf
from statistics import mean, median

wgs2jtsk = Transformer.from_crs(4326,5514, always_xy = True)
vzdalesnot = 0
nejkratsi_vzdalenost = inf
nejblizsi_kontejner = None
novy_soubor = []
max_vzdalenost = 0
try:
    with open("adresy.geojson", encoding = "utf-8") as f, \
        open("kontejnery.geojson", encoding = "utf-8") as h:
        data_adresy = json.load(f)
        data_kontejnery = json.load(h)
        pocet_adres = len(data_adresy['features'])
        pocet_kontejneru = len(data_kontejnery['features'])
        print("Načteno " + str(pocet_adres) + " adres.")
        print ("Načteno " + str(pocet_kontejneru) + " kontejnerů na tříděný odpad.")
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
                    if vzdalenost < nejkratsi_vzdalenost or nejkratsi_vzdalenost == 0:
                        nejkratsi_vzdalenost = vzdalenost
                        nejblizsi_kontejner = soucasny_kontejner
                elif pristup == "obyvatelum domu":
                    nejkratsi_vzdalenost = 0
                
            if nejkratsi_vzdalenost > 10000:
                print("Nejbližší kontejner je dále než 10 km!")
                quit()

                    
                        
            adresa['properties']['vzdalenost k nejblizsimu kontejneru v metrech'] = round(nejkratsi_vzdalenost)
            adresa['properties']['kontejner'] = nejblizsi_kontejner
            if nejkratsi_vzdalenost > max_vzdalenost:
                max_vzdalenost = nejkratsi_vzdalenost
                adresa_nejdale = soucasna_adresa

            nejkratsi_vzdalenost = 0
            novy_soubor.append(adresa)


            

         



except FileNotFoundError:
    print("Soubor nebyl nalezen!")



with open("adresy_kontejnery.geojson", "w", encoding = "utf-8") as nacteni:
    json.dump(novy_soubor, nacteni, ensure_ascii = False, indent = 2)

nejkratsi_vzdalenosti = [adresa["properties"]["vzdalenost k nejblizsimu kontejneru v metrech"] for adresa in data_adresy["features"]]

print("Průměrná vzdálenost ke kontejneru je " + str(round(mean(nejkratsi_vzdalenosti))) + " metrů.")
print("Madián nejkratších vzdáleností ke kontejneru je " + str(round(median(nejkratsi_vzdalenosti))) + " metrů")
print("Nejdále od kontejneru je to " + str(round(max_vzdalenost)) + " metrů a to ze vchodu na adrese " + str(adresa_nejdale))

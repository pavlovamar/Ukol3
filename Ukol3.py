import json
from pyproj import Transformer
from math import sqrt, inf
from statistics import mean, median
from json.decoder import JSONDecodeError

wgs2jtsk = Transformer.from_crs(4326,5514, always_xy = True)
vzdalenost = 0
min_vzdalenost = inf
nejblizsi_kontejner = None
novy_soubor = []
max_vzdalenost = 0

try:
    with open ("adresy.geojson", encoding = "utf-8") as f:
        data_adresy = json.load(f)
except FileNotFoundError:
    print("Soubor nebyl nalezen!")
except PermissionError:
    print("Není oprávnění tento soubor otevřít!")
except JSONDecodeError:
    print("Soubor není validní!")

try:
    with open ("kontejnery.geojson", encoding = "utf-8") as g:
        data_kontejnery = json.load(g)
except FileNotFoundError:
    print("Soubor nebyl nalezen!")
except PermissionError:
    print("Není oprávnění tento soubor otevřít!")
except JSONDecodeError:
    print("Soubor není validní!")

print(f"Načteno {len(data_adresy['features'])} adres.")
print(f"Načteno {len(data_kontejnery['features'])} kontejnerů.")

try:
    for adresa in data_adresy['features']:
        zem_sirka = adresa['geometry']['coordinates'][0]                                #Transformace souřadnic do s-jtsk
        zem_delka = adresa['geometry']['coordinates'][1]
        jtsk = wgs2jtsk.transform(zem_sirka,zem_delka)
        soucasna_adresa = adresa['properties']['addr:street'] + " " + adresa['properties']['addr:housenumber']
        for kontejner in data_kontejnery['features']:
            soucasny_kontejner = kontejner['properties']['ID']
            pristup = kontejner['properties']['PRISTUP']
            if pristup == "volně":                                                      #Výpočet vzdálenosti pro volně přístupné kontejnery
                zem_sirka_kont = kontejner['geometry']['coordinates'][0]
                zem_delka_kont = kontejner['geometry']['coordinates'][1]
                vzdalenost = sqrt((zem_sirka_kont-jtsk[0])**2 + (zem_delka_kont-jtsk[1])**2)
                if vzdalenost < min_vzdalenost or min_vzdalenost == 0:
                    min_vzdalenost = vzdalenost
                    nejblizsi_kontejner = soucasny_kontejner
                elif pristup == "obyvatelum domu":
                    min_vzdalenost = 0
        if min_vzdalenost > 10000:
            print(f"Pro adresu {soucasna_adresa} je nejbližší kontejner dále než 10 km! Zkuste načíst jiný soubor")
            quit()
        if min_vzdalenost > max_vzdalenost:                                            #Určení maximální nejkratší vzdálenosti
            max_vzdalenost = min_vzdalenost
            adresa_nejdale = soucasna_adresa
        adresa['properties']['kontejner'] = nejblizsi_kontejner     
        adresa['properties']['vzdalenost ke kontejneru v m'] = round(min_vzdalenost)
        novy_soubor.append(adresa)
        min_vzdalenost = 0
except KeyError:
    print("V souboru je chyba!")
    quit()
    
try: 
    with open("adresy_kontejnery.geojson", "w", encoding = "utf-8") as nacteni:                    #Načtení do nového souboru
        json.dump(novy_soubor, nacteni, ensure_ascii = False, indent = 2)
except PermissionError:
    print("Namáte oprávnění tento soubor vytvořit/otevřít")

min_vzdalenosti = [adresa['properties']['vzdalenost ke kontejneru v m'] for adresa in data_adresy['features']]          #Uložení všech nejkratších vzdáleností

print(f"Průměrná vzdálenost ke kontejneru je {round(mean(min_vzdalenosti))} metrů.")
print(f"Madián nejkratších vzdáleností ke kontejneru je {round(median(min_vzdalenosti))} metrů")
print(f"Nejdále od kontejneru je to {round(max_vzdalenost)} metrů a to ze vchodu na adrese {adresa_nejdale}")
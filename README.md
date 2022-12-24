## Uživatelská dokumentace

Program načte dva vstupní soubory, jeden s množinou aderesních bodů a druhý s množinou kontejnerů. Následně spočítá vzdálenosti kontejnerů od daných adres a uloží tu nejmenší z nich.  Z těchto vzdáleností dále spočítá a vypíše průměr, medián a také maximální vzdálenost k nejbližsímu kontejneru. Pro toto maximum vypíše i ke které adrese patří. 

Vstupní soubor s adresami se jmenuje <i>adresy.geojson</i> a vstupní soubor s kontejnery se jmenuje <i>kontejnery.geojson</i>.

Program vytvoří nový soubour s názvem <i>adresy_kontejnery</i>, který má stejnou strukturu jako vstupní soubor s adresami, ale nevíc má v klíči <i>kontejner</i> uloženo ID nejbližšího kontejneru a také vzdálesnot k němu určenu v metrech. 


## Vývojářská dokumentace


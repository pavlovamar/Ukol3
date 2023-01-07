### Uživatelská dokumentace

Program načte dva vstupní soubory, jeden s množinou aderesních bodů a druhý s množinou kontejnerů. Tyto dva soubory jsou ve formátu <i>GeoJSON</i>. Následně spočítá vzdálenosti kontejnerů od daných adres a uloží tu nejmenší z nich.  Z těchto vzdáleností dále spočítá a vypíše průměr, medián a také maximální vzdálenost k nejbližsímu kontejneru.

Vstupní soubor s adresami se jmenuje <i>adresy.geojson</i> a vstupní soubor s kontejnery se jmenuje <i>kontejnery.geojson</i>. Soubor s kontejnery je v souřadnicovém systému JTSK a soubor s adresními bodami je v souřadnicovém systému WGS84. Souřadnice adresních bodů se automaticky převedou na souřadnice S-JTSK. 

Struktura souboru s adresami by měla vypadat takto: <br>
<i>features</br>
&#160;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;properties<br>
&#160;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&#160;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;addr:housenumber<br>
&#160;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&#160;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;addr:street<br>
&#160;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;geometry<br>
&#160;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&#160;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;coordinates</i>

Struktura souboru s kontejnery by měla vypadat takto:<br>
<i>features <br>
&#160;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;propeties<br>
&#160;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&#160;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;PRISTUP<br>
&#160;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;geometry <br>
&#160;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&#160;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;coordinates<br></i>

Z atributů <i>addr:housenumber</i> a <i>addr:street</i> zjišťujeme adresu daného domu. V atributu <i>coordinates</i> jsou uloženy souřadnice. V atribut <i>PRISTUP</i> je uvedeno, zda je kontejner přístupný pro všechny (<i>volně</i>) nebo jen obyvatelům domu.

Program vypíše kolik do něj bylo načteno adresních bodů a kolik kontejnerů. Dále také vytvoří nový soubour s názvem <i>adresy_kontejnery</i>, který má stejnou strukturu jako vstupní soubor s adresami, ale navíc má v klíči <i>kontejner</i> uloženo ID nejbližšího kontejneru a v klíči <i>vzdalenost ke kontejneru v m</i> také vzdálesnot k němu určenou v metrech. 


### Vývojářská dokumentace

Program zkontroluje, zda vstupní soubory existují, jsou přístupné a validní. Pokud některou z těchto podmínek nesplňují, program se ukončí s chybovou hláškou. Pokud jsou vstupní soubory v pořádku, vypíše program do konzole počet načtených adresních bodů a kontejnerů. Nejdříve převede souřadnice adresních bodů z WGS84 do S-JTSK, aby se následně mohli pomocí Pythagorovy věty počítat vzdálenosti. Vypočítají se vzdálenosti pro volně přístupné kontejnery, přičemž se pro každou adresu ukládají ty nejkratší z nich. Pokud je kontejner přístupný pouze obyvatelům domu, vzdálenost se nepočítá a je automaticky rovna 0. Pokud je nejbližší kontejner vzdálen více než 10 km, je program ukočen. Program také průběžně ukládá maximální nejkratší vzdálenost a adresu, ke které se vztahuje. 

Dojde k vytvoření dvou nových klíčů, a to <i>kontejner</i> a <i>vzdalenost ke kontejneru v m</i>, které se následně načtou k nově vzniklému souboru <i>adresy_kontejnery.geojson</i>. Dále dojde k uložení všeh nejkratších vzdáleností a následně se spočítá jejich průměr a medián. Do konzole se vypíší tyto výsledky spolu s maximální nejkratší vzdáleností ke kontejneru. 

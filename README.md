# Web_Scraping---Finn.no_boligannonser
Scrapy CrawlSpider på Finn.no boligannonser + maskinlæring med lineær regresjon

Jeg har laget en Scrapy Spider som crawler finn.no sine bolig annonser og henter ut data på de ulike boligene. Selve spideren ligger i **finnSpider/spiders/annonseSpider.py** og alle item er definert i **finnSpider/items.py**. All dataen som spideren finner lagres i en .csv fil: **all_regions.csv**.

Spideren har også en enkel tekstoppsummering ved bruk av Natural Language Processing (NLP). Jeg har brukt Python-biblioteket SpaCy for å gjennomføre tekstoppsummering på avsnittet "Om boligen" fra alle boligannonsene. 

**boligpriser.ipynb** er en Jupyter Notebook hvor dataene blir studert og preprosessert før det trenes modeller med lineær regresjon for å predicte boligpriser. 

Spideren henter følgende data:
- url
- prisantydning
- totalpris
- megler
- by
- adresse
- omkostninger
- felleskost_mnd
- kommunale_avg
- formuesverdi
- boligtype
- eieform
- soverom
- etasje
- primærrom
- bruksareal
- tomteareal
- bruttoareal
- byggeår
- energimerking
- om_boligen

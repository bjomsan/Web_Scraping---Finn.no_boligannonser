# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class FinnAnnonser(scrapy.Item):
    url = scrapy.Field()
    prisantydning = scrapy.Field()
    totalpris = scrapy.Field()
    megler = scrapy.Field()
    by = scrapy.Field()
    adresse = scrapy.Field()
    omkostninger = scrapy.Field()
    felleskost_mnd = scrapy.Field()
    kommunale_avg = scrapy.Field()
    formuesverdi = scrapy.Field()
    boligtype = scrapy.Field()
    eieform = scrapy.Field()
    soverom = scrapy.Field()
    etasje = scrapy.Field()
    primærrom = scrapy.Field()
    bruksareal = scrapy.Field()
    tomteareal = scrapy.Field()
    bruttoareal = scrapy.Field()
    byggeår = scrapy.Field()
    energimerking = scrapy.Field()
    om_boligen = scrapy.Field()
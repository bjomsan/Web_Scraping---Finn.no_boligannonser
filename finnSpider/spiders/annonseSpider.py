from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from finnSpider.items import FinnAnnonser
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from collections import Counter
from heapq import nlargest
import re
import spacy


"""
    Først lager vi noen funksjoner som senere brukes til å 
    endre dataen vi scraper før den lagres.
    
    string_converter()
        - fjerner bokstaver slik at vi sitter igjen med bare tall
          og konverterer str til int. Det er nødvendig siden alle priser
          er strenger med tusendelsseparator eks: 5&nbsp;400&nbsp;000 (5400000)

    text_summarizer()
        - kjører NLP (Natural language processing) på en input str.
          Denne kjøres på avsnittene "om boligen" i alle boligannonser
          for å kutte ned på mengden tekst, men fortsatt få med det viktigste.

    For å scrape alle boligannonsene bruker jeg Scrapy sin CrawlSpider. Fordelen med CrawlSpider
    er at den følger gitte regler og crawler automatisk videre til neste siden.
"""


# fjerner non-digit fra input string 
def string_converter(element):
    element = re.findall('\d', element)
    element = ''.join(element)
    return int(element)

# tekst oppsummering
nlp = spacy.load("nb_core_news_md")
def text_summarizer(input):
    doc = nlp(input)

    # nøkkelord
    keyword = []
    stopwords = list(STOP_WORDS)
    pos_tag = ["PROPN", "ADJ", "NOUN", "VERB"]
    for token in doc:
        if(token.text in stopwords or token.text in punctuation):
            continue
        if(token.pos_ in pos_tag):
            keyword.append(token.text)

    # normalisering    
    freq_word = Counter(keyword)
    most_common = freq_word.most_common(5)
    if most_common:
        max_freq = most_common[0][1]
        for word in freq_word.keys():
            freq_word[word] = (freq_word[word]/max_freq)
    else:
        max_freq = 1
    freq_word.most_common(5)

    # veeing av setning
    sent_strength = {}
    for sent in doc.sents:
        for word in sent:
            if word.text in freq_word.keys():
                if sent in sent_strength.keys():
                    sent_strength[sent] += freq_word[word.text]
                else:
                    sent_strength[sent] = freq_word[word.text]
    
    summarized_sentence = nlargest(3, sent_strength, key=sent_strength.get)
    final_sentences = sorted(summarized_sentence, key=lambda s: s.start)
    final_sentences = [w.text for w in summarized_sentence]
    summary = " ".join(final_sentences)

    # returner oppsummert tekst
    return summary


class FinnArticleSpider(CrawlSpider):
    name = 'finn_articles'
    link_count = 0

    custom_settings = {
         'FEED_EXPORT_FIELDS': ['url', 'prisantydning', 'totalpris', 'megler', 'by', 'adresse', 'omkostninger', 'felleskost_mnd',
                                'kommunale_avg', 'formuesverdi', 'boligtype', 'eieform', 'soverom',
                                'primærrom', 'bruksareal', 'tomteareal', 'bruttoareal', 'byggeår', 'energimerking', 'om_boligen'],
    }

    allowed_domains = ['finn.no']
        # 'https://www.finn.no/realestate/homes/search.html?is_new_property=false&ownership_type=3&ownership_type=4&property_type=1&property_type=3&sort=PUBLISHED_DESC'
    start_urls = [
                "https://www.finn.no/realestate/homes/search.html?is_new_property=false&location=0.22042&ownership_type=3&ownership_type=4&property_type=1&property_type=3&sort=PUBLISHED_DESC",
                "https://www.finn.no/realestate/homes/search.html?is_new_property=false&location=0.22034&ownership_type=3&ownership_type=4&property_type=1&property_type=3&sort=PUBLISHED_DESC",
                "https://www.finn.no/realestate/homes/search.html?is_new_property=false&location=0.20015&ownership_type=3&ownership_type=4&property_type=1&property_type=3&sort=PUBLISHED_DESC",
                "https://www.finn.no/realestate/homes/search.html?is_new_property=false&location=0.20018&ownership_type=3&ownership_type=4&property_type=1&property_type=3&sort=PUBLISHED_DESC",
                "https://www.finn.no/realestate/homes/search.html?is_new_property=false&location=0.20061&ownership_type=3&ownership_type=4&property_type=1&property_type=3&sort=PUBLISHED_DESC",
                "https://www.finn.no/realestate/homes/search.html?is_new_property=false&location=0.20012&ownership_type=3&ownership_type=4&property_type=1&property_type=3&sort=PUBLISHED_DESC",
                "https://www.finn.no/realestate/homes/search.html?is_new_property=false&location=0.22054&ownership_type=3&ownership_type=4&property_type=1&property_type=3&sort=PUBLISHED_DESC",
                "https://www.finn.no/realestate/homes/search.html?is_new_property=false&location=0.20016&ownership_type=3&ownership_type=4&property_type=1&property_type=3&sort=PUBLISHED_DESC",
                "https://www.finn.no/realestate/homes/search.html?is_new_property=false&location=0.22038&ownership_type=3&ownership_type=4&property_type=1&property_type=3&sort=PUBLISHED_DESC",
                "https://www.finn.no/realestate/homes/search.html?is_new_property=false&location=0.22046&ownership_type=3&ownership_type=4&property_type=1&property_type=3&sort=PUBLISHED_DESC",
                "https://www.finn.no/realestate/homes/search.html?is_new_property=false&location=0.22030&ownership_type=3&ownership_type=4&property_type=1&property_type=3&sort=PUBLISHED_DESC",
                  ]
    
    rules = [
            Rule(LinkExtractor(allow=r"https://www\.finn\.no/realestate/homes/ad\..*"),
                callback="parse_items",follow=False),
            Rule(LinkExtractor(restrict_xpaths=('//a[@aria-label="Neste resultatside"]')),
                follow=True)
            ]

    def parse_items(self, response):
        article = FinnAnnonser()
        
        try:
            article['url'] = response.url
        except:
            article['url'] = None

        try:
            article['prisantydning'] = string_converter(response.xpath('//span[@class="text-28 font-bold"]/text()').extract_first())
        except:
            article['prisantydning'] = None

        try:
            article['totalpris'] = string_converter(response.xpath('//div[@data-testid="pricing-total-price"]/dd/text()').extract_first())
        except:
            article['totalpris'] = string_converter(response.xpath('//span[@class="text-28 font-bold"]/text()').extract_first())

        try:
            article['megler'] = response.xpath('//h2[@class="ExtendedProfileBox-module_companyName__QzPMU font-normal text-16 mb-8"]/text()').extract_first()
        except:
            article['megler'] = None

        try:
            article['by'] = str(response.xpath('//span[@data-testid="object-address"][1]/text()').extract_first()).split()[-1]
        except:
            article['by'] = None

        try:
            article['adresse'] = response.xpath('//span[@data-testid="object-address"][@class="pl-4"]/text()').extract_first()
        except:
            article['adresse'] = None

        try:    
            article['omkostninger'] = string_converter(response.xpath('//div[@data-testid="pricing-registration-charge"]/dd/text()').extract_first())
        except:
            article['omkostninger'] = None

        try:
            article['felleskost_mnd'] = string_converter(response.xpath('//div[@data-testid="pricing-common-monthly-cost"]/dd/text()').extract_first())
        except:
            article['felleskost_mnd'] = None
        
        try:
            article['kommunale_avg'] = string_converter(response.xpath('//div[@data-testid="pricing-municipal-fees"]/dd/text()').extract_first())
        except:
            article['kommunale_avg'] = None
        
        try:
            article['formuesverdi'] = string_converter(response.xpath('//div[@data-testid="pricing-tax-value"]/dd/text()').extract_first())
        except:
            article['formuesverdi'] = None

        try:
            temp = response.xpath('//div[@data-testid="info-property-type"]/dd/text()').extract_first()
            if temp == "Leilighet":
                article['boligtype'] = "l"
            elif temp == "Enebolig":
                article['boligtype'] = "e"
        except:
            article['boligtype'] = None

        try:
            temp= response.xpath('//div[@data-testid="info-ownership-type"]/dd/text()').extract_first()
            if temp == "Eier (Selveier)":
                article['eieform'] = "e"
            elif temp == "Andel":
                article['eieform'] = "a"
        except:
            article['eieform'] = None
        
        try:
            article['soverom'] = string_converter(response.xpath('//div[@data-testid="info-bedrooms"]/dd/text()').extract_first())
        except:
            article['soverom'] = None

        try:
            article['etasje'] = int(response.xpath('//div[@data-testid="info-floor"]/dd/text()').extract_first())
        except:
            article['etasje'] = None

        try:
            article['primærrom'] = string_converter(response.xpath('//div[@data-testid="info-primary-area"]/dd/text()').extract_first())
        except:
            article['primærrom'] = None

        try: 
            article['bruksareal'] = string_converter(response.xpath('//div[@data-testid="info-usable-area"]/dd/text()').extract_first())
        except:
            article['bruksareal'] = None

        try:
            article['tomteareal'] = string_converter(response.xpath('//div[@data-testid="info-plot-area"]/dd/text()').extract_first())
        except:
            article['tomteareal'] = None

        try:
            article['bruttoareal'] = string_converter(response.xpath('//div[@data-testid="info-gross-area"]/dd/text()').extract_first())
        except:
            article['bruttoareal'] = None

        try: 
            article['byggeår'] = int(response.xpath('//div[@data-testid="info-construction-year"]/dd/text()').extract_first())
        except:
            article['byggeår'] = None

        try:
            article['energimerking'] = str(response.xpath('//span[@data-testid="energy-label-info"]/text()').extract_first())[0]
        except:
            article['energimerking'] = None

        try:
            temp = response.xpath('//div[@data-testid="om boligen"]/div/text()').extract()
        except:
            try:
                temp = response.xpath('//div[@class="description-area whitespace-pre-wrap"]/p/text()').extract()
            except:
                temp = None
        if temp is not None:
            temp = ' '.join(temp)
            article['om_boligen'] = text_summarizer(temp)
        else:
            article['om_boligen'] = None


        yield article
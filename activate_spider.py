from finnSpider.spiders.annonseSpider import FinnArticleSpider
from scrapy.crawler import CrawlerProcess

def main():
    process = CrawlerProcess(settings = {
        'FEED_URI': 'all_regions.csv',
        'FEED_FORMAT': 'csv',
        })
    
    process.crawl(FinnArticleSpider)
    process.start()


if __name__ == '__main__':
    main()





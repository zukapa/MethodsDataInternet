from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from instaparser.spiders.ig import IgSpider
from instaparser import settings


if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)
    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(IgSpider)
    process.start()


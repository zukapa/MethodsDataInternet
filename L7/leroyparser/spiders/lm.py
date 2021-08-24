import scrapy
from scrapy.http import HtmlResponse
from leroyparser.items import LeroyparserItem
from scrapy.loader import ItemLoader


class LmSpider(scrapy.Spider):
    name = 'lm'
    allowed_domains = ['leroymerlin.ru']

    def __init__(self, param):
        super(LmSpider, self).__init__()
        self.start_urls = [f'https://leroymerlin.ru/catalogue/{param}/']

    def parse(self, response:HtmlResponse):
        button_next = response.xpath("//a[@data-qa-pagination-item='right']/@href").extract_first()
        if button_next:
            yield response.follow(button_next, callback=self.parse)
        links = response.xpath("//a[@data-qa='product-name']")
        for link in links:
            yield response.follow(link, callback=self.parse_ads)

    def parse_ads(self, response: HtmlResponse):
        loader = ItemLoader(item=LeroyparserItem(), response=response)
        loader.add_xpath('name', "//h1/text()")
        loader.add_xpath('photos', "//source[contains(@media, '1024')]/@srcset")
        loader.add_xpath('price', "//span[@slot='price']/text()")
        loader.add_xpath('property', "//div[@class='def-list__group']//text()")
        loader.add_value("url", response.url)
        yield loader.load_item()

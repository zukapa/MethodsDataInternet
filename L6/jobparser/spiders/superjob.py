import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem


class SuperjobSpider(scrapy.Spider):
    name = 'superjob'
    allowed_domains = ['superjob.ru']
    start_urls = ['https://www.superjob.ru/vacancy/search/?catalogues%5B0%5D=48&geo%5Bt%5D%5B0%5D=4&click_from=facet']

    def parse(self, response: HtmlResponse):
        button_next = response.xpath("//a[@rel='next'][1]/@href").extract_first()
        if button_next:
            yield response.follow(button_next, callback=self.parse)
        links = response.xpath("//a[contains(@class, 'icMQ_ _6AfZ9 f-test-link-')]/@href").extract()
        for link in links:
            yield response.follow(link, callback=self.vacancy_parse)

    def vacancy_parse(self, response: HtmlResponse):
        name = response.xpath("//h1/text()").extract_first()
        salary = response.xpath("//span[@class='_1h3Zg _2Wp8I _2rfUm _2hCDz']//text()").extract()
        link = response.url
        source = self.allowed_domains[0]
        yield JobparserItem(name=name, salary=salary, link=link, source=source)
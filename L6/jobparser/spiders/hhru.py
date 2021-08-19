import scrapy
import re
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem


class HhruSpider(scrapy.Spider):
    name = 'hhru'
    allowed_domains = ['hh.ru']
    start_urls = ['https://spb.hh.ru/search/vacancy?st=searchVacancy&L_profession_id=29.8&area=2&no_magic=true&%27%27'
                  'text=%D0%9F%D1%80%D0%BE%D0%B3%D1%80%D0%B0%D0%BC%D0%BC%D0%B8%D1%81%D1%82+Python%27&customDomain=1']

    def parse(self, response: HtmlResponse):
        button_next = response.xpath("//a[@data-qa='pager-next']/@href").extract_first()
        if button_next:
            yield response.follow(button_next, callback=self.parse)
        links = response.xpath("//a[@class='bloko-link']/@data-qa/../@href").extract()
        for link in links:
            yield response.follow(link, callback=self.vacancy_parse)

    def vacancy_parse(self, response: HtmlResponse):
        if len(re.findall('vacancy', response.url)) > 0:
            name = response.xpath("//h1/text()").extract_first()
            salary = response.xpath("//p[contains(@class, 'vacancy-salary')]//text()").extract_first()
            link = response.url
            source = self.allowed_domains[0]
            yield JobparserItem(name=name, salary=salary, link=link, source=source)

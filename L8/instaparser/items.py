import scrapy


class InstaparserItem(scrapy.Item):
    who_is = scrapy.Field()
    user = scrapy.Field()
    sub_name = scrapy.Field()
    sub_id = scrapy.Field()
    sub_picture = scrapy.Field()

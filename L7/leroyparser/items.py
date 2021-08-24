import scrapy
from itemloaders.processors import MapCompose, TakeFirst, Compose


def property_new(ppy):
    no_space = ' '.join(ppy.split())
    if no_space != '':
        return no_space


def type_int(value):
    return int(value[0].replace(' ', ''))


class LeroyparserItem(scrapy.Item):
    name = scrapy.Field(output_processor=TakeFirst())
    photos = scrapy.Field()
    price = scrapy.Field(input_processor=Compose(type_int), output_processor=TakeFirst())
    property = scrapy.Field(input_processor=MapCompose(property_new))
    url = scrapy.Field(output_processor=TakeFirst())

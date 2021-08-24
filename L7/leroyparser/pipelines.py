from itemadapter import ItemAdapter
from pymongo import MongoClient
from scrapy.pipelines.images import ImagesPipeline
import scrapy


class LeroyparserPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.db = client['goods']

    def process_item(self, item, spider):
        product_ppy = {}
        keys = []
        values = []
        for i, v in enumerate(item['property']):
            if i % 2 == 0:
                keys.append(v)
            if i % 2 == 1:
                values.append(v)
        for i, v in enumerate(keys):
            product_ppy[f'{v}'] = values[i]

        product = {'name': item['name'],
                   'photos': item['photos'],
                   'price': item['price'],
                   'property': product_ppy,
                   'url': item['url']}
        collection = self.db[spider.name]
        collection.insert_one(product)
        return item


class LeroyPhotosPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item['photos']:
            for img in item['photos']:
                try:
                    yield scrapy.Request(img)
                except Exception as e:
                    print(e)

    def item_completed(self, results, item, info):
        if results:
            item['photos'] = [info[1] for info in results if info[0]]
        return item

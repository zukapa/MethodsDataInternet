from pymongo import MongoClient


class InstaparserPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.db = client['insta_subscriptions']

    def process_item(self, item, spider):
        sub_user = {'who_is': item['who_is'],
                    'user': item['user'],
                    'sub_name': item['sub_name'],
                    'sub_id': item['sub_id'],
                    'sub_picture': item['sub_picture']}
        collection = self.db[spider.name]
        collection.insert_one(sub_user)
        return item

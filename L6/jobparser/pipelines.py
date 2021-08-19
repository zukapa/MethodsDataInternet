from pymongo import MongoClient
import re


class JobparserPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.db = client['vacancy']

    def process_item(self, item, spider):
        if spider.name == 'hhru':
            salary_db_h = {}
            salary_min_h = None
            salary_max_h = None
            if len(re.findall('\xa0', item['salary'])) > 0:
                salary_h = item['salary'].replace('\xa0', '').split()
                if salary_h[2] == 'до':
                    salary_min_h = int(salary_h[1])
                    salary_max_h = int(salary_h[3])
                if len(salary_h) == 3:
                    salary_min_h = int(salary_h[1])
                    salary_max_h = None
                if salary_h[0] == 'до':
                    salary_min_h = None
                    salary_max_h = int(salary_h[1])
            salary_db_h['name'] = item['name']
            salary_db_h['salary_min'] = salary_min_h
            salary_db_h['salary_max'] = salary_max_h
            salary_db_h['link'] = item['link']
            salary_db_h['source'] = item['source']
            collection = self.db[spider.name]
            collection.insert_one(salary_db_h)
        if spider.name == 'superjob':
            salary_db_s = {}
            salary_sj = ''.join(item['salary'])
            salary_min_s = None
            salary_max_s = None
            if len(re.findall('\xa0', salary_sj)) > 0:
                salary_s = salary_sj.replace('\xa0', ' ').split()
                if salary_s[2] == '—':
                    salary_min_s = int(f'{salary_s[0]}{salary_s[1]}')
                    salary_max_s = int(f'{salary_s[3]}{salary_s[4]}')
                if salary_s[0] == 'от':
                    if len(salary_s) == 3:
                        salary_min_s = int(salary_s[1])
                        salary_max_s = None
                    else:
                        salary_min_s = int(f'{salary_s[1]}{salary_s[2]}')
                        salary_max_s = None
                if salary_s[0] == 'до':
                    salary_min_s = None
                    salary_max_s = int(f'{salary_s[1]}{salary_s[2]}')
            salary_db_s['name'] = item['name']
            salary_db_s['salary_min'] = salary_min_s
            salary_db_s['salary_max'] = salary_max_s
            salary_db_s['link'] = item['link']
            salary_db_s['source'] = item['source']
            collection = self.db[spider.name]
            collection.insert_one(salary_db_s)
        return item

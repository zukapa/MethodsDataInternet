from lxml import html
import requests
import re
from pymongo import MongoClient


header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                        'Chrome/92.0.4515.107 Safari/537.36'}
url = 'https://lenta.ru'
response = requests.get(url, headers=header)
dom = html.fromstring(response.text)
news_dom = dom.xpath("//time[@class='g-time']/../..")
client = MongoClient('127.0.0.1', 27017)
db = client['news']
news_db = db.news
news = []
for ni in news_dom:
    news_item = {}
    name = ni.xpath(".//a/text()")[0]
    link = ni.xpath(".//a/@href")[0]
    date = ni.xpath(".//a/time/@title")[0]
    if len(re.findall('\xa0', name)) != 0:
        name = ni.xpath(".//a/text()")[0].replace('\xa0', ' ')
    if link[0] == '/':
        link = f'{url}{link}'
    if date[0] == ' ':
        date = date[1:]
    news_item['name'] = name
    news_item['link'] = link
    news_item['date'] = date
    news_item['source'] = url
    news.append(news_item)
news_db.insert_many(news)

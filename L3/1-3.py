from bs4 import BeautifulSoup as bs
import requests
import re
from pymongo import MongoClient


def initial_parser(page):
    url = 'https://hh.ru/search/vacancy'
    params = {'text': 'Web-программист',
              'page': page}
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/92.0.4515.107 Safari/537.36'}
    response = requests.get(url, params=params, headers=headers)
    soup = bs(response.text, 'html.parser')
    find_next_button = soup.find('a', attrs={'class': 'bloko-button'})
    vacancy_url = soup.find_all('div', attrs={'class': 'vacancy-serp-item'})
    return vacancy_url, find_next_button


def initial_mongo():
    client = MongoClient('127.0.0.1', 27017)
    db = client['vacancy']
    web_programmer = db.web_programmer
    return web_programmer


def create_vacancy_list(vacancy_list):
    vacancy_selection = []
    for vacancy in vacancy_list:
        vacancy_data = {}
        vacancy_name = vacancy.find('a', attrs={'class': 'bloko-link'}).text
        vacancy_salary = vacancy.find_all('span', attrs={'class': 'bloko-header-section-3 bloko-header-section-3_lite'})
        space_true = 0
        vacancy_salary_min = None
        vacancy_salary_max = None
        vacancy_salary_currency = None
        vacancy_link = vacancy.find('a', attrs={'class': 'bloko-link'}).get('href')
        if len(vacancy_salary) > 1:
            space = vacancy_salary[1].getText().split(' ')
            for vac in space:
                if len(re.findall('\u202f', vac)) != 0:
                    space_true = 1
                    break
            if space_true == 0:
                vacancy_salary = space
            else:
                vacancy_salary = vacancy_salary[1].getText().replace('\u202f', '').split()
        if vacancy_salary.count('–') == 1:
            vacancy_salary_min = int(vacancy_salary[0])
            vacancy_salary_max = int(vacancy_salary[2])
            vacancy_salary_currency = vacancy_salary[3]
        if vacancy_salary.count('от') == 1:
            vacancy_salary_min = int(vacancy_salary[1])
            vacancy_salary_max = None
            vacancy_salary_currency = vacancy_salary[2]
        if vacancy_salary.count('до') == 1:
            vacancy_salary_min = None
            vacancy_salary_max = int(vacancy_salary[1])
            vacancy_salary_currency = vacancy_salary[2]
        vacancy_data['name'] = vacancy_name
        vacancy_data['salary_min'] = vacancy_salary_min
        vacancy_data['salary_max'] = vacancy_salary_max
        vacancy_data['salary_currency'] = vacancy_salary_currency
        vacancy_data['link'] = vacancy_link
        vacancy_selection.append(vacancy_data)
    return vacancy_selection


def build_vacancy_list():
    full_vacancy_selection = []
    count = 0
    parser_data = initial_parser(count)
    if parser_data[1] is not None:
        while parser_data[1] is not None:
            part_data = create_vacancy_list(parser_data[0])
            for vacancy in part_data:
                full_vacancy_selection.append(vacancy)
            count += 1
            parser_data = initial_parser(count)
    return full_vacancy_selection


def save_mongo(data):
    connect = initial_mongo()
    connect.insert_many(data)
    return connect


def save_new_mongo(data):
    connect = initial_mongo()
    for vac in data:
        if connect.count_documents({'link': vac['link']}) == 0:
            connect.insert_one(vac)
    return connect


def print_greater_salary(salary):
    connect = initial_mongo()
    greater_salary = connect.find({'$or': [{'salary_max': {'$gte': salary}}, {'salary_min': {'$gte': salary}}]},
                                  {'name': 1, 'salary_min': 1, 'salary_max': 1, 'salary_currency': 1, '_id': 0})
    for sal in greater_salary:
        print(sal)


save_mongo(build_vacancy_list())  # comment out after first running
# save_new_mongo(build_vacancy_list())  # uncomment after running save_mongo()
print_greater_salary(100000)

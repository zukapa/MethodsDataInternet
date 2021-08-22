import scrapy
import os
import re
from scrapy.http import HtmlResponse
from dotenv import load_dotenv
from instaparser.items import InstaparserItem

env = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path=env)


class IgSpider(scrapy.Spider):
    name = 'ig'
    allowed_domains = ['instagram.com']
    start_urls = ['https://www.instagram.com/']
    login_url_instagram = 'https://www.instagram.com/accounts/login/ajax/'
    login_instagram = os.getenv('LOGIN')
    password_instagram = os.getenv('PASSWORD')
    user_names = ['nataicq', 'oalianova']
    url_subscribe = f'https://i.instagram.com/api/v1/friendships'

    def parse(self, response:HtmlResponse):
        csrf = re.findall('csrf_token":"(\w+)', response.text)
        yield scrapy.FormRequest(self.login_url_instagram,
                                 method='POST',
                                 callback=self.login,
                                 formdata={'username': self.login_instagram,
                                           'enc_password': self.password_instagram},
                                 headers={'x-csrftoken': csrf})

    def login(self, response: HtmlResponse):
        j_data = response.json()
        if j_data['authenticated']:
            for user in self.user_names:
                yield response.follow(f'/{user}',
                                      callback=self.user_parse,
                                      cb_kwargs={'username': user})

    def user_parse(self, response: HtmlResponse, username):
        user_id = re.findall('{"id":"(\w+)', response.text)[0]
        url_subscriptions = f'{self.url_subscribe}/{user_id}/following/?count=12'
        yield response.follow(url_subscriptions,
                              callback=self.user_data_parse,
                              cb_kwargs={'username': username,
                                         'user_id': user_id})
        url_subscribers = f'{self.url_subscribe}/{user_id}/followers/?count=12&search_surface=follow_list_page'
        yield response.follow(url_subscribers,
                              callback=self.user_data_parse,
                              cb_kwargs={'username': username,
                                         'user_id': user_id})

    def user_data_parse(self, response: HtmlResponse, username, user_id):
        j_subscribers = response.json()
        if j_subscribers['big_list']:
            if len(re.findall('following', response.url)) == 1:
                url_subscriptions = f'{self.url_subscribe}/{user_id}/following/?count=12&' \
                                    f'max_id={j_subscribers["next_max_id"]}'
                yield response.follow(url_subscriptions,
                                      callback=self.user_data_parse,
                                      cb_kwargs={'username': username,
                                                 'user_id': user_id})
            if len(re.findall('followers', response.url)) == 1:
                url_subscriptions = f'{self.url_subscribe}/{user_id}/followers/?count=12&' \
                                    f'max_id={j_subscribers["next_max_id"]}&search_surface=follow_list_page'
                yield response.follow(url_subscriptions,
                                      callback=self.user_data_parse,
                                      cb_kwargs={'username': username,
                                                 'user_id': user_id})

        for sub_user in j_subscribers['users']:
            who_is = ''
            if len(re.findall('following', response.url)) == 1:
                who_is = 'subscription'
            if len(re.findall('followers', response.url)) == 1:
                who_is = 'subscriber'
            user = username
            sub_name = sub_user['username']
            sub_id = sub_user['pk']
            sub_picture = sub_user['profile_pic_url']
            yield InstaparserItem(who_is=who_is, user=user, sub_name=sub_name, sub_id=sub_id, sub_picture=sub_picture)

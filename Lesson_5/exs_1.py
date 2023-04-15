# -*- coding: utf-8 -*-
import sqlite3

import requests
from lxml import html

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 '
                  'Safari/537.36 '
}

mail_news_lst = []
lenta_news_lst = []


def parse_lenta_main_news():
    r = requests.get(
        'https://www.leomax.ru/action/tovary_dlya_doma_i_dachi/',
        headers=headers, params=None)
    # print(r.text)
    root = html.fromstring(r.text)
    nwes = root.xpath("//div[contains(@class, 'good-item')]/div/@data-category")
    print(nwes)

parse_lenta_main_news()
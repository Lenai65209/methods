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
        'https://lenta.ru/',
        headers=headers, params=None)
    root = html.fromstring(r.text)
    big_nwes = root.xpath("//a[@class='card-big _topnews _news']")
    all_news = root.xpath("//a[@class='card-mini _topnews']")

    if big_nwes:
        big_nwes_url = "https://lenta.ru/" + big_nwes[0].xpath(
            "./@href")[0]
        big_nwes_text = big_nwes[0].xpath(
            "./div/h3/text()")[
            0].replace('\xa0', ' ')
        big_nwes_source = 'источник не указан'
        big_nwes_website = "https://lenta.ru/"
        big_nwes_time = big_nwes[0].xpath(
            "./div/time/text()")[0]
        big_nwes_tuple = (
            big_nwes_source, big_nwes_website, big_nwes_text, big_nwes_url,
            big_nwes_time)
        lenta_news_lst.append(big_nwes_tuple)
    for news in all_news:
        news_url = "https://lenta.ru/" + news.xpath(
            "./@href")[0]
        news_text = news.xpath(
            "./div[@class = 'card-mini__text']/span["
            "@class='card-mini__title']/text()")[
            0].replace('\xa0', ' ')
        news_source = 'источник не указан'
        nwes_website = "https://lenta.ru/"
        news_time = str(news.xpath(
            "./div[@class = 'card-mini__text']/div/time/text()")[0])
        news_tuple = (news_source, nwes_website, news_text, news_url, news_time)
        lenta_news_lst.append(news_tuple)


def parse_mail_main_news():
    r = requests.get(
        'https://news.mail.ru/',
        headers=headers, params=None)
    root = html.fromstring(r.text)
    all_news = root.xpath("//div[contains(@class,'daynews__item')]")
    for news in all_news:
        news_url = news.xpath(
            ".//span/a/@href")[0]
        news_text = news.xpath(
            ".//span[contains(@class,'photo__title photo__title_new "
            "photo__title_new_hidden js-topnews__notification')]/text()")[
            0].replace('\xa0', ' ')
        news_source = 'источник не указан'
        nwes_website = 'https://news.mail.ru/'
        news_time = 'дата публикации не указана'
        news_tuple = (news_source, nwes_website, news_text, news_url, news_time)
        mail_news_lst.append(news_tuple)


parse_lenta_main_news()
parse_mail_main_news()

conn = sqlite3.connect('database.db')
cur = conn.cursor()
# cur.execute("SQL-ЗАПРОС-ЗДЕСЬ;")
cur.execute("""CREATE TABLE IF NOT EXISTS vacancies(
   news_source TEXT,
   nwes_website TEXT,
   news_text TEXT,
   news_url TEXT,
   news_time TEXT);
""")
conn.commit()

for news in lenta_news_lst:
    cur.execute(f"INSERT INTO vacancies VALUES{news}")
conn.commit()
cur.executemany("INSERT INTO vacancies VALUES(?, ?, ?, ?, ?);", mail_news_lst)

cur.execute("SELECT * FROM vacancies;")
all_results = cur.fetchall()
for news in all_results:
    print(news, end='\n')

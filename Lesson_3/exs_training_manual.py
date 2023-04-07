# -*- coding: utf-8 -*-
from pprint import pprint

import requests
from bs4 import BeautifulSoup as bs

quotes_list = []
flag = True
j = 1
while flag:
    response = requests.get(f'https://quotes.toscrape.com/page/{j}/')
    soup = bs(response.content, 'html.parser')
    # print(soup)
    can_find = soup.find_all('div', attrs={'class': ['col-md-8']})
    can_find_str = can_find[1].text.strip()
    if 'No quotes found!' not in can_find_str:
        quotes = soup.find_all('div', attrs={'class': ['quote']})
        quote_dict = {}
        tegs = []
        for quote in quotes:
            title = quote.select_one('span[class*=text]').text.strip()
            author_lst = quote.select_one(
                'span[class*=text]').find_next_sibling(
                'span').text.split()
            del author_lst[0]
            del author_lst[len(author_lst) - 1]
            author = ' '.join(author_lst)
            tegs_lst = quote.select_one(
                'div[class*=tags]').find_all('a', attrs={'class': ['tag']})
            tegs = []
            for i in range(len(tegs_lst)):
                tegs.extend(tegs_lst[i].text.split())
            quote_dict = {
                'title': title,
                'author': author,
                'tegs': tegs,
            }
            quotes_list.append(quote_dict)
        j += 1
    else:
        # print(can_find[1].text.strip())
        flag = False

print('quotes_list')
pprint(quotes_list)
print('len(quotes_list)', len(quotes_list))
print(f'I went through {j-1} pages')

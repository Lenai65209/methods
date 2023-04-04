# -*- coding: utf-8 -*-
#  !!! Рботает только при полных данных (по з/п), наприер для вакансии "бухгалтер"
# import urllib.request

# import chardet
import pandas as pd
import requests
from lxml import html

url = 'https://arkhangelsk.hh.ru/'
# data = urllib.request.urlopen('https://arkhangelsk.hh.ru/')
# print(chardet.detect(data.read())['encoding'])
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 '
                  'Safari/537.36 '
}

text = input('Введите должность: ')
pages = int(input('Введите число просматриваемых страниц: '))
job_openings_lst = []
salary = []
salary_lst = []
salary_lst_new = []
salary_lst_min = []
salary_lst_max = []
vacancy_link_lst = []

for page in range(0, pages):
    request = requests.get(
        f'https://arkhangelsk.hh.ru/search/vacancy?text={text}&area=3&page={page}',
        headers=headers)

    root = html.fromstring(request.content)
    job_openings = root.xpath(
        "//a[contains(@class, 'serp-item__title')]/text()")
    job_openings_lst.extend(job_openings)
    salary = root.xpath("//span[contains(@class, "
                        "'bloko-header-section-3')]/text()")
    salary_lst.extend(salary)
    vacancy_link = root.xpath("//a[contains(@class, 'serp-item__title')]/@href")
    vacancy_link_lst.extend(vacancy_link)

for i in range(len(salary_lst)):
    if 'от' in salary_lst[i]:
        salary_lst_new.append('min ' + salary_lst[i + 1])
    if 'до' in salary_lst[i]:
        salary_lst_new.append('max ' + salary_lst[i + 1])
    if ' – ' in salary_lst[i]:
        salary_lst_new.append(salary_lst[i])
    if 'не' in salary_lst[i]:
        salary_lst_new.append('не')

for i in range(len(salary_lst_new)):
    if 'max' in salary_lst_new[i]:
        salary_lst_min.append('з/п не указана')
        salary_lst_max.append(salary_lst_new[i].split(" ")[1])
    if 'min' in salary_lst_new[i]:
        salary_lst_min.append(salary_lst_new[i].split(" ")[1])
        salary_lst_max.append('з/п не указана')
    if ' – ' in salary_lst_new[i]:
        salary_lst_min.append(salary_lst_new[i].split(" – ")[0])
        salary_lst_max.append(salary_lst_new[i].split(" – ")[1])
    if 'не' in salary_lst_new[i]:
        salary_lst_min.append('з/п не указана')
        salary_lst_max.append('з/п не указана')
# print(job_openings_lst)
# print(len(job_openings_lst))
# print('salary_lst_min', salary_lst_min)
# print(len(salary_lst_min))
# print('salary_lst_max', salary_lst_max)
# print(len(salary_lst_max))
# print(vacancy_link_lst)
# print(len(vacancy_link_lst))

s1 = pd.Series(job_openings_lst, name='job_openings_lst')
s2 = pd.Series(salary_lst_min, name='salary_lst_min')
s3 = pd.Series(salary_lst_max, name='salary_lst_max')
s4 = pd.Series(vacancy_link_lst, name='vacancy_link_lst')
percentile_list = pd.concat([s1, s2, s3, s4], axis=1)
pd.set_option('display.max_column', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_seq_items', None)
pd.set_option('display.max_colwidth', 500)
pd.set_option('expand_frame_repr', True)
print(percentile_list)
pd.reset_option('display.max_columns')

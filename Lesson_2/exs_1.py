# -*- coding: utf-8 -*-
# Работает с пропущенными данными, даже в случае, если зарплата не указана.
import pandas as pd
import requests
from lxml import html

text = input("Введите должность: ")
pages = int(input("Введите число просматриваемых страниц: "))
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 '
                  'Safari/537.36 '
}
job_openings_lst = []
salary_lst_min = []
salary_lst_max = []
vacancy_link_lst = []

for page in range(0, pages):
    r = requests.get(
        f'https://arkhangelsk.hh.ru/search/vacancy?text={text}&area=3&page={page}',
        headers=headers)

    root = html.fromstring(r.content)
    job_openings = root.xpath("//div[@class='serp-item']")
    for vacancy in job_openings:
        vacancy_name = vacancy.xpath(
            "./div/div/div/div[@class]/h3/span/a[contains(@class, "
            "'serp-item__title')]/text()")[0]
        job_openings_lst.append(vacancy_name)
        vacancy_link = vacancy.xpath("./div/div/div/div/h3/span/a/@href")[0]
        vacancy_link_lst.append(vacancy_link)
        vacancy_salary = vacancy.xpath(
            "./div/div/div/div/span[@class='bloko-header-section-3']/text()")
        if len(vacancy_salary) == 0:
            salary_min = '-'
            salary_max = '-'
            salary_lst_max.append(salary_max)
            salary_lst_min.append(salary_min)
        elif len(vacancy_salary) == 4:
            if 'от' in vacancy_salary[0]:
                salary_min = ''.join(vacancy_salary[1].split('\u202f')).replace(
                    ' ', '')
                salary_max = '-'
                salary_lst_max.append(salary_max)
                salary_lst_min.append(salary_min)
            if 'до' in vacancy_salary[0]:
                salary_max = ''.join(vacancy_salary[1].split('\u202f')).replace(
                    ' ', '')
                salary_min = '-'
                salary_lst_max.append(salary_max)
                salary_lst_min.append(salary_min)
        elif len(vacancy_salary) == 2:
            salary_min = ''.join(
                vacancy_salary[0].split('–')[0].split('\u202f')).replace(
                ' ', '')
            salary_max = ''.join(
                vacancy_salary[0].split('–')[1].split('\u202f')).replace(
                ' ', '')
            salary_lst_max.append(salary_max)
            salary_lst_min.append(salary_min)

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

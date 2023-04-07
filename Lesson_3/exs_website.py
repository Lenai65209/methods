# -*- coding: utf-8 -*-
from time import sleep

import pandas as pd

import requests
from bs4 import BeautifulSoup as bs

text = input("Введите должность: ")
pages = int(input("Введите число просматриваемых страниц: "))
my_salary = int(input("Введите минимальную зарплату (без пробелов): "))
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 '
                  'Safari/537.36 '
}
job_openings_lst = []
salary_lst_min = []
salary_lst_max = []
vacancy_link_lst = []
percentile_list = []

for page in range(0, pages):
    response = requests.get(
        f'https://arkhangelsk.hh.ru/search/vacancy?text={text}&area=3&page={page}',
        headers=headers)
    soup = bs(response.content, 'html.parser')
    new_vacancy = soup.find('div', attrs={'class': ['serp-item']})
    new_vacancy_mame = soup.find_all('a', attrs={'class': ['serp-item__title']})
    for i in range(len(new_vacancy_mame)):
        vacancy_mame = new_vacancy_mame[i].text.strip()
        vacancy_link = new_vacancy_mame[i]['href']
        vacancy_salary_span = new_vacancy_mame[
            i].parent.parent.find_next_sibling(
            'span')
        if vacancy_salary_span:
            vacancy_salary = vacancy_salary_span.text.strip().split()
        else:
            salary_min = 0
            salary_max = 0
        if len(vacancy_salary) == 0:
            salary_min = 0
            salary_max = 0
        if len(vacancy_salary) == 4:
            if 'от' in vacancy_salary[0]:
                del vacancy_salary[0]
                vacancy_salary.pop()
                salary_min = int(''.join(vacancy_salary).strip())
                salary_max = 0
            if 'до' in vacancy_salary[0]:
                del vacancy_salary[0]
                vacancy_salary.pop()
                salary_max = int(''.join(vacancy_salary))
                salary_min = 0
        if len(vacancy_salary) == 6:
            vacancy_salary.pop()
            salary_min = int(''.join(vacancy_salary[0] + vacancy_salary[1]))
            salary_max = int(''.join(vacancy_salary[3] + vacancy_salary[4]))
        if vacancy_link not in vacancy_link_lst:

            if (salary_min >= my_salary) or my_salary <= salary_max:
                vacancy_link_lst.append(vacancy_link)
                job_openings_lst.append(vacancy_mame)
                if salary_max:
                    salary_lst_max.append(salary_max)
                else:
                    salary_lst_max.append('-')
                if salary_min:
                    salary_lst_min.append(salary_min)
                else:
                    salary_lst_min.append("-")
    sleep(2)

if job_openings_lst:
    s1 = pd.Series(job_openings_lst, name='job_openings_lst')
else:
    s1 = pd.Series(job_openings_lst, name='job_openings_lst', dtype='float64')
if salary_lst_min:
    s2 = pd.Series(salary_lst_min, name='salary_lst_min')
else:
    s2 = pd.Series(salary_lst_min, name='salary_lst_min', dtype='float64')
if salary_lst_max:
    s3 = pd.Series(salary_lst_max, name='salary_lst_max')
else:
    s3 = pd.Series(salary_lst_max, name='salary_lst_max', dtype='float64')
if vacancy_link_lst:
    s4 = pd.Series(vacancy_link_lst, name='vacancy_link_lst')
else:
    s4 = pd.Series(vacancy_link_lst, name='vacancy_link_lst', dtype='float64')
percentile_list = pd.concat([s1, s2, s3, s4], axis=1)
pd.set_option('display.max_column', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_seq_items', None)
pd.set_option('display.max_colwidth', 500)
pd.set_option('expand_frame_repr', True)
if percentile_list.empty:
    print("Нет подходящих вариантов )")
else:
    print(percentile_list)
pd.reset_option('display.max_columns')

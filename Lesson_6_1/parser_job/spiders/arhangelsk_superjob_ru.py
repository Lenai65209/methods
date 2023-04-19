import re

import scrapy
from scrapy.http import HtmlResponse

from ..items import ParserJobItem


class ArhangelskSuperjobRuSpider(scrapy.Spider):
    name = "arhangelsk_superjob_ru"
    allowed_domains = ["arhangelsk.superjob.ru"]
    start_urls = ["https://arhangelsk.superjob.ru/vakansii/buhgalter.html"]

    def parse(self, response: HtmlResponse):
        jobs = response.xpath(
            "//div[contains(@class, 'f-test-search-result-item')]")
        url_job_list = []
        for job_openings in jobs:
            url_job = ''.join(
                job_openings.xpath(
                    ".//span[contains(@class, '_1c5Bu _1Yga1 _1QFf5 _2MAQA _1m76X _3UZoC _3zdq9 _1_71a')]/a/@href").getall())
            url_job = 'https://arhangelsk.superjob.ru' + url_job.strip()

            if url_job:
                if url_job not in url_job_list:
                    url_job_list.append(url_job)
                    yield response.follow(url_job, callback=self.parse_jobs)

    def parse_jobs(self, response: HtmlResponse):
        j_url = response.url
        j_title = response.css('h1::text').get()
        salary = response.xpath(
            ".//span[contains(@class, '_2eYAG _1m76X _3UZoC _3iH_l')]/text()").getall()

        if 'от' == salary[0].strip():
            regex = re.compile(r'\xa0')
            salary_min = regex.sub(" ", salary[2]).strip()
            salary_max = 'не определена'
        elif 'до' == salary[0].strip():
            regex = re.compile(r'\xa0')
            salary_max = regex.sub(" ", salary[2]).strip()
            salary_min = 'не определена'
        elif len(salary) == 1:
            salary_min = salary[0]
            salary_max = salary[0]
        elif len(salary) == 3:
            regex = re.compile(r'\xa0')
            salary_min = regex.sub(" ", salary[0]).strip()
            salary_max = 'не определена'
        elif not salary:
            salary_min = ''
            salary_max = ''
        else:
            regex = re.compile(r'\xa0')
            salary_min = regex.sub(" ", salary[0]).strip() + ' ' + salary[
                len(salary) - 1]
            salary_max = regex.sub(" ", salary[4]).strip()
            salary_max = salary_max + ' ' + salary[len(salary) - 1]
        if not salary:
            salary_min = ''
            salary_max = ''

        if salary:
            yield ParserJobItem(
                url=j_url,
                title=j_title,
                salary_min=salary_min,
                salary_max=salary_max,
            )

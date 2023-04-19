import re

import scrapy
from scrapy.http import HtmlResponse

from ..items import ParserJobItem


class ArkhangelskHhRuSpider(scrapy.Spider):
    name = "arkhangelsk_hh_ru"
    allowed_domains = ["arkhangelsk.hh.ru"]
    # start_urls = ["http://arkhangelsk.hh.ru/search/vacancy?text=Бухгалтер+на+дому&from=suggest_post&salary=&area=14&ored_clusters=true"]
    start_urls = [
        'https://arkhangelsk.hh.ru/search/vacancy?text=%D0%91%D1%83%D1%85%D0%B3%D0%B0%D0%BB%D1%82%D0%B5%D1%80&page=1']

    def parse(self, response: HtmlResponse):
        jobs = response.xpath(
            "//div[contains(@class, 'serp-item')]")
        url_job_list = []
        for job_openings in jobs:
            url_job = ''.join(
                job_openings.xpath(
                    ".//h3[contains(@class, 'bloko-header-section-3')]/span/a[contains(@class, 'serp-item__title')]/@href").getall())
            url_job = url_job.strip()

            if url_job:
                if url_job not in url_job_list:
                    url_job_list.append(url_job)
                    yield response.follow(url_job, callback=self.parse_jobs)

    def parse_jobs(self, response: HtmlResponse):
        j_url = response.url
        j_title = response.css('h1::text').get()
        salary = response.xpath(
            ".//div/span[contains(@class, 'bloko-header-section-2 bloko-header-section-2_lite')]/text()").getall()

        if 'от' == salary[0].strip() and 'до' != salary[2].strip():
            regex = re.compile(r'\xa0')
            salary_min = regex.sub(" ", salary[1]).strip()
            salary_min = salary_min + ' ' + salary[len(salary) - 1]
            salary_max = 'не определена'
        elif 'до' == salary[0].strip() and 'от' != salary[2].strip():
            regex = re.compile(r'\xa0')
            salary_max = regex.sub(" ", salary[1]).strip()
            salary_max = salary_max + ' ' + salary[len(salary) - 1]
            salary_min = 'не определена'
        elif 'до' == salary[2].strip():
            regex = re.compile(r'\xa0')
            salary_min = regex.sub(" ", salary[1]).strip()
            salary_min = salary_min + ' ' + salary[len(salary) - 1]
            salary_max = regex.sub(" ", salary[3]).strip()
            salary_max = salary_max + ' ' + salary[len(salary) - 1]

        else:
            salary_min = 'не указана'
            salary_max = 'не указана'

        yield ParserJobItem(
            url=j_url,
            title=j_title,
            salary_min=salary_min,
            salary_max=salary_max,
        )

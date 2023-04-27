import scrapy
from scrapy.http import HtmlResponse

from ...variables import LOGIN, PASSWORD


class GbRuSpider(scrapy.Spider):
    name = "gb_ru"
    allowed_domains = ["gb.ru"]
    start_urls = ["https://gb.ru/login"]
    list_login_link = 'https://gb.ru/login'
    list_login = LOGIN
    list_pwd = PASSWORD

    def parse(self, response: HtmlResponse):
        csrf = 'efh5q7elkEYG3nvo6d3NvU5//fbIK5TFo4D+JhlnH1PrDteRcicUaIhPUHjh/kv7fMD6VA8lhxln2i9kENsh1Q=='
        yield scrapy.FormRequest(
                    self.list_login_link,
                    method='POST',
                    callback=self.after_login,
                    formdata={'user_email': self.list_login, 'user_password': self.list_pwd},
                    headers={'csrf-token': csrf}
                )

    def after_login(self, response: HtmlResponse):
        """Переход намою страницу."""
        # print(response)
        yield response.follow('https://gb.ru/users/7355422',
                              callback=self.see_my)

    def see_my(self, response: HtmlResponse):
        title = response.xpath('//title/text()').get()
        print('**********************')
        print('title', title)
        # print(response)

print()

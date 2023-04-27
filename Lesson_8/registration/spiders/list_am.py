import scrapy
from scrapy.http import HtmlResponse
from scrapy import FormRequest
from ..items import RegistrationItem
from ...variables import LOGIN_LIST, PASSWORD_LIST


class ListAmSpider(scrapy.Spider):
    name = "list_am"
    allowed_domains = ["list.am"]
    start_urls = ["https://www.list.am/login"]
    list_login_link = 'https://www.list.am/login'
    list_login = LOGIN_LIST
    list_pwd = PASSWORD_LIST

    def parse(self, response: HtmlResponse):
        print('Был в parse')
        yield scrapy.FormRequest(
            self.list_login_link,
            method='POST',
            callback=self.after_login,
            formdata={'_idphone_number_or_email': self.list_login, '_idpassword': self.list_pwd},
        )

    def after_login(self, response: HtmlResponse):
        """Переход намою страницу."""
        print('Был в after_login')
        yield response.follow('https://www.list.am/user/2663302',
                              callback=self.see_my)

    def see_my(self, response: HtmlResponse):
        # Not_found = response.xpath('.//div[@class="notfound"]/text()').get()
        name = response.xpath("//a[@class='n']/div/text()").get()
        text =  response.xpath("//div[@class='notfound']/text()").get()
        print('**********************')
        print('Name: ', name)
        print('Text: ', text)
        print(response)
        yield response.follow('https://www.list.am/ru/',
                              callback=self.see_apartment_rentals)

    def see_apartment_rentals(self, response: HtmlResponse):
        print(response)
        categories = response.xpath("//div[@class='s']/div[@class='c c1']")[0]
        category = response.xpath("//div[@class='s']/a/text()").get()
        category_lst = categories.xpath(".//a")
        # print(categories)
        print('category ', category)
        # print('category_lst', category_lst)
        url_el_list = []
        for el in category_lst:
            url_el = 'https://www.list.am' + ''.join(
                el.xpath(
                    "@href").getall())
            # print('url_el', url_el)
            if url_el:
                if url_el not in url_el_list:
                    url_el_list.append(url_el)
                    yield response.follow(url_el, callback=self.parse_el)

    def parse_el(self, response: HtmlResponse):
        print("Я в элементе")
        el_url = response.url
        print('el_url ', el_url)
        el_title = response.css('h1::text').get()
        print('el_title ', el_title)
        el_price = response.xpath("//div[contains(@class, 'price')]/span/text()").getall()
        if el_price:
            el_price = el_price[0]
            print('el_price', el_price)
        else:
            el_price = 'Не определено'
        el_photos = response.xpath("//div[@class='p']/div/img/@src").get()
        el_photos = 'https:' + el_photos
        print('el_photos', el_photos)
        # el_photos_new = []
        # for photo in el_photos:
        #     el_photos_new.append('https:' + photo)
        # print("g_photos_new", el_photos_new)
        # for apartment in apartment_rentals:
        yield RegistrationItem(
            title=el_title,
            url=el_url,
            price=el_price,
            photos=el_photos,
        )

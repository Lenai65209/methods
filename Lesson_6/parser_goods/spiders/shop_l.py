import re

import scrapy
from scrapy.http import HtmlResponse

from ..items import ParserGoodsItem

goods_lst = []


class ShopLSpider(scrapy.Spider):
    name = "shop_l"
    allowed_domains = ["leomax.ru"]
    start_urls = [
        "https://www.leomax.ru/products/tovary_dlya_kuhni/?PROPS%5B869%5D%5B0%5D=2757133"]

    def parse(self, response: HtmlResponse):
        goods = response.xpath(
            "//div[contains(@class, 'good-item')]")
        for product in goods:
            url_product = 'https://www.leomax.ru' + ''.join(
                product.xpath(".//figure/div/a/@href").get()).strip()
            if url_product:
                yield response.follow(url_product, callback=self.parse_goods)

    def parse_goods(self, response: HtmlResponse):
        g_url = response.url
        g_title = response.css('h1::text').getall()
        g_title = str(g_title[0])
        g_price_incl_tax = response.xpath(
            "//p[contains(@class, 'l-price')]/meta/@content").getall()
        g_price_incl_tax = ' '.join(g_price_incl_tax).strip()
        g_price_excl_tax = response.xpath(
            "//p[contains(@class, 'l-price')]/span[contains(@class, 'price price-old')]/text()").getall()
        g_price_excl_tax = g_price_excl_tax[0]
        g_product_description = response.xpath(
            "//div[contains(@class, 'longContent')]/p/text()").getall()
        g_product_description_1 = str(' '.join(g_product_description).strip())
        regex = re.compile(r'[\n\r\t]')
        g_product_description = regex.sub(" ", g_product_description_1).strip()
        g_photos = response.xpath(
            "//div[contains(@class, 'own-carousel')]//li//img/@src").getall()

        # //div[contains(@class, 'own-carousel')]//li//img/@src
        g_photos_new = []
        for photo in g_photos:
            g_photos_new.append('https://www.leomax.ru' + photo)
        print("g_photos_new", g_photos_new)

        yield ParserGoodsItem(
            url=g_url,
            product_description=g_product_description,
            title=g_title,
            price_excl_tax=g_price_excl_tax,
            price_incl_tax=g_price_incl_tax,
            photos=g_photos_new,
        )

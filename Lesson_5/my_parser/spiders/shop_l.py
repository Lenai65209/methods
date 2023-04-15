import re

import scrapy
from scrapy.http import HtmlResponse

from ..items import MyParserItem

goods_lst = []


class ShopLSpider(scrapy.Spider):
    name = "shop_l"
    allowed_domains = ["leomax.ru"]
    start_urls = ["https://www.leomax.ru/action/tovary_dlya_doma_i_dachi/"]

    def parse(self, response: HtmlResponse):
        ##########################
        next_pager = "https://www.leomax.ru/" + response.xpath(
            "//li[contains(@class, 'btn-next-page')]/a/@href").get()
        # print(
        #     '\nnext_pager    pppppppppppppp    next_pager    pppppppppppppp next_pager   pppppppppp\n')
        # print("Это страница")
        # print(f'{next_pager}')
        # print(
        #     '\next_pager    pppppppppppppp    next_pager    pppppppppppppp next_pager   ppppppppp\n')
        if next_pager:
            yield response.follow(next_pager, callback=self.parse)

        ##########################
        goods = response.xpath(
            "//div[contains(@class, 'good-item')]")
        # print('\n#########################################\n')
        # print('Товары на странице')
        # print(goods)
        # print('\n#########################################\n')

        for product in goods:
            # url_product = ''.join(product.xpath(
            #     './/div[contains(@class,"image_container")]/a/@href').getall()).strip()
            url_product = 'https://www.leomax.ru' + ''.join(
                product.xpath(".//figure/div/a/@href").get()).strip()
            # print(
            #     '\nbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb\n')
            # print("Ссылка на товар")
            # print(url_product)
            # print(
            #     '\nbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb\n')
            if url_product:
                yield response.follow(url_product, callback=self.parse_goods)

        # for product in goods:
        #
        #     yield {
        #         'data-category': ''.join(
        #             product.xpath(".//div/@data-category").getall()).strip(),
        #         'name': ''.join(product.xpath(".//img/@alt").get()).strip(),
        #         'picture': 'https://www.leomax.ru' + ''.join(
        #             product.xpath(".//img/@data-src").get()).strip(),
        #         'linc': 'https://www.leomax.ru' + ''.join(
        #             product.xpath(".//figure/div/a/@href").get()).strip(),
        #         'sale_price': ''.join(product.xpath(
        #             ".//p[contains(@class, 'l-price')]/span/text()").get()).strip(),
        #     }

    def parse_goods(self, response: HtmlResponse):
        # print(
        #     '\nxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx\n')
        # print("Это товар")
        g_url = response.url
        # print(g_url)
        # print(
        #     '\nzxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx\n')
        g_title = response.css('h1::text').getall()
        g_title = str(g_title[0])
        # print('g_title ', g_title)
        g_price_incl_tax = response.xpath(
            "//p[contains(@class, 'l-price')]/meta/@content").getall()
        g_price_incl_tax = ' '.join(g_price_incl_tax).strip()
        # print("g_price_excl_tax ", g_price_excl_tax)
        # g_price_excl_tax = response.xpath("//p[contains(@class, 'l-price')]/span[contains(@class, 'price price-new')]").get()
        # print("g_price_excl_tax ", g_price_incl_tax)
        g_price_excl_tax = response.xpath(
            "//p[contains(@class, 'l-price')]/span[contains(@class, 'price price-old')]/text()").getall()
        g_price_excl_tax = g_price_excl_tax[0]
        # print("g_price_excl_tax ", g_price_excl_tax)
        g_product_description = response.xpath(
            "//div[contains(@class, 'longContent')]/p/text()").getall()
        g_product_description_1 = str(' '.join(g_product_description).strip())
        # g_product_description.maketrans(" \r\n", "   ")
        regex = re.compile(r'[\n\r\t]')
        g_product_description = regex.sub(" ", g_product_description_1).strip()

        # print("about_product ", g_product_description)

        yield MyParserItem(
            url=g_url,
            product_description=g_product_description,
            title=g_title,
            price_excl_tax=g_price_excl_tax,
            price_incl_tax=g_price_incl_tax,
        )

import scrapy
from scrapy.http import HtmlResponse

from ..items import MyParserItem


class BooksSpider(scrapy.Spider):
    name = "books"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com/catalogue/category/books_1/", ]

    # 'http://books.toscrape.com/catalogue/category/books/travel_2/index.html', ]

    def parse(self, response: HtmlResponse):
        next_pager = self.start_urls[0] + response.xpath(
            "//li[contains(@class, 'next')]/a/@href").get()
        # print(
        #     '\nnext_pager    pppppppppppppp    next_pager    pppppppppppppp next_pager   pppppppppp\n')
        # print("Это страница")
        # print(next_pager)
        # print(
        #     '\next_pager    pppppppppppppp    next_pager    pppppppppppppp next_pager   ppppppppp\n')
        if next_pager:
            yield response.follow(next_pager, callback=self.parse)

        books = response.xpath("//ol[@class ='row'] / li")
        # print('\n#########################################\n')
        # print("Книги на странице")
        # print(books)
        # print('\n#########################################\n')

        for book in books:
            url_book = ''.join(book.xpath(
                './/div[contains(@class,"image_container")]/a/@href').getall()).strip()
            url_book = 'https://books.toscrape.com/catalogue/' + url_book[6:]
            # print(
            #     '\nbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb\n')
            # print("Ссылка на книгу")
            # print(url_book)
            # print(
            #     '\nbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb\n')
            if url_book:
                yield response.follow(url_book, callback=self.parse_book)

            # yield {
            # Отсюда была запмсь в books.csv и books.json
            #     'image': ''.join(book.xpath(
            #         ".//div[@class='image_container']/a/img/@src").getall()).strip(),
            #     'title': ''.join(book.xpath(".//h3/a/@title").getall()).strip(),
            #     'price': ''.join(book.xpath(
            #         ".//p[@class='price_color']/text()").getall()).strip(),
            #     'instock': ''.join(book.xpath(
            #         ".//p[contains(@class, 'instock')]/text()").getall()).strip(),
            #     'Product_Type': ''.join(book.xpath(
            #         "//div[contains(@class, 'page-header action')]/h1/text()").getall()).strip(),
            #     'url_book': "https://books.toscrape.com/"+''.join(book.xpath('.//div[contains(@class,"image_container")]/a/@href').getall()).strip(),
            # }

    def parse_book(self, response: HtmlResponse):
        # print('\nxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx\n')
        # print("Это книга")
        # Title, Price, In stock, Product Description, UPC, Product Type,
        # Price (excl. tax), Price (incl. tax), Tax, Availability, Number of reviews.
        b_url = str(response.url)
        # print(url)
        b_title = response.css('h1::text').getall()
        b_title = str(b_title[0])
        # print(response.xpath("//div[contains(@class, 'row')]/div[contains("
        #                      "@class, 'col-sm-6 product_main')]/h1/text("
        #                      ")").get())
        b_price = response.xpath("//div[contains(@class, 'row')]/div[contains("
                               "@class, 'col-sm-6 product_main')]/p[contains("
                               "@class, 'price_color')]/text()").get()
        b_price=str(b_price)
        b_in_stock = response.xpath("//div[contains(@class, 'row')]/div[contains("
                                  "@class, 'col-sm-6 product_main')]/p[contains("
                                  "@class, 'instock availability')]/text()").getall()
        b_in_stock = str(b_in_stock[1].strip())
        b_product_description = str(response.xpath("//article/p/text()").get())
        # print(product_description)
        b_upc = response.xpath('//tr[th[text()="UPC"]]/child::td').getall()
        b_upc = str(b_upc[0][4:-5])
        # print('upc', upc)
        b_product_type = response.xpath(
            '//tr[th[text()="Product Type"]]/child::td').getall()
        b_product_type = str(b_product_type[0][4:-5])
        # print('product_type', product_type)
        b_price_excl_tax = response.xpath(
            '//tr[th[text()="Price (excl. tax)"]]/child::td').getall()
        b_price_excl_tax = str(b_price_excl_tax[0][4:-5])
        # print('price_excl_tax', price_excl_tax)
        b_price_incl_tax = response.xpath(
            '//tr[th[text()="Price (incl. tax)"]]/child::td').getall()
        b_price_incl_tax = str(b_price_incl_tax[0][4:-5])
        # print('price_incl_tax', price_incl_tax)
        b_tax = response.xpath(
            '//tr[th[text()="Tax"]]/child::td').getall()
        b_tax = str(b_tax[0][4:-5])
        # print('tax', tax)
        b_availability = response.xpath(
            '//tr[th[text()="Availability"]]/child::td').getall()
        b_availability = str(b_availability[0][4:-5])
        # print('availability', availability)
        b_number_of_reviews = response.xpath(
            '//tr[th[text()="Number of reviews"]]/child::td').getall()
        b_number_of_reviews = str(b_number_of_reviews[0][4:-5])
        # print('number_of_reviews', number_of_reviews)
        # print('\nzxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx\n')

        yield MyParserItem(
            url=b_url,
            title=b_title,
            price=b_price,
            in_stock=b_in_stock,
            product_description=b_product_description,
            upc=b_upc,
            product_type=b_product_type,
            price_excl_tax=b_price_excl_tax,
            price_incl_tax=b_price_incl_tax,
            tax=b_tax,
            availability=b_availability,
            number_of_reviews=b_number_of_reviews,
        )

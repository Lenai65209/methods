# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ParserGoodsItem(scrapy.Item):
    # define the fields for your item here like:
    # Title, Price, In stock, Product Description, UPC, Product Type,
    # Price (excl. tax), Price (incl. tax), Tax, Availability, Number of reviews.

    url = scrapy.Field()
    title = scrapy.Field()
    price = scrapy.Field()
    in_stock = scrapy.Field()
    product_description = scrapy.Field()
    upc = scrapy.Field()
    product_type = scrapy.Field()
    price_excl_tax = scrapy.Field()
    price_incl_tax = scrapy.Field()
    tax = scrapy.Field()
    availability = scrapy.Field()
    number_of_reviews = scrapy.Field()
    photos = scrapy.Field()
    # _id = scrapy.Field()



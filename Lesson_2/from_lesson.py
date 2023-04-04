import requests
from lxml import html

r = requests.get('https://books.toscrape.com')

root = html.fromstring(r.content)
articles = root.xpath("//article")
article_dict = {}

for article in articles:
    title = article.xpath(".//h3/a/@title")[0]
    image = 'https://books.toscrape.com/' + article.xpath(".//div[contains("
                                                          "@class, "
                                                          "'image_container"
                                                          "')]/a/img/@src")[0]
    price = article.xpath(".//p[contains(@class, 'price_color')]/text()")[0]
    instock = article.xpath(".//p[contains(@class, 'instock "
                            "availability')]/text()")[1]
    # print(title, image, price, instock)[0]
    print(title, image, price, instock.strip(), end='\n')

    article_dict[title] = {
        'image': image,
        'price': price,
        'instock': instock.strip()
    }
print(article_dict)

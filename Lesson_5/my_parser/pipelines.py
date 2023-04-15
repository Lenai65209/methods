# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
# from itemadapter import ItemAdapter
# from pymongo import MongoClient
import pathlib
import sqlite3
import sys

from scrapy.utils.serialize import ScrapyJSONEncoder

script_dir = pathlib.Path(sys.argv[0]).parent
db_file = script_dir / 'database.db'
conn = sqlite3.connect(db_file)


class MyParserPipeline:

    def __init__(self):
        # client = MongoClient('127.0.0.1:27017')
        # self.mongo_db = client.parser_xxx
        self.conn = sqlite3.connect(db_file)
        self.encoder = ScrapyJSONEncoder()

    def process_item(self, item, spider):
        # collections = self.mongo_db[spider.name]
        # collections.insert_one(item)
        # print('\n#########################################\n')
        # print("Книги на странице")
        # # print(item)
        # print('\n#########################################\n')
        # print(spider)
        # print('\n#########################################\n')
        # res = tuple(item.values())
        if spider.name == 'books':
            # res_lst = []
            # print('___________________________________________________')
            # print('Я нашел книгу')
            # data = self.encoder.encode(item)
            # res = tuple(data.values())
            res = tuple(item.values())
            # print(res)
            # print(f"{res}")
            # print(len(res))
            # res_lst.append(res)
            # print(res_lst)
            # print('___________________________________________________')
            cur = self.conn.cursor()
            cur.execute("""CREATE TABLE IF NOT EXISTS books(
                availability TEXT,
                in_stock TEXT,
                number_of_reviews TEXT,
                price TEXT,
                price_excl_tax TEXT,
                price_incl_tax TEXT,
                product_description TEXT,
                product_type TEXT,
                tax TEXT,
                title TEXT,
                upc TEXT,
                url TEXT);
            """)
            self.conn.commit()
            cur.execute(f"INSERT INTO books VALUES{res}")
            # data = self.encoder.encode(item)
            # if data:
            #     self.conn.execute('INSERT INTO books VALUES (?)', (data))
            self.conn.commit()
        return item

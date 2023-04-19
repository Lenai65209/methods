# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
# from itemadapter import ItemAdapter
import pathlib
import sqlite3
import sys

from scrapy.utils.serialize import ScrapyJSONEncoder

script_dir = pathlib.Path(sys.argv[0]).parent
db_file = script_dir / 'database.db'
conn = sqlite3.connect(db_file)


class ParserJobPipeline:

    def __init__(self):
        # client = MongoClient('127.0.0.1:27017')
        # self.mongo_db = client.parser_xxx
        self.conn = sqlite3.connect(db_file)
        self.encoder = ScrapyJSONEncoder()

    def process_item(self, item, spider):
        # print('___________________________________________________')
        # print('spider.name', spider.name)
        # print('___________________________________________________')
        # arkhangelsk_hh_ru
        if spider.name == 'arkhangelsk_hh_ru':
            res = tuple(item.values())
            cur = self.conn.cursor()
            cur.execute("""CREATE TABLE IF NOT EXISTS jobs(
                salary_max TEXT,
                salary_min TEXT,
                title TEXT,
                url TEXT);
            """)
            self.conn.commit()
            cur.execute(f"INSERT INTO jobs VALUES{res}")
            self.conn.commit()
            return item

        if spider.name == 'arhangelsk_superjob_ru':
            res = tuple(item.values())
            print('res', res)
            cur = self.conn.cursor()
            #  cur.execute("""CREATE TABLE IF NOT EXISTS jobs(
            cur.execute("""CREATE TABLE IF NOT EXISTS superjob(
                salary_max TEXT,
                salary_min TEXT,
                title TEXT,
                url TEXT);
            """)
            self.conn.commit()
            # cur.execute(f"INSERT INTO jobs VALUES{res}")
            cur.execute(f"INSERT INTO superjob VALUES{res}")
            self.conn.commit()
            return item

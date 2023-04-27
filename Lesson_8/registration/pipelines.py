# -*- coding: utf-8 -*-
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline
from scrapy import Request
import pathlib
import sqlite3
import sys

from scrapy.utils.serialize import ScrapyJSONEncoder

script_dir = pathlib.Path(sys.argv[0]).parent
db_file = script_dir / 'database.db'
conn = sqlite3.connect(db_file)


class RegistrationPipeline:

    def __init__(self):
        self.conn = sqlite3.connect(db_file)
        # self.encoder = ScrapyJSONEncoder()

    def process_item(self, item, spider):
        print('___________________________________________________')
        print('item', item)
        # print(item)
        print('___________________________________________________')
        # list_am
        if spider.name == 'list_am':

            link_photo = item['photos'][0]['url']
            item['photos'] = link_photo
            res = tuple(item.values())
            print('Хочу записать ', res)
            cur = self.conn.cursor()
            cur.execute("""CREATE TABLE IF NOT EXISTS elem(
                        title TEXT,
                        url TEXT,
                        price TEXT,
                        photos TEXT)
                    """)
            self.conn.commit()
            cur.execute(f"INSERT INTO elem VALUES{res}")
            self.conn.commit()
            return item


class ListPhotosPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        print("gckgjgzgdx,jhv.kljcgkhgxhgxnmgxhgkxkhgxjgdx")
        print(item)
        print("gckgjgzgdx,jhv.kljcgkhgxhgxnmgxhgkxkhgxjgdx")
        if item['photos']:
            print("item['photos']", item['photos'])
            print("gckgjgzgdx,jhv.kljcgkhgxhgxnmgxhgkxkhgxjgdx")
            try:
                yield Request(item['photos'])
            except Exception as e:
                print(e)

    def item_completed(self, results, item, info):
        item['photos'] = [itm[1] for itm in results if itm[0]]
        return item
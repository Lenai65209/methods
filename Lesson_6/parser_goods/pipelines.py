from pymongo import MongoClient
from scrapy import Request
from scrapy.pipelines.images import ImagesPipeline


class ParserGoodsPipeline:

    def __init__(self):
        client = MongoClient('127.0.0.1:27017')
        self.mongo_db = client.parser_xxx
        # self.conn = sqlite3.connect(db_file)
        # self.encoder = ScrapyJSONEncoder()

    def process_item(self, item, spider):
        return item


class LeomaxPhotosPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        print("gckgjgzgdx,jhv.kljcgkhgxhgxnmgxhgkxkhgxjgdx")
        print(item)
        print("gckgjgzgdx,jhv.kljcgkhgxhgxnmgxhgkxkhgxjgdx")
        if item['photos']:
            for img in item['photos']:
                try:
                    yield Request(img)
                except Exception as e:
                    print(e)

    def item_completed(self, results, item, info):
        item['photos'] = [itm[1] for itm in results if itm[0]]
        return item

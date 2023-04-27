from twisted.internet import reactor

from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings

from registration.spiders.list_am import ListAmSpider

if __name__ == '__maine__':
    configure_logging()
    settings = get_project_settings()

    runner = CrawlerRunner(settings)
    runner.crawl(ListAmSpider)

    reactor.run()

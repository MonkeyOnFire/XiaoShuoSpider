# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class QdypItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    bid = scrapy.Field()
    bName = scrapy.Field()
    bAuth = scrapy.Field()
    desc = scrapy.Field()
    cat = scrapy.Field()
    catId = scrapy.Field()
    cnt = scrapy.Field()
    rankCnt = scrapy.Field()
    rankNum = scrapy.Field()
    subCat = scrapy.Field()
    subCatId = scrapy.Field()
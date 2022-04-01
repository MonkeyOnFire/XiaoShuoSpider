# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Item, Field

class YsbookstoreItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class BookItem(Item):
    bookId = Field()
    status = Field()
    tags = Field()
    score = Field()
    scorerCount = Field()
    title = Field()
    author = Field()
    cover = Field()
    countWord = Field()
    updateAt = Field()
    caseId = Field()
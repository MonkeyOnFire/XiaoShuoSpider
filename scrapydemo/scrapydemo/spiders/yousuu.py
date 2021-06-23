import scrapy
from scrapy import Spider, Request
import json
from scrapydemo.items import bookItem, bookSourceItem
import logging


class YousuuSpider(scrapy.Spider):
    name = 'yousuu'
    allowed_domains = ['www.yousuu.com']
    book_store_url = 'https://www.yousuu.com/api/bookStore/books?page={page}'
    book_info_url = 'https://www.yousuu.com/api/book/{book_id}'
    #book_list_url = ''
    # start_page = 21
    # end_page = 100
    start_page = 1
    end_page = 12100

    def start_requests(self):
        for i in range(self.start_page, self.end_page + 1):
            logging.info('正在爬取书库列表第{}页'.format(i))
            yield Request(self.book_store_url.format(page=str(i)), callback=self.parse_book_store)

    def parse_book_store(self, response):

        book_store = json.loads(response.text)['data']['books']
        for book in book_store:
            book_id = book['bookId']
            logging.info('正在爬取id={}的书'.format(book_id))
            yield Request(self.book_info_url.format(book_id=book_id), callback=self.parse_book_info)

    def parse_book_info(self, response):

        book_info = json.loads(response.text)['data']['bookInfo']
        bookSources = json.loads(response.text)['data']['bookSource']
        book_item = bookItem()

        for book_atr in book_info:
            if book_atr in ['_id', 'tags', 'shielded', 'scoreDetail', 'recom_ignore', '__v', 'classInfo', 'countWord']:
                if book_atr == '_id':
                    book_item['id'] = book_info['_id']
                elif book_atr == 'tags':
                    book_item['tags'] = '|'.join(book_info['tags'])
                elif book_atr == 'shielded':
                    if book_info['shielded']:
                        book_item['shielded'] = 1
                    else:
                        book_item['shielded'] = 0
                elif book_atr == 'scoreDetail':
                    book_item['scoreDetail1'] = book_info['scoreDetail'][0]
                    book_item['scoreDetail2'] = book_info['scoreDetail'][1]
                    book_item['scoreDetail3'] = book_info['scoreDetail'][2]
                    book_item['scoreDetail4'] = book_info['scoreDetail'][3]
                    book_item['scoreDetail5'] = book_info['scoreDetail'][4]
                elif book_atr == 'recom_ignore':
                    if book_info['recom_ignore']:
                        book_item['recom_ignore'] = 1
                    else:
                        book_item['recom_ignore'] = 0
                elif book_atr == '__v':
                    book_item['v'] = book_info['__v']
                elif book_atr == 'countWord':
                    if None == book_info['countWord']:
                        book_item['countWord'] = 0
                    else:
                        book_item['countWord'] = book_info['countWord']
                elif book_atr == 'classInfo':
                    book_item['classInfo'] = 'meaningless'
                    try:
                        book_item['classId'] = book_info['classInfo']['classId']
                        book_item['className'] = book_info['classInfo']['className']
                        book_item['channel'] = book_info['classInfo']['channel']
                    except TypeError:
                        book_item['classId'] = 0
                        book_item['className'] = "NONE"
                        book_item['channel'] = "NONE"
            else:
                book_item[book_atr] = book_info[book_atr]
        # print(book_item)
        if not book_info.get('cover'):
            book_item['cover'] = ''
            
        yield book_item
        # print('--------------------------------------------------')
        for bookSource in bookSources:
            bookSource_Item = bookSourceItem()
            for bookSourceInfo in bookSource:
                bookSource_Item[bookSourceInfo] = bookSource[bookSourceInfo]
            # print(bookSource_Item)
            yield bookSource_Item

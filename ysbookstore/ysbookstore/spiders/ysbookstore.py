import scrapy
from scrapy import Request
import json
from ysbookstore.items import BookItem


class YsbookstoreSpider(scrapy.Spider):
    name = "ysbookstore"
    allowed_domains = ['yousuu.com']
    start_urls = 'https://api.yousuu.com/api/bookStore/books?page={pageNum}&t=1648726768189'
    start_page = 1
    end_page = 13300
    
    def start_requests(self):
        for i in range(self.start_page, self.end_page + 1):
            self.logger.info('正在爬取第{}页'.format(i))
            yield Request(self.start_urls.format(pageNum=str(i)), callback=self.parse,meta = {'dont_merge_cookies': True})
        



    def parse(self, response):
        try:
            books = json.loads(response.text)['data']['books']
        except KeyError:
            self.logger.info('爬取失败，原因未知')
            self.logger.info(json.loads(response.text))
        

        for book in books:
            book_item = BookItem()
            for item in book:
                book_item[item] = book[item]
                if item == 'tags':
                    tmp = ''
                    for tag in book_item[item]:
                        tmp+="、"+tag
                    book_item[item] = tmp
                if item == 'countWord' and not book_item[item]:
                    
                    book_item[item] = 0
            yield book_item
 
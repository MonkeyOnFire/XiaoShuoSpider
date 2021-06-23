import scrapy
import json
from scrapy import Request
import logging
from math import ceil
import re
from scrapydemo.items import bookListCommentItem, bookListInfoItem, bookSourceItem
from scrapydemo.spiders.yousuu import YousuuSpider


class YousuubooklistSpider(YousuuSpider):
    name = 'yousuubooklist'
    allowed_domains = ['www.yousuu.com']
    bookliststore_url = 'https://www.yousuu.com/api/booklists?type=man&screen=comprehensive&page='
    booklist_url = 'https://www.yousuu.com/api/booklist/{}?page={}&sort=default'
    booklistinfo_url = 'https://www.yousuu.com/api/booklist/{}/info'

    start_page = 452
    end_page = 670
    #end_page = 1
    # custom_settings = {
    # 'ITEM_PIPELINES' : {},
    # 'DOWNLOADER_MIDDLEWARES' : {}

    # }

    def start_requests(self):
        for page_num in range(self.start_page, self.end_page + 1):
            request_url = self.bookliststore_url + str(page_num)
            logging.info('开始爬取书单列表第{}页'.format(page_num))

            yield Request(request_url, callback=self.parse_booklist_list)

    def parse_booklist_list(self, response):

        book_list_ids = json.loads(response.text)['data']['booklists']

        for booklisttemp in book_list_ids:
            book_list_id = booklisttemp['_id']
            request_url = self.booklist_url.format(str(book_list_id), 1)
            logging.info('开始爬取书单{}'.format(book_list_id))

            yield Request(request_url, callback=self.parse_book_list)
            yield Request(self.booklistinfo_url.format(book_list_id), callback=self.parse_booklist_info)

    def parse_book_list(self, response):
        # 获取书单总页数
        page_total = ceil(json.loads(response.text)['data']['total']/20)
        page_index = re.search(r'(?<=page=)([0-9]+)', response.url).group()

        # 如果请求页码小于总页数，页码+1继续请求
        if(int(page_index) < page_total):
            new_url = response.url.replace('page={}'.format(
                page_index), 'page={}'.format(str(int(page_index)+1)))
            yield Request(new_url, callback=self.parse_book_list)

        booklists = json.loads(response.text)['data']['books']
        for booklist in booklists:
            bookList_Item = bookListCommentItem()

            for booklist_data in booklist:
                if booklist_data == '_id':
                    bookList_Item['id'] = booklist['_id']
                elif booklist_data == 'createrId':
                    bookList_Item['createrUserId'] = booklist['createrId']['_id']
                    bookList_Item['createrUserName'] = booklist['createrId']['userName']
                elif booklist_data == 'bookId':
                    bookList_Item['bookId'] = booklist['bookId']['bookId']
                    if booklist['bookId']['bookId']:
                        book_requ = YousuuSpider()

                        yield Request(super().book_info_url.format(book_id=booklist['bookId']['bookId']), callback=super().parse_book_info)

                elif booklist_data == 'tags':
                    if len(booklist['tags']) > 0:
                        bookList_Item['tags'] = '|'.join(booklist['tags'])
                    else:
                        bookList_Item['tags'] = ''

                else:
                    bookList_Item[booklist_data] = booklist[booklist_data]
            yield bookList_Item

    def parse_booklist_info(self, response):
        data = json.loads(response.text)
        if data.get("message") == '获取书单信息成功':
            booklistinfo_item = bookListInfoItem()
            for key in data.get('data'):
                if key in ['_id', 'createrId', '__v']:
                    if key == '_id':
                        booklistinfo_item['id'] = data.get('data')['_id']
                    elif key == 'createrId':
                        booklistinfo_item['createrUserId'] = data.get('data')[
                            'createrId']['_id']
                        booklistinfo_item['createrUserName'] = data.get(
                            'data')['createrId']['userName']
                    elif key == '__v':
                        booklistinfo_item['v'] = data.get('data')['__v']
                else:
                    try:
                        booklistinfo_item[key] = data.get('data')[key]
                    except KeyError:
                        continue
            yield booklistinfo_item

import scrapy
from scrapy import Request
import json

class YsbooklistUrlSpider(scrapy.Spider):
    name = "ysbooklisturl"
    allowed_domains = ['yousuu.com']
    start_urls = 'https://api.yousuu.com/api/bookStore/books?page={pageNum}&t=1648726768189'
    start_page = 1
    end_page = 13000
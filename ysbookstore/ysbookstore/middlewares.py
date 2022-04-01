# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

import json
import logging
from scrapy import signals
import requests
from fake_useragent import UserAgent
import scrapy_redis
from scrapy.exceptions import IgnoreRequest

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter

class RandomUserAgentMiddlware(object):
    '''
    随机更换user-agent
    模仿并替换site-package/scrapy/downloadermiddlewares源代码中的
    useragent.py中的UserAgentMiddleware类
    '''

    def __init__(self, crawler):

        super(RandomUserAgentMiddlware, self).__init__()
        self.ua = UserAgent()
        # 可读取在settings文件中的配置，来决定开源库ua执行的方法，默认是random，也可是ie、Firefox等等
        self.ua_type = crawler.settings.get("RANDOM_UA_TYPE", "random")

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    # 更换UserAgent逻辑在此方法中
    def process_request(self, request, spider):
        def get_ua():
            return getattr(self.ua, self.ua_type)
        #print('using fakeUA')
        logging.debug('using fakeUA')
        request.headers.setdefault('User-Agent', get_ua())

class ProxyMiddleware(object):

    def process_request(self, request, spider):
 
        proxy = requests.get("http://127.0.0.1:5555/random").text

        request.meta['proxy'] = proxy
        logging.info('using proxy: ' + proxy+'-----' + request.url)
        return None

class IpBannedMiddleware(object):


    def process_response(self, request, response, spider):
        logging.info(type(self))
        if response.status == 200:
            try:
                json.loads(response.text)
            except:
                logging.error('不是json数据爬取失败，状态码为{}'.format(response.status) + "服务器返回:" + response.text.encode('utf-8').decode('utf-8') + "代理IP为：" + request.meta['proxy'])
                redis_client = scrapy_redis.get_redis_from_settings(spider.settings)
                redis_client.set('yousuubannedIp:{}'.format(request.meta['proxy']),request.meta['proxy'],ex=259200 )
                #redis_client.sadd("yousuubannedIp",request.meta['proxy'])
                return request

        return response


class NoneTotalMiddleware(object):

    def process_response(self, request, response, spider):
        if response.status == 200:
            total = json.loads(response.text).get('data').get('total')
            if total == 0:
                logging.info('数据为空已抛弃' + response.text)
                raise IgnoreRequest

        return response

class YsbookstoreSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class YsbookstoreDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

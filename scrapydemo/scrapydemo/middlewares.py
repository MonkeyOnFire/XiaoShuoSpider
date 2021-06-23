# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import logging
from scrapy import signals
from fake_useragent import UserAgent
import requests
# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter
import scrapy_redis
import json
from scrapy.exceptions import IgnoreRequest



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
        proxy = ''
        redis_client = scrapy_redis.get_redis_from_settings(spider.settings)
        
        while True:
            proxy = requests.get("http://proxypool:5555/random").text
            banned_ip = redis_client.get('yousuubannedIp:{}'.format(proxy))
            if banned_ip:
                logging.info('ip已被ban，更换ip: ' + proxy+'-----' + request.url)
            else:
                break
        request.meta['proxy'] = proxy
        logging.info('using proxy: ' + proxy+'-----' + request.url)
        return None


class IpBannedMiddleware(object):


    def process_response(self, request, response, spider):

        if response.status == 200:
            try:
                json.loads(response.text)
            except:
                logging.error('不是json数据爬取失败，状态码为{}'.format(response.status) + "服务器返回:" + response.text + "代理IP为：" + request.meta['proxy'])
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

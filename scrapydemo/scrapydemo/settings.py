# Scrapy settings for scrapydemo project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

import datetime

BOT_NAME = 'scrapydemo'

SPIDER_MODULES = ['scrapydemo.spiders']
NEWSPIDER_MODULE = 'scrapydemo.spiders'


# 数据库地址
MYSQL_HOST = 'mysql'
# 数据库用户名:
MYSQL_USER = 'root'
# 数据库密码
MYSQL_PASSWORD = '123456'
# 数据库端口
MYSQL_PORT = 3306
# 数据库名称
MYSQL_DBNAME = 'yousuu'
# MYSQL_DBNAME = 'yousuuTest'
# 数据库编码
MYSQL_CHARSET = 'utf8mb4'

# 最大重试次数
RETRY_TIMES = 100


# 指定Redis的主机名和端口
REDIS_HOST = 'redis'
REDIS_PORT = 6379

# 调度器启用Redis存储Requests队列
SCHEDULER = "scrapy_redis.scheduler.Scheduler"

# 确保所有的爬虫实例使用Redis进行重复过滤
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"

# 将Requests队列持久化到Redis，可支持暂停或重启爬虫
SCHEDULER_PERSIST = True

# Requests的调度策略，默认优先级队列
SCHEDULER_QUEUE_CLASS = 'scrapy_redis.queue.PriorityQueue'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'scrapydemo (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs

# 配置爬取延迟
DOWNLOAD_DELAY = 0.1

# 配置超时时间
DOWNLOAD_TIMEOUT = 60

# The download delay setting will honor only one of:
#配置线程数
CONCURRENT_REQUESTS_PER_DOMAIN = 16
CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
# }

DEFAULT_REQUEST_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'scrapydemo.middlewares.ScrapydemoSpiderMiddleware': 543,
# }

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
# DOWNLOADER_MIDDLEWARES = {
#    'scrapydemo.middlewares.ScrapydemoDownloaderMiddleware': 543,
# }

DOWNLOADER_MIDDLEWARES = {
    #   FakeUserAgent
    'scrapydemo.middlewares.RandomUserAgentMiddlware': 543,
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    #   proxy代理池
    'scrapydemo.middlewares.ProxyMiddleware': 544,
    #   IP被banned重新请求
    'scrapydemo.middlewares.IpBannedMiddleware': 555,
    'scrapydemo.middlewares.NoneTotalMiddleware': 554



}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
# ITEM_PIPELINES = {
#    'scrapydemo.pipelines.ScrapydemoPipeline': 300,
# }
ITEM_PIPELINES = {
    'scrapydemo.pipelines.introductionTooLongPipline': 300,
    'scrapydemo.pipelines.ToMysqlTwistedPipeline': 301,
    #'scrapy_redis.pipelines.RedisPipeline': 301
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

# 配置日志级别及文件
LOG_LEVEL = 'INFO'
to_day = datetime.datetime.now()
log_file_path = './scrapydemo/log/scrapy_{}_{}_{}_{}_{}.log'.format(
    to_day.year, to_day.month, to_day.day, to_day.hour, to_day.minute)
LOG_FILE = log_file_path

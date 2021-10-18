# Scrapy settings for qdyp project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'qdyp'

SPIDER_MODULES = ['qdyp.spiders']
NEWSPIDER_MODULE = 'qdyp.spiders'

# 最大重试次数
RETRY_TIMES = 100

# 数据库地址
MYSQL_HOST = 'mysql'
# 数据库用户名:
MYSQL_USER = 'root'
# 数据库密码
MYSQL_PASSWORD = '123456'
# 数据库端口
MYSQL_PORT = 3306
# 数据库名称
MYSQL_DBNAME = 'xiaoshuo'

# 数据库编码
MYSQL_CHARSET = 'utf8mb4'

# 指定Redis的主机名和端口
REDIS_HOST = '127.0.0.1'
REDIS_PORT = 6379

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'qdyp (+http://www.yourdomain.com)'




# # 调度器启用Redis存储Requests队列
# SCHEDULER = "scrapy_redis.scheduler.Scheduler"

# # 确保所有的爬虫实例使用Redis进行重复过滤
# DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"

# # 将Requests队列持久化到Redis，可支持暂停或重启爬虫
# SCHEDULER_PERSIST = True

# # Requests的调度策略，默认优先级队列
# SCHEDULER_QUEUE_CLASS = 'scrapy_redis.queue.PriorityQueue'




# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# 配置爬取延迟
DOWNLOAD_DELAY = 5

# 配置超时时间
DOWNLOAD_TIMEOUT = 60

#配置线程数
CONCURRENT_REQUESTS_PER_DOMAIN = 1
CONCURRENT_REQUESTS_PER_IP = 1


DEFAULT_REQUEST_HEADERS = {
    'Accept': 'application/json',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
}

DOWNLOADER_MIDDLEWARES = {
    #   FakeUserAgent
    # 'qdyp.middlewares.RandomUserAgentMiddlware': 543,
    # 'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    
    #   proxy代理池
    # 'qdyp.middlewares.ProxyMiddleware': 544,
}

ITEM_PIPELINES = {

    #存mysql
    'qdyp.pipelines.ToMysqlTwistedPipeline': 301,

}


# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = True

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'qdyp.middlewares.QdypSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'qdyp.middlewares.QdypDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    'qdyp.pipelines.QdypPipeline': 300,
#}

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

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import time
import pymysql
from twisted.enterprise import adbapi
from pymysql import cursors
from twisted.enterprise import adbapi
from pymysql.err import IntegrityError
from scrapy.exceptions import DropItem
from pymysql.converters import escape_string

class QdypPipeline:
    def process_item(self, item, spider):
        return item

class ToMysqlTwistedPipeline(object):

    # 初始化函数
    def __init__(self, db_pool):
        self.db_pool = db_pool

    # 从settings配置文件中读取参数
    @classmethod
    def from_settings(cls, settings):
        # 用一个db_params接收连接数据库的参数
        db_params = dict(
            host=settings['MYSQL_HOST'],
            user=settings['MYSQL_USER'],
            password=settings['MYSQL_PASSWORD'],
            port=settings['MYSQL_PORT'],
            database=settings['MYSQL_DBNAME'],
            charset=settings['MYSQL_CHARSET'],
            use_unicode=True,
            # 设置游标类型
            cursorclass=cursors.DictCursor
        )
        # 创建连接池
        db_pool = adbapi.ConnectionPool('pymysql', **db_params)

        # 返回一个pipeline对象
        return cls(db_pool)

    # 处理item函数
    def process_item(self, item, spider):
        # 把要执行的sql放入连接池
        query = self.db_pool.runInteraction(self.insert_into, item)
        # 如果sql执行发送错误,自动回调addErrBack()函数
        query.addErrback(self.handle_error, item, spider)

        # 返回Item
        return item

    # 处理sql函数
    def insert_into(self, cursor, item):
        # 创建sql语句
        #sql = "INSERT INTO book (id,status,tags,shielded,defaultSource,score,scoreDetail1,scoreDetail2,scoreDetail3,scoreDetail4,scoreDetail5,scorerCount,commentCount,addListCount,addListTotal,recom_ignore,title,author,cover,introduction,countWord,updateAt,v,caseId,classInfo,classId,className,channel) VALUES ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(item['id'],item['status'],item['tags'],item['shielded'],item['defaultSource'],item['score'],item['scoreDetail1'],item['scoreDetail2'],item['scoreDetail3'],item['scoreDetail4'],item['scoreDetail5'],item['scorerCount'],item['commentCount'],item['addListCount'],item['addListTotal'],item['recom_ignore'],item['title'],item['author'],item['cover'],item['introduction'],item['countWord'],item['updateAt'],item['v'],item['caseId'],item['classInfo'],item['classId'],item['className'],item['channel'] + ";INSERT INTO bookSource (bookId,siteName,bookPage) VALUES ('{}','{}','{}')".format(item['bookId'],item['siteName'],item['bookPage']))
        updateTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        id = item['bid'] + '_' + time.strftime("%Y-%m-%d", time.localtime())
        sql = r"INSERT INTO qdyp VALUES ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}') ON DUPLICATE KEY UPDATE id='{}',upDateTime='{}'".format(id,item['bid'],item['bName'],item['bAuth'],item['desc'],item['cat'],item['catId'],item['cnt'],item['rankCnt'],item['rankNum'],updateTime,id,updateTime)
        #print(sql)
        cursor.execute(sql)

    # 错误函数
    def handle_error(self, failure, item, spider):
        # #输出错误信息
        # logging.error(failure)
        # logging.error('数据库错误数据)
        print(failure)
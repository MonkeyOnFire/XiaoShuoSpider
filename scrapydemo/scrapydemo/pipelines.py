# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymysql
from twisted.enterprise import adbapi
from pymysql import cursors
from twisted.enterprise import adbapi
from scrapydemo.items import bookItem, bookListCommentItem, bookListInfoItem, bookSourceItem
from pymysql.err import IntegrityError
from scrapy.exceptions import DropItem
import logging
from pymysql.converters import escape_string


class introductionTooLongPipline(object):

    def __init__(self):
        self.limit = 20000

    def process_item(self, item, spider):
        for info in item:
            if None == item.get(info):
                logging.info('Nono数据清洗为0')
                item[info] = 0

        if isinstance(item, bookItem):
            if type(item['introduction']) == str and len(item['introduction']) > self.limit:
                item['introduction'] = item['introduction'][0:self.limit].strip() + ''
                logging.info("introduction过长已截取,bookid为{}".format(item['id']))
            return item

        if isinstance(item, bookListCommentItem):
            try:
                item['tags']
            except:
                item['tags'] = ''
                logging.info("tags不存在，已赋值为空字符串")

            return item

        if isinstance(item, bookListInfoItem):
            if not item.get('praiseTotal'):
                item['praiseTotal'] = 0
                logging.info("praiseTotal为空，已赋值为0")
            if len(item['content']) > self.limit:
                item['content'] = item['content'][0:self.limit].strip() + ''
                logging.info("content过长已截取,bookid为{}".format(item['id']))
            return item
        return item
        # else:
        #     raise DropItem('Missing introduction')


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
        sql = ''
        if isinstance(item, bookItem):
            sql = "INSERT INTO book (id,status,tags,shielded,defaultSource,score,scoreDetail1,scoreDetail2,scoreDetail3,scoreDetail4,scoreDetail5,scorerCount,commentCount,addListCount,addListTotal,recom_ignore,title,author,cover,introduction,countWord,updateAt,v,caseId,classInfo,classId,className,channel,scrapyUpdateTime) VALUES ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}',now())".format(
                item['id'], item['status'], item['tags'], item['shielded'], item['defaultSource'], item['score'], item['scoreDetail1'], item['scoreDetail2'], item['scoreDetail3'], item['scoreDetail4'], item['scoreDetail5'], item['scorerCount'], item['commentCount'], item['addListCount'], item['addListTotal'], item['recom_ignore'], item['title'], item['author'], item['cover'], escape_string(item['introduction']), item['countWord'], item['updateAt'], item['v'], item['caseId'], item['classInfo'], item['classId'], item['className'], item['channel'])
            try:
                cursor.execute(sql)
                logging.info("插入book完成,bookid={}".format(item['id']))
            except IntegrityError:
                logging.info("已存在，更新bookINFO,bookid={}".format(item['id']))
                sql = "UPDATE book set status='{}',tags='{}',shielded='{}',defaultSource='{}',score='{}',scoreDetail1='{}',scoreDetail2='{}',scoreDetail3='{}',scoreDetail4='{}',scoreDetail5='{}'  \
                    ,scorerCount='{}',commentCount='{}',addListCount='{}',addListTotal='{}',recom_ignore='{}',title='{}',author='{}',cover='{}',introduction='{}',countWord='{}',updateAt='{}',v='{}' \
                        ,caseId='{}',classInfo='{}',classId='{}',className='{}',channel='{}',scrapyUpdateTime=now() where id = {}".format(item['status'], item['tags'], item['shielded'], item['defaultSource'], item['score'], item['scoreDetail1'], item['scoreDetail2'], item['scoreDetail3'], item['scoreDetail4'], item['scoreDetail5'], item['scorerCount'], item['commentCount'], item['addListCount'], item['addListTotal'], item['recom_ignore'], item['title'], item['author'], item['cover'], escape_string(item['introduction']), item['countWord'], item['updateAt'], item['v'], item['caseId'], item['classInfo'], item['classId'], item['className'], item['channel'], item['id'])
                cursor.execute(sql)

        elif isinstance(item, bookSourceItem):
            sql = "INSERT INTO bookSource (bookId,siteName,bookPage,scrapyUpdateTime) VALUES ('{}','{}','{}',now())".format(
                item['bookId'], item['siteName'], item['bookPage'])
            try:
                cursor.execute(sql)
                logging.info("插入bookSource完成,bookId={}".format(item['bookId']))
            except IntegrityError:
                logging.info(
                    "已存在，更新bookSource,bookId={}".format(item['bookId']))
                sql = "UPDATE bookSource set siteName='{}',bookPage='{}',scrapyUpdateTime=now() where bookId = {}".format(
                    item['siteName'], item['bookPage'], item['bookId'])
                cursor.execute(sql)

        elif isinstance(item, bookListCommentItem):

            sql = "INSERT INTO bookComment (id,createrUserId,createrUserName,content,createdAt,inReview,\
                jurisdiction,praiseCount,replyCount,score,shielded,tags,stickie,sortId,bookId,collected,\
                    booklistShipId,voting,replyable,scrapyUpdateTime) VALUES ('{}','{}','{}','{}','{}',{},'{}','{}','{}','{}',{},'{}',{},'{}','{}',{},'{}','{}',{},now())".format(item['id'], item['createrUserId'], item['createrUserName'], escape_string(item['content']), item['createdAt'], item['inReview'], item['jurisdiction'], item['praiseCount'], item['replyCount'], item['score'], item['shielded'], item['tags'], item['stickie'], item['sortId'], item['bookId'], item['collected'], item['booklistShipId'], item['voting'], item['replyable'])
            try:
                cursor.execute(sql)
                logging.info("插入bookComment完成,Id={}".format(item['id']))
            except IntegrityError:
                logging.info("已存在，更新bookComment,Id={}".format(item['id']))
                sql = "UPDATE bookComment set createrUserId='{}',createrUserName='{}',content='{}',createdAt='{}',\
                    inReview={},jurisdiction='{}',praiseCount='{}',replyCount='{}',\
                        score='{}',shielded={},tags='{}',stickie={},sortId='{}',\
                            bookId='{}',collected={},booklistShipId='{}',voting='{}',replyable={},scrapyUpdateTime=now()\
                                 where id = '{}'".format(item['createrUserId'], item['createrUserName'], escape_string(item['content']), item['createdAt'], item['inReview'], item['jurisdiction'], item['praiseCount'], item['replyCount'], item['score'], item['shielded'], item['tags'], item['stickie'], item['sortId'], item['bookId'], item['collected'], item['booklistShipId'], item['voting'], item['replyable'], item['id'])
                cursor.execute(sql)

        elif isinstance(item, bookListInfoItem):

            sql = "INSERT INTO bookListInfo (id,inReview,editable,comTotal,clicks,collectNum,\
                favsTotal,bookTotal,praiseTotal,essence,shielded,deleted,unSearch,createrUserId,createrUserName,title,\
                    listType,content,createdAt,updateAt,praiseAt,v,collected,voting,scrapyUpdateTime) VALUES ('{}',{},'{}','{}','{}','{}','{}','{}','{}',{},{},{},{},'{}','{}','{}','{}','{}','{}','{}','{}','{}',{},'{}',now())".format(item['id'], item['inReview'], item['editable'], item['comTotal'], item['clicks'], item['collectNum'], item['favsTotal'], item['bookTotal'], item['praiseTotal'], item['essence'], item['shielded'], item['deleted'], item['unSearch'], item['createrUserId'], item['createrUserName'], item['title'], item['listType'], escape_string(item['content']), item['createdAt'], item['updateAt'], item['praiseAt'], item['v'], item['collected'], item['voting'])
            try:
                cursor.execute(sql)
                logging.info("插入bookListInfo完成,Id={}".format(item['id']))
            except IntegrityError:
                logging.info("已存在，更新bookListInfo,Id={}".format(item['id']))
                sql = "UPDATE bookListInfo set inReview={},editable='{}',comTotal='{}',\
                    clicks='{}',collectNum='{}',favsTotal='{}',bookTotal='{}',\
                        praiseTotal='{}',essence={},shielded={},deleted={},unSearch={},\
                            createrUserId='{}',createrUserName='{}',title='{}',listType='{}',content='{}',\
                                createdAt='{}',updateAt='{}',praiseAt='{}',v='{}',collected={},voting='{}',scrapyUpdateTime=now()\
                                 where id = '{}'".format(item['inReview'], item['editable'], item['comTotal'], item['clicks'], item['collectNum'], item['favsTotal'], item['bookTotal'], item['praiseTotal'], item['essence'], item['shielded'], item['deleted'], item['unSearch'], item['createrUserId'], item['createrUserName'], item['title'], item['listType'], escape_string(item['content']), item['createdAt'], item['updateAt'], item['praiseAt'], item['v'], item['collected'], item['voting'], item['id'])
                cursor.execute(sql)

    # 错误函数
    def handle_error(self, failure, item, spider):
        # #输出错误信息
        logging.error(failure)
        logging.error('数据库错误数据id为' + str(item['id']))

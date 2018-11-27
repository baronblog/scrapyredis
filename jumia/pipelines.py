# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from . import settings
import time
import pymysql
import pymysql.cursors
from twisted.enterprise import adbapi
from twisted.internet import reactor
import asyncio
import aiomysql
from aiomysql.cursors import DictCursor
import redis


# class JumiaPipeline(object):
#     def __init__(self):
#         self.conn = pymysql.connect(
#             host=settings.MYSQL_HOST,
#             db=settings.MYSQL_DBNAME,
#             user=settings.MYSQL_USER,
#             passwd=settings.MYSQL_PASSWORD,
#             charset='utf8',
#             use_unicode=False
#         )
#         self.cursor = self.conn.cursor()
#
#     def process_item(self, item, spider):
#         self.insertdata(item)
#         return item
#
#     def insertdata(self, item):
#         itemstr = '"'
#         dates = str(time.strftime("%Y%m%d"))
#         print("我要开始处理商品详情页数据")
#         print(item)
#         sql = '''insert into jumia_scrapy (l1,l2,l3,goods_name,review,store,sale,rate,product_url,price,dates) values ({l1},{l2},{l3},{goods_name},{review},{store},{sale},{rate},{product_url},{price},{dates})'''.format( \
#             l1=itemstr + str(item['l1'][0]) + itemstr, l2=itemstr + str(item['l2'][0]) + itemstr,
#             l3=itemstr + str(item['l3'][0]) + itemstr,
#             goods_name=itemstr + str(item['goods_name'][0]).replace("'", "").replace('''"''', "") + itemstr,
#             review=itemstr + str(item['review']) + itemstr, store=itemstr + str(item['store'][0]) + itemstr,
#             sale=itemstr + str(item['sale']) + itemstr, \
#             rate=itemstr + str(item['rate']) + itemstr, product_url=item['product_url'],
#             price=itemstr + str(item['price'][0]) + itemstr, dates=itemstr + dates + itemstr)
#         print(type(item['review']))
#         print(sql)
#         print(item['product_url'])
#         self.cursor.execute(sql)
#         self.conn.commit()
#
# class MysqlTwistedPipline(object):
#     def __init__(self, dbpool):
#         self.dbpool=dbpool
#
#     @classmethod
#     def from_settings(cls, settings):
#         #读取settings.py文件中的配置
#         dbparms =dict(
#             host = settings['MYSQL_HOST'],
#             db = settings['MYSQL_DBNAME'],
#             user = settings['MYSQL_USER'],
#             passwd = settings['MYSQL_PASSWORD'],
#             charset = 'utf8',
#             cursorclass=pymysql.cursors.DictCursor,
#             use_unicode=True,
#         )
#         #创建连接池
#         dbpool = adbapi.ConnectionPool("pymysql", **dbparms)
#         return cls(dbpool)
#
#     def process_item(self, item, spider):
#         print("创建连接池")
#         query = self.dbpool.runInteraction(self.insert_data, item)
#         query.addCallback(self.handle_error)
#
#     def handle_error(self, failure):
#         print(failure)
#
#     def insert_data(self, cursor, item):
#         print("开始异步插入数据")
#         dates = int(time.time())
#         insert_sql="insert into jumia_scrapy_tongbu (l1,l2,l3,goods_name,review,store,sale,rate,product_url,price,dates) values (%s ,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
#         parameters = (item['l1'][0], item['l2'][0], item['l3'][0],item['goods_name'][0], \
#                                                                        item['review'][0], item['store'][0], item['sale'], item['rate'], \
#                                                                        item['product_url'], item['price'][0], dates)
#         print(insert_sql)
#         try:
#             cursor.execute(insert_sql, parameters)
#             print("异步插入成功")
#         except:
#             print("异步插入失败")

# class AiomysqlPipeline(object):
#     def __init__(self):
#         self.host = settings.MYSQL_HOST
#         self.port = settings.MYSQL_PORT
#         self.db = settings.MYSQL_DBNAME
#         self.user = settings.MYSQL_USER
#         self.passwd = settings.MYSQL_PASSWORD
#         self.loop = asyncio.get_event_loop()
#
#     async def connect(self):
#         self.conn = await aiomysql.connect(self.host, self.port, self.user, self.passwd,
#                                            self.db, self.loop)
#         return self.conn
#
#     async def close(self):
#         await self.conn.close()
#         return True
#
#     async def process_item(self, item, spider):
#         print("开始执行插入数据")
#         self.loop.run_until_complete(self.conn_item(item, spider))
#
#     async def conn_item(self, item, spider):
#         dates = str(time.strftime("%Y%m%d"))
#         insert_sql = "insert into jumia_scrapy_tongbu (l1,l2,l3,goods_name,review,store,sale,rate,product_url,price,dates) values (%s ,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
#         parameters = (item['l1'][0], item['l2'][0], item['l3'][0],item['goods_name'][0], \
#                                                                                 item['review'][0], item['store'][0], item['sale'], item['rate'], \
#                                                                                 item['product_url'], item['price'][0], dates)
#         async with self.conn.cursor() as cur:
#             await cur.excute(insert_sql, parameters)
#             print("执行成功")

class AiomysqlPipeline(object):
    def __init__(self):
        #self.pool = redis.ConnectionPool(host=settings.redishost, port=settings.redisport,password=settings.redispassword, decode_responses=True, db=1)
        #self.r = redis.Redis(connection_pool=self.pool)
        self.r = redis.Redis(host=settings.redishost, port=settings.redisport,password=settings.redispassword, decode_responses=True,  db=1)

    def process_item(self, item, spider):
        dates = time.strftime("%Y%m%d")
        parameters = (item['l1'][0], item['l2'][0], item['l3'][0], item['goods_name'][0], item['review'][0], item['store'][0], item['sale'], item['rate'], \
        item['product_url'], item['price'][0], dates)
        insert_sql = "insert into jumia_scrapy_tongbu (l1,l2,l3,goods_name,review,store,sale,rate,product_url,price,dates) values ('%s' ,'%s', '%s', '%s', '%s',\
                  '%s', '%s', '%s', '%s', '%s', '%s')"%(parameters)
        try:
            print("开始插入redis数据库")
            self.r.set(item['product_url'], insert_sql)
            print("已经插入完成redis数据库")
        except:
            time.sleep(0.1)
            self.r.set(item['product_url'], insert_sql)
            print("已经出粗，再次插入redis")








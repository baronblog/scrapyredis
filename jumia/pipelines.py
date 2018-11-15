# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from . import settings
import time
import pymysql

class JumiaPipeline(object):
    def __init__(self):
        self.conn = pymysql.connect(
            host=settings.MYSQL_HOST,
            db=settings.MYSQL_DBNAME,
            user=settings.MYSQL_USER,
            passwd=settings.MYSQL_PASSWORD,
            charset='utf8',
            use_unicode=False
        )
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        self.insertdata(item)
        return item

    def insertdata(self, item):
        itemstr = '"'
        dates = str(time.strftime("%Y%m%d"))
        print("我要开始处理商品详情页数据")
        print("品类l1的字符类型是："+str(type(item['l1'][0])))
        print(item)
        sql = '''insert into jumia_scrapy (l1,l2,l3,goods_name,review,store,sale,rate,product_url,price,dates) values ({l1},{l2},{l3},{goods_name},{review},{store},{sale},{rate},{product_url},{price},{dates})'''.format( \
            l1=itemstr + str(item['l1'][0]) + itemstr, l2=itemstr + str(item['l2'][0]) + itemstr,
            l3=itemstr + str(item['l3'][0]) + itemstr,
            goods_name=itemstr + str(item['goods_name'][0]).replace("'", "").replace('''"''', "") + itemstr,
            review=itemstr + str(item['review']) + itemstr, store=itemstr + str(item['store'][0]) + itemstr,
            sale=itemstr + str(item['sale']) + itemstr, \
            rate=itemstr + str(item['rate']) + itemstr, product_url=item['product_url'],
            price=itemstr + str(item['price'][0]) + itemstr, dates=itemstr + dates + itemstr)
        print(type(item['review']))
        print(sql)
        print(item['product_url'])
        self.cursor.execute(sql)
        self.conn.commit()

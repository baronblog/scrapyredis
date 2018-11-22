# -*- coding: utf-8 -*-
import scrapy
from scrapy_redis.spiders import RedisSpider
from ..items import JumiaItem


class JumiaspiderSpider(scrapy.Spider):
    name = 'jumiaspider'
    allowed_domains = ['jumia.co.ke']
    redis_key = 'jumiaspider:start_urls'
    start_urls = ['https://www.jumia.co.ke/']

    def parse(self, response):
        #获取一级品类链接
        categoryurl1 = response.xpath('//a[@class="main-category"]/@href').extract()
        for url in categoryurl1:
            print("正在抓取该url：" + str(url) + "\n")
            yield scrapy.Request(url=url, callback=self.parse_category, meta={"category":1, "url":url})

    def parse_category(self, response):
        print("---------------获得一级分类连接-------："+str(response.meta['url']))
        #得到一级分品类类链接响应，通过xpath获取二级分类
        categoryurl2 = response.xpath('//li[@class="osh-subcategory"]/a/@href').extract()
        #获取一级分类页面最后一页值的id
        try:
            nextproducturl = response.xpath('//ul[@class="osh-pagination -horizontal"]/li/a/@title').extract()[-2]
        except:
            nextproducturl = 0
        print("我要打印categoryurl：" + str(categoryurl2))
        print("我要打印nextproducturl：" + str(nextproducturl))
        print(type(nextproducturl))

        if int(nextproducturl):
            for r in range(1, int(nextproducturl)+1):
                next_category_url = str(response.url) + "?page=" + str(r)
                print("正在抓取一级分类链接分页：" + str(next_category_url))
                yield scrapy.Request(url=next_category_url, callback=self.parse_product,meta={"category": 1})
        else:
            pass

        for categorylv2 in categoryurl2:
            print("正在抓取二级分类链接页面：" + str(categorylv2))
            yield scrapy.Request(url=categorylv2, callback=self.parse_category_l2, meta={"category": 2,"parse_category_l2":categorylv2})

    def parse_category_l2(self, response):
        print("--------------------我获得了二级分类链接-------------------：" + str(response.meta['parse_category_l2']))
        try:
            nextproducturll2 = response.xpath('//ul[@class="osh-pagination -horizontal"]/li/a/@title').extract()[-2]
        except:
            nextproducturll2 = 0
        categoryurll3 = response.xpath('//li[@class="osh-subcategory"]/a/@href').extract()

        if int(nextproducturll2):
            for r in range(1, int(nextproducturll2)+1):
                next_category_urll2 = str(response.url) + "?page=" + str(r)
                print("正在抓取二级分类页面分页：" + str(next_category_urll2))
                yield scrapy.Request(url=next_category_urll2, callback=self.parse_product, meta={"category":2})
        else:
            pass

        for categoryl3 in categoryurll3:
            print("正在抓取三级分类链接页面：" + str(categoryl3))
            yield scrapy.Request(url=categoryl3, callback=self.parse_category_l3, meta={"category":3,"categoryl3":categoryl3})

    def parse_category_l3(self, response):
        print("-------------------获得三级分类连接------------------：" + str(response.meta['categoryl3']))
        try:
            nextproducturll3 = response.xpath('//ul[@class="osh-pagination -horizontal"]/li/a/@title').extract()[-2]
        except:
            nextproducturll3 = 0

        if int(nextproducturll3):
            for r  in range(1, int(nextproducturll3)):
                next_category_urll3 = str(response.url) + "?page=" + str(r)
                print("正在抓取三级分类页面分页：" + str(next_category_urll3))
                yield scrapy.Request(url=next_category_urll3, callback=self.parse_product, meta={"category":3})
        else:
            pass

    def parse_product(self, response):
        producturl = response.xpath('//a[@class="link"]/@href').extract()

        for good in producturl:
            print("正在抓取"+str(response.meta['category'])+"级分类页面的具体内容：" + str(good))
            yield scrapy.Request(url=good, callback=self.product)

    def product(self, response):
        item = JumiaItem()
        item['l1'] = response.xpath('//nav[@class="osh-breadcrumb"]/ul/li[1]/a/@title').extract()
        item['l2'] = response.xpath('//nav[@class="osh-breadcrumb"]/ul/li[2]/a/@title').extract()
        item['l3'] = response.xpath('//nav[@class="osh-breadcrumb"]/ul/li[3]/a/@title').extract()
        item['goods_name'] = response.xpath('//h1/text()').extract()
        item['review'] = response.xpath('//div[@class="total-ratings"]/text()').extract()
        if item['review']:
            pass
        else:
            item['review'] = [0]
        item['store'] = response.xpath('//a[@class="-name"]/text()').extract()
        item['sale'] = response.xpath('//span[@class="text color-default bold -prxs -inline-block -bold"]/text()').extract()
        if item['sale']:
            item['sale'] = item['sale'][0]
        else:
            item['sale'] = 0
        item['rate'] = response.xpath('//span[@class="text color-default-800 -seller_score"]/text()').extract()
        if item['rate']:
            item['rate'] = item['rate'][0]
        else:
            item['rate'] = 0
        item['product_url'] = response.xpath('//li[@class="last-child"]/a/@href').extract()
        item['price'] = response.xpath('//span[@class="price"]/span[@dir="ltr"]/@data-price').extract()
        if item['price']:
            pass
        else:
            item['price'] = response.xpath('//span[@class="price -no-special"]/span[2]/text()').extract()
        print("开始打印item")
        print(item['l1'][0], item['l2'][0], item['l3'][0],item['goods_name'][0], \
                                                                       item['review'][0], item['store'][0], item['sale'], item['rate'], \
                                                                       item['product_url'], item['price'][0])
        yield item

# -*- coding: utf-8 -*-
import scrapy
from scrapy_redis.spiders import RedisSpider
from scrapy import cmdline
from ..items import JumiaItem


class JumiaspiderSpider(RedisSpider):
    name = 'jumiaspider'
    allowed_domains = ['jumia.co.ke']
    redis_key = 'jumiaspider:start_urls'
    start_urls = ['https://www.jumia.co.ke/']

    def parse(self, response):
        categoryurl = response.xpath('//a[@class="main-category"]/@href').extract()
        for url in categoryurl:
            print("正在抓取该url：" + str(url) + "\n")
            yield scrapy.Request(url=url, callback=self.parse_category)


    def parse_category(self,response):
        producturl = response.xpath('''//a[@class="link"]/@href''').extract()
        categoryurl = response.xpath('//li[@class="osh-subcategory"]/a/@href').extract()
        nextproducturl = list(set(response.xpath('//li/a[@title="Next"]/@href').extract()))
        print("我要打印producturl：" + str(producturl))
        print("我要打印nextproducturl：" + str(nextproducturl) )

        for product in producturl:
            print("正在抓取该产品链接：" + str(product) + "\n")
            yield scrapy.Request(url=product, callback=self.paese_product)

        if nextproducturl is not None:
            yield scrapy.Request(url=nextproducturl[0], callback=self.parse_category)

        for category in categoryurl:
            yield scrapy.Request(url=category, callback=self.parse_category)

    def paese_product(self,response):
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
            item['rate'] = 0
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

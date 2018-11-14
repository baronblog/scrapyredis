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
            yield scrapy.Request(url=url, callback=self.parse_category)


    def parse_category(self,response):
        producturl=response.xpath('''//a[@class="link"]''').extract()
        nextproducturl=response.xpath('(//ul[@class="osh-pagination -horizontal"])[last()]/li[last()]').css("a::attr(href)").extract()
        for product in producturl:
            yield scrapy.Request(url=product,callback=self.paese_product)

        if nextproducturl is not None:
            yield scrapy.Request(url=nextproducturl[0],callback=self.parse_category())

    def paese_product(self,response):
        item=JumiaItem()
        item['l1']=response.xpath('/html/body/main/nav/ul/li[1]/a/text()').extract()
        item['l2']=response.xpath('/html/body/main/nav/ul/li[2]/a/text()').extract()
        item['l3']=response.xpath('/html/body/main/nav/ul/li[3]/a/text()').extract()
        item['goods_name']=response.xpath('/html/body/main/section[1]/div[2]/div[1]/span/h1/text()').extract()
        item['review']=response.xpath('/html/body/main/section[1]/div[2]/div[1]/div[4]/div[2]/text()').extract()
        if item['review']:
            item['review']=item['review'][0]
        else:
            item['review']=0
        item['store']=response.xpath('/html/body/main/section[1]/div[2]/div[2]/ul/li[1]/ul/li[1]/span/strong/a/text()').extract()
        if item['store']:
            pass
        else:
            item['store']=response.xpath('/html/body/main/section[1]/div[2]/div[2]/ul/li[1]/div[1]/a/text()').extract()
        item['sale']=response.xpath('/html/body/main/section[1]/div[2]/div[2]/ul/li[1]/ul/li[2]/div[2]/span[1]/text()').extract()
        if item['sale']:
            item['sale']=item['sale'][0]
        else:
            item['sale']=response.xpath('/html/body/main/section[1]/div[2]/div[2]/ul/li[1]/div[2]/div[2]/span[1]/text()').extract()
            if item['sale']:
                item['sale']=item['sale'][0]
            else:
                item['sale']=0
        item['rate']=response.xpath('/html/body/main/section[1]/div[2]/div[2]/ul/li[1]/ul/li[2]/div[1]/div/span/text()').extract()
        if item['rate']:
            item['rate']=item['rate'][0]
        else:
            item['rate']=response.xpath('/html/body/main/section[1]/div[2]/div[2]/ul/li[1]/div[2]/div[1]/div/span/text()').extract()
            if item['rate']:
                item['rate']=item['rate'][0]
            else:
                item['rate']=0
        item['product_url']="'"+str(response.url)+"'"
        item['price']=response.xpath('/html/body/main/section[1]/div[2]/div[1]/div[8]/div[1]/div/span/span[2]/text()').extract()
        if item['price']:
            pass
        else:
            item['price']=response.xpath('/html/body/main/section[1]/div[2]/div[1]/div[7]/div[1]/div/span/span[2]/text()').extract()
        yield item

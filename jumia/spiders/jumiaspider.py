# -*- coding: utf-8 -*-
import scrapy


class JumiaspiderSpider(scrapy.Spider):
    name = 'jumiaspider'
    allowed_domains = ['jumia.co.ke']
    start_urls = ['jumia.co.ke/']

    def parse(self, response):
        

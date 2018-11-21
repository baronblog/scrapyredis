# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class JumiaItem(Item):
    next_url = Field()
    l1 = Field()
    l2 = Field()
    l3 = Field()
    goods_name = Field()
    review = Field()
    store = Field()
    sale = Field()
    rate = Field()
    product_url = Field()
    price = Field()
    dates = Field()


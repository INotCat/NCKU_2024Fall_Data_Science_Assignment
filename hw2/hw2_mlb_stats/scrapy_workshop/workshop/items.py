# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class WorkshopItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    PLAYER = scrapy.Field()
    TEAM = scrapy.Field()
    G = scrapy.Field()
    AB = scrapy.Field()
    R = scrapy.Field()
    H = scrapy.Field()
    # B2 = scrapy.Field()
    # B3 = scrapy.Field()
    HR = scrapy.Field()
    RBI = scrapy.Field()
    BB = scrapy.Field()
    SO = scrapy.Field()
    SB = scrapy.Field()
    # CS = scrapy.Field()
    AVG = scrapy.Field()
    OBP = scrapy.Field()
    SLG = scrapy.Field()
    OPS = scrapy.Field()

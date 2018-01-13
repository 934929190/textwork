#coding=utf-8

#Define here the models for your scraped items

from scrapy.item import Item, Field

class TutorialItem(Item):

    #define the fields for your item here like:
movie_name = Field()
movie_picture = Field()

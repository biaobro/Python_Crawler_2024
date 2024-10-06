# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class LazadaPItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class JapaneseAnimeItem(scrapy.Item):
    """ 定义动漫电影数据结构信息"""
    ranking = scrapy.Field()  # 排名
    title = scrapy.Field()  # 名称
    postImg = scrapy.Field()  # 图片海报
    year = scrapy.Field()  # 年份
    score = scrapy.Field()  # 评分
    ratingPeople = scrapy.Field()  # 评分人数

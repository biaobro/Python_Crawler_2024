# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import logging
import pymongo
import urllib.parse

class MongodbPipeline:
    db_name = 'ScrapyCrawler'
    collection_name = 'transcripts'
    def open_spider(self, spider):
        logging.warning('Spider Opened - Pipeline')
        username = urllib.parse.quote_plus('biaobro')
        password = urllib.parse.quote_plus('ScrapyCrawler')
        # self.client = pymongo.MongoClient("mongodb+srv://%s:%s@cluster0.m2rtj.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"%(username, password))
        # self.client = pymongo.MongoClient("mongodb+srv://biaobro:ScrapyCrawler@cluster0.m2rtj.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
        self.client = pymongo.MongoClient("mongodb://localhost:27017/")
        self.db = self.client[self.db_name]

    def close_spider(self, spider):
        self.client.close()
        logging.warning('Spider Closed - Pipeline')

    def process_item(self, item, spider):
        self.db[self.collection_name].insert_one(item)
        return item

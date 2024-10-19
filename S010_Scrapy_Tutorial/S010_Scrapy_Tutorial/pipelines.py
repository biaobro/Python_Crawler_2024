# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import logging
import pymongo
import urllib.parse
import sqlite3


class MongodbPipeline:
    db_name = 'ScrapyCrawler'
    collection_name = 'transcripts'

    def __init__(self):
        self.db = None
        self.client = None

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


class SQLitePipeline:
    def __init__(self):
        self.cur = None
        self.conn = None

    def open_spider(self, spider):
        self.conn = sqlite3.connect('transcripts.db')
        self.cur = self.conn.cursor()

        # query
        # transcript TEXT,
        try:
            # 注意最后1个字段不要写逗号，否则无法创建TABLE，还没有明确报错
            self.cur.execute('''
                CREATE TABLE IF NOT EXISTS transcripts(
                    title TEXT,
                    plot TEXT,
                    transcript TEXT,
                    url  TEXT
                )
            ''')

            self.conn.commit()
        except sqlite3.OperationalError:
            logging.error('sqlite3 OperationalError')
            pass
        logging.warning('Spider Opened - Pipeline')

    def close_spider(self, spider):
        self.conn.close()
        logging.warning('Spider Closed - Pipeline')

    def process_item(self, item, spider):
        self.cur.execute('''
            INSERT INTO transcripts (title, plot, transcript, url) VALUES(?,?,?,?)
        ''', (
            item.get('title'),
            item.get('plot'),
            item.get('transcript'),
            item.get('url')
        ))

        self.conn.commit()
        return item

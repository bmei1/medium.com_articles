# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.pipelines.images import ImagesPipeline
import codecs
import json
from scrapy.exporters import JsonItemExporter
import MySQLdb
import MySQLdb.cursors
from twisted.enterprise import adbapi
from ArticleSpider.models.es_types import ArticleType
from elasticsearch_dsl.connections import connections


class ArticlespiderPipeline(object):
    def process_item(self, item, spider):
        return item


# class ArticlePicPipeline(ImagesPipeline):
#     def item_completed(self, results, item, info):
#         for ok, value in results:
#             pic_file_path = value["path"]
#         item["front_pic_path"] = pic_file_path
#
#         return item


class JsonWithEncodingPipeline(object):
    # user defined json exporter
    def __init__(self):
        self.file = codecs.open('article.json', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        lines = json.dump(dict(item), ensure_ascii=False) + "\n"
        self.file.write(lines)
        return item

    def spider_closed(self, spider):
        self.file.close()


class JsonExporterPipeline(object):
    # import Scrapy's json exporter
    def __init__(self):
        self.file = open('article_export.json', 'wb')
        self.exporter = JsonItemExporter(self.file, encoding='utf-8', ensure_ascii=False)
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item


class MysqlPipeline(object):
    def __init__(self):
        self.conn = MySQLdb.connect('localhost', 'root', '123456', 'article_spider', charset="utf8mb4", use_unicode=True)
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        insert_sql = """
            INSERT INTO medium_article_data_science_tag(title, create_date, url, url_object_id, author,
            author_description, applause, content)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        self.cursor.execute(insert_sql, (item["title"], item["create_date"], item["url"], item["url_object_id"],
                                         item["author"], item["author_description"], item["applause"], item["content"]))
        self.conn.commit()


class MysqlTwistedPipeline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        dbparms = dict(
            host=settings["MYSQL_HOST"],
            db=settings["MYSQL_DBNAME"],
            user=settings["MYSQL_USER"],
            password=settings["MYSQL_PASSWORD"],
            charset='utf8mb4',
            cursorclass=MySQLdb.cursors.DictCursor,
            use_unicode=True
        )
        dbpool = adbapi.ConnectionPool("MySQLdb", **dbparms)

        return cls(dbpool)

    def process_item(self, item, spider):
        # asynchronous by twisted
        query = self.dbpool.runInteraction(self.do_insert, item)
        query.addErrback(self.handle_error, item, spider)
        return item

    def handle_error(self, failure, item, spider):
        print(failure)

    def do_insert(self, cursor, item):
        insert_sql = "insert into article_spider.medium_article_data_science_tag(title, create_date, url, url_object_id, author, \
                    author_description, applause, content) \
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        params = (item["title"], item["create_date"], item["url"], item["url_object_id"], \
                  item["author"], item["author_description"], item["applause"], item["content"])
        cursor.execute(insert_sql, params)


class ElasticsearchPipeline(object):

    # save data to ES
    def process_item(self, item, spider):
        # transfer data to ES format

        item.save_to_es()

        return item
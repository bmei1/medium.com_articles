# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

from w3lib.html import remove_tags
from ArticleSpider.models.es_types import ArticleType


from elasticsearch_dsl.connections import connections
# es = connections.create_connection(ArticleType._doc_type.using)
# es = connections.create_connection(ArticleType)


# def gen_suggests(index, info_tuple):
#     # generate search suggestion
#     used_words = set()
#     suggests = []
#     for text, weight in info_tuple:
#         if text:
#             # es analyze
#             words = es.indices.analyze(index=index, body="standard", params={'format': 'text', 'filter': ["lowercase"]})
#             analyzed_words = set([r["token"] for r in words["tokens"] if len(r["token"]) > 1])  # filter
#             new_words = analyzed_words - used_words
#         else:
#             new_words = set()
#         if new_words:
#             suggests.append({"input": list(new_words), "weight": weight})
#     return suggests


class ArticlespiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    title = scrapy.Field()
    create_date = scrapy.Field()
    url = scrapy.Field()
    url_object_id = scrapy.Field()  # encode to unique length
    author = scrapy.Field()
    author_description = scrapy.Field()
    applause = scrapy.Field()
    content = scrapy.Field()
    # front_pic_url = scrapy.Field()
    # front_pic_path = scrapy.Field()

    def save_to_es(self):
        # transfer data to ES format
        article = ArticleType()
        article.title = self['title']
        article.create_date = self['create_date']
        article.url = self['url']
        article.meta.id = self['url_object_id']
        article.author = self['author']
        article.author_description = self['author_description']
        article.applause = self['applause']
        article.content = remove_tags(self['content'])

        # article.suggest = gen_suggests((ArticleType._index), ((article.title, 10), (article.content, 2)))

        article.save()

        return

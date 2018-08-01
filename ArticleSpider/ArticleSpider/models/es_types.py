# -*- coding: utf-8 -*-

__author__ = 'bing'

from elasticsearch_dsl import DocType, Date, Mapping, Boolean, \
    analyzer, Completion, Keyword, Text, Integer
from elasticsearch_dsl.connections import connections

connections.create_connection(hosts=["localhost"])



class ArticleType(DocType):
    # medium article type

    title = Text(analyzer="standard")
    create_date = Date()
    url = Keyword()
    url_object_id = Keyword()  # encode to unique length
    author = Text(analyzer="standard")
    author_description = Text()
    applause = Integer()
    content = Text()

    class Meta:
        # mapping = Mapping('article')

        # class Index:
        index = "medium"
        doc_type = "article"


if __name__ == "__main__":
    ArticleType.init()
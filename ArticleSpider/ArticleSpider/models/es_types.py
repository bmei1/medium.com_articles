# -*- coding: utf-8 -*-

__author__ = 'bing'

from elasticsearch_dsl import DocType, Date, Mapping, Boolean, \
    analyzer, Completion, Keyword, Text, Integer, DocType
from elasticsearch_dsl.connections import connections

connections.create_connection(hosts=["localhost"])
# from elasticsearch_dsl.analysis import CustomAnalyzer as _CustomAnalyzer

# class CustomAnalyzer(_CustomAnalyzer):
#     def get_analysis_definition(self):
#         return {}


# standard = CustomAnalyzer("standard", filter=["lowercase"])


class ArticleType(DocType):
    # medium article type
    # suggest = Completion(analyzer=standard)
    title = Text(analyzer="standard")
    create_date = Date()
    url = Keyword()
    url_object_id = Keyword()  # encode to unique length
    author = Text(analyzer="standard")
    author_description = Text(analyzer="standard")
    applause = Integer()
    content = Text(analyzer="standard")

    class Meta:
         mapping = Mapping('article')

    class Index:
    # class Meta:
        name = "medium"
        doc_type = "article"


if __name__ == "__main__":
    ArticleType.init()
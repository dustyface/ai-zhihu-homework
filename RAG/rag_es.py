from elasticsearch7 import Elasticsearch, helpers
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import nltk
import re
import warnings
from .rag_extract_file import paragraphs
import os
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())

warnings.simplefilter("ignore")

nltk.download("punkt")
nltk.download("stopwords")


def to_keyword(input_string):
    """将英文文本只保留关键字?"""
    # 使用正则表达式替换所有非字母数字的字符为空格
    no_symbols = re.sub(r"[^a-zA-Z0-9\s]", " ", input_string)
    word_tokens = word_tokenize(no_symbols)
    stop_words = set(stopwords.words("english"))
    ps = PorterStemmer()
    # 去停用词，取词根
    filtered_sentence = [ps.stem(w) for w in word_tokens if not w.lower() in stop_words]
    return " ".join(filtered_sentence)


# 知乎提供了一个远程的Elasticsearch服务，可以直接使用
es_host = os.getenv("ZHIHU_ELASTICSEARCH_URL")
es_pwd = os.getenv("ZHIHU_ELASTICSEARCH_PWD")
es = Elasticsearch(hosts=[f"http://{es_host}"], http_auth=("elastic", f"{es_pwd}"))

index_name = "string_index"

if es.indices.exists(index=index_name):
    es.indices.delete(index=index_name)

es.indices.create(index=index_name)


def bulk_es(paragraphs):
    actions = [
        {
            "_index": index_name,
            "_source": {
                "keywords": to_keyword(para),
                "text": para,
            },
        }
        for para in paragraphs
    ]
    helpers.bulk(es, actions)


# 把paragh灌库
bulk_es(paragraphs)


def search(query_string, top_n=3):
    search_query = {"match": {"keywords": to_keyword(query_string)}}
    res = es.search(index=index_name, query=search_query, size=top_n)
    return [hit["_source"]["text"] for hit in res["hits"]["hits"]]

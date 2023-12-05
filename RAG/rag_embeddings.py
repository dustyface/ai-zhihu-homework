import numpy as np
from numpy import dot
from numpy.linalg import norm
from ..common import client


def cos_sim(a, b):
    """余弦距离 - 越大越相似"""
    return dot(a, b) / (norm(a) * norm(b))


def l2(a, b):
    """欧式距离 - 越小越相似"""
    x = np.asarray(a) - np.asarray(b)
    return norm(x)


# text-embedding-ada-002, 王老师推荐的目前跨语言生成文本向量最好的模型;
# 踩坑: OpenAI.embeddings.create(v1.x.x)方法要求, texts的list，元素不能是empty string或仅有whitespace的string;
def get_embeddings(texts, model="text-embedding-ada-002"):
    """封装 OpenAI的Embedding API"""
    response = client.embeddings.create(input=texts, model=model)
    return [x.embedding for x in response.data]

from ..common import client


# text-embedding-ada-002, 王老师推荐的目前跨语言生成文本向量最好的模型;
# 踩坑: OpenAI.embeddings.create(v1.x.x)方法要求, texts的list，元素不能是empty string或仅有whitespace的string;
def get_embeddings(texts, model="text-embedding-ada-002"):
    """封装 OpenAI的Embedding API"""
    response = client.embeddings.create(input=texts, model=model)
    return [x.embedding for x in response.data]

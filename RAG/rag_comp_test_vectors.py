from .rag_embeddings import get_embeddings, cos_sim, l2


test_query = ["测试文本"]
vec = get_embeddings(test_query)[0]
print("test_query dimension = ", len(vec))

query = "国际争端"
documents = [
    "联合国就苏丹达尔富尔地区大规模暴力事件发出警告",
    "土耳其、芬兰、瑞典与北约代表将继续就瑞典“入约”问题进行谈判",
    "日本岐阜市陆上自卫队射击场内发生枪击事件 3人受伤",
    "国家游泳中心（水立方）：恢复游泳、嬉水乐园等水上项目运营",
    "我国首次在空间站开展舱外辐射生物学暴露实验",
]

# test_query文本只有一行，get_embeddings返回list中的第一个元素，
# 对应的即是第一行文本的embedding向量值; 该向量值是一个有1536维的list;
query_vec = get_embeddings([query])[0]
doc_vecs = get_embeddings(documents)
print("doc_vecs=", len(doc_vecs))

# 余弦距离比较
print("Consine distance")
print(cos_sim(query_vec, query_vec))
# 和doc_vecs的每一个embedding相比
for vec in doc_vecs:
    print("doc_vec's dimension = ", len(vec))
    print(cos_sim(query_vec, vec))

# 欧式距离比较
print("Eucliden distance")
print(l2(query_vec, query_vec))
for vec in doc_vecs:
    print(l2(query_vec, vec))

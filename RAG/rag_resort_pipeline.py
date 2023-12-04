from sentence_transformers import CrossEncoder
from .rag_common import (
    extract_text_from_pdf,
    MyVectorDBConnector,
    RAG_Bot,
)
from .rag_embeddings import get_embeddings
from ..common import get_completion


paragraphs = extract_text_from_pdf(
    "zhihu_ai_homework/RAG/llama2-test-1-4.pdf", min_line_length=10
)
paragraphs = [p for p in paragraphs if p.strip()]

user_query = "how safe is Llama 2?"
vector_db = MyVectorDBConnector("demo", get_embeddings)
vector_db.add_document(paragraphs)

# search的召回条目，设置为5条;
search_result = vector_db.search(user_query, 2)

# 不使用重排序的RAG
rag_bot = RAG_Bot(vector_db, get_completion)
# reponse_without_resort = rag_bot.chat(user_query)
# print("=== response_without_resort ===")
# print(reponse_without_resort)

model = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2", max_length=512)

scores = model.predict([(user_query, doc) for doc in search_result["documents"][0]])
sorted_list = sorted(
    zip(scores, search_result["documents"][0]), key=lambda x: x[0], reverse=True
)

# check the sorted list
for score, doc in sorted_list:
    print(str(score) + "\t" + doc)
sorted_search_result = [doc for score, doc in sorted_list]
# print("sorted_search_result = ", sorted_search_result)

response_with_resort = rag_bot.chat(user_query, search_doc=sorted_search_result)
print("=== response_with_resort ===")
print(response_with_resort)

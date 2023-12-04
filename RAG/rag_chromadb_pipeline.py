from .rag_common import (
    extract_text_from_pdf,
    MyVectorDBConnector,
    RAG_Bot,
)
from ..common import get_completion
from .rag_embeddings import get_embeddings

paragraphs = extract_text_from_pdf(
    "zhihu_ai_homework/RAG/llama2-test-1-4.pdf", min_line_length=10
)
# 详见rag_embeddings.py get_embeddings()的注释
# 应该在add_document外部，进行filtering, 因为chromadb的collection.add()方法要求，embeddings, documents, ids必须相匹配；
paragraphs = list(filter(lambda x: x.strip(), paragraphs))

vector_db = MyVectorDBConnector("demo", get_embeddings)
vector_db.add_document(paragraphs)

user_query = "Llama 2 有多少参数？"  # RAG的版本，可以正确回答出问题答案
user_query = "Llama 2 有可对话的版本吗?"  # RAG的版本，可以正确回答出问题答案

# 以下2个prompt，输出的结果不同
# 经比较可以看到，英语版本和中文版本，vector db返回的与之匹配相似度的前2个文本是不同的，
# 即在人类看来，中英文的语义是近似的，但vector db比较之后认为的与之相似的语义结果是不一样的;
# 另外，英文版的结果，OpenAI直接给出了肯定答案，说明了训练数据里的差异
user_query = "can Llama 2 be used on commercial purpose?"  # 这个英文问题，却可以回答出正确答案~
user_query = "Llama 2 有可商用的版本吗?"  # 由于切割粒度的问题，无法回答出正确答案；


# 不使用vector db RAG，直接问gpt-3.5-turbo
response_without_rag = get_completion(user_query)
print("=== response_without_rag ===")
print(response_without_rag)

# 使用chromadb RAG
rag_bot = RAG_Bot(vector_db, get_completion)
response = rag_bot.chat(user_query)
print("=== response with rag ===")
print(response)

from .rag_common import extract_text_from_pdf, build_prompt, prompt_template
from ..common import get_completion
import chromadb
from chromadb.config import Settings
from .rag_embeddings import get_embeddings


class MyVectorDBConnector:
    def __init__(self, collection_name, embedding_fn):
        chroma_client = chromadb.Client(Settings(allow_reset=True))
        # 实际上，不需要每次都reset；
        chroma_client.reset()
        self.collection = chroma_client.get_or_create_collection(name="demo")
        self.embedding_fn = embedding_fn

    def add_document(self, documents, metadata={}):
        """把text embeddings和文档灌入到collection中"""
        self.collection.add(
            embeddings=self.embedding_fn(documents),
            documents=documents,
            ids=[f"id{i}" for i in range(len(documents))],
        )

    def search(self, query, top_n):
        """检索向量数据库"""
        result = self.collection.query(
            query_embeddings=self.embedding_fn([query]), n_results=top_n
        )
        return result


paragraphs = extract_text_from_pdf(
    "zhihu_ai_homework/RAG/llama2-test-1-4.pdf", min_line_length=10
)
# 详见rag_embeddings.py get_embeddings()的注释
# 应该在add_document外部，进行filtering, 因为chromadb的collection.add()方法要求，embeddings, documents, ids必须相匹配；
paragraphs = list(filter(lambda x: x.strip(), paragraphs))

vector_db = MyVectorDBConnector("demo", get_embeddings)
vector_db.add_document(paragraphs)

user_query = "Llama 2 有多少参数？"
user_query = "Llama 2 有可对话的版本吗?"

search_result = vector_db.search(user_query, 3)

print("=== search_result ===")
distances = search_result["distances"][0]
documents = search_result["documents"][0]
for k in range(len(distances)):
    print(f"distance={distances[k]}, document={documents[k]}")

prompt = build_prompt(
    prompt_template, info=search_result["documents"][0], query=user_query
)

# 不使用vector db RAG，直接问gpt-3.5-turbo
response_without_rag = get_completion(user_query)
print("=== response_without_rag ===")
print(response_without_rag)

# 使用chromadb RAG
response = get_completion(prompt)
print("=== response with rag ===")
print(response)

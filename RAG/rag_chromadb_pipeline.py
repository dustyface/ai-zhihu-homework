from .rag_common import extract_text_from_pdf
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
# paragraphs = list(filter(lambda x: x.strip(), paragraphs))

vector_db = MyVectorDBConnector("demo", get_embeddings)
vector_db.add_document(paragraphs)

user_query = "Llama 2 有多少参数？"
search_result = vector_db.search(user_query, 3)
print("=== search_result ===")
print(search_result)

from .rag_common import extract_text_from_pdf, split_text, MyVectorDBConnector, RAG_Bot
from ..common import get_completion
from .rag_embeddings import get_embeddings

paragraphs = extract_text_from_pdf(
    "zhihu_ai_homework/RAG/llama2-test-1-4.pdf", min_line_length=10
)

paragraphs = [x for x in paragraphs if x.strip()]

chunks = split_text(paragraphs)

vector_db = MyVectorDBConnector("demo", get_embeddings)
# 用更细粒度的chunk灌库
vector_db.add_document(chunks)

user_query = "Llama 2有可商用的版本吗?"

response_without_rag = get_completion(user_query)
print("=== response_without_rag ===")
print("response_without_rag = ", response_without_rag)

rag_bot = RAG_Bot(vector_db, get_completion)
response = rag_bot.chat(user_query)
print("=== response with rag ===")
print("response = ", response)

from langchain.embeddings.openai import OpenAIEmbeddings
from .langchain_common import (
    extract_text_by_page,
    get_paragraph,
    get_lines_from_pages,
    get_paragraphs_bylangchain,
)
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI

pages = extract_text_by_page("zhihu_ai_homework/LangChain/llama2-test-1-4.pdf")

texts2 = get_paragraphs_bylangchain(pages)
texts = get_paragraph(get_lines_from_pages(pages), min_line_length=15)
# print("=== 检查切割的paragraph ===")
# print("texts2=")
# for t2 in texts2:
#     print(t2)

# print("=== texts ===")
# for t in texts:
#     print('"' + t + '"\n')

embeddings = OpenAIEmbeddings()

# 使用langchain的text_splitter切分出来的段, text2是list[Document]类型;
# text_splitter有它自己切割段落的逻辑，检查结果，比实际段落切割更细，不到一个自然段就形成了一个document
db = Chroma.from_documents(texts2, embeddings)

# texts是list[str]，还不能直接使用它在langchain的Chroma.from_documents中测试;
# db = Chroma.from_documents(texts, embeddings)

qa_chain = RetrievalQA.from_chain_type(
    llm=OpenAI(temperature=0),
    retriever=db.as_retriever(),
)

query = "Llama 2 有多少参数？"
response = qa_chain.run(query)
print(response)

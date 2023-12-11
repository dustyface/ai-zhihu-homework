from langchain.prompts import ChatPromptTemplate
from langchain.embeddings import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.schema.output_parser import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough
from langchain.vectorstores import Chroma

vectorstore = Chroma.from_texts(
    [
        "Sam Altman 是OpenAI的CEO",
        "Sam Altman 被OPenAI解雇了",
        "Sam Altman 被复职了",
    ],
    embedding=OpenAIEmbeddings(),
)
retriever = vectorstore.as_retriever()
template = """Answer the question based only on the following context:
{context}

Question: {question}
"""
prompt = ChatPromptTemplate.from_template(template)
model = ChatOpenAI(temperature=0)

# retriver 是从chromadb中查出的信息
# StrOutputParser(): 由于context: retriever的限制，输出是结构体，StrOutputParser的作用是把字符串从结构体中取出
retriever_chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | model
    | StrOutputParser()
)

output = retriever_chain.invoke("OpenAI的CEO是谁?")
print("output=", output)

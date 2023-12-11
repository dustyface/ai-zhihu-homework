from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnablePassthrough
from pydantic import BaseModel, Field, validator
from langchain.output_parsers import PydanticOutputParser
from typing import Optional
from enum import Enum


class SortEnum(str, Enum):
    data = "data"
    price = "price"


class OrderingEnum(str, Enum):
    ascend = "ascend"
    descend = "descend"

# 回顾，第2课中，用自己写Prompt控制输出，使用Pydantic就简化了这个环节
# 定义Pydantic的子类，用于描述输出的格式
class Semantics(BaseModel):
    name: Optional[str] = Field(description="流量包名称", default=None)
    price_lower: Optional[int] = Field(description="价格下限", default=None)
    price_upper: Optional[int] = Field(description="价格上限", default=None)
    data_lower: Optional[int] = Field(description="流量下限", default=None)
    data_upper: Optional[int] = Field(description="流量上限", default=None)
    sort_by: Optional[SortEnum] = Field(description="按价格或流量排序", default=None)
    ordering: Optional[OrderingEnum] = Field(description="升序或降序", default=None)


# parser 和 promptTemplate的连接，是通过partial()
parser = PydanticOutputParser(pydantic_object=Semantics)
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "将用户的输入解析成JSON表示。输出格式如下：\n{format_instructions}\n不要输出未提及的字段。"),
        ("user", "{query}"),
    ]
).partial(format_instructions=parser.get_format_instructions())
model = ChatOpenAI(temperature=0)

# LCEL expression
# 对比langchain_outputparser.py, LCEL的形式，更加简洁
runnable = {"query": RunnablePassthrough()} | prompt | model | parser

print(runnable.invoke("不超过100元的流量大的套餐有哪些?"))

from langchain.prompts import (
    PromptTemplate,
)
from langchain.chat_models import ChatOpenAI
from langchain.output_parsers import PydanticOutputParser
from .langchain_common import Date

model_name = "gpt-4"
temperature = 0
chat_model = ChatOpenAI(model_name=model_name, temperature=temperature)

# 注意，声明parser变量的方法(可以直接用传参给某个属性)
parser = PydanticOutputParser(pydantic_object=Date)
template = """
提取用户输入中的日期。
{format_instructions}
用户输入:
{query}
"""

# 这是PromptTemplate的另一种形式, 注意partial_variables是从OutputParser中获取的信息;
prompt = PromptTemplate(
    template=template,
    input_variables=["query"],
    # 直接从 OutputParser 中获取输出描述, 并对模板的变量预先赋值
    partial_variables={"format_instructions": parser.get_format_instructions()},
)

# PromptTemplate的使用的基本套路是3个步骤
# 1. 从PromptTemplate获得prompt实例, 形式上有2种方法:
# - PromptTemplate.from_template,
# - PromptTemplate(template=, input_variables=, partial_variables=); 其中partial_variable是接受从parser实例的get_format_instruction()返回的变量;
# 2. 用prompt实例的format() / format_prompt(), 传入自定义变量,得到PromptValue类型;
# 3. 调用PromptValue.to_messages(), 得到OpenAI的输入格式;

user_query = "2023年四月6日天气晴..."
model_input = prompt.format_prompt(query=user_query)

# 和OpenAI交互
output = chat_model(model_input.to_messages())
print("=== ouput ===")
print("output=", output)
print("===Parsed===")
# parser.parse是把dict转成Pydantic类型对象(最后的过程会调用Date的@validator)
cmd = parser.parse(output.content)
print("cmd=", cmd)

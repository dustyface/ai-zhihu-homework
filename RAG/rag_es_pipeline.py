from .rag_es import search
from ..common import get_completion
from .rag_common import build_prompt, prompt_template

user_query = "how many parameters does llama 2 have?"
user_query = "can llama 2 be used for comercial purpose?"

# RAG ES Pipeline 流程上只需4步:

# 1. 准备ES库，指定知识库文档(e.g. llama2 pdf), 灌库;
# 2. 检索(准备的灌库工作已经在rag_es中完成)；

# 注意:
# 第2个参数选择返回2条数据时，无法根据知识库search结果查到目标答案,
# 选择返回5条时，LLM可以查到答案
search_result = search(user_query, 5)
print("=== search_result ===")
for res in search_result:
    print("search_result=", res)

# 3. 构造prompt, 把搜索到的知识的结果，填充到prompt中
prompt = build_prompt(prompt_template, info=search_result, query=user_query)

print("=== prompt ===")
print(prompt)
# 4. 和LLM交互，获得结果；
response = get_completion(prompt)
print("=== response ===")
print(response)

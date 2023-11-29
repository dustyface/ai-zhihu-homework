import json
from ..common import get_completion_with_session, fill_context_in_session, session

context = {
    "role": "system",
    "content": """
你是一个手机流量套餐的客服代表，你叫小瓜。可以帮助用户选择最合适的流量套餐产品。可以选择的套餐包括:
经济套餐，月费50元，10G流量；
畅游套餐，月费180元，100G流量；
无限套餐，月费300元，1000G流量；
校园套餐，月费150元，200G流量，仅限在校生
""",
}

fill_context_in_session(context)
get_completion_with_session("有没有土豪套餐?", "gpt-3.5-turbo", True)
get_completion_with_session("多少钱?")
get_completion_with_session("给我办一个")

"""
总结纯OpenAI实现客服对话选择套餐的实现与NLU+DST+Policy+OpenAI的区别:

- 纯OpenAI接口的方式，多轮交互返回的是自然语言的非结构性的内容，也没有语气，稳定性等控制，如果需要使用其中的数据，需要自己解析；
- NLU+DST+Policy + OpenAI LLM的方式，在对话2轮的过程中(可以变为多轮)，从NLU的输出到DST，到后续的各个环节，手撸代码来清洗转换数据，保持了结构化的数据；这可能这种流程中，对接各个模块所需要的方式;
"""
print(json.dumps(session, indent=4, ensure_ascii=False))
session.clear()

from math import *
from ..common import get_completion_through_dict, func_calling_call_func

prompt = "从1加到10"
# prompt = "3的平方根成以2在开方"

messages = [
    {"role": "system", "content": "你是一个数学家，你可以计算任何算式"},
    {"role": "user", "content": prompt},
]
# 踩坑:
# - tools = ([],)，vscode的black formatter会把`[], `自动格式化为(), 导致OpenAI api回复认为是一个空的tool，出错;
# - tools = [{}],是list, tools = ([],) 是tuple，元素是list, 其中的后置的,号是必须的，否则tuple就只有一个元素了;
tools = [
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "计算一个数学表达式的值",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "a methematical expression in python grammar",
                    }
                },
            },
        },
    }
]

response = get_completion_through_dict(
    messages=messages,
    model="gpt-3.5-turbo-1106",
    seed=1024,
    tools=tools,
    # debug=True,
)


def calculate(**kwargs):
    print("calculate()=", kwargs)
    expression = kwargs["expression"]
    return eval(expression)


response_message = response.choices[0].message
print("=== GPT回复 ===")
print("response=", response)

callback = {"calculate": calculate}
final_response = func_calling_call_func(
    response_message, messages, tools, callback, "calculate"
)
print("=== 最终回复 ===")
print("final_response=", final_response.choices[0].message.content)

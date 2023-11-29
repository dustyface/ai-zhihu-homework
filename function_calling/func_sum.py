from math import *
import json
from ..common import get_completion_through_dict

prompt = "Tell me the sum of 1, 2, 3, 4, 5, 6, 7, 8, 9, 10"
prompt = "桌上有 2 个苹果，四个桃子和 3 本书，一共有几个水果？"
prompt = "1+2+3...+99+100"

# Tools 里没有定义乘法，会怎样？
# 需求要求是乘法，LLM似乎没有正确理解app提供的tools的function定义中没有具备乘法的功能。它的第一轮回复，tool_calls仍然是提取了1024的参数, tool_calls[0].function.name是sum; 但是最终，尽管第2轮告知LLM是错误的2048的结果，LLM仍然会正确回答1024*1024的结果,但用时非常长，有时会
# prompt = "1024 乘以 1024 是多少？"

# 不需要算加法，会怎样？
# LLM的第一轮回复的tool_calls=None, 说明它可以判断出无需执行function calling的流程，直接给出了答案(太阳从东边升起)
# prompt = "太阳从哪边升起？"

messages = [
    {"role": "system", "content": "你是一个小学数学老师，你要教学生加法"},
    {"role": "user", "content": prompt},
]
response = get_completion_through_dict(
    model="gpt-3.5-turbo-1106",  # 本次课程的例子，目前只有2个大模型支持： gpt-3.5-turbo-1106, gpt-4-1106-preview
    messages=messages,
    temperature=0.7,
    tools=[
        {
            "type": "function",
            "function": {
                "name": "sum",  # 其实这个function的名字是非关键性的;
                "description": "加法器, 计算一组数的和",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "numbers": {"type": "array", "items": {"type": "number"}}
                    },
                },
            },
        }
    ],
    debug=True,
)

response_message = response.choices[0].message

# 参考：https://github.com/openai/openai-python/issues/703
# 是为解决v1.1.1 的400 bug; 后续版本不再需要;
# if response_message.content is None:
# response_message.content = ""
messages.append(response_message)  # 把大模型的回复加入到对话历史中(必须注意的关键一步)

# 这时候，LLM会告知app如何调用这个function calling的参数;
print("=== GPT回复 ===")
print("response=", response.choices[0].message.content)

if response_message.tool_calls is not None:
    tool_call = response_message.tool_calls[0]
    if tool_call.function.name == "sum":
        args = json.loads(tool_call.function.arguments)
        print("args=", args)
        result = sum(args["numbers"])
        print("result=", result)

        messages.append(
            {
                "tool_call_id": tool_call.id,
                "role": "tool",
                "name": "sum",
                "content": str(result),  # 数值result必须转成字符串；
            }
        )
    # 最后的和LLM的对话，可以没有tools属性;
    # 踩坑:
    # 把第一次对话LLM对话的assistant role的内容，加到messages历史信息中十分关键;
    # 缺少该信息，则会报: messages with role 'tool' must be a response to a preceding message with 'tool_calls'."错误;
    final_response = get_completion_through_dict(
        messages=messages, model="gpt-3.5-turbo-1106", temperature=0.7, debug=True
    )
    print("=== 最终回复 ===")
    print("final_response=", final_response.choices[0].message.content)

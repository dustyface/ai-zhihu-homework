import json
from ..common import get_completion_through_dict, func_calling_call_func

prompt = "帮我寄给王卓然，地址是北京市朝阳区亮马桥外交办公大楼，电话13012345678"
messages = [
    {"role": "system", "content": "你是一个联系人录入员"},
    {"role": "user", "content": prompt},
]

tools = [
    {
        "type": "function",
        "function": {
            "name": "add_contact",
            "description": "添加联系人",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "联系人姓名"},
                    "address": {"type": "string", "description": "联系人地址"},
                    "tel": {"type": "string", "description": "联系人电话"},
                },
                "required": ["name", "address", "tel"],
            },
        },
    }
]

response = get_completion_through_dict(
    messages=messages,
    tools=tools,
    model="gpt-3.5-turbo-1106",
    seed=1024,
)
print("=== GPT 回复 ===")
print("response=", response)
args = json.loads(response.choices[0].message.tool_calls[0].function.arguments)
print("args=", args)

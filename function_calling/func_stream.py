from ..common import get_completion_through_dict

prompt = "1 + 2 + 3"

messages = [
    {"role": "system", "content": "你是一个小学数学老师, 你要教学生加法"},
    {"role": "user", "content": prompt},
]
tools = [
    {
        "type": "function",
        "function": {
            "name": "sum",
            "description": "计算一组数的加和",
            "parameters": {
                "type": "object",
                "properties": {
                    "numbers": {"type": "array", "items": {"type": "number"}}
                },
            },
        },
    }
]

response = get_completion_through_dict(
    model="gpt-3.5-turbo-1106", messages=messages, tools=tools, stream=True, debug=True
)

print("=== GPT回复 ===")
print("response=", response)

for msg in response:
    print("msg=", msg)
    delta = msg.choices[0].delta

from ..common import get_completion
from ..prompt_text import instruction, output_format

# user_input = input("我是一个流量套餐助手，请输入您想申办的流量套餐:")
user_input = "办个100G的套餐"
# user_input = "我要无限量套餐"
user_input = "有没有便宜的套餐"

prompt = f"""
{instruction}

{output_format}

用户输入:
{user_input}
"""

response = get_completion(prompt)
print(response)

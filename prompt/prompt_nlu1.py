from ..common import get_completion
from ..prompt_text import instruction

# user_input = input("我是一个流量套餐助手，请输入您想申办的流量套餐:")
user_input = "办个100G的套餐"

prompt = f"""
{instruction}

用户输入:
{user_input}
"""

response = get_completion(prompt)
# 虽然temperature=0, 但是answer还是有一些随机性的, 文字不会完全相同;
print(response)

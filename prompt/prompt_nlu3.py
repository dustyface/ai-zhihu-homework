from ..common import get_completion
from ..prompt_text import instruction, output_format, examples

# user_input = input("我是一个流量套餐助手，请输入您想申办的流量套餐:")
# user_input = "办个100G的套餐"
# user_input = "我要无限量套餐"
# user_input = "有没有便宜的套餐"

# 输出了json，monthly_price <= 200, monthly_data > 无上限; 无上限是从例子里侧的；
# 可能和例子中不限流量的描述相关;
user_input = "200元以下，流量大的套餐有啥"

# 推测是10G是经济型套餐;
# user_input = "你说那个10G的套餐，叫啥名字"

prompt = f"""
{instruction}

{output_format}

{examples}

用户输入:
{user_input}
"""

response = get_completion(prompt)
print(response)

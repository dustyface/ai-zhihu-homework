from ..prompt_text import examples, instruction, output_format
from ..common import get_completion

# example 换成了客服与用户的对话；
context_example = f"""
{examples}

客服：有什么可以帮您
用户：100G套餐有什么

{{"data":{{"operator":">=","value":100}}}}

客服：有什么可以帮您
用户：100G套餐有什么
客服：我们现在有无限套餐，不限流量，月费300元
用户：太贵了，有200元以内的不

{{"data":{{"operator":">=","value":100}},"price":{{"operator":"<=","value":200}}}}

客服：有什么可以帮您
用户：便宜的套餐有什么
客服：我们现在有经济套餐，每月50元，10G流量
用户：100G以上的有什么

{{"data":{{"operator":">=","value":100}},"sort":{{"ordering": "ascend","value"="price"}}}}

客服：有什么可以帮您
用户：100G以上的套餐有什么
客服：我们现在有畅游套餐，流量100G，月费180元
用户：流量最多的呢

{{"sort":{{"ordering": "descend","value"="data"}},"data":{{"operator":">=","value":100}}}}
"""

# user_input = input("我是一个流量套餐助手，请输入您想申办的流量套餐:")
# user_input = "办个100G的套餐"
# user_input = "我要无限量套餐"
# user_input = "有没有便宜的套餐"

# 输出了json，price <= 200, data > 无上限; 无上限是从例子里侧的；
# 可能和例子中不限流量的描述相关;
user_input = "200元以下，流量大的套餐有啥"

# 推测是10G是经济型套餐;
# user_input = "你说那个10G的套餐，叫啥名字"

context = f"""
客服: 有什么可以帮您
用户: 有什么10G以上的套餐
客服: 我们现在有畅游套餐和无限套餐，您有什么价格倾向？
用户: {user_input}
"""

prompt = f"""
{instruction}

{output_format}

{context_example}

{context}
"""

get_completion(prompt)

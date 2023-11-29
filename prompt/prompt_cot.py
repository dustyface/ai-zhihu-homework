from ..common import get_completion

instruction = """
给定一段用户与手机流量套餐客服的对话，
你的任务是判断客服介绍产品信息的准确性：

当向用户介绍流量套餐产品时，客服人员必须准确提及产品名称、月费价格和月流量总量 上述信息缺失一项或多项，或信息与实时不符，都算信息不准确

已知产品包括：

经济套餐：月费50元，月流量10G
畅游套餐：月费180元，月流量100G
无限套餐：月费300元，月流量1000G
校园套餐：月费150元，月流量200G，限在校学生办理
"""

# 输出描述
output_format = """
以JSON格式输出。
如果信息准确，输出：{"accurate":true}
如果信息不准确，输出：{"accurate":false}
"""

context = """
用户：你们有什么流量大的套餐
客服：您好，我们现在正在推广无限套餐，每月300元就可以享受1000G流量，您感兴趣吗
"""

context2 = """
用户：有什么便宜的流量套餐
客服：您好，我们有个经济型套餐，50元每月
"""

context3 = """
用户：流量大的套餐有什么
客服：我们推荐畅游套餐，180元每月，100G流量，大多数人都够用的
用户：学生有什么优惠吗
客服：如果是在校生的话，可以办校园套餐，150元每月，含200G流量，比非学生的畅游套餐便宜流量还多
"""

cot = """
请一步一步分析以下对话
"""


def get_prompt(use_cot):
    return f"""
    {instruction}

    {output_format}

    {cot if use_cot else ""}

    对话记录：
    {context3}
    """


# CoT
# 不使用思维链，问LLM，查看判断结果;
response = get_completion(get_prompt(False))
print(response)
print("===")
# 使用思维链，问LLM，查看判断结果;
response = get_completion(get_prompt(True))
print(response)

# Self-consistency
for i in range(5):
    prompt = get_prompt(True)
    print(f"{i + 1}.")
    response = get_completion(prompt, temperature=0.8)
    print(response)

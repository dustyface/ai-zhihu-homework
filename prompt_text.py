instruction = """
你的任务是识别用户对手机流量套餐产品的选择条件。
每种流量套餐产品包含3个属性: 名称(name), 月费价格(price), 月流量(data)。
根据用户的输入，识别用户在上述3种属性上的倾向。
"""

# 输出格式的描述，虽然比较多，但描述是相对不严格的；
# - name, price, data字段，并没有被要求必须同时都存在;
# - LLM可以自己从字面意思推断出价格方面的大小排序，e.g. 经济套餐，它可以理解;
output_format = """
请以JSON格式输出。
1. name字段的取值，应为string类型，取值必须为以下之一: 经济套餐, 畅游套餐, 无限套餐, 校园套餐, 或null;
2. price字段, 取值范围为一个结构体或null; 结构体包含2个字段:
    2.1 operator, string类型, 取值范围: "<=", ">", "==";
    2.2 value, int类型;
3. data字段, 取值范围为一个结构体或null; 结构体包含2个字段:
    3.1 operator, string类型, 取值范围: "<=", ">", "==";
    3.2 value, int类型或string类型， string类型的值只能是"无上限";
4. 用户意图可以依据price和data排序， 用sort字段标识，取值为一个结构体
    4.1 结构体中以ordering="descend"表示降序排序,以value存储待排序字段；
    4.2 结构体中以ordering="ascend"表示升序排序,以value存储待排序字段；

只输出用户提及的字段信息，不要猜测任何用户未直接提及的字段，不输出值为null的字段.
"""

# example 换成了客服与用户的对话；
examples = """
便宜的套餐：{"sort":{"ordering"="ascend","value"="price"}}
有没有不限流量的：{"data":{"operator":"==","value":"无上限"}}
流量大的：{"sort":{"ordering"="descend","value"="data"}}
100G以上流量的套餐最便宜的是哪个：{"sort":{"ordering"="ascend","value"="price"},"data":{"operator":">=","value":100}}
月费不超过200的：{"price":{"operator":"<=","value":200}}
就要月费180那个套餐：{"price":{"operator":"==","value":180}}
经济套餐：{"name":"经济套餐"}
"""

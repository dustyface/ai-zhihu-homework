import json
from ..common import get_completion


def performance_analyzer(text):
    """
    返回给定参数候选人的3方面素质的打分，以json形式返回
    @param: text, 对候选人在速度，耐力，力量表现的描述；
    """
    prompt = f"{text}请根据以上成绩，分析候选人在速度、耐力、力量三方面素质的分档。分档包括：强（3），中（2），弱（1）三档。\
                \n以JSON格式输出，其中key为素质名，value为以数值表示的分档。"
    response = get_completion(prompt)
    return json.loads(response)


def possible_sports(talent, category):
    """
    给出针对某个打分强的素质适合的运动
    @param: talent, 候选人的某一个素质，如速度，耐力，力量；
    @param: category 搏击
    """
    prompt = f"需要{talent}强的{category}运动有哪些？给出10个例子，必须以array形式输出(只输出array，不需要其他内容)，确保输出能由json.loads解析"
    response = get_completion(prompt, temperature=0.8)
    return json.loads(response)


def evaluate(sport, talent, value):
    """
    分析某个sport，对tanlent的要求，LLM给出评分;
    @param: sport, 运动名称
    @param: talent, 候选人的某一个素质，如速度，耐力，力量；
    @param: value, 前面2轮对话对某一个素质的评分；
    @return: boolean, 候选人是否适合该运动
    """
    prompt = f"""
        请分析{sport}运动对{talent}素质的要求，给出3个分档：强（3），中（2），弱（1）
        输出结果格式说明:
        输出结果直接给出分析后的档位数字，只包含数字，不需要任何文字描述。如果{{sport}}对{{talent}}素质有多个分档的结果，请选择最低的一项。NO COMMENT， NO ACKNOWLEGEMENT。
"""
    response = get_completion(prompt)
    val = int(response)
    print(f"{sport}: {talent} {val} {value} {value >= val}")
    return value >= val


def report_generator(name, performance, talents, sport):
    """
    针对evaluate()求出的某个talent是否适合某个运动，让LLM构造出一段推荐语段
    """
    level = ["弱", "中", "强"]
    _talents = {k: level[v - 1] for k, v in talents.items()}
    prompt = f"已知{name}{performance}\n身体素质: {_talents}\n生成一篇{name}适合参加{sport}的分析报告。"
    response = get_completion(prompt)
    return response


name = "小明"
performance = "100米跑成绩：10.5秒，1500米跑成绩：3分20秒，铅球成绩：15米。"
category = "搏击"
talents = performance_analyzer(f"{name}的{performance}")
print("talents=", talents)
cache = set()

for k, v in talents.items():
    if v < 2:
        continue  # 这个素质不强，不用分析了; 调整为2以下不判断；
    # 列出适合素质k的10个运动;
    leafs = possible_sports(k, category)
    print("leafs=", leafs)
    for sport in leafs:
        if sport in cache:
            continue
        cache.add(sport)
        suitable = True
        for t, p in talents.items():
            if t == k:
                continue  # k项素质已经是强，不用再分析了
            if not evaluate(sport, t, p):  # 针对{t}素质，{sport}运动, 询问LLM是否合适
                suitable = False
                break
        if suitable:  # 3项素质都合适，生成报告
            report = report_generator(name, performance, talents, sport)
            print("report=", report)

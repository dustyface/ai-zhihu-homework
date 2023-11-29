from ..common import DialogManager

# 第2轮对话，user获取第一轮的信息之后，询问LLM的模板
prompt_templates = {
    "recommand": "用户说：__INPUT__ \n\n向用户介绍如下产品：__NAME__，月费__PRICE__元，每月流量__DATA__G。",
    "not_found": "用户说：__INPUT__ \n\n没有找到满足__PRICE__元价位__DATA__G流量的产品，询问用户是否有其他选择倾向。",
}

extra_constraint = (
    "尽量口语一些，亲切一些；不用说'抱歉'; 直接给出回答，不要在前面加'小瓜说'; NO COMMENT. NO ACKNOWLEDGEMENTS"
)

prompt_templates = {k: v + extra_constraint for k, v in prompt_templates.items()}

# 目前，DialogManager.run的流程，只管理2轮的对话；
# e.g.
# 第一轮问LLM "有没有200元以下的套餐", dm会把答复存在内部的state中，
# 再把答复中的data, price, 以及用户第一轮输入等信息插入到prompt_templates中, 再指导LLM做出第2轮回答;
#
# 02-prompt课件中，还有增加ext对话信息，e.g.用统一格式回复用户，推荐话术，省略；
dm = DialogManager(prompt_templates)
response = dm.run("有没有200元以下的套餐")

print("response=")
print(response)

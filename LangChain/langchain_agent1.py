# from langchain import SerpAPIWrapper
from langchain.utilities import SerpAPIWrapper
from langchain.tools import Tool, tool
import calendar
import dateutil.parser as parser
from datetime import date
from langchain.chat_models import ChatOpenAI
from langchain.agents import AgentType
from langchain.agents import initialize_agent
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

# 1. 定义tools
# 这是 Google search interface
search = SerpAPIWrapper()
tools = [
    # 从一个函数生成tool
    Tool.from_function(
        func=search.run,
        name="search",
        description="useful for when you need to answer questions about current event",
    )
]


# 利用decorator @tool生成tool
@tool("weekday")
def weekday(date_str: str) -> str:
    """Convert date to weekday name"""
    d = parser.parse(date_str)
    return calendar.day_name[d.weekday()]


tools += [weekday]

# 2. 指定智能体类型 & 初始化智能体, 执行
llm = ChatOpenAI(model="gpt-4", temperature=0)
agent = initialize_agent(
    tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True
)
user_query = "周杰伦生日那天是星期几?"
agent.run(user_query)

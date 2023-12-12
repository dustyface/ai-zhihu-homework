from langchain.utilities import SerpAPIWrapper

# from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.agents import initialize_agent, Tool
from langchain.agents import AgentType

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

llm = ChatOpenAI(model="gpt-4", temperature=0)
# llm = OpenAI(temperature=0)  # 续写model，本例无法适用
search = SerpAPIWrapper()

tools = [
    Tool(
        name="Intermediate Answer",
        func=search.run,
        description="useful for when you need to ask with search",
    )
]


# bugfix: 暂时用这个办法，让第一步predict的结果可以被跳过，连接到下一步执行;
# 但未解决根本问题
# def handle_parsing_errors(error) -> str:
#     aftercolon = str(error).split(":")[-1].strip()
#     if aftercolon.startswith("Yes"):
#         # return AgentAction("Intermediate Answer", aftercolon, error)
#         return aftercolon
#     return str(error)


self_ask_with_search = initialize_agent(
    tools,
    llm,
    agent=AgentType.SELF_ASK_WITH_SEARCH,
    verbose=True,
    # handle_parsing_errors=handle_parsing_errors,
    handle_parsing_errors=True,
)
self_ask_with_search.run("吴京的老婆的主持过哪些节目")

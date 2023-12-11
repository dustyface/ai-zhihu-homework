from langchain.utilities import SerpAPIWrapper
from langchain.llms import OpenAI
from langchain.agents import initialize_agent, Tool
from langchain.agents import AgentType

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

llm = OpenAI(temperature=0)
search = SerpAPIWrapper()

tools = [
    Tool(
        name="Intermediate Answer",
        func=search.run,
        description="useful for when you need to ask with search",
    )
]

self_ask_with_search = initialize_agent(
    tools,
    llm,
    agent=AgentType.SELF_ASK_WITH_SEARCH,
    verbose=True,
    handle_parsing_errors=True,
)
self_ask_with_search.run("吴京的老婆的主持过哪些节目")

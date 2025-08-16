# Import relevant functionality
from langchain.chat_models import init_chat_model
from langchain_tavily import TavilySearch
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph.state import CompiledStateGraph
from langgraph.prebuilt import create_react_agent

from agents.agents import AgentBuilder

# Default system prompt for the news agent
system_prompt = """You are a news agent. 
Your goal is to get the most relevant financial news that would relate to the potential investments our user could make.
Only restrict to news for investing in Argentina.

Only return the title of the news, and the source for it"""

class NewsAgentBuilder(AgentBuilder):

    def __init__(self) -> None:
        super().__init__()

    def build(self, **kwargs) -> CompiledStateGraph:
        # Create the agent
        memory = MemorySaver()
        model = init_chat_model("gpt-5-mini", model_provider="openai")        
        search = TavilySearch(max_results=10)
        tools = [search]
        return create_react_agent(model, tools, checkpointer=memory, prompt=system_prompt)
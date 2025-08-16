# Import relevant functionality
from langchain.chat_models import init_chat_model
from langchain_tavily import TavilySearch
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph.state import CompiledStateGraph
from langgraph.prebuilt import create_react_agent
from pydantic import BaseModel, Field

from agents.agents import AgentBuilder

# Default system prompt for the news agent
system_prompt = """You are an agent responsible for generating an investment plan for a user
THe user will explain what he wants to do, and you will also get the information about the user (location, etc)


Respond with the suggested investments in the following schema (JSON Object):
{
    "investments": [{
        "name": "Name of the investment",
        "amount": 34000,
        "percentage": 35,
        "reason": "Exaplain the reason to choose this investment"
    }]
}
"""

class InvestmentAmount(BaseModel):
    amount: float = Field(description='The amount to invest')
    percentage: float = Field(description='The percent to invest')
    name: str = Field(description='The name of this investment')
    reason: str = Field(description='The reason to include this investment')
    explanation: str | None = Field(default=None)

class AgentResponse(BaseModel):
    investments: list[InvestmentAmount] = Field(description='List of the investments')

class InvestmentPlannerAgent(AgentBuilder):

    def __init__(self) -> None:
        super().__init__()

    def build(self, **kwargs) -> CompiledStateGraph:
        # Create the agent
        memory = MemorySaver()
        model = init_chat_model("gpt-5-mini", model_provider="openai")        
        tools = []
        return create_react_agent(
            model, 
            tools, 
            checkpointer=memory, 
            prompt=system_prompt,
            response_format=('Respond in this format', AgentResponse)
        )
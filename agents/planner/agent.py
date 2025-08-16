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
        "risk": 1,
        "ease_of_use": 3
    }]
}

The meaning of the fields are:
- Name: the name of the asset
- Amount: The amount to invest in the asset
- Percentage: What percentage of the total amount we're investing here
- Reason: The reason to invest in this asset
- Risk: A val between 1 and 10 to identify the risk
- Ease of use: How easy is it for the user to invest in the asset  Value between 1 and 10  This in important, since we'll be advicing the user to start by investing a little bit of its money on the one with the lowest value
"""

class InvestmentAmount(BaseModel):
    amount: float = Field(description='The amount to invest')
    percentage: float = Field(description='The percent to invest')
    name: str = Field(description='The name of this investment')
    reason: str = Field(description='The reason to include this investment')
    explanation: str | None = Field(default=None)
    risk: int = Field(description='A val between 1 and 10 describing the risk')
    ease_of_use: int = Field('A val between 1 and 10 that describes the ease of use')

class AgentResponse(BaseModel):
    investments: list[InvestmentAmount] = Field(description='List of the investments')

class InvestmentPlannerAgent(AgentBuilder):

    def __init__(self, model) -> None:
        super().__init__(model)

    def build(self, **kwargs) -> CompiledStateGraph:
        # Create the agent
        memory = MemorySaver()
        tools = []
        return create_react_agent(
            self.model, 
            tools, 
            checkpointer=memory, 
            prompt=system_prompt,
            response_format=('Respond in this format', AgentResponse)
        )
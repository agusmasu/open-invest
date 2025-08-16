from langchain.chat_models import init_chat_model
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph.state import CompiledStateGraph
from langgraph.prebuilt import create_react_agent
from agents.agents import AgentBuilder


system_prompt = """
    You are an agent responsible of explaining an investment to someone who's not familiar with investments
    You are given an investment idea, and you will explain what does the investment mean in a short sentence/paragraph.

    This needs to be for someone who is not in the investment world.

    ONLY include the explanation in your response.
"""

class ExplainingAgent(AgentBuilder):
    def build(self, **kwargs) -> CompiledStateGraph:
        # Create the agent
        memory = MemorySaver()
        model = init_chat_model("gpt-5-mini", model_provider="openai")        
        tools = []
        return create_react_agent(
            model, 
            tools, 
            checkpointer=memory, 
            prompt=system_prompt
        )

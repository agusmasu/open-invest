from langchain.chat_models import init_chat_model
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph.state import CompiledStateGraph
from langgraph.prebuilt import create_react_agent
from agents.agents import AgentBuilder

system_prompt = """
    You are an agent responsible of explaining an investment to someone who's not familiar with investments
    You are given an investment idea, and you will explain what does the investment mean in a short sentence/paragraph.

    This needs to be for someone who is not in the investment world.

    With the investment, you'll also receive something that the user likes (like a sport, or anything).
    When explaning, use an analogy with this preference of the user, so it's simpler for the user to know what each investment type represents

    ONLY include the explanation in your response.
"""

class ExplainingAgent(AgentBuilder):

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
            prompt=system_prompt
        )

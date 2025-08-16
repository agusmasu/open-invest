from abc import abstractmethod, ABC

from langgraph.graph.state import CompiledStateGraph

class AgentBuilder(ABC): 
    """Interface to build AI Agents"""

    def __init__(self, model) -> None:
        self.model = model

    @abstractmethod
    def build(self, **kwargs) -> CompiledStateGraph:
        """Build the agent and return"""
        pass
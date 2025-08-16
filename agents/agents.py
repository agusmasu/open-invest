from abc import abstractmethod, ABC

from langgraph.graph.state import CompiledStateGraph

class AgentBuilder(ABC): 
    """Interface to build AI Agents"""

    @abstractmethod
    def build(self, **kwargs) -> CompiledStateGraph:
        """Build the agent and return"""
        pass
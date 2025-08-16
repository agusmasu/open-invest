import json
import operator
from typing import Annotated, TypedDict
from langgraph.graph import StateGraph
from langgraph.types import Send
from pydantic import BaseModel
from agents.explainer.agent import ExplainingAgent
from agents.planner.agent import AgentResponse, InvestmentAmount, InvestmentPlannerAgent
from IPython.display import Image, display

user_context = {
    "country": "Argentina",
    "investmentProfile": "moderate",
    "user_idea": "Quiero invertir para tener un fondo para retirarme",
    "age": 28
}

class InvestmentGraphState(TypedDict):
    user_message: str
    investments: Annotated[list, operator.add]
    explained_investments: Annotated[list, operator.add]
    user_context: any

def get_investment_ideas(state: InvestmentGraphState) -> InvestmentGraphState:
    agent = InvestmentPlannerAgent().build()
    
    prompt = f"Message: {state['user_message']}. User Context: {state['user_context']}"

    investment_plan = agent.invoke({"messages": [prompt]})
    content = investment_plan["messages"][-1].content

    json_data = json.loads(content)
    parsed_response = AgentResponse(**json_data)
    state["investments"] = parsed_response.investments
    return state

def continue_to_explanation(state: InvestmentGraphState):
    print('Sending investments!')
    return [Send("explain_investment", {"investment": i}) for i in state["investments"]]

# Create a new Graph
workflow = StateGraph(state_schema=InvestmentGraphState)

def explain_investment(investment: InvestmentAmount):
    print('Received investment', investment)
    message = f"Investment: {investment}"
    agent = ExplainingAgent().build()
    agent_response = agent.invoke({"messages": [message]})

    explanation = agent_response["messages"][-1].content
    print('explanation', explanation)

    investment['investment'].explanation = explanation
    return {"explained_investments": [investment]}

# Add the nodes
workflow.add_node("investment_plan", get_investment_ideas)
workflow.add_node("explain_investment", explain_investment)

# Add the Edges
# workflow.add_edge("investment_plan", "node_2")
workflow.add_conditional_edges("investment_plan", continue_to_explanation, ["explain_investment"])
workflow.set_entry_point("investment_plan")
workflow.set_finish_point("explain_investment")

#Run the workflow
app = workflow.compile()

# state = InvestmentGraphState(
#     investmentPlan="",
#     user_message='Tengo 6000 dolares para invertir',
#     investments=[]
#     user_context=user_context
# )

# result = app.invoke(state)

# Save the Mermaid graph as a PNG file instead of trying to display it
graph_image = app.get_graph().draw_mermaid_png()
with open("investment_workflow.png", "wb") as f:
    f.write(graph_image)
print("Graph saved as 'investment_workflow.png'")

graph = app

# print(result)
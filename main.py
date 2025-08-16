from typing import Dict, List
from email import message
from typing import Any
from fastapi import FastAPI
from graph import InvestmentGraphState, graph
from pydantic import BaseModel

app = FastAPI(
    title="Open-Invest API",
    description="AI-Powered Investment Planning Agent",
    version="1.0.0"
)

class PlanInput(BaseModel):
    user_context: Dict[str, Any]  # Fixed: proper type annotation
    message: str
    likes: List[str]

@app.get("/")
async def root():
    return {"message": "Open-Invest API is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "Open-Invest API"}

@app.post('/plan')
async def create_plan(body: PlanInput):
    user_context = body.user_context
    initial_state = InvestmentGraphState(
        user_context=user_context,
        explained_investments=[],
        investments=[],
        user_message=body.message
    )
    result = graph.invoke(initial_state)
    return result['explained_investments']

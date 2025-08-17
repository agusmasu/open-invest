from typing import Dict, List
from email import message
from typing import Any
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from graph import InvestmentGraphState, graph
from pydantic import BaseModel
from models import PlanInput, PlanResponse, UserCreate, User, DatabaseResponse, InvestmentPlanCreate, InvestmentAmount
from database import Database, create_investment_plan, get_investment_plan_by_id, get_investment_plans_by_user, create_user, get_user_by_email
from datetime import datetime
import json

# Database lifecycle
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await Database.connect_db()
    yield
    # Shutdown
    await Database.close_db()

app = FastAPI(
    title="Open-Invest API",
    description="AI-Powered Investment Planning Agent with MongoDB",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PlanInput(BaseModel):
    user_context: Dict[str, Any]
    message: str
    likes: List[str]

def extract_investment_data(investment_dict):
    """Extract investment data from the nested structure returned by AI workflow"""
    try:
        # The AI workflow returns: {'investment': Investment..., risk: X, ease_of_use: Y}
        if 'investment' in investment_dict:
            # Extract the nested investment object
            investment = investment_dict['investment']
            
            # Handle both object and dict cases
            if hasattr(investment, 'name'):
                # It's an object with attributes
                name = getattr(investment, 'name', 'Unknown')
                amount = getattr(investment, 'amount', 0)
                percentage = getattr(investment, 'percentage', 0)
                reason = getattr(investment, 'reason', 'No reason provided')
                explanation = getattr(investment, 'explanation', None)
            elif isinstance(investment, dict):
                # It's a dictionary
                name = investment.get('name', 'Unknown')
                amount = investment.get('amount', 0)
                percentage = investment.get('percentage', 0)
                reason = investment.get('reason', 'No reason provided')
                explanation = investment.get('explanation', None)
            else:
                # Fallback for unknown types
                name = str(investment)
                amount = 0
                percentage = 0
                reason = 'Data extraction failed'
                explanation = None
            
            # Create a new dict with the flattened structure
            extracted = {
                'name': name,
                'amount': float(amount) if amount is not None else 0,
                'percentage': float(percentage) if percentage is not None else 0,
                'reason': reason,
                'risk': int(investment_dict.get('risk', 5)),  # Default to 5 if not present
                'ease_of_use': int(investment_dict.get('ease_of_use', 5)),  # Default to 5 if not present
                'explanation': explanation
            }
            return extracted
        else:
            # If no nested structure, try to extract directly
            if isinstance(investment_dict, dict):
                return {
                    'name': investment_dict.get('name', 'Unknown'),
                    'amount': float(investment_dict.get('amount', 0)),
                    'percentage': float(investment_dict.get('percentage', 0)),
                    'reason': investment_dict.get('reason', 'No reason provided'),
                    'risk': int(investment_dict.get('risk', 5)),
                    'ease_of_use': int(investment_dict.get('ease_of_use', 5)),
                    'explanation': investment_dict.get('explanation', None)
                }
            else:
                # Return a default structure to prevent crashes
                return {
                    'name': 'Unknown Investment',
                    'amount': 0,
                    'percentage': 0,
                    'reason': 'Data extraction failed',
                    'risk': 5,
                    'ease_of_use': 5,
                    'explanation': None
                }
    except Exception as e:
        print(f"❌ Error extracting investment data: {e}")
        print(f"❌ Investment dict: {investment_dict}")
        # Return a default structure to prevent crashes
        return {
            'name': 'Unknown Investment',
            'amount': 0,
            'percentage': 0,
            'reason': 'Data extraction failed',
            'risk': 5,
            'ease_of_use': 5,
            'explanation': None
        }

@app.get("/")
async def root():
    return {"message": "Open-Invest API is running", "database": "MongoDB"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "Open-Invest API", "database": "connected"}

@app.post('/plan', response_model=PlanResponse)
async def create_plan(body: PlanInput):
    try:
        # Create investment plan using the AI workflow
        initial_state = InvestmentGraphState(
            user_context=body.user_context,
            explained_investments=[],
            investments=[],
            user_message=body.message
        )
        
        print(f"🔍 Initial state: {initial_state}")
        result = graph.invoke(initial_state)
        print(f"🔍 AI workflow result: {json.dumps(result, default=str, indent=2)}")
        
        # Extract and flatten the investment data
        explained_investments = []
        for investment_dict in result.get('explained_investments', []):
            extracted = extract_investment_data(investment_dict)
            explained_investments.append(extracted)
        
        print(f"🔍 Extracted investments: {json.dumps(explained_investments, indent=2)}")
        
        # For now, we'll create a mock user_id (in production, you'd get this from authentication)
        # You can modify this to use actual user authentication
        mock_user_id = "mock_user_123"  # Simple string ID
        
        # Create investment plan in database using the proper model
        plan_data = InvestmentPlanCreate(
            user_id=mock_user_id,
            user_context=body.user_context,
            message=body.message,
            likes=body.likes,
            investments=explained_investments,
            explained_investments=explained_investments
        )
        
        print(f"🔍 Created plan data: {plan_data.model_dump()}")
        
        # Save to database
        saved_plan = await create_investment_plan(plan_data)
        
        return PlanResponse(
            plan_id=str(saved_plan.id),
            investments=explained_investments,
            message=body.message,
            created_at=saved_plan.created_at
        )
        
    except Exception as e:
        print(f"❌ Error creating plan: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error creating plan: {str(e)}")

@app.get('/plans/{user_id}', response_model=List[Dict[str, Any]])
async def get_user_plans(user_id: str, limit: int = 10):
    """Get all investment plans for a specific user."""
    try:
        plans = await get_investment_plans_by_user(user_id, limit)
        return [plan.model_dump() for plan in plans]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching plans: {str(e)}")

@app.get('/plan/{plan_id}', response_model=Dict[str, Any])
async def get_plan(plan_id: str):
    """Get a specific investment plan by ID."""
    try:
        plan = await get_investment_plan_by_id(plan_id)
        if not plan:
            raise HTTPException(status_code=404, detail="Plan not found")
        return plan.model_dump()
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching plan: {str(e)}")

@app.post('/users', response_model=User)
async def create_user_endpoint(user_data: UserCreate):
    """Create a new user."""
    try:
        user = await create_user(user_data)
        return user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating user: {str(e)}")

@app.get('/users/{email}', response_model=User)
async def get_user(email: str):
    """Get user by email."""
    try:
        user = await get_user_by_email(email)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching plan: {str(e)}")

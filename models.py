from datetime import datetime
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field, EmailStr

# User Models
class UserBase(BaseModel):
    email: EmailStr
    country: str
    investment_profile: str = Field(..., pattern="^(conservative|moderate|aggressive)$")
    age: int = Field(..., ge=18, le=100)
    user_idea: Optional[str] = None

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: str = Field(alias="_id")
    created_at: datetime
    updated_at: datetime

    model_config = {
        "populate_by_name": True,
        "arbitrary_types_allowed": True
    }

# Investment Models - Updated to match AI workflow output
class InvestmentAmount(BaseModel):
    name: str
    amount: float
    percentage: float
    reason: str
    risk: int = Field(..., ge=1, le=10)
    ease_of_use: int = Field(..., ge=1, le=10)
    explanation: Optional[str] = None

class InvestmentAmountWithId(InvestmentAmount):
    id: str = Field(alias="_id")
    created_at: datetime
    updated_at: datetime

    model_config = {
        "populate_by_name": True,
        "arbitrary_types_allowed": True
    }

# Investment Plan Models
class InvestmentPlanBase(BaseModel):
    user_context: Dict[str, Any]
    message: str
    likes: List[str]
    investments: List[InvestmentAmount]
    explained_investments: List[InvestmentAmount]

class InvestmentPlanCreate(InvestmentPlanBase):
    user_id: str

class InvestmentPlan(InvestmentPlanBase):
    id: str = Field(alias="_id")
    user_id: str
    created_at: datetime
    updated_at: datetime

    model_config = {
        "populate_by_name": True,
        "arbitrary_types_allowed": True
    }

# API Request/Response Models
class PlanInput(BaseModel):
    user_context: Dict[str, Any]
    message: str
    likes: List[str]

class PlanResponse(BaseModel):
    plan_id: str
    investments: List[InvestmentAmount]
    message: str
    created_at: datetime

# Database Response Models
class DatabaseResponse(BaseModel):
    success: bool
    message: str
    data: Optional[Any] = None
    error: Optional[str] = None

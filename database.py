import os
from datetime import datetime
from typing import List, Optional, Dict, Any
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from models import User, UserCreate, InvestmentPlan, InvestmentPlanCreate, InvestmentAmount

class Database:
    client: AsyncIOMotorClient = None
    db = None

    @classmethod
    async def connect_db(cls):
        """Create database connection."""
        mongodb_uri = os.getenv("MONGODB_URI", "mongodb://localhost:27017/investing_agent")
        cls.client = AsyncIOMotorClient(mongodb_uri)
        cls.db = cls.client.investing_agent
        print(f"✅ Connected to MongoDB: {mongodb_uri}")

    @classmethod
    async def close_db(cls):
        """Close database connection."""
        if cls.client:
            cls.client.close()
            print("✅ MongoDB connection closed")

    @classmethod
    async def get_collection(cls, collection_name: str):
        """Get a collection from the database."""
        return cls.db[collection_name]

# User operations
async def create_user(user_data: UserCreate) -> User:
    """Create a new user."""
    collection = await Database.get_collection("users")
    
    # Check if user already exists
    existing_user = await collection.find_one({"email": user_data.email})
    if existing_user:
        raise ValueError("User with this email already exists")
    
    user_dict = user_data.model_dump()
    user_dict["created_at"] = datetime.utcnow()
    user_dict["updated_at"] = datetime.utcnow()
    
    result = await collection.insert_one(user_dict)
    user_dict["_id"] = str(result.inserted_id)
    
    return User(**user_dict)

async def get_user_by_email(email: str) -> Optional[User]:
    """Get user by email."""
    collection = await Database.get_collection("users")
    user_data = await collection.find_one({"email": email})
    if user_data:
        user_data["_id"] = str(user_data["_id"])
        return User(**user_data)
    return None

async def get_user_by_id(user_id: str) -> Optional[User]:
    """Get user by ID."""
    collection = await Database.get_collection("users")
    try:
        user_data = await collection.find_one({"_id": ObjectId(user_id)})
        if user_data:
            user_data["_id"] = str(user_data["_id"])
            return User(**user_data)
    except:
        pass
    return None

# Investment Plan operations
async def create_investment_plan(plan_data: InvestmentPlanCreate) -> InvestmentPlan:
    """Create a new investment plan."""
    collection = await Database.get_collection("investment_plans")
    
    plan_dict = plan_data.model_dump()
    plan_dict["created_at"] = datetime.utcnow()
    plan_dict["updated_at"] = datetime.utcnow()
    
    result = await collection.insert_one(plan_dict)
    plan_dict["_id"] = str(result.inserted_id)
    
    return InvestmentPlan(**plan_dict)

async def get_investment_plans_by_user(user_id: str, limit: int = 10) -> List[InvestmentPlan]:
    """Get investment plans for a specific user."""
    collection = await Database.get_collection("investment_plans")
    
    try:
        cursor = collection.find({"user_id": user_id}).sort("created_at", -1).limit(limit)
        plans = []
        
        async for plan_data in cursor:
            plan_data["_id"] = str(plan_data["_id"])
            plans.append(InvestmentPlan(**plan_data))
        
        return plans
    except:
        return []

async def get_investment_plan_by_id(plan_id: str) -> Optional[InvestmentPlan]:
    """Get investment plan by ID."""
    collection = await Database.get_collection("investment_plans")
    try:
        plan_data = await collection.find_one({"_id": ObjectId(plan_id)})
        if plan_data:
            plan_data["_id"] = str(plan_data["_id"])
            return InvestmentPlan(**plan_data)
    except:
        pass
    return None

async def update_investment_plan(plan_id: str, update_data: Dict[str, Any]) -> bool:
    """Update an investment plan."""
    collection = await Database.get_collection("investment_plans")
    
    update_data["updated_at"] = datetime.utcnow()
    try:
        result = await collection.update_one(
            {"_id": ObjectId(plan_id)},
            {"$set": update_data}
        )
        return result.modified_count > 0
    except:
        return False

async def delete_investment_plan(plan_id: str) -> bool:
    """Delete an investment plan."""
    collection = await Database.get_collection("investment_plans")
    try:
        result = await collection.delete_one({"_id": ObjectId(plan_id)})
        return result.deleted_count > 0
    except:
        return False

# Analytics and reporting
async def get_user_investment_summary(user_id: str) -> Dict[str, Any]:
    """Get investment summary for a user."""
    collection = await Database.get_collection("investment_plans")
    
    try:
        pipeline = [
            {"$match": {"user_id": user_id}},
            {"$unwind": "$investments"},
            {"$group": {
                "_id": "$investments.type",
                "total_amount": {"$sum": "$investments.amount"},
                "count": {"$sum": 1},
                "avg_percentage": {"$avg": "$investments.percentage"}
            }},
            {"$sort": {"total_amount": -1}}
        ]
        
        cursor = collection.aggregate(pipeline)
        summary = []
        
        async for doc in cursor:
            summary.append({
                "type": doc["_id"],
                "total_amount": doc["total_amount"],
                "count": doc["count"],
                "avg_percentage": round(doc["avg_percentage"], 2)
            })
        
        return {
            "user_id": user_id,
            "investment_summary": summary,
            "total_plans": await collection.count_documents({"user_id": user_id})
        }
    except:
        return {
            "user_id": user_id,
            "investment_summary": [],
            "total_plans": 0
        }

async def get_popular_investments(limit: int = 10) -> List[Dict[str, Any]]:
    """Get most popular investment types across all users."""
    collection = await Database.get_collection("investment_plans")
    
    try:
        pipeline = [
            {"$unwind": "$investments"},
            {"$group": {
                "_id": "$investments.type",
                "total_mentions": {"$sum": 1},
                "avg_amount": {"$avg": "$investments.amount"},
                "avg_percentage": {"$avg": "$investments.percentage"}
            }},
            {"$sort": {"total_mentions": -1}},
            {"$limit": limit}
        ]
        
        cursor = collection.aggregate(pipeline)
        popular = []
        
        async for doc in cursor:
            popular.append({
                "type": doc["_id"],
                "total_mentions": doc["total_mentions"],
                "avg_amount": round(doc["avg_amount"], 2),
                "avg_percentage": round(doc["avg_percentage"], 2)
            })
        
        return popular
    except:
        return []

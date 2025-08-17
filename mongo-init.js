// MongoDB initialization script for Investing Agent
// This script runs when the MongoDB container starts for the first time

// Switch to the investing_agent database
db = db.getSiblingDB('investing_agent');

// Create collections with validation
db.createCollection('users', {
  validator: {
    $jsonSchema: {
      bsonType: 'object',
      required: ['email', 'created_at'],
      properties: {
        email: {
          bsonType: 'string',
          pattern: '^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$'
        },
        country: { bsonType: 'string' },
        investment_profile: { 
          bsonType: 'string',
          enum: ['conservative', 'moderate', 'aggressive']
        },
        age: { bsonType: 'int', minimum: 18, maximum: 100 },
        created_at: { bsonType: 'date' },
        updated_at: { bsonType: 'date' }
      }
    }
  }
});

db.createCollection('investment_plans', {
  validator: {
    $jsonSchema: {
      bsonType: 'object',
      required: ['user_id', 'user_context', 'message', 'investments', 'created_at'],
      properties: {
        user_id: { bsonType: 'string' },
        user_context: { bsonType: 'object' },
        message: { bsonType: 'string' },
        likes: { bsonType: 'array' },
        investments: { bsonType: 'array' },
        explained_investments: { bsonType: 'array' },
        created_at: { bsonType: 'date' },
        updated_at: { bsonType: 'date' }
      }
    }
  }
});

db.createCollection('investments', {
  validator: {
    $jsonSchema: {
      bsonType: 'object',
      required: ['name', 'amount', 'percentage', 'reason', 'risk', 'ease_of_use'],
      properties: {
        name: { bsonType: 'string' },
        amount: { bsonType: 'number', minimum: 0 },
        percentage: { bsonType: 'number', minimum: 0, maximum: 100 },
        reason: { bsonType: 'string' },
        risk: { bsonType: 'int', minimum: 1, maximum: 10 },
        ease_of_use: { bsonType: 'int', minimum: 1, maximum: 10 },
        explanation: { bsonType: 'string' },
        created_at: { bsonType: 'date' },
        updated_at: { bsonType: 'date' }
      }
    }
  }
});

// Create indexes for better performance
db.users.createIndex({ "email": 1 }, { unique: true });
db.users.createIndex({ "country": 1 });
db.users.createIndex({ "investment_profile": 1 });

db.investment_plans.createIndex({ "user_id": 1 });
db.investment_plans.createIndex({ "created_at": -1 });
db.investment_plans.createIndex({ "user_id": 1, "created_at": -1 });

db.investments.createIndex({ "risk": 1 });
db.investments.createIndex({ "ease_of_use": 1 });
db.investments.createIndex({ "created_at": -1 });

// Create a compound index for user plans
db.investment_plans.createIndex({ "user_id": 1, "created_at": -1 });

print('✅ MongoDB initialized successfully for Investing Agent!');
print('📊 Collections created: users, investment_plans, investments');
print('🔍 Indexes created for optimal query performance');

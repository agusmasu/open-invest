# Open-Invest: AI-Powered Investment Planning Agent

An intelligent investment planning application that uses AI agents to help users create personalized investment plans and get detailed explanations of investment options. Now with MongoDB persistence for storing user data and investment plans.

## Features

- **Investment Planning**: AI-powered investment strategy creation based on user context
- **Smart Explanations**: Detailed explanations of investment options tailored to user preferences
- **Multi-Agent Workflow**: Uses LangGraph for orchestrated AI agent interactions
- **FastAPI Backend**: Modern, fast web API with automatic documentation
- **MongoDB Database**: Persistent storage for users and investment plans
- **Data Analytics**: Investment summaries and popular investment tracking

## Quick Start with Docker

### Prerequisites

- Docker and Docker Compose installed
- OpenAI API key
- Tavily API key (for news search functionality)

### 1. Clone and Setup

```bash
git clone <your-repo-url>
cd investing-agent
```

### 2. Environment Configuration

Copy the environment example file and configure your API keys:

```bash
cp env.example .env
```

Edit `.env` and add your API keys:
```bash
OPENAI_API_KEY=your_openai_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
MONGO_ROOT_USERNAME=admin
MONGO_ROOT_PASSWORD=password
```

### 3. Run with Docker Compose

```bash
# Build and start the application with MongoDB
docker-compose up --build

# Or run in detached mode
docker-compose up -d --build
```

The application will be available at: http://localhost:8000
MongoDB will be available at: localhost:27017

### 4. Access the API

- **Application**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## Manual Setup (Without Docker)

### Prerequisites

- Python 3.11+
- pip
- MongoDB 7.0+ (running locally or cloud instance)

### Installation

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export OPENAI_API_KEY=your_key_here
export TAVILY_API_KEY=your_key_here
export MONGODB_URI=mongodb://localhost:27017/investing_agent

# Run the application
python -m uvicorn main:app --reload
```

## API Usage

### Create User

```bash
curl -X POST "http://localhost:8000/users" \
     -H "Content-Type: application/json" \
     -d '{
       "email": "user@example.com",
       "country": "Argentina",
       "investment_profile": "moderate",
       "age": 28,
       "user_idea": "Quiero invertir para tener un fondo para retirarme"
     }'
```

### Create Investment Plan

```bash
curl -X POST "http://localhost:8000/plan" \
     -H "Content-Type: application/json" \
     -d '{
       "user_context": {
         "country": "Argentina",
         "investmentProfile": "moderate",
         "user_idea": "Quiero invertir para tener un fondo para retirarme",
         "age": 28
       },
       "message": "Tengo 6000 dolares para invertir",
       "likes": ["futbol"]
     }'
```

### Get User Plans

```bash
curl "http://localhost:8000/plans/507f1f77bcf86cd799439011?limit=5"
```

### Get Specific Plan

```bash
curl "http://localhost:8000/plan/507f1f77bcf86cd799439011"
```

## Database Schema

### Collections

- **users**: User profiles and preferences
- **investment_plans**: Complete investment plans with AI-generated recommendations
- **investments**: Individual investment items with explanations

### Key Features

- **Data Validation**: MongoDB schema validation for data integrity
- **Indexing**: Optimized queries for user plans and investment analytics
- **Flexible Schema**: JSON-like documents for evolving investment data structures

## Docker Commands

### Build the image
```bash
docker build -t investing-agent .
```

### Run the container
```bash
docker run -p 8000:8000 --env-file .env investing-agent
```

### View logs
```bash
docker-compose logs -f
```

### Stop the application
```bash
docker-compose down
```

### Rebuild and restart
```bash
docker-compose down
docker-compose up --build
```

### MongoDB operations
```bash
# Access MongoDB shell
docker-compose exec mongo mongosh -u admin -p password

# View MongoDB logs
docker-compose logs mongo

# Backup database
docker-compose exec mongo mongodump --out /backup
```

## Project Structure

```
investing-agent/
├── agents/                 # AI agent implementations
│   ├── explainer/         # Investment explanation agent
│   ├── news_agent/        # News analysis agent
│   └── planner/           # Investment planning agent
├── main.py                # FastAPI application entry point
├── graph.py               # LangGraph workflow definition
├── models.py              # Pydantic models for API and database
├── database.py            # MongoDB operations and CRUD functions
├── mongo-init.js          # MongoDB initialization script
├── Dockerfile             # Docker configuration
├── docker-compose.yml     # Docker Compose configuration
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `OPENAI_API_KEY` | OpenAI API key for AI models | Yes | - |
| `TAVILY_API_KEY` | Tavily API key for news search | Yes | - |
| `MONGO_ROOT_USERNAME` | MongoDB root username | No | admin |
| `MONGO_ROOT_PASSWORD` | MongoDB root password | No | password |
| `MONGODB_URI` | MongoDB connection string | No | mongodb://mongo:27017/investing_agent |
| `LANGCHAIN_TRACING_V2` | Enable LangChain tracing | No | false |
| `LANGCHAIN_ENDPOINT` | LangChain endpoint URL | No | - |
| `LANGCHAIN_API_KEY` | LangChain API key | No | - |
| `LANGCHAIN_PROJECT` | LangChain project name | No | - |

## Troubleshooting

### Common Issues

1. **Port already in use**: Change the port in `docker-compose.yml` or stop other services using port 8000
2. **API key errors**: Ensure your `.env` file is properly configured with valid API keys
3. **Build failures**: Make sure Docker has enough memory allocated (recommended: 4GB+)
4. **MongoDB connection issues**: Check if MongoDB container is running and healthy
5. **Database validation errors**: Ensure your data matches the defined schema

### Health Check

The application includes health checks for both the API and MongoDB:

```bash
# Check API health
curl http://localhost:8000/health

# Check MongoDB health
docker-compose exec mongo mongosh --eval "db.adminCommand('ping')"
```

### Logs and Debugging

```bash
# View all logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f investing-agent
docker-compose logs -f mongo

# Access MongoDB shell for debugging
docker-compose exec mongo mongosh -u admin -p password
```

## Development

### Adding New Dependencies

1. Add to `requirements.txt`
2. Rebuild the Docker image: `docker-compose up --build`

### Code Changes

The application uses volume mounting, so most code changes will be reflected immediately without rebuilding.

### Database Migrations

For schema changes, update the `mongo-init.js` file and restart the MongoDB container:

```bash
docker-compose restart mongo
```

## Performance Considerations

- **MongoDB Indexing**: Optimized indexes for user queries and investment analytics
- **Connection Pooling**: Motor (async MongoDB driver) handles connection management
- **Data Validation**: Schema validation at the database level for data integrity
- **Health Checks**: Regular health monitoring for both API and database

## Security Notes

- **Production**: Change default MongoDB credentials
- **Network**: Restrict MongoDB port access in production
- **Authentication**: Implement proper user authentication and authorization
- **CORS**: Configure CORS origins properly for production

## License

[Your License Here]
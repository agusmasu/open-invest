# Open-Invest: AI-Powered Investment Planning Agent

An intelligent investment planning application that uses AI agents to help users create personalized investment plans and get detailed explanations of investment options.

## Features

- **Investment Planning**: AI-powered investment strategy creation based on user context
- **Smart Explanations**: Detailed explanations of investment options tailored to user preferences
- **Multi-Agent Workflow**: Uses LangGraph for orchestrated AI agent interactions
- **FastAPI Backend**: Modern, fast web API with automatic documentation

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
```

### 3. Run with Docker Compose

```bash
# Build and start the application
docker-compose up --build

# Or run in detached mode
docker-compose up -d --build
```

The application will be available at: http://localhost:8000

### 4. Access the API

- **API Documentation**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## Manual Setup (Without Docker)

### Prerequisites

- Python 3.11+
- pip

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

# Run the application
python -m uvicorn main:app --reload
```

## API Usage

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

## Project Structure

```
investing-agent/
├── agents/                 # AI agent implementations
│   ├── explainer/         # Investment explanation agent
│   ├── news_agent/        # News analysis agent
│   └── planner/           # Investment planning agent
├── main.py                # FastAPI application entry point
├── graph.py               # LangGraph workflow definition
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
| `LANGCHAIN_TRACING_V2` | Enable LangChain tracing | No | false |
| `LANGCHAIN_ENDPOINT` | LangChain endpoint URL | No | - |
| `LANGCHAIN_API_KEY` | LangChain API key | No | - |
| `LANGCHAIN_PROJECT` | LangChain project name | No | - |

## Troubleshooting

### Common Issues

1. **Port already in use**: Change the port in `docker-compose.yml` or stop other services using port 8000
2. **API key errors**: Ensure your `.env` file is properly configured with valid API keys
3. **Build failures**: Make sure Docker has enough memory allocated (recommended: 4GB+)

### Health Check

The application includes a health check endpoint. If the health check fails, check the logs:

```bash
docker-compose logs investing-agent
```

## Development

### Adding New Dependencies

1. Add to `requirements.txt`
2. Rebuild the Docker image: `docker-compose up --build`

### Code Changes

The application uses volume mounting, so most code changes will be reflected immediately without rebuilding.

## License

[Your License Here]
<p align="center">
<img src="https://github.com/Tensorone-AI/tensorone/blob/main/images/icon.png?raw=true" width="35%" />
<br />
</p>
<p align="center">
<a href="https://docs.tensorone.ai/"><img src="https://img.shields.io/badge/docs-API-blue.svg" /></a> &nbsp;
<a href="https://github.com/Tensorone-AI/tensorone">
  <img src="https://img.shields.io/github/stars/Tensorone-AI/tensorone?style=social" />
</a>
</a>
<a href="#"><img src="https://img.shields.io/badge/built_with-JavaScript-f7df1e.svg" /></a>

<p align="center">
Unlock AI & ML potential with <code>Tensor One</code>. Access and contribute to cutting-edge AI agents & tools.
</p>
<p align="center">
It powers the <a href="https://dapp.tensorone.ai/">Tensor One App</a>, check it out to see what <code>Tensor One</code> is capable of

## Tensor One Architecture

![Agent Infrastructure](https://github.com/Tensorone-AI/tensorone/blob/main/images/infra.jpg?raw=true)

![GPU Framework](https://github.com/Tensorone-AI/tensorone/blob/main/images/gpu.png?raw=true)

## Features

-   🤖 No-code AI agent builder with customizable behavior, personality, and voice
-   🎨 Access powerful AI tools like voice cloning, media generation, and app/website creation
-   ⚡ Distributed compute via browser extension with real-time GPU contribution
-   💸 Monetization options for builders through usage fees or subscriptions
-   🧠 Agent coordination and prompt execution through a unified interface
-   📊 Usage analytics and performance tracking (future)

For complete rundown of features, check out the
[documentation](https://docs.tensorone.ai/).

## 🏗️ Architecture

This is a monorepo containing:

- **Frontend**: SvelteKit web application with Web3 wallet integration
- **Backend**: Python Flask API with AI/ML capabilities
- **AI Stack**: Pydantic AI agents, OpenAI compatibility, RAG with Weaviate
- **Search**: Tavily web search integration
- **Database**: Supabase (PostgreSQL) + Weaviate vector database
- **Blockchain**: Ethereum mainnet integration via Reown (WalletConnect)

## 📁 Project Structure

```
tensorone/
├── frontend/                # SvelteKit web application
│   ├── src/
│   │   ├── routes/          # SvelteKit pages and API routes
│   │   ├── lib/             # Shared components and utilities
│   │   └── app.html         # Main HTML template
│   ├── static/              # Static assets
│   ├── package.json
│   └── docker/              # Frontend Docker configuration
├── backend/                 # Python Flask API server
│   ├── app/
│   │   ├── agents/          # Pydantic AI agent definitions
│   │   ├── rag/             # RAG implementation with Weaviate
│   │   ├── search/          # Tavily search integration
│   │   ├── models/          # Data models and schemas
│   │   └── routes/          # Flask API endpoints
│   ├── requirements.txt
│   ├── Dockerfile
│   └── docker-compose.yml
├── shared/                  # Shared configurations and schemas
├── docs/                    # Documentation
├── scripts/                 # Development and deployment scripts
└── docker-compose.yml       # Full stack orchestration
```

## 🚀 Quick Start

### Prerequisites

- Node.js 20+ and npm
- Python 3.11+
- Docker and Docker Compose
- Git

### Environment Setup

1. **Clone the repository:**
```bash
git clone <repository-url>
cd tensorone
```

2. **Copy environment files:**
```bash
# Frontend environment
cp frontend/.env.example frontend/.env

# Backend environment  
cp backend/.env.example backend/.env
```

3. **Configure environment variables** (see [Environment Variables](#environment-variables) section)

### Development Setup

#### Option 1: Docker Compose (Recommended)

```bash
# Start all services (frontend, backend, databases)
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

Services will be available at:
- Frontend: http://localhost:3000
- Backend API: http://localhost:5000
- Weaviate: http://localhost:8080
- PostgreSQL: localhost:5432

#### Option 2: Manual Setup

**Frontend Setup:**
```bash
cd frontend
npm install
npm run dev
```

**Backend Setup:**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

**Database Setup:**
```bash
# Start Weaviate and PostgreSQL
docker-compose up -d weaviate postgres redis

# Run database migrations
cd backend
python -m flask db upgrade
```

## 🤖 AI Stack Components

### Pydantic AI Agents
- **Agent Framework**: Structured AI agents with type validation
- **OpenAI Compatible**: Works with OpenAI, Anthropic, and local models
- **Multi-modal**: Support for text, image, and audio processing
- **Tool Integration**: Function calling and external API integration

### RAG (Retrieval Augmented Generation)
- **Vector Database**: Weaviate for semantic search and storage
- **Document Processing**: MarkItDown server for document conversion
- **Embedding Models**: Support for various embedding providers
- **Chunk Management**: Intelligent document chunking and indexing

### Web Search Integration
- **Tavily API**: Real-time web search capabilities
- **Search Enhancement**: AI-powered search result processing
- **Context Integration**: Search results are integrated into agent responses

## 🔧 Environment Variables

### Frontend (.env)
```bash
# Supabase Configuration
VITE_SUPABASE_URL=your_supabase_url
VITE_SUPABASE_API_KEY=your_supabase_anon_key

# Backend API URLs
VITE_DAPP_BACKEND_URL=http://localhost:5000
VITE_MCP_BACKEND_URL=http://localhost:5000

# Web3 Configuration
PUBLIC_REOWN_PROJECT_ID=your_reown_project_id
```

### Backend (.env)
```bash
# Flask Configuration
FLASK_ENV=development
SECRET_KEY=your_secret_key

# Database URLs
DATABASE_URL=postgresql://user:password@localhost:5432/tensorone
WEAVIATE_URL=http://localhost:8080

# AI Service APIs
OPENAI_API_KEY=your_openai_api_key
ANTHROPIC_API_KEY=your_anthropic_api_key
TAVILY_API_KEY=your_tavily_api_key

# Supabase (for user management)
SUPABASE_URL=your_supabase_url
SUPABASE_SERVICE_KEY=your_supabase_service_key

# Redis (for caching)
REDIS_URL=redis://localhost:6379
```

## 📡 API Endpoints

### Core API Routes
- `GET /api/health` - Health check
- `POST /api/chat` - Chat with AI agents
- `POST /api/agents` - Create/manage AI agents
- `GET /api/agents/{id}` - Get agent details

### AI Services
- `POST /api/generate/image` - Text-to-image generation
- `POST /api/generate/speech` - Text-to-speech synthesis
- `POST /api/generate/video` - Text-to-video generation
- `POST /api/search` - Web search with Tavily

### RAG Services
- `POST /api/rag/upload` - Upload documents for indexing
- `POST /api/rag/query` - Query knowledge base
- `GET /api/rag/documents` - List indexed documents

## 🧪 Development Workflow

### Running Tests
```bash
# Frontend tests
cd frontend
npm test

# Backend tests
cd backend
python -m pytest

# Integration tests
docker-compose -f docker-compose.test.yml up --abort-on-container-exit
```

### Code Formatting
```bash
# Frontend (Prettier)
cd frontend
npm run format

# Backend (Black + isort)
cd backend
black .
isort .
```

### Database Migrations
```bash
cd backend
python -m flask db migrate -m "Migration description"
python -m flask db upgrade
```

## 🐳 Docker Configuration

### Full Stack Deployment
```bash
# Production build and deployment
docker-compose -f docker-compose.prod.yml up -d

# Development with hot reload
docker-compose -f docker-compose.dev.yml up -d
```

### Individual Services
```bash
# Frontend only
docker-compose up frontend

# Backend + databases
docker-compose up backend weaviate postgres redis

# AI services only
docker-compose up backend weaviate
```

## 📈 Monitoring and Logging

- Application logs via Python logging
- Database query monitoring
- API endpoint metrics
- Docker container health checks
- Vector database performance monitoring

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🚀 Deployment

### Production Deployment
```bash
# Build production images
docker-compose -f docker-compose.prod.yml build

# Deploy with orchestration
docker-compose -f docker-compose.prod.yml up -d

# Health check
curl http://localhost:3000/health
curl http://localhost:5000/api/health
```

### Cloud Deployment
- Supports deployment to AWS, GCP, Azure
- Kubernetes manifests available in `k8s/` directory
- CI/CD pipelines configured for GitHub Actions

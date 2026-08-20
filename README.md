# FatigueSense

## Intelligent AI-Powered Fatigue Analysis Platform

FatigueSense is a modular AI application designed to analyze visible
facial indicators associated with fatigue from uploaded images. It
combines **Computer Vision, AI Agents, Retrieval-Augmented Generation
(RAG), LangGraph orchestration, memory, databases, FastAPI, React, and
Docker-ready deployment** into one integrated platform.

> **Project status:** Active development and team integration.

------------------------------------------------------------------------

## Overview

FatigueSense processes a facial image through a structured analysis
pipeline. The system validates the input, extracts facial and
eye-related features, retrieves supporting knowledge from a reference
corpus, calculates a fatigue score, determines a risk level, generates
recommendations, and presents the result through a web interface.

The architecture is modular so that Computer Vision, RAG, frontend,
orchestration, memory, database, and API components can be developed
independently and integrated through clearly defined interfaces.

### End-to-End Pipeline

``` text
User
  |
  v
React Frontend
  |
  v
FastAPI Backend
  |
  v
LangGraph Orchestration
  |
  +--> Computer Vision / Image Analysis
  |
  +--> Face Validation
  |
  +--> RAG Retrieval
  |
  +--> Fatigue Scoring
  |
  +--> Recommendation
  |
  +--> Memory / Database
  |
  v
Final Analysis Result
  |
  v
React Dashboard
```

------------------------------------------------------------------------

## ✨ Key Features

### Computer Vision

-   Facial image validation
-   Human face detection
-   Eye-state analysis
-   Eye aspect ratio analysis
-   Blink detection
-   Yawning detection
-   Facial feature extraction
-   Under-eye feature analysis

### AI Agent Layer

-   Image analysis agent
-   Fatigue scoring agent
-   Recommendation agent
-   Agent tools for supporting operations

### 📚 RAG Pipeline

-   PDF, JSON, and TXT document ingestion
-   Document parsing and preprocessing
-   Multiple chunking strategies
-   Embedding generation
-   Vector storage
-   Semantic search
-   BM25 search
-   Hybrid retrieval
-   Reranking

### LangGraph Orchestration

-   Shared workflow state
-   Modular graph nodes
-   Conditional routing
-   Agent and pipeline coordination
-   Extensible multi-step workflow

### Memory

-   Session memory
-   Long-term memory
-   Memory management
-   Context management

### Data Storage

-   MySQL for structured application data
-   NoSQL storage for document-oriented data
-   CRUD and connection layers
-   Database setup scripts

### Web Application

-   Image upload
-   Fatigue score display
-   Risk-level display
-   Recommendations
-   Analysis details
-   History
-   Dashboard and charts

### Engineering

-   Modular backend architecture
-   Automated tests
-   GitHub workflow support
-   Docker-ready architecture

------------------------------------------------------------------------

## 🏗️ System Architecture

``` text
+-------------------------------------------------------------+
|                         FRONTEND                            |
|                    React + Vite + UI                        |
|                                                             |
| Upload | Analysis | Score | Risk | Recommendation | History |
+-----------------------------+-------------------------------+
                              |
                              | REST API
                              v
+-------------------------------------------------------------+
|                         BACKEND                             |
|                         FastAPI                             |
+-------------------------------------------------------------+
|                         API Layer                           |
| Analyze | Upload | History | Documents | Health             |
+-------------------------------------------------------------+
|                    LANGGRAPH LAYER                          |
|                                                             |
| State <-> Nodes <-> Router <-> Graph <-> Configuration      |
+----------------------+----------------------+---------------+
                       |                      |
                       v                      v
                Computer Vision             RAG
                       |                      |
                       |               Loaders / Parsers
                       |               Preprocessing
                       |               Chunking
                       |               Embeddings
                       |               Vector Store
                       |               Retrieval
                       |                      |
                       +----------+-----------+
                                  |
                                  v
                         Fatigue Scoring
                                  |
                                  v
                         Recommendation
                                  |
                                  v
                         Memory / Storage
                                  |
                                  v
                         Final Response
```

------------------------------------------------------------------------

## 🔄 LangGraph Workflow

The orchestration layer is designed around the following workflow:

``` text
                    +----------------+
                    |  Input State   |
                    +-------+--------+
                            |
                            v
                  +-------------------+
                  | Image Analysis    |
                  |      Node         |
                  +---------+---------+
                            |
                            v
                  +-------------------+
                  | Face Validation   |
                  +---------+---------+
                            |
                   +--------+--------+
                   |                 |
                Invalid             Valid
                   |                 |
                   v                 v
                  END        +----------------+
                             |    RAG Node    |
                             +-------+--------+
                                     |
                                     v
                             +---------------+
                             | Fatigue Score |
                             +-------+-------+
                                     |
                                     v
                             +---------------+
                             | Recommendation|
                             +-------+-------+
                                     |
                                     v
                             +---------------+
                             | Memory / DB   |
                             +-------+-------+
                                     |
                                     v
                             +---------------+
                             | Final Result  |
                             +---------------+
```

### Orchestration Modules

  File                   Responsibility
  ---------------------- --------------------------------------------
  `state.py`             Shared state passed between graph nodes
  `nodes.py`             Individual workflow node implementations
  `graph.py`             Builds and compiles the LangGraph workflow
  `router.py`            Conditional routing and workflow decisions
  `workflow_config.py`   Workflow configuration

------------------------------------------------------------------------

## RAG Architecture

``` text
Reference Documents
        |
        v
     Loaders
        |
        v
     Parsers
        |
        v
  Preprocessing
        |
        v
    Chunking
        |
        v
   Embeddings
        |
        v
  Vector Store
        |
        v
    Retrieval
     /    |    \
Semantic BM25 Hybrid
        |
        v
     Reranker
        |
        v
Relevant Context
        |
        v
LangGraph Workflow
```

Reference documents are organized under:

``` text
backend/data/reference_documents/
├── pdf/
├── json/
└── txt/
```

Generated chunks and embeddings are kept separately:

``` text
backend/data/chunks/
backend/data/embeddings/
```

------------------------------------------------------------------------

## 🗂️ Project Structure

``` text
FatigueSense/
|
├── README.md
├── .gitignore
├── .env
├── .env.example
|
├── backend/
|   ├── requirements.txt
|   ├── run.py
|   |
|   ├── app/
|   |   ├── __init__.py
|   |   ├── main.py
|   |   |
|   |   ├── agents/                    # Member A
|   |   |   ├── image_analysis_agent.py
|   |   |   ├── fatigue_scoring_agent.py
|   |   |   ├── recommendation_agent.py
|   |   |   └── agent_tools.py
|   |   |
|   |   ├── cv/                        # Member A
|   |   |   ├── face_detection.py
|   |   |   ├── eye_analysis.py
|   |   |   ├── blink_detection.py
|   |   |   ├── yawn_detection.py
|   |   |   ├── facial_features.py
|   |   |   └── feature_extraction.py
|   |   |
|   |   ├── preprocessing/             # Member A
|   |   |   ├── format_detector.py
|   |   |   ├── format_normalizer.py
|   |   |   ├── image_validator.py
|   |   |   └── image_preprocessor.py
|   |   |
|   |   ├── rag/                       # Member B
|   |   |   ├── loaders/
|   |   |   ├── parsers/
|   |   |   ├── preprocessing/
|   |   |   ├── chunking/
|   |   |   ├── embeddings/
|   |   |   ├── vector_store/
|   |   |   ├── retrieval/
|   |   |   ├── rag_agent_tool.py
|   |   |   └── pipeline.py
|   |   |
|   |   ├── orchestration/             # Member D - LangGraph
|   |   |   ├── state.py
|   |   |   ├── nodes.py
|   |   |   ├── graph.py
|   |   |   ├── router.py
|   |   |   └── workflow_config.py
|   |   |
|   |   ├── memory/                    # Member D
|   |   |   ├── session_memory.py
|   |   |   ├── long_term_memory.py
|   |   |   ├── memory_manager.py
|   |   |   └── context_manager.py
|   |   |
|   |   ├── database/                  # Member D
|   |   |   ├── mysql/
|   |   |   └── nosql/
|   |   |
|   |   ├── api/                       # Member D
|   |   |   ├── dependencies.py
|   |   |   └── routes/
|   |   |
|   |   ├── schemas/
|   |   ├── services/                  # Member D
|   |   └── utils/
|   |
|   ├── tests/
|   ├── data/
|   |   ├── test_images/
|   |   ├── reference_documents/
|   |   ├── chunks/
|   |   └── embeddings/
|   |
|   └── scripts/
|
├── frontend/                          # Member C
|   ├── package.json
|   ├── vite.config.js
|   ├── public/
|   └── src/
|       ├── components/
|       ├── pages/
|       ├── services/
|       ├── hooks/
|       ├── utils/
|       ├── App.jsx
|       ├── main.jsx
|       └── index.css
|
├── database/                           # Member D
|   ├── mysql/
|   └── nosql/
|
├── docs/                               # All Members
|   ├── architecture/
|   ├── project_report/
|   └── api/
|
├── docker/
|   ├── Dockerfile.backend
|   ├── Dockerfile.frontend
|   └── docker-compose.yml
|
└── .github/
    └── workflows/
        └── tests.yml
```

------------------------------------------------------------------------

## 👥 Team Responsibilities

  -----------------------------------------------------------------------
  Member                  Primary Responsibility  Main Modules
  ----------------------- ----------------------- -----------------------
  **A**                   Computer Vision and     `agents/`, `cv/`,
                          image analysis          `preprocessing/`

  **B**                   RAG and knowledge       `rag/`, document
                          retrieval               ingestion, embeddings,
                                                  retrieval

  **C**                   Frontend and user       `frontend/`
                          interface               

  **D**                   LangGraph orchestration `orchestration/`,
                          and backend integration `memory/`, `database/`,
                                                  `api/`, `services/`

  **All**                 Testing and             `tests/`, `docs/`
                          documentation           
  -----------------------------------------------------------------------

This ownership model keeps the major components independent while
defining clear integration points between them.

------------------------------------------------------------------------

## 🛠️ Technology Stack

  Layer                 Technology
  --------------------- ----------------------------------------
  Frontend              React
  Build Tool            Vite
  Styling               Tailwind CSS
  Charts                Recharts
  Icons                 Lucide React
  Backend               Python
  API                   FastAPI
  Computer Vision       Python CV / facial-analysis components
  AI Agents             Modular agent architecture
  Orchestration         LangGraph
  RAG                   Modular custom RAG pipeline
  Vector Store          Chroma-compatible architecture
  Structured Database   MySQL
  NoSQL                 NoSQL database layer
  Testing               Pytest
  Containerization      Docker / Docker Compose
  Version Control       Git / GitHub

------------------------------------------------------------------------

## Getting Started

### 📋 Prerequisites

Install:

-   Python 3.10+
-   Node.js 18+
-   npm
-   Git
-   MySQL
-   Required NoSQL service/database
-   Docker and Docker Compose (optional)

### 1. Clone the Repository

``` bash
git clone https://github.com/nehasahu11/FatigueSense.git
cd FatigueSense
```

### 2. Backend Setup

Windows PowerShell:

``` powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
cd backend
pip install -r requirements.txt
cd ..
```

### 3. Environment Configuration

Create the environment file:

``` powershell
Copy-Item .env.example .env
```

Then configure the required database, model, API, and RAG settings.

Never commit real secrets to GitHub.

### 4. Database Setup

Use the SQL files under:

``` text
database/mysql/
```

If the setup script is configured for the project:

``` powershell
python backend/scripts/setup_mysql.py
```

Configure the NoSQL service according to the environment configuration.

### 5. Run the Backend

From the project root:

``` powershell
python -m uvicorn backend.app.main:app --reload
```

Backend:

``` text
http://127.0.0.1:8000
```

Swagger API documentation:

``` text
http://127.0.0.1:8000/docs
```

### 6. Run the Frontend

Open another terminal:

``` powershell
cd frontend
npm install
npm run dev
```

Open the URL displayed by Vite.

------------------------------------------------------------------------

## Docker

The repository is structured for containerized deployment:

``` text
docker/
├── Dockerfile.backend
├── Dockerfile.frontend
└── docker-compose.yml
```

After the Docker configuration is completed:

``` bash
docker compose up --build
```

------------------------------------------------------------------------

## 🧪 Testing

Run backend tests:

``` bash
pytest
```

Before committing changes, also verify:

``` bash
git status
```

For the frontend:

``` bash
cd frontend
npm run lint
npm run build
```

------------------------------------------------------------------------

## 🔌 API Endpoints

The backend is organized around the following route groups:

``` text
/api/analyze
/api/upload
/api/history
/api/documents
/api/health
```

Interactive API documentation is available through FastAPI at:

``` text
/docs
```

when the backend is running.

------------------------------------------------------------------------

## 🌿 Development Workflow

Create a feature branch:

``` bash
git checkout -b feature/<feature-name>
```

Use descriptive commits:

``` text
feat: add eye closure analysis
feat: integrate RAG retrieval
feat: add LangGraph workflow node
fix: resolve image validation issue
test: add workflow tests
docs: update README
```

Before pushing:

``` bash
git status
pytest
git add .
git commit -m "describe the change"
git push
```

For team integration, use pull requests rather than directly overwriting
another member's work.

------------------------------------------------------------------------

## Security

Do not commit:

``` text
.env
API keys
Database passwords
Private credentials
Sensitive datasets
Private model files
```

Use `.env.example` to document required environment variables without
exposing their values.

------------------------------------------------------------------------

## ⚖️ Limitations and Responsible Use

FatigueSense is an educational/research-oriented software project.

The system analyzes visible facial indicators and produces an
algorithmic fatigue assessment. **It is not a medical diagnostic system
and should not be used as a substitute for professional medical
evaluation.**

Lighting, camera quality, facial expression, image angle, individual
differences, and other environmental factors can affect computer-vision
results.

------------------------------------------------------------------------

## 🚀 Future Enhancements

Planned or potential improvements include:

-   Real-time video-based fatigue monitoring
-   Temporal analysis across multiple frames
-   Improved fatigue prediction models
-   More personalized recommendations
-   Larger and more diverse knowledge bases
-   Advanced memory and user-history capabilities
-   Model evaluation and benchmarking
-   Cloud deployment
-   Production monitoring and observability
-   Scalable containerized deployment
-   Stronger authentication and authorization

------------------------------------------------------------------------

## Project Objectives

FatigueSense aims to:

1.  Detect observable facial indicators associated with fatigue.
2.  Extract meaningful Computer Vision features.
3.  Combine visual analysis with knowledge retrieval.
4.  Coordinate multiple AI components through a graph-based workflow.
5.  Maintain useful analysis context and history.
6.  Present results through a modern web interface.
7.  Provide a modular architecture that can be extended and deployed.

------------------------------------------------------------------------

## Repository

**FatigueSense**

GitHub: https://github.com/nehasahu11/FatigueSense

------------------------------------------------------------------------

## Project Summary

``` text
Computer Vision
       +
AI Agents
       +
RAG
       +
LangGraph
       +
Memory
       +
FastAPI
       +
React
       +
Databases
       +
Docker
       =
FatigueSense
```

**Built as a collaborative AI engineering project.**

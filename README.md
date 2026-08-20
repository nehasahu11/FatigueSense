# FatigueSense

## 🧠 AI-Powered Facial Fatigue Analysis Platform

FatigueSense is an AI-powered fatigue analysis platform that uses computer vision, intelligent agents, Retrieval-Augmented Generation (RAG), memory, and a modern web application stack to analyze facial indicators associated with fatigue.

The system accepts facial images, extracts visual features, validates the presence of a human face, retrieves relevant fatigue-related information, calculates a fatigue score, classifies the risk level, and presents the results through a web interface.

> **Project Status:** Active development / team integration

---

## 📚 Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [System Workflow](#system-workflow)
- [Architecture](#architecture)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Backend](#backend)
- [Frontend](#frontend)
- [Computer Vision Pipeline](#computer-vision-pipeline)
- [RAG Pipeline](#rag-pipeline)
- [Fatigue Scoring](#fatigue-scoring)
- [API Endpoints](#api-endpoints)
- [Installation](#installation)
- [Environment Configuration](#environment-configuration)
- [Running the Project](#running-the-project)
- [Testing](#testing)
- [Database](#database)
- [Reference Documents](#reference-documents)
- [Development Notes](#development-notes)
- [Future Enhancements](#future-enhancements)
- [Contributing](#contributing)
- [License](#license)

---

## 🔎 Overview

Fatigue can affect concentration, reaction time, productivity, and overall performance. FatigueSense provides a software-based approach for analyzing visible facial indicators associated with fatigue.

The platform is designed around a modular architecture so that computer vision, scoring, retrieval, memory, databases, APIs, and frontend components can be developed and maintained independently.

The current analysis workflow is:

```text
User
  |
  v
Frontend
  |
  | Upload 3-4 facial images
  v
FastAPI Backend
  |
  v
FatigueWorkflow
  |
  +--> ImageAnalysisAgent
  |       |
  |       +--> Human Face Validation
  |       +--> Facial Feature Extraction
  |
  +--> RAGPipeline
  |       |
  |       +--> Retrieve relevant fatigue context
  |
  +--> FatigueScoringAgent
  |       |
  |       +--> Calculate fatigue score
  |       +--> Determine risk level
  |
  v
Result Aggregation
  |
  +--> Fatigue Score
  +--> Risk Level
  +--> Signal Breakdown
  +--> Recommendation
  +--> Analysis History
  |
  v
Frontend Dashboard
```

---

## ✨ Key Features

### 👁️ Facial Fatigue Analysis

- Facial image-based fatigue analysis
- Human face validation
- Computer vision feature extraction
- Eye-state analysis
- Eye closure detection
- Eye aspect ratio analysis
- Blink-related signals
- Mouth aspect ratio analysis
- Yawning detection
- Under-eye darkness analysis
- Dark-circle detection

### 🤖 Intelligent Analysis

- Modular agent-based architecture
- Dedicated image analysis agent
- Dedicated fatigue scoring agent
- Orchestration workflow
- RAG-based contextual retrieval
- Feature-driven RAG query generation
- Aggregated analysis across multiple images

### 📊 Results and Recommendations

- Numerical fatigue score
- Low / Medium / High risk classification
- Signal-level breakdown
- Human-readable recommendation
- Number of successfully analyzed images
- Per-image analysis information
- Timestamped analysis results

### ⚙️ Backend Services

- FastAPI REST API
- CORS support
- File upload handling
- Image validation
- Temporary file management
- In-memory user history
- API health checks
- Workflow resource cleanup

### 🖥️ Frontend

- React-based web application
- Vite development environment
- Responsive dashboard architecture
- Data visualization using Recharts
- Modern component-based UI

### 📚 Data and Retrieval

- MySQL database integration
- NoSQL database integration
- Document processing
- Vector retrieval infrastructure
- Embedding support
- Reference document storage
- RAG-related preprocessing and retrieval modules

---

## 🔄 System Workflow

### 1. Image Upload

The user uploads between 3 and 4 facial images through the frontend.

The backend validates:

- User ID
- Number of images
- File name
- File extension
- File content
- File size

Supported image formats:

```text
JPG
JPEG
PNG
```

Maximum image size:

```text
10 MB per image
```

---

### 2. Image Analysis

Each image is processed independently by the `ImageAnalysisAgent`.

The computer vision pipeline extracts facial indicators such as:

- Face presence
- Eye state
- Eye aspect ratio
- Eye closure
- Blink-related indicators
- Mouth aspect ratio
- Yawning
- Under-eye darkness
- Dark circles

If no human face is detected, the workflow stops for that image and returns a validation error.

---

### 3. RAG Retrieval

The extracted computer vision features are converted into a text-based query.

For example:

```text
fatigue assessment eye state closed
eye aspect ratio 0.18
both eyes closed
yawning fatigue
under eye darkness
```

The query is passed to the `RAGPipeline`, which retrieves relevant documents from the project's fatigue-related knowledge base.

The retrieved context can be used as supporting information for the analysis pipeline.

---

### 4. Fatigue Scoring

The `FatigueScoringAgent` processes the extracted features and calculates a fatigue score.

The score is converted into a risk category:

```text
0 - 33   -> Low
34 - 66  -> Medium
67 - 100 -> High
```

The scoring pipeline also exposes component-level contributions used to create the frontend signal breakdown.

---

### 5. Multi-Image Aggregation

When multiple images are uploaded, each image is analyzed independently.

The final fatigue score is calculated using the average of all successfully analyzed image scores.

```text
Final Score =
    Sum of Successful Image Scores
    -------------------------------
       Number of Successful Images
```

The aggregated result contains:

- Final fatigue score
- Risk level
- Recommendation
- Signal breakdown
- Images analyzed
- Image names
- Individual image analyses
- Timestamp

---

### 6. Result Presentation

The frontend receives the aggregated response and displays the analysis through the dashboard.

The UI can present:

- Overall fatigue score
- Risk level
- Signal breakdown
- Recommendations
- Analysis history
- Individual analysis information
- Visual charts

---

## 🏗️ Architecture

FatigueSense follows a modular layered architecture.

```text
+--------------------------------------------------+
|                  React Frontend                  |
|       Dashboard / Upload / History / UI          |
+--------------------------+-----------------------+
                           |
                           | REST API
                           v
+--------------------------------------------------+
|                    FastAPI                       |
|       Routes / Validation / API Responses        |
+--------------------------+-----------------------+
                           |
                           v
+--------------------------------------------------+
|              Application Services                |
|     Analysis / Upload / History / Recommendation |
+--------------------------+-----------------------+
                           |
                           v
+--------------------------------------------------+
|                 Orchestration                    |
|        FatigueWorkflow / Agent Routing           |
+-------------+-------------------+----------------+
              |                   |
              v                   v
+------------------------+   +---------------------+
| Computer Vision Agents |   |     RAG Pipeline    |
| Image Analysis Agent   |   | Load / Parse /      |
| Fatigue Scoring Agent  |   | Embed / Retrieve    |
+------------+-----------+   +----------+----------+
             |                          |
             +-------------+------------+
                           |
                           v
+--------------------------------------------------+
|             Memory / Database Layer              |
|       MySQL / NoSQL / Session / Long-Term        |
+--------------------------------------------------+
```

---

## 🛠️ Technology Stack

### 🖥️ Frontend

| Technology | Purpose |
|---|---|
| React | User interface |
| Vite | Frontend development and build tooling |
| Recharts | Data visualization |
| Lucide React | UI icons |
| Tailwind CSS | Styling |
| JavaScript / TypeScript tooling | Frontend development |

### 🔧 Backend

| Technology | Purpose |
|---|---|
| Python | Backend development |
| FastAPI | REST API framework |
| Uvicorn | ASGI server |
| Pydantic | Data validation and configuration |
| Python Multipart | File upload handling |
| Python-dotenv | Environment configuration |

### Computer Vision and Machine Learning

| Technology | Purpose |
|---|---|
| OpenCV | Image processing |
| MediaPipe | Facial landmark / vision processing |
| NumPy | Numerical computation |
| SciPy | Scientific computation |
| Pillow | Image handling |
| scikit-learn | Machine learning utilities |
| PyTorch | ML / deep learning support |
| Transformers | Transformer-based ML support |
| Sentence Transformers | Text embeddings |

### RAG and Retrieval

| Technology | Purpose |
|---|---|
| ChromaDB | Vector storage / retrieval |
| Rank-BM25 | Keyword-based retrieval |
| PyPDF | PDF processing |
| PyMuPDF | PDF/document processing |
| Sentence Transformers | Embedding generation |

### 🗄️ Database

| Technology | Purpose |
|---|---|
| MySQL | Relational data storage |
| SQLAlchemy | Database ORM |
| PyMySQL | MySQL connectivity |
| Firebase Admin | Firebase integration |
| NoSQL components | Document-oriented storage |

### 🧪 Testing

| Technology | Purpose |
|---|---|
| pytest | Python testing |
| pytest-asyncio | Async testing |
| HTTPX | API testing |

---

## 📁 Project Structure

```text
FatigueSense/
|
+-- backend/
|   |
|   +-- app/
|   |   |
|   |   +-- agents/
|   |   |   +-- image_analysis_agent.py
|   |   |   +-- fatigue_scoring_agent.py
|   |   |
|   |   +-- api/
|   |   |   +-- __init__.py
|   |   |   +-- dependencies.py
|   |   |   +-- routes/
|   |   |       +-- analyze.py
|   |   |       +-- documents.py
|   |   |       +-- health.py
|   |   |       +-- history.py
|   |   |       +-- upload.py
|   |   |
|   |   +-- cv/
|   |   |   +-- Facial analysis modules
|   |   |
|   |   +-- database/
|   |   |   +-- mysql/
|   |   |   +-- nosql/
|   |   |
|   |   +-- memory/
|   |   |   +-- context_manager.py
|   |   |   +-- long_term_memory.py
|   |   |   +-- memory_manager.py
|   |   |   +-- session_memory.py
|   |   |
|   |   +-- orchestration/
|   |   |   +-- agent_router.py
|   |   |   +-- state.py
|   |   |   +-- workflow.py
|   |   |   +-- workflow_config.py
|   |   |
|   |   +-- preprocessing/
|   |   |
|   |   +-- rag/
|   |   |   +-- chunking/
|   |   |   +-- embeddings/
|   |   |   +-- loaders/
|   |   |   +-- parsers/
|   |   |   +-- preprocessing/
|   |   |   +-- retrieval/
|   |   |   +-- vector_store/
|   |   |
|   |   +-- schemas/
|   |   +-- services/
|   |   +-- utils/
|   |
|   +-- data/
|   |   +-- chunks/
|   |   +-- embeddings/
|   |   +-- models/
|   |   +-- reference_documents/
|   |   |   +-- json/
|   |   |   +-- pdf/
|   |   |   +-- txt/
|   |   +-- test_images/
|   |
|   +-- scripts/
|   +-- tests/
|   +-- requirements.txt
|   +-- run.py
|
+-- database/
|   |
|   +-- mysql/
|   |   +-- schema.sql
|   |   +-- tables.sql
|   |   +-- indexes.sql
|   |   +-- seed.sql
|   |
|   +-- nosql/
|
+-- frontend/
|   +-- src/
|   +-- public/
|   +-- package.json
|   +-- vite.config.*
|
+-- .github/
|   +-- workflows/
|
+-- README.md
```

> Generated `__pycache__` directories and compiled Python files are intentionally excluded from the project structure above.

---

## 🔧 Backend

The backend is implemented using FastAPI and provides the application API layer.

### Main Backend Responsibilities

- Accept image uploads
- Validate requests
- Execute the fatigue-analysis workflow
- Coordinate AI agents
- Execute RAG retrieval
- Aggregate multiple image results
- Generate recommendations
- Maintain analysis history
- Provide health checks
- Handle temporary uploaded files
- Manage workflow resources

### Main Workflow Class

The primary orchestration class is:

```python
FatigueWorkflow
```

Located at:

```text
backend/app/orchestration/workflow.py
```

The workflow coordinates:

```text
ImageAnalysisAgent
        |
        v
Face Validation
        |
        v
RAGPipeline
        |
        v
FatigueScoringAgent
        |
        v
Final Analysis Result
```

---

## 🖥️ Frontend

The frontend is a React + Vite application.

The frontend communicates with the FastAPI backend using HTTP requests.

The frontend package includes:

- React
- React DOM
- Vite
- Recharts
- Lucide React
- Tailwind CSS
- ESLint
- TypeScript tooling

### 🖥️ Frontend Commands

Install dependencies:

```bash
cd frontend
npm install
```

Start development server:

```bash
npm run dev
```

Create production build:

```bash
npm run build
```

Preview production build:

```bash
npm run preview
```

Run linting:

```bash
npm run lint
```

---

## 👁️ Computer Vision Pipeline

The computer vision layer is responsible for extracting visual signals from facial images.

### Eye Analysis

The system can use eye-related measurements such as:

- Eye state
- Average eye aspect ratio
- Left eye closure
- Right eye closure
- Both-eye closure
- Possible blink

### Mouth Analysis

The system can analyze:

- Mouth aspect ratio
- Mouth opening
- Yawn detection

### Under-Eye Analysis

The pipeline can analyze:

- Under-eye darkness
- Dark-circle presence
- Average under-eye darkness

These signals are passed into the fatigue scoring process.

---

## 📖 RAG Pipeline

FatigueSense includes a Retrieval-Augmented Generation infrastructure for retrieving relevant information from reference material.

The RAG subsystem contains modules for:

```text
Document Loading
       |
       v
Parsing
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
```

Reference documents can be organized under:

```text
backend/data/reference_documents/
```

Supported document categories include:

```text
PDF
TXT
JSON
```

The workflow generates a query from extracted facial features and sends it to the RAG pipeline.

---

## 📈 Fatigue Scoring

The fatigue scoring layer converts extracted facial signals into a fatigue score.

The resulting score is categorized into three risk levels:

| Score | Risk Level |
|---:|---|
| 0-33 | Low |
| 34-66 | Medium |
| 67-100 | High |

The scoring components can contribute to the frontend signal breakdown.

The API can expose signals such as:

- Eye Closure
- Eye State
- Blink / Eye Closure
- Yawn
- Under-Eye Darkness

The score should be interpreted as a software-generated indicator rather than a medical diagnosis.

---

## 🔌 API Endpoints

The backend exposes REST endpoints for application functionality.

### Root

```http
GET /
```

Returns basic API information.

### Health Check

```http
GET /health
```

Returns the service health status.

### Analyze

```http
POST /analyze
```

Accepts:

- `user_id`
- 3-4 image files

Example request structure:

```text
multipart/form-data

user_id: user123
images: image1.jpg
images: image2.jpg
images: image3.jpg
```

### History

```http
GET /history?user_id=user123
```

Returns the latest analysis history for the requested user.

### API Documentation

When the backend is running, FastAPI automatically provides:

```text
/docs
/redoc
```

---

## 🚀 Installation

### Prerequisites

Install the following before running the project:

- Python 3.10+
- Node.js and npm
- Git
- MySQL, if database functionality is enabled
- Required computer vision model files

---

## 📥 Clone the Repository

```bash
git clone <repository-url>
cd FatigueSense
```

---

## 🔧 Backend Setup

Create and activate a virtual environment.

### Windows PowerShell

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell execution policy prevents activation:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
.\.venv\Scripts\Activate.ps1
```

Install backend dependencies:

```powershell
pip install -r backend\requirements.txt
```

---

## 🔐 Environment Configuration

Create an environment file as required by the project configuration.

Example:

```env
# Application
APP_ENV=development

# Database
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=your_password
MYSQL_DATABASE=fatiguesense

# NoSQL / Firebase
# Add credentials required by the enabled integration.

# RAG
# Add model/vector-store configuration required by the deployment.
```

Do not commit secrets, API keys, passwords, private credentials, or service-account files to Git.

---

## 🧩 Required Model Files

The workflow expects the model directory at:

```text
backend/data/models/
```

The directory must exist before the workflow is initialized.

If the required MediaPipe or other model files are missing, the backend workflow may fail during startup or image analysis.

---

## ▶️ Running the Backend

From the project root:

```powershell
.\.venv\Scripts\Activate.ps1
uvicorn backend.app.main:app --reload
```

Depending on the final backend entry point configured in the repository, the project can also be started using:

```powershell
python backend/run.py
```

The API is normally available at:

```text
http://127.0.0.1:8000
```

FastAPI documentation:

```text
http://127.0.0.1:8000/docs
```

---

## ▶️ Running the Frontend

Open another terminal:

```powershell
cd frontend
npm install
npm run dev
```

Vite will display the local frontend URL in the terminal.

The frontend communicates with the backend API according to the configured API base URL.

---

## 🚀 Running the Complete Project

Open two terminals.

### Terminal 1 - Backend

```powershell
.\.venv\Scripts\Activate.ps1
uvicorn backend.app.main:app --reload
```

### Terminal 2 - Frontend

```powershell
cd frontend
npm run dev
```

Then open the frontend URL shown by Vite.

---

## 🧪 Testing

Backend tests use `pytest`.

Run all tests:

```powershell
pytest
```

Run tests from the backend directory if required:

```powershell
cd backend
pytest
```

For asynchronous tests:

```powershell
pytest -v
```

The repository also contains GitHub Actions workflow configuration for automated testing.

---

## 🗄️ Database

FatigueSense contains database infrastructure for both relational and document-oriented storage.

### MySQL

Database scripts are located at:

```text
database/mysql/
```

Typical files include:

```text
schema.sql
tables.sql
indexes.sql
seed.sql
```

The backend database layer is located at:

```text
backend/app/database/mysql/
```

It contains database connection, model, and CRUD functionality.

### NoSQL

NoSQL infrastructure is located at:

```text
backend/app/database/nosql/
```

and:

```text
database/nosql/
```

The NoSQL layer supports document-oriented data structures used by the application architecture.

---

## 🧠 Memory System

FatigueSense includes a modular memory layer:

```text
backend/app/memory/
```

The memory subsystem contains components for:

- Session memory
- Long-term memory
- Context management
- Memory management

This architecture allows user-related analysis context to be managed separately from the core computer vision pipeline.

---

## 🗂️ Data Organization

Application data is organized under:

```text
backend/data/
```

### Chunks

```text
backend/data/chunks/
```

Stores processed document chunks used by the retrieval pipeline.

### Embeddings

```text
backend/data/embeddings/
```

Stores embedding-related data generated for retrieval.

### Models

```text
backend/data/models/
```

Stores required model files.

### Reference Documents

```text
backend/data/reference_documents/
```

Contains source material for the RAG pipeline.

### Test Images

```text
backend/data/test_images/
```

Contains images used during development and testing.

---

## 🛡️ Error Handling

The backend validates uploaded images before analysis.

Validation includes:

- Missing user ID
- Incorrect number of images
- Missing filenames
- Unsupported file extensions
- Empty files
- Files larger than 10 MB
- Images without a detectable human face
- Workflow analysis failures

Temporary uploaded files are removed after processing.

---

## 🔒 Security Considerations

The application includes several basic protections:

- Filename sanitization
- File extension validation
- File size limits
- Temporary upload cleanup
- CORS configuration
- Environment-based configuration
- Separation of application and database layers

For production deployment, additional security controls should be added, including:

- Authentication and authorization
- Rate limiting
- Secure production CORS configuration
- HTTPS
- Request validation
- Secure secret management
- Database access controls
- Production logging and monitoring

---

## 🔏 Privacy Considerations

FatigueSense processes facial images, which can be sensitive data.

For production use:

- Do not store facial images longer than necessary.
- Use secure transport.
- Protect stored analysis data.
- Avoid committing user images to Git.
- Restrict access to uploaded data.
- Clearly communicate how analysis data is processed.
- Follow applicable privacy and data-protection requirements.

The current workflow removes temporary uploaded image files after analysis.

---

## 👨‍💻 Development Notes

The repository is structured to support team-based development.

Major application areas are separated into:

```text
agents
api
cv
database
memory
orchestration
preprocessing
rag
schemas
services
utils
```

This separation allows individual components to evolve without placing all application logic in a single file.

The orchestration layer acts as the central coordinator between image analysis, retrieval, scoring, and final result generation.

---

## 🔮 Future Enhancements

Potential future improvements include:

- Real-time webcam fatigue monitoring
- Video-based fatigue analysis
- Temporal fatigue tracking
- Improved personalization
- More advanced fatigue scoring models
- Expanded RAG knowledge base
- Better retrieval evaluation
- Persistent user history
- Authentication and authorization
- Advanced analytics dashboard
- Notification and alert system
- Model performance monitoring
- Cloud deployment
- Containerized deployment using Docker
- Production-grade observability
- Automated model evaluation

---

## 👥 Team Development

For team development, use feature branches rather than committing directly to the main integration branch.

Recommended workflow:

```bash
git checkout team-integration
git pull origin team-integration

git checkout -b feature/your-feature

# Make changes

git add .
git commit -m "Add your feature"

git push origin feature/your-feature
```

Create a Pull Request and merge the feature after review.

Before pushing an integration branch:

```bash
git status
git pull origin team-integration
```

Resolve conflicts carefully if Git reports unmerged paths.

---

## 🩺 Troubleshooting

### 🔧 Backend does not start

Check:

```bash
python --version
pip --version
```

Then reinstall dependencies:

```powershell
pip install -r backend\requirements.txt
```

Verify that the model directory exists:

```text
backend/data/models/
```

---

### 🖥️ Frontend does not start

Run:

```powershell
cd frontend
npm install
npm run dev
```

If dependencies are corrupted, remove `node_modules` and reinstall:

```powershell
Remove-Item -Recurse -Force node_modules
npm install
```

---

### API is running but frontend cannot connect

Verify that the backend is running and check:

```text
http://127.0.0.1:8000/docs
```

Then verify the frontend API base URL and CORS configuration.

---

### Image upload fails

Verify:

- 3-4 images are selected
- Images are JPG, JPEG, or PNG
- Each image is below 10 MB
- Files contain a visible human face
- Backend is running
- Required computer vision model files are available

---

### RAG retrieval fails

Check:

- Reference documents are available
- Required embedding models are installed
- Vector-store configuration is correct
- Required data directories exist

---

## 📄 License

This project is developed as an academic/team software project.

Add the project's final license here before public distribution.

---

## 📌 Project Summary

FatigueSense brings together computer vision, AI agents, retrieval, memory, backend services, databases, and a modern React interface into a modular fatigue-analysis platform.

The system is designed to transform facial indicators into an interpretable fatigue assessment while maintaining a clear separation between image processing, intelligent analysis, retrieval, scoring, API services, and presentation.

---

**FatigueSense**  
**🧠 AI-Powered Facial Fatigue Analysis Platform**

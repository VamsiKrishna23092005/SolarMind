# Enhanced SolarMind Pipeline

This is a production-ready, fully open-source implementation of the SolarMind pipeline. It uses completely free, locally hostable components including **Ollama** (for local LLMs), **ChromaDB** (for vector storage), **DuckDuckGo search** (for web research), **Florence-2** (for visual analysis of graphs), and **LangGraph** (for orchestrating the agent workflows with parallel execution and SQLite checkpointer persistence).

## Architecture

The project is structured into multiple phases:
- **Phase 1: Environment & Core Architecture** (`solarmind/state.py`, `solarmind/graph.py`) - State, nodes, and LangGraph routing.
- **Phase 2: Domain-Specific RAG Pipeline** (`solarmind/rag.py`) - Ingesting and querying papers (e.g., Solar forecasting, PatchTST) via ChromaDB.
- **Phase 3: Critic & Feedback Loops** (`solarmind/graph.py`) - Iterative improvement and conditional edges.
- **Phase 4: Human-in-the-Loop & UI** (`app.py`, `solarmind/vision.py`) - Streamlit dashboard, interrupt handling before final output, and multimodal Florence-2 graph analysis.
- **Phase 5: Evaluation & Deployment** (`api.py`, `test_pipeline.py`, `Dockerfile`) - Pytest, FastAPI wrapper, and Dockerization.
- **Pro Differentiator:** Parallel researcher execution using LangGraph's Send API for Market, Tech, and Policy research.

---

## 🛠 Prerequisites

Before starting, ensure you have the following installed:
1. **Python 3.10+**
2. **[Ollama](https://ollama.com/)** running locally

### Pull Necessary Local Models in Ollama
Make sure your local Ollama instance has the required models downloaded:
```bash
ollama pull llama3
ollama pull nomic-embed-text
```

---

## 🚀 Setup & Installation

**1. Navigate to the project directory**
```bash
cd "d:\18 march genai project"
```

**2. Create and activate a Virtual Environment (Optional but Recommended)**
```bash
python -m venv venv

# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate
```

**3. Install Dependencies**
```bash
pip install -r requirements.txt
```

---

## ▶ Running the Pipeline

You have several ways to run and interact with the SolarMind Pipeline:

### Option A: The Visual Dashboard (Streamlit)
Launch the interactive Human-in-the-Loop dashboard. Here you can run parallel researcher agents, interrupt generation for human review, and run local visual models on solar data graphs.
```bash
streamlit run app.py
```
> *Note: The first time you use the multimodal vision feature (Florence-2), it will download the model weights (~1-2GB).*

### Option B: The API Server (FastAPI)
Run the production-ready API wrapper to integrate the LangGraph agent DAG natively into other services.
```bash
uvicorn api:app --reload
```
Once it's running, you can test endpoints at: `http://localhost:8000/docs`. To invoke via POST:
```bash
curl -X 'POST' \
  'http://localhost:8000/invoke' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "research_query": "solar panel irradiance trends 2024",
  "thread_id": "api-thread-1"
}'
```

### Option C: Run Tests (Pytest)
Validate the LangGraph critic logic and loop conditions.
```bash
pytest test_pipeline.py
```

---

## 🐳 Running with Docker

You can build and run this entire stack via Docker.
**1. Build Check**
```bash
docker build -t solarmind .
```
**2. Run Interactive UI Container**
```bash
docker run -p 8501:8501 -p 8000:8000 solarmind
```
> *Important: Ensure Ollama is reachable from within the Docker container (you might need to adjust network settings or point the Langchain Ollama URL to `host.docker.internal` instead of localhost).*

---

## 💡 Using Domain-specific RAG (ChromaDB)

To prime the AI with specific data (e.g., technical PDFs on PatchTST efficiency):
1. Write a simple Python script to point `ingest_papers(paper_paths)` inside `solarmind/rag.py` to your local files.
2. The pipeline handles automatic semantic search extraction using locally computed `nomic-embed-text` embeddings.

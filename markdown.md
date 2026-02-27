# LLM Evaluator - Project Structure

## 📁 Complete Folder Structure

llm-evaluator/
│
├── Dockerfile # Multi-stage Python container
├── docker-compose.yml # Postgres/pgvector + Redis + API
├── requirements.txt # All Python dependencies
│
├── app/
│ ├── main.py # FastAPI app + endpoints
│ ├── models.py # Pydantic schemas
│ ├── database.py # SQLAlchemy + pgvector init
│ ├── kb_service.py # LlamaIndex + file parsing
│ ├── eval_service.py # DeepEval + LiteLLM
│ └── tasks.py # Celery async ingestion
│
├── data/ # Docker volumes (auto-created)
│ └── sessions/ # /data/sessions/{session_id}/docs/
│
└── README.md # This file + Quick Start


## 🚀 Quick Start

```bash
mkdir llm-evaluator && cd llm-evaluator
# Copy all code files from conversation
echo "OPENAI_API_KEY=sk-your-key" > .env

docker compose up --build


📋 File Details Table
| File               | Purpose              | Key Features                     |
| ------------------ | -------------------- | -------------------------------- |
| Dockerfile         | Production container | Multi-stage, ~250MB              |
| docker-compose.yml | Local stack          | pgvector + Redis + API           |
| main.py            | FastAPI Core         | /sessions, /kb/upload, /evaluate |
| kb_service.py      | RAG Pipeline         | PDF/Excel → pgvector per-session |
| eval_service.py    | Metrics Engine       | DeepEval + 100+ LLMs via LiteLLM |

🗃️ Docker Volumes (Auto-Created)

sessions_data/      # /data/sessions/{uuid}/docs/
pgdata/             # Postgres + pgvector tables  
redis/              # Celery queues


🔗 API Endpoints

POST /sessions                    # → { "session_id": "uuid" }
POST /sessions/{id}/kb/upload     # Upload PDF/Excel (async)
POST /sessions/{id}/evaluate      # RAG → LLM → Metrics
GET /health                       # Status check


🛠️ Tech Stack

FastAPI + Uvicorn
LlamaIndex + pgvector (session-isolated)
DeepEval + LiteLLM (multi-LLM)
Celery + Redis (async ingestion)
PyMuPDF + pandas (PDF/Excel parsing)
Docker → OCP-ready


☁️ Production Path

docker compose → kubectl apply -f k8s/
PVC → /data/sessions
HPA → Auto-scale pods
Ingress → Load balancer
Secrets → LLM API keys


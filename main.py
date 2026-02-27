# main.py
from fastapi import FastAPI, UploadFile, File, Depends, HTTPException, Path
from fastapi.responses import JSONResponse
import uuid
import shutil
from pathlib import Path
import os
from models import CreateSession, EvaluateRequest
from kb_service import KBService
from eval_service import EvalService
from database import get_db
from tasks import celery_app
import json

app = FastAPI(title="Session LLM Evaluator")
kb_service = KBService(os.getenv("DATABASE_URL"))
eval_service = EvalService()

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.post("/sessions", response_model=dict)
def create_session():
    session_id = str(uuid.uuid4())
    init_session_table(session_id)
    return {"session_id": session_id, "message": "Session created"}

@app.post("/sessions/{session_id}/kb/upload")
async def upload_kb(
    session_id: str = Path(..., description="Session ID"),
    files: list[UploadFile] = File(...)
):
    session_dir = Path("/data/sessions") / session_id / "docs"
    session_dir.mkdir(parents=True, exist_ok=True)
    
    doc_paths = []
    for file in files:
        path = session_dir / file.filename
        with open(path, "wb") as f:
            shutil.copyfileobj(file.file, f)
        doc_paths.append(str(path))
    
    celery_app.send_task("ingest_session_kb", args=[session_id, doc_paths])
    return {"status": "uploaded", "doc_paths": doc_paths}

@app.post("/sessions/{session_id}/evaluate")
def evaluate(
    session_id: str = Path(...),
    req: EvaluateRequest = Depends()
):
    try:
        results = eval_service.run_eval(session_id, req.query, req.models, kb_service, req.ground_truth)
        return results
    except Exception as e:
        raise HTTPException(500, str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

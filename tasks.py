# tasks.py
from celery import Celery
from kb_service import KBService
import os

celery_app = Celery("tasks", broker=os.getenv("REDIS_URL"))

@celery_app.task
def ingest_session_kb(session_id: str, doc_paths: list):
    kb_service = KBService(os.getenv("DATABASE_URL"))
    kb_service.ingest_kb(session_id, doc_paths)

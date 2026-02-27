# database.py
import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
import uuid

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

@contextmanager
def get_db():
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()

def init_session_table(session_id: str):
    table = f"kb_vectors_{session_id.replace('-', '_')}"
    with engine.connect() as conn:
        conn.execute(text(f"""
            CREATE TABLE IF NOT EXISTS {table} (
                id TEXT PRIMARY KEY,
                embedding VECTOR(384),
                text TEXT,
                metadata JSONB
            );
            CREATE INDEX IF NOT EXISTS idx_{table}_hnsw ON {table} USING hnsw (embedding vector_cosine_ops);
        """))
        conn.commit()
    return table

# kb_service.py
from llama_index.core import Document, VectorStoreIndex, StorageContext
from llama_index.vector_stores.postgres import PGVectorStore
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
import fitz  # PyMuPDF
import pandas as pd
from pathlib import Path
import os

embed_model = HuggingFaceEmbedding(model_name="sentence-transformers/all-MiniLM-L6-v2")

class KBService:
    def __init__(self, db_url: str):
        self.db_url = db_url
    
    def ingest_kb(self, session_id: str, doc_paths: list):
        table = init_session_table(session_id)
        vector_store = PGVectorStore.from_params(
            database=self.db_url, table_name=table,
            embed_dim=384
        )
        
        docs = []
        for path in doc_paths:
            if path.endswith('.pdf'):
                doc = fitz.open(path)
                text = "\n".join([page.get_text() for page in doc])
                docs.append(Document(text=text[:10000], metadata={"file": path}))
            elif path.endswith(('.xlsx', '.xls')):
                df = pd.read_excel(path)
                text = df.to_string()
                docs.append(Document(text=text[:10000], metadata={"file": path}))
        
        index = VectorStoreIndex.from_documents(
            docs, storage_context=StorageContext.from_defaults(vector_store=vector_store)
        )
    
    def retrieve(self, session_id: str, query: str, top_k=3):
        table = init_session_table(session_id)
        vector_store = PGVectorStore.from_params(database=self.db_url, table_name=table)
        index = VectorStoreIndex.from_vector_store(vector_store)
        retriever = index.as_retriever(similarity_top_k=top_k)
        return retriever.retrieve(query)

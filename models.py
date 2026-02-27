# models.py
from pydantic import BaseModel
from typing import List, Optional
from enum import Enum

class LLMModel(str, Enum):
    gpt4o = "openai/gpt-4o-mini"
    claude = "anthropic/claude-3-5-sonnet-20240620"

class CreateSession(BaseModel):
    pass  # Returns session_id

class UploadRequest(BaseModel):
    pass  # Files via multipart

class EvaluateRequest(BaseModel):
    query: str
    models: List[LLMModel] = [LLMModel.gpt4o]
    ground_truth: Optional[str] = None

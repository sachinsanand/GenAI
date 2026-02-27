# eval_service.py
from deepeval.metrics import FaithfulnessMetric
from deepeval.test_case import LLMTestCase
from deepeval import evaluate
from litellm import completion
import os
import json
from typing import Dict

class EvalService:
    def __init__(self):
        self.metric = FaithfulnessMetric(threshold=0.7)
    
    def generate(self, model: str, messages: list) -> str:
        response = completion(model=model, messages=messages, temperature=0)
        return response.choices[0].message.content
    
    def compute_metrics(self, output: str, context: str, ground_truth: str = "") -> Dict:
        test_case = LLMTestCase(input="", actual_output=output, retrieval_context=[context])
        result = evaluate([test_case], [self.metric])[0]
        return {"faithfulness": result.score, "reason": result.reason}
    
    def run_eval(self, session_id: str, query: str, models: list, kb_service, ground_truth: str = "") -> Dict:
        nodes = kb_service.retrieve(session_id, query)
        context = "\n".join([n.text for n in nodes])
        
        results = {}
        for model in models:
            response = self.generate(model, [{"role": "user", "content": f"Query: {query}\nContext: {context}"}])
            metrics = self.compute_metrics(response, context, ground_truth)
            results[model] = {"response": response, "metrics": metrics}
        
        return results

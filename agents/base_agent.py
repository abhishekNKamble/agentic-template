# agents/base_agent.py
from models.model_client import ModelClient

class BaseAgent:
    def __init__(self, model_client: ModelClient):
        self.model = model_client

    def run(self, task: str):
        prompt = f"""You are an SDET-focused Test Case Generator AI.

Requirement:
{task}

Produce a JSON array of test cases. For each test case include:
- id
- category
- objective
- preconditions
- steps (array)
- expected_result

Generate functional, negative, and boundary tests where applicable.
Return ONLY valid JSON (no explanation or markdown).
"""
        return self.model.generate(prompt)

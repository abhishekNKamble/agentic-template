# agents/reflection_agent.py
import json
from models.model_client import ModelClient

class ReflectionAgent:
    def __init__(self, model_client: ModelClient):
        self.model = model_client

    def review(self, testcases_json, reflection_model=None):
        # testcases_json should be a Python list or JSON string
        if isinstance(testcases_json, list):
            payload = json.dumps(testcases_json, indent=2)
        else:
            payload = str(testcases_json)

        prompt = f"""You are a JSON validation and correction agent.

Here is a list of test cases (JSON). Ensure the output is a valid JSON array of objects with fields:
id, category, objective, preconditions, steps (array), expected_result.
- Fix obvious issues (missing fields, steps not an array, minor typos).
- Do NOT change the intent of test cases.
- Return ONLY the corrected JSON array.

Input JSON:
{payload}
"""

        model_name = reflection_model
        resp = self.model.generate(prompt, model_name=model_name)
        # attempt to parse; if fails, return empty list for the caller to handle
        try:
            return json.loads(resp)
        except Exception:
            # ask model to repair into strict JSON
            repair_prompt = f"Convert the following into strict JSON array only (no commentary):\n\n{resp}"
            repaired = self.model.generate(repair_prompt, model_name=model_name)
            try:
                return json.loads(repaired)
            except Exception:
                return []

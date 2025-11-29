# models/model_client.py
import requests
import os
import json
from config import MODEL_BACKEND, MODEL_NAME, OPENAI_MODEL, OPENAI_API_KEY, REFLECTION_MODEL

OLLAMA_BASE = os.environ.get("OLLAMA_BASE", "http://localhost:11434")

class ModelClient:
    def __init__(self, backend=None):
        self.backend = backend or MODEL_BACKEND
        # default names; user may override when calling
        self.default_model = MODEL_NAME
        self.reflection_model = REFLECTION_MODEL

    def generate(self, prompt: str, model_name: str = None, max_tokens: int = 1500, temperature: float = 0.2):
        model = model_name or self.default_model
        if self.backend == "ollama":
            return self._generate_ollama(prompt, model=model, max_tokens=max_tokens, temperature=temperature)
        else:
            return self._generate_openai(prompt, model_name=model, max_tokens=max_tokens, temperature=temperature)

    def _generate_ollama(self, prompt: str, model: str, max_tokens: int, temperature: float):
        # Ollama API: POST /api/generate
        url = f"{OLLAMA_BASE}/api/generate"
        payload = {
            "model": model,
            "prompt": prompt,
            "options": {
                "temperature": temperature,
                "num_predict": max_tokens
            },
            "stream": False
        }
        resp = requests.post(url, json=payload, timeout=300)
        resp.raise_for_status()
        data = resp.json()
        # Try common response locations
        # Newer Ollama returns "response" (string); some versions return dict with 'choices'->text
        if isinstance(data, dict):
            if "response" in data:
                return data["response"]
            if "choices" in data and len(data["choices"]) > 0:
                c = data["choices"][0]
                # support either 'text' or 'content' keys
                return c.get("text") or c.get("content") or json.dumps(c)
        # Fallback: return raw text
        return str(data)

    def _generate_openai(self, prompt: str, model_name: str, max_tokens: int, temperature: float):
        # Minimal OpenAI wrapper using openai package if available; fallback to environment-based usage
        try:
            from openai import OpenAI
            client = OpenAI(api_key=OPENAI_API_KEY or os.environ.get("OPENAI_API_KEY"))
            resp = client.chat.completions.create(
                model=model_name,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=max_tokens,
                temperature=temperature
            )
            # Extract textual content
            return resp.choices[0].message["content"]
        except Exception as e:
            # As a last resort, raise an informative error
            raise RuntimeError("OpenAI generation failed. Set OPENAI_API_KEY or use Ollama local backend.") from e

# Minimal Agentic AI Template (Ollama default)

This repository is a minimal, GitHub-ready template demonstrating an **Agentic AI** pattern:
- Base Agent (generates content)
- Reflection Agent (validates & improves)
- Pluggable model backend: Ollama (local) or OpenAI (cloud)

## Quickstart

1. Clone or download this repo.
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. If using **Ollama** (recommended for local experimentation):
   - Install and run Ollama server (see https://ollama.com)
   - Pull models, e.g.:
     ```
     ollama pull qwen2.5:14b-instruct
     ollama pull qwen3:7b-instruct
     ```
4. Run:
   ```
   python main.py
   ```

## Configuration

Edit `config.py` to switch backend or model names.
Default backend = Ollama.

## Files

- `models/model_client.py` : abstracts model calls (Ollama/OpenAI)
- `agents/base_agent.py` : base test-case generator
- `agents/reflection_agent.py` : reflection/repair agent
- `main.py` : example runner and Excel export

## Notes

- This template is intentionally minimal and educational — production systems need more error handling, authentication, rate-limiting, and observability.

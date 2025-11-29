# config.py
# Default to local Ollama backend; fallback to OpenAI if configured.

MODEL_BACKEND = "ollama"   # "ollama" or "openai"
MODEL_NAME = "qwen2.5:14b-instruct"  # default Ollama model for generation
REFLECTION_MODEL = "qwen3:7b-instruct"  # reflection model (local)

# OpenAI fallback settings (only used if MODEL_BACKEND == "openai")
OPENAI_MODEL = "gpt-4.1-mini"
OPENAI_API_KEY = ""  # set via environment variable or fill here

import os

from dotenv import load_dotenv
from openai import OpenAI
from sentence_transformers import SentenceTransformer


# ===========================================
# Load Environment Variables
# ===========================================

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "").strip()
requested_provider = os.getenv("LLM_PROVIDER", "auto").strip().lower()

if requested_provider not in {"auto", "openrouter", "ollama"}:
    raise SystemExit("Set LLM_PROVIDER to openrouter, ollama, or auto in .env.")

if requested_provider == "openrouter" or (requested_provider == "auto" and OPENROUTER_API_KEY):
    if not OPENROUTER_API_KEY:
        raise SystemExit(
            "Create an OpenRouter API key at https://openrouter.ai/keys "
            "and set OPENROUTER_API_KEY in .env or your terminal environment."
        )
    PROVIDER_NAME = "OpenRouter"
    MODEL_NAME = os.getenv("OPENROUTER_MODEL", "openrouter/free")
    completion_options = {}
    client = OpenAI(
        api_key=OPENROUTER_API_KEY,
        base_url="https://openrouter.ai/api/v1",
        timeout=60,
        max_retries=0,
    )
else:
    PROVIDER_NAME = "Ollama"
    MODEL_NAME = os.getenv("OLLAMA_MODEL", "qwen3.5:9b")
    completion_options = {
        "extra_body": {"reasoning_effort": "none"},
        "max_tokens": 512,
    }
    client = OpenAI(
        api_key="ollama",
        base_url="http://127.0.0.1:11434/v1",
        timeout=240,
        max_retries=0,
    )


# ===========================================
# LLM Helper Function
# ===========================================

def generate_response(prompt: str) -> str:
    """
    Send a prompt to the configured provider
    and return the generated text.
    """

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2,
        **completion_options,
    )

    if response.choices and response.choices[0].message.content:
        return response.choices[0].message.content
    return f"{PROVIDER_NAME} returned no answer. Try again or select another model."


# ===========================================
# Load Embedding Model
# ===========================================

print("\nLoading Embedding Model...")

embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

print("Embedding Model Loaded Successfully!")


# ===========================================
# Embedding Helper Function
# ===========================================

def get_embedding(text):
    """
    Generate a sentence embedding using
    SentenceTransformer.
    """

    return embedding_model.encode(text)

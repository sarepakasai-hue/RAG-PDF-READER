from openai import (
    APIConnectionError,
    APIStatusError,
    APITimeoutError,
    AuthenticationError,
    NotFoundError,
    RateLimitError,
)

from config import MODEL_NAME, PROVIDER_NAME, generate_response


def generate_answer(prompt):

    print("\n" + "=" * 60)
    print(f"STEP 8 : {PROVIDER_NAME.upper()} GENERATING ANSWER")
    print("=" * 60)

    try:

        return generate_response(prompt)

    except APITimeoutError:
        if PROVIDER_NAME == "Ollama":
            return (
                f"Timed out waiting for Ollama to answer with {MODEL_NAME}. "
                "Run ollama ps in another terminal to check whether the model is loaded."
            )
        return "Timed out waiting for OpenRouter to answer."

    except APIConnectionError:
        if PROVIDER_NAME == "Ollama":
            return "Could not reach Ollama. Open the Ollama app or run ollama serve."
        return "Could not reach OpenRouter. Check your internet connection."

    except AuthenticationError:
        return (
            f"{PROVIDER_NAME} rejected the API credentials. "
            "For OpenRouter, check OPENROUTER_API_KEY or create a key at "
            "https://openrouter.ai/keys."
        )

    except RateLimitError:
        return f"{PROVIDER_NAME} rate limit reached for {MODEL_NAME}. Try again later."

    except NotFoundError:
        if PROVIDER_NAME == "Ollama":
            return f"Ollama could not find {MODEL_NAME}. Run ollama pull {MODEL_NAME}."
        return f"OpenRouter could not find {MODEL_NAME}. Check OPENROUTER_MODEL."

    except APIStatusError as error:
        if PROVIDER_NAME == "OpenRouter" and error.status_code == 402:
            return "OpenRouter reported insufficient credits. Check OPENROUTER_MODEL and your balance."
        return f"{PROVIDER_NAME} could not generate an answer (HTTP {error.status_code})."

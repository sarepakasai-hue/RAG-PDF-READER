# PDF Chatbot

The chatbot reads `data/sample.pdf` and answers questions in your terminal.

## Run on macOS

Choose an answer provider in the `.env` file in the project folder:

- **OpenRouter** — [Create an API key](https://openrouter.ai/keys), set
  `LLM_PROVIDER=openrouter`, and paste your key after `OPENROUTER_API_KEY=`.
  Keep the key in the Git-ignored `.env` or your terminal environment.
  The default is `openrouter/free`. To select another model, copy its slug
  from the [model catalog](https://openrouter.ai/models) into `OPENROUTER_MODEL`.
- **Ollama** — Set `LLM_PROVIDER=ollama`, open the Ollama app or run
  `ollama serve` in a separate terminal, and set `OLLAMA_MODEL` to the exact
  name shown by `ollama list`. The default is `qwen3.5:9b`.
- **Auto** — Set `LLM_PROVIDER=auto` to use OpenRouter when a key is present
  and Ollama otherwise. This is also the default when the setting is absent.

Restart `python app.py` after changing providers. OpenRouter receives the
question and retrieved PDF excerpts, while Ollama processes them locally.

Run these commands from the project folder using Python 3.13:

```sh
python3.13 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python app.py
```

Wait for `Ask Question (exit to quit):`, then try
`What architecture does the paper introduce?`. Enter `exit` to quit.

The embedding model downloads on the first run if it is not cached.

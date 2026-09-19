## Local startup

Start the AI API on the canonical local address:

```bash
uv run uvicorn app.main:app --host 127.0.0.1 --port 3000
```

The API is available at `http://127.0.0.1:3000/api/v1`; Ollama remains an
independent dependency at its existing configured address.

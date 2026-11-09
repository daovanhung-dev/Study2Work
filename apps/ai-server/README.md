## Run with local Ollama (PowerShell)

Open PowerShell in the repository, enter `apps/ai-server`, and confirm that
Ollama has the model:

```powershell
Set-Location C:\study2work\Study2Work\apps\ai-server
ollama list
```

If Ollama is not already running, start it in a separate terminal with
`ollama serve`. The model name used here is `qwen2.5-coder:1.5b`.

Copy the example configuration once, then start the API:

```powershell
Copy-Item .env.example .env
uv run --env-file .env ai-server
```

The AI API listens on `http://127.0.0.1:3000`. It calls Ollama at
`http://127.0.0.1:11434` using `OLLAMA_BASE_URL`, `OLLAMA_MODEL`, and
`OLLAMA_TIMEOUT` from `.env`. `uv run --env-file` loads that file; the
application does not load `.env` on its own. The database entries in the
example file are currently unused by the active chat path.

In another PowerShell terminal, test the existing chat endpoint:

```powershell
$body = @{ prompt = 'Reply with the word OK' } | ConvertTo-Json
Invoke-RestMethod -Uri 'http://127.0.0.1:3000/api/v1/chat_log_ai' -Method Post -ContentType 'application/json' -Body $body
```

Expected response shape: `{"response":"..."}`. `GET http://127.0.0.1:3000/`
checks only that FastAPI is running; the chat request also tests the connection
to Ollama and the model. Stop the API with `Ctrl+C`.

The app shares one HTTPX `AsyncClient` per process, with at most 100 outbound
connections and a 5-second pool wait. A prompt must be a nonblank string of at
most 8,000 characters. Invalid prompts receive FastAPI HTTP 422. Ollama
connection, timeout, invalid response, and pool wait errors receive 503, 504,
502, and 503 respectively, with `{"error":{"code":"...","message":"..."}}`.
This pool limit does not determine how many generations Ollama can run at once.

Run focused tests from `apps/ai-server` with
`& .venv/Scripts/python.exe -m unittest discover -s tests -v` in PowerShell.
The tests mock Ollama; measure latency and throughput on the deployment host.

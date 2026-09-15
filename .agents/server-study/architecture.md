# Study Server architecture

## Intended composition visible in current source

```text
app/main.py:create_app
  -> app/api/v1.py:router
  -> app/core/config.py
  -> app/core/database.py
  -> app/core/middleware.py
  -> app/core/exceptions.py
  -> app/core/responses.py
  -> app/core/trace.py
```

Current composition and API #1 register flow are runnable and covered by HTTP
tests. Routes without a current implementation remain unwired.

## Verified ownership

- `app/main.py`: FastAPI composition root, CORS, middleware, exception handlers, root/health routes.
- `app/api/v1.py`: declared `/api/v1` routes; currently exposes health-adjacent
  utility routes and API #1 register.
- `app/core/config.py`: typed settings backed by `app/core/constants.py`.
- `app/core/database.py`: sync SQLAlchemy engine/session/query primitives.
- `app/core/security/*`: password, access token, refresh token primitives.
- `app/modules/auth/*`: API #1 register request model, query and use-case flow.
- `app/service/ai/ollama_service.py`: Ollama adapter copied/shared with Study codebase; no live Study caller after business modules disappeared.

## Unwired ownership

No current source establishes:

- chat log business flow;
- login/refresh/current-user orchestration;
- Study domain modules beyond API #1 register.

## Runtime compatibility repairs

1. `app.api.v1` imports the existing `app.modules.auth` package.
2. `responses.py` exposes canonical `success_response`/`error_response` and the legacy `error_payload` adapter.
3. `TraceIdMiddleware` uses the current trace helper names.

Together these repairs restore the current composition; future fix tasks must
re-evaluate the complete import chain rather than stop at the first error.

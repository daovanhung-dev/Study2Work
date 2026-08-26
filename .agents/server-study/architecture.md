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

Current composition cannot complete imports, nên sơ đồ trên là **declaration map**, không phải runnable runtime proof.

## Verified ownership

- `app/main.py`: FastAPI composition root, CORS, middleware, exception handlers, root/health routes.
- `app/api/v1.py`: declared `/api/v1` routes; imports missing business modules.
- `app/core/config.py`: typed env/settings.
- `app/core/database.py`: sync SQLAlchemy engine/session/query primitives.
- `app/core/security/*`: password, access token, refresh token primitives.
- `app/service/ai/ollama_service.py`: Ollama adapter copied/shared with Study codebase; no live Study caller after business modules disappeared.

## Missing ownership

`app/module/` is absent. Therefore no current source establishes:

- auth request models/use cases/query layer;
- user table mapping;
- chat log business flow;
- transaction owner for register/login/refresh;
- Study domain modules.

## Startup blockers

1. `app.api.v1` imports missing `app.module.*`.
2. `main.py` expects `success_response` absent from current responses module.
3. exception handlers expect `error_response` absent from current responses module.
4. trace middleware expects differently named helpers than current trace module.

Any one of these is enough to prevent the intended app from working correctly; fix tasks must re-evaluate all four rather than stop at the first import error.

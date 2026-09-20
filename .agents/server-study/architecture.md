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

Current composition, API #1 register flow and API #3 login/refresh flow are
present. The auth test modules use the `guest` namespace and the full test
collection is available; routes without a current implementation remain
unwired.

## Verified ownership

- `app/main.py`: FastAPI composition root, CORS, middleware, exception handlers, root/health routes.
- `app/api/v1.py`: declared `/api/v1` routes; currently exposes health-adjacent
  utility routes and API #1 register.
- `app/core/config.py`: typed settings backed by `app/core/constants.py`.
- `app/core/database.py`: sync SQLAlchemy engine/session/query primitives.
- `app/core/security/*`: password, access token, refresh token primitives.
- `app/utils/auth.py`: access/refresh token issuance, expiry metadata and public auth payload mapping.
- `app/utils/validate.py`: shared pure normalization helpers used by request models.
- `app/modules/guest/auth_login/models.py`: login and refresh request contracts.
- `app/modules/guest/auth_login/validate.py`: pure auth request validation.
- `app/modules/guest/auth_login/query.py`: SQL constants for user lookup and refresh-token persistence.
- `app/modules/guest/auth_login/view.py`: login credential flow, refresh rotation, transaction and response mapping.
- `app/modules/guest/register_account/models.py`: API #1 register request model,
  type/basic validation and normalization.
- `app/modules/guest/register_account/validate.py`: special validation boundary;
  currently empty and unwired.
- `app/modules/guest/register_account/query.py`: duplicate lookup and users
  insert SQL/query helpers.
- `app/modules/guest/register_account/view.py`: register orchestration,
  business check, password hashing, transaction and response mapping.
- `app/service/ai/ollama_service.py`: Ollama adapter copied/shared with Study codebase; no live Study caller after business modules disappeared.

## Unwired ownership

No current source establishes:

- chat log business flow;
- current-user orchestration;
- Study domain modules beyond API #1 register and API #3 auth.

## Runtime compatibility repairs

1. `app.api.v1` imports the existing `app.modules.guest` package.
2. `responses.py` exposes canonical `success_response`/`error_response` and the legacy `error_payload` adapter.
3. `TraceIdMiddleware` uses the current trace helper names.

Together these repairs restore the current composition; future fix tasks must
re-evaluate the complete import chain rather than stop at the first error.

## Validation workflow boundary

```text
app/utils/validate.py: shared normalization helper
→ model.py
→ type/required/basic length/format/normalization
→ module validate.py
→ named, pure special validation
→ view.py
→ DB-backed business validation/query/transaction
```

Examples such as no whitespace or an allowed email domain are only applicable
when the API contract confirms them. The current register source still keeps
its password/full-name validators in `models.py`; email whitespace normalization
is reused from `app/utils/validate.py`. Auth login/refresh uses the same shared
helpers while keeping token persistence and transaction ownership in the module
view.

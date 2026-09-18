# Study core runtime contracts

Status: source-backed; `app.main` imports and composes the current routes. The
register pytest module still blocks full test collection through a stale import.

The local Study API startup address is `127.0.0.1:3003`. Containerized startup
binds internally to `0.0.0.0:3003` and publishes the host address separately.

## `app/main.py`

### `_settings_for_request(request)`
- Purpose: prefer `request.app.state.settings`, fallback to cached `get_settings()`.
- Return: `Settings`.
- Side effect: none.
- Caller: health handlers.

### `create_app(app_settings=None)`
- Purpose: compose FastAPI instance; optionally inject test/runtime settings and DB factory.
- Calls: `build_engine`, `build_session_factory`, CORS middleware, `TraceIdMiddleware`, exception handlers, router.
- Side effects: creates engine/session factory when explicit settings supplied; installs dependency override for `get_db`.
- Declared routes: `/`, `/health/live`, `/health/ready` plus `/api/v1/*` router.
- Runtime status: source-backed/import-verified for current routes, including API
  #1 register.

### root/health handlers
- Intended return: standard success envelope via `success_response`.
- `health_live`: reports service + environment only.
- `health_ready`: reports database as `configured`; it does **not** execute a DB probe. Redis is only `configured/not_configured` from settings.
- Runtime status: source-backed; full Study test suite is not currently
  collectable because of the stale register test import.

## `app/core/responses.py`

### `ErrorDetail`
Pydantic model `{field?, code, message}`, `extra=forbid`.

### `ApiError.__init__`
Controlled exception carrying HTTP status, business code, safe message, trace ID, tuple of field errors and optional headers.

### `ApiResponse.success_payload()`
Returns canonical success keys:
`success`, `businessCode`, `message`, `data`, `meta`, `traceId`.

### `ApiResponse.raise_error()`
Raises `ApiError` with the model's status/business code/message/trace ID.

`success_response` and `error_response` are the canonical functional adapters;
`error_payload` remains only for legacy callers/tests.

## `app/core/exceptions.py`

- `_validation_field(loc)`: removes protocol location prefixes (`body/query/path/header/cookie`) and joins remaining field path.
- `api_error_handler`: renders `ApiError` through `error_response`.
- `http_exception_handler`: preserves already-safe error dicts; otherwise maps to `HTTP_ERROR`.
- `request_validation_exception_handler`: maps Pydantic errors to `ErrorDetail`, using
  `DESIGN_VALIDATION_ERROR` for API #1 register and `VALIDATION_ERROR` elsewhere.
- `unhandled_exception_handler`: logs internal exception with trace ID; returns
  `DESIGN_INTERNAL_ERROR` for API #1 register and `INTERNAL_SERVER_ERROR` elsewhere.

## `app/core/trace.py`

- `TRACE_HEADER = "X-Trace-Id"`.
- `create_trace_id()`: UUID4 string.
- `validate_trace_id(value)`: valid UUID normalized to string else `None`.
- `get_trace_id(request)`: read validated `request.state.trace_id`, otherwise generate/store one.
- `set_trace_id(value)` / `reset_trace_id(token)`: manage ContextVar.
- `get_current_trace_id()`: read ContextVar without Request.

## `app/core/middleware.py:TraceIdMiddleware.dispatch`
Flow: validate incoming header -> create if invalid -> attach request/context -> call next -> set response header -> safe 500 on exception -> reset context.

Middleware uses `validate_trace_id`, `set_trace_id` and `reset_trace_id` from the
current trace module.

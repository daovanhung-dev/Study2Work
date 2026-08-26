# Study core runtime contracts

Status: source-backed, but composition is `DECLARED_NOT_RUNNABLE`.

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
- Blockers: imports `success_response`; imported router itself imports missing `app.module.*`.

### root/health handlers
- Intended return: standard success envelope via `success_response`.
- `health_live`: reports service + environment only.
- `health_ready`: reports database as `configured`; it does **not** execute a DB probe. Redis is only `configured/not_configured` from settings.
- Runtime status: blocked before trustworthy request execution because required response helper is absent.

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

Important discrepancy: this file does **not** expose `success_response` or `error_response` required by current `main.py`/`exceptions.py`.

## `app/core/exceptions.py`

- `_validation_field(loc)`: removes protocol location prefixes (`body/query/path/header/cookie`) and joins remaining field path.
- `api_error_handler`: intended to render `ApiError` through missing `error_response`.
- `http_exception_handler`: preserves already-safe error dicts; otherwise maps to `HTTP_ERROR`.
- `request_validation_exception_handler`: maps Pydantic errors to `ErrorDetail`, intended business code `VALIDATION_ERROR`, HTTP 422.
- `unhandled_exception_handler`: logs internal exception with trace ID; intended safe 500 `INTERNAL_SERVER_ERROR`.

Because `error_response` import is invalid, these handlers are not runnable as a module at snapshot.

## `app/core/trace.py`

- `TRACE_HEADER = "X-Trace-Id"`.
- `create_trace_id()`: UUID4 string.
- `validate_trace_id(value)`: valid UUID normalized to string else `None`.
- `get_trace_id(request)`: read validated `request.state.trace_id`, otherwise generate/store one.
- `set_trace_id(value)` / `reset_trace_id(token)`: manage ContextVar.
- `get_current_trace_id()`: read ContextVar without Request.

## `app/core/middleware.py:TraceIdMiddleware.dispatch`
Intended flow: normalize incoming header -> create if invalid -> attach request/context -> call next -> set response header -> safe 500 on exception -> reset context.

Current imports request **nonexistent names** `normalize_trace_id`, `set_current_trace_id`, `reset_current_trace_id`. Closest current functions are `validate_trace_id`, `set_trace_id`, `reset_trace_id`; do not silently alias them without an approved fix.

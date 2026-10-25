# Study Server module index

## Module layout

```text
app/modules/<feature>/
├── models.py   # declarative request/response model classes and data conversion
├── validate.py # input validation and normalization for this API
├── query.py    # optional: SQL statement constants when this API queries a DB
└── view.py     # main API flow, side effects and response orchestration
```

`models.py` contains model class declarations only: fields, types, defaults,
model configuration and data/type conversion. Do not put standalone constants,
helpers, input validation, normalization or business rules there. Runtime input
rules belong in the API's `validate.py`.

An API validator returns normalized model/data when valid and uses only
`return error_response(...)` to return invalid-input errors. It must not raise
an API response, construct an alternate error response, query DB or perform
side effects. Do not use built-in `ValueError` in Study Server source or tests.
A shared pure helper returns `ErrorDetail`, a sentinel or
another typed result that carries validation failure; the API validator/view
maps it through `error_response(...)` at the HTTP boundary. `error_response(errors=...)`
accepts `ErrorDetail` instances and serializes the canonical `meta.fieldErrors`
shape. Errors outside HTTP keep their internal error handling and do not become
`JSONResponse`. Keep schema-only request metadata in route declarations. Do not
apply a rule such as `@gmail.com` unless the current API contract confirms it.

Module-local `validate.py` files contain API-specific request rules where
needed; API #4 uses the shared current-user guard directly and has no
module-local validator. Shared email, blank-value, sort and search helpers live
in `app/utils/validate.py`; Bearer/JWT and token helpers live in
`app/utils/auth.py`. APIs #4, #13, #14 and #46 reuse
`validate_current_user_request(...)` with an explicit role (`STUDENT` or
`MENTOR`) rather than implementing Bearer/JWT checks in module code.

`query.py` is present only when the module needs SQL. It contains SQL statement
string constants only: no functions, classes, helpers, application/DB imports,
parameter preparation or database calls. Put parameter binding and
`query_one`/`query_many` calls in `view.py`. Modules without DB access should not
add an empty `query.py`; API #2 currently dispatches through an email provider
and has no query file.

`view.py` is the primary API flow: it calls validators and query/provider
helpers, performs DB-backed business checks, owns side effects and transaction
boundaries, maps failures, and builds the response. Add a concise Vietnamese
comment for every meaningful operation in each handler and helper, including
validation, external/DB calls, branches, rollback/commit, data mapping and
response construction. One comment may cover consecutive statements in one
cohesive operation; simple variable assignments do not need separate comments.
API-facing functions keep a short API header comment immediately before the
function; internal helpers do not. Comments explain the purpose of the step and
describe current source behavior when a DD differs.

The router remains thin and delegates the API flow to `view.py`.

## Current modules

| Module | Status | Context |
|---|---|---|
| `guest/api_01_auth_register` | `SOURCE_BACKED` | `register-account.md` |
| `guest/api_03_auth_login` | `SOURCE_BACKED` | Login and refresh-token flow in current source |
| `guest/api_04_users_me` | `SOURCE_BACKED` | API #4 current Student profile read flow |
| `guest/api_12_resources_detail` | `SOURCE_BACKED` | API #12 public resource metadata read with published-parent check; response returns stored URL |
| `guest/api_13_users_me_avatar` | `SOURCE_BACKED` | Student JSON Data URL upload through injectable S3-compatible storage; no DB access |
| `guest/api_14_users_me_profile` | `SOURCE_BACKED` | Student profile update; reuses `validate_current_user_request(..., role="STUDENT")` from `app/utils/auth.py` |
| `guest/api_05_categories` | `SOURCE_BACKED` | API #5 public active-category read flow |
| `guest/api_02_auth_verify_email_send` | `SOURCE_BACKED` | API #2 public verification dispatch through injectable stub provider |
| `guest/api_06_courses` | `SOURCE_BACKED` | API #6 public course list with pagination |
| `guest/api_07_courses_search` | `SOURCE_BACKED` | API #7 public course search with pagination |
| `guest/api_08_courses_detail` | `SOURCE_BACKED` | API #08 public published-course detail; composition and HTTP tests pass in the current full suite |
| `guest/api_09_courses_curriculum` | `SOURCE_BACKED` | API #09 public published-course curriculum; composition and HTTP tests pass in the current full suite |
| `mentor/api_46_mentor_courses` | `SOURCE_BACKED` | API #46 Mentor-owned course list with optional status and pagination; numeric `sub`/`MENTOR` authorization |

Shared course catalog boundary:
`guest/_shared/course_catalog` contains only response models and pure helpers
used by APIs #6–#8.
| Other Study domain modules | `NOT_FOUND`/`UNWIRED` | Require source/contract before implementation |

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
side effects. A shared pure helper may raise a validation exception internally;
the API validator catches it and maps it through `error_response(...)`. Keep
schema-only request metadata in route declarations. Do not apply a rule such as
`@gmail.com` unless the current API contract confirms it.

Module-local `validate.py` files contain API-specific request rules where
needed; API #4 uses the shared current-user guard directly and has no
module-local validator. Shared email, blank-value, sort and search helpers live
in `app/utils/validate.py`; Bearer/JWT and token helpers live in
`app/utils/auth.py`. API #14 profile validation reuses that shared auth guard.

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
| `guest/api_14_users_me_profile` | `SOURCE_BACKED` | Student profile update; reuses the shared Student guard through `app/utils/auth.py` |
| `guest/api_05_categories` | `SOURCE_BACKED` | API #5 public active-category read flow |
| `guest/api_02_auth_verify_email_send` | `SOURCE_BACKED` | API #2 public verification dispatch through injectable stub provider |
| `guest/api_06_courses` | `SOURCE_BACKED` | API #6 public course list with pagination |
| `guest/api_07_courses_search` | `SOURCE_BACKED` | API #7 public course search with pagination |

Shared course catalog boundary:
`guest/_shared/course_catalog` contains only response models and pure helpers
used by API #6 and API #7.
| Other Study domain modules | `NOT_FOUND`/`UNWIRED` | Require source/contract before implementation |

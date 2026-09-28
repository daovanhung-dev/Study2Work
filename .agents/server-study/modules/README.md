# Study Server module index

## Module layout

```text
app/modules/<feature>/
├── models.py   # request/response contract and basic model validation
├── validate.py # input validation and normalization for this API
├── query.py    # SQL string constants only
└── view.py     # query execution, business orchestration and transaction boundary
```

`query.py` must not define Python functions/classes, import application helpers
or execute DB operations. Put `query_one`/`query_many` calls and any SQL
parameter preparation in `view.py`; keep the parameterized SQL text in
`query.py`.

`models.py` declares input/output fields, types, defaults and Pydantic type
conversion. Put runtime validation and normalization in the API's `validate.py`
and shared pure helpers in `app/utils/validate.py`. An API validator returns
`ApiError(...)` directly for invalid input and normalized model data otherwise.
It runs before business checks and DB access; it must not query DB or perform
side effects. Keep schema-only request metadata in route declarations. Do not
apply an example such as `@gmail.com` unless the current API contract confirms it.

APIs #1–#7 each have a module-local `validate.py`; shared email, bearer/JWT,
sort and search normalization helpers live in `app/utils/validate.py`.

API-facing functions use a short API header comment immediately before the
function; internal helpers do not. Keep event comments concise and attach a DD
step only when it clarifies the flow.

DB-backed checks such as duplicate, existence, permission or state belong to
`view.py`, which executes SQL constants from `query.py`. The router remains
thin.

## Current modules

| Module | Status | Context |
|---|---|---|
| `guest/api_01_auth_register` | `SOURCE_BACKED` | `register-account.md` |
| `guest/api_03_auth_login` | `SOURCE_BACKED` | Login and refresh-token flow in current source |
| `guest/api_04_users_me` | `SOURCE_BACKED` | API #4 current Student profile read flow |
| `guest/api_05_categories` | `SOURCE_BACKED` | API #5 public active-category read flow |
| `guest/api_02_auth_verify_email_send` | `SOURCE_BACKED` | API #2 public verification dispatch through injectable stub provider |
| `guest/api_06_courses` | `SOURCE_BACKED` | API #6 public course list with pagination |
| `guest/api_07_courses_search` | `SOURCE_BACKED` | API #7 public course search with pagination |

Shared course catalog boundary:
`guest/_shared/course_catalog` contains only response models and pure helpers
used by API #6 and API #7.
| Other Study domain modules | `NOT_FOUND`/`UNWIRED` | Require source/contract before implementation |

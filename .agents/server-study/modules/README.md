# Study Server module index

## Module layout

```text
app/modules/<feature>/
├── models.py   # request/response contract and basic model validation
├── validate.py # named pure special validation when module-specific rules are needed
├── query.py    # SQL statements/constants; view owns query execution
└── view.py     # business orchestration and transaction boundary
```

`model.py` handles type, required, basic length, format and normalization that
belongs to the request contract. `validate.py` is for special, pure and
reusable rules with an explicit field, condition and error message, such as no
whitespace, a required prefix/suffix or an allowed email domain. It must not
query DB, commit/rollback or return HTTP responses. Do not apply an example
such as `@gmail.com` unless the current API contract confirms it.

API #3 login/refresh request models bind the shared auth validators directly
from `app/utils/validate.py`; its module does not need a local `validate.py`.
API #4 binds `extract_bearer_token` and `validate_access_claims` directly from
`app/utils/validate.py`; its module does not need a local `validate.py`.

API-facing functions use a short API header comment immediately before the
function; internal helpers do not. Keep event comments concise and attach a DD
step only when it clarifies the flow.

DB-backed checks such as duplicate, existence, permission or state belong to
`view.py`, using `query.py` where SQL is needed. The router remains thin.

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

# Study Server module index

## Module layout

```text
app/modules/<feature>/
├── models.py   # request/response contract and basic model validation
├── validate.py # named pure special validation
├── query.py    # SQL statements/constants; view owns query execution
└── view.py     # business orchestration and transaction boundary
```

`model.py` handles type, required, basic length, format and normalization that
belongs to the request contract. `validate.py` is for special, pure and
reusable rules with an explicit field, condition and error message, such as no
whitespace, a required prefix/suffix or an allowed email domain. It must not
query DB, commit/rollback or return HTTP responses. Do not apply an example
such as `@gmail.com` unless the current API contract confirms it.

DB-backed checks such as duplicate, existence, permission or state belong to
`view.py`, using `query.py` where SQL is needed. The router remains thin.

## Current modules

| Module | Status | Context |
|---|---|---|
| `guest/register_account` | `SOURCE_BACKED` | `register-account.md` |
| `guest/auth_login` | `SOURCE_BACKED` | Login and refresh-token flow in current source |
| `guest/users_me` | `SOURCE_BACKED` | API #4 current Student profile read flow |
| `guest/categories` | `SOURCE_BACKED` | API #5 public active-category read flow |
| `guest/verify_email_send` | `SOURCE_BACKED` | API #2 public verification dispatch through injectable stub provider |
| `guest/courses` | `SOURCE_BACKED` | API #6 public published-course list with pagination |
| Other Study domain modules | `NOT_FOUND`/`UNWIRED` | Require source/contract before implementation |

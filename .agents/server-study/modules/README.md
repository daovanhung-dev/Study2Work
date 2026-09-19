# Study Server module index

## Module layout

```text
app/modules/<feature>/
├── models.py   # request/response contract and basic model validation
├── validate.py # named pure special validation
├── query.py    # parameterized SQL/query helpers
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
| `auth/register_account` | `SOURCE_BACKED` | `register-account.md` |
| Other Study domain modules | `NOT_FOUND`/`UNWIRED` | Require source/contract before implementation |

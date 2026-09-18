# Contract registry context

Use this page only when a task crosses app boundaries or changes an API,
event, shared envelope, or local deployable contract.

| Contract | Source | Producer | Consumer | Status |
|---|---|---|---|---|
| API guidelines | `contracts/api-guidelines/README.md` | repository API conventions | Study, Work, Web | `VERIFIED` |
| Study → Work events | `contracts/events/study-work/` | Study | Work | `DECLARED_NOT_RUNNABLE` — schemas and examples exist, consumer is absent |
| Work OpenAPI | `contracts/openapi/work/legacy-web.openapi.json` and `openapi.json` | Work contract files | Work server/Web | `DISCREPANCY` — legacy file aligns to current routes; target file is not wired |
| Study OpenAPI | `contracts/openapi/study/README.md` | Study | Study Web | `NOT_FOUND` — placeholder only |
| Skill taxonomy | `contracts/skill-taxonomy/` | repository taxonomy | future modules | `VERIFIED`, no current server caller |
| DB Admin local contract | `apps/db-admin-server/app/core/contracts.py` and `app/api/routes.py` | DB Admin server | DB Admin Web | `VERIFIED` |

Cross-scope event behavior must not be inferred from the JSON Schemas alone:
signature validation, idempotency, persistence and consumer wiring remain
`DECLARED_NOT_RUNNABLE` until source evidence exists.

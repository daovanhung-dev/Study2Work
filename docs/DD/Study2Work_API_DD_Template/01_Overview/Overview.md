# Overview - {{API_CODE}}

| Field | Value |
|---|---|
| API code | `{{API_CODE}}` |
| API name | `{{API_NAME}}` |
| Module | `{{MODULE_CODE}}` |
| Method | `{{HTTP_METHOD}}` |
| Endpoint | `/api/v1/{{ENDPOINT}}` |
| Primary actor | `{{ACTOR}}` |
| Caller app | `{{CALLER_APP}}` |
| Auth scheme | `{{AUTH_SCHEME}}` |
| Permission | `{{PERMISSION}}` |
| Status | `DRAFT` |
| Version | `v0.1` |
| Updated | `{{YYYY-MM-DD}}` |

## Business Goal

`{{ONE_PARAGRAPH_BUSINESS_GOAL}}`

## Study Scope

In scope:

- `{{IN_SCOPE_ITEM}}`

Out of scope:

- Employer, recruitment, job, CV, interview, matching, shortlist, offer, and hiring workflows.
- `{{API_SPECIFIC_OUT_OF_SCOPE_ITEM}}`

## Source Trace

| Source | Link / ID | Note |
|---|---|---|
| BD | `docs/BD/Study2Work_Study_BD_Codex_Ready.md#{{SECTION}}` | `{{NOTE}}` |
| API checklist | `docs/checklists/API.md` | `{{API_CODE}}` |
| Activity diagram | `docs/diagrams/02_activity/{{FILE}}` | `{{NOTE}}` |
| Sequence diagram | `docs/diagrams/04_sequence/{{FILE}}` | `{{NOTE}}` |
| Class diagram | `docs/diagrams/03_class/{{FILE}}` | `{{NOTE}}` |
| ADR | `docs/adr/{{ADR_FILE}}` | `{{NOTE}}` |

## Preconditions

- `{{PRECONDITION}}`

## Postconditions

- `{{POSTCONDITION_SUCCESS}}`
- Failed requests must not create partial business state unless explicitly documented.

## Authorization And Scope

| Actor | Permission | Ownership/scope rule |
|---|---|---|
| `{{ACTOR}}` | `{{PERMISSION}}` | `{{OWNERSHIP_SCOPE_RULE}}` |

## Data Ownership

| Table / aggregate | Read | Write | Owner module | Note |
|---|---:|---:|---|---|
| `{{TABLE}}` | Y/N | Y/N | `{{MODULE}}` | `{{NOTE}}` |

## Events And Async Work

| Event/job | When emitted | Delivery | Consumer | Retry rule |
|---|---|---|---|---|
| `{{EVENT_OR_JOB}}` | `{{WHEN}}` | `sync/after_commit/outbox/celery` | `{{CONSUMER}}` | `{{RETRY_RULE}}` |

## Open Questions

| ID | Owner | Status | Question |
|---|---|---|---|
| `{{API_CODE}}-OQ-001` | `{{OWNER}}` | `OPEN` | `{{QUESTION}}` |

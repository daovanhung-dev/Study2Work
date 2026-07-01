# Data Mapping - {{API_CODE}}

## Runtime Flow

| Step | Layer | Action | Input | Output | Rule/error | Write? |
|---:|---|---|---|---|---|---:|
| 1 | Presentation | Parse request. | HTTP request | Request DTO | `E422` | N |
| 2 | Presentation | Authenticate if required. | Token/session | Actor context | `E401` | N |
| 3 | Application | Authorize role and ownership/scope. | Actor + resource ID | Authorized command/query | `E403` | N |
| 4 | Application | Load required entities/read models. | Repository port | Domain objects | `E404` | N |
| 5 | Domain/Application | Validate business rules and state transition. | Domain objects + command | Decision | `E422/E409` | N |
| 6 | Infrastructure | Persist writes in short transaction. | Domain decision | Stored rows | `E409/E500` | Y/N |
| 7 | Infrastructure | Write audit/outbox/event after source decision. | Stored rows | Audit/event rows | `E500` | Y/N |
| 8 | Presentation | Map response envelope. | Result | JSON envelope | _none_ | N |

## Table Access

| Table | Operation | Columns | Repository method | Transaction scope | Note |
|---|---|---|---|---|---|
| `{{table_name}}` | `read/write` | `{{columns}}` | `{{method}}` | `inside/outside` | `{{note}}` |

## Application Pseudocode

```text
handler(command, actor_context):
    authorize(actor_context, command.resource_id)
    entity = repository.get(...)
    entity.apply_business_rule(...)
    with transaction:
        repository.save(entity)
        audit_repository.append(...)
        outbox_repository.append(...)
    return result
```

## Transaction And Idempotency

| Item | Decision |
|---|---|
| Transaction boundary | `{{BOUNDARY}}` |
| Idempotency key | `Required / Optional / Not applicable` |
| Concurrency control | `Optimistic lock / unique constraint / not applicable` |
| Retry rule | `{{RETRY_RULE}}` |

## Audit, Event, Job

| Type | Name | When | Payload fields | Delivery | Consumer | Retry/DLQ |
|---|---|---|---|---|---|---|
| Audit | `{{ACTION}}` | `{{WHEN}}` | `traceId`, `actorId`, `resourceId` | transaction | audit viewer | N/A |
| Event/job | `{{EVENT_OR_JOB}}` | after commit | `{{FIELDS}}` | outbox/Celery | `{{CONSUMER}}` | `{{RULE}}` |

## Tests Derived From Mapping

| Test ID | Scenario | Expected result |
|---|---|---|
| `{{API_CODE}}-TC-001` | Happy path | Success envelope and expected data. |
| `{{API_CODE}}-TC-002` | Validation failure | `422` with safe field error. |
| `{{API_CODE}}-TC-003` | Ownership/scope denied | `403` with no mutation. |
| `{{API_CODE}}-TC-004` | Invalid state transition | Stable business error and no partial write. |

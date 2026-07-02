# Data Mapping - LEARN-PLACEMENT-001

## Runtime Flow

| Step | Layer | Action | Input | Output | Rule/error | Write? |
|---:|---|---|---|---|---|---:|
| 1 | Presentation | Parse request và tạo/nhận `traceId`. | HTTP request | Request DTO | E422 | N |
| 2 | Presentation | Authenticate nếu endpoint không public. | Authorization/service token | Actor context | E401 | N |
| 3 | Application | Authorize role và ownership/scope. | Actor + resource IDs | Authorized command/query | E403 | N |
| 4 | Application | Load entity/read model cần thiết. | Repository ports | quiz_attempt, quiz_answer, skill_assessment | E404 | N |
| 5 | Domain/Application | Áp dụng business rule và state transition. | Domain objects + command | Decision | E422/E409 | N |
| 6 | Infrastructure | Persist write trong transaction ngắn nếu có mutation. | Domain decision | Stored rows | E409/E500 | Y |
| 7 | Infrastructure | Ghi audit/outbox/event/job nếu source yêu cầu. | Stored rows | Audit/event rows | E500 | Y |
| 8 | Presentation | Map standard response envelope. | Result | JSON envelope | none | N |

## Table Access

| Table | Operation | Columns | Repository method | Transaction scope | Note |
|---|---|---|---|---|---|
| `quiz_attempt` | read/write | id, status, owner/scope, timestamps, business fields cần thiết | quiz_attempt_repository | inside transaction for writes | Cột chi tiết cần review khi APPROVED. |
| `quiz_answer` | read/write | id, status, owner/scope, timestamps, business fields cần thiết | quiz_answer_repository | inside transaction for writes | Cột chi tiết cần review khi APPROVED. |
| `skill_assessment` | read/write | id, status, owner/scope, timestamps, business fields cần thiết | skill_assessment_repository | inside transaction for writes | Cột chi tiết cần review khi APPROVED. |

## Application Pseudocode

```text
handler(command_or_query, actor_context):
    trace_id = command_or_query.trace_id
    authorize(actor_context, command_or_query.resource_scope)
    current_state = repository.load_required_models(...)
    decision = domain_service.apply_rules(current_state, command_or_query)
    if decision.has_writes:
        with transaction:
            repository.persist(decision.changes)
            audit_repository.append(trace_id, actor_context, "LEARN-PLACEMENT-001")
            outbox_repository.append_after_commit(decision.events)
    return response_mapper.to_envelope(decision.result, trace_id)
```

## Transaction And Idempotency

| Item | Decision |
|---|---|
| Transaction boundary | Một transaction ngắn bao gồm write chính, audit và outbox/job record nếu có. |
| Idempotency key | Required |
| Concurrency control | Optimistic lock hoặc unique constraint theo aggregate; chi tiết cần review khi implement. |
| Retry rule | Client có thể retry an toàn. |

## Audit, Event, Job

| Type | Name | When | Payload fields | Delivery | Consumer | Retry/DLQ |
|---|---|---|---|---|---|---|
| Audit | `LEARN-PLACEMENT-001` | Khi API thành công hoặc bị từ chối bởi rule quan trọng. | traceId, actorId, apiCode, resourceId | transaction/log sink | audit viewer | N/A |
| Event/job | `LearningPathAssigned` | Sau commit thành công. | traceId, actorId, resourceId, occurredAt | outbox/Celery | consumer liên quan | Retry/DLQ theo worker policy |

## Tests Derived From Mapping

| Test ID | Scenario | Expected result |
|---|---|---|
| `LEARN-PLACEMENT-001-TC-001` | Happy path đúng actor và scope hợp lệ. | Success envelope với `LEARN-PLACEMENT-001-SUCCESS`. |
| `LEARN-PLACEMENT-001-TC-002` | Validation failure. | `422` với safe field error và không ghi partial state. |
| `LEARN-PLACEMENT-001-TC-003` | Missing/invalid auth khi endpoint cần auth. | `401` với `AUTH-RESP-UNAUTHORIZED`. |
| `LEARN-PLACEMENT-001-TC-004` | Permission hoặc ownership/scope bị từ chối. | `403` và không mutation. |
| `LEARN-PLACEMENT-001-TC-005` | Resource không tồn tại hoặc không visible. | `404` với safe message. |
| `LEARN-PLACEMENT-001-TC-006` | State conflict, duplicate hoặc concurrency conflict. | `409` và state cũ được giữ nguyên. |
| `LEARN-PLACEMENT-001-TC-007` | Dependency/system failure. | Safe error envelope có `traceId`; log không lộ secret/PII. |

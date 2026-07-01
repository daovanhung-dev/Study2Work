# 05. Data Mapping – {{API_NAME}}

> **Mục đích:** đây là phần thực thi chi tiết nhất của DD. Nó mô tả API chạy như thế nào ở runtime: API nhận dữ liệu từ đâu, khởi tạo biến gì, validate/authorize ra sao, truy vấn/ghi bảng nào, repository/service nào được gọi, transaction/cache/event/external call vận hành thế nào, và từng field response xuất phát từ đâu.
>
> **Yêu cầu chất lượng:** Backend phải có thể chuyển tài liệu này thành controller → DTO → use case/service → repository → transaction → event → response mapper. QA phải có thể suy ra test boundary. AI coding không được tự đoán các bước còn thiếu.

---

## 1. Runtime metadata

| Thuộc tính | Giá trị |
|---|---|
| API business code | `{{API_CODE}}` |
| API name | `{{API_NAME}}` |
| Use case / command-query | `{{UC_ID}} / {{COMMAND_OR_QUERY_NAME}}` |
| Bounded context | `{{BOUNDED_CONTEXT}}` |
| Aggregate / domain owner | `{{AGGREGATE_ROOT_OR_DOMAIN_SERVICE}}` |
| Controller / handler | `{{CONTROLLER_METHOD}}` |
| Application service / use case | `{{APPLICATION_SERVICE_METHOD}}` |
| Transaction type | `Read-only / Required / Requires new / Async saga` |
| Data consistency | `Strong / Eventual / Read-your-writes required` |
| Concurrency model | `{{OPTIMISTIC_LOCK_UNIQUE_CONSTRAINT_ROW_LOCK_OR_NA}}` |
| Idempotency model | `{{IDEMPOTENCY_MODEL_OR_NA}}` |
| Correlation fields | `traceId`, `apiCode`, `moduleCode`, `actorUserId`, `{{EXTRA_FIELDS}}` |

## 2. Flow assumptions and invariants

### 2.1. Input assumptions

| ID | Assumption | Source | Validation / fallback | Impact if false |
|---|---|---|---|---|
| `ASM-01` | `{{ASSUMPTION}}` | `{{SOURCE}}` | `{{CHECK_OR_FALLBACK}}` | `{{ERROR_OR_DEGRADATION}}` |

### 2.2. Business invariants

| Rule ID | Invariant | Enforced by | When checked | Failure code | Notes |
|---|---|---|---|---|---|
| `BR-{{NNN}}` | `{{INVARIANT}}` | `{{AGGREGATE_OR_DOMAIN_SERVICE}}` | `{{FLOW_STEP}}` | `{{ERROR_CODE}}` | `{{NOTES}}` |

## 3. Input and runtime variable initialization

> Liệt kê **mọi biến có ý nghĩa nghiệp vụ/technical** được khởi tạo, không chỉ field request. Không ghi raw credential/token vào log. `Source` phải chỉ ra property/chủ thể thật, ví dụ `JWT.sub`, `request.path.assignmentId`, `user.status`, `system_setting.max_submission_size`.

| No. | Variable name | Type | Initial value / expression | Source | Normalization / conversion | Sensitive? | Lifetime / scope | Used at steps | Log policy | Notes |
|---:|---|---|---|---|---|---|---|---|---|---|
| 1 | `traceId` | `UUID` | `request.header.x-request-id ?? generatedUuid()` | Gateway/request context | Validate <= 64 char if client supplied. | N | Entire request | All | Log as plain correlation ID. | Must be returned to client. |
| 2 | `actorUserId` | `UUID` | `jwt.sub` | Authenticated JWT claim | No body override allowed. | Internal | Request | AuthZ/audit/query | Log allowed. | `null` only for public API. |
| 3 | `actorRoles` | `Role[]` | `jwt.roles` / permission resolver | JWT / cache / DB | Deduplicate / normalize enum. | Internal | Request | AuthZ | Log summarized. | Do not trust body roles. |
| 4 | `{{normalizedField}}` | `{{TYPE}}` | `normalize(request.body.{{fieldName}})` | Request body | `{{TRANSFORM}}` | `{{Y/N}}` | Command scope | `{{STEP_RANGE}}` | `{{MASK_OR_NEVER}}` | `{{NOTES}}` |
| 5 | `{{resourceId}}` | `UUID` | `request.params.{{resourceId}}` | URL path | Parse + UUID validate. | N | Command scope | `{{STEP_RANGE}}` | Plain | `{{NOTES}}` |
| 6 | `nowUtc` | `Instant` | `clock.nowUtc()` | Server clock | UTC only. | N | Transaction | `{{STEP_RANGE}}` | Plain | Use injected clock in tests. |
| 7 | `{{systemSetting}}` | `{{TYPE}}` | `settingsService.get('{{KEY}}')` | system_setting/cache | Validate safe default. | Internal | Request / cached | `{{STEP_RANGE}}` | Mask if secret. | `{{NOTES}}` |

## 4. End-to-end processing flow

> Luồng phải đúng thứ tự thực tế. Ghi rõ branch, condition, error code, side effect, input/output và checkpoint log. Không ghi “xử lý nghiệp vụ” chung chung.

| Step | Phase | Layer / component | Action | Inputs | Outputs / state changed | Rule / condition | Failure code | Transaction | Log / metric checkpoint |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | Receive | `{{Gateway/Controller}}` | Receive request, create/propagate `traceId`, enforce max payload/content type. | HTTP method/path/header/body | Parsed request context. | Content type/size/JSON valid. | `{{ERROR_CODE}}` | No | `{{MODULE}}-{{ACTION}}-REQ_RECEIVED` |
| 2 | Authenticate | `{{AuthGuard}}` | Validate authentication and populate `actorUserId`/claims. | Authorization header/cookie | Auth context. | JWT active/not expired/not revoked. | `{{ERROR_CODE}}` | No | `AUTH-CONTEXT_RESOLVED` |
| 3 | Authorize | `{{Policy/PermissionGuard}}` | Check role, permission and ownership relationship. | Actor context + route/body IDs | Authorization result. | `{{POLICY}}` | `{{ERROR_CODE}}` | No | `{{MODULE}}-AUTHZ_CHECKED` |
| 4 | Validate | `{{DTO/Validator}}` | Schema + field + cross-field validation. | Parsed request | Validated command candidate. | `{{RULE_IDS}}` | `{{ERROR_CODE}}` | No | `{{MODULE}}-VALIDATION_PASSED` |
| 5 | Normalize | `{{Mapper}}` | Canonicalize input, initialize command variables. | Validated request | `{{COMMAND_NAME}}`. | `{{NORMALIZATION_RULES}}` | `{{ERROR_CODE_OR_NA}}` | No | `{{MODULE}}-COMMAND_CREATED` |
| 6 | Load | `{{Repository/QueryService}}` | Load required source-of-truth records. | IDs/actor/status | Existing entities/read model. | Not deleted/visible/within scope. | `{{ERROR_CODE}}` | `{{TX_STATE}}` | `{{MODULE}}-RESOURCE_LOADED` |
| 7 | Business rule | `{{Domain service/Aggregate}}` | Evaluate state transition/eligibility/invariants. | Command + entity state | Proposed mutation/decision. | `{{BR_IDS}}` | `{{ERROR_CODE}}` | `{{TX_STATE}}` | `{{MODULE}}-RULE_PASSED` |
| 8 | Persist | `{{Repository}}` | Write source-of-truth and enforce optimistic/unique constraints. | Entity mutation | New persisted state/version. | `{{CONSTRAINT_OR_LOCK_RULE}}` | `{{ERROR_CODE}}` | `Begin/Commit/Rollback` | `{{MODULE}}-PERSISTED` |
| 9 | Audit/outbox | `{{Audit/Outbox repository}}` | Store audit row and transactional event. | Actor/action/resource/change set | Audit/event record. | Required for critical mutation. | `{{ERROR_CODE_OR_ALERT}}` | Same transaction | `{{MODULE}}-AUDIT_WRITTEN` |
| 10 | Commit | `{{Transaction manager}}` | Commit all required writes atomically. | Pending transaction | Committed data. | All writes success. | `{{ERROR_CODE}}` | Commit | `{{MODULE}}-TX_COMMITTED` |
| 11 | After commit | `{{Event handler/Cache}}` | Invalidate cache/publish event/send notification if non-blocking. | Event/keys | Async work scheduled. | Must not reverse committed result unless explicitly saga. | `{{ERROR_CODE_OR_WARNING}}` | After commit | `{{MODULE}}-POST_COMMIT_TRIGGERED` |
| 12 | Respond | `{{ResponseMapper}}` | Map state/read model to response envelope. | Persisted entity/query result | DTO response. | Field visibility/serialization policy. | `{{ERROR_CODE}}` | No | `{{MODULE}}-{{ACTION}}-SUCCESS` |

### 4.1. Flow pseudocode

```text
function {{applicationServiceMethod}}(requestContext, requestDto):
  traceId = resolveOrCreateTraceId(requestContext)
  actor = authenticate(requestContext.authorization)
  authorize(actor, {{policy}}, requestDto, requestContext.path)

  validated = validateSchemaAndCrossFields(requestDto)
  command = mapAndNormalize(validated, actor, nowUtc)

  begin transaction
    resources = loadRequiredResources(command)
    assertResourcesVisibleAndActive(resources, actor)
    decision = domainRuleEngine.execute(command, resources)
    persisted = repository.persist(decision)
    auditLogRepository.append(buildAuditLog(actor, persisted, traceId))
    outboxRepository.enqueue(buildDomainEvents(persisted, traceId))
  commit transaction

  invalidateCachesAndPublishAsyncWork(persisted)
  return mapSuccessResponse(persisted, traceId)
```

## 5. Authorization and ownership mapping

| Check ID | Actor source | Required role / permission | Target resource | Ownership / relationship condition | Enforcement point | Failure behavior |
|---|---|---|---|---|---|---|
| `AUTHZ-01` | `jwt.sub` | `{{PERMISSION}}` | `{{RESOURCE}}` | `{{EXACT_RELATIONSHIP_RULE}}` | Guard/policy + repository predicate | `403/404 {{ERROR_CODE}}` |
| `AUTHZ-02` | `jwt.organizationId` | `{{PERMISSION}}` | `{{RESOURCE}}` | `{{TENANT_OR_ORGANIZATION_SCOPE_RULE}}` | Query predicate | `403/404 {{ERROR_CODE}}` |

> Nếu ẩn sự tồn tại resource nhằm tránh enumeration, ghi rõ rule nào trả `404` thay cho `403` và bảo đảm test coverage.

## 6. Business rule decision table

| Rule ID | Inputs / source | Condition | Decision/action | State transition | Persistence impact | Error / outcome | Test IDs |
|---|---|---|---|---|---|---|---|
| `BR-{{NNN}}` | `{{VARIABLES_AND_TABLE_FIELDS}}` | `{{BOOLEAN_CONDITION}}` | `{{ACTION}}` | `{{FROM_STATE}} → {{TO_STATE}}` | `{{TABLE.COLUMNS}}` | `{{ERROR_CODE_OR_SUCCESS_CODE}}` | `{{TEST_IDS}}` |

## 7. Database access and repository mapping

> Liệt kê từng query/write riêng biệt, kể cả existence check, lock, audit/outbox, soft delete, read model query. Không gộp “query user table” thành một dòng mơ hồ.

| Step | Operation | Repository / method | Table / read model | Columns read / written | Predicate / join / filter | Index / lock / constraint | Input variables | Output | Purpose | Transaction scope | Error mapping |
|---:|---|---|---|---|---|---|---|---|---|---|---|
| 6.1 | `READ` | `{{repository}}.find{{Entity}}ByIdAndScope(...)` | `{{table}}` | `id,status,owner_id,version,deleted_at` | `id = :resourceId AND deleted_at IS NULL AND {{scope}}` | PK / partial index / `FOR UPDATE` if needed | `resourceId, actorUserId` | `{{entityOrNull}}` | Load target + enforce visibility. | `{{NONE_OR_TX}}` | `{{NOT_FOUND_OR_FORBIDDEN_CODE}}` |
| 6.2 | `READ` | `{{repository}}.exists{{Condition}}(...)` | `{{table}}` | `id` | `{{predicate}}` | Unique index `{{index}}` | `{{variables}}` | `boolean` | Pre-check business condition. | `{{NONE_OR_TX}}` | `{{CONFLICT_CODE}}` |
| 8.1 | `INSERT` | `{{repository}}.create(...)` | `{{table}}` | `{{written_columns}}` | N/A | PK / FK / CHECK / UNIQUE | `{{variables}}` | `{{createdEntity}}` | Create source of truth. | Main transaction | `{{CONFLICT_OR_DB_ERROR}}` |
| 8.2 | `UPDATE` | `{{repository}}.updateWithVersion(...)` | `{{table}}` | `{{written_columns}}, updated_at, version` | `id=:id AND version=:expectedVersion` | Optimistic version / row count = 1 | `{{variables}}` | `{{updatedEntityOrAffectedRows}}` | State transition. | Main transaction | `{{PRECONDITION_OR_CONFLICT_CODE}}` |
| 9.1 | `INSERT` | `auditLogRepository.append(...)` | `audit_log` | `actor_id,action,entity_type,entity_id,before_json,after_json,trace_id` | N/A | Index by `entity_type,entity_id,created_at` | `actorUserId, traceId, changes` | `auditLogId` | Audit material business action. | Main transaction | `{{SYSTEM_ERROR_OR_REQUIRED_POLICY}}` |
| 9.2 | `INSERT` | `outboxRepository.enqueue(...)` | `outbox_event` / chosen table | `event_type,payload,trace_id,status` | N/A | Idempotency/event key unique | `eventData` | `eventId` | Reliable async publication. | Main transaction | `{{SYSTEM_ERROR_OR_ALERT_POLICY}}` |

### 7.1. SQL/ORM query intent (optional but recommended for critical API)

```sql
-- Pseudocode only. Must use parameter binding; never interpolate raw client input.
SELECT id, status, owner_id, version
FROM {{table}}
WHERE id = :resourceId
  AND deleted_at IS NULL
  AND owner_id = :actorUserId;
```

| Query ID | Expected cardinality | Explain plan / index expectation | Max rows | Avoid N+1? | Notes |
|---|---|---|---:|---|---|
| `Q-01` | `0..1` | `{{INDEX_NAME}}` | `1` | `N/A` | `{{NOTES}}` |

## 8. Command-to-persistence field mapping

| Domain / command field | Source variable | Target table.column | Transform | Write condition | Null/default policy | Audit? | Notes |
|---|---|---|---|---|---|---|---|
| `{{command.field}}` | `{{normalizedField}}` | `{{table.column}}` | `{{TRANSFORM}}` | `{{WHEN}}` | `{{POLICY}}` | `Y/N` | `{{NOTES}}` |
| `createdAt` | `nowUtc` | `{{table.created_at}}` | UTC timestamp | Create only | Required | `Y` | Server-generated. |
| `updatedAt` | `nowUtc` | `{{table.updated_at}}` | UTC timestamp | Every write | Required | `Y` | Server-generated. |
| `updatedBy` | `actorUserId` | `{{table.updated_by}}` | None | Every write if column exists | Required | `Y` | Derived from auth only. |

## 9. Transaction, consistency and concurrency

### 9.1. Transaction boundary

| Item | Decision | Detail |
|---|---|---|
| Begins before | `{{FIRST_WRITE_OR_READ_LOCK_STEP}}` | `{{WHY}}` |
| Includes writes | `{{TABLES_INCLUDED}}` | Must commit/rollback together. |
| Isolation level | `{{READ_COMMITTED / REPEATABLE_READ / SERIALIZABLE}}` | Rationale tied to race condition. |
| Locking | `{{NONE / FOR_UPDATE / ADVISORY_LOCK / OPTIMISTIC_VERSION}}` | Target rows/keys. |
| Commit condition | `{{ALL_REQUIRED_WRITES_SUCCESS}}` | `{{DETAIL}}` |
| Rollback conditions | `{{LIST_OF_FAILURES}}` | No partial business state. |
| External calls inside transaction? | `No` by default | If `Yes`, justify, timeout and compensation mandatory. |
| Post-commit actions | `{{CACHE_INVALIDATION_EVENTS_NOTIFICATIONS}}` | Use outbox/job where reliable delivery is needed. |

### 9.2. Race-condition analysis

| Race / duplicate risk | Example | Prevention | Failure outcome | Test approach |
|---|---|---|---|---|
| Duplicate create | Two requests create same unique resource. | Unique index + idempotency key. | `409 {{ERROR_CODE}}` or return first result. | Parallel integration test. |
| Stale update | Two users edit same record. | Version/ETag optimistic lock. | `409/412 {{ERROR_CODE}}` | Concurrent update test. |
| State transition race | Submit/review happens twice. | Atomic `WHERE status IN (...)` + version. | `409 {{ERROR_CODE}}` | Double-submit test. |
| Quota / capacity race | Two users claim last slot. | Transactional count/lock/reservation. | `409 {{ERROR_CODE}}` | Parallel boundary test. |

## 10. Cache mapping

> Chỉ điền khi cache thực sự được dùng. Ghi rõ cache không phải source of truth.

| Cache operation | Key pattern | Value source | TTL | Read condition | Invalidation trigger | Failure behavior | Notes |
|---|---|---|---|---|---|---|---|
| `GET` | `{{namespace}}:{{key}}` | `{{TABLE_OR_READ_MODEL}}` | `{{SECONDS}}` | `{{WHEN_TO_LOOKUP}}` | N/A | Fallback DB. | `{{NOTES}}` |
| `SET` | `{{namespace}}:{{key}}` | Response/read model | `{{SECONDS}}` | On cache miss | Write/update/delete event. | Do not fail API unless required. | `{{NOTES}}` |
| `DEL/PUBLISH` | `{{namespace}}:{{key}}` | Mutation event | N/A | Post-commit | `{{EVENT}}` | Async retry/alert if critical. | `{{NOTES}}` |

## 11. External service / storage / AI mapping

| Call ID | Dependency | Trigger condition | Request mapping | Response mapping | Timeout | Retry/circuit breaker | Fallback / compensation | Data classification | Observability |
|---|---|---|---|---|---:|---|---|---|---|
| `EXT-01` | `{{SERVICE}}` | `{{WHEN}}` | `{{REQUEST_FIELDS_TO_EXTERNAL}}` | `{{EXTERNAL_FIELDS_TO_DOMAIN}}` | `{{MS}}` | `{{POLICY}}` | `{{FALLBACK_OR_FAIL}}` | `{{CLASS}}` | `traceId, metric, error code` |

> AI outputs are suggestions/drafts, not source-of-truth. If AI result changes user-visible or persistent business data, specify review/approval, prompt safety, moderation and retention policy.

## 12. Event, job and notification mapping

| Event / job | When generated | Payload fields | Delivery | Consumer(s) | Idempotency key | Retry / DLQ | User-visible effect |
|---|---|---|---|---|---|---|---|
| `{{DomainEventName}}` | After committed `{{STATE_TRANSITION}}` | `{{SAFE_PAYLOAD_FIELDS}}` | Outbox/queue | `{{CONSUMERS}}` | `{{KEY}}` | `{{POLICY}}` | `{{NOTIFICATION_OR_ASYNC_WORK}}` |

## 13. Response field lineage

> Một response field có thể đến từ table, derived calculation, snapshot hoặc external result. Ghi cụ thể để tránh mapping sai/lộ PII.

| Response JSON path | Source type | Source | Transform / mask | Authorization/visibility filter | Null/empty rule | Notes |
|---|---|---|---|---|---|---|
| `data.{{fieldName}}` | `table column` | `{{table.column}}` | `{{TRANSFORM}}` | `{{POLICY}}` | `{{NULL_POLICY}}` | `{{NOTES}}` |
| `data.{{derivedField}}` | `derived` | `{{formula_or_service}}` | `{{ROUNDING_MAPPING}}` | `{{POLICY}}` | `{{NULL_POLICY}}` | Mark not source of truth. |
| `data.{{snapshotField}}` | `snapshot` | `{{snapshot_table.column}}` | `{{TRANSFORM}}` | `{{POLICY}}` | `{{NULL_POLICY}}` | Include snapshot timestamp/version if needed. |
| `data.{{items[]}}` | `query result` | `{{query_or_read_model}}` | `{{SORT_FILTER_MAP}}` | `{{POLICY}}` | `[]` for zero result | `{{NOTES}}` |

## 14. Audit, logging, metrics and tracing

### 14.1. Audit log

| Audit field | Source | Required | Masking / retention | Notes |
|---|---|---:|---|---|
| `actor_id` | `actorUserId` | `Y/N` | Internal; retention per policy. | `null` for guest/system action as defined. |
| `action` | API/business action | Y | Internal | Example `ASSIGNMENT_SUBMISSION_CREATED`. |
| `entity_type/entity_id` | Persisted result | Y | Internal | Resource impacted. |
| `before_json/after_json` | Diff mapper | Conditional | Mask PII/credential. | Do not include password/token. |
| `trace_id` | `traceId` | Y | Internal | Cross-system correlation. |

### 14.2. Structured logs

| Level | Checkpoint | Required fields | Masked fields | Alert? |
|---|---|---|---|---|
| `INFO` | `{{MODULE}}-{{ACTION}}-REQ_RECEIVED` | traceId, apiCode, actorUserId?, request summary | credentials/PII | No |
| `INFO` | `{{MODULE}}-{{ACTION}}-SUCCESS` | traceId, durationMs, resourceId?, outcome | PII | No |
| `WARN` | `{{MODULE}}-{{ACTION}}-BUSINESS_REJECTED` | traceId, businessCode, ruleId | raw request PII | Threshold-based |
| `ERROR` | `{{MODULE}}-{{ACTION}}-ERROR` | traceId, error class, dependency, durationMs | stack/internal details restricted | Yes for severity threshold |

### 14.3. Metrics and SLO

| Metric | Type | Labels | Target / alert |
|---|---|---|---|
| `api_request_total` | Counter | apiCode,httpStatus,businessCode | Track volume/outcome. |
| `api_duration_ms` | Histogram | apiCode,method | p95 `{{TARGET}}`. |
| `api_error_total` | Counter | apiCode,errorCategory | Alert threshold `{{THRESHOLD}}`. |
| `db_query_duration_ms` | Histogram | queryId/table | Detect regression. |
| `external_dependency_duration_ms` | Histogram | dependency,outcome | Circuit breaker alert. |

## 15. Failure branches and mapping

| Flow step | Failure condition | Rollback? | HTTP / business code | Client-safe response | Internal action |
|---:|---|---|---|---|---|
| 2 | Token invalid/expired/revoked. | N/A | `401 {{ERROR_CODE}}` | Auth message. | Security log, no raw token. |
| 3 | Role/ownership fails. | N/A | `403/404 {{ERROR_CODE}}` | Permission/not found safe message. | Audit as policy. |
| 4 | DTO/cross-field validation fail. | N/A | `400/422 {{ERROR_CODE}}` | `errors[]` field detail. | Validation metric. |
| 6 | Target resource absent/soft-deleted. | N/A | `404 {{ERROR_CODE}}` | Not-found message. | `WARN` if unexpected. |
| 7 | State/invariant invalid. | N/A | `409 {{ERROR_CODE}}` | State conflict message. | Business reject log. |
| 8/10 | Unique/FK/check/version DB failure. | Yes | `409/500 {{ERROR_CODE}}` | Conflict/generic message. | Rollback + error log. |
| 11 | Notification/cache/event fails post-commit. | No (unless saga) | `{{SUCCESS_OR_WARNING_POLICY}}` | Do not lie about core business outcome. | Retry/DLQ/alert. |
| External | Timeout/unavailable. | Depends | `502/503/504 {{ERROR_CODE}}` | Temporary failure message. | Circuit breaker/metric. |

## 16. Test data and observability fixtures

| Fixture ID | Initial state | Request variation | Expected DB state | Expected response | Expected logs/events |
|---|---|---|---|---|---|
| `FX-01` | `{{HAPPY_STATE}}` | Valid request. | `{{EXPECTED_WRITES}}` | `2xx {{SUCCESS_CODE}}` | Success checkpoint + audit/event. |
| `FX-02` | `{{NO_PERMISSION_STATE}}` | Valid syntax, unauthorized actor. | No writes. | `403/404 {{ERROR_CODE}}` | AuthZ rejected log. |
| `FX-03` | `{{CONFLICT_STATE}}` | Duplicate/stale operation. | No invalid mutation. | `409/412 {{ERROR_CODE}}` | Conflict log. |
| `FX-04` | `{{DEPENDENCY_FAILURE_STATE}}` | Valid request. | `{{ROLLBACK_OR_PENDING}}` | `{{STATUS_CODE}}` | Dependency error trace/metric. |

## 17. DataMapping review checklist

- [ ] Every runtime variable has source, type, transform and log/masking policy.
- [ ] Flow shows parse → validate → authN → authZ → load → domain rule → persist → audit/outbox → commit → post-commit → response.
- [ ] Every DB access lists repository method, operation, table/columns, predicate, constraint/lock, input/output and error mapping.
- [ ] Transaction, rollback, concurrency and duplicate/retry behavior are explicit.
- [ ] Cache/external service/AI/event/notification behavior is specific and safe.
- [ ] Response field lineage can be traced to source/derived/snapshot data.
- [ ] Audit/log/metric/trace requirements support debugging with `traceId`.

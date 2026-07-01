# 06. Error – {{API_NAME}}

> **Mục đích:** chuẩn hóa các lỗi API ở mức business và technical để Client biết cách xử lý, Backend trả contract ổn định, QA có test case rõ ràng, và vận hành có log/alert đúng nơi. Mỗi lỗi phải an toàn cho client và đủ chính xác cho developer/support thông qua `traceId` và internal log.

---

## 1. Error policy

1. Mỗi lỗi nghiệp vụ có **business code ổn định**, không thay đổi tùy ý theo message hoặc exception class.
2. HTTP status diễn đạt loại kết quả transport; business code diễn đạt nguyên nhân/action có ý nghĩa nghiệp vụ.
3. Không đưa stack trace, SQL, internal URL, secret, token, thông tin account khác hoặc dependency raw response ra client.
4. Validation lỗi phải định vị được field/rule nhưng không được dùng để enumeration hoặc tiết lộ PII.
5. Lỗi `404 resource not found` khác `200 empty list`.
6. Lỗi `401` khác `403`: `401` chưa xác thực, `403` đã xác thực nhưng không được phép.
7. Chỉ retry các lỗi transient và chỉ khi operation retry-safe/idempotent; không retry validation, permission, business rule hay duplicate conflict một cách mù quáng.
8. DB exception cần map sang business code deterministically (unique → conflict; version conflict → precondition/conflict; unknown → internal), không để raw exception leak.
9. Mọi `5xx`, dependency failure, auth abuse và lỗi critical phải có trace/metric/alert theo severity.

## 2. Error code convention

### 2.1. Business error code pattern

```text
{{MODULE}}-{{CATEGORY}}-{{NNN}}
```

Ví dụ:

```text
AUTH-VALIDATION-001
AUTH-CREDENTIAL-001
LEARN-NOT-FOUND-001
LEARN-STATE-002
PROJECT-CONFLICT-001
EMPLOYER-FORBIDDEN-001
AI-DEPENDENCY-001
SYSTEM-RATE-LIMIT-001
```

### 2.2. Category standard

| Category | Khi dùng | HTTP thường dùng | Retry mặc định |
|---|---|---:|---|
| `VALIDATION` | Field schema/format/range/cross-field invalid. | `400` hoặc `422` | No |
| `UNAUTHENTICATED` | Missing/invalid/expired/revoked auth. | `401` | Conditional after refresh/login |
| `FORBIDDEN` | Actor lacks role/permission/ownership. | `403` | No |
| `NOT_FOUND` | Resource không tồn tại/không visible theo policy. | `404` | No |
| `CONFLICT` | Duplicate unique value, concurrent/state conflict. | `409` | Conditional after user resolution/refetch |
| `PRECONDITION` | ETag/version or precondition not met. | `412` | Conditional after reload |
| `STATE` | Resource state không cho phép hành động. | `409` | No until state changes |
| `LIMIT` | Quota/capacity/domain limit reached. | `409` hoặc `422` | No until condition changes |
| `RATE_LIMIT` | Request frequency too high. | `429` | Yes after `Retry-After` |
| `DEPENDENCY` | External service/storage/queue unavailable. | `502/503/504` | Yes if idempotent/backoff |
| `SECURITY` | Unsafe/security policy/replay/suspicious input. | `400/401/403/429` | No/Conditional |
| `INTERNAL` | Unexpected server failure. | `500` | Conditional |

### 2.3. Legacy/system correlation (optional)

Nếu hệ thống cần map code kỹ thuật tổng quát, dùng thêm reference nội bộ nhưng **không thay thế** business code:

| Internal technical class | Typical HTTP | Reference | Usage |
|---|---:|---|---|
| Unauthorized | `401` | `E401` | JWT/session technical issue. |
| Forbidden | `403` | `E403` | Permission technical issue. |
| Not found | `404` | `E404` | Resource query returned no row. |
| Duplicate | `409` | `E409` | Unique constraint/concurrent duplicate. |
| Validation | `400/422` | `E422` | DTO/schema invalid. |
| Internal | `500` | `E500` | Unhandled/system exception. |
| Bad gateway | `502` | `E502` | Dependency bad response. |
| Timeout | `504` | `E504` | Dependency/request timed out. |

## 3. Standard error response contract

```json
{
  "businessCode": "{{MODULE}}-{{CATEGORY}}-{{NNN}}",
  "message": "{{SAFE_CLIENT_MESSAGE}}",
  "timestamp": "2026-07-01T11:45:00Z",
  "traceId": "6a0ae20b-8407-4f0e-93c3-0279d8171c5e",
  "errors": [
    {
      "field": "{{JSON_PATH_OR_NULL}}",
      "code": "{{FIELD_OR_SUB_ERROR_CODE}}",
      "message": "{{SAFE_FIELD_MESSAGE}}",
      "meta": {
        "{{ONLY_SAFE_PUBLIC_CONSTRAINT}}": "{{VALUE}}"
      }
    }
  ]
}
```

| Field | Required | Rule |
|---|---:|---|
| `businessCode` | Y | Stable, documented in error catalog. |
| `message` | Y | Safe, concise, user-facing/localizable; no implementation detail. |
| `timestamp` | Y | Server UTC ISO-8601. |
| `traceId` | Y | Shareable with support; maps to internal log. |
| `errors` | Conditional | Required for repairable validation when safe; omit/empty on generic security/internal cases according to policy. |
| `errors[].field` | Conditional | Exact request JSON path or `null` for global error. |
| `errors[].code` | Conditional | More granular field/rule code; does not replace top-level businessCode. |
| `errors[].meta` | Optional | Only allowed constraints such as min/max, never internal query/result. |

## 4. API-specific error catalog

> Một dòng cho mỗi lỗi có ý nghĩa khác nhau. Không dùng một code `FAILED` cho nhiều nguyên nhân không liên quan.

| No. | Error code | HTTP | Category | When returned / trigger | Technical detection point | Safe client message | Field / resource | Client action | Retry | Severity | Log level / checkpoint | Alert / owner | Test ID |
|---:|---|---:|---|---|---|---|---|---|---|---|---|---|---|
| 1 | `{{MODULE}}-VALIDATION-001` | `400/422` | Validation | `{{MISSING_OR_INVALID_INPUT}}` | DTO/validation pipe | `{{SAFE_MESSAGE}}` | `{{FIELD}}` | Correct input. | N | Low | WARN `{{MODULE}}-{{ACTION}}-VALIDATION_FAILED` | No / Backend | `{{TEST_ID}}` |
| 2 | `{{MODULE}}-UNAUTHENTICATED-001` | `401` | Unauthenticated | Missing/expired/invalid token. | Auth guard/session validator | `Authentication is required.` | `null` | Login/refresh token by policy. | Conditional | Medium | WARN `AUTH-UNAUTHENTICATED` | Security threshold / Backend | `{{TEST_ID}}` |
| 3 | `{{MODULE}}-FORBIDDEN-001` | `403` | Forbidden | Actor lacks permission/ownership. | Policy/ownership query | `You do not have permission to perform this action.` | `{{RESOURCE_OR_NULL}}` | Stop or request correct access. | N | Medium | WARN `{{MODULE}}-AUTHZ_DENIED` | Security review if spike / Backend | `{{TEST_ID}}` |
| 4 | `{{MODULE}}-NOT-FOUND-001` | `404` | Not found | Resource absent/soft-deleted/not visible by policy. | Repository query | `The requested resource was not found.` | `{{RESOURCE}}` | Refresh/back to list. | N | Low | INFO/WARN `{{MODULE}}-RESOURCE_NOT_FOUND` | No / Backend | `{{TEST_ID}}` |
| 5 | `{{MODULE}}-CONFLICT-001` | `409` | Conflict | Duplicate/state/version conflict. | Unique constraint/domain check/version update count | `{{SAFE_CONFLICT_MESSAGE}}` | `{{FIELD_OR_RESOURCE}}` | Resolve conflict/reload/retry only if safe. | Conditional | Medium | WARN `{{MODULE}}-CONFLICT` | Threshold / Backend | `{{TEST_ID}}` |
| 6 | `{{MODULE}}-STATE-001` | `409` | State | Resource state disallows action. | Aggregate/domain service | `{{SAFE_STATE_MESSAGE}}` | `{{RESOURCE}}` | Wait/change state. | N | Medium | WARN `{{MODULE}}-INVALID_STATE` | No / Backend | `{{TEST_ID}}` |
| 7 | `{{MODULE}}-LIMIT-001` | `409/422` | Limit | Quota/capacity/attempt limit exceeded. | Domain service/count query | `{{SAFE_LIMIT_MESSAGE}}` | `{{RESOURCE}}` | Wait/change plan/contact admin. | N | Medium | WARN `{{MODULE}}-LIMIT_REACHED` | Product metric / Owner | `{{TEST_ID}}` |
| 8 | `SYSTEM-RATE-LIMIT-001` | `429` | Rate limit | Caller exceeds configured policy. | Gateway/rate limiter | `Too many requests. Please try again later.` | `null` | Respect `Retry-After`. | Y | Medium | WARN `SYSTEM-RATE_LIMITED` | Security threshold / DevOps | `{{TEST_ID}}` |
| 9 | `{{MODULE}}-DEPENDENCY-001` | `502/503/504` | Dependency | External service/storage/queue timeout or unavailable. | Integration adapter | `A dependent service is temporarily unavailable.` | `null` | Retry with backoff if operation safe. | Y | High | ERROR `{{MODULE}}-DEPENDENCY_ERROR` | On-call / dependency owner | `{{TEST_ID}}` |
| 10 | `SYSTEM-INTERNAL-001` | `500` | Internal | Unexpected exception / unmapped failure. | Global exception filter | `An unexpected error occurred. Please try again later.` | `null` | Retry only if client policy says safe; provide traceId to support. | Conditional | Critical | ERROR `{{MODULE}}-{{ACTION}}-ERROR` | On-call / Backend | `{{TEST_ID}}` |

## 5. Field validation error catalog (optional but recommended)

| Field JSON path | Rule ID | Sub-code | Condition | HTTP/top-level code | Field message | Example invalid input | Example valid input |
|---|---|---|---|---|---|---|---|
| `{{fieldName}}` | `REQ-VAL-001` | `{{MODULE}}-VALIDATION-{{FIELD}}-REQUIRED` | Missing/blank not allowed. | `422 / {{MODULE}}-VALIDATION-001` | `{{FIELD}} is required.` | `null`, `""` | `{{VALID_VALUE}}` |
| `{{fieldName}}` | `REQ-VAL-002` | `{{MODULE}}-VALIDATION-{{FIELD}}-FORMAT` | Invalid format/pattern. | `422 / {{MODULE}}-VALIDATION-001` | `{{FIELD}} format is invalid.` | `{{INVALID}}` | `{{VALID}}` |
| `{{fieldName}}` | `REQ-VAL-003` | `{{MODULE}}-VALIDATION-{{FIELD}}-RANGE` | Outside min/max/range. | `422 / {{MODULE}}-VALIDATION-001` | `{{FIELD}} must be between {{MIN}} and {{MAX}}.` | `{{INVALID}}` | `{{VALID}}` |

## 6. Error decision and masking rules

| Situation | HTTP / code policy | Client message | Internal log detail | Security / privacy note |
|---|---|---|---|---|
| Unknown email vs wrong password | Use same non-enumerating auth response where required. | Generic credentials message. | Record actual reason safely. | Prevent account enumeration. |
| Resource owned by another user | Return `403` or `404` according to visibility policy. | Generic safe message. | Store actor/resource/policy only. | Never leak owner identity. |
| Unique email/phone | `409 CONFLICT` + field sub-error. | Already in use. | Constraint name safe internally. | Avoid exposing account details beyond explicit registration policy. |
| DB unavailable | `500/503`, dependency/internal code. | Temporary generic message. | Exception class/queryId, no SQL/PII in client. | Alert on recurrence. |
| External AI/service error | `502/503/504` or async job failure. | Temporary service message. | Provider error class/request ID. | Do not log prompt content raw if PII/sensitive. |
| File rejected | `400/422` security/validation code. | Safe file rule explanation. | Scanner reason, hash, mime. | Never echo malicious content. |

## 7. Retry and client recovery policy

| Category | Is retry allowed? | Retry method | Max attempts | Backoff | Idempotency requirement | Client UX |
|---|---|---|---:|---|---|---|
| Validation | No | User fixes input. | 0 | N/A | N/A | Highlight field. |
| Auth expired | Conditional | Refresh once, then re-login. | 1 | Immediate/controlled | Refresh flow safe. | Preserve unsent non-sensitive draft where safe. |
| Forbidden/not found/state | No | User changes context/state. | 0 | N/A | N/A | Explain/redirect. |
| Conflict/precondition | Conditional | Refetch then user-confirm retry. | 1 | Immediate | Must not overwrite silently. | Show conflict state. |
| Rate limit | Yes | Respect `Retry-After`. | `{{MAX}}` | Server instructed/exponential | Safe request. | Countdown/throttle UI. |
| Dependency/internal | Conditional | Exponential backoff + jitter. | `{{MAX}}` | `{{POLICY}}` | Idempotency or read-only. | Retry action with traceId. |

## 8. Observability and incident handling

### 8.1. Error log fields

| Field | Required | Notes |
|---|---:|---|
| `timestamp` | Y | UTC. |
| `traceId` | Y | Same as response. |
| `apiCode` / `moduleCode` | Y | Correlate business operation. |
| `httpStatus` / `businessCode` | Y | Categorize outcome. |
| `actorUserId` | Conditional | Do not log raw PII if not needed. |
| `resourceId` | Conditional | Use if safe/useful. |
| `errorClass` / `dependency` | Y for technical error | Internal only. |
| `durationMs` | Y | Detect slow failures. |
| `retryAttempt` | Conditional | Important for async/external. |
| `maskedRequestSummary` | Conditional | Never include password/token/OTP/raw CV content. |

### 8.2. Alert policy

| Condition | Severity | Alert target | Initial action | Escalation |
|---|---|---|---|---|
| `5xx rate > {{THRESHOLD}}` over `{{WINDOW}}` | Critical | On-call Backend/DevOps | Check dashboard + trace samples. | Incident process. |
| Dependency timeout/circuit open | High | Dependency owner + Backend | Verify provider/network/fallback. | Product if feature impact. |
| Repeated auth failures from identity/IP | High | Security / DevOps | Rate limit/review suspicious pattern. | Security incident if confirmed. |
| Validation/conflict spike | Medium | Product + Backend | Inspect UX/contract/regression. | Release rollback if change-induced. |
| Single user-reported `traceId` | Low/Medium | Support + Backend | Search trace, follow safe support process. | Escalate by severity. |

## 9. Error test matrix

| Test ID | Precondition | Request / fault injection | Expected HTTP | Expected business code | DB state | Log / metric / alert expectation |
|---|---|---|---:|---|---|---|
| `{{API_CODE}}-E01` | None | Missing required `{{field}}`. | `422` | `{{MODULE}}-VALIDATION-001` | No write. | Validation WARN, no alert. |
| `{{API_CODE}}-E02` | Missing/expired token. | No/invalid auth header. | `401` | `{{MODULE}}-UNAUTHENTICATED-001` | No write. | Auth WARN, masked token. |
| `{{API_CODE}}-E03` | Unauthorized actor. | Valid data but wrong owner/role. | `403/404` | `{{MODULE}}-FORBIDDEN-001` | No write. | AuthZ denied log. |
| `{{API_CODE}}-E04` | Missing resource. | Unknown id. | `404` | `{{MODULE}}-NOT-FOUND-001` | No write. | Resource-not-found event. |
| `{{API_CODE}}-E05` | Existing conflicting resource/version. | Duplicate/stale request. | `409/412` | `{{MODULE}}-CONFLICT-001` | Atomic no invalid write. | Conflict WARN. |
| `{{API_CODE}}-E06` | Dependency stub timeout. | Valid request. | `504` | `{{MODULE}}-DEPENDENCY-001` | Rollback/pending per design. | ERROR + metric/alert policy. |
| `{{API_CODE}}-E07` | Force unknown exception. | Valid request. | `500` | `SYSTEM-INTERNAL-001` | Rollback required writes. | ERROR with traceId; no leakage. |

## 10. Error review checklist

- [ ] Every error scenario has unique business code, HTTP status, trigger, client action, retry rule and test ID.
- [ ] No sensitive/internal details appear in client message or error meta.
- [ ] 401/403/404/409/422/429/5xx semantic differences are correctly applied.
- [ ] Error codes map consistently to request validation, data mapping branches and response examples.
- [ ] Retry policy respects idempotency and prevents duplicate mutation.
- [ ] Critical errors have trace/log/metric/alert owner.

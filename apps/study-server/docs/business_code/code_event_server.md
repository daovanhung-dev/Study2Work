# Server business/event code catalog

Nguồn: runtime source và Work OpenAPI còn tồn tại, kiểm tra ngày 2026-08-26.
`status` phân biệt code chạy được với declaration/unwired helper.

| Code | Module | Meaning / condition | HTTP | Used by | Status |
|---|---|---|---:|---|---|
| `SYSTEM_ROOT_LOADED` | Study system | Intended root response | 200 | `apps/study-server/app/main.py` | `DECLARED_NOT_RUNNABLE` |
| `SYSTEM_HEALTH_LIVE` | Study health | Intended liveness response | 200 | `apps/study-server/app/main.py` | `DECLARED_NOT_RUNNABLE` |
| `SYSTEM_HEALTH_READY` | Study health | Intended configured-dependency response; no probe | 200 | `apps/study-server/app/main.py` | `DECLARED_NOT_RUNNABLE` |
| `AUTH_CURRENT_USER_FOUND` | Study auth | Intended authenticated-user response | 200 | `apps/study-server/app/api/v1.py` | `DECLARED_NOT_RUNNABLE` |
| `VALIDATION_ERROR` | Study core | Intended request validation failure | 422 | `apps/study-server/app/core/exceptions.py` | `DECLARED_NOT_RUNNABLE` |
| `HTTP_ERROR` | Study core | Intended safe mapping of framework HTTP errors | source status | `apps/study-server/app/core/exceptions.py` | `DECLARED_NOT_RUNNABLE` |
| `INTERNAL_SERVER_ERROR` | Study core | Intended unhandled exception mapping | 500 | `apps/study-server/app/core/exceptions.py` | `DECLARED_NOT_RUNNABLE` |
| `SYSTEM_ROOT_LOADED` | Work system | Public Work API root loaded | 200 | `src/system/system.controller.ts` | `VERIFIED` |
| `SYSTEM_HEALTH_LIVE` | Work health | Process is live | 200 | `src/health/health.controller.ts` | `VERIFIED` |
| `SYSTEM_HEALTH_READY` | Work health | PostgreSQL probe succeeded | 200 | `src/health/health.controller.ts` | `VERIFIED` |
| `DEPENDENCY_UNAVAILABLE` | Work health/auth/core | DB/JWKS or status-503 dependency unavailable | 503 | health service, JWKS service, exception filter | `VERIFIED` |
| `AUTHENTICATION_REQUIRED` | Work auth | Non-public route lacks one valid Bearer token | 401 | `src/auth/jwks-auth.guard.ts` | `VERIFIED`, no current protected route |
| `INVALID_ACCESS_TOKEN` | Work auth | Signature/claims/type/token invalid | 401 | `src/auth/jwks-auth.service.ts` | `VERIFIED`, no current protected route |
| `ACCESS_TOKEN_EXPIRED` | Work auth | JWT expired | 401 | `src/auth/jwks-auth.service.ts` | `VERIFIED`, no current protected route |
| `VALIDATION_ERROR` | Work HTTP | Global DTO validation failed | 422 | `src/common/http/validation-exception.ts` | `VERIFIED`, no current DTO route |
| `HTTP_ERROR` | Work HTTP | Framework `HttpException` safe fallback | exception status | `src/common/http/api-exception.filter.ts` | `VERIFIED` |
| `INTERNAL_SERVER_ERROR` | Work HTTP | Unhandled non-503 error | 500 | `src/common/http/api-exception.filter.ts` | `VERIFIED` |
| `REQUEST_SUCCEEDED` | Work HTTP | Default success metadata when route has no `ApiSuccess` | 200/default | `src/common/http/api-envelope.interceptor.ts` | `VERIFIED` fallback; no current caller |

AI server hiện không phát business code và trả raw JSON. Không tự gán code cho
AI route nếu chưa có contract.

## Maintenance rule

Trước khi thêm identifier, search catalog + source, kiểm tra trùng meaning và
scope owner, rồi cập nhật condition, HTTP mapping, `used_by`, tests và module
context trong cùng change.

# HTTP status catalog

Chỉ ghi status có bằng chứng trong runtime/contract/test hiện tại.

| HTTP | Scope | Condition | Business code |
|---:|---|---|---|
| 200 | Work | Root/live/ready success | `SYSTEM_ROOT_LOADED`, `SYSTEM_HEALTH_LIVE`, `SYSTEM_HEALTH_READY` |
| 200 | AI | Raw root/chat success; FastAPI default | none |
| 200 | Study | Default/intended declared route success | Study system/auth codes hoặc none; app hiện không runnable |
| 204 | Work | CORS preflight handled by Fastify CORS | none |
| 401 | Work | Missing/invalid/expired Bearer access token | `AUTHENTICATION_REQUIRED`, `INVALID_ACCESS_TOKEN`, `ACCESS_TOKEN_EXPIRED` |
| 404 | Work | Unknown route through exception filter | `HTTP_ERROR` |
| 422 | Work | Global DTO/class-validator failure | `VALIDATION_ERROR` |
| 422 | Study | Intended FastAPI/Pydantic validation handler | `VALIDATION_ERROR` (not runnable) |
| 422 | AI | FastAPI default body validation | none; noncanonical response |
| 500 | Work | Unhandled server failure | `INTERNAL_SERVER_ERROR` |
| 500 | Study | Intended unhandled handler | `INTERNAL_SERVER_ERROR` (not runnable) |
| 500 | AI | Unmapped provider/runtime failure | none; FastAPI default behavior |
| 503 | Work | PostgreSQL/JWKS/recognized dependency unavailable | `DEPENDENCY_UNAVAILABLE` |

`HTTP_ERROR` giữ status gốc của `HttpException`, vì vậy có thể xuất hiện với
status protocol khác 404. Không mặc định 201, 400, 403, 409 hoặc các status khác
cho API mới nếu contract/source chưa yêu cầu.

## Approved design proposal — AC_UNICA V1

Các mã dưới đây chỉ áp dụng cho approved design contract tại
`docs/lists/list_api.md`; chúng chưa được runtime/OpenAPI implement.

| HTTP | Scope | Condition | Business code | Status |
|---:|---|---|---|---|
| 200 | AC_UNICA V1 | Read, synchronous update/delete, operation lookup | `DESIGN_RESOURCE_RETRIEVED`, `DESIGN_RESOURCE_UPDATED`, `DESIGN_RESOURCE_DELETED`, `DESIGN_OPERATION_RETRIEVED` | `DESIGN_PROPOSAL` |
| 201 | AC_UNICA V1 | Synchronous resource creation | `DESIGN_RESOURCE_CREATED` | `DESIGN_PROPOSAL` |
| 202 | AC_UNICA V1 | Queued verification, payment, notification delivery or export | `DESIGN_OPERATION_ACCEPTED` | `DESIGN_PROPOSAL` |
| 401 | AC_UNICA V1 | Missing or invalid JWT | `DESIGN_AUTHENTICATION_REQUIRED` | `DESIGN_PROPOSAL` |
| 403 | AC_UNICA V1 | Role, ownership or resource access denied | `DESIGN_ACCESS_DENIED` | `DESIGN_PROPOSAL` |
| 404 | AC_UNICA V1 | Resource or operation not found | `DESIGN_RESOURCE_NOT_FOUND` | `DESIGN_PROPOSAL` |
| 409 | AC_UNICA V1 | Invalid state or duplicate operation | `DESIGN_STATE_CONFLICT` | `DESIGN_PROPOSAL` |
| 422 | AC_UNICA V1 | Schema or business validation failed | `DESIGN_VALIDATION_ERROR` | `DESIGN_PROPOSAL` |
| 503 | AC_UNICA V1 | Payment, storage, delivery or export dependency unavailable | `DESIGN_DEPENDENCY_UNAVAILABLE` | `DESIGN_PROPOSAL` |
| 500 | AC_UNICA V1 | Unmapped internal failure | `DESIGN_INTERNAL_ERROR` | `DESIGN_PROPOSAL` |

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

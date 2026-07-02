# Request - LEARN-PATH-002

| Field | Value |
|---|---|
| Method | `POST` |
| Endpoint | `/api/v1/learning-paths/{pathId}/enroll` |
| Content-Type | `application/json; charset=utf-8` |
| Accept | `application/json` |
| Auth | `Bearer JWT.` |
| Idempotency | `Required` |

## Headers

| Header | Required | Type | Purpose | Sensitive | Error |
|---|---:|---|---|---:|---|
| `Authorization` | Y | `Bearer <token>` | Xác thực actor nếu endpoint được bảo vệ. | Y | `E401` |
| `X-Trace-Id` | N | UUID | Correlation ID; server tạo mới nếu invalid/missing. | N | _none_ |
| `Idempotency-Key` | Y | string <= 255 | Safe retry cho mutation API cần tránh tạo trùng. | N | `E409` |

## Path Parameters

| Field | Type | Required | Validation | Example | Error |
|---|---|---:|---|---|---|
| `pathId` | `UUID/string` | Y | UUID nếu là ID; enum/string nếu là provider. | 7c3a2f1b-31c5-4a21-9b3e-7d1745c4748a | E422 |

## Query Parameters

| Field | Type | Required | Default | Validation | Example | Error |
|---|---|---:|---|---|---|---|
| _none_ | N/A | N | N/A | Không có query parameter bắt buộc theo source hiện tại. | N/A | N/A |

## Body Fields

| Field | Type | Required | Nullable | Validation | Sensitive class | Example | Error |
|---|---|---:|---:|---|---|---|---|
| `operationData` | `object` | Y | N | Payload nghiệp vụ draft; schema chi tiết cần review. | internal/PII tùy field con | {} | E422 |
| `clientRequestId` | `UUID` | N | N | Correlation id phía client nếu có. | internal | 7c3a2f1b-31c5-4a21-9b3e-7d1745c4748a | E422 |

## Validation Sequence

1. Parse HTTP method, endpoint, header, path, query và body.
2. Validate format, enum, range và required field.
3. Validate cross-field rule nếu body có nhiều field liên quan.
4. Authenticate theo auth scheme.
5. Authorize permission và ownership/scope.
6. Validate state hiện tại và business rules: Eligibility, uniqueness, idempotency, `learning_path_enrollment` source of access.

## Example

```json
{
  "operationData": {},
  "clientRequestId": "7c3a2f1b-31c5-4a21-9b3e-7d1745c4748a"
}
```

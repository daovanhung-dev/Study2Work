# Request - AUTH-OAUTH-001

| Field | Value |
|---|---|
| Method | `GET/POST` |
| Endpoint | `/api/v1/auth/oauth/{provider}` |
| Content-Type | `application/json; charset=utf-8` |
| Accept | `application/json` |
| Auth | `None for public entry; vẫn áp dụng rate limit và anti-abuse.` |
| Idempotency | `Optional` |

## Headers

| Header | Required | Type | Purpose | Sensitive | Error |
|---|---:|---|---|---:|---|
| `Authorization` | N | `Bearer <token>` | Xác thực actor nếu endpoint được bảo vệ. | Y | `E401` |
| `X-Trace-Id` | N | UUID | Correlation ID; server tạo mới nếu invalid/missing. | N | _none_ |
| `Idempotency-Key` | N | string <= 255 | Safe retry cho mutation API cần tránh tạo trùng. | N | `E409` |

## Path Parameters

| Field | Type | Required | Validation | Example | Error |
|---|---|---:|---|---|---|
| `provider` | `UUID/string` | Y | UUID nếu là ID; enum/string nếu là provider. | 7c3a2f1b-31c5-4a21-9b3e-7d1745c4748a | E422 |

## Query Parameters

| Field | Type | Required | Default | Validation | Example | Error |
|---|---|---:|---|---|---|---|
| `state` | `string` | Y | none | Must match server state. | oauth_state_example | E422 |
| `code` | `string` | N | none | Provider callback code. | oauth_code_example | E422 |

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
6. Validate state hiện tại và business rules: Provider allowlist, callback validation, state/nonce, identity linking and no raw OAuth secret logging.

## Example

```json
{
  "operationData": {},
  "clientRequestId": "7c3a2f1b-31c5-4a21-9b3e-7d1745c4748a"
}
```

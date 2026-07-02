# Request - LEARN-LESSON-001

| Field | Value |
|---|---|
| Method | `GET` |
| Endpoint | `/api/v1/lessons/{lessonId}` |
| Content-Type | `application/json; charset=utf-8` |
| Accept | `application/json` |
| Auth | `Bearer JWT.` |
| Idempotency | `Not applicable` |

## Headers

| Header | Required | Type | Purpose | Sensitive | Error |
|---|---:|---|---|---:|---|
| `Authorization` | Y | `Bearer <token>` | Xác thực actor nếu endpoint được bảo vệ. | Y | `E401` |
| `X-Trace-Id` | N | UUID | Correlation ID; server tạo mới nếu invalid/missing. | N | _none_ |
| `Idempotency-Key` | N | string <= 255 | Safe retry cho mutation API cần tránh tạo trùng. | N | `E409` |

## Path Parameters

| Field | Type | Required | Validation | Example | Error |
|---|---|---:|---|---|---|
| `lessonId` | `UUID/string` | Y | UUID nếu là ID; enum/string nếu là provider. | 7c3a2f1b-31c5-4a21-9b3e-7d1745c4748a | E422 |

## Query Parameters

| Field | Type | Required | Default | Validation | Example | Error |
|---|---|---:|---|---|---|---|
| _none_ | N/A | N | N/A | Không có query parameter bắt buộc theo source hiện tại. | N/A | N/A |

## Body Fields

| Field | Type | Required | Nullable | Validation | Sensitive class | Example | Error |
|---|---|---:|---:|---|---|---|---|
| _none_ | N/A | N | N | Không có request body theo source hiện tại. | public | N/A | N/A |

## Validation Sequence

1. Parse HTTP method, endpoint, header, path, query và body.
2. Validate format, enum, range và required field.
3. Validate cross-field rule nếu body có nhiều field liên quan.
4. Authenticate theo auth scheme.
5. Authorize permission và ownership/scope.
6. Validate state hiện tại và business rules: Enforce `BR-LEARN-001`; enrollment ownership and unlock rule; no draft content to student.

## Example

```json
{}
```

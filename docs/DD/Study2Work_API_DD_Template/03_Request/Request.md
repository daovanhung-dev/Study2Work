# Request - {{API_CODE}}

| Field | Value |
|---|---|
| Method | `{{HTTP_METHOD}}` |
| Endpoint | `/api/v1/{{ENDPOINT}}` |
| Content-Type | `application/json; charset=utf-8` |
| Accept | `application/json` |
| Auth | `{{AUTH_SCHEME}}` |
| Idempotency | `Required / Optional / Not applicable` |

## Headers

| Header | Required | Type | Purpose | Sensitive | Error |
|---|---:|---|---|---:|---|
| `Authorization` | Y/N | `Bearer <token>` | Authenticated actor. | Y | `E401` |
| `X-Trace-Id` | N | UUID | Correlation ID; generated if invalid/missing. | N | _none_ |
| `Idempotency-Key` | Y/N | string <= 255 | Safe retry for mutation APIs. | N | `E409` |

## Path Parameters

| Field | Type | Required | Validation | Example | Error |
|---|---|---:|---|---|---|
| `{{fieldName}}` | `UUID` | Y | `{{RULE}}` | `{{UUID}}` | `E422` |

## Query Parameters

| Field | Type | Required | Default | Validation | Example | Error |
|---|---|---:|---|---|---|---|
| `{{fieldName}}` | `string` | N | `{{DEFAULT}}` | `{{RULE}}` | `{{EXAMPLE}}` | `E422` |

## Body Fields

| Field | Type | Required | Nullable | Validation | Sensitive class | Example | Error |
|---|---|---:|---:|---|---|---|---|
| `{{fieldName}}` | `string` | Y | N | `{{RULE}}` | `public/internal/PII/credential/token` | `{{EXAMPLE}}` | `E422` |

## Validation Sequence

1. Parse transport schema.
2. Validate field formats and ranges.
3. Validate cross-field rules.
4. Authenticate where required.
5. Authorize permission and ownership/scope.
6. Validate entity state and business rules.

## Example

```json
{
  "{{fieldName}}": "{{value}}"
}
```

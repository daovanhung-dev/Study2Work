# Error - {{API_CODE}}

## Error Catalog

| ID | HTTP | Error code | Business code | Condition | Safe message | Retry | Log level | Test ID |
|---|---:|---|---|---|---|---|---|---|
| `{{API_CODE}}-ERR-001` | 400 | `E422` | `{{MODULE}}-RESP-INVALID_INPUT` | Invalid request payload. | Validation failed. | No | WARN | `{{API_CODE}}-TC-002` |
| `{{API_CODE}}-ERR-002` | 401 | `E401` | `AUTH-RESP-UNAUTHORIZED` | Missing or invalid token. | Authentication required. | Refresh/re-login | WARN | `{{API_CODE}}-TC-003` |
| `{{API_CODE}}-ERR-003` | 403 | `E403` | `{{MODULE}}-RESP-FORBIDDEN` | Permission or ownership/scope denied. | You do not have permission for this action. | No | WARN | `{{API_CODE}}-TC-004` |
| `{{API_CODE}}-ERR-004` | 404 | `E404` | `{{MODULE}}-RESP-NOT_FOUND` | Resource not found or unavailable. | Resource not found. | No | INFO | `{{API_CODE}}-TC-005` |
| `{{API_CODE}}-ERR-005` | 409 | `E409` | `{{MODULE}}-RESP-CONFLICT` | Duplicate or concurrent state conflict. | Request conflicts with current state. | Maybe | WARN | `{{API_CODE}}-TC-006` |
| `{{API_CODE}}-ERR-006` | 500 | `E500` | `SYSTEM-RESP-INTERNAL_ERROR` | Unexpected server failure. | Internal server error. | Maybe | ERROR | `{{API_CODE}}-TC-007` |

## Error Envelope

```json
{
  "businessCode": "{{MODULE}}-RESP-INVALID_INPUT",
  "message": "Validation failed.",
  "timestamp": "2026-07-01T10:00:00Z",
  "traceId": "7c3a2f1b-31c5-4a21-9b3e-7d1745c4748a",
  "errors": [
    {
      "field": "{{fieldName}}",
      "code": "E422",
      "message": "{{SAFE_FIELD_MESSAGE}}"
    }
  ]
}
```

## Logging Rules

- Never log passwords, raw access tokens, refresh tokens, OAuth secrets, hidden tests, raw private PII, or raw learner source code containing secrets.
- Always include `traceId`, `moduleCode`, `apiCode`, timestamp, and resource identifiers when available.
- Send stack traces only to observability tooling, never to the client.

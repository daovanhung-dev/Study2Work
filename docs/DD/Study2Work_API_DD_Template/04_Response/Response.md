# Response - {{API_CODE}}

## Response Matrix

| Scenario | HTTP | Business code | Data/errors | Client behavior |
|---|---:|---|---|---|
| Success | `200/201/202/204` | `{{MODULE}}-{{ACTION}}-SUCCESS` | `data` | `{{CLIENT_BEHAVIOR}}` |
| Validation failed | `422` | `{{MODULE}}-RESP-INVALID_INPUT` | `errors[]` | Show safe field errors. |
| Unauthorized | `401` | `AUTH-RESP-UNAUTHORIZED` | `errors[]` | Re-login or refresh token. |
| Forbidden | `403` | `{{MODULE}}-RESP-FORBIDDEN` | `errors[]` | Hide or block action. |
| Not found | `404` | `{{MODULE}}-RESP-NOT_FOUND` | `errors[]` | Show not-found state. |
| Conflict | `409` | `{{MODULE}}-RESP-CONFLICT` | `errors[]` | Refresh or resolve state. |
| Dependency unavailable | `502/503/504` | `{{MODULE}}-RESP-DEPENDENCY_UNAVAILABLE` | `errors[]` | Retry only safe actions. |
| Internal error | `500` | `SYSTEM-RESP-INTERNAL_ERROR` | `errors[]` | Show safe support message. |

## Success Envelope

```json
{
  "businessCode": "{{MODULE}}-{{ACTION}}-SUCCESS",
  "message": "{{SUCCESS_MESSAGE}}",
  "timestamp": "2026-07-01T10:00:00Z",
  "traceId": "7c3a2f1b-31c5-4a21-9b3e-7d1745c4748a",
  "data": {}
}
```

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

## Data Fields

| Field | Type | Required | Nullable | Source | Sensitive | Note |
|---|---|---:|---:|---|---:|---|
| `{{fieldName}}` | `string` | Y | N | `{{TABLE_OR_SERVICE}}` | N | `{{NOTE}}` |

## Pagination

If the API returns a list, include pagination:

```json
{
  "pagination": {
    "page": 1,
    "pageSize": 20,
    "totalItems": 0,
    "totalPages": 0
  }
}
```

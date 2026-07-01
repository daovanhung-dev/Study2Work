# 04. Response – {{API_NAME}}

> **Mục đích:** mô tả toàn bộ kết quả API có thể trả về: HTTP status, business code, response envelope, field dictionary, empty case, pagination, async case, success/error sample và hành vi client. `Response` phải cho FE/Mobile/QA biết rõ **trạng thái nào có thể xảy ra** và **xử lý client phải làm gì**.

---

## 1. Response contract summary

| Thuộc tính | Giá trị |
|---|---|
| API business code | `{{API_CODE}}` |
| Success response type | `{{SUCCESS_RESPONSE_DTO}}` |
| Error response type | `{{ERROR_RESPONSE_DTO}}` |
| Media type | `application/json; charset=utf-8` |
| Default charset | `UTF-8` |
| Time standard | ISO-8601 UTC |
| Traceability | `traceId` is returned on all responses unless transport fails before app boundary. |
| Message policy | Safe client message; technical/root-cause details only in internal logs. |
| Response envelope | `Study2Work standard / Exception: {{EXCEPTION_REASON_OR_NA}}` |

## 2. Response scenario matrix

| Scenario | HTTP status | Business code | Data behavior | Message semantics | Client action | Retry? | Notes |
|---|---:|---|---|---|---|---|---|
| Success – existing resource | `200` | `{{MODULE}}-{{ACTION}}-SUCCESS` | `data` populated | Action/query completed. | Render / continue flow. | `N` | `{{NOTE}}` |
| Success – created resource | `201` | `{{MODULE}}-{{ACTION}}-CREATED` | `data` includes identity/state. | Resource created. | Navigate/update state. | `N` | Include `Location` header if applicable. |
| Success – accepted async | `202` | `{{MODULE}}-{{ACTION}}-ACCEPTED` | `data.jobId` / polling URL. | Accepted, not completed. | Poll/subscribe status. | `N` | Must specify final status endpoint. |
| Success – no content | `204` | `{{MODULE}}-{{ACTION}}-SUCCESS` | No JSON body. | State changed successfully. | Refresh local state. | `N` | Use only when client truly needs no payload. |
| Success – empty list | `200` | `{{MODULE}}-{{ACTION}}-SUCCESS` | `data: []`, `totalItems: 0` | Query valid, no item matches. | Render empty state. | `N` | Not `404`. |
| Invalid request | `400` or `422` | `{{MODULE}}-VALIDATION-{{NNN}}` | `errors[]` field details. | Input invalid. | Highlight/repair input. | `N` | No DB write. |
| Unauthenticated | `401` | `AUTH-UNAUTHENTICATED-{{NNN}}` | No sensitive data. | Missing/invalid/expired authentication. | Refresh/login according to client policy. | Conditional | Do not expose token detail. |
| Forbidden | `403` | `{{MODULE}}-FORBIDDEN-{{NNN}}` | No protected data. | Authenticated but not authorized. | Disable/redirect/show permission message. | `N` | Ownership failure may intentionally map to 404; specify policy. |
| Resource not found | `404` | `{{MODULE}}-NOT-FOUND-{{NNN}}` | No resource payload. | Target does not exist/visible. | Refresh/list/back. | `N` | Distinguish from empty search result. |
| State or duplicate conflict | `409` | `{{MODULE}}-CONFLICT-{{NNN}}` | Optional current state/version. | Operation conflicts with current state. | Refresh/resolve/retry after user action. | Conditional | E.g. duplicate email, already submitted. |
| Precondition failed | `412` | `{{MODULE}}-PRECONDITION-{{NNN}}` | Optional latest version. | ETag/version requirement failed. | Reload resource then retry. | Conditional | For optimistic concurrency. |
| Rate limited | `429` | `SYSTEM-RATE-LIMIT-{{NNN}}` | Optional `retryAfterSeconds`. | Too many requests. | Wait then retry. | `Y` | Return `Retry-After` header. |
| Dependency failure | `502/503/504` | `{{MODULE}}-DEPENDENCY-{{NNN}}` | No internal dependency detail. | Temporary downstream problem. | Backoff/retry if safe. | `Y` | Include retry policy. |
| Unexpected internal failure | `500` | `SYSTEM-INTERNAL-{{NNN}}` | No technical detail. | Unexpected failure. | Show generic error; support uses traceId. | Conditional | Must be logged/alerted. |

> Loại bỏ scenario không áp dụng chỉ sau khi có lý do. Không dùng `200` cho lỗi nghiệp vụ.

## 3. Canonical response envelope

### 3.1. Success envelope

| JSON path | Type | Required | Nullable | Default | Source | Visibility | Description | Example |
|---|---|---:|---:|---|---|---|---|---|
| `businessCode` | `string` | Y | N | `-` | Application result | Public | Mã nghiệp vụ ổn định biểu diễn outcome. | `LEARN-QUIZ-SUCCESS` |
| `message` | `string` | Y | N | `-` | Message catalog | Public | Message an toàn, có thể localize. | `Quiz submitted successfully.` |
| `timestamp` | `string(date-time)` | Y | N | Server UTC clock | API boundary | Public | Thời điểm server trả response. | `2026-07-01T11:45:00Z` |
| `traceId` | `string` | Y | N | Trace middleware | Observability | Public/Internal support | Correlation ID cho log/tracing. | `6a0ae...` |
| `data` | `object / array / null` | Y* | Depends | `-` | Response mapper | Depends | Payload nghiệp vụ thành công. | `{}` |
| `pagination` | `object` | Conditional | N | omitted | Query mapper | Public | Chỉ dùng list/search phân trang. | `{...}` |
| `meta` | `object` | Conditional | N | omitted | Application | Public | Metadata kỹ thuật/async/filter/sort, không chứa secret. | `{}` |

`*` Với `204 No Content`, không có body. Với response lỗi, `data` không xuất hiện trừ khi contract nêu rõ.

### 3.2. Error envelope

| JSON path | Type | Required | Nullable | Default | Source | Visibility | Description | Example |
|---|---|---:|---:|---|---|---|---|---|
| `businessCode` | `string` | Y | N | `-` | Error catalog | Public | Mã lỗi ổn định. | `AUTH-VALIDATION-001` |
| `message` | `string` | Y | N | `-` | Error catalog | Public | Safe message cấp response. | `Validation failed.` |
| `timestamp` | `string(date-time)` | Y | N | Server UTC clock | API boundary | Public | Timestamp response. | `2026-07-01T11:45:00Z` |
| `traceId` | `string` | Y | N | Trace middleware | Observability | Public/Internal support | Dùng khi support/debug. | `6a0ae...` |
| `errors` | `array<object>` | Conditional | N | `[]` | Validation/error mapper | Public | Chi tiết lỗi field/rule nếu an toàn. | `[{...}]` |
| `errors[].field` | `string` | Conditional | Y | `null` | Validator | Public | JSON path field lỗi; `null` khi lỗi toàn cục. | `email` |
| `errors[].code` | `string` | Conditional | N | `-` | Error catalog | Public | Mã lỗi field/rule cụ thể. | `AUTH-VALIDATION-EMAIL-001` |
| `errors[].message` | `string` | Conditional | N | `-` | Message catalog | Public | Safe message theo field. | `Email format is invalid.` |
| `errors[].meta` | `object` | Conditional | N | omitted | Validator | Public | Only safe constraints, ví dụ min/max allowed. | `{"min": 8}` |

## 4. Success data field dictionary

> Điền một dòng cho mọi property lồng nhau và item của array. `Source` phải tham chiếu source of truth, derived calculation, snapshot hay external service; không ghi “DB” chung chung.

| No. | Logical field | JSON path | Type | Required | Nullable | Default | Format / Enum | Source / mapping | Data classification | Description | Example | Stable contract? |
|---:|---|---|---|---:|---:|---|---|---|---|---|---|---|
| 1 | `{{FIELD_LOGICAL_NAME}}` | `data.{{fieldName}}` | `uuid` | Y | N | `-` | UUID | `{{table.column}}` | Internal | `{{DESCRIPTION}}` | `{{UUID}}` | `Y` |
| 2 | `{{FIELD_LOGICAL_NAME}}` | `data.{{nested.fieldName}}` | `string` | Y | `{{Y/N}}` | `{{DEFAULT}}` | `{{FORMAT}}` | `{{mapper_or_calculation}}` | Public / PII | `{{DESCRIPTION}}` | `{{EXAMPLE}}` | `Y/N` |
| 3 | `{{FIELD_LOGICAL_NAME}}` | `data.{{items[]}}` | `array<object>` | Y | N | `[]` | `max {{N}}` | `{{query_result}}` | Internal | `{{DESCRIPTION}}` | `[]` | `Y` |
| 4 | `{{FIELD_LOGICAL_NAME}}` | `data.{{items[].fieldName}}` | `{{TYPE}}` | Y | `{{Y/N}}` | `{{DEFAULT}}` | `{{FORMAT}}` | `{{table_or_snapshot.column}}` | `{{CLASSIFICATION}}` | `{{DESCRIPTION}}` | `{{EXAMPLE}}` | `Y/N` |

### 4.1. Data type declaration

```ts
// Documentation-only pseudo TypeScript. Must match OpenAPI/DTO.
interface {{SUCCESS_RESPONSE_DATA_DTO}} {
  {{fieldName}}: {{Type}};
  {{optionalFieldName}}?: {{Type}} | null;
  {{items}}: Array<{
    {{itemField}}: {{Type}};
  }>;
}
```

## 5. Pagination, filter and sorting response

> Chỉ điền cho API list/search. Chọn **một** strategy: page-based hoặc cursor-based; không trộn không có lý do.

### 5.1. Page-based pagination

| JSON path | Type | Description | Example |
|---|---|---|---|
| `pagination.page` | `integer` | Trang hiện tại, 1-based. | `1` |
| `pagination.pageSize` | `integer` | Số item thực trả/requested after cap. | `20` |
| `pagination.totalItems` | `integer` | Tổng số record match filter tại thời điểm query. | `137` |
| `pagination.totalPages` | `integer` | `ceil(totalItems / pageSize)`. | `7` |
| `meta.sort` | `array<object>` | Sort thực áp dụng sau khi default/canonicalize. | `[{"field":"createdAt","direction":"DESC"}]` |
| `meta.appliedFilters` | `object` | Filter server chấp nhận. | `{}` |

### 5.2. Cursor-based pagination

| JSON path | Type | Description | Example |
|---|---|---|---|
| `pagination.nextCursor` | `string` | Cursor opaque cho page tiếp, `null` nếu hết. | `eyJ...` |
| `pagination.previousCursor` | `string` | Cursor opaque cho page trước nếu hỗ trợ. | `null` |
| `pagination.hasNextPage` | `boolean` | Có page sau hay không. | `true` |
| `pagination.pageSize` | `integer` | Số item giới hạn. | `20` |

## 6. Response examples

### 6.1. Success – object payload

```json
{
  "businessCode": "{{MODULE}}-{{ACTION}}-SUCCESS",
  "message": "{{SUCCESS_MESSAGE}}",
  "timestamp": "2026-07-01T11:45:00Z",
  "traceId": "6a0ae20b-8407-4f0e-93c3-0279d8171c5e",
  "data": {
    "{{fieldName}}": "{{value}}",
    "{{nestedObject}}": {
      "{{nestedField}}": "{{value}}"
    }
  }
}
```

### 6.2. Success – empty list

```json
{
  "businessCode": "{{MODULE}}-{{ACTION}}-SUCCESS",
  "message": "No matching records found.",
  "timestamp": "2026-07-01T11:45:00Z",
  "traceId": "6a0ae20b-8407-4f0e-93c3-0279d8171c5e",
  "data": [],
  "pagination": {
    "page": 1,
    "pageSize": 20,
    "totalItems": 0,
    "totalPages": 0
  }
}
```

### 6.3. Success – asynchronous accepted

```json
{
  "businessCode": "{{MODULE}}-{{ACTION}}-ACCEPTED",
  "message": "Your request has been accepted for processing.",
  "timestamp": "2026-07-01T11:45:00Z",
  "traceId": "6a0ae20b-8407-4f0e-93c3-0279d8171c5e",
  "data": {
    "jobId": "{{UUID}}",
    "status": "PENDING",
    "statusUrl": "/api/v1/{{resource}}/jobs/{{UUID}}"
  }
}
```

### 6.4. Error – validation

```json
{
  "businessCode": "{{MODULE}}-VALIDATION-001",
  "message": "Validation failed.",
  "timestamp": "2026-07-01T11:45:00Z",
  "traceId": "6a0ae20b-8407-4f0e-93c3-0279d8171c5e",
  "errors": [
    {
      "field": "{{fieldName}}",
      "code": "{{MODULE}}-VALIDATION-{{FIELD}}-001",
      "message": "{{SAFE_FIELD_MESSAGE}}",
      "meta": {
        "{{SAFE_CONSTRAINT}}": "{{VALUE}}"
      }
    }
  ]
}
```

### 6.5. Error – conflict/state

```json
{
  "businessCode": "{{MODULE}}-CONFLICT-001",
  "message": "The resource cannot be updated in its current state.",
  "timestamp": "2026-07-01T11:45:00Z",
  "traceId": "6a0ae20b-8407-4f0e-93c3-0279d8171c5e",
  "errors": [
    {
      "field": null,
      "code": "{{MODULE}}-STATE-001",
      "message": "{{SAFE_STATE_MESSAGE}}"
    }
  ]
}
```

## 7. Response headers

| Header | Applies to | Required | Value / source | Client behavior |
|---|---|---:|---|---|
| `Content-Type` | JSON response | Y | `application/json; charset=utf-8` | Parse JSON. |
| `X-Trace-Id` | All app responses | Y | Same as body `traceId` or gateway trace ID. | Store for support/debug. |
| `Location` | `201 Created` | Conditional | Newly created resource URI. | Optional navigation/reference. |
| `ETag` | Read/update concurrency | Conditional | Current version hash. | Send via `If-Match` on update. |
| `Retry-After` | `429/503` | Conditional | Seconds/date. | Respect before retry. |
| `Cache-Control` | Cacheable GET | Conditional | `private,max-age={{seconds}}` | Follow cache policy. |

## 8. Client behavior mapping

| Response category | UI state | State management action | User-facing behavior | Telemetry |
|---|---|---|---|---|
| 2xx object | Success | Update entity/cache. | Continue flow/show success when needed. | `{{SUCCESS_EVENT}}` |
| 2xx empty list | Empty | Store empty collection, preserve valid filters. | Render empty state, not technical error. | `{{EMPTY_EVENT}}` |
| 202 | Processing | Store `jobId/statusUrl`; subscribe/poll. | Show processing state. | `{{ASYNC_EVENT}}` |
| 400/422 | Form error | Map `errors[].field` to form control. | Explain repairable input. | `{{VALIDATION_EVENT}}` |
| 401 | Session state | Refresh/logout according to policy; avoid retry loop. | Re-authentication action. | `{{AUTH_EVENT}}` |
| 403 | Forbidden | Do not expose inaccessible data. | Permission feedback/redirect. | `{{FORBIDDEN_EVENT}}` |
| 404 | Missing | Remove stale local entity or return to list. | Not-found state. | `{{NOT_FOUND_EVENT}}` |
| 409/412 | Conflict | Refetch latest resource. | Resolve conflict/retry explicitly. | `{{CONFLICT_EVENT}}` |
| 429/5xx | Temporary error | Backoff/limited retry only if safe. | Retry UI with traceId support. | `{{DEPENDENCY_EVENT}}` |

## 9. Response review checklist

- [ ] Every scenario returns an intentional HTTP status and stable business code.
- [ ] Empty list, not found, no content and async accepted have distinct semantics.
- [ ] All payload fields include JSON path/type/nullability/source/example/classification.
- [ ] Derived/snapshot/external values are explicitly marked.
- [ ] Pagination and sort/filter behavior are fully defined for list/search APIs.
- [ ] Error examples contain safe details only and are consistent with `06_Error/Error.md`.
- [ ] Client behavior for 2xx/4xx/5xx is documented.

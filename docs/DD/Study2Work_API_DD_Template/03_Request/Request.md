# 03. Request – {{API_NAME}}

> **Mục đích:** mô tả đầy đủ mọi dữ liệu client/hệ thống gửi vào API: route, path, query, header, cookie, body, multipart file, semantic của `missing/null/empty`, validation order, transform, security và idempotency. Đây là contract đầu vào, không phải chỉ là mẫu JSON.

---

## 1. Request summary

| Thuộc tính | Giá trị |
|---|---|
| API business code | `{{API_CODE}}` |
| HTTP method | `{{HTTP_METHOD}}` |
| Endpoint | `/api/v{{API_VERSION}}/{{RESOURCE_PATH}}` |
| Request content type | `application/json; charset=utf-8` |
| Response accept | `application/json` |
| Authentication | `{{AUTH_SCHEME}}` |
| Authorization policy | `{{AUTHORIZATION_POLICY}}` |
| Idempotency | `{{REQUIRED_OR_NOT}}` |
| Max request size | `{{MAX_REQUEST_SIZE}}` |
| Request timeout | `{{TIMEOUT_MS}} ms` |
| Caller(s) | `{{CALLERS}}` |
| DTO/schema | `{{REQUEST_DTO_OR_SCHEMA}}` |

## 2. Request transport contract

### 2.1. URL and route parameters

| Location | Name | JSON / URL name | Type | Required | Format / range | Source | Description | Example | Error if invalid |
|---|---|---|---|---|---|---|---|---|---|
| Path | `{{LOGICAL_NAME}}` | `{{pathParam}}` | `uuid / string / integer` | `Y` | `{{FORMAT}}` | URL path | `{{DESCRIPTION}}` | `{{EXAMPLE}}` | `{{ERROR_CODE}}` |
| Query | `{{LOGICAL_NAME}}` | `{{queryParam}}` | `{{TYPE}}` | `N` | `{{FORMAT}}` | Query string | `{{DESCRIPTION}}` | `{{EXAMPLE}}` | `{{ERROR_CODE}}` |

**Endpoint resolution example**

```text
{{HTTP_METHOD}} /api/v{{API_VERSION}}/{{resource}}/{{resourceId}}?{{queryKey}}={{queryValue}}
```

### 2.2. Request headers

| Header | Required | Type / format | Value source | Description | Example | Mask in logs? | Error / behavior if absent |
|---|---|---|---|---|---|---|---|
| `Authorization` | `Y/N` | `Bearer {{JWT}}` | Client session | Token xác thực user/service. | `Bearer eyJ...redacted` | `Y` | `401 {{ERROR_CODE}}` |
| `Content-Type` | `Y` | `application/json; charset=utf-8` | Client | Định dạng body. | `application/json` | `N` | `415 {{ERROR_CODE}}` |
| `Accept` | `Y/N` | `application/json` | Client | Định dạng response chấp nhận. | `application/json` | `N` | `406 {{ERROR_CODE}}` |
| `X-Request-Id` | `N` | UUID/string <= 64 | Client / gateway | Correlation id do client gửi; server có thể tạo `traceId`. | `app-...` | `N` | Server tự tạo nếu vắng. |
| `Idempotency-Key` | `Y/N` | UUID/string <= 255 | Client | Bắt buộc cho create/payment/side-effect không được lặp. | `{{UUID}}` | `N` | `400/409 {{ERROR_CODE}}` |
| `If-Match` | `Y/N` | ETag/version | Client | Optimistic concurrency cho update. | `"v12"` | `N` | `409/412 {{ERROR_CODE}}` |
| `X-Client-Version` | `N` | SemVer | Client | Hỗ trợ compatibility/debug. | `1.8.2` | `N` | Không block trừ khi enforce min version. |
| `X-Timezone` | `N` | IANA time zone | Client | Timezone hiển thị; server vẫn lưu UTC. | `Asia/Ho_Chi_Minh` | `N` | Default server policy. |

> Xóa các dòng không dùng. Thêm header custom phải nêu rõ lý do, source, ttl/semantics và logging policy.

### 2.3. Cookie (chỉ khi áp dụng)

| Cookie | Required | HttpOnly | Secure | SameSite | Source | Purpose | Mask in logs? | Missing behavior |
|---|---|---|---|---|---|---|---|---|
| `{{COOKIE_NAME}}` | `Y/N` | `Y/N` | `Y/N` | `Strict/Lax/None` | `{{SOURCE}}` | `{{PURPOSE}}` | `Y` | `{{BEHAVIOR}}` |

## 3. Request body schema

### 3.1. Field dictionary

> Mỗi field, bao gồm nested object/array item, bắt buộc có một dòng. `Required` khác `Nullable`: required nghĩa là key phải xuất hiện; nullable nghĩa value có thể là `null`.

| No. | Logical field | JSON path | Location | Type | Required | Nullable | Default | Min / Max | Format / Pattern | Allowed value / Enum | Source | Normalization | Validation rules | Sensitive class | Description | Valid example | Error code(s) |
|---:|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | `{{FIELD_LOGICAL_NAME}}` | `{{fieldName}}` | `body` | `string` | `Y` | `N` | `-` | `1 / 100` | `trimmed string` | `-` | UI input | `trim` | `REQ-VAL-001` | `Public / PII / Credential / Internal` | `{{DESCRIPTION}}` | `{{EXAMPLE}}` | `{{ERROR_CODES}}` |
| 2 | `{{FIELD_LOGICAL_NAME}}` | `{{nested.fieldName}}` | `body` | `uuid` | `Y` | `N` | `-` | `36 / 36` | UUID v4 | `-` | UI/state/route | `none` | `REQ-VAL-002` | `Internal` | `{{DESCRIPTION}}` | `{{UUID}}` | `{{ERROR_CODES}}` |
| 3 | `{{FIELD_LOGICAL_NAME}}` | `{{items[]}}` | `body` | `array<object>` | `N` | `N` | `[]` | `0 / 50` items | `-` | `-` | UI input | `deduplicate by id` | `REQ-VAL-003` | `Public` | `{{DESCRIPTION}}` | `[]` | `{{ERROR_CODES}}` |
| 4 | `{{FIELD_LOGICAL_NAME}}` | `{{items[].fieldName}}` | `body` | `string` | `Conditional` | `N` | `-` | `{{MIN/MAX}}` | `{{FORMAT}}` | `{{ENUM}}` | Array item | `{{NORMALIZE}}` | `{{RULES}}` | `{{CLASS}}` | `{{DESCRIPTION}}` | `{{EXAMPLE}}` | `{{ERROR_CODES}}` |

### 3.2. Object schema / type declaration

```ts
// Documentation-only pseudo TypeScript. Replace with actual DTO/schema reference.
interface {{REQUEST_DTO_NAME}} {
  {{fieldName}}: {{Type}};
  {{optionalFieldName}}?: {{Type}} | null;
  {{nestedObject}}?: {
    {{nestedField}}: {{Type}};
  };
  {{items}}?: Array<{
    {{itemField}}: {{Type}};
  }>;
}
```

### 3.3. Required / null / empty semantic matrix

| Input state | Is key present? | Is valid? | Meaning | Server behavior | Typical error |
|---|---:|---:|---|---|---|
| Field missing | No | `{{Y/N}}` | Client không gửi field. | `{{DEFAULT_OR_REJECT}}` | `{{ERROR_CODE}}` |
| `null` | Yes | `{{Y/N}}` | Chủ đích xóa/không có giá trị. | `{{ALLOW_CLEAR_OR_REJECT}}` | `{{ERROR_CODE}}` |
| Empty string `""` | Yes | `{{Y/N}}` | Không có text. | `{{TRIM_THEN_REJECT_OR_ALLOW}}` | `{{ERROR_CODE}}` |
| Whitespace string | Yes | `{{Y/N}}` | Input có khoảng trắng. | `{{NORMALIZATION}}` | `{{ERROR_CODE}}` |
| Empty array `[]` | Yes | `{{Y/N}}` | Không có phần tử. | `{{ALLOW_OR_REJECT}}` | `{{ERROR_CODE}}` |
| Empty object `{}` | Yes | `{{Y/N}}` | Object không có property. | `{{ALLOW_OR_REJECT}}` | `{{ERROR_CODE}}` |
| Unknown field | Yes | `No` by default | Client gửi key không được contract. | Reject hoặc ignore phải được chốt. | `{{ERROR_CODE_OR_IGNORE_POLICY}}` |

## 4. Validation and normalization

### 4.1. Validation sequence

| Order | Validation type | Rule ID | Field(s) | Rule / expected condition | Layer | Failure code | Notes |
|---:|---|---|---|---|---|---|---|
| 1 | Transport | `REQ-TRN-001` | Header/body | Content-Type, max size, JSON parse hợp lệ. | Gateway / controller | `{{ERROR_CODE}}` | Không vào business service nếu fail. |
| 2 | Schema | `REQ-VAL-001` | `{{FIELD}}` | Required/type/min/max/pattern/enum. | DTO / validation pipe | `{{ERROR_CODE}}` | Gộp field errors theo policy. |
| 3 | Canonicalization | `REQ-NRM-001` | `{{FIELD}}` | trim/lowercase/timezone/Unicode normalization/sanitize. | Mapper | `{{ERROR_CODE_OR_NA}}` | Nêu input và output sau transform. |
| 4 | Cross-field | `REQ-XFD-001` | `{{FIELD_A}}, {{FIELD_B}}` | `{{RELATIONSHIP_RULE}}` | Application service | `{{ERROR_CODE}}` | Ví dụ startAt < endAt. |
| 5 | Domain / business | `BR-{{NNN}}` | `{{FIELD_OR_STATE}}` | `{{BUSINESS_RULE}}` | Domain service / aggregate | `{{ERROR_CODE}}` | Không trộn với schema validation. |
| 6 | Authorization-bound | `AUTHZ-{{NNN}}` | JWT/path/body | Actor có quyền và ownership relation. | Guard/policy | `{{ERROR_CODE}}` | Không leak resource existence. |
| 7 | Persistence constraint | `DB-{{NNN}}` | `{{FIELD}}` | Unique/FK/check/version constraint. | Repository/DB | `{{ERROR_CODE}}` | Map deterministic DB conflict sang business error. |

### 4.2. Normalization map

| Field | Raw source | Transform | Output variable | Reason | Idempotent? | Log raw value? |
|---|---|---|---|---|---|---|
| `{{fieldName}}` | `request.body.{{fieldName}}` | `trim / lowercase / parse ISO date / sanitize` | `normalized{{FieldName}}` | `{{REASON}}` | `Y/N` | `Never / Masked / Yes` |

## 5. Request examples

### 5.1. Valid request

```http
{{HTTP_METHOD}} /api/v{{API_VERSION}}/{{RESOURCE_PATH}} HTTP/1.1
Authorization: Bearer {{REDACTED_ACCESS_TOKEN}}
Content-Type: application/json; charset=utf-8
Accept: application/json
X-Request-Id: {{UUID}}
Idempotency-Key: {{UUID_IF_APPLICABLE}}

{
  "{{fieldName}}": "{{value}}",
  "{{optionalFieldName}}": null,
  "{{nestedObject}}": {
    "{{nestedField}}": "{{value}}"
  },
  "{{items}}": [
    {
      "{{itemField}}": "{{value}}"
    }
  ]
}
```

### 5.2. Representative invalid request

```json
{
  "{{fieldWithInvalidValue}}": "{{INVALID_VALUE}}"
}
```

**Expected validation result:** `{{HTTP_STATUS}} {{BUSINESS_CODE}}`, field `{{FIELD}}`, rule `{{RULE_ID}}`.

## 6. Idempotency, concurrency and replay protection

| Topic | Decision | Implementation / check | Error / response behavior |
|---|---|---|---|
| Idempotency key | `Required / Not applicable` | `{{STORE_KEY_SCOPE_TTL_REQUEST_HASH}}` | `{{RETURN_SAME_RESPONSE_OR_CONFLICT}}` |
| Duplicate submission | `{{POLICY}}` | Unique constraint / status check / dedupe key. | `{{ERROR_CODE}}` |
| Optimistic concurrency | `{{VERSION_ETAG_POLICY}}` | `{{FIELD_OR_HEADER}}` | `409/412 {{ERROR_CODE}}` |
| Retry-safe? | `Yes / No / Conditional` | `{{WHY}}` | Client retry rule. |
| Replay/nonce | `{{POLICY}}` | Timestamp/nonce/OTP token validation. | `{{ERROR_CODE}}` |

## 7. Request security and privacy

| Concern | Rule |
|---|---|
| Credential/token | `{{CREDENTIAL_POLICY}}` |
| PII validation | `{{PII_POLICY}}` |
| HTML/file input | `{{SANITIZATION_OR_SCAN_POLICY}}` |
| Injection prevention | Use typed parameters/ORM/query builder; never build SQL from raw input. |
| Mass assignment | Whitelist DTO properties; map input explicitly to command. |
| Log masking | `{{MASKED_FIELD_LIST}}` |
| Authorization data source | JWT claims must not be overridden by body/path input without explicit policy. |

## 8. FE / Mobile / Backend integration notes

| Consumer | Requirement | Owner | Notes |
|---|---|---|---|
| `web-student` | `{{INTEGRATION_NOTE}}` | FE | `{{NOTES}}` |
| `mobile-app` | `{{INTEGRATION_NOTE}}` | Mobile | `{{NOTES}}` |
| Backend | `{{DTO_VALIDATION_OR_MAPPING_NOTE}}` | BE | `{{NOTES}}` |
| QA | `{{TEST_DATA_OR_BOUNDARY_NOTE}}` | QA | `{{NOTES}}` |

## 9. Request review checklist

- [ ] All path/query/header/body/file inputs are documented.
- [ ] Nested fields and array item fields are explicitly described.
- [ ] Required, nullable, empty/default/unknown semantic is unambiguous.
- [ ] Validation order separates transport, schema, business, permission and database constraint.
- [ ] Examples match the exact field name/type/format in the dictionary.
- [ ] Sensitive fields are masked and never logged raw.
- [ ] Idempotency/concurrency policy is decided for side-effect API.

# {{SCREEN_ID}} — API Integration

> API phải được đối chiếu với OpenAPI, code backend hoặc API catalog. Nếu chưa có, đánh dấu `CẦN_XÁC_NHẬN`, tuyệt đối không coi ví dụ là contract thật.

## 1. API usage matrix
| API ID | Method | Path | Event | Auth |
|---|---|---|---|---|
| `{{SCREEN_ID}}-API-001` | {{METHOD}} | `{{API_PATH}}` | `{{SCREEN_ID}}-EV-001` | {{AUTH}} |

## 2. {{SCREEN_ID}}-API-001 — {{API_NAME}}
- Contract/source/version: {{CONTRACT_SOURCE}}
- Method/path: `{{METHOD}} {{API_PATH}}`
- Auth/permissions: {{AUTH_PERMISSIONS}}
- Headers: {{HEADERS}}
- Query/path params: {{PARAMS}}
- Request body (nếu có): {{REQUEST_BODY}}

**Response example — chưa xác nhận nếu thiếu nguồn:**
```json
{{RESPONSE_JSON}}
```

**Field mapping:** {{RESPONSE_MAPPING}}

**Error handling:**
| Status / loại lỗi | Ý nghĩa | UI/State hành động | Retry? |
|---|---|---|---|
| {{STATUS}} | {{MEANING}} | {{ACTION}} | {{RETRY}} |

**Timeout/retry/idempotency/cancel:** {{NETWORK_POLICY}}

## 3. API không sử dụng
- Ghi rõ xử lý local nếu screen không cần API; bỏ API giả.

## 4. References
[Events](02-events.md) · [Data flow](03-data-flow.md) · [Tests](07-test-cases.md)

# {{SCREEN_ID}} — Data Flow & State

## 1. Nguồn dữ liệu
| Field / object | Type | Source | Destination | Cập nhật khi |
|---|---|---|---|---|
| {{DATA_FIELD}} | {{TYPE}} | {{SOURCE}} | {{DESTINATION}} | `{{SCREEN_ID}}-EV-001` |

## 2. State model
```ts
interface ScreenState {
  // {{STATE_DEFINITION}}
}
```

## 3. API DTO → ViewModel mapping
| API field | Transformation | UI state / element |
|---|---|---|
| {{API_FIELD}} | {{TRANSFORM}} | `{{SCREEN_ID}}-EL-001` |

## 4. Luồng đọc (Read)
1. {{READ_STEP_1}}
2. {{READ_STEP_2}}
3. {{READ_STEP_3}}

## 5. Luồng ghi (Write)
1. {{WRITE_STEP_1}}
2. {{WRITE_STEP_2}}
3. {{WRITE_STEP_3}}

## 6. Cache / concurrency / lifecycle
- Cache và invalidation: {{CACHE_RULE}}
- Stale response/race: {{RACE_POLICY}}
- Cleanup/unmount: {{CLEANUP}}
- Derived values, pagination, query params: {{DERIVED_RULE}}

## 7. Data errors & security
- Invalid/missing data: {{INVALID_DATA_POLICY}}
- Sensitive data: {{SECURITY_POLICY}}

## 8. Trace
[Events](02-events.md) · [API](04-api-integration.md) · [Rules](05-business-rules.md)

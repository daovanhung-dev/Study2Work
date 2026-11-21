# {{SCREEN_ID}} — Navigation

## 1. Route definition
- Current route: `{{ROUTE}}`
- Route params/types: {{ROUTE_PARAMS}}
- Query params/defaults: {{QUERY_PARAMS}}
- Route guards: {{ROUTE_GUARD}}

## 2. Điểm vào
| From screen/route | Trigger | Params | Guard / fallback |
|---|---|---|---|
| {{FROM_SCREEN}} | {{ENTER_TRIGGER}} | {{ENTER_PARAMS}} | {{ENTER_FALLBACK}} |

## 3. Điểm ra
| Destination | Trigger | Params | Điều kiện |
|---|---|---|---|
| {{TO_SCREEN}} | `{{SCREEN_ID}}-EV-001` | {{EXIT_PARAMS}} | {{EXIT_GUARD}} |

## 4. Back / refresh / deep link
- Back behavior: {{BACK_RULE}}
- Preserve filters/scroll/form state: {{PRESERVE_RULE}}
- Refresh/direct URL: {{DEEPLINK_RULE}}
- Invalid or missing ID: {{INVALID_ROUTE}}
- Not authenticated/authorized: {{AUTH_FALLBACK}}

## 5. Diagram
```mermaid
flowchart LR
  A[{{FROM_SCREEN}}] --> B[{{SCREEN_ID}}]
  B --> C[{{TO_SCREEN}}]
```

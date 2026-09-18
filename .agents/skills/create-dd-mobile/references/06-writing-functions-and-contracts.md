# 06 — Viết Function_List.md và Contract

Function là một trách nhiệm có thể implement/test độc lập: handler, controller,
use case, service, repository, datasource, API adapter, background job hoặc
event handler.

## Hợp đồng bắt buộc

- Purpose và boundary: làm gì, không làm gì.
- Parent feature và trigger.
- Layer và intended file.
- Input: field, type, required, source, validation, sensitivity.
- Output: success, validation, permission, not-found, conflict, system error.
- Preconditions, invariants, postconditions.
- Processing steps và pseudocode khi có algorithm.
- Applied business rules.
- Data operations, transaction boundary, idempotency và concurrency.
- Permission/security/data isolation.
- Side effects: audit, event, notification, cache, analytics.
- Dependency failure: timeout, retry, fallback, compensation.
- Minimum test cases.

## Dependency direction

```text
Presentation → Provider/Controller → Use case/Service
→ Repository → Datasource/DAO/API client
```

UI không gọi DAO/API trực tiếp; domain/use case không phụ thuộc widget, HTTP
client hoặc ORM cụ thể; repository không phụ thuộc UI.

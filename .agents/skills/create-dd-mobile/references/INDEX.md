# DD Skill Reference Index

Đây là router bắt buộc của package. Không viết DD theo cách đọc ngẫu nhiên.

## Luồng bắt buộc

```text
BD/BRD
  → phân tích evidence và conflict
  → scope / actor / data / state / rule
  → identifier và traceability
  → Overall
  → Features
  → Functions / contracts
  → Views / UI states
  → Import / file / dependency map
  → diagrams / assets / history
  → review gates
  → validator
  → worklog và project validation
```

## Bảng định tuyến

| Bước | Tài liệu | Khi đọc |
|---:|---|---|
| 0 | [00-read-first-and-routing](00-read-first-and-routing.md) | Mọi DD mới hoặc DD update |
| 1 | [01-input-analysis-and-evidence](01-input-analysis-and-evidence.md) | Sau khi xác định BD/BRD |
| 2 | [02-module-scope-actors-data-states](02-module-scope-actors-data-states.md) | Trước khi tạo feature |
| 3 | [03-identifiers-and-traceability](03-identifiers-and-traceability.md) | Trước khi viết ID hoặc bảng mapping |
| 4 | [04-writing-overall](04-writing-overall.md) | Khi viết nguồn sự thật cấp module |
| 5 | [05-writing-features](05-writing-features.md) | Khi tách capability thành feature |
| 6 | [06-writing-functions-and-contracts](06-writing-functions-and-contracts.md) | Khi chuyển feature thành use case/API/data operation |
| 7 | [07-writing-views-and-ui-states](07-writing-views-and-ui-states.md) | Khi module có UI hoặc trạng thái người dùng nhìn thấy |
| 8 | [08-writing-imports-diagrams-assets](08-writing-imports-diagrams-assets.md) | Trước khi chốt file/dependency và sơ đồ |
| 9 | [09-review-gates-and-status](09-review-gates-and-status.md) | Trước BA/PO/Tech Lead/QA review |
| 10 | [10-change-control-worklog](10-change-control-worklog.md) | Khi DD được tạo, sửa hoặc thay đổi quyết định |
| 11 | [11-nanobio-source-truth-and-constraints](11-nanobio-source-truth-and-constraints.md) | Khi DD chạm runtime, access, Supabase, AI, privacy hoặc FamilyPlus |
| 12 | [12-agent-runbook](12-agent-runbook.md) | Khi Codex/agent thực hiện workflow |

## Tài liệu hỗ trợ

- [Template DD](../template/)
- [10 DD examples](../examples/README.md)
- [Preflight checklist](../checklists/preflight.md)
- [Authoring checklist](../checklists/authoring.md)
- [Review checklist](../checklists/review.md)
- [Definition of Ready/Done](../checklists/definition-of-ready-done.md)
- [Static validator](../scripts/validate_dd_pack.py)

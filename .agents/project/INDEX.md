# Project context index

Đây là context dùng khi task đi qua nhiều app, boundary deployable hoặc shared
contract. Task cục bộ phải đi từ root router tới scope entry trước; không đọc
toàn bộ project context nếu không có dependency thật.

## Load order

```text
AGENTS.md
→ .agents/AGENTS.md
→ .agents/context-map.md
→ project/INDEX.md
→ đúng scope AGENTS.md
→ exact source/API/module/core/service/test page
```

## Pages

| Chủ đề | Page |
|---|---|
| Ownership và boundary | `architecture.md` |
| Cross-scope dependencies | `dependencies.md` |
| Database source/status | `database.md` |
| Business code/HTTP mapping | `business-code.md` |
| Repository conventions/workflow | `conventions.md` |
| Design system | `design.md` |
| Snapshot/status/discrepancy | `source-status.md` |
| Shared/local contracts | `contracts.md` |
| Workflow routing | `workflows.md` |

## Mandatory task artifacts

- Context map: `../context-map.md` (human-readable load and relationship graph).
- Skill registry: `../skills/INDEX.md`.
- Worklog contract: `../worklog/README.md` and `../worklog/TEMPLATE.md`.
- Expected/current behavior must remain separate; conflicts are recorded as
  `DISCREPANCY` rather than silently resolved.

`source-status.md` là nơi ghi discrepancy cấp repository; scope page vẫn phải
được ưu tiên cho chi tiết runtime của scope đó.

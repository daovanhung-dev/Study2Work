# Project context index

Đây là context dùng khi task đi qua nhiều app, boundary deployable hoặc shared
contract. Task cục bộ phải đi từ root router tới scope entry trước; không đọc
toàn bộ project context nếu không có dependency thật.

## Load order

```text
AGENTS.md
→ .agents/AGENTS.md
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

`source-status.md` là nơi ghi discrepancy cấp repository; scope page vẫn phải
được ưu tiên cho chi tiết runtime của scope đó.

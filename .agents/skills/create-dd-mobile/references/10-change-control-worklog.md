# 10 — Change Control và Worklog

Khi requirement thay đổi, cập nhật theo thứ tự:

```text
BD/Requirement → Overall → Features → Functions
→ Views → Import/File → diagrams/assets → tests/source/worklog
```

Mỗi thay đổi phải ghi:

- Version và ngày.
- Source/decision mới.
- ID bị ảnh hưởng.
- API/entity/schema/migration impact.
- Test/regression impact.
- Open question hoặc decision đã đóng.

Với phiên tạo/cập nhật DD, tạo worklog tại `.agents/worklog/<yyyy-mm-dd>/`, ghi
changed files, commands, risks, completion và self-review. Sau worklog phải chạy
`.codex/tools/update_worklog_learning.ps1` để refresh project memory.

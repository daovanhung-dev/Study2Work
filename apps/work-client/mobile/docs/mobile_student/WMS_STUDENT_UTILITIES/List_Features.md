# Feature list — WMS_STUDENT_UTILITIES

## WMS_STUDENT_UTILITIES-F01 — Tiện ích sinh viên

**Mô tả:** Các utility view interview, support, course và news hiện có.

| Trường | Giá trị |
|---|---|
| Actor | Sinh viên |
| Trigger | Route entry hoặc user action trong current composition |
| Preconditions | App khởi động; local/remote dependency phù hợp với view |
| Postconditions | UI current result/error/empty state |
| Rule | WMS_STUDENT_UTILITIES-BR01 |
| Implementation | Source-only |

### Acceptance criteria

- [ ] Tất cả view của pack được inventory đúng path/status.
- [ ] Active view chỉ claim behavior có route/import evidence.
- [ ] Legacy, placeholder, UI-only và unwired giữ đúng status.
- [ ] Function/view/test IDs trace được hai chiều.
- [ ] Open questions không bị chuyển thành approved rule.

| Feature | Function | View | Rule | Test |
|---|---|---|---|---|
| WMS_STUDENT_UTILITIES-F01 | WMS_STUDENT_UTILITIES-FN01..FN04 | WMS_STUDENT_UTILITIES-V01..V04 | WMS_STUDENT_UTILITIES-BR01 | WMS_STUDENT_UTILITIES-TC01..TC04 |


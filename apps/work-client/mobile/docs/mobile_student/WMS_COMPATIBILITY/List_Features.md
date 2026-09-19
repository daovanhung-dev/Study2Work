# Feature list — WMS_COMPATIBILITY

## WMS_COMPATIBILITY-F01 — Màn hình compatibility chưa wired

**Mô tả:** Inventory các view tồn tại nhưng chưa có active caller evidence trong student route graph.

| Trường | Giá trị |
|---|---|
| Actor | Sinh viên |
| Trigger | Route entry hoặc user action trong current composition |
| Preconditions | App khởi động; local/remote dependency phù hợp với view |
| Postconditions | UI current result/error/empty state |
| Rule | WMS_COMPATIBILITY-BR01 |
| Implementation | Source-only |

### Acceptance criteria

- [ ] Tất cả view của pack được inventory đúng path/status.
- [ ] Active view chỉ claim behavior có route/import evidence.
- [ ] Legacy, placeholder, UI-only và unwired giữ đúng status.
- [ ] Function/view/test IDs trace được hai chiều.
- [ ] Open questions không bị chuyển thành approved rule.

| Feature | Function | View | Rule | Test |
|---|---|---|---|---|
| WMS_COMPATIBILITY-F01 | WMS_COMPATIBILITY-FN01..FN01 | WMS_COMPATIBILITY-V01..V01 | WMS_COMPATIBILITY-BR01 | WMS_COMPATIBILITY-TC01..TC01 |


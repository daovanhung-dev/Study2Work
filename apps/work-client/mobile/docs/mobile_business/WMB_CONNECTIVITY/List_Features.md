# Feature list — WMB_CONNECTIVITY

## WMB_CONNECTIVITY-F01 — Kiểm tra kết nối

**Mô tả:** Hiển thị connectivity và cho phép retry/exit về login.

| Trường | Giá trị |
|---|---|
| Actor | Doanh nghiệp |
| Trigger | Route entry hoặc user action trong current composition |
| Preconditions | App khởi động; local/remote dependency phù hợp với view |
| Postconditions | UI current result/error/empty state |
| Rule | WMB_CONNECTIVITY-BR01 |
| Implementation | Source-only |

### Acceptance criteria

- [ ] Tất cả view của pack được inventory đúng path/status.
- [ ] Active view chỉ claim behavior có route/import evidence.
- [ ] Legacy, placeholder, UI-only và unwired giữ đúng status.
- [ ] Function/view/test IDs trace được hai chiều.
- [ ] Open questions không bị chuyển thành approved rule.

| Feature | Function | View | Rule | Test |
|---|---|---|---|---|
| WMB_CONNECTIVITY-F01 | WMB_CONNECTIVITY-FN01..FN01 | WMB_CONNECTIVITY-V01..V01 | WMB_CONNECTIVITY-BR01 | WMB_CONNECTIVITY-TC01..TC01 |


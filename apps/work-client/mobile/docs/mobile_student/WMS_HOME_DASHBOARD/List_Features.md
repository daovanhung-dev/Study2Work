# Feature list — WMS_HOME_DASHBOARD

## WMS_HOME_DASHBOARD-F01 — Trang chủ và thông tin sinh viên

**Mô tả:** Student home, thông báo, profile/detail presentation và route tới utilities.

| Trường | Giá trị |
|---|---|
| Actor | Sinh viên |
| Trigger | Route entry hoặc user action trong current composition |
| Preconditions | App khởi động; local/remote dependency phù hợp với view |
| Postconditions | UI current result/error/empty state |
| Rule | WMS_HOME_DASHBOARD-BR01 |
| Implementation | Partial |

### Acceptance criteria

- [ ] Tất cả view của pack được inventory đúng path/status.
- [ ] Active view chỉ claim behavior có route/import evidence.
- [ ] Legacy, placeholder, UI-only và unwired giữ đúng status.
- [ ] Function/view/test IDs trace được hai chiều.
- [ ] Open questions không bị chuyển thành approved rule.

| Feature | Function | View | Rule | Test |
|---|---|---|---|---|
| WMS_HOME_DASHBOARD-F01 | WMS_HOME_DASHBOARD-FN01..FN04 | WMS_HOME_DASHBOARD-V01..V04 | WMS_HOME_DASHBOARD-BR01 | WMS_HOME_DASHBOARD-TC01..TC04 |

# Feature list — WMB_HOME_DASHBOARD

## WMB_HOME_DASHBOARD-F01 — Trang chủ và thông tin doanh nghiệp

**Mô tả:** Dashboard doanh nghiệp, thông báo và các màn hình thông tin/detail.

| Trường | Giá trị |
|---|---|
| Actor | Doanh nghiệp |
| Trigger | Route entry hoặc user action trong current composition |
| Preconditions | App khởi động; local/remote dependency phù hợp với view |
| Postconditions | UI current result/error/empty state |
| Rule | WMB_HOME_DASHBOARD-BR01 |
| Implementation | Partial |

### Acceptance criteria

- [ ] Tất cả view của pack được inventory đúng path/status.
- [ ] Active view chỉ claim behavior có route/import evidence.
- [ ] Legacy, placeholder, UI-only và unwired giữ đúng status.
- [ ] Function/view/test IDs trace được hai chiều.
- [ ] Open questions không bị chuyển thành approved rule.

| Feature | Function | View | Rule | Test |
|---|---|---|---|---|
| WMB_HOME_DASHBOARD-F01 | WMB_HOME_DASHBOARD-FN01..FN05 | WMB_HOME_DASHBOARD-V01..V05 | WMB_HOME_DASHBOARD-BR01 | WMB_HOME_DASHBOARD-TC01..TC05 |


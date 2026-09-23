# Feature list — WMB_REPORTING

## WMB_REPORTING-F01 — Thống kê và báo cáo

**Mô tả:** Hiển thị báo cáo/thống kê doanh nghiệp bằng local presentation data.

| Trường | Giá trị |
|---|---|
| Actor | Doanh nghiệp |
| Trigger | Route entry hoặc user action trong current composition |
| Preconditions | App khởi động; local/remote dependency phù hợp với view |
| Postconditions | UI current result/error/empty state |
| Rule | WMB_REPORTING-BR01 |
| Implementation | Partial |

### Acceptance criteria

- [ ] Tất cả view của pack được inventory đúng path/status.
- [ ] Active view chỉ claim behavior có route/import evidence.
- [ ] Legacy, placeholder, UI-only và unwired giữ đúng status.
- [ ] Function/view/test IDs trace được hai chiều.
- [ ] Open questions không bị chuyển thành approved rule.

| Feature | Function | View | Rule | Test |
|---|---|---|---|---|
| WMB_REPORTING-F01 | WMB_REPORTING-FN01..FN02 | WMB_REPORTING-V01..V02 | WMB_REPORTING-BR01 | WMB_REPORTING-TC01..TC02 |


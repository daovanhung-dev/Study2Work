# Feature list — WMB_JOB_MANAGEMENT

## WMB_JOB_MANAGEMENT-F01 — Đăng và quản lý tin tuyển dụng

**Mô tả:** Tạo, liệt kê và xem chi tiết JD thuộc doanh nghiệp hiện tại.

| Trường | Giá trị |
|---|---|
| Actor | Doanh nghiệp |
| Trigger | Route entry hoặc user action trong current composition |
| Preconditions | App khởi động; local/remote dependency phù hợp với view |
| Postconditions | UI current result/error/empty state |
| Rule | WMB_JOB_MANAGEMENT-BR01 |
| Implementation | Implemented |

### Acceptance criteria

- [ ] Tất cả view của pack được inventory đúng path/status.
- [ ] Active view chỉ claim behavior có route/import evidence.
- [ ] Legacy, placeholder, UI-only và unwired giữ đúng status.
- [ ] Function/view/test IDs trace được hai chiều.
- [ ] Open questions không bị chuyển thành approved rule.

| Feature | Function | View | Rule | Test |
|---|---|---|---|---|
| WMB_JOB_MANAGEMENT-F01 | WMB_JOB_MANAGEMENT-FN01..FN03 | WMB_JOB_MANAGEMENT-V01..V03 | WMB_JOB_MANAGEMENT-BR01 | WMB_JOB_MANAGEMENT-TC01..TC03 |


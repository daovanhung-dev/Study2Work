# Feature list — WMS_CV_MANAGEMENT

## WMS_CV_MANAGEMENT-F01 — Quản lý CV sinh viên

**Mô tả:** Tải, hiển thị và cập nhật CV của sinh viên hiện tại.

| Trường | Giá trị |
|---|---|
| Actor | Sinh viên |
| Trigger | Route entry hoặc user action trong current composition |
| Preconditions | App khởi động; local/remote dependency phù hợp với view |
| Postconditions | UI current result/error/empty state |
| Rule | WMS_CV_MANAGEMENT-BR01 |
| Implementation | Implemented |

### Acceptance criteria

- [ ] Tất cả view của pack được inventory đúng path/status.
- [ ] Active view chỉ claim behavior có route/import evidence.
- [ ] Legacy, placeholder, UI-only và unwired giữ đúng status.
- [ ] Function/view/test IDs trace được hai chiều.
- [ ] Open questions không bị chuyển thành approved rule.

| Feature | Function | View | Rule | Test |
|---|---|---|---|---|
| WMS_CV_MANAGEMENT-F01 | WMS_CV_MANAGEMENT-FN01..FN01 | WMS_CV_MANAGEMENT-V01..V01 | WMS_CV_MANAGEMENT-BR01 | WMS_CV_MANAGEMENT-TC01..TC01 |


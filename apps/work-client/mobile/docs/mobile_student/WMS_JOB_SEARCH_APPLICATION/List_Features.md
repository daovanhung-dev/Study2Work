# Feature list — WMS_JOB_SEARCH_APPLICATION

## WMS_JOB_SEARCH_APPLICATION-F01 — Tìm việc và ứng tuyển

**Mô tả:** Tải JD, lọc local, xem chi tiết và gửi application.

| Trường | Giá trị |
|---|---|
| Actor | Sinh viên |
| Trigger | Route entry hoặc user action trong current composition |
| Preconditions | App khởi động; local/remote dependency phù hợp với view |
| Postconditions | UI current result/error/empty state |
| Rule | WMS_JOB_SEARCH_APPLICATION-BR01 |
| Implementation | Partial |

### Acceptance criteria

- [ ] Tất cả view của pack được inventory đúng path/status.
- [ ] Active view chỉ claim behavior có route/import evidence.
- [ ] Legacy, placeholder, UI-only và unwired giữ đúng status.
- [ ] Function/view/test IDs trace được hai chiều.
- [ ] Open questions không bị chuyển thành approved rule.

| Feature | Function | View | Rule | Test |
|---|---|---|---|---|
| WMS_JOB_SEARCH_APPLICATION-F01 | WMS_JOB_SEARCH_APPLICATION-FN01..FN03 | WMS_JOB_SEARCH_APPLICATION-V01..V03 | WMS_JOB_SEARCH_APPLICATION-BR01 | WMS_JOB_SEARCH_APPLICATION-TC01..TC03 |


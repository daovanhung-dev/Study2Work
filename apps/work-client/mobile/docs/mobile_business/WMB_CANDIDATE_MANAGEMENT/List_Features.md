# Feature list — WMB_CANDIDATE_MANAGEMENT

## WMB_CANDIDATE_MANAGEMENT-F01 — Ứng viên và lọc CV

**Mô tả:** Tìm kiếm, xem và thao tác với ứng viên/CV trong phạm vi doanh nghiệp.

| Trường | Giá trị |
|---|---|
| Actor | Doanh nghiệp |
| Trigger | Route entry hoặc user action trong current composition |
| Preconditions | App khởi động; local/remote dependency phù hợp với view |
| Postconditions | UI current result/error/empty state |
| Rule | WMB_CANDIDATE_MANAGEMENT-BR01 |
| Implementation | Partial |

### Acceptance criteria

- [ ] Tất cả view của pack được inventory đúng path/status.
- [ ] Active view chỉ claim behavior có route/import evidence.
- [ ] Legacy, placeholder, UI-only và unwired giữ đúng status.
- [ ] Function/view/test IDs trace được hai chiều.
- [ ] Open questions không bị chuyển thành approved rule.

| Feature | Function | View | Rule | Test |
|---|---|---|---|---|
| WMB_CANDIDATE_MANAGEMENT-F01 | WMB_CANDIDATE_MANAGEMENT-FN01..FN04 | WMB_CANDIDATE_MANAGEMENT-V01..V04 | WMB_CANDIDATE_MANAGEMENT-BR01 | WMB_CANDIDATE_MANAGEMENT-TC01..TC04 |


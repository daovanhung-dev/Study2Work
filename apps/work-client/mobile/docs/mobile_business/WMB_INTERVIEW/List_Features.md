# Feature list — WMB_INTERVIEW

## WMB_INTERVIEW-F01 — Lịch phỏng vấn

**Mô tả:** Hiển thị và thao tác local interview schedule/form.

| Trường | Giá trị |
|---|---|
| Actor | Doanh nghiệp |
| Trigger | Route entry hoặc user action trong current composition |
| Preconditions | App khởi động; local/remote dependency phù hợp với view |
| Postconditions | UI current result/error/empty state |
| Rule | WMB_INTERVIEW-BR01 |
| Implementation | Partial |

### Acceptance criteria

- [ ] Tất cả view của pack được inventory đúng path/status.
- [ ] Active view chỉ claim behavior có route/import evidence.
- [ ] Legacy, placeholder, UI-only và unwired giữ đúng status.
- [ ] Function/view/test IDs trace được hai chiều.
- [ ] Open questions không bị chuyển thành approved rule.

| Feature | Function | View | Rule | Test |
|---|---|---|---|---|
| WMB_INTERVIEW-F01 | WMB_INTERVIEW-FN01..FN02 | WMB_INTERVIEW-V01..V02 | WMB_INTERVIEW-BR01 | WMB_INTERVIEW-TC01..TC02 |


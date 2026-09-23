# Feature list — WMB_INTERNSHIP

## WMB_INTERNSHIP-F01 — Chương trình thực tập

**Mô tả:** Hiển thị listing/form chương trình thực tập hiện có.

| Trường | Giá trị |
|---|---|
| Actor | Doanh nghiệp |
| Trigger | Route entry hoặc user action trong current composition |
| Preconditions | App khởi động; local/remote dependency phù hợp với view |
| Postconditions | UI current result/error/empty state |
| Rule | WMB_INTERNSHIP-BR01 |
| Implementation | Partial |

### Acceptance criteria

- [ ] Tất cả view của pack được inventory đúng path/status.
- [ ] Active view chỉ claim behavior có route/import evidence.
- [ ] Legacy, placeholder, UI-only và unwired giữ đúng status.
- [ ] Function/view/test IDs trace được hai chiều.
- [ ] Open questions không bị chuyển thành approved rule.

| Feature | Function | View | Rule | Test |
|---|---|---|---|---|
| WMB_INTERNSHIP-F01 | WMB_INTERNSHIP-FN01..FN02 | WMB_INTERNSHIP-V01..V02 | WMB_INTERNSHIP-BR01 | WMB_INTERNSHIP-TC01..TC02 |

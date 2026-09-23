# Feature list — WMB_SCHOOL_LINK

## WMB_SCHOOL_LINK-F01 — Liên kết nhà trường

**Mô tả:** Cung cấp UI shell cho liên kết doanh nghiệp - nhà trường.

| Trường | Giá trị |
|---|---|
| Actor | Doanh nghiệp |
| Trigger | Route entry hoặc user action trong current composition |
| Preconditions | App khởi động; local/remote dependency phù hợp với view |
| Postconditions | UI current result/error/empty state |
| Rule | WMB_SCHOOL_LINK-BR01 |
| Implementation | Source-only |

### Acceptance criteria

- [ ] Tất cả view của pack được inventory đúng path/status.
- [ ] Active view chỉ claim behavior có route/import evidence.
- [ ] Legacy, placeholder, UI-only và unwired giữ đúng status.
- [ ] Function/view/test IDs trace được hai chiều.
- [ ] Open questions không bị chuyển thành approved rule.

| Feature | Function | View | Rule | Test |
|---|---|---|---|---|
| WMB_SCHOOL_LINK-F01 | WMB_SCHOOL_LINK-FN01..FN01 | WMB_SCHOOL_LINK-V01..V01 | WMB_SCHOOL_LINK-BR01 | WMB_SCHOOL_LINK-TC01..TC01 |


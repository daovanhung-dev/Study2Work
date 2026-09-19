# Feature list — WMB_AUTH_SESSION

## WMB_AUTH_SESSION-F01 — Xác thực và phiên doanh nghiệp

**Mô tả:** Đăng nhập doanh nghiệp, dựng shell điều hướng và kết thúc phiên cục bộ.

| Trường | Giá trị |
|---|---|
| Actor | Doanh nghiệp |
| Trigger | Route entry hoặc user action trong current composition |
| Preconditions | App khởi động; local/remote dependency phù hợp với view |
| Postconditions | UI current result/error/empty state |
| Rule | WMB_AUTH_SESSION-BR01 |
| Implementation | Partial |

### Acceptance criteria

- [ ] Tất cả view của pack được inventory đúng path/status.
- [ ] Active view chỉ claim behavior có route/import evidence.
- [ ] Legacy, placeholder, UI-only và unwired giữ đúng status.
- [ ] Function/view/test IDs trace được hai chiều.
- [ ] Open questions không bị chuyển thành approved rule.

| Feature | Function | View | Rule | Test |
|---|---|---|---|---|
| WMB_AUTH_SESSION-F01 | WMB_AUTH_SESSION-FN01..FN04 | WMB_AUTH_SESSION-V01..V04 | WMB_AUTH_SESSION-BR01 | WMB_AUTH_SESSION-TC01..TC04 |


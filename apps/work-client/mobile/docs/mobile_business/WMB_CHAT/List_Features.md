# Feature list — WMB_CHAT

## WMB_CHAT-F01 — Trò chuyện doanh nghiệp - sinh viên

**Mô tả:** Liệt kê partner, đọc/gửi message và polling message mới.

| Trường | Giá trị |
|---|---|
| Actor | Doanh nghiệp |
| Trigger | Route entry hoặc user action trong current composition |
| Preconditions | App khởi động; local/remote dependency phù hợp với view |
| Postconditions | UI current result/error/empty state |
| Rule | WMB_CHAT-BR01 |
| Implementation | Implemented |

### Acceptance criteria

- [ ] Tất cả view của pack được inventory đúng path/status.
- [ ] Active view chỉ claim behavior có route/import evidence.
- [ ] Legacy, placeholder, UI-only và unwired giữ đúng status.
- [ ] Function/view/test IDs trace được hai chiều.
- [ ] Open questions không bị chuyển thành approved rule.

| Feature | Function | View | Rule | Test |
|---|---|---|---|---|
| WMB_CHAT-F01 | WMB_CHAT-FN01..FN02 | WMB_CHAT-V01..V02 | WMB_CHAT-BR01 | WMB_CHAT-TC01..TC02 |


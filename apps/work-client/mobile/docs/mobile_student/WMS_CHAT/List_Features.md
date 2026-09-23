# Feature list — WMS_CHAT

## WMS_CHAT-F01 — Trò chuyện sinh viên - doanh nghiệp

**Mô tả:** Liệt kê business partner, đọc/gửi message và polling message mới.

| Trường | Giá trị |
|---|---|
| Actor | Sinh viên |
| Trigger | Route entry hoặc user action trong current composition |
| Preconditions | App khởi động; local/remote dependency phù hợp với view |
| Postconditions | UI current result/error/empty state |
| Rule | WMS_CHAT-BR01 |
| Implementation | Implemented |

### Acceptance criteria

- [ ] Tất cả view của pack được inventory đúng path/status.
- [ ] Active view chỉ claim behavior có route/import evidence.
- [ ] Legacy, placeholder, UI-only và unwired giữ đúng status.
- [ ] Function/view/test IDs trace được hai chiều.
- [ ] Open questions không bị chuyển thành approved rule.

| Feature | Function | View | Rule | Test |
|---|---|---|---|---|
| WMS_CHAT-F01 | WMS_CHAT-FN01..FN02 | WMS_CHAT-V01..V02 | WMS_CHAT-BR01 | WMS_CHAT-TC01..TC02 |


# SH-01 — Business Rules

> **Current approved implementation scope (2026-11-21):** Public guest access; independent read-only #05/#06; only PUBLISHED #06 items; no category query; search q is trimmed and routed to GS-02; public 401/403 stays a scoped error; categories are informational; course cards do not navigate; “Xem tất cả” targets GS-01 and registration targets SH-03; price is hidden until currency is defined. No email lead is collected and no screenshot-only claim is presented as factual. These choices define the 100% screen-score scope for this task; unresolved live API/DB/deployment status remains separate.

## 1. Rule index
| Rule ID (package alias) | Tên / source ID | Áp dụng | Thực thi | Tests |
|---|---|---|---|---|
| `SH-01-BR-001` | Source rules/gates bundle (alias only) | See source DD | Not re-inferred | See source acceptance |

## 2. Rules, security, discrepancy và gate từ source
- Inventory purpose: Giới thiệu giá trị học tập, tìm khóa học và CTA đăng nhập/đăng ký.
- Gate/status (giữ nguyên): **R**
- BR IDs trong file này chỉ là alias trỏ tới source rule/gate bundles; không thêm business rule. Không khẳng định rule FE/BE mới khi source chưa xác nhận.

### Trích từ DD nguồn: 8. Bảo mật và quyền riêng tư

- Hai endpoint là thao tác đọc công khai; không truy cập DB từ client, không có bí mật API phía client.
- Mô tả khóa học và rich text tương lai phải được hiển thị dưới dạng văn bản hoặc làm sạch an toàn theo hợp đồng client; trang này chưa có nội dung rich text được duyệt.
- Không thu thập/lưu email hiển thị trên ảnh mẫu.
- Chỉ dùng tham số q đã duyệt cho tìm kiếm; không thêm token, session ID hoặc dữ liệu người dùng khác vào URL.
- Chỉ trình bày khóa học PUBLISHED do #06 trả về. Không suy luận ghi danh, thanh toán, tình trạng ngoài phản hồi hoặc quyền sở hữu.
- Không tải khóa lưu trữ nội bộ hoặc URL phương tiện ngoài chưa được duyệt từ bản mẫu.

## 3. Quy tắc chưa xác nhận
- `CẦN_XÁC_NHẬN`: các quyết định/blocker trong inventory và DD nguồn chưa được giải quyết.
- Related IDs/source refs: Không có BR ID nguồn được chuẩn hóa.; xem [API](04-api-integration.md), [Events](02-events.md), [Tests](07-test-cases.md).

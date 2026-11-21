# SH-02 — Business Rules

| ID | Quy tắc | Nơi thực thi | Event / Test |
|---|---|---|---|
| `SH-02-BR-001` | Khóa học phải published mới public-read | Backend | EV-001 / TC-001, TC-007 |
| `SH-02-BR-002` | Đăng ký cần auth | FE UX + BE bắt buộc | EV-004 / TC-003 |
| `SH-02-BR-003` | Mỗi người chỉ có một đăng ký hợp lệ mỗi khóa | BE unique constraint + FE guard | EV-004 / TC-004/005 |
| `SH-02-BR-004` | Không tạo request POST đồng thời từ 1 CTA | FE + BE | EV-004 / TC-006 |
| `SH-02-BR-005` | courseId phải hợp lệ | FE validate + BE lookup | EV-001 / TC-002/007 |

## SH-02-BR-001 — Visibility
- BE chỉ trả detail khi course published; khóa private/unpublished trả 404 theo mô hình demo (không tiết lộ tồn tại).

## SH-02-BR-002 — Auth
- Anonymous không gửi POST; redirect login kèm `returnUrl=/courses/{courseId}`.
- BE POST bắt buộc token hợp lệ, server tự xác định userId từ token; không tin userId do client gửi.

## SH-02-BR-003 — Không trùng enrollment
- BE đảm bảo unique (userId, courseId) cho đăng ký active; POST trùng trả 409 `ALREADY_ENROLLED`.
- FE nhận 409 ALREADY_ENROLLED → cập nhật trạng thái đã đăng ký, không hiển thị lỗi đỏ.

## SH-02-BR-004 — Chống double-submit
- Trong `enrollStatus='submitting'`, disable CTA; BE vẫn xử lý an toàn khi client gửi lặp; không cam kết idempotency-key vì demo contract không hỗ trợ.

## SH-02-BR-005 — Path parameter
- `courseId` phải là nonempty URL decoded string, max 64 kí tự; ví dụ `crs-101`; invalid → 404 UI mà không gọi API.

> Các rule là giả định học thuật và cần được xác minh trên sản phẩm thật.

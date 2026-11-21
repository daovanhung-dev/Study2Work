# SH-01 — Business Rules

| ID | Rule | Nơi thực thi | Events | Tests |
|---|---|---|---|---|
| `SH-01-BR-001` | Chuẩn hóa từ khóa | FE; BE tự validate query | EV-002 | TC-002, TC-004 |
| `SH-01-BR-002` | Reset phân trang khi đổi bộ lọc | FE | EV-002, EV-003 | TC-002, TC-003 |
| `SH-01-BR-003` | Giới hạn giá trị page/topic | FE & BE | EV-003, EV-005 | TC-005 |
| `SH-01-BR-004` | Chỉ trả khóa học công khai | BE | EV-001, EV-002 | TC-001 |
| `SH-01-BR-005` | Response cũ không được ghi đè mới | FE | EV-002, EV-003, EV-005 | TC-006 |

## SH-01-BR-001 — Từ khóa
- Trim khoảng trắng hai đầu; giữ khoảng trắng giữa từ; maxlength 80 ký tự Unicode (theo ký tự hiển thị, tùy sản phẩm cần thống nhất grapheme); empty string tương đương không lọc.
- Không cắt thầm dữ liệu; input giới hạn 80 ký tự, nếu vượt thì không chấp nhận phần nhập thêm.

## SH-01-BR-002 — Reset trang
- Khi `searchKeyword` hoặc `topic` thay đổi, đặt `page=1` trước request mới; khi chuyển trang giữ nguyên query và topic.

## SH-01-BR-003 — Query hợp lệ
- `topic ∈ {all, programming, backend}`; `page` integer >=1; `pageSize=6` cố định trong demo.
- Không cho click các trang ngoài `[1,totalPages]`; backend cũng xác thực params, trả 422 nếu không hợp lệ.

## SH-01-BR-004 — Public visibility
- Backend chỉ đưa vào kết quả những khóa học `status=published`; UI không có quyền tự lọc dữ liệu bảo mật thay backend.

## SH-01-BR-005 — Tránh race condition
- Chỉ áp dụng response khi request key/token khớp lượt gần nhất; request bị thay thế có thể abort; lỗi của request cũ cũng không ghi đè UI của request mới.

**Phạm vi:** tất cả là giả định để minh họa DD, không khẳng định logic thực tế Study2Work.

# SH-01 — Test Cases

## 1. Test matrix
| Test ID | Loại | Input / precondition | Steps | Expected | Links |
|---|---|---|---|---|---|
| `SH-01-TC-001` | Happy path | API 200, 2 published courses | Load `/courses` | 2 cards, `2 khóa học`, không empty/error | EV-001, BR-004, API-001 |
| `SH-01-TC-002` | Search | Keyword `  Python  `, API 200 1 item | Gõ vào search, dừng >300ms | Request `keyword=Python`, page=1, 1 card | EV-002, BR-001/002 |
| `SH-01-TC-003` | Filter/Empty | topic=backend, API 200 `items=[]` | Chọn Backend → Reset | Empty UI; Reset về all+page=1 và request mới | EV-003/007, BR-002 |
| `SH-01-TC-004` | Boundary | 80 kí tự hợp lệ rồi thêm 1 kí tự | Nhập search | Chỉ nhận tối đa 80 kí tự, request không quá 80 | EV-002, BR-001 |
| `SH-01-TC-005` | Pagination | 14 items, 3 pages | Click Next ở page=1; click page 99 thủ công (simulate) | API page=2; nút ngoài range bị từ chối | EV-005, BR-003 |
| `SH-01-TC-006` | Race | Search A chậm, search B nhanh | Gõ A rồi B | Chỉ response B được render, lỗi A bị bỏ qua | EV-002/003, BR-005 |
| `SH-01-TC-007` | Navigation | Card `crs-101` | Click/Enter card | URL `/courses/crs-101`, mở SH-02 | EV-004 |
| `SH-01-TC-008` | Failure/Retry | API timeout lần 1; 200 lần 2 | Load → Thử lại | Lỗi rõ ràng; retry giữ filter/page; sau đó cards | EV-001/006, API-001 |

## 2. Kiểm tra bổ sung
- API 422 → không hiển thị stale list và banner lỗi query; API 429 → retry thủ công.
- Tab/card/next/previous điều khiển được bằng keyboard; role/labels hợp lệ.
- Responsive smoke test: 1280px và 375px, không tràn ngang.
- Backend phải chỉ trả published courses; dùng integration test, không chỉ test lọc phía UI.

**Fixture:** Tất cả responses và course IDs là dữ liệu minh họa, không phải dữ liệu thật.

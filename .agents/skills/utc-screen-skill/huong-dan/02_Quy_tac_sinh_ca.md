# QUY TẮC THIẾT KẾ CA KIỂM THỬ TỪ DD SCREEN

## 1. Ba tầng bao phủ

| Tầng | Căn cứ | Góc nhìn kiểm thử |
|---|---|---|
| Toàn màn hình (MH) | Tổng quan, flow, API, rule, trạng thái, phân quyền | Khi vào/rời trang, thứ tự gọi API, các state, tổng hợp dữ liệu, quyền, xử lý lỗi, bất đồng bộ |
| Thành phần (TP) | Element list, marker, screenshot, UI specification | Nhãn, hiển thị, giá trị, trạng thái, input/validation, thông báo, focus/keyboard, UI/UX |
| Sự kiện (SK) | Event definition, navigation, data flow, API contract | Trigger/response, phân nhánh, hành vi click/submit/hover, reset, lỗi, điều hướng, bất đồng bộ |

**Phân loại:** một testcase có thể chạm nhiều góc nhìn nhưng chỉ thuộc **một tầng chính** để tránh tính trùng số ca; tham chiếu các yêu cầu còn lại bằng danh sách `requirement_ids`.

## 2. Kỹ thuật từ ISTQB áp dụng khi có cơ sở

- **Phân hoạch tương đương:** nhóm dữ liệu hợp lệ/không hợp lệ mà DD quy định cùng xử lý.
- **Giá trị biên:** với giới hạn `maxLength=20` được duyệt, tạo riêng ca 19/20/21; không bịa maxLength khi DD không nói.
- **Bảng quyết định:** cho điều kiện phân quyền/ẩn hiện độc lập, dựng bảng role × điều kiện và một ca mỗi nhánh có hành vi khác.
- **Chuyển trạng thái:** kiểm tra từ loading sang empty/ready/error, chuyển page/sort; xác định trạng thái trước/sau dựa DD.
- **Kiểm thử theo kinh nghiệm:** có thể đề xuất exploratory/race tests, nhưng ghi rõ “Chờ xác nhận” nếu chưa là acceptance.

## 3. Mẫu ca đúng và sai

**Không chấp nhận:** “Nhấn nút. Kết quả đúng thiết kế.”

**Có thể chấp nhận (giả định DD đã duyệt):**

- Tiền điều kiện: màn hình ở trang 2, size=20, sort=name:asc.
- Dữ liệu: thao tác chọn `price:desc` (nằm trong allowlist API).
- Bước: thay lựa chọn sort, quan sát request #06 và state.
- Kỳ vọng: request có `page=1`, `size=20`, `sort=price:desc`; không gửi `category`; thay danh sách sau response hợp lệ.

Với GS-01 hiện tại, **sort control chưa được thiết kế/phê duyệt** nên ca phải có trạng thái `Chờ xác nhận`, dù thông số API đã rõ.

## 4. Ma trận nhánh chuẩn theo loại màn hình

| Góc nhìn | Tình huống thường xét | Lưu ý |
|---|---|---|
| API | thành công, rỗng, lỗi validation, lỗi server, timeout | Chỉ ghi kỳ vọng xử lý lỗi khi DD quy định; không gộp các lỗi có hành vi khác |
| Trạng thái | loading → ready/empty/error, stale data | Có thể cần nhiều ca cho cùng event |
| Nhập liệu | hợp lệ, rỗng, vượt giới hạn, ký tự Unicode, khoảng trắng | Chỉ dùng giới hạn đã có nguồn |
| Quyền | Guest/User/Admin, không phiên, phiên hết hạn | Không tự tạo route guard mới |
| Điều hướng | click link, route params, back/refresh | Không suy từ `href="#"` trong prototype |
| UI | content, disabled, feedback, focus, responsive | Ảnh tĩnh không chứng minh hành vi |
| Bảo mật | không lộ tài nguyên riêng tư, không gửi dữ liệu nhạy cảm | Phân biệt kiểm thử UI với kiểm thử API/penetration chuyên biệt |
| Bất đồng bộ | request liên tiếp, kết quả về sai thứ tự, cancellation | Phải có nguồn nói xử lý request cũ hoặc ghi đề xuất |

## 5. Quy tắc phân rã và mã hóa

- Mã theo dạng `GS-01-TC-MH-001`, `GS-01-TC-TP-001`, `GS-01-TC-SK-001`.
- Một ca → một kết quả có thể đánh giá Đạt/Không đạt độc lập; nhiều bước trong một hành vi là hợp lệ.
- Mỗi element có ít nhất một ca; mỗi event có ít nhất một ca.
- Mã yêu cầu nội bộ chưa phải ID DD chính thức: ghi nguồn tương ứng và không đổi source ID.
- Không phát sinh username/password thực, token hay dữ liệu người dùng.

## 6. Quy tắc trạng thái

**Tình trạng DD:** `Đã xác nhận`, `Chờ xác nhận`, `Không áp dụng`.

**Trạng thái thực thi:** `Chưa chạy`, `Đạt`, `Không đạt`, `Bị chặn`, `Không áp dụng`.

- `Đã xác nhận` chỉ có nghĩa nội dung đã đủ nguồn thiết kế, **không có nghĩa implementation đã đúng**.
- `Chờ xác nhận` cần danh sách quyết định và người phụ trách trước khi thực thi như một acceptance test.
- Khi phát hành mới từ DD, tất cả ca đều `Chưa chạy`; không điền bằng chứng/kết quả thật giả định.
- Sau khi test, mỗi ca Đạt/Không đạt/Bị chặn phải có kết quả thực tế, bằng chứng, người và ngày; cột `Kiểm tra hồ sơ` cảnh báo nếu thiếu.

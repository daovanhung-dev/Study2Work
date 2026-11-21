# OPEN_QUESTIONS — API #38

**Status:** Draft — Needs Confirmation
**Endpoint:** GET /api/v1/users/me/achievements

## Q-01 — Achievement unlock criteria

**Evidence:** AC-18 chỉ nêu “Đọc achievement unlocked”; DB guide nói achievements được tính từ dữ liệu hiện có nhưng không ghi rule.
**Impact:** Không thể xác định award nào đủ điều kiện, thời điểm unlocked hoặc có thể bị thu hồi hay không.
**Decision needed:** Chốt từng loại achievement, điều kiện/threshold, input source và cách xác định trạng thái unlocked.

## Q-02 — Achievement definition và response projection

**Evidence:** Catalog định nghĩa id, code, title, awarded_at và course_id?; ERD V1/checked-in DDL không có bảng achievements. DB guide để achievement ở dạng tính từ dữ liệu hiện có.
**Impact:** Chưa xác định nguồn tạo id/code/title/awarded_at/course_id hoặc cách giữ code/title ổn định giữa các lần gọi.
**Decision needed:** Chỉ rõ registry/config/source và phép ánh xạ cho từng response field; xác nhận derived result được tính on-read hay có materialized source khác.

## Q-03 — Ý nghĩa query course_id

**Evidence:** Catalog khai báo course_id?:int64; Achievement có course_id?; AC-18 không định nghĩa filter semantics hoặc predicate quyền truy cập course.
**Impact:** Chưa biết request có course_id có bao gồm achievement toàn cục không gắn course, và xử lý course không tồn tại/ngoài quyền ra sao.
**Decision needed:** Chốt quy tắc lọc, enrollment/ownership/access predicate và mapping 403; catalog hiện không khai báo 404.

## Q-04 — Pagination và ordering

**Evidence:** Response là Page<Achievement> với page, size, total, total_pages; API #38 chỉ khai báo query course_id.
**Impact:** Chưa biết page/size lấy từ đâu, giới hạn/default, total count predicate hoặc thứ tự ổn định.
**Decision needed:** Chốt pagination/order policy; nếu cần request page/size/sort parameters thì cập nhật approved catalog trước khi sửa DD.

## Q-05 — Empty result

**Evidence:** API được đặt tên “nếu có”; response schema là Page<Achievement>, nhưng AC/catalog không nói trạng thái khi Student chưa có achievement phù hợp.
**Impact:** UI và caller không biết phân biệt chưa có award với lỗi hay trường hợp khác.
**Decision needed:** Chốt success empty page shape và các trường pagination; không thêm 404 vì hiện không có trong catalog.

## Q-06 — course_id parse và domain validation

**Evidence:** Query field có type int64 optional; catalog chỉ liệt kê error codes 200/401/403/500.
**Impact:** Không xác định được behavior khi course_id không parse được hoặc ngoài miền hợp lệ.
**Decision needed:** Chốt validation/mapping; nếu cần 400/422 hoặc business code khác, cập nhật catalog trước khi đưa vào DD.

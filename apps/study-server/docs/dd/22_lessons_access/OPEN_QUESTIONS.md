# OPEN_QUESTIONS

Các quyết định dưới đây chặn việc chuyển DD sang Ready/Final hoặc dùng làm implementation contract. Bản Draft giữ nguyên contract đã có và không tự chọn câu trả lời.

<a id="q-22-01"></a>

## Q-22-01 — Access predicate, enrollment status và prerequisite

**Bằng chứng**

- AC-14 precondition nói Student đã enrolled vào course chứa lesson.
- AC-14 diagram gọi bước kiểm tra là `enrollment/prerequisite` và có nhánh `Allowed?`.
- DB design có `enrollments.user_id`, `course_id`, `status`; enum/status eligibility chưa được canonical hóa.

**Vấn đề**

- Chưa xác định enrollment status nào cấp quyền.
- Chưa có nguồn về prerequisite model, quan hệ, cách đánh giá hoặc thứ tự với enrollment check.

**Ảnh hưởng**

- Không thể chốt điều kiện allow/deny, query predicate hoặc hành vi cho prerequisite chưa đạt.

**Cần quyết định**

- Xác nhận access rule đầy đủ, enrollment eligibility/status và prerequisite source/evaluation trước khi viết query hoặc implementation.

<a id="q-22-02"></a>

## Q-22-02 — JWT identity dùng cho enrollment check

**Bằng chứng**

- Catalog yêu cầu Bearer JWT và role Student.
- DB design liên kết `enrollments.user_id` với user.
- Shared Study auth helper hiện parse JWT `sub` thành numeric user ID; API #22 chưa được wire để dùng helper.

**Vấn đề**

- Chưa có API-specific contract xác nhận claim/identity này được bind vào enrollment lookup như thế nào.

**Ảnh hưởng**

- Không thể hoàn chỉnh ownership predicate hoặc khai báo đó là behavior đã xác nhận của API #22.

**Cần quyết định**

- Xác nhận identity claim và mapping tới enrollment trước khi khóa điều kiện truy vấn.

<a id="q-22-03"></a>

## Q-22-03 — Wire shape của lý do 403

**Bằng chứng**

- AC-14 diagram ghi `NO → 403 + lý do`.
- API catalog chỉ khai báo `403 DESIGN_ACCESS_DENIED`; `ApiEnvelope<T>` không định nghĩa error-specific reason field.

**Vấn đề**

- Chưa rõ lý do nằm ở message, `data`, `meta` hay field khác; reason values cũng chưa được liệt kê.

**Ảnh hưởng**

- Client handling, response schema và ví dụ 403 chưa thể chốt. Example trong DD chỉ mang tính sơ đồ.

**Cần quyết định**

- Xác nhận vị trí, type, allowed values và message policy của lý do 403; cập nhật catalog/diagram nếu cần.

<a id="q-22-04"></a>

## Q-22-04 — Ý nghĩa HTTP 404

**Bằng chứng**

- Catalog khai báo `404 DESIGN_RESOURCE_NOT_FOUND`.
- AC-14 diagram không nêu resource/visibility condition cho 404.
- AC-15 có bước kiểm tra access và publish status cho endpoint lấy nội dung riêng.

**Vấn đề**

- Chưa rõ 404 có áp dụng cho lesson không tồn tại, course/parent không tồn tại, hoặc điều kiện visibility nào.
- Không được chuyển publish predicate từ API khác sang API #22 nếu chưa xác nhận.

**Ảnh hưởng**

- Không thể chốt query guard, response/message semantics hoặc phân biệt 403 với 404.

**Cần quyết định**

- Xác nhận tài nguyên và điều kiện cụ thể trả 404 cho API #22.

<a id="q-22-05"></a>

## Q-22-05 — Query, projection và schema baseline

**Bằng chứng**

- API response schema là `Lesson`; DB design ghi candidate fields trong `lessons` và relation `lessons.course_id`.
- Enrollment data có trong DB design, nhưng API #22 query/predicate không có.
- Current source không có API #22 module/query; checked-in DDL chưa chứng minh live schema.

**Vấn đề**

- Chưa xác định query kết hợp access decision với Lesson retrieval, selected columns, join/filters hoặc prerequisite data source.
- Live database metadata chưa được kiểm tra.

**Ảnh hưởng**

- Các mapping `lessons.*` trong DD chỉ là candidate design mapping; không thể dùng làm SQL đã phê duyệt hoặc runtime claim.

**Cần quyết định**

- Cung cấp/duyệt query source và baseline schema cho API #22, gồm projection cần trả về và bảng phục vụ prerequisite.

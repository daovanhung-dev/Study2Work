# OPEN_QUESTIONS

## Q-15-00 — Endpoint trong execution plan thiếu suffix

**Bằng chứng**

- Một dòng trong execution plan ghi `GET /api/v1/courses/{course_id}`.
- Canonical `list_api.md`, AC API index và AC-12 diagram ghi `GET /api/v1/courses/{course_id}/enrollment-status`.

**Quyết định authoring**

- DD dùng endpoint canonical có suffix `/enrollment-status`.
- Nếu path rút gọn là chủ đích, cần cập nhật đồng bộ API catalog, AC index và diagram trước khi triển khai.

## Q-15-01 — Public endpoint xác định enrollment của user nào?

**Bằng chứng**

- list_api.md ghi API #15 là Public; no Bearer token.
- Enrollment gồm user_id.
- enrollments có quan hệ user_id và course_id.

**Vấn đề**

- Request chỉ có course_id; không có user identity.
- Một course có thể có nhiều enrollment.

**Ảnh hưởng**

- Không thể khóa predicate chọn một Enrollment duy nhất.
- Không thể tự thêm JWT, query user_id, header hoặc response schema mới.

**Khuyến nghị**

- Giữ Public trong DD theo canonical contract.
- Product/architecture owner cần xác nhận identity source hoặc sửa contract trước runtime implementation.

## Q-15-02 — HTTP 404 đại diện cho resource nào?

**Bằng chứng**

- Contract chỉ khai báo 404 DESIGN_RESOURCE_NOT_FOUND.
- AC-12 sequence có bước đọc course và bước kiểm tra enrollment.

**Vấn đề**

- Chưa rõ 404 xảy ra khi course không tồn tại, enrollment không tồn tại, hay cả hai.

**Ảnh hưởng**

- Error mapping và message semantics chưa thể chốt.

**Khuyến nghị**

- Giữ một 404 design row ở DD và không tạo business code mới.

## Q-15-03 — Có giới hạn course PUBLISHED không?

**Bằng chứng**

- AC-12 sequence có bước Đọc Course PUBLISHED.
- API #15 row không ghi rõ predicate visibility.

**Vấn đề**

- Không biết API #15 cần kiểm tra mọi course hay chỉ course PUBLISHED.

**Ảnh hưởng**

- WHERE clause của Q1 và 404 semantics.

**Khuyến nghị**

- Ghi PUBLISHED là derived evidence, chờ confirmation trước khi coi là normative.

## Q-15-04 — Quy tắc nhiều enrollment cùng course/user là gì?

**Bằng chứng**

- Schema hiện tại không có unique constraint được xác nhận cho user_id + course_id.
- Contract trả một object Enrollment, không phải list.

**Vấn đề**

- Chưa có rule chọn active/latest/primary row hoặc integrity error.

**Ảnh hưởng**

- Không được dùng LIMIT 1 với order tự chọn.

**Khuyến nghị**

- Chốt uniqueness hoặc selection rule trước runtime implementation.

## Q-15-05 — Enum hợp lệ của enrollments.status là gì?

**Bằng chứng**

- DB.sql chỉ khai báo VARCHAR(20) DEFAULT ACTIVE.
- Contract dùng EnrollmentStatus nhưng không liệt kê enum values.

**Vấn đề**

- Không thể kiểm tra hoặc chuẩn hóa status ngoài việc map trực tiếp.

**Khuyến nghị**

- Bổ sung enum catalog hoặc giữ status opaque string trong implementation contract.

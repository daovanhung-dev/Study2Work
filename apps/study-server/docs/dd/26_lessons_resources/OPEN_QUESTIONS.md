# OPEN_QUESTIONS — Study API #26

Các quyết định dưới đây cần được xác nhận trước khi chuyển DD sang Ready/Final hoặc dùng làm implementation contract. Bản Draft giữ nguyên contract hiện có và không tự chọn câu trả lời.

<a id="q-26-01-response-type-và-resource-payload"></a>

## Q-26-01 — Response type và Resource payload

**Bằng chứng**

- API catalog và AC-15 diagram khai báo `ApiEnvelope<Lesson>`.
- API #26 tên “Lấy tài nguyên đính kèm”; AC-15 hậu điều kiện hiển thị tài nguyên.
- Reusable schema định nghĩa `Lesson` và `Resource` riêng; `Lesson` không liệt kê Resource field.

**Vấn đề**

- Contract chưa nói API #26 trả Lesson, một Resource, danh sách Resource, hoặc một schema khác.

**Ảnh hưởng**

- Không thể chốt response fields, item mapping, JSON example, client contract hoặc response source matrix.

**Cần quyết định**

- API/schema owner xác nhận payload type/cardinality và cập nhật catalog/diagram nếu contract hiện tại không đúng.

<a id="q-26-02-cardinality-ordering-and-empty-result"></a>

## Q-26-02 — Cardinality, ordering và empty result

**Bằng chứng**

- ERD mô tả `resources.lesson_id → lessons.id`, cho phép nhiều resource theo lesson.
- API #26 không có pagination hoặc sort parameter.

**Vấn đề**

- Chưa có quy tắc số lượng item, thứ tự ổn định, pagination hoặc behavior khi lesson chưa có resource.

**Ảnh hưởng**

- Không thể chốt query ordering, array/page shape, performance bound hoặc empty response.

**Cần quyết định**

- Xác nhận cardinality, ordering, pagination (nếu có) và empty-result behavior; cập nhật canonical contract.

<a id="q-26-03-authorization-and-publish-policy"></a>

## Q-26-03 — Student entitlement và publish policy

**Bằng chứng**

- Catalog yêu cầu Student Bearer JWT.
- AC-15 precondition nói Student có quyền xem lesson.
- Diagram có bước kiểm tra access và trạng thái publish trong lesson flow, nhưng không định nghĩa query/predicate cụ thể cho lời gọi API #26 độc lập.

**Vấn đề**

- JWT identity binding, enrollment/prerequisite rule, entity publish state và direct-call authorization chưa chốt.

**Ảnh hưởng**

- Không thể xác định query guard, điều kiện 403 hoặc thông tin cần che khi không có quyền.

**Cần quyết định**

- Xác nhận server-side entitlement, claim binding, publish scope và 403/404 visibility policy.

<a id="q-26-04-resource-visibility"></a>

## Q-26-04 — Resource visibility source

**Bằng chứng**

- Reusable `Resource` schema có `visibility:ResourceVisibility`.
- ERD V1 và checked-in DDL không có `resources.visibility`.

**Vấn đề**

- Chưa có source cho visibility value, storage hoặc access predicate.

**Ảnh hưởng**

- Không thể trả field visibility hoặc filter resource theo visibility.

**Cần quyết định**

- Xác nhận source of truth/schema migration nếu visibility cần dùng; cập nhật contract và DB design trước khi mapping.

<a id="q-26-05-url-and-signed-url-behavior"></a>

## Q-26-05 — URL và signed URL behavior

**Bằng chứng**

- DB design/DDL lưu `resources.url`.
- API #12 adjacent design mô tả signed URL cho private resource, nhưng API #26 diagram không chỉ định external call hoặc URL transform.

**Vấn đề**

- Chưa rõ API #26 trả stored URL hay resolve signed URL, và signed URL có thuộc API #12 hay không.

**Ảnh hưởng**

- Không thể chốt source field, expiry, external dependency, security handling hoặc lỗi dependency.

**Cần quyết định**

- Xác nhận URL contract và API chịu trách nhiệm ký URL; bổ sung dependency/error code nếu cần.

<a id="q-26-06-not-found-and-error-semantics"></a>

## Q-26-06 — 404 condition và error payload

**Bằng chứng**

- Catalog khai báo 401/403/404/500, không khai báo error payload/message policy.
- `DESIGN_RESOURCE_NOT_FOUND` chưa gắn với lesson missing, resource missing, empty list hoặc visibility.

**Vấn đề**

- Chưa rõ khi không có resource thì trả 200 empty hay 404; 403/404 có che giấu resource hay không.

**Ảnh hưởng**

- Không thể chốt client behavior, error examples hoặc acceptance cases beyond catalog codes.

**Cần quyết định**

- Xác nhận điều kiện 404, empty result, 403/404 split và error envelope/message fields.

<a id="q-26-07-resource-schema-and-path-validation"></a>

## Q-26-07 — Resource schema và path validation

**Bằng chứng**

- ERD ghi `resources.lesson_id` là bắt buộc; checked-in DDL khai báo `BIGINT REFERENCES lessons(id)` nhưng không có `NOT NULL`.
- `Resource.type` dùng `ResourceType`; enum values chưa được liệt kê.
- Catalog chỉ ghi `lesson_id:int64!`, không ghi range hoặc positivity rule.

**Vấn đề**

- Candidate DB nullability khác nhau; enum và path constraint/status mapping chưa có nguồn chốt.

**Ảnh hưởng**

- Không thể chốt data integrity assumption, allowed resource types hoặc invalid-path behavior.

**Cần quyết định**

- Xác nhận schema baseline, `ResourceType` values, `lesson_id` constraints và invalid path behavior.

## Điều kiện đóng các câu hỏi

- Cập nhật canonical API/schema/diagram/DB source trước khi chuyển DD sang Ready/Final.
- Sau khi contract được xác nhận, cập nhật response/data mapping, error conditions và acceptance scenarios liên quan.
- Không xem ERD/DDL checked-in là bằng chứng về live schema.


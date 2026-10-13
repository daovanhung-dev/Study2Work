# OPEN_QUESTIONS

Các quyết định dưới đây cần được xác nhận trước khi chuyển DD sang Ready/Final hoặc dùng làm implementation contract. Bản Draft giữ contract hiện có và không tự chọn câu trả lời.

<a id="q-25-01"></a>

## Q-25-01 — Ý nghĩa và nơi lưu `position`

**Bằng chứng**

- API catalog yêu cầu body `position:int32!`.
- `lesson_progress` trong ERD và checked-in DDL không có cột `position`.

**Vấn đề**

- Chưa rõ `position` là thời gian video, offset nội dung hay một đơn vị khác; schema hiện có không có target column.

**Ảnh hưởng**

- Không thể chốt validation, persistence mapping, resume behavior hoặc data migration.

**Cần quyết định**

- API/schema owner xác nhận ý nghĩa, đơn vị, null/range semantics và nguồn lưu có thẩm quyền; cập nhật schema/design trước khi chốt mapping.

<a id="q-25-02"></a>

## Q-25-02 — Range và quan hệ giữa `percent` với `position`

**Bằng chứng**

- Catalog chỉ chốt `percent:int32!`.
- DB design có `progress_percent SMALLINT DEFAULT 0` nhưng ERD không ghi CHECK range.

**Vấn đề**

- Chưa biết range, rounding, cách chuyển int32 sang SMALLINT hoặc field nào là nguồn chuẩn khi `percent` không khớp `position`.

**Ảnh hưởng**

- Không thể chốt validation, 422 trigger, SQL type conversion hoặc expected-value tests.

**Cần quyết định**

- Chốt allowed range, rounding và precedence/consistency rule; cung cấp schema constraint nếu có.

<a id="q-25-03"></a>

## Q-25-03 — State transition và timestamps

**Bằng chứng**

- AC-14 ghi `completed = YES` → mark `COMPLETED`; `NO` → giữ `IN_PROGRESS`.
- Candidate `lesson_progress` có `status`, `last_accessed_at`, `completed_at`; enum ngoài default chưa được canonical hóa.

**Vấn đề**

- Chưa rõ cách persist `completed`, timestamp nào được set/clear, hoặc hành vi khi row hiện tại đã COMPLETED và request mới có `completed=false`.

**Ảnh hưởng**

- Không thể đặc tả update mapping, state machine, timestamp behavior hoặc retry/out-of-order result.

**Cần quyết định**

- Xác nhận allowed states, transition matrix, timestamp source và preservation/reset policy cho mọi nhánh.

<a id="q-25-04"></a>

## Q-25-04 — Upsert identity, uniqueness và repeated/out-of-order requests

**Bằng chứng**

- DB design gọi API #25 là UPDATE/upsert.
- Checked-in DDL chỉ khai báo primary key `id`; không khai báo unique `(user_id, lesson_id)`.

**Vấn đề**

- Chưa rõ API update row bắt buộc tồn tại hay tạo mới, conflict key nào được hỗ trợ, và request lặp/đến sai thứ tự có được idempotent hoặc có thể làm giảm tiến độ hay không.

**Ảnh hưởng**

- Không thể chốt conflict target, concurrency safety, state preservation hoặc retry contract.

**Cần quyết định**

- Xác nhận row identity, unique constraint/index, create-vs-update behavior, concurrency policy và out-of-order handling.

<a id="q-25-05"></a>

## Q-25-05 — Direct-call authorization và Student identity

**Bằng chứng**

- Catalog yêu cầu Bearer JWT và role Student.
- AC-14 precondition yêu cầu Student đã enrolled; flow đặt API #22 access check trước API #25.

**Vấn đề**

- Chưa biết API #25 phải kiểm tra entitlement khi được gọi độc lập, claim nào map sang `lesson_progress.user_id`, hoặc enrollment/prerequisite predicate nào áp dụng.

**Ảnh hưởng**

- Không thể chốt write ownership, query predicate, 403 condition hoặc tránh sửa progress của Student khác.

**Cần quyết định**

- Xác nhận JWT identity binding, direct-call authorization requirement, enrollment/prerequisite policy và behavior khi access denied.

<a id="q-25-06"></a>

## Q-25-06 — 404/422 conditions và error payload

**Bằng chứng**

- Catalog khai báo 404 `DESIGN_RESOURCE_NOT_FOUND` và 422 `DESIGN_VALIDATION_ERROR`.
- Request chỉ nêu types/required markers; API #25 chưa có runtime route để xác nhận trigger.

**Vấn đề**

- Chưa rõ resource nào gây 404, validation nào gây 422, 403/404 phân biệt ra sao, hoặc message/error data wire shape là gì.

**Ảnh hưởng**

- Không thể chốt client-visible error handling, validation tests hoặc visibility policy.

**Cần quyết định**

- Chốt resource condition, path/body constraints, HTTP/business mapping và error envelope/message policy.

<a id="q-25-07"></a>

## Q-25-07 — Course aggregate, transaction và failure behavior

**Bằng chứng**

- AC-14 ghi “UPDATE lesson progress + course aggregate”.
- Không có aggregate formula, source/target table, transaction boundary hoặc rollback rule trong catalog/diagram.

**Vấn đề**

- Chưa rõ aggregate là computed hay persisted, phạm vi lesson nào, update đồng bộ/không đồng bộ, hoặc xử lý thế nào nếu chỉ một phần mutation thành công.

**Ảnh hưởng**

- Không thể chốt query/mutation, atomicity, retry behavior hoặc consistency guarantee.

**Cần quyết định**

- Xác nhận aggregate source/target/formula, thời điểm update, transaction/failure policy và schema có thẩm quyền.

<a id="q-25-08"></a>

## Q-25-08 — `ApiEnvelope<Lesson>` payload sau mutation

**Bằng chứng**

- Catalog khai báo `ApiEnvelope<Lesson>`.
- AC-14 diagram ghi generic `ApiEnvelope`; không nêu Lesson projection hoặc response assembly sau progress update.

**Vấn đề**

- Chưa rõ success response trả Lesson hiện tại, Lesson có progress, hay một shape khác; query/projection không có trong source.

**Ảnh hưởng**

- Không thể chốt response source, serialization/example hoặc client contract beyond catalog type.

**Cần quyết định**

- Xác nhận response payload/type và Lesson projection; cập nhật canonical catalog/diagram nếu payload khác schema đang khai báo.

---

## Điều kiện đóng các câu hỏi

- Cập nhật nguồn canonical/schema trước khi chuyển DD sang Ready/Final.
- Sau khi contract được xác nhận, cập nhật request, response, mutation mapping, error cases và acceptance scenarios liên quan.
- Không xem checked-in DDL/ERD là bằng chứng về live schema.

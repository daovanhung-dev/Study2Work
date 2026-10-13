# OPEN_QUESTIONS

Các quyết định dưới đây cần được xác nhận trước khi chuyển DD sang Ready/Final hoặc dùng làm implementation contract. Bản Draft giữ nguyên contract hiện có và không tự chọn câu trả lời.

<a id="q-23-01"></a>

## Q-23-01 — UPSERT identity, conflict key và uniqueness

**Bằng chứng**

- AC-14 diagram ghi UPSERT lesson progress = IN_PROGRESS.
- Checked-in DDL có lesson_progress.user_id và lesson_progress.lesson_id nhưng không khai báo unique constraint cho cặp này.

**Vấn đề**

- Chưa biết điều kiện nhận diện bản ghi tiến độ, index/constraint tương ứng hoặc cách xử lý nếu có nhiều bản ghi cùng user/lesson.

**Ảnh hưởng**

- Không thể đặc tả conflict target, SQL upsert hoặc tính an toàn khi các lần start đồng thời.

**Cần quyết định**

- Xác nhận khóa nghiệp vụ và constraint/index được hỗ trợ bởi schema có thẩm quyền trước khi chốt mutation.

<a id="q-23-02"></a>

## Q-23-02 — Field updates và state preservation

**Bằng chứng**

- AC-14 chỉ ghi trạng thái đích IN_PROGRESS.
- DDL candidate có status, progress_percent, last_accessed_at và completed_at.

**Vấn đề**

- Chưa rõ upsert chỉ set status hay còn cập nhật last_accessed_at; chưa rõ xử lý progress_percent/completed_at hiện có hoặc bản ghi đã COMPLETED.

**Ảnh hưởng**

- Không thể hoàn chỉnh insert/update mapping hoặc bảo đảm API start không làm mất tiến độ đã ghi nhận.

**Cần quyết định**

- Chốt field được ghi ở insert/update, state transition khi gọi lại và field phải giữ nguyên/reset; cung cấp nguồn cho giá trị timestamp nếu cần.

<a id="q-23-03"></a>

## Q-23-03 — Repeated start, idempotency và HTTP 201

**Bằng chứng**

- Catalog quy định POST thành công trả 201 DESIGN_RESOURCE_CREATED.
- AC-14 dùng từ UPSERT, bao gồm khả năng bản ghi đã tồn tại nhưng không định nghĩa branch response.

**Vấn đề**

- Chưa biết lần gọi lại tạo mới hay chỉ cập nhật bản ghi, có idempotency guarantee hay không, và 201 có dùng cho cả hai nhánh không.

**Ảnh hưởng**

- Client không thể diễn giải chính xác 201 khi progress row đã tồn tại; không thể chốt retry behavior.

**Cần quyết định**

- Xác nhận semantics cho row mới/existing, HTTP/business code và idempotency/retry contract.

<a id="q-23-04"></a>

## Q-23-04 — Success payload và response assembly

**Bằng chứng**

- API catalog khai báo ApiEnvelope<Lesson>.
- AC-14 diagram ghi ApiEnvelope, không nêu generic payload; API #24 GET lesson là bước riêng tiếp theo.
- Checked-in DDL/DB design có lessons candidate schema nhưng không có query API #23.

**Vấn đề**

- Chưa rõ API #23 trả Lesson hay envelope không có payload, và nếu trả Lesson thì source/projection nào tạo payload.

**Ảnh hưởng**

- Chưa thể coi ví dụ hoặc Lesson field mapping là response serialization đã được xác minh.

**Cần quyết định**

- Xác nhận contract response giữa catalog và AC diagram, cùng nguồn dữ liệu/projection Lesson nếu catalog type được giữ nguyên.

<a id="q-23-05"></a>

## Q-23-05 — Direct-call authorization, enrollment/prerequisite và 403

**Bằng chứng**

- Catalog yêu cầu Student Bearer JWT và liệt kê 403 DESIGN_ACCESS_DENIED.
- AC-14 precondition yêu cầu Student enrolled; diagram đặt API #22 enrollment/prerequisite check trước API #23.

**Vấn đề**

- Chưa biết API #23 có tự kiểm tra access khi được gọi trực tiếp hay dựa vào API #22, cũng như identity claim và predicate cụ thể.

**Ảnh hưởng**

- Không thể chốt 403 condition hoặc write authorization; thứ tự gọi trên client không phải bằng chứng server-side access control.

**Cần quyết định**

- Xác nhận entitlement check bắt buộc tại API #23, enrollment/prerequisite rule, token-to-user binding và behavior khi access denied.

<a id="q-23-06"></a>

## Q-23-06 — 404 và 422 conditions

**Bằng chứng**

- Catalog khai báo 404 DESIGN_RESOURCE_NOT_FOUND và 422 DESIGN_VALIDATION_ERROR.
- Request chỉ khai báo path lesson_id:int64!; không có range, existence, visibility hoặc validation mapping chi tiết.

**Vấn đề**

- Chưa rõ tài nguyên nào vắng mặt dẫn tới 404 hoặc điều kiện nào của path trả 422.

**Ảnh hưởng**

- Không thể chốt query guard, error mapping hoặc phân biệt 403 với 404.

**Cần quyết định**

- Xác nhận 404 resource condition và 422 validation rules/wire mapping; không suy ra lesson visibility từ API khác.

<a id="q-23-07"></a>

## Q-23-07 — Transaction, failure và live schema

**Bằng chứng**

- API #23 có write side effect trong AC-14 nhưng không có transaction/failure behavior.
- Checked-in DDL là design evidence; live schema chưa được xác minh.

**Vấn đề**

- Chưa rõ transaction ownership, atomicity với success response, rollback khi write/query thất bại và schema đang chạy có tương thích hay không.

**Ảnh hưởng**

- Không thể khẳng định consistency/failure behavior hoặc sử dụng DDL checked-in như runtime guarantee.

**Cần quyết định**

- Xác nhận transaction/failure contract và schema baseline trước khi hoàn thiện implementation mapping.

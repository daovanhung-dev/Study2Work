# ST-08 — Events (đặc tả xử lý)

## 1. Event index
| Event ID trong package | Source Event ID / heading | Chi tiết |
|---|---|---|
| `ST-08-EV-001` | `ST08-EV-01` / ST08-EV-01 — Vào trang và nạp enrollment list | See source event detail below |
| `ST-08-EV-002` | `ST08-EV-02` / ST08-EV-02 — Nạp progress và ghép với course | See source event detail below |
| `ST-08-EV-003` | `ST08-EV-03` / ST08-EV-03 — Thay đổi filter trạng thái (expected, element chưa được thiết kế) | See source event detail below |
| `ST-08-EV-004` | `ST08-EV-04` / ST08-EV-04 — Mở tổng quan tiến độ | See source event detail below |
| `ST-08-EV-005` | `ST08-EV-05` / ST08-EV-05 — Điều hướng từ header | See source event detail below |
| `ST-08-EV-006` | `ST08-EV-06` / ST08-EV-06 — Điều hướng từ footer | See source event detail below |
| `ST-08-EV-007` | `ST08-EV-07` / ST08-EV-07 — Chọn khóa học để mở ST-09 (expected, card chưa tồn tại) | See source event detail below |
| `ST-08-EV-008` | `Source heading` / API contract, dữ liệu và bảo mật | See source event detail below |
| `ST-08-EV-009` | `Source heading` / API #20 — Lấy khóa đã đăng ký | See source event detail below |
| `ST-08-EV-010` | `Source heading` / API #21 — Lấy progress tổng hợp | See source event detail below |
| `ST-08-EV-011` | `Source heading` / Data mapping và tính tiến độ | See source event detail below |
| `ST-08-EV-012` | `Source heading` / Bảo mật và quyền riêng tư | See source event detail below |

> Event IDs trong package là alias để theo template; Source Event IDs, steps và API links giữ theo DD nguồn. Alias không chứng minh event runtime.

## 2. Chi tiết event từ DD nguồn

### Trích từ DD nguồn: D. Đặc tả sự kiện

### ST08-EV-01 — Vào trang và nạp enrollment list

| Thuộc tính | Mô tả |
|---|---|
| Trigger / loại | Route entry hoặc page load; loại `Load`. |
| Element | Page-level event; không có control/EL ID. |
| Điều kiện | Route dự kiến `/student/courses`; AC-13 yêu cầu Student đã đăng nhập. Client guard/session chưa có source. |
| Input | URL path; session/token và role theo auth context nếu được triển khai. API #20 nhận query tùy chọn `status?: string`, `page?: int32`; giá trị mặc định/enum/page base/page size chưa định nghĩa. Không có path param hoặc body. |
| API thiết kế | `GET /api/v1/users/me/courses`; `Authorization: Bearer <JWT>`; role `Student` theo catalog. Catalog khai báo response `ApiEnvelope<UserProfile>`. Các field bên trong envelope không được schema hóa tại catalog row. |

**Trình tự thiết kế:** (1) nhận route và query state nếu có; (2) yêu cầu danh tính Student theo AC/catalog, nhưng chưa có guard hiện hành; (3) tạo GET #20, không gửi user ID riêng theo endpoint `/me`; (4) đọc HTTP/business result; với `200 DESIGN_RESOURCE_RETRIEVED`, contract hiện chỉ cho phép kỳ vọng `ApiEnvelope<UserProfile>` nên không có mapping đã xác nhận từ payload sang course rows; (5) không suy ra collection rỗng hoặc thành công render list từ `UserProfile`; (6) cập nhật screen state chỉ sau khi API schema, pagination và enrollment projection được chốt. Hiện tại toàn bộ request/UI flow này là chưa wired.

**Kết quả/lỗi theo catalog:** `200 DESIGN_RESOURCE_RETRIEVED`; `401 DESIGN_AUTHENTICATION_REQUIRED`; `403 DESIGN_ACCESS_DENIED`; `422 DESIGN_VALIDATION_ERROR`; `500 DESIGN_INTERNAL_ERROR`. Catalog không chỉ rõ body lỗi hoặc UI mapping. Network failure, timeout, retry, duplicate load, cache, cancellation và stale response policy chưa có contract; không tự đặt quy tắc. #20 không có route/module/query/test source trong checkout.

### ST08-EV-02 — Nạp progress và ghép với course

| Thuộc tính | Mô tả |
|---|---|
| Trigger / loại | Sau khi #20 được thiết kế để trả danh sách cần ghép, hoặc theo AC-13 orchestration; loại `Load/API`. |
| Element | Page-level event; không có control/EL ID. |
| Điều kiện | Chỉ sau khi API #20/#21 schema và thứ tự request được xác nhận. Inventory cho gọi #21 nếu #20 không kèm progress; AC-13 yêu cầu cả #20 và #21. |
| Input | Catalog ghi nguyên văn query `course_id list hoặc aggregate?:string`; chưa xác định tên/kiểu query thực tế, nhiều giá trị truyền thế nào, hay `aggregate` là filter, mode hay flag. Không có body/path param. |
| API thiết kế | `GET /api/v1/users/me/progress`; `Authorization: Bearer <JWT>`; role `Student`; response catalog `ApiEnvelope<UserProfile>`. |

**Trình tự thiết kế:** (1) nhận course identifiers từ response #20 chỉ khi contract xác nhận field/kiểu; (2) xác minh Student/session như API design yêu cầu; (3) gọi #21 theo query grammar đã duyệt; (4) với `200 DESIGN_RESOURCE_RETRIEVED`, kiểm tra schema đã chốt; (5) ghép record theo `course_id` như AC-13/inventory nhưng không tự chọn duplicate policy, missing-progress default hoặc formula; (6) chỉ render percent khi progress numerator/denominator, completed rule và rounding đã được xác nhận. Hiện không thể thực hiện các bước mapping vì cả hai response đều khai báo `UserProfile` và không có endpoint source.

**Thứ tự và lỗi:** AC-13 flow mô tả #20 → lấy progress → merge; inventory mô tả #20 rồi #21 “nếu cần”. Chưa thể quyết định sequential/parallel/conditional. Catalog status: `200 DESIGN_RESOURCE_RETRIEVED`, `401 DESIGN_AUTHENTICATION_REQUIRED`, `403 DESIGN_ACCESS_DENIED`, `500 DESIGN_INTERNAL_ERROR`; không liệt kê 422 cho #21. Không có timeout/retry/partial-failure/cache contract. Inventory có `partial-progress` state nhưng chưa định nghĩa khi nào thiếu progress là partial thay vì error/zero; không hiển thị 0% theo suy đoán.

### ST08-EV-03 — Thay đổi filter trạng thái (expected, element chưa được thiết kế)

| Thuộc tính | Mô tả |
|---|---|
| Trigger / loại | User đổi status filter; loại dự kiến `Change`. |
| Element | **Chưa tồn tại** trong HTML/PNG; không có Element ID hoặc marker. |
| Điều kiện | Chỉ có thể triển khai khi control, option values, default và status semantics được duyệt. |
| Input | Inventory/API #20 chỉ cho biết query `status?: string`. Chưa rõ lọc `enrollments.status` hay `courses.status`, enum, case sensitivity, empty/all semantics hoặc giá trị mặc định. |
| API / xử lý | Ý định inventory là truyền status vào #20; catalog liệt kê #20 `422 DESIGN_VALIDATION_ERROR`. Do chưa có contract enum và UI element, không chuẩn hóa, không tạo request, không giữ/cập nhật filter state ở bản hiện tại. |
| Kết quả / ngoại lệ | Sau khi được xác nhận: response phải được ánh xạ theo schema/paging đã chốt; hiện không thể định nghĩa empty/partial/error output. #20 runtime route chưa có. |

**Blocker:** API DD #20 Q-20-02 cần quyết định status áp dụng cho Enrollment hay Course và tập giá trị/default/case semantics; Q-20-03 cần chốt paging/order. Thiết kế loaded state/filter control cũng chưa có.

### ST08-EV-04 — Mở tổng quan tiến độ

| Thuộc tính | Mô tả |
|---|---|
| Trigger / loại | Click `ST08-EL-07`, CTA “Xem tiến độ học tập”; `Click/navigation`. |
| Điều kiện | Link tồn tại trong HTML tĩnh; route `/student/progress` là route đề xuất của ST-20. Destination/runtime auth guard chưa verify. |
| Input | Không có user input hoặc course ID; anchor href không mang query. Current student context được thiết kế bởi `/me` API family, nhưng handoff/session store chưa được xác nhận. |
| Xử lý | Trình duyệt theo href trong mockup; không có client router source để xác nhận SPA navigation, history hoặc route protection. Không gọi API ở click theo HTML hiện tại. |
| Kết quả / lỗi | Expected destination ST-20. Destination file [ST-20 source HTML](../../screen_stitch/03_student/ST-20_tong-quan-tien-do/code.html) là asset thiết kế; router, screen state, lỗi auth và back behavior chưa được xác minh. |

### ST08-EV-05 — Điều hướng từ header

| Thuộc tính | Mô tả |
|---|---|
| Trigger / loại | Click brand hoặc một link trong `ST08-EL-02`; `Click/navigation`. |
| Điều kiện | Anchor tương ứng được render. Role guard/runtime route chưa có source. |
| Input | Chọn một trong các href tĩnh: `/student` (brand hoặc Tổng quan), `/student/courses` (Khóa học của tôi), `/student/progress` (Tiến độ). |
| Xử lý | Mockup dùng native anchors; không truyền course data, filter hoặc progress state. Không gọi API tại event này trong HTML. |
| Kết quả / lỗi | `/student` là ST-01; `/student/courses` là ST-08; `/student/progress` là ST-20 theo inventory. Các route là expected destinations; runtime, active-nav state sau navigation, redirect 401/403 và history chưa verify. |

### ST08-EV-06 — Điều hướng từ footer

| Thuộc tính | Mô tả |
|---|---|
| Trigger / loại | Click một link trong `ST08-EL-09`; `Click/navigation`. |
| Điều kiện | Footer anchor được render. |
| Input | Href tĩnh `/student`, `/student/courses` hoặc `/student/progress`; không có query/body. |
| Xử lý | Native anchor trong HTML; không có client router source, data handoff hoặc API call. |
| Kết quả / lỗi | Expected destinations ST-01, ST-08, ST-20 tương ứng. Browser/app navigation failure, session expiry và return path chưa có behavior source-backed. |

### ST08-EV-07 — Chọn khóa học để mở ST-09 (expected, card chưa tồn tại)

| Thuộc tính | Mô tả |
|---|---|
| Trigger / loại | Click course card/row; loại dự kiến `Click/navigation`, liên kết được inventory khai báo tới ST-09. |
| Element | **Chưa tồn tại** trong HTML/PNG; không có Element ID, marker, card fields hoặc click target để mô tả current behavior. |
| Điều kiện | Chỉ khả dụng sau khi API #20 trả course identifier đã xác nhận và screen design cho loaded-state/card được duyệt. Cần đảm bảo khóa thuộc enrollment hiện tại; contract kiểm tra ownership chưa có source. |
| Input | Ý định route của ST-09 là `/student/courses/:courseId`; giá trị `courseId` phải đến từ #20 khi field/schema được chốt. Không suy ra ID từ DDL hoặc tạo route param từ tên khóa. |
| Xử lý | Không có card nên event không thể phát sinh trong current UI. Không thể xác định click target, keyboard semantics, selected/loading state hay prefetch. ST-09 inventory còn yêu cầu xác nhận course thuộc danh sách #20 trước khi tải #37. |
| Kết quả / lỗi | Expected destination ST-09 với path `courseId`; [ST-09 source HTML](../../screen_stitch/03_student/ST-09_tong-quan-khoa-dang-hoc/code.html) chỉ là asset thiết kế. Chưa có quy tắc xử lý ID thiếu, enrollment revoked, 404/403 hoặc back-to-list filter restoration tại ST-08. |

### API contract, dữ liệu và bảo mật

### API #20 — Lấy khóa đã đăng ký

| Thuộc tính | Contract đang khai báo |
|---|---|
| Method / endpoint | `GET /api/v1/users/me/courses` |
| Authentication / authorization | `Bearer JWT`; role `Student` trong catalog. Runtime endpoint không tìm thấy. Cách bind principal tới enrollment owner là open question. |
| Path / query / body | Không có path param; `status?: string`, `page?: int32`; không khai báo body. Enum/default/validation chi tiết và page metadata chưa được chốt. |
| Response | `ApiEnvelope<UserProfile>` theo catalog; không đủ biểu diễn course collection theo AC-13. Không đổi sang `Page<Course>` hoặc tự thêm field. |
| HTTP/business codes | `200 DESIGN_RESOURCE_RETRIEVED`; `401 DESIGN_AUTHENTICATION_REQUIRED`; `403 DESIGN_ACCESS_DENIED`; `422 DESIGN_VALIDATION_ERROR`; `500 DESIGN_INTERNAL_ERROR`. Error body chưa được đối chiếu source. |
| Runtime/source status | `NOT_FOUND` trong source/tests hiện đã rà soát; API DD là Draft — Needs Confirmation. Không có test xác minh. |

### API #21 — Lấy progress tổng hợp

| Thuộc tính | Contract đang khai báo |
|---|---|
| Method / endpoint | `GET /api/v1/users/me/progress` |
| Authentication / authorization | `Bearer JWT`; role `Student` trong catalog. Runtime endpoint không tìm thấy. User scoping chưa được xác minh. |
| Path / query / body | Không có path param; catalog ghi `course_id list hoặc aggregate?:string` (cú pháp/kiểu không rõ); không khai báo body. |
| Response | `ApiEnvelope<UserProfile>` theo catalog; không xác định tiến độ/course ID, aggregation, nullability hoặc empty shape. |
| HTTP/business codes | `200 DESIGN_RESOURCE_RETRIEVED`; `401 DESIGN_AUTHENTICATION_REQUIRED`; `403 DESIGN_ACCESS_DENIED`; `500 DESIGN_INTERNAL_ERROR`. Catalog không khai báo 422 cho #21. |
| Runtime/source status | `NOT_FOUND` trong source/tests hiện đã rà soát; API DD là Draft — Needs Confirmation. Không có test xác minh. |

### Data mapping và tính tiến độ

- AC-13 yêu cầu ghép khóa và progress theo `course_id`, nhưng API contract chưa khai báo course/progress DTO hoặc merge-key type.
- Legacy DDL `infra/postgres/study-server/DB.sql` có BIGSERIAL `courses`/`enrollments` và `lesson_progress(user_id, lesson_id, status, progress_percent, last_accessed_at, completed_at)`. Đây là candidate DDL, chưa xác nhận live schema hoặc query được dùng bởi API #20/#21.
- V1-PILOT DDL `infra/postgres/02_study_db.sql` dùng course-version/enrollment model với UUID (`course_enrollments.id`, `learner_id`, `course_version_id`) và progress facts/snapshots (`lesson_progress_facts`, `progress_snapshots`). Đây là artifact thiết kế khác, không interchangeable với legacy BIGINT tables; không xác định được từ source hiện tại mô hình nào sẽ phục vụ #20/#21.
- Hai DDL artifact không xác nhận live schema, query hoặc API projection. Không suy luận `courseId` type từ `ST-09` route, API #20 query, hay legacy columns.
- DDL chưa định nghĩa ở đây cách tính aggregate theo số lesson, quiz/assignment, trạng thái hoàn tất, bài bị ẩn/đã xóa, rounding hoặc progress cho course không có lesson. Không dùng `lesson_progress.progress_percent` trực tiếp làm tổng tiến độ khóa học nếu chưa có quy tắc.
- `enrollments.status` và `courses.status` cùng tồn tại; DDL không cho biết query `status` của #20 lọc trường nào. DDL cũng không chứng minh page order, enrollment uniqueness hay missing-user behavior.
- API #37 là course progress chi tiết cho ST-09/ST-20 theo inventory; không thay #21 hoặc tự dùng làm aggregate cho ST-08 khi chưa được xác nhận.

### Bảo mật và quyền riêng tư

- Catalog giới hạn #20/#21 cho role Student và Bearer JWT. Không gửi user ID do client tự nhập; đường dẫn `/me` hàm ý principal context nhưng quy tắc bind/ownership phải được API owner xác nhận.
- Không hiển thị enrollment/progress của người khác; hiện không có endpoint implementation để xác minh scoping hoặc authorization. Không coi việc ẩn UI nav là kiểm soát truy cập.
- 401/403 được liệt kê trong catalog nhưng chưa có contract UI: refresh/reauth, redirect, giữ return path và nội dung lỗi đều chưa quyết định. Không tự chọn hành vi.
- Nếu Study Web được triển khai, cần xác minh session không bị lộ qua URL/log và dữ liệu private không hiển thị trước authorization; chưa có client source để xác nhận các biện pháp này.

## Trace links
- [UI Elements](01-ui-elements.md) · [API Integration](04-api-integration.md) · [Business Rules](05-business-rules.md) · [Navigation](06-navigation.md) · [Test Cases](07-test-cases.md)

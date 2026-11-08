# ST-16 — Kết quả bài kiểm tra · Tổng quan

| Trường | Giá trị |
|---|---|
| Screen ID | `ST-16` |
| Module | Student |
| Route | `/student/attempts/:attemptId/result` — route trong inventory, không phải xác nhận router runtime |
| Actor/role | Theo DD nguồn; xem overview/source trace bên dưới |
| DD status | Draft (package được chuyển đổi); source status: **Trạng thái:** DD BLOCKED; IMPLEMENTATION BLOCKED; RUNTIME NOT VERIFIED. API #32 đang là design contract/draft DD, không có route Student hiện hành. |
| Owner | Không được xác định trong inventory/DD nguồn đã chuyển; `CẦN_XÁC_NHẬN` |
| Version / last updated | 0.1 / 2026-11-08 |
| Nguồn đối chiếu | [ST-16.md](../../screen_stitch/03_student/ST-16_ket-qua-bai-kiem-tra/ST-16.md), [ST-16_PLAN.md](../../screen_stitch/03_student/ST-16_ket-qua-bai-kiem-tra/ST-16_PLAN.md), [ST-16_markers.json](../../screen_stitch/03_student/ST-16_ket-qua-bai-kiem-tra/ST-16_markers.json), [list_screen.md](../../list_screen.md) |

## 1. Mục tiêu & phạm vi
- Mục tiêu: Điểm/trạng thái chấm và feedback nếu được trả; không lộ đáp án ngoài policy.
- In-scope: GET #32 sau accepted #31; pending hiển thị trạng thái, không suy ra score=0; `GRADED` không tự nghĩa là pass; chỉ render field được phép theo response/disclosure policy.
- Out-of-scope: Xem gate bên dưới; không kết luận Study Web route/UI đã wired hoặc runtime đã chạy.

## 2. Use cases chính
| Use case / AC | Actor | Kết quả kỳ vọng theo inventory |
|---|---|---|
| AC-16 | Theo DD nguồn; `CẦN_XÁC_NHẬN` nếu nguồn chưa chốt | Điểm/trạng thái chấm và feedback nếu được trả; không lộ đáp án ngoài policy. |

## 3. Precondition / Entry / Dependencies
- Điều kiện vào, role guard và dependency: xem trích đoạn tổng quan nguồn; không bổ sung giả định.
- API references: #32
- Liên kết màn hình dự kiến: [ST-09](../ST-09-TongQuanKhoaDangHoc/00-overview.md), [ST-20](../ST-20-TongQuanTienDo/00-overview.md)
- Links: [UI](01-ui-elements.md) · [Events](02-events.md) · [Navigation](06-navigation.md)

## 4. UI states
| State | Nguồn | Giá trị |
|---|---|---|
| Inventory states | `list_screen.md` | pending/graded/unavailable/error |
| Current runtime | Worklog/context Study Web | `UNWIRED` / `RUNTIME NOT VERIFIED` |

## 5. Luồng chính và hình ảnh
- Ảnh clean: [screen-clean.png](images/screen-clean.png) (copy từ [ST-16 source screen.png](../../screen_stitch/03_student/ST-16_ket-qua-bai-kiem-tra/screen.png))
- Ảnh numbered: [screen-numbered.png](images/screen-numbered.png) (copy từ [source annotated PNG](../../screen_stitch/03_student/ST-16_ket-qua-bai-kiem-tra/screen_annotated.png))
- Luồng: GET #32 sau accepted #31; pending hiển thị trạng thái, không suy ra score=0; `GRADED` không tự nghĩa là pass; chỉ render field được phép theo response/disclosure policy.
- Priority: P1; Gate/source status: **D; DD BLOCKED; IMPLEMENTATION BLOCKED; RUNTIME NOT VERIFIED:** API #32 Draft Q-32-01…06 còn mở về ownership, pending score, answer/feedback disclosure, shape/order và path/error; Student #32 route/module/test NOT_FOUND; Study Web UNWIRED; legacy BIGINT và V1-PILOT UUID attempt/answer models lệch, adapter/live schema chưa xác minh; PNG loaded Student và HTML unavailable Guest khác nhau, cả hai chưa khớp design target; screenshot fields/CTAs thiếu nguồn

## 6. Open questions / Change log
- `CẦN_XÁC_NHẬN`: các gate/source questions trong inventory và DD nguồn vẫn giữ nguyên; không tự đóng blocker.
- 2026-11-08 — Chuyển nội dung nguồn sang 8-file template; không chỉnh source, không xác minh runtime.

## Trạng thái và ranh giới bằng chứng

# ST-16 — Kết quả bài kiểm tra

> **Trạng thái:** DD BLOCKED; IMPLEMENTATION BLOCKED; RUNTIME NOT VERIFIED. API #32 đang là design contract/draft DD, không có route Student hiện hành.

## Trích đoạn tổng quan từ DD nguồn

### Trích từ DD nguồn: A. Tổng quan màn hình

### A.1. Định danh, mục tiêu và quyền truy cập

| Thuộc tính | Đặc tả |
|---|---|
| Screen ID / tên | ST-16 — Kết quả bài kiểm tra (Page) |
| Mục tiêu | Hiển thị trạng thái chấm và phần kết quả quiz mà Student được phép xem sau khi submit. |
| Actor/Role | Student có quyền đọc attempt; authentication là Student Bearer JWT theo API #32. Quy tắc ownership/masking chưa chốt. |
| Route thiết kế | `/student/attempts/:attemptId/result` |
| Screen trước / liên quan | ST-15 — Xác nhận nộp bài kiểm tra; inventory liệt kê ST-09 và ST-20 là màn hình liên quan. Các CTA trên mockup chưa có destination contract. |
| API thiết kế | #32 `GET /api/v1/attempts/{attempt_id}/result`. |
| Element / event | 38 elements `ST16-EL-01`…`ST16-EL-38`; 6 events `ST16-EV-01`…`ST16-EV-06`. |
| Hiện trạng | Study Web UNWIRED; API #32 route/module/test NOT_FOUND trong current source; API #32 DD `Draft — Needs Confirmation`; không có runtime verification. |

### A.2. Điều kiện vào/ra

- **Điều kiện vào theo F05:** ST-15 đã nhận accepted response từ #31 và điều hướng với `attemptId`. AC-16 yêu cầu Student được phép làm quiz; chính sách cho direct entry/refresh và attempt state khác chưa chốt.
- **Khởi tạo:** đọc `attemptId` từ route, yêu cầu Student context và gọi GET #32. Không gửi `user_id`, answer, score hoặc quyền trong URL/query/body.
- **Đầu vào API #32:** path `attempt_id:int64`, Bearer Student; không có query/body. Response contract là `ApiEnvelope<QuizAttempt>`.
- **Kết quả:** AC-16 đưa cả hai nhánh `GRADED` và `PENDING_GRADE` tới #32. `PENDING_GRADE` phải thể hiện đang chờ chấm; không quy thành score `0`. `GRADED` chỉ nói đã chấm, không tự chứng minh pass.
- **Rời màn hình:** inventory đánh dấu ST-09/ST-20 là màn hình liên quan. Nút “Xem lại đề cương”, “Tiếp tục bài học tiếp theo”, PDF và đích đến cụ thể không có trong route/API contract; phải chờ owner xác nhận.

### A.3. Expected behavior và current behavior

**Expected behavior theo inventory/AC:** Student mở route kết quả sau submit; #32 trả trạng thái/điểm được phép xem. AC-16 nói đọc score + feedback/status ở cả nhánh auto-graded và pending-grade; không lộ đáp án ngoài policy.

**Current behavior theo assets/source:** PNG là loaded-result mockup với badge PASSED, 90%, 18/20, 9/10, GPA A+, 2/3 lần làm, skill metrics, answer key, giải thích/feedback, video, mở khóa bài tiếp theo và PDF. HTML lại là Guest header cùng thông báo “Kết quả chưa sẵn sàng” và link quay về `/student/courses`; script tìm `.review-tab-btn`/`.question-card` nhưng DOM không có các selector đó. HTML không gọi API.

Study Web checkout hiện có docs/assets và ignored `dist` root-only; không có editable source/router/package/Student route. Study Server current source không có Student #32 route/module/test. Hai tài sản là design/prototype evidence, không phải runtime.

**DISCREPANCY:** loaded screenshot khác empty/unavailable HTML; screenshot là actor Student còn HTML có Đăng nhập/Đăng ký; review DOM trong script không tồn tại; không có source nào chứng minh score, pass, skill chart, feedback hoặc CTA đang hoạt động.

### A.4. API #32 contract và giới hạn

| Thuộc tính | API catalog / DD hiện có | Giới hạn cần giữ |
|---|---|---|
| Method/endpoint | `GET /api/v1/attempts/{attempt_id}/result` | Contract design-only; current Student route/module/test không tồn tại. |
| Authentication | Bearer JWT, role Student | Không truyền `user_id`; backend owner predicate chưa chốt. |
| Path | `attempt_id:int64!` | Không có min/max/range/parse mapping cụ thể; catalog không có 400/422. |
| Query/body | Không khai báo | Không thêm query/body/Content-Type. |
| Success | HTTP 200 `DESIGN_RESOURCE_RETRIEVED`; `ApiEnvelope<QuizAttempt>` | Response DD Draft. |
| Errors | 401 `DESIGN_AUTHENTICATION_REQUIRED`; 403 `DESIGN_ACCESS_DENIED`; 404 `DESIGN_RESOURCE_NOT_FOUND`; 500 `DESIGN_INTERNAL_ERROR` | 403-vs-404 cho attempt của user khác chưa chốt; không thêm 409/422. |
| Logical fields | `id`, `quiz_id`, `status`, `started_at`, `submitted_at?`, `score?`, `answers[]`; `QuizAnswer` có `question_id`, `choice_ids?`, `text_answer?`, `correct?`, `score?` | Projection, ordering, nullable/omit rule và field disclosure còn mở. |

API #32 DD `Draft — Needs Confirmation` nêu Q-32-01…06: ownership/masking; availability và score khi `PENDING_GRADE`; tiết lộ correctness/điểm câu; feedback field; answer shape/order; path/error mapping. AC-16 có “feedback” nhưng response schema và candidate tables không có feedback. Không tự thêm field hoặc API khác để lấp khoảng trống.

### A.5. Database candidates and visual-system alignment

**Database contract discrepancy:** API #32 catalog uses an int64 `attempt_id` and the reusable logical `QuizAttempt`/`QuizAnswer` schema. The legacy Study Server DDL has BIGINT `quiz_attempts`/`quiz_answers`, nullable attempt score/submission time, and one selected `choice_id` per answer. The separate V1-PILOT design uses UUID `assessment_attempts`, a required submitted payload snapshot, and immutable `assessment_answers` with selected-option/text fields. These models differ in identifier, lifecycle, and answer shape. Neither DDL artifact establishes a live schema or an approved adapter from V1-PILOT to API #32. Do not choose one, cast IDs, or infer an answer projection in this screen DD; backend ownership must resolve the mapping.

**Design-system discrepancy:** the Study Web target in `.agents/web-study/design.md` calls for ocean tokens, Inter/system typography without remote font dependencies, restrained surfaces, approximately 1120px content width, responsive 768/1024px breakpoints, and controls at least 44px high. The ST-16 PNG instead uses a bright cobalt/green gradient treatment, dense navigation and small text; the companion HTML separately imports Google Plus Jakarta Sans and Material Symbols and Tailwind from CDNs and renders a different Guest/unavailable composition. Neither artifact matches the target consistently or proves a current app implementation. Preserve the supplied assets; resolve which result state is canonical and align a future frontend design before implementation.

### A.6. Bảo mật và dữ liệu

- Chỉ yêu cầu #32 với Student Bearer session theo contract. Không coi tên/avatar trong PNG hoặc trạng thái UI là xác thực.
- Server phải kiểm tra quyền đọc attempt bằng identity đã xác minh. Không nhận `user_id` từ route/query/body. Chính sách owner mismatch 403 hay masked 404 vẫn là blocker.
- Không hiển thị answer key từ `quiz_choices.is_correct`. `QuizAnswer.correct`/`score` chỉ được hiển thị sau khi policy disclosure được duyệt và response thực sự cung cấp field.
- Với `PENDING_GRADE`, không giả lập score, không hiển thị score `0`, không tuyên bố pass/fail. Với `GRADED`, chỉ show score nếu có trong response và policy cho phép; không tự tính pass/GPA từ screenshot.
- Legacy `quiz_attempts`/`quiz_answers` và V1-PILOT `assessment_attempts`/`assessment_answers` đều là design candidates; chúng không chứng minh live schema hoặc API #32 đang truy vấn chúng.

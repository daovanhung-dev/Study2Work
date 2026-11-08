# ST-14 — Làm bài kiểm tra · Tổng quan

| Trường | Giá trị |
|---|---|
| Screen ID | `ST-14` |
| Module | Student |
| Route | `/student/quizzes/:quizId/attempts/:attemptId` — route trong inventory, không phải xác nhận router runtime |
| Actor/role | Theo DD nguồn; xem overview/source trace bên dưới |
| DD status | Draft (package được chuyển đổi); source status: **DD status: BLOCKED. Implementation: BLOCKED. Runtime: NOT VERIFIED.** |
| Owner | Không được xác định trong inventory/DD nguồn đã chuyển; `CẦN_XÁC_NHẬN` |
| Version / last updated | 0.1 / 2026-11-08 |
| Nguồn đối chiếu | [ST-14.md](../../screen_stitch/03_student/ST-14_lam-bai-kiem-tra/ST-14.md), [ST-14_PLAN.md](../../screen_stitch/03_student/ST-14_lam-bai-kiem-tra/ST-14_PLAN.md), [ST-14_markers.json](../../screen_stitch/03_student/ST-14_lam-bai-kiem-tra/ST-14_markers.json), [list_screen.md](../../list_screen.md) |

## 1. Mục tiêu & phạm vi
- Mục tiêu: Điều hướng câu hỏi, đồng hồ nếu server cung cấp, lưu đáp án, đánh dấu câu chưa trả lời.
- In-scope: AC-16: GET #28 → đọc Quiz/rules/questions → eligibility → POST #29 tạo attempt → PUT #30 khi đáp án đổi. Screen owner của #29 chưa thống nhất giữa ST-13 Start và ST-14; route ST-14 đã yêu cầu `attemptId`. Chốt handoff duy nhất, không POST lặp.
- Out-of-scope: Xem gate bên dưới; không kết luận Study Web route/UI đã wired hoặc runtime đã chạy.

## 2. Use cases chính
| Use case / AC | Actor | Kết quả kỳ vọng theo inventory |
|---|---|---|
| AC-16 | Theo DD nguồn; `CẦN_XÁC_NHẬN` nếu nguồn chưa chốt | Điều hướng câu hỏi, đồng hồ nếu server cung cấp, lưu đáp án, đánh dấu câu chưa trả lời. |

## 3. Precondition / Entry / Dependencies
- Điều kiện vào, role guard và dependency: xem trích đoạn tổng quan nguồn; không bổ sung giả định.
- API references: #28, #29, #30
- Liên kết màn hình dự kiến: [ST-15](../ST-15-XacNhanNopBaiKiemTra/00-overview.md)
- Links: [UI](01-ui-elements.md) · [Events](02-events.md) · [Navigation](06-navigation.md)

## 4. UI states
| State | Nguồn | Giá trị |
|---|---|---|
| Inventory states | `list_screen.md` | unsaved/saving/saved/retrying/expired |
| Current runtime | Worklog/context Study Web | `UNWIRED` / `RUNTIME NOT VERIFIED` |

## 5. Luồng chính và hình ảnh
- Ảnh clean: [screen-clean.png](images/screen-clean.png) (copy từ [ST-14 source screen.png](../../screen_stitch/03_student/ST-14_lam-bai-kiem-tra/screen.png))
- Ảnh numbered: [screen-numbered.png](images/screen-numbered.png) (copy từ [source annotated PNG](../../screen_stitch/03_student/ST-14_lam-bai-kiem-tra/screen_annotated.png))
- Luồng: AC-16: GET #28 → đọc Quiz/rules/questions → eligibility → POST #29 tạo attempt → PUT #30 khi đáp án đổi. Screen owner của #29 chưa thống nhất giữa ST-13 Start và ST-14; route ST-14 đã yêu cầu `attemptId`. Chốt handoff duy nhất, không POST lặp.
- Priority: P1; Gate/source status: **D; DD BLOCKED; IMPLEMENTATION BLOCKED; RUNTIME NOT VERIFIED:** #30 answer representation/storage/upsert/ownership/state/response/retry chưa chốt; không có GET attempt/answers để restore; time/progress source thiếu; legacy BIGINT và V1-PILOT UUID/lifecycle khác nhau; PNG/HTML và WebSocket/idempotency claims chưa được xác nhận; Study Web UNWIRED; Student APIs #28–#32 NOT_FOUND

## 6. Open questions / Change log
- `CẦN_XÁC_NHẬN`: các gate/source questions trong inventory và DD nguồn vẫn giữ nguyên; không tự đóng blocker.
- 2026-11-08 — Chuyển nội dung nguồn sang 8-file template; không chỉnh source, không xác minh runtime.

## Trạng thái và ranh giới bằng chứng

# ST-14 — Làm bài kiểm tra

> **DD status: BLOCKED. Implementation: BLOCKED. Runtime: NOT VERIFIED.**
> Đây là thiết kế có truy vết, chưa đủ để triển khai answer autosave/resume mà không suy đoán contract.

## Trích đoạn tổng quan từ DD nguồn

### Trích từ DD nguồn: A. Tổng quan màn hình

### A.1. Định danh, mục tiêu và trạng thái

| Thuộc tính | Đặc tả |
|---|---|
| Screen ID / tên | ST-14 — Làm bài kiểm tra |
| Actor | Student; API #28–#30 yêu cầu Student Bearer JWT theo catalog. |
| Route trong inventory | `/student/quizzes/:quizId/attempts/:attemptId` |
| Mục tiêu | Hiển thị câu hỏi của quiz, cho phép điều hướng/chọn đáp án, lưu đáp án theo contract đã chốt và đưa người học sang bước xác nhận nộp bài. |
| API trong inventory | #28 GET quiz; #29 POST attempt; #30 PUT answers. Tất cả hiện là design contract, không phải runtime endpoint đã xác minh. |
| Màn hình trước/sau | ST-13 → ST-14 → ST-15 → ST-16. Handoff #29 từ ST-13 có mâu thuẫn với dòng ST-14; #31 thuộc luồng xác nhận ở ST-15; #32 thuộc ST-16. |
| Trạng thái | `DD BLOCKED`; `IMPLEMENTATION BLOCKED`; `RUNTIME NOT VERIFIED`. |

### A.2. Điều kiện vào/ra

- **Đầu vào dự kiến:** `quizId:int64` và `attemptId:int64` trên path; Student access token theo contract API. `attemptId` phải bắt nguồn từ attempt đã được #29 tạo thành công, không lấy từ copy/số lần làm mẫu trên ảnh.
- **Trạng thái trước:** theo AC-16, Student có quyền làm quiz, quiz đang mở và attempt ở `IN_PROGRESS`. Predicate eligibility, trạng thái hợp lệ, deadline và cách xử lý attempt hết hạn chưa được API #28/#29/#30 chốt.
- **Đầu ra:** đáp án có thể được lưu bởi #30 sau khi request representation và upsert policy được xác nhận; nút nộp dẫn tới ST-15. Không xem click nộp là trạng thái đã submit.
- **Refresh/direct entry:** inventory không có API đọc attempt/answers. #28 trả Quiz, #29 tạo attempt. Vì vậy chưa có cách contract-backed để nạp lại câu trả lời/tiến độ cho route đã có `attemptId` sau refresh hoặc khi mở deep link.

### A.3. Expected behavior và current behavior

| Chủ đề | Expected / nguồn thiết kế | Current source/runtime |
|---|---|---|
| UI | PNG thể hiện phiên làm quiz, chọn đáp án, điều hướng, câu hỏi grid và trạng thái lưu/kết nối. | HTML companion là fallback “Bài kiểm tra chưa sẵn sàng để làm”, chỉ có hai anchor tĩnh; không có form, input, native button, API, timer hoặc event handler. PNG và HTML không cùng UI state. |
| Web client | Route, auth, API và các state phải đáp ứng inventory/contract sau khi được quyết định. | Study Web chỉ có tài liệu/assets và ignored `dist` chứa route `/`; editable source, router, package manifest và Student screen không có. `UNWIRED`; serving chưa xác minh. |
| API | Catalog liệt kê #28–#30 và AC-16 mô tả attempt/answer flow. | Study Server source không có Student route/module/test #28–#32. API #87–#91 là API quiz dành cho Admin, không phải các endpoint này. Student API runtime `NOT_FOUND` / `DECLARED_NOT_RUNNABLE`. |
| Autosave | Inventory yêu cầu #30 khi đáp án thay đổi; AC-16 gọi bước ghi là upsert AttemptAnswer. | API #30 DD là `Draft — Needs Confirmation`. Request field `answer(s)` không có JSON representation đã chốt; upsert key/concurrency/ownership/state/response cũng còn mở. |
| Attempt handoff | ST-13 phải mở ST-14 với `quizId` và `attemptId` hợp lệ. | ST-13 EV-02 nói POST #29 chạy khi nhấn Start tại ST-13 rồi mới điều hướng. Dòng ST-14/F05 có thể bị đọc thành tạo attempt trong ST-14. `DISCREPANCY`; không gọi #29 hai lần. |
| Timer/progress | Inventory chỉ cho phép timer nếu server cung cấp; tiến độ phản ánh trạng thái câu được xác nhận. | Mockup có hai timer; `14/20` trong khi answered/unanswered là `13/6`, và flag count `1` chưa rõ có thể overlap. Không có nguồn thời gian, công thức progress hoặc projection answers được xác minh. |
| Kết nối | Có thể hiển thị save/network state khi protocol có nguồn. | Claim WebSocket ping 18ms và “Idempotent Autosave hoạt động an toàn” chỉ có trong PNG; không có endpoint/giao thức/runtime evidence. |

### A.4. API contract liên quan

| API | Contract catalog | Request/response và lỗi | Bằng chứng current runtime |
|---|---|---|---|
| #28 | `GET /api/v1/quizzes/{quiz_id}`; Student Bearer; `path{quiz_id:int64!}`; `ApiEnvelope<Quiz>`. | 200 `DESIGN_RESOURCE_RETRIEVED`; 401 `DESIGN_AUTHENTICATION_REQUIRED`; 403 `DESIGN_ACCESS_DENIED`; 404 `DESIGN_RESOURCE_NOT_FOUND`; 500 `DESIGN_INTERNAL_ERROR`. | Không tìm thấy Student route/module/test trong source hiện tại; không có source UI gọi API. |
| #29 | `POST /api/v1/quizzes/{quiz_id}/attempts`; Student Bearer; `path{quiz_id:int64!}`; không body/query; `ApiEnvelope<QuizAttempt>`. AC-16 đặt sau GET #28 và eligibility decision. | 201 `DESIGN_RESOURCE_CREATED`; 401/403/404/422/409/500 với business code tương ứng. | Không có Student endpoint/module/test. ST-13 gắn #29 với Start; ST-14 cũng liệt kê #29 nhưng route đã yêu cầu `attemptId`. Screen owner/handoff chưa được chốt. |
| #30 | `PUT /api/v1/attempts/{attempt_id}/answers`; Student Bearer; `path{attempt_id:int64!}`; catalog ghi `body{question_id:int64!, answer(s):string!}`; `ApiEnvelope<QuizAttempt>`. | 200 `DESIGN_RESOURCE_UPDATED`; 401/403/404/422/500. Catalog không có 409. Exact JSON property, representation, limits và response answers chưa xác nhận. | Không có Student route/module/caller/test hoặc runtime DB write. API DD và DDL chỉ là design evidence. |
| #31/#32 | #31 POST submit, #32 GET result theo inventory/API catalog; nằm ở ST-15/ST-16. | #31 có 200/401/403/404/422/409/500; #32 có 200/401/403/404/500. Không gọi ở ST-14. | Student runtime source không có các endpoint này. |

### A.5. Ràng buộc bảo mật và dữ liệu

- Không lấy identity, quyền, answer, score, attempt ordinal, deadline hay eligibility từ client sample; server phải xác thực Bearer/role/ownership theo contract đã duyệt.
- Không gửi `user_id` trong request #30. API catalog chỉ khai báo `attempt_id`, `question_id`, answer notation; không tự thêm field, header, query, idempotency key hay version.
- Không hiển thị `QuizAnswer.correct` hoặc answer score trước khi policy được duyệt. API #30 DD ghi grading thuộc sau #31; response có các field này vẫn chưa được phép suy diễn.
- `infra/postgres/study-server/DB.sql` là candidate DDL. Không khẳng định live schema, transaction, FK, uniqueness, hoặc persisted answer behavior.
- Schema artifacts còn có hai mô hình không tương thích trực tiếp với contract int64/autosave: legacy `DB.sql` dùng `quiz_answers.choice_id` một choice mỗi row, còn V1-PILOT `infra/postgres/02_study_db.sql` dùng UUID assessments/attempts/answers, yêu cầu `submitted_payload_snapshot` và khai báo answer payload immutable sau submit. Không có mapping được duyệt cho #28–#30 hoặc pre-submit save; cả hai artifact đều không chứng minh live schema.
- UI Design System của Study Web là intended target; ảnh desktop không chứng minh responsive, focus, keyboard/accessibility hoặc runtime UI đã đạt tiêu chí.

# ST-15 — Xác nhận nộp bài kiểm tra · Tổng quan

| Trường | Giá trị |
|---|---|
| Screen ID | `ST-15` |
| Module | Student |
| Route | `/student/attempts/:attemptId/submit` — route trong inventory, không phải xác nhận router runtime |
| Actor/role | Theo DD nguồn; xem overview/source trace bên dưới |
| DD status | Draft (package được chuyển đổi); source status: **Trạng thái:** DD BLOCKED; IMPLEMENTATION BLOCKED; RUNTIME NOT VERIFIED. Đây là DD theo design contract hiện có, chưa phải bằng chứng có route hoặc API đang chạy. |
| Owner | Không được xác định trong inventory/DD nguồn đã chuyển; `CẦN_XÁC_NHẬN` |
| Version / last updated | 0.1 / 2026-11-08 |
| Nguồn đối chiếu | [ST-15.md](../../screen_stitch/03_student/ST-15_xac-nhan-nop-bai-kiem-tra/ST-15.md), [ST-15_PLAN.md](../../screen_stitch/03_student/ST-15_xac-nhan-nop-bai-kiem-tra/ST-15_PLAN.md), [ST-15_markers.json](../../screen_stitch/03_student/ST-15_xac-nhan-nop-bai-kiem-tra/ST-15_markers.json), [list_screen.md](../../list_screen.md) |

## 1. Mục tiêu & phạm vi
- Mục tiêu: Xem số câu chưa làm, xác nhận nộp và khóa chỉnh sửa khi server chấp nhận.
- In-scope: Flush PUT #30 pending trước đúng một POST #31 → ST-16; không gọi #31 sau flush lỗi/không rõ và không retry mù sau 409/timeout; chỉ chuyển tiếp sau accepted response.
- Out-of-scope: Xem gate bên dưới; không kết luận Study Web route/UI đã wired hoặc runtime đã chạy.

## 2. Use cases chính
| Use case / AC | Actor | Kết quả kỳ vọng theo inventory |
|---|---|---|
| AC-16 | Theo DD nguồn; `CẦN_XÁC_NHẬN` nếu nguồn chưa chốt | Xem số câu chưa làm, xác nhận nộp và khóa chỉnh sửa khi server chấp nhận. |

## 3. Precondition / Entry / Dependencies
- Điều kiện vào, role guard và dependency: xem trích đoạn tổng quan nguồn; không bổ sung giả định.
- API references: #30, #31
- Liên kết màn hình dự kiến: [ST-16](../ST-16-KetQuaBaiKiemTra/00-overview.md), [ST-14](../ST-14-LamBaiKiemTra/00-overview.md)
- Links: [UI](01-ui-elements.md) · [Events](02-events.md) · [Navigation](06-navigation.md)

## 4. UI states
| State | Nguồn | Giá trị |
|---|---|---|
| Inventory states | `list_screen.md` | confirm/submitting/submitted/ambiguous-network |
| Current runtime | Worklog/context Study Web | `UNWIRED` / `RUNTIME NOT VERIFIED` |

## 5. Luồng chính và hình ảnh
- Ảnh clean: [screen-clean.png](images/screen-clean.png) (copy từ [ST-15 source screen.png](../../screen_stitch/03_student/ST-15_xac-nhan-nop-bai-kiem-tra/screen.png))
- Ảnh numbered: [screen-numbered.png](images/screen-numbered.png) (copy từ [source annotated PNG](../../screen_stitch/03_student/ST-15_xac-nhan-nop-bai-kiem-tra/screen_annotated.png))
- Luồng: Flush PUT #30 pending trước đúng một POST #31 → ST-16; không gọi #31 sau flush lỗi/không rõ và không retry mù sau 409/timeout; chỉ chuyển tiếp sau accepted response.
- Priority: P1; Gate/source status: **D; DD BLOCKED; IMPLEMENTATION BLOCKED; RUNTIME NOT VERIFIED:** #30 body/queue/upsert/order/outcome/retry và #31 ownership/state/repeat/deadline/concurrency/grading/transaction/response còn mở; ST-14 summary/dirty-queue handoff/direct entry chưa có contract; legacy BIGINT và V1-PILOT UUID/payload/lifecycle khác; PNG/HTML, timer/count/saved/attempt/instant-grading claims không thống nhất; Student #30–#32 route/module/test NOT_FOUND; Study Web UNWIRED; live schema chưa xác minh

## 6. Open questions / Change log
- `CẦN_XÁC_NHẬN`: các gate/source questions trong inventory và DD nguồn vẫn giữ nguyên; không tự đóng blocker.
- 2026-11-08 — Chuyển nội dung nguồn sang 8-file template; không chỉnh source, không xác minh runtime.

## Trạng thái và ranh giới bằng chứng

# ST-15 — Xác nhận nộp bài kiểm tra

> **Trạng thái:** DD BLOCKED; IMPLEMENTATION BLOCKED; RUNTIME NOT VERIFIED. Đây là DD theo design contract hiện có, chưa phải bằng chứng có route hoặc API đang chạy.

## Trích đoạn tổng quan từ DD nguồn

### Trích từ DD nguồn: A. Tổng quan màn hình

### A.1. Định danh, mục tiêu và quyền truy cập

| Thuộc tính | Đặc tả |
|---|---|
| Screen ID / tên | ST-15 — Xác nhận nộp bài kiểm tra (hộp thoại) |
| Mục tiêu | Cho Student xem tóm tắt bài làm và xác nhận trước khi gửi bài; nếu chấp nhận, chuyển sang kết quả ST-16. |
| Actor/Role | Student có quyền trên attempt theo AC-16. Điều kiện ownership/masking 403/404 của API #31 còn mở. |
| Route thiết kế | `/student/attempts/:attemptId/submit` |
| Screen trước / sau | ST-14 — Làm bài kiểm tra / ST-16 — Kết quả bài kiểm tra |
| API liên quan | #30 `PUT /api/v1/attempts/{attempt_id}/answers` để hoàn tất answer đang chờ; #31 `POST /api/v1/attempts/{attempt_id}/submit` để nộp; #32 được ST-16 dùng để đọc kết quả. |
| Element / event | 18 elements `ST15-EL-01`…`ST15-EL-18`; 7 events `ST15-EV-01`…`ST15-EV-07`. |
| Hiện trạng | Study Web UNWIRED; Student API #31 NOT_FOUND trong source scan; API #31 DD là Draft — Needs Confirmation. Không có runtime verification. |

### A.2. Điều kiện vào/ra

- **Điều kiện vào theo thiết kế:** đã có `attemptId:int64` từ ST-14; người dùng có phiên Student hợp lệ; attempt thuộc Student và còn đủ điều kiện nộp theo policy do server xác nhận. Route/state handoff hiện chưa được implement hoặc chốt.
- **Dữ liệu cần có:** summary bài làm, số câu chưa trả lời, cờ đánh dấu, thời gian và các answer write còn pending. ST-14 handoff hiện chỉ nêu `attemptId` và flush pending #30; không có contract truyền summary/dirty queue hoặc endpoint đọc attempt để dựng lại khi refresh/direct entry.
- **Thành công:** chỉ khi #31 trả 200 `DESIGN_RESOURCE_UPDATED` mới coi submit được server chấp nhận và chuyển ST-16. AC-16 cho hai nhánh `PENDING_GRADE` hoặc `GRADED`; không mặc định có điểm ngay.
- **Quay lại:** “Tiếp tục kiểm tra” dự kiến trở về ST-14 với cùng `attemptId`; route/history, phục hồi dirty state và hành vi đóng hộp thoại chưa được xác nhận.
- **Không được suy ra:** các số 18/20, 2 câu chưa làm, câu 15 được đánh dấu, 12:15, 45:20, attempt 2/3, còn một lượt và chấm điểm tức thì đều là nội dung mẫu.

### A.3. Expected behavior và current behavior

**Expected behavior theo inventory/AC:** ST-15 hiển thị xác nhận, có số câu chưa trả lời, chờ các cập nhật #30 đang pending hoàn tất trước khi gửi, sau xác nhận phát một POST #31, ngăn double-submit và xử lý conflict; sau khi server chấp nhận thì sang ST-16. AC-16 đặt attempt thành `SUBMITTED`, tự chấm phần có thể chấm và trả nhánh `PENDING_GRADE` nếu còn câu cần chấm tay, nếu không thì `GRADED`.

**Current behavior theo source/assets:** PNG cho thấy modal xác nhận trên quiz bị làm mờ và header. `code.html` là fallback lỗi khác: thông báo dữ liệu hợp lệ chưa được ghi nhận, không thể nộp, chỉ có nút quay lại. Script HTML tham chiếu `btn-submit-exam` không có trong DOM; nhánh dormant sẽ đổi hash sang route hardcode sau 600 ms nếu có nút. Không có request API trong asset. Không tìm thấy app/router Student hiện hành hoặc route/module/test #31 trong Study Server. Các trạng thái mockup và JavaScript tĩnh không phải runtime behavior.

**DISCREPANCY:** PNG và HTML biểu diễn hai trạng thái khác nhau; timer header và modal khác nhau; ST-14 cũng có snapshot số câu khác. Không có contract nối những giá trị mẫu với nhau.

### A.4. API contract liên quan

| API | Contract thiết kế đã thấy | Điều chưa được xác nhận |
|---|---|---|
| #30 flush answer | `PUT /api/v1/attempts/{attempt_id}/answers`; Student Bearer; path `attempt_id:int64!`; catalog ghi `question_id:int64!`, `answer(s):string!`; 200 `DESIGN_RESOURCE_UPDATED`; 401/403/404/422/500; response `ApiEnvelope<QuizAttempt>`. | Tên/encoding answer; queue ordering; upsert key; ownership/state checks; concurrency; version/idempotency; retry/timeout reconciliation; response projection. Catalog không khai báo 409. |
| #31 submit | `POST /api/v1/attempts/{attempt_id}/submit`; Student Bearer; path `attempt_id:int64!`; không query/body; response `ApiEnvelope<QuizAttempt>`; 200 `DESIGN_RESOURCE_UPDATED`; 401 `DESIGN_AUTHENTICATION_REQUIRED`, 403 `DESIGN_ACCESS_DENIED`, 404 `DESIGN_RESOURCE_NOT_FOUND`, 422 `DESIGN_VALIDATION_ERROR`, 409 conflict code theo catalog, 500 `DESIGN_INTERNAL_ERROR`. | Q-31-01…06: ownership/masking, allowed states/expiry/repeat/concurrency/idempotency/locking, grading formula/manual detection, transaction/rollback, timestamp/response fields/disclosure và error mapping. |
| #32 result | `GET` theo API catalog, được ST-16 dùng để đọc kết quả sau submit. | Việc đọc lại sau timeout hoặc 409 không được #31 DD chốt làm reconciliation; không tự gọi #32 từ ST-15. |

Các API trên là design contract, không phải bằng chứng endpoint đang chạy. Không thêm request body, query parameter, header ngoài Bearer đã nêu, retry policy hoặc cache mutation.

**DISCREPANCY — database candidates:** `infra/postgres/study-server/DB.sql` mô hình hóa legacy `quiz_attempts`/`quiz_answers` bằng BIGSERIAL/BIGINT, `status` mặc định `IN_PROGRESS`, một `choice_id` trên mỗi answer và `is_correct NOT NULL`. `infra/postgres/02_study_db.sql` là DDL V1-PILOT riêng, dùng UUID `assessment_attempts`, yêu cầu `submitted_payload_snapshot` ngay lúc tạo attempt và mô hình hóa `assessment_answers` là immutable với `selected_option_ids`/text fields. V1-PILOT còn mô tả nhánh QUIZ `SUBMITTED → PASSED|FAILED`, khác AC-16 `SUBMITTED → PENDING_GRADE|GRADED`. Chưa có mapping được duyệt từ autosave #30/submit #31 sang các schema này; cả hai chỉ là candidate DDL, không xác nhận live schema.

### A.5. Bảo mật và dữ liệu

- Dùng identity từ phiên Bearer Student; không nhận `user_id`, quyền, score, answer hoặc trạng thái submit từ URL/client payload.
- `attemptId` là path input. Không đưa token, answers hoặc dữ liệu bài làm vào URL/log/analytics.
- Server phải tự kiểm tra ownership, eligibility, quiz-open/deadline và state trước khi chấp nhận submit; các predicate cụ thể đang mở ở API #31.
- Chỉ gửi #31 sau khi pending answer write đã được giải quyết thành công theo contract được phê duyệt. Không báo “đã đồng bộ” chỉ dựa trên local state.
- Không lộ đáp án đúng/điểm hoặc dữ liệu chấm tay trước policy được duyệt. `PENDING_GRADE` không tương đương với điểm cuối cùng.

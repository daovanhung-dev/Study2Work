# ST-13 — Business Rules

## 1. Rule index
| Rule ID (package alias) | Tên / source ID | Áp dụng | Thực thi | Tests |
|---|---|---|---|---|
| `ST-13-BR-001` | Source rules/gates bundle (alias only) | See source DD | Not re-inferred | See source acceptance |

## 2. Rules, security, discrepancy và gate từ source
- Inventory purpose: Tiêu đề, thời hạn và quy định chấm; xác nhận bắt đầu.
- Gate/status (giữ nguyên): **D; DD BLOCKED; IMPLEMENTATION BLOCKED; RUNTIME NOT VERIFIED:** #28/#29 Student route/module/test NOT_FOUND; PNG/HTML mismatch; eligibility, answer exposure, timing, attempt limit/resume/idempotency và CTA destinations open; #29 owner/order/entry route conflicts across ST-13/F05/ST-14; legacy BIGINT Quiz/Attempt differs from V1-PILOT UUID Assessment model; sample history/proctoring/scoring/certificate claims unsupported; Study Web UNWIRED
- BR IDs trong file này chỉ là alias trỏ tới source rule/gate bundles; không thêm business rule. Không khẳng định rule FE/BE mới khi source chưa xác nhận.

### Trích từ DD nguồn: F. Quy tắc, discrepancy, blocker và nghiệm thu

### Quy tắc bảo mật / dữ liệu

- Chỉ Student Bearer JWT theo API #28/#29 catalog; claim, token refresh, session storage và recovery thuộc contract auth chung chưa xác minh ở Study Web.
- Không tin `quizId`, user identity, attempt ordinal, score, câu trả lời hay entitlement do client tự gửi ngoài input được catalog khai báo.
- Không expose `quiz_choices.is_correct` hoặc đáp án đúng trước thời điểm được policy duyệt. Không suy ra “view attempt” cho phép xem đáp án.
- API catalog/API DD và candidate DB design không chứng minh route deployed, live schema, enrollment/authorization predicate hoặc DB commit.
- Không hiển thị chứng nhận, anti-cheat/proctoring, realtime autosave, auto-submit hoặc bảo đảm phục hồi mạng như tính năng đã hoạt động.

### Discrepancy và blocker

| ID | Bằng chứng | Trạng thái | Ảnh hưởng |
|---|---|---|---|
| ST13-B01 | `screen.png` hiển thị full quiz overview; `code.html` là fallback “Thông tin … chưa sẵn sàng”, không có API/handler. | `DISCREPANCY` | Không thể coi hai asset là cùng một UI state hoặc runtime. |
| ST13-B02 | Study Web design status: chỉ docs/assets và ignored root `dist`; editable source/package/Student route thiếu. | `UNWIRED` | Không xác minh auth, route, event, data loading hoặc visual implementation. |
| ST13-B03 | API catalog và API DD #28 tồn tại; current Study route/module/test scan không thấy Student GET #28. | `NOT_FOUND` / `DECLARED_NOT_RUNNABLE` | Metadata/questions không có API runtime source. |
| ST13-B04 | Catalog/API DD #29 và AC-16 khai báo tạo attempt; current Student route/module/test không có POST #29. Admin #87–#91 là API khác. | `NOT_FOUND` / `DECLARED_NOT_RUNNABLE` | Start button chưa có create-attempt runtime. |
| ST13-B05 | AC-16 yêu cầu entitlement/open quiz; API #28 DD Q-28-01..06 và API #29 Q-29-01..05 mở eligibility, status, limit, expiry, resume và 403/409 mapping. | `BLOCKER — product/API decision` | Không thể xác định trạng thái `available/closed`, điều kiện enable Start hoặc response recovery. |
| ST13-B06 | G-09 và API #28 DD để mở duration/answer visibility; QuizChoice schema, question ordering và field serialization chưa hoàn tất. | `BLOCKER — contract` | Không thể xác nhận số liệu/giới hạn/answer projection từ mockup. |
| ST13-B07 | API #29 no request body; idempotency, concurrent create và initial QuizAttempt response còn mở. | `BLOCKER — API lifecycle` | Timeout/double click có nguy cơ ambiguity; không có retry/resume protocol đã duyệt. |
| ST13-B08 | PNG chứa attempt count, history/result, instructor, cover, timer, scoring, proctoring, auto-submit, transcript/certificate claims không có mapping hợp đồng đã xác nhận. | `DESIGN_ONLY / SOURCE_REQUIRED` | Không được chuyển copy mẫu thành logic hoặc dữ liệu runtime. |
| ST13-B09 | CTA ôn bài/xem attempt, support, breadcrumb/header/footer có destination thiếu; HTML link graph khác screenshot. | `UNWIRED / HANDOFF MISSING` | Không thể quyết định điều hướng/dữ liệu truyền. |
| ST13-B10 | `DB.sql` là checked-in candidate schema; quiz foreign keys/status/time fields không xác nhận live schema/constraints. | `NOT VERIFIED` | Không suy luận DB read/write, uniqueness, transaction hoặc concurrency guarantees. |
| ST13-B11 | Legacy `DB.sql` dùng BIGINT `quizzes/quiz_attempts/quiz_choices`; V1-PILOT `02_study_db.sql` dùng UUID `assessments/assessment_attempts`, `quiz_questions.assessment_id` và `quiz_options`. | `DISCREPANCY / LIVE SCHEMA NOT VERIFIED` | Không map `quiz_id:int64`, `QuizAttempt`, eligibility hoặc write behavior vào một mô hình bằng suy đoán. |
| ST13-B12 | ST-13 inventory row đặt POST #29 sau Start; F05 đặt create attempt ở ST-14; ST-14 row lại ghi POST #29 rồi GET #28 và ST-14 DD ghi nhận sequence conflict. ST-14 route hiện yêu cầu `attemptId` trên path. | `DISCREPANCY / OWNER DECISION REQUIRED` | Chốt screen owner, GET/POST order và entry route; nếu chưa có attempt ID thì route ST-14 hiện tại chưa thể là điểm gọi POST #29. Không gọi attempt-create lặp hoặc điều hướng thiếu ID. |

### Tiêu chí nghiệm thu

- [x] ST-13_PLAN được lập trước DD và annotation.
- [x] PNG gốc/HTML giữ nguyên; ghi nhận dimensions, hashes và mismatch.
- [x] 30 marker tuần tự, duy nhất và map một-một tới element IDs trong bảng `C`.
- [x] Ảnh annotate giữ đúng tỉ lệ; marker đã được xem lại để tránh che text/control chính.
- [x] Đặc tả có expected/current separation, API mapping, event input/process/output, state/navigation và các nhánh lỗi theo contract.
- [x] API #28/#29 được đối chiếu với API catalog, AC-16, API DD và current Study route scan; không gán runtime behavior từ DD; #29 screen owner/order discrepancy được ghi rõ.
- [x] Legacy BIGINT và V1-PILOT UUID assessment schema được đối chiếu riêng; không khẳng định live schema hoặc map ID.
- [x] Discrepancy, `NOT_FOUND`, `UNWIRED`, candidate DB và câu hỏi chưa chốt được ghi rõ; không thêm field/API/rule.
- [x] Relative links, hashes, marker bounds/order/mapping, dimensions, tracker inventory và `git diff --check` được kiểm tra tĩnh; không chạy test/runtime.
- [ ] Eligibility/open/deadline/time-source, answer exposure, attempt-limit/resume/idempotency, Quiz/QuizChoice/QuizAttempt response details và UI recovery được owner chốt.
- [ ] Study Web route/UI/API integrations được implement và kiểm tra thực tế.
- [ ] Loaded/closed/error states, history source and CTA destinations được thiết kế/duyệt.

**Kết luận:** artifact DD có source trace và blocker được mô tả, nhưng chưa đủ quyết định để là `DD READY`. `IMPLEMENTATION BLOCKED`; `RUNTIME NOT VERIFIED`.

## 3. Quy tắc chưa xác nhận
- `CẦN_XÁC_NHẬN`: các quyết định/blocker trong inventory và DD nguồn chưa được giải quyết.
- Related IDs/source refs: Không có BR ID nguồn được chuẩn hóa.; xem [API](04-api-integration.md), [Events](02-events.md), [Tests](07-test-cases.md).

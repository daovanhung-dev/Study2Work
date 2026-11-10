# ST-14_PLAN — Làm bài kiểm tra

> Trạng thái: PLAN COMPLETE; DD BLOCKED; IMPLEMENTATION BLOCKED; RUNTIME NOT VERIFIED

## 1. Phạm vi và phân loại

- Phiên này chỉ xử lý **ST-14 — Làm bài kiểm tra**; không bắt đầu Screen ID khác.
- `primary_task_type: docs`; `secondary_task_types: []`; `project_scopes: [web-work, server-study]`.
- Cross-scope dependencies: handoff ST-13 → ST-14 qua `quizId`/`attemptId`; API #28/#29 → #30; AC-16; G-09; tiếp nối ST-15 (#30 flush → #31 submit).
- Inventory: Student; route `/student/quizzes/:quizId/attempts/:attemptId`; AC-16; API #28/#29/#30; next screen ST-15. AC-16 order là GET #28 → eligibility → POST #29 → PUT #30 khi đổi đáp án. Inventory ST-13/ST-14 chưa thống nhất screen owner của #29; route ST-14 yêu cầu `attemptId` khi entry.
- **Không gọi #29 hai lần.** DD phải giữ discrepancy về vị trí sở hữu POST #29 và yêu cầu owner xác định handoff duy nhất trước implementation.
- Study Web hiện chỉ có docs/assets và ignored `dist` với route `/`; không có editable source, package/router hay Student UI có thể kiểm tra. Mọi tương tác dưới đây là yêu cầu thiết kế/contract, không phải hành vi đang chạy.

## 2. Asset baseline và giao diện hiện có

- `screen.png` nguyên trạng, 1600×1468 RGB; SHA-256 `63ab0e25bd3c502d5f2ce699e93df046532a32862aa0256d3bb5bca1cae89cb8`.
- `code.html` nguyên trạng, 6,636 bytes; SHA-256 `0579187c7347daaf9e48118f4422fef7dc719f00345f01b6f2fe1a15669afdfc`.
- Hai asset không cùng state: PNG là quiz đang làm với question 14/20 và lựa chọn A; HTML là fallback “Bài kiểm tra chưa sẵn sàng để làm”, không có form/control/API/timer/handler. Các anchor HTML tới `/student/quizzes/:quizId` là text tĩnh, không chứng minh route đã wire.
- PNG thể hiện 2 đồng hồ (`45:20 còn lại`, `18:39 thời gian`), header `14/20` trong khi summary là 13 đã trả lời + 6 chưa làm + 1 gắn cờ. Flag có thể overlap nhưng không có rule; answered/unanswered và progress vẫn chưa được giải thích. WebSocket ping/idempotent autosave cũng là copy mẫu, không phải state hoặc guarantee runtime.
- Giữ nguyên PNG/HTML. Không tái dựng source UI từ ảnh và không chuyển các số liệu/claim mẫu thành business rule.

## 3. Contract kỳ vọng và giới hạn nguồn

- Inventory/API catalog: #28 `GET /api/v1/quizzes/{quiz_id}` Student Bearer, `ApiEnvelope<Quiz>`, 200/401/403/404/500; #29 `POST /api/v1/quizzes/{quiz_id}/attempts`, không body/query, `ApiEnvelope<QuizAttempt>`, 201/401/403/404/422/409/500; #30 `PUT /api/v1/attempts/{attempt_id}/answers`, body catalog ghi `question_id:int64!`, `answer(s):string!`, `ApiEnvelope<QuizAttempt>`, 200/401/403/404/422/500.
- AC-16 mô tả eligibility, tạo Attempt `IN_PROGRESS`, trả lời, #30 upsert AttemptAnswer, rồi #31 submit và #32 result. Diagram gắn hết lượt/hết hạn với 403/409 nhưng chưa phân API/owner; #30 catalog không khai báo 409.
- API #30 DD Draft/Needs Confirmation: tên property/representation answer, validation, upsert key/cardinality, concurrency/transaction/retry, ownership/state/expiry, response projection và disclosure answer/score đều mở. DDL candidate `quiz_answers` chỉ có `choice_id`, `is_correct NOT NULL`, `score_received`; không có text answer hoặc uniqueness `(attempt_id, question_id)`. DB table design và DDL còn mâu thuẫn nullability; không xác nhận live schema.
- G-09 để mở answer versioning/autosave, idempotency, thời gian/deadline. Không có contract được xác nhận cho flag persistence, resume, websocket, autosubmit hoặc ping.
- Current Study Server không có Student API #28–#32 route/module/test; API admin quiz #87–#91 là phạm vi khác. Không có runtime caller/callee/DB write để mô tả cho #30.
- ST-15 là confirm-submit dialog: inventory yêu cầu flush PUT #30 pending rồi POST #31 một lần; trạng thái nộp/409/ambiguous network chưa chốt. ST-14 không được tự mô tả #31 như endpoint đã chạy.

## 4. Kế hoạch element/marker

Tạo marker tuần tự, duy nhất, cùng ánh xạ một-một trong bảng element của `ST-14.md`. Đặt chấm trong margin/whitespace; không che nhãn hoặc nội dung câu hỏi.

1. Thoát bài thi; 2. thương hiệu Study2Work Exam; 3. đồng hồ header “còn lại”; 4. profile người học.
5. Nút quay lại; 6. tiêu đề quiz; 7. tên kỳ thi/khóa học; 8. badge số lần làm.
9. đồng hồ thời gian trong phần thi; 10. trạng thái “tự động lưu/API #30”; 11. tiến độ câu hỏi; 12. nút nộp bài.
13. chỉ số câu hiện tại/tổng câu; 14. điểm câu; 15. tag chủ đề; 16. nội dung câu hỏi; 17. code snippet.
18–21. Bốn lựa chọn A–D (A đang được chọn trong ảnh mẫu).
22. câu trước; 23. gắn cờ; 24. câu tiếp; 25. chú giải phím tắt.
26. tiêu đề danh sách câu; 27. nhãn phần/chủ đề; 28. nhóm thống kê đã trả lời/chưa làm/gắn cờ; 29. lưới câu 1–20; 30. lọc câu chưa trả lời; 31. thẻ kết nối/autosave; 32. thẻ giảng viên chấm.

Các nhóm lặp (choices và grid) được mô tả rõ phạm vi phần tử con trong DD; marker chỉ nhận diện component/group nhìn thấy, không khẳng định backend persistence.

## 5. Sự kiện và luồng cần đặc tả

1. **ST14-EV-01 — Mở route/khởi tạo:** đọc `quizId`, `attemptId`, kiểm tra cấu trúc path và auth theo contract; xác định attempt handoff. #28 có thể đọc metadata theo inventory; không tự POST #29 từ route. Refresh/direct entry không có API đọc attempt trong inventory nên resume bị chặn.
2. **ST14-EV-02 — Nạp quiz/khôi phục state:** #28 chỉ có Quiz contract; không xác nhận endpoint đọc attempt/answers. Map các field được contract định nghĩa; không dựng lựa chọn đã lưu từ mockup. Xử lý HTTP/business codes đúng catalog, không tự suy nghĩa 403/404/409.
3. **ST14-EV-03 — Chọn/cập nhật đáp án:** capture `attemptId`, `questionId` và lựa chọn hiện tại; validate membership/shape chỉ khi contract chốt; cập nhật local dirty state theo thiết kế; #30 payload không thể triển khai cho đến khi `answer(s)` được định nghĩa. Nếu #30 thất bại, không tuyên bố đã đồng bộ và không tự retry/replay khi idempotency/version protocol chưa có.
4. **ST14-EV-04 — Đổi câu:** previous/next/grid/filter/phím mũi tên cập nhật chỉ số câu cục bộ; không làm mất câu trả lời dirty và không ngụ ý đã persist. Không xác định thứ tự câu hoặc phạm vi filter ngoài dữ liệu được cấp.
5. **ST14-EV-05 — Gắn/bỏ cờ:** UI hiển thị trạng thái cờ nếu có nguồn state; không có API/persistence contract, nên toggle chỉ là hành vi thiết kế cục bộ cho đến khi owner xác nhận.
6. **ST14-EV-06 — Đồng hồ:** chỉ render countdown nếu server trả duration/deadline hoặc contract time source được duyệt; hai số trong PNG mâu thuẫn. Không tự tính deadline từ client clock, tự submit, hay khóa form khi hết giờ.
7. **ST14-EV-07 — Nộp bài:** nút đi tới ST-15 theo inventory. ST-15 chịu trách nhiệm hỏi xác nhận, flush #30 và gọi #31 sau khi có contract; không đánh dấu submitted từ click hoặc gọi #31 tại ST-14.
8. **ST14-EV-08 — Thoát/quay lại:** route đích và cách bảo toàn answer state chưa được xác nhận; cảnh báo dirty-state/confirm-exit chưa có policy. Không lấy anchor fallback làm route proof.
9. **ST14-EV-09 — Phím tắt:** ảnh nêu 1–4 chọn đáp án, mũi tên chuyển câu, P gắn cờ; xử lý chỉ khi focus/IME/accessibility không xung đột và mapping choice/order được server xác nhận. Phím tắt là thiết kế trong mockup, chưa có implementation source.
10. **ST14-EV-10 — Trạng thái mạng:** không nối WebSocket hoặc hiển thị ping/idempotency guarantee nếu chưa có giao thức/nguồn. UI trạng thái online/offline cần contract riêng; current asset HTML không triển khai.

## 6. Trạng thái, block và đầu ra

- Đặc tả state matrix cho `loading`, `ready/in_progress`, `dirty`, `saving`, `saved`, `save_error/retrying` (nếu protocol được chốt), `submitting`, `expired`, `denied`, `not_found`, `network_ambiguous` và `exited`; đánh dấu state nào chỉ là inventory/design, state nào chưa thể quyết định.
- Tạo `ST-14_markers.json`, `ST-14_markers_overlay.svg`, `screen_annotated.png` (overlay renderer scale 2) và `ST-14.md` theo A–F: 32 nhóm element, event input/process/output, API catalog/error mapping, state/navigation, security, acceptance checklist và source links.
- DD phải nêu rõ: #29 trigger/handoff conflict; answer schema/upsert/state/response/privacy open; attempt resume endpoint/data thiếu; PNG/HTML mismatch; time/progress mismatch; unsupported realtime/idempotency; Student UI/API runtime `UNWIRED`/`NOT_FOUND`.
- Không đánh dấu `DD READY` khi event/payload/state/restore không thể lập trình mà không suy đoán. Kết quả dự kiến `DD BLOCKED; IMPLEMENTATION BLOCKED; RUNTIME NOT VERIFIED`.
- Static audit sau khi hoàn tất: asset hashes; marker IDs/số/bounds và one-to-one map; ảnh annotate dimensions/aspect; SVG hợp lệ; relative links; tracker count/pointer; `git diff --check`. Không chạy tests hoặc runtime.

## 7. Nguồn truy vết trong DD

- [Screen inventory, F05, API index, G-09](../../../list_screen.md)
- [Ảnh gốc](./screen.png), [HTML companion](./code.html)
- [ST-13 DD handoff](../ST-13_gioi-thieu-bai-kiem-tra/ST-13.md)
- [API catalog](../../../../../../docs/lists/list_api.md), [AC-16 index](../../../../../../apps/study-server/docs/diagrams/AC_UNICA/00_AC_API_INDEX.md), [AC-16 activity diagram](../../../../../../apps/study-server/docs/diagrams/AC_UNICA/AC_02_STUDENT_LEARNING.drawio)
- API #30 DD: [request](../../../../../../apps/study-server/docs/dd/30_attempts_answers/03_Request.md), [mapping](../../../../../../apps/study-server/docs/dd/30_attempts_answers/05_Data_Mapping.md), [errors](../../../../../../apps/study-server/docs/dd/30_attempts_answers/06_Error.md), [open questions](../../../../../../apps/study-server/docs/dd/30_attempts_answers/OPEN_QUESTIONS.md)
- [Answer table design](../../../../../../apps/study-server/docs/diagrams/DB_UNICA_TABLES.md), [legacy candidate DDL](../../../../../../infra/postgres/study-server/DB.sql), [V1-PILOT schema artifact](../../../../../../infra/postgres/02_study_db.sql)
- [Declared Study routes](../../../../../../.agents/server-study/apis/declared-routes.md), [current router](../../../../../../apps/study-server/app/api/v1.py), [Study Web status](../../../../../../.agents/web-work/study/INDEX.md)
- [ST-15 submit flow](../ST-15_xac-nhan-nop-bai-kiem-tra/), [Study Web design guide](../../../../../../.agents/web-study/design.md)

## 8. Re-audit trước khi chỉnh DD/tracker (2026-11-07)

Đã đối chiếu lại plan này với source hiện tại trước mọi chỉnh sửa DD hoặc tracker trong phiên ST-14. Các kết quả xác định việc cần giữ nguyên marker/assets và làm rõ handoff/schema; không chạy application tests, browser runtime hoặc live database.

- **AC-16 order:** XML trang `AC16` xác nhận GET #28 → đọc Quiz/rule/question set → quyết định eligibility → POST #29 tạo Attempt `IN_PROGRESS` → Student trả lời → PUT #30 UPSERT AttemptAnswer → POST #31. Đây là call order thiết kế. Screen owner của #29 vẫn chưa nhất quán: ST-13 inventory đặt sau explicit Start, ST-14 inventory ghi `POST #29 → GET #28`, trong khi route ST-14 đòi `attemptId` khi vào. F05/ST-13 DD đang giữ câu hỏi owner/entry route mở; không chuyển #29 sang ST-14 hoặc POST lặp nếu chưa có quyết định.
- **API/runtime:** catalog #28–#30 và API DD #28/#29/#30 còn Draft/Needs Confirmation; open questions Q-28-01…06, Q-29-01…05, Q-30-01…06 còn mở. Current Study route scan và Student module/test path scan không tìm thấy Student API #28–#30; route #87–#91 hiện tại là Admin quiz. Study Web hiện có docs, `dist`, `node_modules` và build-info, không có editable `src`, package manifest hoặc router; không có runtime verification.
- **Database evidence:** legacy `DB.sql` dùng BIGSERIAL/BIGINT quiz/attempt/answer IDs; `quiz_answers` chỉ có một `choice_id`, `is_correct NOT NULL`, và không có unique pair `(attempt_id, question_id)`. V1-PILOT `02_study_db.sql` dùng UUID `assessments`/`assessment_attempts`/`assessment_answers`; attempt yêu cầu `submitted_payload_snapshot` và mặc định `SUBMITTED`, answer payload được khai báo immutable sau submit. Hai artifact không cung cấp mapping đã duyệt cho int64 API #28–#30 hay pre-submit autosave; không chứng minh live schema.
- **Asset/static audit:** `screen.png` remains 1600×1468 (SHA-256 `63ab0e25bd3c502d5f2ce699e93df046532a32862aa0256d3bb5bca1cae89cb8`); `code.html` remains 6,636 bytes (SHA-256 `0579187c7347daaf9e48118f4422fef7dc719f00345f01b6f2fe1a15669afdfc`). Annotated PNG is 3200×2936. Marker JSON and transparent SVG each contain 32 sequential labels/IDs, in-bounds, matching 32 DD element rows; visual review confirms margins remain legible. HTML parser finds two static anchors and no form/input/native buttons/event attributes, fetch/XHR, WebSocket or timer calls; PNG is a loaded mockup with a distinct fallback HTML state.
- **Planned document/tracker edits:** revise ST-14 DD only to tighten AC-16/#29 ownership language, record the separate V1-PILOT lifecycle mismatch and mark static checklist items as audited; revise the ST-14 inventory orchestration/gate and F05 handoff summary to preserve AC-16 order and unresolved screen ownership; append this screen's dated checkpoint to `dd_screens/PLAN.md`; finish this session's worklog. Do not change any other Screen ID or API/DD/DDL source.

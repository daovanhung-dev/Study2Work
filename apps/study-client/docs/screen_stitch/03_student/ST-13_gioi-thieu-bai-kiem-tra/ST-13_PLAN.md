# ST-13_PLAN — Giới thiệu bài kiểm tra

> Trạng thái: PLAN COMPLETE; DD BLOCKED; IMPLEMENTATION BLOCKED; RUNTIME NOT VERIFIED

## 1. Phạm vi và phân loại

- Phiên này chỉ xử lý **ST-13 — Giới thiệu bài kiểm tra**; không bắt đầu ST-14 hoặc Screen ID khác.
- `primary_task_type: docs`; `secondary_task_types: []`; `project_scopes: [web-work, server-study]`.
- Cross-scope dependencies: ST-13 → ST-14 qua `quizId`/attempt được tạo; GET API #28 → POST API #29; AC-16; G-09.
- Inventory: Student; route thiết kế `/student/quizzes/:quizId`; AC-16; API #28 là dữ liệu màn hình, POST #29 chỉ sau thao tác Start; screen sau là ST-14.
- Không giả định route, UI handler hay hành vi mạng đang chạy. Study Web hiện không có source/router có thể kiểm chứng trong checkout.

## 2. Asset baseline và giao diện hiện có

- `screen.png` là ảnh nguồn nguyên trạng 1349×1600 RGB; SHA-256 `b9cfdb6704a6d037a25803dfa271f96786b4ff0a708c4caaa30aac29320884f6`.
- `code.html` là HTML tĩnh 8,568 bytes; SHA-256 `7640023e9147dfe7870528bbf9ade3024d3df374473ed2e8cdaa908de85d19d8`.
- Hai asset không đồng nhất: HTML hiển thị fallback “Thông tin bài kiểm tra hiện chưa sẵn sàng” với link quay lại khóa học; PNG hiển thị trang giới thiệu quiz đầy đủ, dữ liệu ví dụ, lịch sử attempt và nhiều tuyên bố về thi/chấm/chứng chỉ. Giữ nguyên cả hai và ghi discrepancy trong DD.
- HTML không có handler/API/router; link là anchor tĩnh tới các path như `/`, `/courses`, `/student/courses`, `/login`, `/register`. Đây không phải bằng chứng các route đó được nối trong Study Web.
- Ảnh chỉ là giao diện thiết kế. Các giá trị “20 câu”, “30 phút”, “80%”, “2/3”, “Attempt 2”, điểm “65% (13/20)”, lịch sử, proctoring, auto-submit, auto-save/realtime webhook, quy tắc trừ điểm, ISO/chứng chỉ và nút xem lại chưa được xác nhận như dữ liệu hay policy runtime.

## 3. Contract kỳ vọng và giới hạn nguồn

- Inventory/F05: GET #28 để đọc metadata/câu hỏi được phép hiển thị; người học xác nhận Start; POST #29 chỉ khi bắt đầu; chuyển sang ST-14 sau khi attempt được tạo.
- API catalog #28: `GET /api/v1/quizzes/{quiz_id}`, Bearer JWT, role Student, path `quiz_id:int64!`, `ApiEnvelope<Quiz>`, 200/401/403/404/500. Catalog và API DD là thiết kế, không chứng minh runtime.
- API #28 DD Draft mô tả logical Quiz gồm `id`, `course_id`, `title`, optional `duration_minutes`, `passing_score`, `questions`. Hình dạng QuizQuestion/QuizChoice, thứ tự lựa chọn, nullable/time serialization, điều kiện mở/quyền và mapping 403/404 còn mở. Student projection không được lộ `is_correct`.
- API catalog #29: `POST /api/v1/quizzes/{quiz_id}/attempts`, Bearer JWT, path `quiz_id:int64!`, không định nghĩa query/body, `ApiEnvelope<QuizAttempt>`, 201/401/403/404/422/409/500. Chỉ gọi sau khi người dùng chủ động xác nhận bắt đầu. Response và điều kiện retry/409 còn Draft.
- AC-16 precondition: Student có quyền làm quiz và quiz đang mở. Diagram đặt bước đọc quiz/rule/question set, quyết định eligibility, rồi tạo attempt; diagram gắn nhánh hết lượt/hết hạn với 403/409 trong khi API #28 catalog không có 409. Không tự phân phối eligibility giữa #28/#29 hoặc ánh xạ lỗi.
- G-09 chặn quy tắc đáp án/duration và các quyết định quiz/attempt khác; policy hiển thị đáp án, deadline, timer/time source, số lượt, resume/idempotency, grading formula và visibility chưa được suy ra.
- Candidate `DB.sql` có quizzes, quiz_questions, quiz_choices, quiz_attempts, quiz_answers; DDL thiết kế không xác minh live schema. Không dùng bảng này để khẳng định attempt count, deadline, timer, score calculation hay status enum.

## 4. Kế hoạch element/marker

Tạo marker map một-một với 30 nhóm element nhìn thấy; nhóm text tĩnh cùng component để marker không che nội dung. Marker theo thứ tự đọc từ đầu trang xuống cuối:

1. Brand/header; 2. search; 3. primary navigation; 4. notification/account controls; 5. breadcrumb;
6. quiz labels; 7. quiz title; 8. instructor card; 9. cover/preview;
10. quiz status/attempt badge; 11. score-goal panel; 12. question-count metric;
13. duration metric; 14. passing-score metric; 15. attempt-count metric;
16. primary Start button; 17. CTA ôn bài; 18. certification/validity note; 19. academic support card;
20. rules heading; 21. proctor/security notice; 22. scoring card; 23. auto-submit card; 24. certificate card;
25. history heading/count; 26. previous-attempt row; 27. review-attempt button;
28. footer brand/description/badges; 29. footer navigation columns; 30. footer copyright/tagline.

Không biến các marker thành khẳng định rằng giá trị, button handler, timer, bảo mật, chứng chỉ hoặc navigation đã được triển khai.

## 5. Sự kiện và luồng cần đặc tả

1. **ST13-EV-01 — Vào route/tải quiz:** đọc `quizId` từ path, yêu cầu Student auth theo catalog, GET #28 theo thiết kế; ghi rõ API/routing chưa wired, path validation và eligibility mapping còn mở; đặc tả UI data/error mapping không vượt contract.
2. **ST13-EV-02 — Bắt đầu làm bài:** chỉ sau click Start và khi prerequisite được server chấp nhận, POST #29 với path `quiz_id`, không body/query theo catalog; phân tích HTTP/business code và response; chỉ điều hướng ST-14 nếu có attempt ID hợp lệ. Attempt 2, chống double-click/idempotency, 409 recovery và resume policy chưa được xác nhận.
3. **ST13-EV-03 — Chọn ôn lại bài giảng:** CTA hiện có trong PNG nhưng route/lesson ID/handoff chưa có contract; không tạo điều hướng mới.
4. **ST13-EV-04 — Xem lại attempt cũ:** PNG có CTA nhưng API/route/cấp quyền và liên kết tới ST-16 chưa được inventory xác nhận cho ST-13; không tự gọi #32 hoặc tự dựng attempt ID.
5. **ST13-EV-05 — Header/footer/support links:** HTML có anchors tĩnh; Study Web router không có trong source hiện tại. Ghi nhận destinations là chưa được xác minh, không coi anchor là navigation runtime.

## 6. Trạng thái, block và tiêu chí đầu ra

- Expected state từ inventory: `loading / closed / available / denied`; các trạng thái lỗi mạng/401/404/500 chỉ đặc tả khi gắn đúng response catalog. Không suy ra closed từ UI copy hay 409 cho API #28.
- Chụp nguyên ảnh gốc không chỉnh sửa; tạo `ST-13_markers.json`, `ST-13_markers_overlay.svg`, `screen_annotated.png` giữ đúng tỉ lệ; tạo `ST-13.md` gồm tổng quan A–F, element 1–30, event inputs/process/results, API mapping, state/navigation, acceptance checklist và source trace.
- BLOCKERS cần giữ: HTML/PNG mismatch; Study Web UNWIRED; API #28/#29 NOT_FOUND ở runtime; eligibility/access/status mapping; duration/deadline/time source; answer exposure/QuizChoice; attempt limit/resume/idempotency/409; sample values/history/proctor/auto-save/auto-submit/scoring/certification chưa có nguồn; CTA destinations chưa chốt; candidate schema khác nhau và live schema chưa xác nhận.
- Chỉ tĩnh kiểm tra hash nguyên bản, kích thước/tỉ lệ, marker sequence/bounds/ánh xạ, links và tracker, cùng `git diff --check`. Không chạy test, browser flow hay runtime.
- Không đánh dấu DD READY khi policy/route/data/event chưa đủ nguồn. Kết quả dự kiến: `DD BLOCKED; IMPLEMENTATION BLOCKED; RUNTIME NOT VERIFIED`.

## 7. Nguồn cần truy vết trong DD

- [Screen inventory, F05, API index, G-09](../../../list_screen.md)
- [Screen source PNG](./screen.png), [HTML](./code.html)
- [API catalog](../../../../../../docs/lists/list_api.md), API rows #28/#29
- [AC-16 API index](../../../../../../apps/study-server/docs/diagrams/AC_UNICA/00_AC_API_INDEX.md), [AC-16 diagram](../../../../../../apps/study-server/docs/diagrams/AC_UNICA/AC_02_STUDENT_LEARNING.drawio)
- [API #28 DD](../../../../../../apps/study-server/docs/dd/28_quizzes_detail/00_Cover.md) and [open questions](../../../../../../apps/study-server/docs/dd/28_quizzes_detail/OPEN_QUESTIONS.md)
- [API #29 DD](../../../../../../apps/study-server/docs/dd/29_quizzes_attempts/00_Cover.md) and [open questions](../../../../../../apps/study-server/docs/dd/29_quizzes_attempts/OPEN_QUESTIONS.md)
- [Current Study router](../../../../../../apps/study-server/app/api/v1.py), [declared route inventory](../../../../../../.agents/server-study/apis/declared-routes.md), [candidate DDL](../../../../../../infra/postgres/study-server/DB.sql)
- [Study Web status](../../../../../../.agents/web-work/study/INDEX.md), [Study Web design guidance](../../../../../../.agents/web-study/design.md), [ST-12 prior screen](../ST-12_tai-lieu-kem-bai-hoc/ST-12.md)

## 8. Re-audit trước khi chỉnh DD/tracker (2026-11-07)

- **Artifact hiện tại:** sáu artifact đã tồn tại trước re-audit. `screen.png` vẫn 1349×1600 RGB, SHA-256 `b9cfdb6704a6d037a25803dfa271f96786b4ff0a708c4caaa30aac29320884f6`; `code.html` 8,568 bytes, SHA-256 `7640023e9147dfe7870528bbf9ade3024d3df374473ed2e8cdaa908de85d19d8`. `screen_annotated.png` là 2698×3200 (2×); marker JSON và SVG cùng có 30 ID. PNG gốc được giữ nguyên.
- **Review trực quan/static:** PNG thể hiện full quiz overview với metric, history và claims mẫu; HTML hiển thị fallback “Thông tin bài kiểm tra hiện chưa sẵn sàng”, có 15 anchor tĩnh và nạp Tailwind từ CDN kèm inline theme config, nhưng không có form/input/button, API request hoặc app event/timer handler. Đây là mismatch asset, không phải hai trạng thái runtime; CDN/config chỉ là prototype styling. Ảnh annotated đã xem trực tiếp; marker 1–30 tuần tự, unique, in-bounds và map 1:1 tới 30 row element; SVG XML hợp lệ, đủ 30 label/circle; vị trí badge không che text/control chính.
- **Expected contract:** API catalog #28 GET `ApiEnvelope<Quiz>` và #29 POST `ApiEnvelope<QuizAttempt>` đều là design-only; API DD #28/#29 còn Draft. AC-16 yêu cầu Student có quyền và quiz đang mở; diagram đi #28 → eligibility decision → #29, nhưng quy tắc eligibility/attempt/expiry/error mapping chưa chốt. `is_correct` không thuộc Student projection.
- **Cross-screen discrepancy cần giữ:** ST-13 inventory row đặt POST #29 sau thao tác Start; F05 rút gọn luồng thành “ST-13 #28 → Start → ST-14 #29”; ST-14 inventory row lại ghi POST #29 rồi GET #28, và ST-14 DD đã đánh dấu owner/sequence discrepancy. Route ST-14 còn yêu cầu `attemptId` trên path, nên nếu #29 thuộc ST-14 thì entry route/handoff chưa khả thi theo route hiện mô tả cho tới khi được quyết định. Không chọn screen owner hoặc thứ tự, không cho phép POST lặp; bổ sung blocker `ST13-B12` cho handoff.
- **Current source:** re-scan `apps/study-server/app/api/v1.py`, module tree và tests không tìm thấy Student API #28/#29; route quiz hiện diện là Admin #87–#91, không phải consumer Student. Study Web hiện chỉ có docs/assets và `tsconfig.tsbuildinfo`; không có editable source, package manifest hay router. Trạng thái vẫn `NOT_FOUND` / `UNWIRED`.
- **Schema discrepancy mới cần đưa vào DD:** legacy candidate `infra/postgres/study-server/DB.sql` dùng `BIGSERIAL/BIGINT quizzes`, `quiz_questions`, `quiz_choices`, `quiz_attempts`. Checked-in V1-PILOT `infra/postgres/02_study_db.sql` dùng versioned UUID `assessments`, `assessment_attempts`, UUID `quiz_questions` gắn `assessment_id`, và `quiz_options`; chưa xác minh live schema. Không map API `quiz_id:int64`/`QuizAttempt` sang một trong hai mô hình bằng suy đoán; thêm blocker `ST13-B11` và cập nhật tracker.
- **Kế hoạch sửa sau re-audit:** cập nhật DD phần current behavior/flow/state và blocker để thể hiện schema hai họ và #29 handoff conflict; cập nhật ST-13 inventory row, F05 note, global-plan row/checkpoint và worklog. Giữ nguyên PNG, HTML, marker JSON/SVG và annotated PNG vì static/visual checks đạt. Không đổi API catalog/DD, ST-14 artifact, source code, schema hoặc runtime.
- **Trạng thái giữ nguyên:** `DD BLOCKED`; `IMPLEMENTATION BLOCKED`; `RUNTIME NOT VERIFIED`. Không chạy application tests, browser runtime hoặc live DB check.

## 9. Kết quả sau DD và static audit (2026-11-07)

- Cập nhật `ST-13.md` phần current behavior, flow, Start event, transition matrix và blocker table: thêm `ST13-B11` cho legacy BIGINT vs V1-PILOT UUID schema; thêm `ST13-B12` cho #29 owner/order/entry-route discrepancy. Không tự chọn API owner, schema, retry hay eligibility policy.
- Cập nhật ST-13 inventory row và F05 để giữ rõ #29 call-site/order mismatch; global tracker row/checkpoint phản ánh blockers và ba status riêng. Không sửa artifact của ST-14.
- Static audit đạt: đủ sáu core artifacts; original image/HTML hash khớp baseline; `screen.png` 1349×1600, `screen_annotated.png` 2698×3200; 30 marker ID tuần tự/unique/in-bounds map đúng 30 DD element rows; SVG XML hợp lệ với 30 label/circle; direct image review không thấy marker che text/control; local Markdown target paths resolve; authored text không có trailing whitespace; `git diff --check` sạch.
- HTML companion hiện có 15 placeholder anchors và styling-only Tailwind CDN/config; không có app request/control/event/timer handler. PNG overview và HTML unavailable fallback vẫn là asset discrepancy.
- Không chạy application tests, browser/runtime hoặc live DB/schema verification. Kết quả: `DD BLOCKED`; `IMPLEMENTATION BLOCKED`; `RUNTIME NOT VERIFIED`. Phiên chỉ xử lý ST-13; ST-14 là phiên riêng.

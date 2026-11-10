# AD-16 PLAN — Tạo/chỉnh sửa bài kiểm tra

## 1. Phạm vi phiên

- Hoàn thiện **chỉ AD-16** theo inventory row 74, AC-35 và goal objective; dừng trước AD-17.
- Tạo screen DD A–F, marker JSON/SVG, `screen_annotated.png`, cập nhật inventory/API reverse index, global plan và worklog.
- Giữ nguyên ảnh `screen.png` và `code.html`. Không sửa Study Web/Study Server source hoặc API DDs.
- UI-only DD chưa có skill canonical trong registry; `createDD-markdown` được đăng ký cho Web/API DD nhưng loại trừ `web-ui-only-dd`.

## 2. Expected behavior và AC-35

- Inventory row 74 định nghĩa AD-16 là builder tạo/chỉnh sửa Quiz, route candidate `/admin/quizzes/new` hoặc `/admin/quizzes/:quizId/edit`, actor Admin, AC-35, API #88/#89, và links AD-15/AD-17. AC-35 yêu cầu Admin có quiz-management permission; sơ đồ biểu diễn GET #87 trước nhánh CREATE #88 hoặc UPDATE #89. AC không định nghĩa body, quy tắc thay thế câu hỏi, attempt policy hay đích sau save.
- Direct catalog #88: `POST /api/v1/admin/quizzes`, Bearer JWT/Admin, body top-level `{config:string!, questions:string!}`, `ApiEnvelope<Quiz>`, 201/401/403/422/500. API #88 DD còn `Draft — Needs Confirmation`.
- Direct catalog #89: `PUT /api/v1/admin/quizzes/{quiz_id}`, Bearer JWT/Admin, path `quiz_id:int64!`, catalog không khai báo body, `ApiEnvelope<Quiz>`, 200/401/403/404/422/500. API #89 DD còn `Draft — Needs Confirmation`.
- Không coi nested JSON, full-replacement, history refusal, course move, locking, field ranges, hoặc route success là contract đã được owner duyệt.

## 3. Current source, asset và discrepancy cần giữ rõ

- Folder ban đầu chỉ có `screen.png` (1600×1402; SHA-256 `d8495b7625c4668957fd54df8a500e71b31e374c99e61895e6d450cdd3f7894f`) và `code.html` (21,782 bytes; SHA-256 `adf60f52ab9e16ad71d90ba14e1deab1d1e4db1a18c5effbd403d3ea356c403d`). Giữ nguyên hai source file.
- Prototype có admin shell/navigation, breadcrumb quay AD-15, tiêu đề “Thiết lập và biên tập bài kiểm tra trắc nghiệm”, Safe Mode notice, config form rỗng, Questions section rỗng, Add Question và Save disabled, Cancel hash link, và footer. Không có `<form>`, handler/validation, fetch/XHR, route, localStorage autosave hoặc data load.
- Config hiện thấy: title input, course select chỉ có placeholder disabled, duration input HTML min=1/max=300, passing score min=0/max=100. Các giới hạn mockup không phải API/business contract. Notice “autosave draft locally”, RBAC/readiness/schema/gate là copy tĩnh.
- Questions Builder hiện không có question/choice editor; Add Question disabled. Do đó UI không thể tạo nested `questions` payload mà local #88/#89 hiện đòi hỏi.
- Study Web checkout có `docs/`, `dist/`, `node_modules/` và build metadata nhưng không có editable `src/`, package manifest, router hoặc API client. AD-16 `UNWIRED`; serving/runtime chưa xác minh.
- Local #88/#89 route/module/query/model/validator/test source tồn tại. Shared `ADMIN` guard được gọi trước parse/DB. #88 local fallback yêu cầu hai outer string; decode nested JSON theo shape DERIVED: `config(course_id:int,title:string,duration_minutes?:int|null,passing_score:string)` và `questions[{text,type,choices[{text,is_correct?}]}]`; enum local gồm `SINGLE_CHOICE|MULTIPLE_CHOICE|TRUE_FALSE`, course phải tồn tại. Tạo Quiz/Question/Choice atomically theo thứ tự request, response Admin có `is_correct`, rồi commit. Nested shape, field/range semantics và physical schema chưa được owner-approved.
- #89 catalog path-only nhưng local route parse body và reuse #88 validation. Local fallback kiểm tra positive int64, khóa quiz/children, trả 404 nếu thiếu/deleted, từ chối update nếu có `quiz_attempts` hoặc `quiz_answers`, khóa course, cập nhật metadata, xóa choices trước questions, thêm replacement set theo thứ tự request và giữ status/created_at. Body/full replacement/history gate/course move/locking đều DERIVED; không có optimistic version. #88/#89 fake DB test reports trong `.agents/server-study/tests.md` là test source đã được xem, không chứng minh DB triển khai.
- Schema source là legacy BIGINT `quizzes`/`quiz_questions`/`quiz_choices`; migration `infra/postgres/study-server/migrations/013_quiz_question_type_and_choice_order.sql` bổ sung `question_type` nullable và `sort_order` cho choices. Migration/DDL không xác minh live deployment. V1-PILOT UUID `assessments/questions/options` không tương thích với ID/API legacy. Admin Quiz response có answer key; Student API #28 phải tiếp tục loại `is_correct`.
- Không có GET Admin Quiz detail. #87 trả metadata-only list với `questions=[]`, vì vậy edit deep link không có nguồn đã xác minh để populate form/Question Builder. AD-15 là entry point; AD-17 là statistics handoff, nhưng save destination/reload policy chưa được chốt.
- Screenshot/prototype dùng full-width cobalt/Plus Jakarta styling; `.agents/web-study/design.md` định nghĩa target ocean-blue, Inter/system, centered/responsive. Ghi là target design, không coi là runtime behavior.

## 4. Event plan

| Event | Trigger | Quy trình cần đặc tả |
|---|---|---|
| EV-01 | Open/create initialization | Candidate route/auth/permission; field defaults rỗng theo ảnh; không load options/API khi chưa có contract; `UNWIRED`. |
| EV-02 | Open/edit initialization | ID từ route cần kiểm tra; không có GET detail, #87 không đủ; giữ blocker và không dựng initial data. |
| EV-03 | Edit title/course/duration/passing score | Ghi input/HTML constraints và local validator phân biệt; không biến constraints thành business rules; dirty/invalid semantics chưa wire. |
| EV-04 | Add question / question builder | Control disabled, handler/editor/choice model vắng; không thể sinh `questions`; mở gate chỉ sau schema/UX được duyệt. |
| EV-05 | Save create (#88) | Button disabled; mô tả direct catalog request riêng local fallback; validation, response/business code, rollback, duplicate-submit/cache/navigation chưa được client thiết kế. |
| EV-06 | Save update (#89) | Button disabled; catalog path-only vs local body discrepancy; edit data/history policy blocker; không khẳng định submit được. |
| EV-07 | Cancel/back to AD-15 | Hash target quan sát được nhưng router không có; dirty confirmation/preservation chưa được thiết kế; không có API. |
| EV-08 | Safe Mode/autosave notices | Copy tĩnh, không có persistence/security implementation; mô tả như informational prototype only. |
| EV-09 | Admin shell/breadcrumb/footer navigation | Anchor destinations `#`/`#/admin/quizzes`; không có route/session handlers để xác nhận điều hướng. |
| EV-10 | Validation/auth/API failure states | Catalog errors và local source fallback tách biệt; map loading/invalid/unauthorized/forbidden/not-found/conflict/service-error làm trạng thái candidate, không claim UI runtime. |

## 5. Marker plan

Tạo 35 marker tuần tự theo thứ tự thị giác từ header xuống footer; tọa độ pixel theo ảnh gốc 1600×1402. Mỗi marker ánh xạ chính xác một dòng §C của DD. Marker đặt trong gutter/whitespace cạnh element, tránh che label/giá trị. Hidden tooltip không có marker riêng.

| ID | Element |
|---:|---|
| 1 | Study2Work brand block |
| 2–6 | Năm Admin navigation links, theo thứ tự trái sang phải |
| 7 | Static System Normal badge |
| 8 | Notifications button |
| 9 | Static Admin identity/avatar |
| 10 | Global breadcrumb trail |
| 11 | Static RBAC verification indicator |
| 12 | Local breadcrumb trail |
| 13 | Return to AD-15 link |
| 14 | Screen title |
| 15 | Safe Mode notice |
| 16 | Config section heading and part label |
| 17 | Quiz title field group |
| 18 | Course selector field group |
| 19 | Duration field group |
| 20 | Passing score field group |
| 21 | Local autosave notice |
| 22 | Questions section heading and part label |
| 23 | Schema notice |
| 24 | Empty-state icon |
| 25 | Empty-state heading |
| 26 | Empty-state description |
| 27 | Disabled Add Question button and temporary-lock badge |
| 28 | Questions Builder Gate notice |
| 29 | Static RBAC/access status strip |
| 30 | Cancel link/button |
| 31 | Disabled Save button |
| 32 | Footer brand/copyright block |
| 33 | Privacy policy link |
| 34 | RBAC standards link |
| 35 | Technical support link |

## 6. Blocker register

- Không có GET detail; #87 metadata list không hydrate câu hỏi, chặn edit prefill.
- #89 catalog không khai báo body, local source bắt buộc body tương tự #88 và thay thế cả Question/Choice set.
- UI thiếu question/choice editor và course option source; Save/Add đang disabled.
- Title/course/duration/score business validation và map sang nested JSON chưa được owner xác nhận.
- AC-35 quiz-management permission vs local shared `ADMIN`; candidate legacy schema/migration chưa xác nhận live; Admin answer-key privacy phải giữ tách khỏi Student #28.
- Autosave, Safe Mode, schema sync, RBAC/readiness, route behavior, dirty-navigation protection, post-save navigation/cache/idempotency chưa có runtime evidence hoặc approved contract.
- API #88/#89 DD Draft; Study Web `UNWIRED`; server fake DB tests không xác minh live PostgreSQL/deployment/locking.

## 7. Work order và checklist

1. [x] Đọc goal objective, root router/context, selector và đúng 3 docs worklogs; thêm handoff AD-15.
2. [x] Đọc project/scope context, AC-35, inventory/API catalog/API DD, server source/tests/schema context, Study Web assets/design.
3. [x] Lưu plan này trước marker JSON/SVG, annotated image hoặc AD-16 DD.
4. [x] Tạo marker JSON/SVG và `screen_annotated.png`; static audit xác nhận source hashes, order, unique IDs, bounds, không overlap, tọa độ và visual legibility.
5. [x] Viết DD A–F với event sequence, field/control table, API variants/errors, states, route handoffs, source citations và blockers.
6. [x] Cập nhật inventory/API reverse index/global checkpoint/worklog; giữ API DDs Draft.
7. [x] Chạy static audit tài liệu/assets/links/counts/whitespace; không chạy application tests/runtime.
8. [x] Chốt AD-16 only, report `DD BLOCKED`, `IMPLEMENTATION BLOCKED`, `RUNTIME NOT VERIFIED`; dừng trước AD-17.

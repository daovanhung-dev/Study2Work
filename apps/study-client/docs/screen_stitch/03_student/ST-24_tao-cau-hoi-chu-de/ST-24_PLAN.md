# ST-24 — Kế hoạch DD màn hình tạo câu hỏi/chủ đề

> Phạm vi phiên: chỉ ST-24. Trạng thái sau rà soát: `DD BLOCKED`; `IMPLEMENTATION BLOCKED`; `RUNTIME NOT VERIFIED` do form/API #40 còn thiếu contract và runtime.

## 1. Mục tiêu và ranh giới

- Hoàn thiện ST-24 theo `apps/study-client/docs/list_screen.md`: `/student/discussions/new`, actor Student, AC-19, API #40 create và #39 list; liên kết ST-23/ST-25.
- Mô tả form trong phạm vi evidence hiện có; không tạo endpoint, request field, validation, persistence, route behavior hoặc transaction chưa được xác nhận.
- Lập kế hoạch trước marker/DD; chỉ xử lý ST-24 trong phiên này.

## 2. Expected behavior

- Inventory ST-24 yêu cầu soạn title/body, chọn course đã ghi danh, lưu và quay về danh sách. Inventory nêu API #40/#39 và states `draft/invalid/submitting/created`.
- F07: ST-23 #39 → ST-24 #40; nhánh reply đi riêng qua ST-25 #42 → #41 → reload #42. Không autosave mutation.
- AC-19: Student phải đăng nhập và có quyền tham gia discussion của course; postcondition topic/comment được tạo, thread cập nhật. Activity diagram có GET #39 trước khi chọn nhánh create/reply và POST #40 cho nhánh tạo.
- Catalog API #40: `POST /api/v1/discussions`, Student Bearer, body `{course_id:int64!, title:string!, content:int64!}`; thành công HTTP 201 `DESIGN_RESOURCE_CREATED`; catalog errors 401 `DESIGN_AUTHENTICATION_REQUIRED`, 403 `DESIGN_ACCESS_DENIED`, 422 `DESIGN_VALIDATION_ERROR`, 500 `DESIGN_INTERNAL_ERROR`; response `ApiEnvelope<Page<Discussion>>`.
- API #40 DD ở trạng thái `Draft — Needs Confirmation`, có 8 open questions. Giữ `content:int64` theo catalog nhưng không biến editor text thành số, không đề xuất encoding; giữ `title` là `SOURCE_REQUIRED` vì DDL không có cột. Enrollment ACTIVE, root/status ACTIVE, timestamp, comments rỗng, author lookup, và page 1/1/1/1 đều là proposals DERIVED chờ xác nhận.

## 3. Current behavior và source trace

- `screen.png` là PNG 1600×1591 dùng được, hash `45517c46e5274de6a835bc5a746069511f65714803295387cc33459c3d2511ab`. Ảnh chứa shell Student, sample semester/status/online-mentor/SLA, hai selector, title+counter, tags và rich-text/Markdown composer. Phần cuối ảnh chỉ thấy editor; không thấy CTA submit/save/cancel.
- `code.html` hash `3311de86bd3e1a6de624cccad1daf709d249d8c9f2ef24d7b79bf9f22693ce35`; khác với PNG: static “form chưa sẵn sàng” empty state, link về `/student/discussions`; không có form controls, API, auth, data binding hay event handler. Giữ nguyên, không dùng để thay thế screenshot.
- Study Web hiện không có editable source/package/router cho `/student/discussions/new`; route trong inventory chưa phải runtime evidence.
- API #40 Draft chỉ là catalog/DD declaration. Search trong `apps/study-server/app/api/v1.py`, `app/modules` và `tests` chỉ thấy Admin #97/#98 discussion routes; không có Student #39–#42 implementation/tests. Admin endpoints không thể đại diện cho Student create flow.
- Checked-in `DB.sql` có candidate `discussions` columns `id`, nullable `course_id`, `user_id`, `parent_id`, required `content TEXT`, `status` default `ACTIVE`, required timestamps không có default; không có `title`. Đây là DDL artifact, không chứng minh live schema.

## 4. Asset/annotation decision

- Giữ nguyên cả `screen.png` và `code.html`; source PNG là thiết kế duy nhất thể hiện form và đủ rõ để annotate. Dùng trực tiếp PNG làm nền `screen_annotated.png`, không render HTML.
- Tạo `ST-24_markers.json`, `ST-24_markers_overlay.svg` và `screen_annotated.png` riêng. Dùng gutter/callout để số marker không che label, input, toolbar hoặc nội dung editor.
- Marker planned: 26 nhóm theo thứ tự đọc từ trên xuống:
  1) brand/logo; 2) primary nav; 3) global search; 4) notification; 5) profile menu;
  6) institutional breadcrumb; 7) semester/enrollment-status strip; 8) page breadcrumb;
-  9) mentor-online badge; 10) hero context-label group (1-on-1 support and code-review focus);
  11) page title; 12) supporting copy; 13) SLA panel;
  14) section 01 header/required note; 15) course selector; 16) module/lesson selector;
  17) topic-title input; 18) displayed title counter;
  19) tag field and selected chips; 20) add-tag entry; 21) suggested-tag text;
  22) section 02 heading; 23) compose tab; 24) preview tab;
  25) formatting toolbar (bold/italic/heading/quote/code/link/lists/image-log/GFM);
  26) editor content area.
- Composite markers are limited to named control groups; DD C must enumerate grouped child controls/actions and their events. Samples, tags, counts, SLA, mentor-online count and editor text are static design content, not API data. Expected submit/cancel/error/loading controls are absent and must not receive fabricated markers.

## 5. Events planned for the DD

1. Enter route and resolve Student/course context; no route/auth runtime currently exists.
2. Choose course; inventory requires an enrolled course, but no options API or access predicate is established for this screen.
3. Choose module/lesson context; displayed by screenshot, absent from API #40 body and has no identified source/field.
4. Edit title; `string` required by catalog. Screenshot counter `74/150` is visual only; max/blank/trim policy is not canonical.
5. Add/remove tags; screenshot behavior is visual only and API #40 has no tags field.
6. Edit body/formatting; toolbar and GFM hint are visible; do not assume renderer, sanitizer, attachments or wire representation.
7. Switch compose/preview; no handler or preview contract exists in current HTML/runtime.
8. Attach image/log; UI control is present, but no upload API, file restrictions or asset-reference mapping is identified.
9. Submit/create; expected API #40 201, but there is no visible submit CTA and request `content:int64` cannot carry the text editor under approved sources. Specify unresolved flow; do not call or implement it.
10. Navigate back to ST-23; screenshot/HTML link target `/student/discussions`; actual route and state/return behavior are not wired.
11. Handle auth, access, field validation, API and network errors; preserve only catalog status/code mappings; messages/retry/rollback behavior remain unspecified.

Each event in DD must state trigger, inputs and provenance, prerequisite, ordered handling, API contract when applicable, output/state transition and exceptions. Unsupported action details remain explicit blockers.

## 6. Open decisions / blockers

- API #40 Q-01…Q-08: content representation; physical title; Page response; course participation predicate; topic status/visibility; server timestamps and transaction; course/user nullability; author and comments projection.
- Missing submit/save/cancel design and resulting success navigation/refresh sequence.
- Course/module option source, enrollment eligibility, and whether lesson/module is contextual UI or persisted data; catalog #40 only accepts course_id/title/content.
- Screenshot-only sample values: course, lesson, Student, semester, eight online mentors, `<45 phút` SLA, title max 150, tag vocabulary and editor content.
- Study Web route/UI and Student #40 runtime/tests are absent. No live DB/schema/deployment evidence.

## 7. Verification plan

- Record original PNG and HTML SHA-256 and verify both remain unchanged; verify output PNG dimensions.
- Validate JSON and SVG; marker numbering `1..26`, unique element IDs and coordinates within both source and annotated canvases; match exactly 26 marker rows in DD C. Visually inspect annotated image for collisions/readability.
- Verify DD sections A–F; eleven events in order with trigger/input/process/output/exception; API #40 fields/statuses match catalog and the eight draft questions remain explicit; local Markdown links resolve; no unapproved API body, content encoding, title source, submit action, validation limit or business rule is introduced.
- Update `dd_screens/PLAN.md` count/pointers based on actual current core artifacts and record blockers/status separately.
- Run `git diff --check`. No tests/API calls/runtime checks; no `.agents` context page/manifest change planned. Run context validator only if a context page/manifest is changed.

## 8. Handoff target

- Status will remain `DD BLOCKED; IMPLEMENTATION BLOCKED; RUNTIME NOT VERIFIED` unless source/contract evidence resolves the blockers above.
- Next Student screen after this separate session: ST-25. Cross-screen contract owners need to resolve API #40 before ST-24 implementation.

## 9. Kết quả thực hiện và kiểm tra

- Giữ nguyên `screen.png` (1600×1591, SHA-256 `45517c46e5274de6a835bc5a746069511f65714803295387cc33459c3d2511ab`) và `code.html` (SHA-256 `3311de86bd3e1a6de624cccad1daf709d249d8c9f2ef24d7b79bf9f22693ce35`).
- Tạo annotation trực tiếp từ PNG gốc; `screen_annotated.png` là 1744×1639, có gutter ngoài ảnh để giữ nguyên nội dung/controls.
- Tạo marker JSON/SVG với 26 số tuần tự, duy nhất, trong bounds; 26 marker khớp chính xác 26 row C của DD. Đã xem ảnh annotated: marker rõ, không che text editor hoặc toolbar; marker cho tabs trỏ vào vùng control nhưng tránh label.
- DD có A–F và 11 event tuần tự, mỗi event ghi trigger, điều kiện, input, xử lý, API boundary khi có, output và ngoại lệ. Local links, JSON/SVG và API #40 body/status references được kiểm tra tĩnh.
- Kiểm kê cuối phiên: 40/83 ID có đủ bốn artifact cốt lõi (`screen_annotated.png`, `<ID>.md`, `<ID>_PLAN.md`, `<ID>_markers.json`); 43 ID còn thiếu ít nhất một file. ME-07 có đủ các file này nhưng plan vẫn `IN PROGRESS`; số đếm chỉ phản ánh sự hiện diện artifact, không xác nhận DD READY. ST-24 đã đủ artifact nhưng vẫn DD/implementation blocked.
- Tests, API calls và runtime không chạy; không có Student #40 route/test. `git diff --check` và kiểm tra whitespace trên các file ST-24/tracker/worklog đạt sau cập nhật cuối.

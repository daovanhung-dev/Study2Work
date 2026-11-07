# ST-25_PLAN — Chi tiết thread và phản hồi

> Phạm vi phiên: chỉ ST-25. Plan được lập sau khi rà soát requirement, screenshot/HTML, AC-19, API #41/#42, route hiện tại và DDL candidate; trước khi tạo marker, ảnh annotated hoặc DD. Trạng thái dự kiến: `DD BLOCKED`; `IMPLEMENTATION BLOCKED`; `RUNTIME NOT VERIFIED`.

## 1. Expected behavior

- Inventory: `/student/discussions/:discussionId`, actor Student, AC-19, API #42 (GET thread) và #41 (POST reply); màn liên quan ST-23. Flow kỳ vọng: GET #42 → người dùng gửi reply qua POST #41 → GET #42 để reload thread. Cần xử lý quyền sở hữu/quyền tham gia và double-send.
- AC-19 precondition: Student đăng nhập và được phép tham gia discussion của course. Postcondition: topic/comment được tạo và thread cập nhật. Activity Diagram nhánh REPLY thực hiện POST #41, node `INSERT Comment + update counters`, rồi GET #42 và hiển thị thread mới nhất.
- API #41 catalog: Student Bearer; `POST /api/v1/discussions/{discussion_id}/comments`; `discussion_id:int64!`; body `{content:int64!}`; success 201 `DESIGN_RESOURCE_CREATED`, response `ApiEnvelope<Page<Discussion>>`; lỗi 401/403/404/422/500 với business code catalog.
- API #42 catalog: Student Bearer; `GET /api/v1/discussions/{discussion_id}`; path `discussion_id:int64!`; response `ApiEnvelope<Page<Discussion>>`; success 200 `DESIGN_RESOURCE_RETRIEVED`; lỗi 401/403/404/500 với business code catalog.
- API DD #41 và #42 đều `Draft — Needs Confirmation`, mỗi DD có 8 open questions. Page semantics, title source, access/status, direct-child model, comment order, body conversion, timestamps, author mapping và counter policy chưa được duyệt.
- Registry không có skill canonical cho Web UI-only DD; không dùng API DD skill/template như contract giao diện.

## 2. Current behavior and source assets

- `screen.png` (573×1600, SHA-256 `36eee9dfb585bec24af84f264fd10f5bb69762ba9a916c17d384ce2cb6e8c903`) là thiết kế populated: Student header, topic + sample tags/metrics/author/body/code/source link; status/course/related-topic/Mentor sidebars; accepted solution, reply, sort và composer.
- `code.html` (SHA-256 `d5498ad73e7621e38fe0da865323f13fd737580d25f1a578fe8890a650e69efc`) là fallback static “Nội dung thảo luận hiện chưa sẵn sàng.”; có Guest login/register header và link về `/student/discussions`, không có topic/thread/reply form, button, API call, auth hoặc data wiring. Không render HTML để thay thế screenshot.
- Giữ nguyên cả hai nguồn; tạo `screen_annotated.png` trực tiếp từ PNG nguồn với gutters ngoài canvas, marker JSON và SVG overlay riêng.
- Current Study Web: editable source/package/router/Student route không có trong checkout; ignored `dist` chỉ có `/`. Screen/UI runtime chưa được xác minh.
- Current Study Server: tìm thấy Admin #97/#98; không tìm thấy Student #41/#42 route/module/query/test. API #98 là `/api/v1/admin/discussions/{discussion_id}`, có ADMIN guard, derive Admin title từ content và đọc mọi direct child status; đó không phải API #42/Student runtime hoặc nguồn chấp thuận cho title/status mapping của Student.
- Checked-in DDL candidate `discussions`: `id BIGSERIAL`, nullable `course_id`, `user_id`, `parent_id`, required `content TEXT`, `status` default ACTIVE, required timestamps không có default; không có `title` hoặc counter. DDL không phải bằng chứng live schema.
- `.agents/web-study/design.md` là visual/accessibility target, không phải UI runtime. Khi triển khai về sau, dùng responsive Study tokens, labels/focus/keyboard states và không dựa vào remote font/dependency từ HTML mockup; không thay đổi nguồn trong phiên DD này.

## 3. Scope and evidence rules

- Expected/current được trình bày riêng; screenshot literal không biến thành API data/defaults.
- Không derive `Discussion.title` từ content; không serialize editor text thành integer; không suy ra sort/like/save/moderation/counter API từ control mockup.
- ACTIVE enrollment/topic/comment, root-only `discussion_id`, direct children, chronological order và one-item Page trong API DD là `DERIVED` proposals. Không xem như runtime/approved behavior.
- `API #41` response có Page<Discussion> nhưng AC-19 tiếp tục yêu cầu GET #42; giữ đúng thứ tự POST rồi GET. Không mô tả response #41 là thay thế reload.
- Các nút `Lưu`, like/vote/reply, course/video, related discussions, mentor booking và copy/source links được ghi theo ảnh; contract/destination không có bằng chứng thì event bị chặn, không gán API/route.

## 4. Planned marker map

40 nhóm visual/control, đánh số theo thứ tự quét từ trên xuống dưới, trái sang phải trong vùng đồng hàng:

1. Brand/logo; 2. primary navigation; 3. global search; 4. notification control; 5. profile menu.
6. semester/enrollment status strip; 7. breadcrumb; 8. back-to-list action; 9. save-thread action.
10. topic tags; 11. view/reply/time metadata; 12. topic title; 13. thread status/details panel.
14. topic author/role card; 15. linked course/module card and lesson action; 16. topic reaction; 17. topic body; 18. related-thread list and “see more”.
19. topic code/copy; 20. Mentor Office Hour CTA; 21. source-link/View-Code card.
22. replies heading/count; 23. sort selector; 24. accepted-solution badge; 25. accepted-reply author/role/votes; 26. accepted-reply text; 27. accepted-reply code/copy; 28. accepted-reply action row.
29. secondary-reply author/votes; 30. secondary-reply text/code; 31. secondary-reply action.
32. composer heading; 33. current-user avatar; 34. formatting toolbar and Markdown hint; 35. reply textarea; 36. discussion rule note; 37. send-reply button.
38. footer brand/description; 39. footer navigation/contact columns; 40. footer certification/legal/meta strip.

Grouped markers must enumerate their child controls/actions in DD section C. Number badges will sit in the outer gutters, with leaders kept outside source pixels; screenshot-only values remain unverified. Absent controls such as loading/error indicators do not receive markers.

## 5. Event coverage planned

1. Enter route/parse `discussionId` and load #42; route and API are not wired.
2. Map #42 success to thread UI, keeping title/metadata/page/comment fields with missing/derived sources explicit.
3. Handle #42 401/403/404/500/network and empty/closed/moderated data without inventing copy or status policy.
4. Return to ST-23; route is inventory/HTML target only, runtime back behavior absent.
5. Save/bookmark topic; no catalog endpoint or persist contract found.
6. Like topic or replies; no reaction endpoint/identity/idempotency contract found.
7. Copy code / open source link; define only visible source controls, no hidden clipboard/external-link behavior without a confirmed handler/URL.
8. Open linked course/material, related discussion or Mentor appointment; destination flows are not source-backed for this screen.
9. Change reply sort; screenshot offers a selector but no approved sort values/API input/order rule exists.
10. Reply to an individual comment; API #41 path may be root or comment ID and nested-reply semantics are unresolved.
11. Enter/edit reply text; body is a string editor while API #41 requires `content:int64`; validation/length/blank rules are open.
12. Use formatting toolbar/Markdown; parser, accepted syntax, sanitization and request representation are unspecified.
13. Submit reply: catalog #41 request/path/auth/response/errors; no Student endpoint exists. Avoid concurrent duplicate sends while pending as the inventory requires double-send handling; retry/idempotency after an ambiguous network result remains blocked.
14. After #41 201, call #42 in order and update rendered thread from #42, not from an unapproved #41 Page projection.
15. Handle session expiry, lost permission, moderated/closed thread, validation, transport and API failures; only catalog status/business-code pairs are fixed.

Every authored event will identify trigger, precondition, data/provenance, ordered handling, API boundary when applicable, output/state and exceptions. Unsupported actions remain blocked/source-required.

## 6. Blockers

- API #41/#42 Draft status and eight open questions each.
- `content:int64` request cannot be reconciled with editor string, reusable comment string or DDL TEXT; no conversion approved.
- Required `Discussion.title` is absent from physical DDL/ERD; comments/author/profile and page projection have unresolved fields.
- AC-19 “update counters” has no physical counter target or response field.
- Course access, topic/comment visibility/status, nested/direct reply, comment ordering and missing/inaccessible resource semantics are unresolved.
- The populated PNG and unavailable-state HTML differ; sample thread/status/votes/course/mentor data and screenshot-only actions lack APIs/contracts.
- Study Web route/component and Student #41/#42 implementation/tests are absent; live schema/deployment is not verified.

## 7. Verification plan

- Verify source screenshot and HTML hashes remain unchanged; check source and annotated PNG dimensions.
- Validate marker JSON and SVG, 1–40 ordering/unique element IDs/bounds, and exact 1:1 mapping to section C; visually inspect callout overlap/readability.
- Check DD sections A–F, every marker row, sequential events and required trigger/condition/input/processing/API/output/exception coverage; verify #41/#42 catalog fields/statuses and open-question boundaries.
- Check local Markdown links, source-backed versus derived labels, ST-23/ST-24 handoff order and global tracker count/pointers.
- Run `git diff --check` plus a whitespace audit on authored files. Do not run API tests or runtime/browser probes for this docs-only task.

## 8. Handoff

- Planned status remains `DD BLOCKED; IMPLEMENTATION BLOCKED; RUNTIME NOT VERIFIED` until API, screen states/actions and Study Web source are aligned.
- After this separate ST-25 session, next Student screen is ST-26.

## 9. Kết quả thực hiện và kiểm tra

- Giữ nguyên `screen.png` (SHA-256 `36eee9dfb585bec24af84f264fd10f5bb69762ba9a916c17d384ce2cb6e8c903`) và `code.html` (SHA-256 `d5498ad73e7621e38fe0da865323f13fd737580d25f1a578fe8890a650e69efc`).
- `screen_annotated.png` là 797×1648, giữ screenshot 573×1600 pixel-exact tại offset (112,24); ImageMagick absolute-error crop comparison `AE=0`. Gutter callouts không phủ nội dung nguồn; ảnh đã xem trực quan.
- Tạo 40 marker sequential/unique trong `ST-25_markers.json` và transparent `ST-25_markers_overlay.svg`; tất cả tọa độ trong bounds, 40 marker khớp chính xác 40 element row trong section C.
- DD hoàn tất A–F, có 18 event sequential; mỗi event mô tả trigger/condition/input/processing/API/output/exception. GET #42 load → POST #41 → GET #42 reload được giữ theo AC-19; nội dung/route/API gaps đánh dấu rõ.
- Local Markdown links, PNG dimensions/source hashes, JSON/SVG parse, marker bounds/order, DD rows/events và API #41/#42 catalog/open-question references static audit đạt. Global tracker hiện 42/83 bộ bốn core artifacts, 41 ID thiếu ít nhất một; số file không đồng nghĩa DD READY.
- Không chạy Student/API tests, API calls, browser hoặc runtime; không sửa context pages.

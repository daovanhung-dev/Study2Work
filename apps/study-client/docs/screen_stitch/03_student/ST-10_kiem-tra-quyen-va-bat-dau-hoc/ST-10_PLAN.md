# ST-10 — Kế hoạch chi tiết

> Rà soát ban đầu: 2026-11-06 · Tái kiểm toán: 2026-11-07
> Trạng thái: PLAN COMPLETE; DD BLOCKED; IMPLEMENTATION BLOCKED; RUNTIME NOT VERIFIED

## 1. Phạm vi và phân loại

- Phiên này chỉ xử lý **ST-10 — Kiểm tra quyền và bắt đầu học (Transition)**; không bắt đầu ST-11 hoặc Screen ID khác.
- Phân loại: primary_task_type docs; secondary_task_types []; project_scopes [web-work, server-study]; cross_scope_dependencies [ST-09 lesson selection/lessonId; AC-14 access/start flow; APIs #22/#23/#24; ST-11 content player; Study Web source/runtime boundary].
- Inventory: route dự kiến /student/lessons/:lessonId/start, actor Student, AC-14, APIs #22/#23/#24; liên kết ST-09 và ST-11. Expected sequence: GET #22; nếu allowed thì POST #23, chống gửi lặp; GET #24; chuyển ST-11. Denied thì không gọi #24 và không phát media.
- AC-14 yêu cầu Student đã enrolled vào course chứa lesson; AC-15 yêu cầu quyền xem lesson. API catalog/DD #22–#24 đều yêu cầu Bearer JWT Student, path lesson_id:int64!, không khai báo query/body. Đây là expected design, không phải runtime.
- Registry .agents/context-manifest.json xác nhận createDD-markdown dành cho Web/API DD và loại trừ web-ui-only-dd; không có skill canonical cho UI-only screen DD. Không áp dụng API DD template làm screen contract.

## 2. Asset baseline và annotation plan

- ST-10 folder trước khi xử lý chỉ có screen.png và code.html; chưa có plan, DD, marker map hoặc annotated image.
- screen.png là ảnh hoàn chỉnh, đọc được, 1566×1600, SHA-256 5d1386bbeba8a21d2ee48cc4b62099cdd6fab3a0d3e0d96b2bc24f3133e840ce. Sử dụng trực tiếp làm ảnh nền chú thích; không cần render thay thế.
- code.html SHA-256 87178684dcd4dd6f4ca47fa3ed26ff63823616d84ca402015aa72a190d431b87. HTML tĩnh, không có router/fetch/handler sản phẩm; mọi anchor href=#; nút Bắt đầu học có disabled và aria-disabled=true; không có lessonId binding.
- Plan 21 marker theo nhóm nhìn thấy: (1) brand; (2) primary nav; (3) student identity; (4) breadcrumb/course/ST-10; (5) Entitlement Gate: Active pill; (6) shield/hand-off/main heading; (7) SECURITY_GATE_ENFORCED badge; (8) gate progress/status 423 panel; (9) protected lesson/player placeholder; (10) session-token restriction pill; (11) technical security contract callout; (12) return-to-ST-09 link; (13) disabled start-to-ST-11 button; (14) FSM heading/description/badge; (15) checking card; (16) denied card; (17) started card; (18) API status card; (19) integration/security notice; (20) footer copyright/WCAG badge; (21) footer terms/privacy/help links.
- Giữ nguyên screen.png và code.html. Annotated image đặt marker/callout ở gutter, không che nội dung.

## 3. Expected behavior và current evidence

| Chủ đề | Expected/design source | Current evidence | Tác động |
|---|---|---|---|
| Entry/course selection | ST-09 chọn một lesson và truyền lessonId sang ST-10. | ST-09 asset không có lesson list/lessonId; CTA chỉ là href=#. | Không có source-backed đầu vào lessonId hoặc route binding. |
| Auth/access | Student session; #22 kiểm tra enrollment/prerequisite; denied thì không gọi #24/media. | APIs #22–#24 không có current route/module/query/test source; client route/session source absent. | Gate chỉ là copy/UI, không phải security boundary. |
| Start | Allowed thì POST #23, chống submit lặp, rồi GET #24. | #23 Draft; AC ghi UPSERT lesson_progress=IN_PROGRESS/201, nhưng key/update/repeated-start/idempotency và response projection còn mở. | Không thiết kế retry/dedup semantics bằng suy đoán. |
| Lesson content | #24 trả Lesson sau access/publish checks; success đi ST-11. | #24 Draft/không wired; access predicate, publish filter, response projection/nullability còn mở. | Không thể khẳng định video/content được bảo vệ; API #09 public hiện trả content/video_url không auth/enrollment check. |
| Screen FSM | Expected checking/denied/started/failure từ inventory; AC14 order. | Asset hiển thị checking/denied/started static labels; button bị disable vĩnh viễn; status 423_LOCKED và “Session Token” không thuộc API catalog. | Ghi discrepancy; không tuyên bố API trả 423, cấp token hoặc media grant. |
| Navigation | Denied dừng ở ST-10; success tới /student/lessons/:lessonId (ST-11); return ST-09. | Anchor href=#; không có router/API event. | Navigation chỉ là ý đồ. |
| Backend/API schemas | Catalog #22/#23/#24; API DD Draft. | #22/#23/#24 không có Student route/module/query/test; chỉ thấy current Admin lesson routes khác path/role. | API declaration không chứng minh availability hoặc authorization. |
| Database | DB design mô tả enrollments và lesson_progress; candidate fields có status/last_accessed_at/progress. | Checked-in DB.sql có candidate tables; live schema chưa xác minh; lesson_progress không có unique(user_id,lesson_id) trong DDL candidate. | Không chốt access query/upsert conflict key hoặc transaction từ DDL này. |

## 4. Planned event coverage

1. ST10-EV-01 route entry, lessonId parse/context input; missing upstream handoff.
2. ST10-EV-02 Student session/auth guard; current client guard absent.
3. ST10-EV-03 GET #22 access check; declared 200/401/403/404/500, response/access decision mismatch and open 403 reason.
4. ST10-EV-04 denied/failure branch; block #23/#24/media on denied, with no defined UI mapping/retry.
5. ST10-EV-05 POST #23 start after allowed; declared 201/401/403/404/422/500; idempotency/repeated-upsert/response open.
6. ST10-EV-06 GET #24 lesson content after approved access/start sequence; declared 200/401/403/404/500; direct-call authorization/publish/projection open.
7. ST10-EV-07 successful handoff to ST-11; current button is disabled and has no handler.
8. ST10-EV-08 return link to ST-09; placeholder anchor.
9. ST10-EV-09 header navigation; all current destinations are placeholder anchors.
10. ST10-EV-10 footer legal/help navigation; destination contracts absent.
- Static status badges, progress illustration, gate/policy copy, FSM card labels and icons do not create API events by themselves.

## 5. Planned source trace

- Recheck ST-10 row/F04, AC-14 and AC-15 API index/diagram, list_api #22–#24, each API Draft and open questions.
- Search current Study Server router, modules and tests for the three Student endpoints; distinguish Admin #83/#84 lesson-detail routes from Student APIs.
- Inspect checked-in DB candidate only for what it actually declares; preserve live-schema uncertainty and missing unique key.
- Compare source PNG/HTML, extract visible content/controls/anchors, preserve hashes and visual state.
- Trace ST-09 lessonId input and ST-11 expected destination; no other Screen ID is to be authored this session.
- No test suites or runtime API calls are requested; do not run them.

## 6. Acceptance, blockers and outputs

- Create ST-10.md, ST-10_markers.json, ST-10_markers_overlay.svg, screen_annotated.png after this plan. Preserve original image/HTML.
- DD must cover every visible marker, expected/current handoff, all 10 events, API method/route/auth/path/response/errors/status, state matrix, navigation and security implications.
- Keep status panel/API/business-code discrepancies explicit: 423_LOCKED is not catalogued; #22–#24 are Draft and absent from current source; #22 ApiEnvelope<Lesson> lacks allow/reason field; #23 repeated POST/upsert behavior unresolved; #24 access/publish/content projection unresolved.
- DD is expected to remain BLOCKED until access predicate/JWT mapping, 403 reason shape, 404/422 semantics, #23 unique key/update/idempotency/transaction, #24 authorization/publish/projection/null rules, loaded/error UI and ST-09 lessonId handoff are approved/source-backed.
- Update global tracker to separate DD/implementation/runtime status and increment artifact bundle count only after static audit. Next pointer after this session: ST-11.
- No context page change is planned unless source audit reveals an inaccurate registered page. If a context page changes, update it with evidence and run node scripts/validate-agent-context.mjs.

## 8. Tái kiểm toán và kế hoạch chỉnh lý (2026-11-07)

### Kết quả đối chiếu nguồn

- AC-14 diagram xác nhận thứ tự `GET #22 access → quyết định enrollment/prerequisite → POST #23 → UPSERT lesson progress = IN_PROGRESS → GET #24 → đọc Lesson/content`. Nhánh deny/error tại bước access ghi `403 + lý do`; vị trí/schema reason chưa được định nghĩa. AC-15 đặt kiểm tra access và publish status trước khi đọc lesson/content.
- Catalog #22–#24 khai báo Student Bearer JWT, path `lesson_id:int64!`, không query/body. #22: `GET /api/v1/lessons/{lesson_id}/access`, `ApiEnvelope<Lesson>`, 200/401/403/404/500; #23: `POST /api/v1/lessons/{lesson_id}/start`, `ApiEnvelope<Lesson>`, 201/401/403/404/422/500; #24: `GET /api/v1/lessons/{lesson_id}`, `ApiEnvelope<Lesson>`, 200/401/403/404/500. Ba API DD đều `Draft — Needs Confirmation`; open questions giữ access/JWT/reason/404, start upsert/idempotency/transaction/response và #24 entitlement/publish/projection/null/path chưa chốt.
- Tái tìm trong router, app modules và test modules xác nhận không có Student route/module/query/test #22–#24. Router chỉ có các Admin lesson endpoints #82–#86 với path/role/use case khác; không dùng thay thế. Không chạy application tests.
- API #09 hiện có route/module/query/test source public: query chỉ lấy course và lesson `PUBLISHED`, trả `content` và `video_url` cùng Lesson fields; endpoint không nhận JWT/enrollment context. Đây là current behavior riêng, không chứng minh quyền học/media cho ST-10 và làm tăng yêu cầu phải có gate phía server được duyệt.
- Có hai DDL Study trong checkout, cả hai chưa xác nhận live. Legacy `infra/postgres/study-server/DB.sql` dùng BIGINT `lesson_progress(user_id, lesson_id, status, progress_percent, last_accessed_at, completed_at)` và không khai báo unique `(user_id, lesson_id)`. V1-PILOT `infra/postgres/02_study_db.sql` dùng UUID `lesson_progress_facts(enrollment_id, lesson_id, status, first_started_at, completed_at)` với unique `(enrollment_id, lesson_id)`. Không gộp hai mô hình hoặc suy ra API #23 upsert key/schema; cần xác nhận schema áp dụng và mapping.
- ST-09 hiện không có lesson selector/lessonId handoff; ST-11 route kỳ vọng `/student/lessons/:lessonId` và cũng liệt kê #24 khi vào player, nên request ownership/duplicate read vẫn cần quyết định. Study Web không có tracked editable source/package; ignored `dist` chỉ có root `/`, không chứng minh route/deployment.
- Assets nguồn vẫn nguyên trạng: `screen.png` 1566×1600 SHA-256 `5d1386bbeba8a21d2ee48cc4b62099cdd6fab3a0d3e0d96b2bc24f3133e840ce`; `code.html` SHA-256 `87178684dcd4dd6f4ca47fa3ed26ff63823616d84ca402015aa72a190d431b87`. HTML là static mockup, anchors `href="#"`, nút Start bị disabled; các copy `423_LOCKED`, Session Token, media release và “khóa vĩnh viễn” không có trong API contract.

### Kế hoạch chỉnh lý trước khi DD/marker edit

1. Sắp xếp DD theo sáu phần rõ `A–F`; giữ riêng expected behavior, current source, Draft contract, unresolved decisions và ba status `DD BLOCKED / IMPLEMENTATION BLOCKED / RUNTIME NOT VERIFIED`.
2. Giữ 21 element và 10 event; diễn đạt đúng response/error/status catalog, access/start/content sequence, #22 `Lesson` response không có `allowed` field, #23 `201` vs AC-14 UPSERT, API #24 direct-call authorization và ST-10/ST-11 duplicate #24 ownership. Không tạo reason/status/token/retry/cache/payload mới.
3. Bổ sung discrepancy giữa legacy BIGINT DDL và V1-PILOT UUID DDL vào phần dữ liệu/blockers; bỏ mọi hàm ý rằng một DDL đã được chọn làm live schema.
4. Kiểm tra lại marker JSON/SVG leader endpoints, target mapping và ảnh annotated. Chỉ sửa marker/ảnh nếu lỗi alignment được xác minh; giữ nguyên source PNG/HTML.
5. Cập nhật duy nhất ST-10 trong `list_screen.md` và `dd_screens/PLAN.md`, đếm bundle từ inventory hiện tại thay vì kế thừa checkpoint lịch sử; next pointer vẫn là ST-11 ở phiên riêng.
6. Cập nhật worklog sau source audit và sau static verification. Chạy static checks cho JSON/XML, ảnh/hash/dimensions, link nội bộ, A–F, marker ↔ element rows, event IDs, inventory/bundle count và `git diff --check`; không chạy application tests/runtime.

### Kết quả phiên ST-10

- Đã lưu kế hoạch tái kiểm toán trước khi sửa screen DD; cập nhật `ST-10.md` theo các phần A–F và làm rõ current source, Draft contract, API #09 public projection, hai DDL khác nhau, blocker và trạng thái. Giữ nguyên 21 elements, 10 events và ba trạng thái `DD BLOCKED`, `IMPLEMENTATION BLOCKED`, `RUNTIME NOT VERIFIED`.
- Không sửa marker map/SVG/ảnh vì kiểm tra mapping đạt: 21 marker tuần tự, 21 element rows, 21 SVG number/circle/leader; tọa độ target theo scale/offset, circle/label/leader endpoints khớp JSON; embedded PNG hash trùng nguồn. Annotation được xem lại; marker đặt ở gutter, không che nội dung.
- Giữ nguyên `screen.png` và `code.html`; SHA-256 không đổi. Ảnh nguồn 1566×1600; annotated 3372×3200. JSON/XML parse, liên kết Markdown cục bộ, A–F, 10 event IDs và `git diff --check` đạt.
- Inventory có 83 folders/IDs; 82/83 có đủ bốn artifacts cốt lõi, thiếu duy nhất ST-01. Đã cập nhật ST-10 ở `list_screen.md` và global plan; ST-11 là màn hình kế tiếp cho một phiên riêng.
- Không chạy application tests, runtime hoặc kiểm tra live database. Các blockers nghiệp vụ/API/client vẫn giữ nguyên; không đánh dấu DD READY hoặc RUNTIME VERIFIED.


## 7. Kết quả tạo artifacts (mốc lịch sử 2026-11-06)

- Đã tạo `ST-10.md`, `ST-10_markers.json`, `ST-10_markers_overlay.svg` và `screen_annotated.png`; giữ nguyên `screen.png` và `code.html`.
- Đối chiếu tĩnh đạt: 21 marker tuần tự/duy nhất, 21 element row khớp ID, 10 event, 21 SVG circles; annotated PNG 3372×3200 và nguồn 1566×1600. Hash PNG/HTML giữ nguyên theo baseline ở trên.
- Liên kết Markdown nội bộ đã kiểm tra; DD vẫn **BLOCKED** theo open contract, không phải vì thiếu artifact. Không chạy test hoặc runtime.
- Ở checkpoint lúc tạo artifacts, tracker ghi ST-10 `DD BLOCKED; IMPLEMENTATION BLOCKED; RUNTIME NOT VERIFIED` và 19/83 bundle đầy đủ. Con số này là snapshot lịch sử đã được checkpoint sau đó supersede; xem kết quả inventory hiện tại tại mục 8.

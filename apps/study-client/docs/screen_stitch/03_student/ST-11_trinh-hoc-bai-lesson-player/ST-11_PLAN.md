# ST-11 — Kế hoạch chi tiết

> Ngày rà soát: 2026-11-06<br>
> Trạng thái: PLAN COMPLETE; DD BLOCKED; IMPLEMENTATION BLOCKED; RUNTIME NOT VERIFIED

## 1. Phạm vi và phân loại

- Phiên này chỉ xử lý **ST-11 — Trình học bài / lesson player**; không bắt đầu ST-12 hoặc Screen ID khác.
- `primary_task_type: docs`; `secondary_task_types: []`; `project_scopes: [web-work, server-study]`; dependency chính: ST-10 → lessonId → ST-11, APIs #24–#27; resource handoff ST-12; progress/quiz/assignment destinations ST-09/ST-13/ST-17.
- Inventory: route `/student/lessons/:lessonId`; actor Student; AC-14/AC-15; APIs #24 (GET lesson), #25 (PATCH progress), #26 (GET lesson resources), #27 (GET next lesson). Expected flow: GET #24; GET #26 lazy; PATCH #25 khi có progress event hợp lệ; GET #27 sau completion. States inventory: loading/playing/paused/progress-saving/finished. Inventory blocker: throttle progress và autosave policy chưa chốt.
- Skill registry xác nhận `createDD-markdown` loại trừ `web-ui-only-dd`; không có skill canonical cho UI-only Screen DD. Không dùng API DD template làm UI contract.

## 2. Asset baseline và giao diện hiện có

- Trước plan, ST-11 chỉ có `screen.png` (1280×1024; SHA-256 `a7548e9f2523f9b6f4b8b71f986a1a199eb36e0654ed5bafdd454ccc8d37de33`) và `code.html` (7,033 bytes; SHA-256 `237ab57e4700a87b98e387f8a99554f4524ff7b6467d79a58b7f8d4e2c1d80e4`). Giữ nguyên hai file.
- Screenshot và HTML thể hiện cùng fallback tĩnh: header Study2Work, nút “Quay lại khóa học của tôi”, breadcrumb, card giữa trang với icon `play_lesson`, heading “Bài học”, thông báo “Nội dung bài học hiện chưa sẵn sàng.”, mô tả và CTA quay về khóa học của tôi, footer brand + ba liên kết.
- HTML có 7 anchors: href `/student/courses` (5), `/student` (1), `/student/progress` (1); không có `<video>`, `<audio>`, `<iframe>`, `<source>`, `<form>`, `<input>`, `<canvas>`, `<button>` hoặc inline event handler. Script chỉ nạp Tailwind CDN/config; không có API/client logic.
- UI asset là unavailable-content fallback, không phải loaded player. Không dựng marker cho media controls, progress bar, chapter/resource list, completion control hoặc Next CTA không có trong ảnh.

## 3. Expected behavior và source trace

| Chủ đề | Expected/design source | Current source | Tác động |
|---|---|---|---|
| Route/session | Student mở `/student/lessons/:lessonId`; path IDs theo catalog #24–#27 là required int64 và APIs khai báo Bearer JWT/Student. | Study Web editable source/package/router không có; ST-10 design hiện cũng chưa cung cấp lessonId từ ST-09. | Route/session/lessonId handoff UNWIRED; không tạo ID mặc định hoặc redirect/auth behavior. |
| Lesson | ST-11 inventory gọi GET #24; payload catalog `ApiEnvelope<Lesson>` với id/course_id/title/content?/video_url?/order/status. | #24 chỉ có API catalog/DD Draft; không có Student route/module/query/test. | Entitlement độc lập, publish gate, projection, `LessonStatus`, null/URI và 403/404 đều chưa chốt. |
| Media playback | Intended screen function là xem nội dung/video. | Không có media element, video URL binding, control hoặc player runtime trong HTML/ảnh. | Không khẳng định auto-play, play/pause, seek, buffering, transcript, URL signing hoặc player vendor. |
| Progress | Inventory: PATCH #25 khi có progress event hợp lệ. Catalog body `position:int32!`, `percent:int32!`, `completed:boolean!`; response `ApiEnvelope<Lesson>`. | #25 không có Student route/module/query/test. Candidate `lesson_progress` không có `position` hoặc UNIQUE(`user_id`,`lesson_id`); API DD open. | Unit/range/mapping/identity/state/timestamp/aggregate, autosave/throttle/retry/idempotency chưa được quyết định. |
| Resources | Inventory: GET #26 lazy; ST-12 cũng dùng #26. | Không có resource panel/link trong ST-11 asset; #26 không có source. Candidate `resources` table có nhiều resource, nhưng catalog response `Lesson`, không Resource collection. | Trigger/cardinality/order/empty/visibility/signed URL/direct auth còn mở; không fetch hay mở external URL từ asset. |
| Next lesson | Inventory: GET #27 sau completed; AC-15 expects next navigation. | Không có Next control; #27 không có source. API DD open về course/order/tie-break/terminal item/response semantics. | Không tự chọn bài tiếp, không coi 404 là “end of course” nếu chưa có contract. |
| Study Server | Catalog + API DD #24–#27; all Draft — Needs Confirmation. | Router scan: no `/lessons` Student path; current `/admin/lessons*` routes are Admin APIs #82–#86 and not substitutes. No focused tests for #24–#27. | Mark `DECLARED_NOT_RUNNABLE` / `NOT_FOUND`; no runtime/API claim. |
| Design/a11y | Study UI guide intends Inter/system, width about 1120px, ocean tokens, responsive layout/focus/accessibility. | Asset uses remotely loaded Plus Jakarta Sans, max-width 1440px, fixed header and no runtime focus/player states; CTA has visible label. | Record design-guide discrepancy and focus/reflow/icon semantics for later implementation review; do not modify source asset. |

### API sequence and cross-screen discrepancies

- ST-10 inventory says GET #24 before success handoff to ST-11; ST-11 inventory says GET #24 when opening the player. It is unclear whether #24 belongs to transition only, player only, or both. The DD must preserve this as a fetch-ownership blocker; do not resolve by caching or duplicate request assumptions.
- AC-15 diagram orders #24 → access/publish check → lesson/content → #26 resources → #27 next → render. ST-11 inventory says #26 is lazy and #25 runs on valid progress events. Preserve eager-vs-lazy ordering discrepancy; no source adjudicates it.
- API #26 returns `ApiEnvelope<Lesson>` by catalog although its name/use case is attached Resources; reusable `Resource` schema and candidate `resources` table are distinct. Record without substituting a new response.
- API #25 calls for progress and course aggregate, but range, position storage, aggregate formula, transaction and autosave are open. Candidate DDL is not a live schema.

## 4. Planned marker and event coverage

### Marker plan

Use **14 ordered marker groups** on the original screenshot. The four breadcrumb/footer link groups keep separate visible link targets distinct.

1. Header Study2Work brand link.
2. Header “Quay lại khóa học của tôi” link.
3. Breadcrumb “Khóa học của tôi” link.
4. Breadcrumb separator and current location “Bài học”.
5. Unavailable-state card/container.
6. `play_lesson` decorative icon.
7. H1 “Bài học”.
8. Bold unavailable message “Nội dung bài học hiện chưa sẵn sàng.”
9. Supporting fallback explanation.
10. Primary “Quay lại khóa học của tôi” CTA.
11. Footer Study2Work brand.
12. Footer “Tổng quan” link.
13. Footer “Khóa học của tôi” link.
14. Footer “Tiến độ” link.

Badges/leader placement will use whitespace and the card edges; no source text or action may be obscured. Each JSON `element_id` will map to exactly one `ST11-EL-##` row.

### Event plan

1. `ST11-EV-01` route entry, parse lessonId and obtain Student context; current route/auth source absent and ST-09 handoff missing.
2. `ST11-EV-02` load authorized lesson via #24, include request/schema/status contract and open access/publish/error projection; record duplicate ownership with ST-10.
3. `ST11-EV-03` playback start/pause/seek as expected player interactions; controls and media URL policy are absent, so no runnable steps can be asserted.
4. `ST11-EV-04` save progress via #25 on an approved progress event; describe catalog request/body/status and explicitly mark trigger, normalization, throttle, autosave, retry, dedup, position mapping and aggregate as unresolved.
5. `ST11-EV-05` completed state and #27 next lesson flow; do not invent completion threshold, terminal lesson response or auto-navigation.
6. `ST11-EV-06` lazy #26 resources; trigger/panel absent, response/cardinality/visibility/URL handling unresolved, cross-link ST-12.
7. `ST11-EV-07` header/CTA/back-to-course navigation using actual static hrefs; destinations are paths in HTML but Study Web router is not present.
8. `ST11-EV-08` footer navigation to `/student`, `/student/courses`, `/student/progress`; no browser behavior/runtime claim.

## 5. DD contents, blockers and acceptance

- DD will contain overview/evidence, expected vs current flow, Mermaid sequence with unresolved decisions, 14-element mapping, 8 event contracts, API/security matrix for #24–#27, state/navigation matrix, design/accessibility observations, blockers and acceptance checklist.
- Blockers to retain: fallback vs player design; ST-10/ST-11 #24 ownership; missing ST-09 lessonId and Study Web route/auth; no current #24–#27 Student APIs/tests; entitlement/JWT/publish/error rules; #25 position/range/state/upsert/aggregate/autosave; #26 Resource payload/cardinality/visibility/signed URL; #27 order/tie-break/no-next/404; no player/media URL/security/accessibility contract; loaded/error/recovery/player controls absent.
- DD READY is not expected from current evidence. Status remains **DD BLOCKED; IMPLEMENTATION BLOCKED; RUNTIME NOT VERIFIED** until canonical design/API decisions and sources close these items.
- No tests/runtime calls are requested. Static verification after authoring: source hashes unchanged; dimensions; marker IDs sequential/unique and matching DD; SVG circles/embedded source bytes; local links; visual review; `git diff --check`; tracker/worklog.

## 6. Re-audit trước khi hoàn thiện DD (2026-11-07)

Đã đối chiếu lại contract, source backend, hai nhánh DDL và bộ asset hiện có trước khi sửa DD/marker:

- **API #24–#27:** Catalog vẫn khai báo lần lượt GET lesson, PATCH progress, GET resources và GET next. API DD tương ứng đều `Draft — Needs Confirmation`; các `OPEN_QUESTIONS.md` giữ mở entitlement/JWT/publish/error/projection (Q-24), ý nghĩa và nơi lưu `position`, percent/state/upsert/aggregate/transaction/response (Q-25), payload/cardinality/empty/access/visibility/URL (Q-26), curriculum order/tie-break/auth/terminal result (Q-27). Không có quyết định mới để đóng các câu hỏi này.
- **Current Study Server:** Rà lại router `app/api/v1.py`, modules và tests không thấy Student route/module/query/test cho #24–#27. Student modules hiện có không bao gồm lesson player APIs; các `/admin/lessons*` APIs #82–#86 thuộc Admin và không xác minh endpoint Student. Catalog/API DD không phải runtime implementation.
- **Database candidates cần phân biệt:** `infra/postgres/study-server/DB.sql` mô tả mô hình legacy BIGINT: `lessons.course_id` nullable; `resources.lesson_id` nullable; `lesson_progress` có `status`, `progress_percent`, `last_accessed_at`, `completed_at`, không có `position` hay unique `(user_id, lesson_id)`. `infra/postgres/02_study_db.sql` mô tả V1-PILOT UUID/versioned model khác: `lessons` gắn `chapter_id`/`course_version_id`; `lesson_progress_facts` gắn `enrollment_id`/`lesson_id`, lưu state/timestamps nhưng không có `position`/`percent`; `block_progress_facts.last_position_seconds` thuộc block progress và không xác nhận mapping cho API #25. Hai DDL artifact không được gộp thành một schema contract và không chứng minh live schema.
- **Cross-screen/API effects:** ST-10 và ST-11 vẫn cùng liệt kê #24; ST-09 chưa cung cấp `lessonId`. AC-15 vẽ #26/#27 trước render, còn inventory ghi #26 lazy và #27 sau completed. ST-12 cũng dùng #26. Không có nguồn mới để chọn request owner, eager/lazy order hoặc điều kiện next.
- **Asset/current UI:** `screen.png` (1280×1024) và `code.html` giữ nguyên hashes đã ghi ở phần trên; HTML vẫn là unavailable-content fallback tĩnh, 7 anchors và không có media/player/progress/resource/next controls. Bộ marker 14 ID và 8 event giữ nguyên vì asset không có element bổ sung.
- **Plan trước khi sửa DD:** Chuyển các mục hiện có thành các phần A–F tường minh (overview, flow, element, events/API/security, state/navigation, acceptance), giữ riêng UI/accessibility, blockers, asset/source evidence. Bổ sung blocker ghi rõ hai họ DDL khác nhau và `last_position_seconds` của block progress không phải bằng chứng lưu lesson `position`. Không đổi ảnh nguồn, không tự thêm control/response field/route/behavior; giữ DD BLOCKED, IMPLEMENTATION BLOCKED, RUNTIME NOT VERIFIED.

Phạm vi re-audit này là đầu vào kế hoạch cho bản DD; không thay thế quyết định từ product/API/schema owner và không tuyên bố xác minh runtime.

## 7. Planned outputs and next pointer

- Hoàn thiện `ST-11.md`, `ST-11_markers.json`, `ST-11_markers_overlay.svg`, và `screen_annotated.png`; preserve `screen.png` và `code.html`.
- Update global tracker with ST-11 artifact/status/blockers; recalculate complete artifact-bundle count after static audit; move pointer to ST-12.
- No context page changes planned. If any context page changes, run `node scripts/validate-agent-context.mjs` before finishing.

## 8. Kết quả thực hiện và kiểm tra tĩnh

- Đã hoàn thiện `ST-11.md`, `ST-11_markers.json`, `ST-11_markers_overlay.svg` và `screen_annotated.png`; giữ nguyên `screen.png` và `code.html`.
- Đối chiếu tĩnh đạt: 14 marker tuần tự/duy nhất, 14 DD element rows khớp IDs, 8 event headings, 14 SVG circles; source 1280×1024, annotated 2820×2048; SVG embed đúng bytes của ảnh nguồn. Annotation đã được mở xem; marker đặt gần element mà không che nội dung quan trọng.
- Recount hiện tại: 83/83 inventory IDs có source folder và PNG/HTML; 82/83 có đủ core bundle `screen.png`, `screen_annotated.png`, `code.html`, `<ID>.md`, `<ID>_PLAN.md`, `<ID>_markers.json`. ST-01 là ID duy nhất còn thiếu DD bundle. Đây là tiến độ toàn repo tại lần kiểm kê này, không phải chỉ riêng 03_student.
- Tracker đã ghi ST-11 `DD BLOCKED; IMPLEMENTATION BLOCKED; RUNTIME NOT VERIFIED`; vị trí tiếp theo là ST-12. Link local, JSON/XML, A–F, event IDs, core-bundle count, hashes và scoped whitespace check sẽ được ghi nhận trong worklog sau kiểm tra cuối.
- Không chạy application tests, browser/runtime hoặc live DB check.

# AD-13 — Kế hoạch Detailed Design

## 1. Phạm vi và kết quả cần tạo

- Phiên này chỉ hoàn thiện **AD-13 — Chi tiết bài học quản trị**; dừng trước AD-14.
- Giữ nguyên `screen.png` và `code.html`. Tạo plan này trước marker, ảnh chú thích hoặc DD.
- Tạo `AD-13_markers.json`, `AD-13_markers.svg`, `screen_annotated.png` và `AD-13.md`, mục A–F; mỗi số marker có đúng một element row.
- Đối chiếu AD-12 handoff, AC-34/API #83, current route/module/query/model/test source, legacy/V1-PILOT schema candidates, Study Web source status và Study design guide.
- Cập nhật inventory/API reverse index/global `dd_screens/PLAN.md` và worklog; giữ API #83 DD là `Draft — Needs Confirmation`.

## 2. Expected behavior và current behavior

### Expected behavior

- Inventory row 71 đề xuất `/admin/lessons/:lessonId`, Actor Admin theo AC-34 có lesson-management permission, GET #83, xem lesson content/status/linked progress theo contract; liên kết AD-14; states loading/ready/404/error.
- AC-34 flow: AD-12/#82 → chọn Lesson → AD-13/#83 → AD-14/#84 update, #85 status hoặc #86 delete → reload AD-12. Handoff chỉ dùng numeric `Lesson.id` nếu response #82 hiện hành có row ID; API #83 yêu cầu path `lesson_id:int64`.
- Catalog #83: `GET /api/v1/admin/lessons/{lesson_id}`, Bearer JWT/Admin, required path int64, direct `ApiEnvelope<Lesson>`, HTTP 200, errors 401/403/404/500.
- AC-34 node n5 ghi “Đọc lesson + dependencies”, nhưng không nêu dependency fields, counts hay nơi đặt output. Giữ điểm này là clarification/blocker.

### Current behavior đã xác minh từ source

- Thư mục hiện chỉ có `screen.png` (1600×1595; SHA-256 `3e91e4b99567c2a8bfdcedd534d1e2c0b88360010fe742ede20fd91802bfa0dd`) và `code.html` (SHA-256 `a638941b112888e0b241c487b632197a8c689cbd6ff4100554749e8e5298ead5`). Prototype là empty state, sáu metadata cards, resources/quiz/discussion summaries, admin action, metric/SSE panel, audit/concurrency/sync claims.
- Study Web tree được kiểm tra lại: chỉ có `dist`, `docs`, `node_modules`, `tsconfig.tsbuildinfo`; không editable source/package/router/API client. HTML không binding/listener/request/EventSource/WebSocket/timer; anchors là `href="#"`; nút điều hướng AD-14 bị disabled. Status `UNWIRED`; runtime `NOT VERIFIED`.
- Route #83 được compose tại `GET /api/v1/admin/lessons/{lesson_id}` với `GetAdminLessonEnvelope`/direct `Lesson`. Shared Bearer/JWT role `ADMIN` guard chạy trước raw path parsing và DB. Custom parser chấp nhận signed int64 trong bounds; malformed/overflow/overlength path → local 404 (DERIVED), không gọi DB.
- Query bind ID vào một row `lessons`; loại `status='DELETED'`, không lọc `PUBLISHED`, không join/query resources/progress, không mutate. Output fields: `id`, `course_id`, `title` (`name`), nullable `content`, nullable `video_url`, `order` (`sort_order`), `status`. Success là 200 direct `data` object; missing/deleted→404 + rollback; query/mapping/required-field failure→safe 500 + rollback; success không commit.
- API #83 DD vẫn Draft. Focused test source đã đọc, không chạy; tests dùng fake DB và không xác minh live schema/deployment. Legacy BIGINT DDL nullable `course_id/order/status` khác reusable Lesson required fields; V1-PILOT DDL là UUID/versioned model không tương thích trực tiếp.
- API #86 current source khóa Lesson, kiểm tra `lesson_progress`, `resources`, `lesson_uploads` tại thời điểm delete; có dependency thì trả 422. Điều đó không tạo dependency counts cho #83, và không cho phép dựa vào detail-time state để quyết định delete.

## 3. Discrepancies / blockers phải giữ trong DD

1. Inventory/AC mong xem linked progress/dependencies; #83 response chỉ có Lesson và không query dependencies. API #86 tự kiểm tra tiến độ/resource/upload khi delete. Cần owner xác định có cần endpoint/output dependencies hay không.
2. Mockup hiển thị course title, content type, resource/quiz/discussion counts và lesson identifier; #83 chỉ có numeric `course_id`, `id`, title, content, video_url, order, status. Không có title/slug/type/resource count.
3. Mockup hiển thị engagement metrics và Realtime SSE (students, completion/submission/rating, connection state); #83 không có metrics, stream, paging, or SSE contract.
4. Mockup tuyên bố auto concurrent lock, Audit Log Level 1, sync state, secure media extraction và Admin isolation. #83 là GET read-only; không chứng minh write lock/audit/sync/identity or media authorization.
5. AC-34 yêu cầu lesson-management permission, current guard chỉ kiểm tra role `ADMIN`; status enum/casing và tombstone policy vẫn mở. Live schema/deployment chưa xác minh.
6. Study UI mockup dùng cobalt/Plus Jakarta Sans/full width, lệch `.agents/web-study/design.md` ocean tokens/Inter-or-system/content width ~1120px. Ghi nhận và áp dụng guide khi implement; không sửa source image.

## 4. Kế hoạch marker

Ảnh nguồn `1600×1595`; dự kiến 61 marker, đánh số theo thứ tự đọc từ shell, nội dung lesson, resource/action/metrics, tới footer. JSON/SVG ghi tâm marker theo pixel nguồn; vòng tròn và stroke nằm trong bounds. Section C phải có chính xác 61 hàng tương ứng.

| Marker | Phần tử được ánh xạ |
|---:|---|
| #1–#9 | Brand, 5 Admin nav links, SYSTEM NORMAL, notification, static Admin identity/avatar |
| #10–#11 | Breadcrumb hệ thống; static RBAC assurance |
| #12–#16 | Breadcrumb Quản trị đào tạo/Quản lý bài học/Chi tiết bài học; endpoint kicker; back-to-AD-12 link |
| #17–#21 | AD-13 badge; Admin access badge; H1; subtitle; static sync-status card |
| #22–#33 | Lesson info heading; static record count; empty icon/heading/copy/AD-12 link; sáu metadata cards (title, lesson ID, course, content type, order, publication status) |
| #34–#41 | Resources heading/payload badge; empty icon/heading/copy; quiz, attachment, discussion summary cards |
| #42–#48 | Admin action heading/copy; disabled AD-14 button; access-policy notice; data-protection heading; concurrent-lock row; audit-level row |
| #49–#55 | Metrics heading/status dot; aggregate loading claim; three metric rows; Realtime SSE/disconnected row |
| #56–#57 | Display standards heading and static isolation/data claim |
| #58–#61 | Copyright/system footer; privacy, RBAC, support links |

Tạo `AD-13_markers.svg` cùng số/tọa độ/nhãn với JSON. Render overlay 2× (`3200×3190`) và ghép trên source đã resize 2×; không chỉnh sửa `screen.png`. Sau render xem trực tiếp để rà che phủ, trật tự, tương phản và tính dễ đọc.

## 5. Events cần đặc tả

1. **EV-01 — Route entry/load detail:** route param → GET #83; auth-first; signed int64 custom parser; lookup/tombstone; direct Lesson response; 401/403/404/500; nullable/missing projection; no query/body.
2. **EV-02 — Map/render Lesson fields:** `id/title/course_id/order/status/content/video_url` mapping; không tạo course title/content type/status label; response nulls giữ rõ; screenshot placeholder không phải response.
3. **EV-03 — Content/media preview:** #83 có nullable text `content`/`video_url` nhưng không có content-block/resource schema, signer/player/DRM/expiry/authorization. Không tự render URL/payload như trusted media; policy cần nguồn riêng.
4. **EV-04 — Linked resources/progress/quiz/discussion:** prototype counters không được #83 cung cấp; AC dependencies chưa định nghĩa output. #86 rechecks progress/resources/uploads at delete time; không hiển thị stale detail counts như delete eligibility.
5. **EV-05 — Engagement metrics/SSE:** current panel static; #83 không trả metrics/stream. Do not create API #65/#66 substitutions across Mentor/Admin boundaries; do not show percentages/counts as live.
6. **EV-06 — Mở AD-14 action:** prototype button disabled; expected handoff preserves numeric `lessonId`. #84/#85/#86 are downstream flows, not mutations fired by this detail button; route/access/payload belong AD-14 session.
7. **EV-07 — Quay lại danh sách AD-12:** back/inline anchors `href="#"`; expected return to AD-12. Query preservation, refetch, selected row and browser-history behavior unresolved.
8. **EV-08 — Admin shell/footer/status/compliance copy:** static anchors/badges; no notification, health, role profile, audit, SSE or policy endpoint; no action/runtime claim.

## 6. State, authorization và navigation

- Target candidate states: `UNWIRED`, `loading`, `ready`, `not-found`, `unauthorized`, `forbidden`, `service-error`, `selection-required` (prototype-only until route rule set). Không suy ra state transition từ static copy.
- Current #83 outcomes: 200 direct Lesson; 401 auth; 403 role; 404 malformed/overflow/overlength ID or absent/DELETED row; 500 query/identity/required projection failure. No 422 in API #83 OpenAPI error set.
- Numeric `Lesson.id` từ AD-12 là handoff candidate; title-only slug chưa được API/source xác nhận. API #83 không nhận query/body. Return target AD-12; action target AD-14. Route guards and browser history are not implemented.
- Access expected: Admin with lesson-management permission; current source only enforces `ADMIN`. Không để client-side UI gating thay thế server authorization.
- Apply Study Web design guide for responsive layout, ocean tokens, typography, keyboard/focus, empty/loading/error states and reduced motion when a real frontend exists; current mockup is not evidence of those behaviors.

## 7. Thứ tự thực hiện và kiểm tra

1. [x] Đọc objective/router/context, docs worklog selector và 3 selected worklogs; load project/web-work/server-study context và registry.
2. [x] Đối chiếu AD-13 source assets/DOM, inventory/AC-34/API #83 catalog/DD/route/module/query/model/test/schema; recheck Study Web source tree.
3. [x] Lưu plan trước marker JSON/SVG, annotation và screen DD.
4. [x] Tạo 61 marker JSON/SVG và annotated PNG 2×; xem lại trực tiếp.
5. [x] Viết A–F DD với 61 element rows, EV-01…EV-08, field mapping, API/errors, access/dependency/media/metrics blockers and state/navigation.
6. [x] Cập nhật AD-13 inventory/API #083 reverse index D→R per local route/module/test source; update global checkpoint/worklog; giữ API DD Draft và không sửa AD-14.
7. [x] Static audit: source hashes/dimensions; JSON/XML; marker sequence/coordinates/stroke bounds; 1:1 C rows; local links; 83 IDs/folders/core artifact count; image review; `git diff --check`. Không chạy application tests/runtime.
8. [x] Kết thúc AD-13; giữ blocker statuses rõ ràng và dừng trước AD-14.

# AD-11 — Kế hoạch Detailed Design

## 1. Phạm vi và kết quả cần tạo

- Chỉ hoàn thiện Screen ID **AD-11 — Duyệt/từ chối nội dung** trong phiên này.
- Thư mục nguồn: `apps/study-client/docs/screen_stitch/05_admin/AD-11_duyet-tu-choi-noi-dung/`.
- Giữ nguyên `screen.png` và `code.html`; tạo plan này trước, sau đó `AD-11_markers.json`, `AD-11_markers.svg`, `screen_annotated.png` và `AD-11.md`.
- Đặc tả A–F, nối AC-33, AD-10 và API #79/#80/#81; ghi rõ khác biệt AC/catalog/source, không tự quyết định moderation permission, publish policy, revision, reason validation hay live-schema behavior.
- Cập nhật inventory AD-11, reverse API index #079–#081 nếu có route/module/test source, global checkpoint và worklog. Không author AD-12.

## 2. Expected behavior và current behavior

### Expected behavior

- Inventory row 69 đề xuất `/admin/content/:contentId/review`, actor Admin/AC-33, GET #79 detail, sau đó PATCH #80 approve hoặc PATCH #81 reject với `reason`, rồi reload AD-10/#78.
- AC-33 kỳ vọng Content/version/author detail, quyết định approved/rejected có audit và queue reload. Diagram node #9 ghi `APPROVED/PUBLISHED + audit`; điều này xung đột với API #80 catalog/local source hiện ghi `APPROVED`. Giữ discrepancy mở.
- API catalog: #79 `GET /api/v1/admin/content/{content_id}` path `int64`, response `ApiEnvelope<Content>`; #80 `PATCH /api/v1/admin/content/{content_id}/approve` path-only; #81 `PATCH /api/v1/admin/content/{content_id}/reject` path + JSON `{reason:string!}`. Cả ba yêu cầu Bearer/Admin; catalog errors 401/403/404/500 cho #79 và 401/403/404/422/500 cho #80/#81.
- Rejection reason bắt buộc theo #81; screenshot lại ghi “Tùy chọn”. Mọi UI behavior vượt catalog/AC/source phải được nêu là cần quyết định.

### Current behavior đã xác minh

- Study Web editable source/router/package/API client chưa có trong checkout; prototype không wire request. Runtime `UNWIRED` / `NOT VERIFIED`.
- HTML tĩnh: shell links `href="#"`; back-to-AD-10 link `href="#"`; notification không handler; approve/reject disabled; textarea `#review-comments` disabled; không có form/input/select/table/video/iframe hoặc fetch/XHR/API URL/timer/listener.
- Preview rỗng, badge “Chưa liên kết ID”; title/author/course/date là `--`, content ID `NULL`, version `N/A`. Secure video/SCORM/PDF renderer text là claim tĩnh, không có renderer/source.
- Decision panel ghi reason optional, khóa action và giải thích ownership-policy; #81 hiện yêu cầu `reason` field nhưng chấp nhận empty string, không trim/blank/min/max validation. Approve label nói “xuất bản”, nhưng #80 chỉ đặt status `APPROVED`.
- Rubric v2 hiện có ba criterion đều được đánh dấu check nhưng progress ghi `0/3 tiêu chí được nạp`; không có rubric API, model hay policy source.
- #79 current local handler trả trực tiếp Content projection gồm đúng tám trường: `id`, `course_id`, `content_type`, `title`, object `payload`, `status`, nullable `parent_id`, `order`; không có author/version/course name/submitted date. Detail chỉ đọc active row; không có status predicate, revision selector/version token.
- #80 current local handler yêu cầu role `ADMIN`, lock active Content row, chỉ chuyển `PENDING_REVIEW → APPROVED`, ghi một audit row với reason NULL, trả Content projection; không phát hành publish transition/notification/version. Invalid int64 path→422; missing/deleted→404; non-pending→422; safe 500 + rollback khi lỗi DB/projection/commit.
- #81 current local handler yêu cầu body strict `{reason:string}`; auth/ADMIN guard, pending-only transition `PENDING_REVIEW → REJECTED`, một audit row giữ reason nguyên văn; không trả reason trong Content response. Empty string được test/accept; invalid path→422, missing/deleted→404, non-pending→422, safe 500 + rollback.
- #80/#81 không mang revision ID/expected version/idempotency key. Thao tác được đánh giá trên logical row đang current khi request chạy; retry sau success có thể nhận 422 do không còn pending. Local tests fake DB không chứng minh PostgreSQL, migration deployment hay live role policy.
- Migration 011 là checked-in BIGINT audit schema candidate; legacy BIGINT content tables và V1-PILOT UUID review model khác nhau; live DB chưa xác minh.

## 3. Discrepancies và blocker cần giữ trong DD

1. AC-33 diagram `APPROVED/PUBLISHED`; catalog/local #80 `APPROVED`; Mentor #52 là luồng riêng `APPROVED ↔ PUBLISHED`.
2. Screenshot “Approve publish” và “reason optional” xung đột với #80 state và #81 required field; disabled textarea khiến không thể nhập reason.
3. #79 projection thiếu author/version/course title/submitted date; preview claim cần payload decoder/media contract chưa có.
4. AC #79 version/author intent không có version token/author mapping hiện hành; stale queue, current-row decision và conflict policy chưa được xác định.
5. `ADMIN` guard là shared role; không chứng minh moderation-specific permission.
6. Rubric criteria/check states/progress là static and internally contradictory; chưa có source cho rubric version, load state, scoring/pass policy.
7. Legacy DB/migration evidence không chứng minh live schema/deployment; V1-PILOT UUID model khác.
8. Study Web route/client/runtime, loading/error/session/navigation/reload behavior chưa được wire.

## 4. Kế hoạch marker

Ảnh nguồn **1566×1600**. Tạo 48 marker đánh số theo thứ tự từ trên xuống dưới; đặt trên khoảng trống cạnh mục tiêu để hạn chế che nội dung:

| Marker | Element được ánh xạ |
|---:|---|
| #1–#6 | Brand Admin và năm mục navigation; Kiểm duyệt active |
| #7–#9 | System Normal tĩnh, notification, Admin identity/avatar |
| #10–#11 | Breadcrumb hệ thống và badge RBAC tĩnh |
| #12–#15 | Breadcrumb kiểm duyệt, queue/detail crumb và back-to-AD-10 link |
| #16–#18 | Kicker cổng kiểm định, title, subtitle |
| #19–#20 | Status card icon/copy “Cổng phê duyệt đang khóa (#79/#80)” |
| #21–#22 | Preview header/title và “Chưa liên kết ID” badge |
| #23–#26 | Empty preview icon, empty heading, instruction, secure renderer/SCORM/PDF claim |
| #27–#33 | Metadata heading; title, author, course, date, Content ID NULL, version N/A |
| #34–#41 | Decision heading, Khóa badge, optional reason label, disabled textarea, ownership warning, disabled approve/reject, API #81 claim |
| #42–#47 | Rubric heading/version, three checked criteria, contradictory 0/3 progress |
| #48 | Footer copyright and policy/support links |

- JSON schema: ordered objects `{number,x,y,label}`, coordinates in original 1566×1600 pixels. Keep complete marker circles/strokes within bounds.
- SVG uses same IDs, labels and coordinates as JSON. Render at 2× (3132×3200) and composite over resized original without modifying `screen.png`.
- DD section C must contain exactly one row for every marker #1–#48.

## 5. Event cần đặc tả

1. **EV-01 — Open detail/load:** route param candidate `contentId` → #79; explain auth-first path parse, local detail projection/status behavior and 401/403/404/500; no current caller.
2. **EV-02 — Preview decode:** empty preview current state; do not invent media URL, secure player, SCORM/PDF decoder or safe renderer behavior from static text.
3. **EV-03 — Metadata render:** exact eight-field #79 mapping and explicit unavailable author/version/course name/submitted date; `NULL`/`N/A` are static placeholders.
4. **EV-04 — Enter rejection reason:** textarea disabled in prototype; expected #81 body requires `reason:string`; local strict schema permits empty string; trim/blank/length policy remains open.
5. **EV-05 — Approve:** target #80 path-only; current local pending-only transition to APPROVED with audit; do not equate with PUBLISHED.
6. **EV-06 — Reject/request changes:** #81 body, exact current transition/audit; “request revision” semantics are not distinguished by API.
7. **EV-07 — Rubric evaluation:** three static checked criteria and 0/3-loaded contradiction; no supported dynamic state, scoring, veto or pass rule.
8. **EV-08 — Back, shell and completion navigation:** current anchors have no route; AC-33 expects queue reload after decision, but query preservation/cache invalidation/history not implemented or approved.

## 6. API, state and navigation trace

- Expected: AD-10 selection → numeric `content_id` → #79 → one decision branch (#80 or #81) → reload #78. The AD-10→AD-11 ID handoff is only a candidate because current #78/#79 responses have no revision identity.
- #79 current direct response local `Content` has eight fields above; no `author_id`, author profile, course title, submitted timestamp, `content_version_id`, version token, signed media URL or rubric response.
- #80/#81 source paths/tests will be cited individually. Preserve API catalog/AC vs source differences; no implementation claims from mockup.
- State candidates: `UNWIRED`, `loading`, `ready`, `pending-review`, `preview-unavailable`, `approving`, `rejecting`, `success-reload`, `not-found/deleted`, `stale-or-not-pending`, `unauthorized`, `forbidden`, `validation-error`, `service/network-error`. Only source-backed server outcomes are documented as current; client state transitions are target/open until a frontend contract exists.
- #80/#81 mutations are not revision-bound/idempotent. If #79 detail becomes stale before decision, current handler evaluates the row at mutation time; no `409` stale-version response exists in these APIs.

## 7. Execution and verification order

1. [x] Docs preflight, exact-type worklog selection/review, context map and scope routing.
2. [x] Inspect AD-11 assets/DOM, AC-33, API catalog/DD, route/modules/query/model/validator, focused test source, DB/migration context and Mentor #52 publication path.
3. [x] Save this plan before marker JSON/SVG, annotated PNG or screen DD.
4. [ ] Create ordered 48 JSON/SVG markers and 2× annotated PNG; visually review.
5. [ ] Author A–F DD, 48 element rows, EV-01…EV-08, API/error trace, states/navigation and blockers.
6. [ ] Update inventory AD-11 and reverse API #079–#081 source status; update global tracker/checkpoint and worklog.
7. [ ] Static audit: source hashes/dimensions, JSON/XML, order/coordinates/stroke bounds, C-row bijection, local links, 83 IDs/folders/core-artifact count, whitespace and annotated image. Do not run app tests/runtime.
8. [ ] Finalize worklog and stop after AD-11; AD-12 remains a separate session.

# ME-13 — Kế hoạch Detailed Design

> Status: COMPLETE (plan actions executed); DD BLOCKED; Screen ID: ME-13; Date: 2026-11-06

## 1. Mục tiêu và ranh giới

Đặc tả bước chọn khóa học và người nhận thông báo của Mentor, giữ nguyên ảnh nguồn và HTML, tạo marker map tuần tự, overlay/ảnh có chú thích, DD A–F, rồi cập nhật inventory, kế hoạch tổng và worklog. Chỉ xử lý ME-13 trong phiên này. Không triển khai Study Web, không sửa API server, không soạn ME-14.

Expected flow từ inventory là GET #46 để lấy các khóa của Mentor, GET #62 theo course_id để lấy roster, rồi preserve các Student IDs cho ME-14. API #63 là downstream dependency để kiểm tra payload handoff, không phải API được gọi từ ME-13.

## 2. Phân loại bằng chứng

### Expected behavior

- list_screen.md định nghĩa route đề xuất /mentor/notifications/new/recipients, AC-25, actor Mentor, #46/#62, các trạng thái loading/empty/selected/denied, và bước tiếp theo ME-14.
- AC-25 mô tả chọn course, tải ACTIVE enrollments, chọn người nhận và chuyển dữ liệu recipient sang API tạo thông báo. Diagram ghi recipient là CSV Student IDs, nhưng contract #63 hiện vẫn Draft và phải giữ trạng thái DERIVED khi đối chiếu runtime source.
- Ảnh mô tả ba scope all, support_needed, specific; hỗ trợ học kỳ hiện tại, khóa được phân công, privacy mode, channel theo LMS/email và WCAG. Đây là tuyên bố trong prototype, chưa phải bằng chứng backend.

### Current source behavior

- screen.png là ảnh tĩnh 1600×1546; code.html là prototype tĩnh, không có handler/fetch/router. Các liên kết đều href="#"; Continue đang disabled.
- Study Web vẫn UNWIRED, nên route, component state và API requests chưa có runtime hiện hành.
- API #46 có route/module/tests cục bộ; trả danh sách course do Mentor trực tiếp sở hữu, có status DRAFT/PUBLISHED và page/size. Source không trả semester hoặc assigned-course relationship.
- API #62 có route/module/tests cục bộ; trả Student id:int64, full_name và optional avatar_url cho ACTIVE enrollments của course trực tiếp thuộc Mentor. Không trả progress/checkpoint, email hay pagination.
- API #63 có route/module/tests cục bộ, nhưng DD còn Draft/Needs Confirmation và các recipient/channel mapping là DERIVED. Body yêu cầu recipients:string CSV, title:string tối đa 200, content:int64, channels:string CSV. Response 202 chỉ xác nhận transaction đã enqueue Notification và QUEUED delivery outbox; không chứng minh Push/Email đã phát.
- API source, fake-session tests và DDL/migration cục bộ không xác minh live schema, deployment hay delivery worker/provider.

## 3. Asset và source cần giữ

| File | Vai trò | Điều kiện |
|---|---|---|
| screen.png | Ảnh nguồn 1600×1546 | Giữ nguyên bytes; SHA-256 trước khi sửa: 2764685b871d5e2340942fded53ed9c67a392cd9d65dd4239c007d282ecf45ed. |
| code.html | Prototype tĩnh, 22,336 bytes | Giữ nguyên bytes; SHA-256 trước khi sửa: 2547eb7f6b7263cb509916a66833b2484c9494b3d608263e856da15c807b72ca. |
| ME-13_PLAN.md | Kế hoạch riêng này | Ghi trước khi tạo marker, annotated image và DD. |
| ME-13_markers.json | Mapping marker → element/tọa độ ảnh nguồn | ID 1..49, tuần tự, unique, in-bounds. |
| ME-13_markers.svg | Overlay tái tạo được | Cùng marker order và tọa độ với JSON; viewBox theo ảnh nguồn. |
| screen_annotated.png | Ảnh nguồn + marker overlay | Xuất 3200×3092; không sửa screen.png. |
| ME-13.md | DD Screen A–F | Mỗi marker có đúng một element row; mỗi event có input, bước xử lý, kết quả, lỗi và nguồn. |

## 4. API/AC trace được dùng trong DD

| Nguồn | Hành vi hiện hành liên quan | Giới hạn cần đặc tả |
|---|---|---|
| AC-25 | Course selection → GET course students → chọn recipients/title/content → POST notification → database/outbox → external Push/Email → status. | Diagram ghi #62 trước #63, nhưng không xác định frontend route state, support-needed criteria hoặc handoff persistence. |
| #46 GET /api/v1/mentor/courses | Mentor Bearer; query status? (DRAFT/PUBLISHED), page≥1, size 1..100; default pagination; owner-scoped courses, order created_at DESC, id ASC; 200 page envelope, rỗng là 200. | Không có semester/current-term, enrollment count, assigned Mentor hay label slug-to-int64 mapping. Owner semantics là direct-owner fallback; open questions còn Draft. |
| #62 GET /api/v1/mentor/courses/{course_id}/students | Mentor Bearer; signed int64 path; invalid/missing ID 404, missing course 404, other owner 403; active enrollment + role STUDENT, distinct users ordered id ASC. 200 envelope data[]: {id:int64, full_name:string, avatar_url?:string}, meta={}; empty array hợp lệ. | Không account-status filter, page/cursor, email, course name, progress, checkpoint, lateness, attendance, or support classification. |
| #63 POST /api/v1/mentor/notifications | Strict body with required recipients CSV string, title string ≤200, content signed int64, channels CSV PUSH/EMAIL. Auth precedes CSV validation and DB work. Whole ID set must match ACTIVE Student roster of at least one directly-owned common course. | Body has no course_id/scope enum; CSV format and int64 content disagree with unresolved product text contract. No Idempotency-Key. Delivery worker/provider absent. |
| #63 success/errors | 202 DESIGN_OPERATION_ACCEPTED after DB commit; data Operation {id:UUID, kind=NOTIFICATION_DISPATCH, status=QUEUED, owner_id:int64, submitted_at, updated_at}; meta.notification_ids:int64[]. Errors: 401, 403, 422, 503, 500 with DESIGN_* codes. | Operation UUID differs from notification IDs. Queued is not delivered; #18 and #64 are separate later-session dependencies. |

## 5. Blockers / discrepancy phải giữ

1. Prototype option values cs101/fe202/ba301/qa401 are slugs, while #46 and #62 require numeric int64 course IDs; no source maps these values.
2. Prototype says “Học kỳ hiện tại” and lists assigned teaching courses. #46 has no term field/filter and implements direct ownership; assigned-course access is not present.
3. support_needed criteria mention late submissions, low checkpoints and absences. #62 has no progress or attendance fields/filter; do not derive this cohort.
4. #62 does not return roster data to render as selectable rows in this static HTML; current prototype only shows an empty-state. Define loaded, selection and empty-result design from approved UI/API contract.
5. all/specific must resolve to explicit #62 numeric IDs for #63. #63 locally uses CSV, but DD is Draft and the serialization is DERIVED; confirm selected-ID persistence and exact ME-14 handoff.
6. #63 content:int64 conflicts with the screen’s expected free-form notification content; do not implement text-to-int conversion or infer template semantics.
7. Screenshot claims anonymity, linked-school email and WCAG 2.1 AA. #46/#62/#63 do not establish these behaviors. Channel choice and privacy semantics need product/security approval.
8. #63 has no idempotency contract and no worker/provider. A 202 response only means queued rows committed; do not promise delivery or retry safety.
9. All navigation href values are "#"; route destinations are proposals until Study Web exists. No runtime behavior is verified.

## 6. Planned events

| Event | Trigger | Planned trace |
|---|---|---|
| E01 | Load ME-13 | Gate on Mentor auth/role when a real shell exists; request #46; map page data; represent empty, loading, access, session and API error. No runtime route exists today. |
| E02 | Change course | Clear selection/list from prior course; accept only confirmed numeric course_id; request #62; map Student IDs and summaries; handle empty, 403/404/401/500 and stale response. Do not treat screenshot slugs as IDs. |
| E03 | Change recipient scope | Record selected radio locally only after scope semantics are approved. all derives all roster IDs; specific requires explicit selected rows; support_needed is blocked without a source-backed definition. No API call is evidenced for scope change. |
| E04 | Select/deselect student | Preserve unique positive int64 IDs from #62 in roster order; reject stale IDs after course change. This is a design requirement; the static HTML has no rows/checkboxes. |
| E05 | Continue to ME-14 | Require a selected course and valid non-empty recipient IDs; pass IDs only through an approved handoff. Do not navigate/send if the payload contract is unresolved. The button is disabled in the current prototype. |
| E06 | Cancel | Follow confirmed destination after product/router contract; source anchor is "#", so no target can be claimed. |
| E07 | Header/breadcrumb navigation | Use confirmed application routes; current href="#" values do not navigate. |
| E08 | Footer links | Use approved internal/external destinations; current href="#" values do not establish targets. |

## 7. Marker plan (49 elements, source coordinates)

Coordinates use the unmodified source image, origin at top-left. Badge positions should sit beside target edges/whitespace, with a 2× output so marker labels remain legible. JSON, SVG, annotated image, and DD §C use this order.

| ID | Element target | Anchor (x,y) |
|---:|---|---:|
| 1 | Study2Work Mentor brand lockup | (28,40) |
| 2 | Tổng quan header navigation | (292,39) |
| 3 | Khóa học phụ trách header navigation | (420,39) |
| 4 | Chấm bài header navigation | (628,39) |
| 5 | Hộp thư hỗ trợ header navigation | (753,39) |
| 6 | Thông báo header navigation | (910,39) |
| 7 | Notification bell and unread dot | (1244,67) |
| 8 | Mentor name, role and profile action | (1571,69) |
| 9 | Breadcrumb Thông báo | (44,111) |
| 10 | Breadcrumb Soạn thông báo mới | (170,111) |
| 11 | Current breadcrumb Bước 1: Chọn người nhận | (341,111) |
| 12 | Hệ thống thông báo học vụ badge | (31,158) |
| 13 | ME-13 process code | (304,176) |
| 14 | Screen title | (645,248) |
| 15 | Permission claim chip | (1575,214) |
| 16 | Current step number 1 | (52,324) |
| 17 | Current step label and title | (430,356) |
| 18 | Step progress indicator | (548,326) |
| 19 | Next step number 2 | (1080,321) |
| 20 | Next step ME-14 label and title | (1515,300) |
| 21 | Thiết lập phạm vi gửi card heading | (44,453) |
| 22 | Required indicator | (632,437) |
| 23 | Course field label | (43,520) |
| 24 | Học kỳ hiện tại copy | (645,522) |
| 25 | Course select control | (638,569) |
| 26 | Course helper copy | (48,631) |
| 27 | Recipient scope field label | (43,720) |
| 28 | All students radio card | (51,779) |
| 29 | Support-needed radio card | (51,901) |
| 30 | Specific students radio card | (51,1021) |
| 31 | Notification policy card | (50,1154) |
| 32 | Target student list card heading | (697,459) |
| 33 | Selected recipient count badge | (1130,470) |
| 34 | Anonymity mode chip | (1537,478) |
| 35 | Empty-state illustration | (1062,565) |
| 36 | Empty-state title | (865,729) |
| 37 | Empty-state explanatory copy | (790,847) |
| 38 | Source-not-synced badge | (874,884) |
| 39 | WCAG AA badge | (1372,884) |
| 40 | Estimated recipient count row | (703,1005) |
| 41 | Inactive status label | (1542,1008) |
| 42 | Cancel action | (53,1359) |
| 43 | Course-required helper note | (785,1358) |
| 44 | Continue to ME-14 disabled action | (1151,1313) |
| 45 | Footer brand icon | (31,1470) |
| 46 | Copyright and compliance text | (789,1470) |
| 47 | Footer Mentor rules link | (1050,1470) |
| 48 | Footer assessment standards link | (1244,1470) |
| 49 | Footer technical support link | (1424,1470) |

## 8. Static review gate

- Confirm source screenshot and HTML hashes are unchanged.
- Confirm marker IDs are exactly 1..49, unique, within 1600×1546, and align with 49 DD element rows.
- Confirm SVG parses and marker count/order/titles match JSON.
- Inspect the annotated image at full size for clipping or text obstruction.
- Confirm all API/event errors, empty states, navigation destinations, unresolved contract points and implementation/runtime statuses are stated.
- Do not run application tests or claim runtime verification for this documentation-only task.

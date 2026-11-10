# ME-12 — Kế hoạch Detailed Design

> Status: COMPLETE (plan actions executed); DD BLOCKED; Screen ID: ME-12; Date: 2026-11-06

## 1. Mục tiêu và ranh giới

Đặc tả màn hình chi tiết yêu cầu hỗ trợ của Mentor: đọc thread, gửi phản hồi và resolve yêu cầu khi đủ điều kiện. Giữ nguyên screen.png và code.html; lập marker map theo thứ tự đọc giao diện, tạo ảnh chú thích, viết DD đủ phần A–F, cập nhật inventory/tracker/worklog. Không triển khai Study Web, không sửa API server, không xử lý Screen ID khác.

Màn hình nằm sau ME-11. Expected handoff là SupportRequest data[].id từ API #58 vào route đề xuất /mentor/support/:requestId. ME-12 dùng #59 để đọc chi tiết, #60 để gửi phản hồi và #61 để resolve. Luồng này là thiết kế kỳ vọng; app Study Web hiện chưa có source/package/router nên chưa có runtime route hoặc request thực tế.

## 2. Phân loại bằng chứng

### Expected behavior

- list_screen.md định nghĩa AC-24, route đề xuất /mentor/support/:requestId, ba API #59/#60/#61, các state loading/replying/resolving/resolved/error và thứ tự GET #59 → POST #60 → reload #59; PATCH #61 resolve sau xác nhận.
- F09 quy định ME-11 #58 → ME-12 #59 → #60 reply → #61 resolve khi được phép; chưa có API Student tạo support request, vì vậy không thiết kế CTA tạo yêu cầu trong Student V1.
- AC-24 xác định Mentor có request thuộc course mình quản lý; khi người học đã được giải đáp thì resolve, nếu chưa thì giữ OPEN.

### Current source behavior

- screen.png (1600×1585) và code.html là static prototype. HTML không có script, form submit, fetch/XHR/WebSocket hoặc route binding. href="#" trên điều hướng không chứng minh navigation.
- Request ID “Đang nạp...”, status “Đang mở”, empty thread, “0 / 2000”, textarea, disabled send/resolve và cảnh báo khóa đều là literal markup. Không có nút/chọn file để tạo attachment_refs.
- API #59–#61 có route, module, tests và API DD local. Study Web là UNWIRED; repository không chứng minh UI runtime đang gọi APIs.
- API source, fake-session tests và checked-in migration không chứng minh live database/deployment. API DD #59–#61 vẫn Draft — Needs Confirmation; các fallback schema/lifecycle còn DERIVED.

## 3. Asset và source cần giữ

| File | Vai trò | Điều kiện trước/sau |
|---|---|---|
| screen.png | Ảnh nguồn nguyên trạng 1600×1585 | Giữ nguyên bytes và hash 35e218e17f8e9a55d7a8ba315887f3910979b2e3920801ef9d2c781e6b6f6df4. |
| code.html | Static prototype | Giữ nguyên bytes và hash 4d4290f881dfaa94208851250083f95e4fddfa619be787fe43fcfc6512f3e6fc. |
| ME-12_PLAN.md | Kế hoạch này | Tạo trước marker, overlay, annotated screenshot và DD. |
| ME-12_markers.json | Mapping marker → element/tọa độ nguồn | Tạo sau khi plan được chốt; ID 1..43, unique, in-bounds. |
| ME-12_markers.svg | Overlay marker | Cùng thứ tự và tọa độ với JSON; viewBox theo ảnh nguồn. |
| screen_annotated.png | Ảnh nguồn + overlay | 3200×3170; không sửa screen.png. |
| ME-12.md | DD Screen A–F | Mỗi marker có đúng một dòng Element; mỗi event có trace nguồn và ngoại lệ. |

## 4. API/backend trace sẽ được dùng trong DD

| API | Local route/source behavior liên quan đến UI | Response/error/side effect cần mô tả |
|---|---|---|
| #59 GET /api/v1/mentor/support/{request_id} | Mentor Bearer auth trước parse path/DB; signed int64 parser; query request, course/student và toàn bộ message thread, order created_at ASC NULLS FIRST, id ASC; attachment order theo asset_position ASC; không có pagination. Request ngoài owner trả 403; thiếu/invalid path/request trả 404; lỗi projection/DB trả safe 500. | 200 DESIGN_RESOURCE_RETRIEVED, data là một SupportRequest, meta:{}; messages:[] hợp lệ. Null optional fields bị loại bỏ. GET không commit; lỗi query rollback. |
| #60 POST /api/v1/mentor/support/{request_id}/reply | Body strict: {message: string, attachment_refs: string}; cả hai bắt buộc. attachment_refs là chuỗi JSON của mảng unique signed-int64 UploadAsset IDs; "[]" biểu diễn không đính kèm. Blank-only message bị từ chối; source không có max length. Auth Mentor, ownership check, khóa request; upload phải thuộc Mentor/course và thỏa LECTURE + UPLOADED. Tạo message và ordered links trong một transaction. | 200 DESIGN_RESOURCE_UPDATED, data là SupportRequest đầy đủ sau update. 401/403/404/422/500 theo catalog. Rollback khi lỗi insert/projection/commit. Không idempotency key: POST retry có thể tạo message trùng. Source không chặn reply trên RESOLVED/CANCELLED và không tự mở lại status. |
| #61 PATCH /api/v1/mentor/support/{request_id}/resolve | Không body/query. Auth Mentor rồi parse signed int64; khóa request và kiểm owner. OPEN, IN_PROGRESS, WAITING_LEARNER chuyển RESOLVED; RESOLVED retry idempotent; CANCELLED/state khác trả 422. Source không yêu cầu tối thiểu một message. | 200 DESIGN_RESOURCE_UPDATED, full SupportRequest/thread; resolved_at được set khi transition và có thể null trên retry row cũ. 401/403/404/422/500; transaction commit sau response validation, lỗi rollback. |

Response request shape dùng chung #58: id, course_id, student{id,full_name,avatar_url?}, status, messages[{id,author{id,full_name,avatar_url?},content,attachments[{id,name,url,content_type,size_bytes,status}],created_at}], created_at, resolved_at?. Hiện API không trả course title/slug, SLA state, satisfaction result, socket/session state, pagination cursor hoặc resolution reason.

## 5. BLOCKER / discrepancy phải giữ trong DD

1. D→R ở inventory chỉ biểu thị APIs #59–#61 có route/module/test source cục bộ; API DD vẫn Draft, migration/live DB chưa xác minh, Study Web vẫn UNWIRED.
2. ME-11 cung cấp ID numeric theo expected #58 data[].id; route là proposal. ME-12 source không parse/validate ID và không gọi API.
3. AC-24 precondition yêu cầu request tồn tại/thuộc Mentor nhưng mockup thể hiện “Đang nạp...” và empty thread. Đây là loading/empty-thread presentation, không phải bằng chứng inbox rỗng hoặc request không tồn tại.
4. Mockup giới hạn 2000 ký tự, trong khi #60 source không đặt maximum; chưa có business approval cho giới hạn và cách đếm. Không gán 2000 thành API rule.
5. Mockup nói chỉ unlock resolve sau ít nhất một lượt trao đổi hợp lệ; #61 không enforce minimum message. AC-24 xác nhận learner satisfied nhưng không nêu modal/confirmation UI hoặc cách thu nhận xác nhận.
6. #60 không chặn reply sau resolve/cancel; #61 chỉ cho phép resolve một tập trạng thái. Lifecycle policy cần BA/BE xác nhận trước khi mở controls.
7. Inventory yêu cầu GET sau POST; #60 trả lại full thread nên refetch có thể redundant. Thiết kế cần giữ expected refetch, đồng thời nêu rõ response POST là bằng chứng gửi thành công để không báo thất bại/auto-POST lại khi GET sau đó lỗi.
8. Screenshot quảng bá Socket TLS 1.3, SLA 24 giờ, auto-settlement, satisfaction survey và privacy/source standards; APIs #59–#61 không trả hoặc đảm bảo các dữ liệu/hành vi này.
9. Reply composer không có upload picker dù API nhận attachment_refs; không thiết kế upload control/asset source chưa có evidence. Có thể gửi "[]" nếu không đính kèm, theo contract source hiện tại.
10. Full thread response không có limit/pagination; loaded conversation UI chưa có mẫu được cung cấp. Cần quyết định thiết kế loaded-state và tải lớn trước khi coi screen đủ sẵn sàng implement.
11. Test report hiện có là lịch sử chạy fake DB; không chạy lại trong task docs và không gọi đó là runtime/live schema verification.

## 6. Event/state plan

| Event | Trigger | Planned sequence | Success / failure | Status |
|---|---|---|---|---|
| E01 | Route entry / screen load | Đọc requestId; yêu cầu Mentor session; GET #59; map SupportRequest/thread; render loading/ready/empty/error. Không gọi API nếu route id/auth thiếu; policy redirect/401 handling phải theo shared app auth khi có app source. | 200 maps request/student/status/messages/attachments; 403/404 show access/not-found state; 401 session flow; 500/network retry is user initiated. Full-thread scale unresolved. | Designed; UI runtime unwired. |
| E02 | Back to ME-11 | Navigate /mentor/support; optionally restore list state only when a real router/state contract exists. | No mutation/API required; retain no fabricated list filters. | Proposed route; static href is #. |
| E03 | Type reply | Keep local draft; show count; validate non-whitespace before submit. Do not set a max of 2000 until confirmed; clarify Unicode counting and user-visible limit. | Disabled/validation feedback from blank-only source rule; no API. | BLOCKER: max/character count policy. |
| E04 | Send reply | Normalize route ID/body; send required message plus JSON-string attachment_refs (currently "[]" because no picker); disable duplicate click in flight; POST #60 once; map success response; then perform inventory-required GET #59 refresh. Never auto-retry POST on ambiguous network response. | POST errors per exact API set; on POST success + GET failure, preserve success and show stale refresh indication without resending. Duplicate submit policy only client-side; backend has no idempotency. | API source exists; attachment UI/limit and retry policy open. |
| E05 | Resolve request | Only after AC-24 satisfaction confirmation and currently permitted state; PATCH #61 with no body; do not invent modal layout. Refetch/map response only if required after mutation policy is confirmed; #61 already returns full SupportRequest. | Active statuses → RESOLVED; repeated RESOLVED is idempotent; CANCELLED/unsupported → 422. Does not prove survey or auto-settlement. | BLOCKER: confirmation UI and message/status gate mismatch. |
| E06 | Header/footer/guide links | Activate nav/back-to-list/help/footer actions according to confirmed application routes. | No API evidenced. Prototype anchors are #; destination and external URL are unknown. | Static navigation only; targets unresolved. |

### Proposed state matrix

loading → ready-empty | ready-with-thread | not-found | forbidden | session-error | error; while sending ready-* → replying → ready-* on success or validation/API failure; while resolving ready-* → resolving → resolved/ready-* or error. replying and resolving are intended UI operation states, not current runtime states. A resolved request is read-only only if policy is approved; current #60 contradicts a UI assumption that resolved requests cannot accept replies. Preserve request ID across refresh/deep link. Do not infer a loading indicator, confirmation modal, success toast or error component from the static mockup.

## 7. Marker plan (43 elements, source image coordinates)

Coordinates use source pixels with origin at the top-left. Markers should be placed on nearby whitespace/edge of each target so labels remain readable. Keep marker IDs sequential and use the same row order in JSON, SVG, image, and DD §C.

| ID | Element target | Planned anchor (x,y) | Notes |
|---:|---|---:|---|
| 1 | Mentor logo/brand lockup | (76,72) | Header left, marker below the lockup. |
| 2 | Tổng quan navigation | (304,19) | Header. |
| 3 | Khóa học phụ trách navigation | (432,19) | Header. |
| 4 | Chấm bài navigation | (630,19) | Header. |
| 5 | Hộp thư hỗ trợ active navigation | (738,18) | Header, marker beside the active item. |
| 6 | Thông báo navigation | (924,19) | Header. |
| 7 | Notification bell/badge | (1244,64) | Header right, marker below the bell. |
| 8 | Mentor name/role/profile | (1538,69) | Header right, marker below profile. |
| 9 | Breadcrumb Hộp thư hỗ trợ | (48,126) | Breadcrumb. |
| 10 | Breadcrumb Chi tiết yêu cầu trao đổi | (207,126) | Current location. |
| 11 | Quay lại danh sách yêu cầu (ME-11) | (1180,190) | Back action, marker below button. |
| 12 | Mã tiến trình ME-12 badge | (58,258) | Hero, marker just left of badge. |
| 13 | Main title | (50,282) | Hero, marker just left of text. |
| 14 | Description | (50,335) | Hero, marker just left of text. |
| 15 | Mã yêu cầu value/loading | (1202,268) | Request identifier. |
| 16 | Trạng thái request | (1382,268) | Status chip. |
| 17 | Luồng hội thoại hỗ trợ heading | (58,477) | Conversation card, marker left of icon. |
| 18 | Socket synchronization claim | (660,461) | Unsupported realtime claim, marker before text/icon. |
| 19 | Empty-state illustration | (465,650) | Empty thread graphic, marker just left of illustration. |
| 20 | Empty-state heading | (342,764) | No messages currently shown, marker left of text. |
| 21 | Empty-state explanatory copy | (240,805) | Wait/sync text, marker left of text. |
| 22 | Socket/TLS 1.3 status badge | (320,884) | Unsupported transport claim, marker left of badge. |
| 23 | Reply composer heading | (58,1111) | Reply card, marker left of icon. |
| 24 | Character count | (856,1095) | Static 0 / 2000, marker before text. |
| 25 | Reply textarea | (58,1160) | Input field, marker left of box. |
| 26 | Locked reply warning | (52,1357) | Contract not connected copy, marker left of warning. |
| 27 | Send reply button (disabled) | (760,1358) | Action, marker left of button. |
| 28 | Resolve card heading | (1094,485) | Resolution card, marker left of icon. |
| 29 | Resolve explanatory copy | (1093,560) | Learner satisfaction text, marker left of copy. |
| 30 | Auto-settlement row | (1095,614) | Claim/value, marker left of text. |
| 31 | Satisfaction survey row | (1095,652) | Claim/value, marker left of text. |
| 32 | Mark resolved button (disabled) | (1095,706) | Action, marker left of button. |
| 33 | Minimum-exchange gate note | (1095,790) | Conflicts with #61 source, marker left of copy. |
| 34 | Mentor standards card heading | (1095,950) | Standards card, marker left of icon. |
| 35 | Standard 1: 24-hour SLA | (1095,991) | Claim, marker left of text. |
| 36 | Standard 2: sources/references | (1095,1047) | Claim, marker left of text. |
| 37 | Standard 3: privacy | (1095,1103) | Claim, marker left of text. |
| 38 | Help-guide link | (1095,1174) | Destination unknown, marker left of link. |
| 39 | Footer logo icon | (53,1565) | Footer, marker below logo. |
| 40 | Copyright/WCAG footer text | (80,1507) | Compliance/ownership claim, marker above text. |
| 41 | Quy chế Giảng viên link | (1050,1507) | Destination #, marker above link. |
| 42 | Tiêu chuẩn đánh giá link | (1230,1507) | Destination #, marker above link. |
| 43 | Hỗ trợ kỹ thuật link | (1415,1507) | Destination #, marker above link. |

## 8. Ordered completion steps and gates

1. Finish source/API/AC trace; preserve expected/current split and all unresolved policy questions above.
2. Confirm this plan is saved before creating markers, overlay, annotated image, or DD.
3. Create ME-12_markers.json for IDs 1–43; render SVG overlay and 2× annotated PNG without touching source PNG/HTML.
4. Visually inspect annotated output for readability, overlap, complete coverage, and in-bounds labels; adjust anchors if needed.
5. Write ME-12.md with sections A–F, 43 exact element rows, six complete event specifications, API mappings/errors, state/navigation matrix, traceability and explicit blockers.
6. Update list_screen.md ME-12 row and API #59–#61 reverse dependency codes from D to R based only on local route/module/query/model/test source; keep Draft, DERIVED, live schema and Study Web status explicit. Recompute aggregate counts.
7. Update dd_screens/PLAN.md only for ME-12 and session progress; do not start ME-13.
8. Update worklog with exact changed files, source findings and static audit results.
9. Static verify source asset hashes unchanged, image dimensions, JSON sequence/uniqueness/bounds, SVG ordering, 1:1 marker-to-DD rows, all event IDs, links and git diff --check. Do not run tests/runtime for this docs task.

## 9. Completion/status decision

Target deliverable is a complete and traceable DD package, but source-supported implementation decisions remain unresolved: loaded-thread layout/scale, reply length policy, attachment picker/asset purpose, resolve confirmation/minimum-exchange gate, post-resolve reply policy, and unsupported prototype claims. Expected final statuses are DD BLOCKED, IMPLEMENTATION BLOCKED, RUNTIME NOT VERIFIED; update these only if evidence added during this session resolves a blocker. A complete documentation pass does not imply DD READY or runtime verification.

# AD-10 — Kế hoạch Detailed Design

## 1. Phạm vi và kết quả cần tạo

- Chỉ xử lý Screen ID **AD-10 — Hàng đợi kiểm duyệt nội dung** trong phiên này.
- Thư mục nguồn: `apps/study-client/docs/screen_stitch/05_admin/AD-10_hang-doi-kiem-duyet-noi-dung/`.
- Giữ nguyên `screen.png` và `code.html`; tạo `screen_annotated.png`, `AD-10_markers.json`, SVG nguồn marker và `AD-10.md`.
- Đặc tả A–F, nối AC-33 với API #78 và handoff `Content.id` tới AD-11/#79; ghi rõ mọi discrepancy, không tự quyết định chính sách kiểm duyệt.
- Cập nhật `list_screen.md`, `screen_stitch/dd_screens/PLAN.md` và worklog AD-10. Không author AD-11.

## 2. Expected behavior và current behavior

### Expected behavior

- Inventory đề xuất route `/admin/content/pending`, actor Admin, AC-33 và API #78; hiển thị hàng đợi Content `PENDING_REVIEW`, lọc theo type/course/page, có empty state và chuyển `content_id` sang AD-11.
- AC-33 flow: mở queue → GET #78 → đọc Content/version/author bằng #79 → approve #80 hoặc reject #81 với reason → reload queue.
- Catalog/diagram #78 khai báo `GET /api/v1/admin/content/pending`, Bearer/Admin, query `type?:string`, `course?:int64`, `page?:int32`, response `ApiEnvelope<Content>`, lỗi 401/403/500. API DD còn `Draft — Needs Confirmation`.

### Current behavior đã xác minh

- Study Web hiện chỉ có docs/assets, ignored `dist`, `node_modules` và `tsconfig.tsbuildinfo`; editable source, package manifest, route và API client không có. Runtime `UNWIRED` / `NOT VERIFIED`.
- HTML là prototype tĩnh: search không có tên/handler; type/course select không có handler và dùng giá trị mẫu; refresh chỉ xoay icon/disable nút 700 ms bằng timer; “Kiểm tra nội dung mới” và pagination disabled; không có fetch/XHR/API URL/interval.
- HTML hiển thị table empty state và count `0/0`, page `1`, `System Normal`, RBAC/quality copy và auto-sync 30 giây. Các status/counter/auto-sync là nội dung tĩnh; không có row thật để mở.
- Current API #78 local route/module/query/model/validator và test source tồn tại. Role `ADMIN` được kiểm tra trước raw query validation/DB. Query đọc active legacy `contents` có `status='PENDING_REVIEW'`, optional exact `content_type` và signed-int64 `course_id`, count + page cố định 20 theo `id ASC`, page mặc định 1; response là `Page<ContentResponse>`.
- Local source trả 200 Page rỗng/trang quá cuối, thêm 422 cho numeric `course`/`page`, và safe 500 cho query/projection errors. Các lựa chọn Page, page defaults/order, exact-filter và soft-delete exclusion là `DERIVED`; catalog chỉ có 401/403/500 và Content đơn.
- `ContentResponse` chỉ có `id`, `course_id`, `content_type`, `title`, object `payload`, `status`, nullable `parent_id`, `order`. Không có author, course title, submitted timestamp, revision/version hay reviewer metadata.
- Checked-in legacy `DB.sql` và migrations 006/007 có BIGINT `contents`/`content_versions`; API #50/#51 hiện đặt logical row thành `PENDING_REVIEW`. V1-PILOT UUID `content_blocks`/`content_review_decisions` là mô hình khác; không chứng minh live schema/deployment.
- API #79 hiện cũng trả Content projection tám field, không join author/course/version. AC-33 metadata/version intent và #79/#80/#81 revision identity còn mở.

## 3. Discrepancies và blocker cần giữ trong DD

1. Catalog/AC #78 trả một Content; queue/page và local source trả `Page<Content>`.
2. Mockup search theo title/lecturer nhưng #78 không có keyword; type enum chưa được chốt; course filter cần int64 nhưng option HTML là slug mẫu.
3. Table header yêu cầu course name, lecturer/author và submitted time nhưng #78 response không có các trường/joins đó.
4. AC-33 cần version/author ở #79, nhưng current #78/#79 chỉ đọc logical Content row; revision binding/stale-item handling chưa quyết định.
5. Shared `ADMIN` guard không chứng minh moderation-specific permission; soft-deleted/stale queue visibility chưa được owner chốt.
6. Local legacy DDL/migrations tồn tại, trái ghi chú inventory “Content persistence chưa có trong DDL”; live schema/deploy và lựa chọn giữa legacy BIGINT với V1-PILOT UUID vẫn chưa xác minh.
7. Study Web chưa có app route/client. Các filter, refresh, polling, pagination, row action, error/session/navigation behavior chưa được triển khai.

## 4. Kế hoạch marker

Ảnh nguồn 1600×1461. Tạo **39 marker**, đánh số từ trên xuống dưới; đặt ở mép/whitespace cạnh phần tử để không che label hoặc trạng thái:

| Marker | Element được ánh xạ |
|---:|---|
| #1 | Logo/brand Admin |
| #2–#6 | Năm mục điều hướng Admin; mục Kiểm duyệt active |
| #7–#9 | System Normal, notification, Admin identity/avatar |
| #10–#11 | Global breadcrumb và badge RBAC tĩnh |
| #12–#13 | Breadcrumb kiểm duyệt và API #78 Active badge |
| #14–#15 | Tiêu đề hàng đợi và subtitle |
| #16–#17 | Hai status card tĩnh: trạng thái cổng và cấp Admin/RBAC |
| #18–#21 | Search, type select, course select, refresh |
| #22 | Table header gồm bảy cột: content ID/title/type/course/lecturer/submitted time/action |
| #23–#27 | Empty icon, heading, copy, disabled check button, auto-sync copy |
| #28–#31 | Count summary, Previous, current page, Next |
| #32–#35 | Quality notice icon/title/copy và rubric link |
| #36–#39 | Copyright và ba footer links |

- JSON dùng `number`, `x`, `y`, `label` theo pixel tọa độ ảnh gốc; mọi vòng marker, gồm stroke, phải nằm trong bounds.
- SVG có cùng 39 ID/tọa độ; render/composite ảnh 2× thành 3200×2922, không ghi lên `screen.png`.
- Section C của DD có đúng một hàng cho mỗi marker #1–#39. Element group như table headings được mô tả đầy đủ trong hàng tương ứng.

## 5. Event cần đặc tả

1. **EV-01 — Mở queue/load:** Admin route, auth/session và GET #78; phân biệt loading, empty, ready, 401/403/422/500/network. Ghi catalog-vs-local response discrepancy.
2. **EV-02 — Search:** ghi current input behavior không có handler/API; keyword không thuộc #78 nên không tự filter local hoặc tạo request.
3. **EV-03 — Lọc type:** HTML values `all/video/doc/quiz`; #78 nhận raw exact `type` string, không enum/normalization. Không tự map giá trị mẫu thành enum được duyệt.
4. **EV-04 — Lọc course:** HTML option values là slug; #78 yêu cầu numeric int64. Không suy course IDs hoặc tự gọi #73 nếu chưa có approved option-source flow.
5. **EV-05 — Refresh/auto-sync:** nút refresh chỉ spinner/disable 700 ms, không request; check button disabled; không có `setInterval`. “30 giây/lần” là claim tĩnh.
6. **EV-06 — Chọn Content → AD-11:** AC-33 chọn Content; handoff candidate là `data.items[].id` (`int64`) tới `content_id` của #79 sau khi Page/list contract được chốt. Empty state không có row/action hiện tại.
7. **EV-07 — Pagination:** current page `1`, count `0/0`, Previous/Next disabled và tĩnh. Local #78 Page candidate dùng page 1/default, size 20, id ASC; no page control handler.
8. **EV-08 — Shell, notice, rubric/footer:** anchors `#`, notification no-handler, status/RBAC/quality statements static; không suy ra monitoring, permission, legal policy hay rubric destination.

## 6. API/data/navigation trace

- #78: `GET /api/v1/admin/content/pending`; Bearer/Admin theo catalog. Query `type?:string`, `course?:int64`, `page?:int32`, no body. Direct response `ApiEnvelope<Content>`, errors 401/403/500. Local response Page/422/filters/order are derived candidates; no mutation/commit.
- Local Content item mapping: eight reusable fields listed in section 2; `data.items[].id` is the #79 numeric identity candidate. No author/course-name/submitted-time mapping is available.
- #79 is the next detail API and returns direct Content locally; AC-33 version/author requirement remains unresolved. #80/#81 decisions stay in AD-11 and are only named as later branches.
- After review, AC-33 asks to reload queue. Exact back navigation, query preservation, refetch/cache policy and success/error presentation are not implemented or approved.
- Cross-screen note: API `#078` source status should change `D→R` in the reverse API index after confirming current route/module/test source. API DD remains Draft. Inventory/global screen status stays DD/implementation blocked, runtime unverified.

## 7. Execution and verification order

1. [x] Docs preflight; exact-type selector and three selected worklogs recorded/read; context map, scope pages and registry consulted.
2. [x] Review AD-10 assets/DOM, AC-33, API catalog/DD/open questions, #78 current route/module/query/model/validator/test source, related Content/#79 projections and checked-in schema candidates.
3. [x] Save this plan before marker JSON/SVG, annotated PNG or screen DD.
4. [x] Create 39 ordered JSON/SVG markers and 2× annotated PNG; review image visually.
5. [x] Author A–F DD, 39 element rows, EV-01…EV-08, API/error trace, states/navigation and blockers.
6. [x] Update AD-10 and reverse API #078 source status plus global tracker/checkpoint.
7. [x] Static audit: source hashes/dimensions, JSON/XML, marker order/coordinates/bounds and C-row bijection, local links, inventory/folder/core-artifact counts, whitespace and final image. Do not run application tests/runtime.
8. [x] Finalize worklog and stop after AD-10; AD-11 remains a separate session.

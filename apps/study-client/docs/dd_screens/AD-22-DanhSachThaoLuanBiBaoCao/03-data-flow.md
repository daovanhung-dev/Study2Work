# AD-22 — Data Flow & State

## 1. Nguồn dữ liệu
| Field / object | Type | Source | Destination | Cập nhật khi |
|---|---|---|---|---|
| Chỉ liệt kê theo bằng chứng trong excerpt bên dưới | Theo DD/API source | API/inventory/design; status phải giữ nguyên | UI/state nêu ở DD nguồn | Theo event source |

## 2. State model

> Không tạo DTO/ViewModel mới khi chưa có contract. State, DTO và mapping được trích nguyên ngữ cảnh từ DD nguồn bên dưới.

## 3. API DTO → ViewModel mapping

### Trích từ DD nguồn: B. Mô tả luồng hoạt động tổng thể

### B.1. Expected flow — khi có route/client và contract được xác nhận

1. Admin mở candidate route sau khi auth và authorization policy của AC-37 được thực thi. Không dựa vào identity, “System Normal” hay “RBAC” text trong HTML.
2. Client chuẩn bị query `reason?`, `severity?`, `page?` theo đúng #97. Catalog chỉ nói các trường optional; default, allowed values, ordering, page size, kết hợp filter và việc `all` có phải sentinel hay không chưa được chốt trong catalog.
3. Gửi `GET /api/v1/admin/discussions/reported` với Bearer JWT. Không có request body. Contract trực tiếp là `ApiEnvelope<Page<Discussion>>`; success là HTTP 200 `DESIGN_RESOURCE_RETRIEVED`; errors là 401 `DESIGN_AUTHENTICATION_REQUIRED`, 403 `DESIGN_ACCESS_DENIED`, 500 `DESIGN_INTERNAL_ERROR`.
4. Khi response thành công, kiểm tra envelope và schema đúng contract rồi mới render. Không giả định `Discussion` chứa report count/reason/severity/reporter/report time; catalog #97 không khai báo các field này. Không lấy metrics/status từ mockup để lấp response.
5. Nếu Page không có item, hiện empty state theo nội dung/UX đã duyệt. Prototype ghi “không có báo cáo” và `0/0`, nhưng đây là nội dung tĩnh, không phải kết quả API. Không phân biệt `no reports` với `out-of-range page` bằng dữ liệu chưa được contract cung cấp.
6. Khi có một item và người dùng chọn nó, dùng Discussion `id` (int64 theo current #97 projection) làm `discussion_id` cho AD-23/#98. AC-37 yêu cầu detail đọc thread/comments/reports; current #98 source không đọc report relation, nên handoff dữ liệu nghiệp vụ chưa hoàn chỉnh.
7. Từ chối report / moderation / delete / audit / reload là các bước sau trong AC-37; xử lý tại AD-23 và chỉ sau khi #99/#100 cùng report lifecycle được xác nhận.

Không có contract cho debounce, cache, timeout, retry, request cancellation, refresh cadence hoặc auto-polling. Không tự thêm các hành vi này.

### B.2. Current prototype behavior

1. `code.html` render shell, breadcrumb, title, badge, hai số liệu tĩnh, input/select, table header, empty state, disabled pagination, ba policy cards và footer.
2. Search input và ba select không có listener. Các nav/footer anchors dùng `href="#"`; chuông notifications không có handler. Không có Study router hoặc API client.
3. Hai nút refresh gọi cùng `handleRefreshAction()`. Handler chỉ thêm/bỏ CSS class `animate-spin` cho icon trong 700 ms; không gửi request và không tải lại dữ liệu.
4. Pagination controls có `disabled` và `aria-disabled="true"`. Table hiện không có row. Cột `Thao tác` chỉ là header, không có nút chi tiết.
5. Câu “Hệ thống phân tích tự động kiểm tra định kỳ 60 giây”, metric `0`, `18`, “SẠCH VI PHẠM”, nội dung tuân thủ, policy SLA/ẩn tạm/audit đều là copy prototype. Trong HTML không có timer, metrics API, policy endpoint hay audit implementation.

### B.3. Current Study Server #97 source flow

1. Router đăng ký `GET /admin/discussions/reported`; giữ nguyên raw `reason`, `severity`, `page` và Authorization rồi gọi view #97.
2. `validate_current_user_request(..., role="ADMIN")` chạy trước page parsing và query DB. Fine-grained permission/tenant policy của AC-37 chưa được xác minh.
3. Validator mặc định `page=1`; chỉ page được parse/validate. Giá trị phải là signed int32 dương. `reason` và `severity` giữ raw, không chuẩn hóa/validate taxonomy.
4. Query đếm `COUNT(DISTINCT d.id)` và lấy các Discussion có report `OPEN` hoặc `IN_REVIEW`. `reason_code` và `severity` exact-match, kết hợp AND trên cùng report. Local query dùng page size 20 và sắp xếp theo report phù hợp mới nhất trước, rồi Discussion ID giảm dần. Các lựa chọn này là `DERIVED` trong #97 DD, không phải quy tắc trực tiếp từ catalog.
5. Local mapping trả `id`, `course_id`, title lấy từ content đã gộp whitespace và cắt 120 ký tự, `content`, `author`, `status`, `comments:[]`. Không có report metadata. Missing/invalid required projection như course/author/status gây safe 500 thay vì bịa field.
6. Query/mapping lỗi trả 500 `DESIGN_INTERNAL_ERROR`; lỗi DB được rollback an toàn. GET không commit, không insert/update/delete report, Discussion hoặc audit. Không tìm thấy row hoặc page ngoài phạm vi trả 200 Page rỗng trong local implementation.
7. Invalid page trả 422 `DESIGN_VALIDATION_ERROR` từ local source; đây là `DERIVED`, vì API catalog #97 không liệt kê 422.

### B.4. API contract và field mapping

| API | Direct contract | Current local evidence | AD-22 consequence |
|---|---|---|---|
| #97 queue | `GET /api/v1/admin/discussions/reported`; Bearer JWT, role Admin; query `reason?:string`, `severity?:string`, `page?:int32`; no body; `ApiEnvelope<Page<Discussion>>`; 200 `DESIGN_RESOURCE_RETRIEVED`; 401/403/500 theo catalog. | Route, view, query, validator, model hiện có; shared `ADMIN` guard. Local page default 1, size 20, unique Discussion grain, OPEN/IN_REVIEW, exact filters, latest-report ordering là DERIVED. Local invalid page thêm 422. | Dùng đúng direct params/response; không gửi `q`/status/size/order; không xem local derived rules như product-approved. |
| #98 detail (handoff) | `GET /api/v1/admin/discussions/{discussion_id}`; Bearer JWT, role Admin; path int64; `ApiEnvelope<Page<Discussion>>`; 200, 401/403/404/500. | Current route/module tồn tại, nhận int64 và trả Discussion detail projection; không query `discussion_reports`. API #98 DD vẫn ghi `UNWIRED / NOT_FOUND`, xung đột với source. | Discussion ID có thể định danh candidate route; AC-37 reports/comments handoff chưa đáp ứng. Không mở AD-23 như đã source-verified. |

`Page<Discussion>` local response chứa `items` và `pagination{page,size,total,total_pages}`. Đây là response hiện tại của code; không khẳng định đây là toàn bộ direct schema chỉ từ UI prototype. Catalog không cung cấp fields `report_count`, `reason`, `severity`, `reporter`, `reported_at`, queue status hay metric. `discussion_reports` chỉ có trong candidate DDL/migration 014 và query #97; live schema/migration deployment và writer chưa xác minh. Không thấy `INSERT INTO discussion_reports` hoặc report creation endpoint trong Study app/tests hiện tại.

### Trích từ DD nguồn: E. Ma trận trạng thái và điều hướng

### State matrix

| State | Điều kiện / evidence | Hành vi được xác nhận |
|---|---|---|
| `UNWIRED` | Study Web tracked `src`/router/API client không có; candidate route chỉ trong inventory/prototype. | Không tuyên bố page runtime hoặc auth flow đã hoạt động. |
| `PROTOTYPE_STATIC` | HTML tải độc lập; data, counts, policy copy và status đều literal. | Hiển thị mockup; controls không có filter/navigation/network effect trừ refresh icon animation. |
| `LOADING` (expected) | Inventory state checklist; current UI không implement. | Loading component/skeleton, cancellation và retry chưa có design/contract. |
| `READY` (expected) | Successful #97 response có items. | Chỉ render fields được response trả; report-specific columns đang thiếu field contract. |
| `EMPTY` (expected/local API possible) | #97 trả Page không có items; local source cũng trả empty page khi out-of-range. | Empty content copy cần được duyệt; không kết luận mọi Discussion compliant hoặc report đã xử lý. |
| `ERROR` (expected) | API/auth/query error; inventory có error state. | Preserve HTTP/business code; cụ thể message, retry, SH-05 handling và trace display chưa được định nghĩa cho AD-22. |
| `FILTER_UNSUPPORTED` | Search/status controls trong prototype; #97 không nhận q/status. | Không gửi filter request hoặc giả lập kết quả. |
| `PAGE_INVALID` | Current local source nhận page sai/non-positive/out-of-int32. | Local DERIVED 422 `DESIGN_VALIDATION_ERROR`; catalog #97 không liệt kê 422. |
| `AUTH_REQUIRED / ACCESS_DENIED` | Direct #97 401/403; local guard role `ADMIN`. | Không khẳng định AC permission mapping; route recovery/SH-05 behavior cần shared policy. |
| `HANDOFF_INCOMPLETE` | Row selected expected, nhưng #97 không trả report fields và #98 current source không đọc reports. | AD-23 handoff block; không tự tạo detail payload/report ID. |
| `POLICY_COPY_UNVERIFIED` | Cards claim threshold, SLA, audit trail; no matching current source located. | Copy không được dùng làm validation/business rule hoặc service guarantee. |

### Navigation / handoff matrix

| From | To / API | Data passed | Current status |
|---|---|---|---|
| Admin shell → AD-22 | Candidate `/admin/discussions/reported` | None defined beyond route. | Shell anchors are `#`; Study Web route absent. |
| AD-22 load/filter → #97 | GET reported list | `reason?`, `severity?`, `page?`; Bearer JWT. No `q`, `status`, `size`, or body. | Study Server route wired locally; client not wired; report writer/live DB unverified. |
| AD-22 row → AD-23 | `/admin/discussions/:discussionId/moderate`; then #98 | Candidate positive int64 Discussion ID from #97 item. No report ID in response. | Row action absent; #98 source exists but report lookup is absent and DD status conflicts. |
| AD-23 → AD-22 refresh | #99/#100 then #97 | Action/reason or Discussion ID per later contracts; not specified in AD-22. | Out of scope; #99/#100 current source not registered per source boundary. |

## 4. Luồng đọc (Read)
- Orchestration từ inventory: GET #97 → detail AD-23; không tự giả lập endpoint report discussion.
- Chi tiết current/source mapping: xem [API Integration](04-api-integration.md) và DD nguồn.

## 5. Luồng ghi (Write)
- Chỉ mô tả mutation được DD/API source nêu; không thêm endpoint hoặc side effect.
- Source trace: [AD-22](../../screen_stitch/05_admin/AD-22_danh-sach-thao-luan-bi-bao-cao/AD-22.md)

## 6. Cache / concurrency / lifecycle
- Cache, race, cleanup, pagination: xem các section source bên dưới; nếu không có bằng chứng thì để `CẦN_XÁC_NHẬN`.

## 7. Data errors & security
- Theo error/security/source-status section của DD nguồn; không coi state trong mockup là runtime behavior.

## 8. Trace
[Events](02-events.md) · [API](04-api-integration.md) · [Rules](05-business-rules.md)

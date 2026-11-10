# AD-22 — API Integration

> API/status dưới đây lấy từ inventory và DD nguồn. Package-local API IDs chỉ là alias truy vết cho API catalog reference; chúng không tạo contract mới. `R/S/D/M/UX` hoặc nhãn cục bộ là evidence status, không tự động xác nhận UI/runtime. Route/contract thiếu nguồn phải giữ `CẦN_XÁC_NHẬN`.

## 1. API usage matrix
| API ID (package-local usage alias) | Source catalog ref | Method/path | Event | Auth |
|---|---|---|---|---|
| `AD-22-API-001` | #97 | See source contract excerpt | Source event IDs are preserved in [Events](02-events.md) | See source auth/permission evidence |

## 2. Contract / source detail

- API refs trong inventory: #97
- Orchestration/data notes: GET #97 → detail AD-23; không tự giả lập endpoint report discussion.
- BE/source status và gate: **R** local #97 route/module/query/validator/model source; API DD Draft. **BLOCK:** Chưa tìm thấy report writer hoặc xác minh live schema; #97 không trả count/reason/severity/reporter/time cho cột UI; search/status/pending priority/AC permission vs `ADMIN` chưa chốt; Study Web UNWIRED
- Contract sources and discrepancies are preserved in the source excerpts below.

### Trích từ DD nguồn: B.1. Expected flow — khi có route/client và contract được xác nhận

1. Admin mở candidate route sau khi auth và authorization policy của AC-37 được thực thi. Không dựa vào identity, “System Normal” hay “RBAC” text trong HTML.
2. Client chuẩn bị query `reason?`, `severity?`, `page?` theo đúng #97. Catalog chỉ nói các trường optional; default, allowed values, ordering, page size, kết hợp filter và việc `all` có phải sentinel hay không chưa được chốt trong catalog.
3. Gửi `GET /api/v1/admin/discussions/reported` với Bearer JWT. Không có request body. Contract trực tiếp là `ApiEnvelope<Page<Discussion>>`; success là HTTP 200 `DESIGN_RESOURCE_RETRIEVED`; errors là 401 `DESIGN_AUTHENTICATION_REQUIRED`, 403 `DESIGN_ACCESS_DENIED`, 500 `DESIGN_INTERNAL_ERROR`.
4. Khi response thành công, kiểm tra envelope và schema đúng contract rồi mới render. Không giả định `Discussion` chứa report count/reason/severity/reporter/report time; catalog #97 không khai báo các field này. Không lấy metrics/status từ mockup để lấp response.
5. Nếu Page không có item, hiện empty state theo nội dung/UX đã duyệt. Prototype ghi “không có báo cáo” và `0/0`, nhưng đây là nội dung tĩnh, không phải kết quả API. Không phân biệt `no reports` với `out-of-range page` bằng dữ liệu chưa được contract cung cấp.
6. Khi có một item và người dùng chọn nó, dùng Discussion `id` (int64 theo current #97 projection) làm `discussion_id` cho AD-23/#98. AC-37 yêu cầu detail đọc thread/comments/reports; current #98 source không đọc report relation, nên handoff dữ liệu nghiệp vụ chưa hoàn chỉnh.
7. Từ chối report / moderation / delete / audit / reload là các bước sau trong AC-37; xử lý tại AD-23 và chỉ sau khi #99/#100 cùng report lifecycle được xác nhận.

Không có contract cho debounce, cache, timeout, retry, request cancellation, refresh cadence hoặc auto-polling. Không tự thêm các hành vi này.

### Trích từ DD nguồn: B.4. API contract và field mapping

| API | Direct contract | Current local evidence | AD-22 consequence |
|---|---|---|---|
| #97 queue | `GET /api/v1/admin/discussions/reported`; Bearer JWT, role Admin; query `reason?:string`, `severity?:string`, `page?:int32`; no body; `ApiEnvelope<Page<Discussion>>`; 200 `DESIGN_RESOURCE_RETRIEVED`; 401/403/500 theo catalog. | Route, view, query, validator, model hiện có; shared `ADMIN` guard. Local page default 1, size 20, unique Discussion grain, OPEN/IN_REVIEW, exact filters, latest-report ordering là DERIVED. Local invalid page thêm 422. | Dùng đúng direct params/response; không gửi `q`/status/size/order; không xem local derived rules như product-approved. |
| #98 detail (handoff) | `GET /api/v1/admin/discussions/{discussion_id}`; Bearer JWT, role Admin; path int64; `ApiEnvelope<Page<Discussion>>`; 200, 401/403/404/500. | Current route/module tồn tại, nhận int64 và trả Discussion detail projection; không query `discussion_reports`. API #98 DD vẫn ghi `UNWIRED / NOT_FOUND`, xung đột với source. | Discussion ID có thể định danh candidate route; AC-37 reports/comments handoff chưa đáp ứng. Không mở AD-23 như đã source-verified. |

`Page<Discussion>` local response chứa `items` và `pagination{page,size,total,total_pages}`. Đây là response hiện tại của code; không khẳng định đây là toàn bộ direct schema chỉ từ UI prototype. Catalog không cung cấp fields `report_count`, `reason`, `severity`, `reporter`, `reported_at`, queue status hay metric. `discussion_reports` chỉ có trong candidate DDL/migration 014 và query #97; live schema/migration deployment và writer chưa xác minh. Không thấy `INSERT INTO discussion_reports` hoặc report creation endpoint trong Study app/tests hiện tại.

## 3. API không sử dụng
- Không bổ sung API ngoài inventory và DD nguồn. Nếu screen không cần API, trạng thái phải được xác nhận từ source DD.

## 4. References
[Events](02-events.md) · [Data flow](03-data-flow.md) · [Tests](07-test-cases.md) · [Source DD](../../screen_stitch/05_admin/AD-22_danh-sach-thao-luan-bi-bao-cao/AD-22.md)

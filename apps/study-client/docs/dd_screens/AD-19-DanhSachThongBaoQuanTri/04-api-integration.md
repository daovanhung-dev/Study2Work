# AD-19 — API Integration

> API/status dưới đây lấy từ inventory và DD nguồn. Package-local API IDs chỉ là alias truy vết cho API catalog reference; chúng không tạo contract mới. `R/S/D/M/UX` hoặc nhãn cục bộ là evidence status, không tự động xác nhận UI/runtime. Route/contract thiếu nguồn phải giữ `CẦN_XÁC_NHẬN`.

## 1. API usage matrix
| API ID (package-local usage alias) | Source catalog ref | Method/path | Event | Auth |
|---|---|---|---|---|
| `AD-19-API-001` | #92 | See source contract excerpt | Source event IDs are preserved in [Events](02-events.md) | See source auth/permission evidence |

## 2. Contract / source detail

- API refs trong inventory: #92
- Orchestration/data notes: Catalog #92 chỉ có status/channel/page và direct ApiEnvelope<Notification>; local #92 trả derived Page<Notification>, delivery-backed rows. No search, recipient/send-time fields or metrics mapping. AD-20 CTA path is /admin/notifications/create in HTML vs inventory /admin/notifications/new; guideline link unresolved.
- BE/source status và gate: **R** local #92 route/validator/query/model/view/focused-test source; API DD Draft. **DD BLOCKED; IMPLEMENTATION BLOCKED:** catalog singleton vs local Page; enum/search/metric and recipient/send-time mapping; AC-36 permission vs ADMIN; notification grain/live schema; CTA/guidelines destinations; Study Web UNWIRED; **RUNTIME NOT VERIFIED**
- Contract sources and discrepancies are preserved in the source excerpts below.

### Trích từ DD nguồn: API #92 — request/response và lỗi

| Thành phần | Direct contract | Current local source |
|---|---|---|
| Method / URI | GET /api/v1/admin/notifications | Route GET được đăng ký cùng đường dẫn. |
| Auth | Bearer JWT; role=Admin theo catalog. AC-36 dùng notification-management permission. | Shared guard role ADMIN; chạy trước page parse/query. Fine-grained permission chưa có. |
| Query | status?:string, channel?:string, page?:int32; không có size/search. | status/channel nguyên văn; page mặc định 1 và >=1 signed int32. Không trim, lowercase/uppercase normalization hoặc enum validation cho filter. |
| Body | Không có. | Không đọc request body. |
| Success | HTTP 200, DESIGN_RESOURCE_RETRIEVED, ApiEnvelope<Notification>. | Envelope success/businessCode/message/data/meta/traceId; data là Page với items và pagination. Direct response shape mismatch. |
| Item | Notification fields theo reusable schema ở trên. | Pydantic model literal EMAIL/PUSH và FAILED/QUEUED/SENT; optional read_at/scheduled_at mặc định None và được serializer bỏ qua. |
| 401 / 403 | DESIGN_AUTHENTICATION_REQUIRED / DESIGN_ACCESS_DENIED. | Shared JWT/ADMIN guard trước truy vấn. HTTP 403 cho role thiếu; không chứng minh permission chi tiết AC-36. |
| 422 | Không nằm trong direct #92 catalog error list. | DERIVED local page error DESIGN_VALIDATION_ERROR; field page, INT_PARSING hoặc GREATER_THAN_EQUAL. Kiểm tra sau auth và trước DB. |
| 503 | DESIGN_DEPENDENCY_UNAVAILABLE. | Operational/connection-invalidated DB failures được map 503; owner chưa xác nhận trigger. |
| 500 | DESIGN_INTERNAL_ERROR. | SQL errors khác, lỗi projection/mapping hoặc response validation trả 500; lỗi mapping rollback an toàn. |
| Empty / page ngoài range | Không định nghĩa response cụ thể. | HTTP 200 Page rỗng; message “No notifications found.”, total_pages=0 khi total=0. |
| Side effect | GET/read. | Hai read queries; không commit, không gọi delivery provider. |

No application retry, request deduplication, local cache, timeout value or client-side refresh policy is present in the checked-in Study Web source. Do not add one based on the mockup.

### Trích từ DD nguồn: Navigation data contract

- AD-19 → AD-20: inventory relationship; current CTA uses a conflicting path. Không có payload được định nghĩa. #93 request body thuộc AD-20.
- AD-19 → AD-21: nếu owner duyệt row grain/response và có item.id:int64, candidate path parameter notificationId. Không truyền recipient ID, campaign ID hay operation UUID bằng suy luận.
- AD-21 → AD-19: filter/page preservation và refresh semantics chưa được định nghĩa. AC-36 chỉ yêu cầu reload management sau action.
- AD-19 → SH-07: chỉ nếu một API trả operation_id theo contract được duyệt. API #92 không trả operation; #93 bridge còn open.
- Back/session-expiry navigation, URL-state persistence và browser history chưa được Study Web source xác minh.

### Trích từ DD nguồn: Artifact và truy vết

- [x] 48 marker tuần tự/unique có trong JSON, SVG và DD; tọa độ dùng nguồn 1600×1411.
- [x] screen.png giữ nguyên; screen_annotated.png là 3200×2822 và đã visual review.
- [x] Mỗi marker ánh xạ tới đúng một element row; element/event IDs được liệt kê rõ.
- [x] Có plan trước khi tạo markers, image annotation và DD.
- [x] Inventory/AC/catalog/current source/test evidence được dẫn; expected và current không bị nhập làm một.

### Trích từ DD nguồn: Logic và contract

- [x] Có event load, search, filter, reset, refresh, CTA, row handoff, pagination, guidelines và shell navigation.
- [x] API #92 direct response/errors được tách khỏi Page/error behavior của current source.
- [x] Không tự thêm search query, metrics API, recipient field, status/channel alias, policy rule hoặc route.
- [x] Empty/loading/ready/error/auth/permission/pagination/navigation states và unresolved handoff được ghi.
- [ ] Owner xác nhận singleton vs Page, pagination, enum/filter/search/metrics, permission/grain/schema, CTA/guidelines route và operation bridge.
- [ ] Study Web route/API client, live DB/migrations, runtime permission and response behavior được xác minh.
- [ ] Do các mục blocker còn mở, DD status chưa đạt DD READY; implementation và runtime chưa verified.

## 3. API không sử dụng
- Không bổ sung API ngoài inventory và DD nguồn. Nếu screen không cần API, trạng thái phải được xác nhận từ source DD.

## 4. References
[Events](02-events.md) · [Data flow](03-data-flow.md) · [Tests](07-test-cases.md) · [Source DD](../../screen_stitch/05_admin/AD-19_danh-sach-thong-bao-quan-tri/AD-19.md)

# ME-11 — API Integration

> API/status dưới đây lấy từ inventory và DD nguồn. Package-local API IDs chỉ là alias truy vết cho API catalog reference; chúng không tạo contract mới. `R/S/D/M/UX` hoặc nhãn cục bộ là evidence status, không tự động xác nhận UI/runtime. Route/contract thiếu nguồn phải giữ `CẦN_XÁC_NHẬN`.

## 1. API usage matrix
| API ID (package-local usage alias) | Source catalog ref | Method/path | Event | Auth |
|---|---|---|---|---|
| `ME-11-API-001` | #58 | See source contract excerpt | Source event IDs are preserved in [Events](02-events.md) | See source auth/permission evidence |

## 2. Contract / source detail

- API refs trong inventory: #58
- Orchestration/data notes: GET #58; chuyển `data[].id` sang ME-12; không tự thêm contact fields.
- BE/source status và gate: **R**; **BLOCK:** #58 có route/view/query/model/test source và DDL/migration 008 local, nhưng projection/lifecycle là DERIVED, live schema chưa xác minh; loaded-row design, status grouping/counts, course slug→int64 mapping, full-thread không pagination, AC-24 precondition vs empty state, SLA/realtime/Meet claims và Study Web UNWIRED còn chặn
- Contract sources and discrepancies are preserved in the source excerpts below.

### Trích từ DD nguồn: A.2. Điều kiện vào/ra và API boundary

- **Expected entry:** Mentor mở ME-11 từ ME-01 hoặc điều hướng được duyệt. AC-24 bắt đầu bằng GET #58; inventory cho phép `loading/empty/ready/error` và yêu cầu danh sách theo khóa học Mentor phụ trách.
- **Current API #58:** route nhận `course_id` tùy chọn kiểu positive signed-int64, `status` tùy chọn string; Bearer header; response `ApiEnvelope<SupportRequest[]>`. API DD #58 vẫn `Draft — Needs Confirmation`; collection shape, BIGINT schema, lifecycle và attachment mapping là fallback được chọn cho local implementation, chưa phải contract-owner approval.
- **Expected exit:** khi chọn request đã hiển thị, chuyển `data[].id` sang ME-12. F09 định tuyến tiếp #59 → #60 → #61 trong ME-12. Không gọi #59 từ ME-11 theo inventory hiện hành.
- **Không có Student producer xác nhận:** source route hiện có các Mentor support APIs #58–#61, nhưng không tìm thấy endpoint Student tạo support request. Không suy ra CTA/tạo mới cho Student từ empty-state copy.
- **Dữ liệu trả về:** #58 gồm toàn bộ `messages[]` cho từng request, dù #59 cũng đọc thread. Không phân trang/giới hạn; trước khi triển khai inbox cần chốt payload grain và cách dùng thread từ list.

### Trích từ DD nguồn: B.1. API #58 — request, response và lỗi

| Mục | Contract hiện có |
|---|---|
| API ID / method | #58 — `GET` |
| Endpoint | `/api/v1/mentor/support/requests` |
| Authentication | `Authorization: Bearer <token>`; shared current-user guard yêu cầu role `MENTOR`. |
| Query | `course_id?: int64`, `1 ≤ value ≤ 2^63−1`; `status?: string` tùy chọn, không enum-validate. Không có path params/body. |
| Ownership | Request luôn lọt qua `courses.mentor_id = mentor_id`; nếu filter course tồn tại nhưng thuộc mentor khác → 403. Course ID không tồn tại không lỗi, collection rỗng. |
| Filter semantics | Optional `course_id` và `status` kết hợp AND; status exact match. Giá trị status lạ không có match → 200 `data: []`. |
| Ordering | Requests `created_at DESC, id DESC`; messages `created_at ASC, id ASC`; attachment order theo `asset_position`. Không có pagination, cursor hoặc page size. |
| Success | 200, `success=true`, `businessCode=DESIGN_RESOURCE_RETRIEVED`, `message` là `Support requests retrieved.` hoặc `No support requests found.`, `data: SupportRequest[]`, `meta:{}`, `traceId`. |
| Errors | 401 `DESIGN_AUTHENTICATION_REQUIRED`; 403 `DESIGN_ACCESS_DENIED`; 422 `DESIGN_VALIDATION_ERROR` cho query `course_id` invalid; 500 `DESIGN_INTERNAL_ERROR` cho DB/projection/envelope failure. Error envelope dùng `data:null`; không lộ stack/raw nội bộ. |
| Transaction | GET không commit. SQL/projection/attachment mapping lỗi gọi rollback an toàn trước 500. Course owner mismatch cũng rollback trước 403. |
| Response field mapping | Request: `id`, `course_id`, `student`, `status`, full `messages[]`, `created_at`, optional `resolved_at`. Student/author summary: `id`, `full_name`, optional `avatar_url`. Message: `id`, `author`, `content`, `attachments[]`, `created_at`. UploadAsset chỉ được ghép khi upload ID/author/course/role-purpose/`UPLOADED` match. Optional null fields bị loại khỏi JSON. |
| Giới hạn projection | Không có `course_title`, count, unread state, last activity, SLA timestamp, student contact data, pagination hoặc summary-only thread. Payload toàn bộ messages có thể lớn. |

**Source trace:** [#58 route](../../../../study-server/app/api/v1.py) → [view/auth/query orchestration](../../../../study-server/app/modules/mentor/api_58_mentor_support_requests/view.py) → [SQL](../../../../study-server/app/modules/mentor/api_58_mentor_support_requests/query.py) → [models](../../../../study-server/app/modules/mentor/api_58_mentor_support_requests/models.py). API DD [verification](../../../../study-server/docs/dd/58_mentor_support_requests/VERIFICATION_REPORT.md) reports route/module/model/test source wired, while retaining Draft status and derived local fallback decisions. Historical focused tests are recorded there; they use fake sessions and do not verify live DB/migration deployment.

## 3. API không sử dụng
- Không bổ sung API ngoài inventory và DD nguồn. Nếu screen không cần API, trạng thái phải được xác nhận từ source DD.

## 4. References
[Events](02-events.md) · [Data flow](03-data-flow.md) · [Tests](07-test-cases.md) · [Source DD](../../screen_stitch/04_mentor/ME-11_hop-thu-ho-tro-hoc-vien/ME-11.md)

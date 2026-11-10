# AD-04 — API Integration

> API/status dưới đây lấy từ inventory và DD nguồn. Package-local API IDs chỉ là alias truy vết cho API catalog reference; chúng không tạo contract mới. `R/S/D/M/UX` hoặc nhãn cục bộ là evidence status, không tự động xác nhận UI/runtime. Route/contract thiếu nguồn phải giữ `CẦN_XÁC_NHẬN`.

## 1. API usage matrix
| API ID (package-local usage alias) | Source catalog ref | Method/path | Event | Auth |
|---|---|---|---|---|
| `AD-04-API-001` | #69 | See source contract excerpt | Source event IDs are preserved in [Events](02-events.md) | See source auth/permission evidence |
| `AD-04-API-002` | #70 | See source contract excerpt | Source event IDs are preserved in [Events](02-events.md) | See source auth/permission evidence |

## 2. Contract / source detail

- API refs trong inventory: #69, #70
- Orchestration/data notes: Numeric ID từ AD-03; GET #69 → PUT #70 → GET #69. Catalog/AC bỏ body; local strict body `full_name, phone, avatar_url, role` là `DERIVED`; không gửi email/status/adminNotes hoặc tự map `lecturer`.
- BE/source status và gate: **R**; #70 source-backed locally nhưng body/role `DERIVED`; **DD BLOCKED; IMPLEMENTATION BLOCKED:** body approval, role/PII/permission/ID-route/gate policy và Study Web `UNWIRED`; **RUNTIME NOT VERIFIED**
- Contract sources and discrepancies are preserved in the source excerpts below.

### Trích từ DD nguồn: API #69 profile và #70 body candidate

| Field | Kiểu / quy tắc hiện có | Dùng trên AD-04 |
|---|---|---|
| `id` | `int64` path/ID candidate trong local legacy API. | Khóa user cho GET/PUT; không tự ánh xạ `USR-9281-VN` sang số. Live schema/deploy chưa xác minh. |
| `full_name` | #69 trả `string`; local #70 body yêu cầu string, trim, không rỗng, tối đa 150 ký tự. Body/rule #70 là `DERIVED`. | Candidate field có thể sửa sau khi body được duyệt. |
| `email` | #69 trả `string`; không có trong body/update #70. | Chỉ đọc; quy tắc hiển thị/masking PII chưa duyệt. |
| `phone` | #69 trả `string \| null`; local #70 yêu cầu key, nhận string/null, trim, blank thành null, tối đa 20 ký tự nếu là string. | Không có input trong prototype; phải giữ nguyên từ #69 nếu hợp đồng full-replacement được duyệt. |
| `avatar_url` | #69 trả `string \| null`; local #70 yêu cầu key, nhận string/null, trim, blank thành null; không kiểm tra URL syntax/length. | Không có input trong prototype; phải giữ nguyên từ #69 nếu hợp đồng full-replacement được duyệt. |
| `role` | #69 trả `string`; local #70 body chỉ nhận `STUDENT`, `MENTOR`, `ADMIN`. Allowlist và rule chuyển vai trò đều `DERIVED`. | Prototype hiển thị `student/lecturer/admin`; không tự map `lecturer` thành `MENTOR`. |
| `status` | #69 trả `string`; không thuộc body/update #70. #71 là API trạng thái riêng, ngoài mutation AD-04. | Chỉ đọc theo policy; không gửi `active/locked/pending` vào #70. |
| `adminNotes` | Không có trong #69/#70. | Không lưu/gửi; prototype textarea hiện bị khóa. Cần contract riêng nếu nghiệp vụ yêu cầu. |
| `created_at`, `updated_at` | Có trong UserProfile success response. | Hiển thị nếu có thiết kế và định dạng được duyệt; không coi actor/audit là các timestamp này. |

### Trích từ DD nguồn: Nguồn truy vết

- [Inventory](../../list_screen.md) · [Kế hoạch tổng](../../screen_stitch/dd_screens/PLAN.md) · [AD-04 plan](../../screen_stitch/05_admin/AD-04_chinh-sua-nguoi-dung/AD-04_PLAN.md) · [AD-03](../../screen_stitch/05_admin/AD-03_chi-tiet-nguoi-dung/AD-03.md)
- [Ảnh gốc](../../screen_stitch/05_admin/AD-04_chinh-sua-nguoi-dung/screen.png) · [Ảnh chú thích](../../screen_stitch/05_admin/AD-04_chinh-sua-nguoi-dung/screen_annotated.png) · [HTML prototype](../../screen_stitch/05_admin/AD-04_chinh-sua-nguoi-dung/code.html) · [Marker map](../../screen_stitch/05_admin/AD-04_chinh-sua-nguoi-dung/AD-04_markers.json) · [SVG overlay](../../screen_stitch/05_admin/AD-04_chinh-sua-nguoi-dung/AD-04_markers.svg)
- [API catalog](../../../../../docs/lists/list_api.md) · [AC-31 diagram](../../../../study-server/docs/diagrams/AC_UNICA/AC_04_ADMIN_MANAGEMENT.drawio)
- API #70 DD: [Overview](../../../../study-server/docs/dd/70_admin_user_update/02_Overview.md) · [Request](../../../../study-server/docs/dd/70_admin_user_update/03_Request.md) · [Response](../../../../study-server/docs/dd/70_admin_user_update/04_Response.md) · [Mapping](../../../../study-server/docs/dd/70_admin_user_update/05_Data_Mapping.md) · [Errors](../../../../study-server/docs/dd/70_admin_user_update/06_Error.md) · [Open questions](../../../../study-server/docs/dd/70_admin_user_update/OPEN_QUESTIONS.md)
- API #70 source: [route](../../../../study-server/app/api/v1.py) · [model](../../../../study-server/app/modules/admin/api_70_admin_user_update/models.py) · [validation](../../../../study-server/app/modules/admin/api_70_admin_user_update/validate.py) · [query](../../../../study-server/app/modules/admin/api_70_admin_user_update/query.py) · [view](../../../../study-server/app/modules/admin/api_70_admin_user_update/view.py) · [focused test source](../../../../study-server/tests/modules/admin/api_70_admin_user_update/test_admin_user_update.py)
- [Study Web boundary](../../../../../.agents/web-work/study/AGENTS.md) · [Study Web design target](../../../../../.agents/web-study/design.md) · [Study Server API source status](../../../../../.agents/project/source-status.md)

### Trích từ DD nguồn: Response và lỗi API

| API | Thành công | HTTP/business error theo catalog/source | UI mapping cần thiết |
|---|---|---|---|
| #69 GET | 200 `DESIGN_RESOURCE_RETRIEVED`; `ApiEnvelope<UserProfile>`. | 401 `DESIGN_AUTHENTICATION_REQUIRED`; 403 `DESIGN_ACCESS_DENIED`; 404 `DESIGN_RESOURCE_NOT_FOUND`; 500 `DESIGN_INTERNAL_ERROR`. | loading → ready; 401/403 auth states; 404 not-found; 500/network error. Error envelope `data:null`; không hiển thị fake empty profile. |
| #70 PUT | 200 `DESIGN_RESOURCE_UPDATED`; `ApiEnvelope<UserProfile>`. | 401 `DESIGN_AUTHENTICATION_REQUIRED`; 403 `DESIGN_ACCESS_DENIED`; 404 `DESIGN_RESOURCE_NOT_FOUND`; 422 `DESIGN_VALIDATION_ERROR`; 500 `DESIGN_INTERNAL_ERROR`. | 422 giữ form và gắn lỗi theo field/message nếu response có thông tin; schema lỗi cụ thể cần đồng bộ. 401/403 xử lý theo auth shell; 404 user không còn tồn tại; 500/network giữ input. Error envelope `data:null`. |

## 3. API không sử dụng
- Không bổ sung API ngoài inventory và DD nguồn. Nếu screen không cần API, trạng thái phải được xác nhận từ source DD.

## 4. References
[Events](02-events.md) · [Data flow](03-data-flow.md) · [Tests](07-test-cases.md) · [Source DD](../../screen_stitch/05_admin/AD-04_chinh-sua-nguoi-dung/AD-04.md)

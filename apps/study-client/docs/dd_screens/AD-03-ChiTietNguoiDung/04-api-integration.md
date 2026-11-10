# AD-03 — API Integration

> API/status dưới đây lấy từ inventory và DD nguồn. Package-local API IDs chỉ là alias truy vết cho API catalog reference; chúng không tạo contract mới. `R/S/D/M/UX` hoặc nhãn cục bộ là evidence status, không tự động xác nhận UI/runtime. Route/contract thiếu nguồn phải giữ `CẦN_XÁC_NHẬN`.

## 1. API usage matrix
| API ID (package-local usage alias) | Source catalog ref | Method/path | Event | Auth |
|---|---|---|---|---|
| `AD-03-API-001` | #69 | See source contract excerpt | Source event IDs are preserved in [Events](02-events.md) | See source auth/permission evidence |

## 2. Contract / source detail

- API refs trong inventory: #69
- Orchestration/data notes: Nhận `id` từ AD-02/#68 → GET #69; không đưa PII vào URL. #69 không trả audit/sync; không nhận diện `204/NULL_PAYLOAD` như success.
- BE/source status và gate: **R**; **DD BLOCKED; IMPLEMENTATION BLOCKED:** #69 source-backed locally, nhưng ADMIN permission mapping, legacy/live schema, PII/enum/lifecycle và audit/retention policy còn mở; Study Web UNWIRED; prototype 204/audit/sync claims không được API #69 hỗ trợ; RUNTIME NOT VERIFIED
- Contract sources and discrepancies are preserved in the source excerpts below.

### Trích từ DD nguồn: UserProfile mapping khả dụng từ API #69

| Response field | Kiểu / null | AD-03 sử dụng | Giới hạn |
|---|---|---|---|
| `id` | `int` / signed-int64 candidate | Mã người dùng; làm path handoff. | Legacy BIGINT candidate; live schema chưa xác minh. |
| `full_name` | `string` | Họ và tên. | Bắt buộc theo runtime model. |
| `email` | `string` | Địa chỉ email. | PII; masking/visibility policy chưa xác nhận. |
| `phone` | `string \| null` | Số điện thoại. | PII; giữ null nếu hiển thị, không tự thay bằng giá trị khác. |
| `role` | `string` | Vai trò hệ thống. | Enum members và nhãn hiển thị chưa được định nghĩa. |
| `status` | `string` | Trạng thái tài khoản. | Enum members và lifecycle visibility chưa được định nghĩa. |
| `avatar_url` | `string \| null` | Không hiển thị trong ảnh hiện tại. | Có trong model; không thêm element ngoài screenshot trong phiên này. |
| `created_at`, `updated_at` | date-time | Không hiển thị trong ảnh hiện tại. | Timezone/format UI chưa được chốt. |
| `bio` | Không có trong runtime response model | Không hiển thị. | Catalog optionality không tạo field trong local model; không lấy từ UUID pilot profile. |

### Trích từ DD nguồn: Nguồn truy vết

- [Inventory và screen flow](../../list_screen.md) · [Kế hoạch tổng](../../screen_stitch/dd_screens/PLAN.md) · [Plan AD-03](../../screen_stitch/05_admin/AD-03_chi-tiet-nguoi-dung/AD-03_PLAN.md)
- [Ảnh gốc](../../screen_stitch/05_admin/AD-03_chi-tiet-nguoi-dung/screen.png) · [Ảnh đánh số](../../screen_stitch/05_admin/AD-03_chi-tiet-nguoi-dung/screen_annotated.png) · [HTML prototype](../../screen_stitch/05_admin/AD-03_chi-tiet-nguoi-dung/code.html) · [Marker map](../../screen_stitch/05_admin/AD-03_chi-tiet-nguoi-dung/AD-03_markers.json)
- [API catalog #69](../../../../../docs/lists/list_api.md) · [AC-31 activity diagram](../../../../study-server/docs/diagrams/AC_UNICA/AC_04_ADMIN_MANAGEMENT.drawio)
- [API #69 Overview](../../../../study-server/docs/dd/69_admin_user_detail/02_Overview.md) · [Request](../../../../study-server/docs/dd/69_admin_user_detail/03_Request.md) · [Response](../../../../study-server/docs/dd/69_admin_user_detail/04_Response.md) · [Error](../../../../study-server/docs/dd/69_admin_user_detail/06_Error.md) · [Open questions](../../../../study-server/docs/dd/69_admin_user_detail/OPEN_QUESTIONS.md)
- [API #69 route](../../../../study-server/app/api/v1.py) · [API #69 view](../../../../study-server/app/modules/admin/api_69_admin_user_detail/view.py) · [query](../../../../study-server/app/modules/admin/api_69_admin_user_detail/query.py) · [validation](../../../../study-server/app/modules/admin/api_69_admin_user_detail/validate.py) · [model](../../../../study-server/app/modules/admin/api_69_admin_user_detail/models.py) · [focused test source](../../../../study-server/tests/modules/admin/api_69_admin_user_detail/test_admin_user_detail.py)
- [Study Web design target](../../../../../.agents/web-study/design.md) · [Study Web boundary](../../../../../.agents/web-work/study/AGENTS.md) · [Project API source status](../../../../../.agents/project/source-status.md)

## 3. API không sử dụng
- Không bổ sung API ngoài inventory và DD nguồn. Nếu screen không cần API, trạng thái phải được xác nhận từ source DD.

## 4. References
[Events](02-events.md) · [Data flow](03-data-flow.md) · [Tests](07-test-cases.md) · [Source DD](../../screen_stitch/05_admin/AD-03_chi-tiet-nguoi-dung/AD-03.md)

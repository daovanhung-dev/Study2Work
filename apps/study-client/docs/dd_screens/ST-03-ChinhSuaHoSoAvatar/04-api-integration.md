# ST-03 — API Integration

> API/status dưới đây lấy từ inventory và DD nguồn. Package-local API IDs chỉ là alias truy vết cho API catalog reference; chúng không tạo contract mới. `R/S/D/M/UX` hoặc nhãn cục bộ là evidence status, không tự động xác nhận UI/runtime. Route/contract thiếu nguồn phải giữ `CẦN_XÁC_NHẬN`.

## 1. API usage matrix
| API ID (package-local usage alias) | Source catalog ref | Method/path | Event | Auth |
|---|---|---|---|---|
| `ST-03-API-001` | #04 | See source contract excerpt | Source event IDs are preserved in [Events](02-events.md) | See source auth/permission evidence |
| `ST-03-API-002` | #13 | See source contract excerpt | Source event IDs are preserved in [Events](02-events.md) | See source auth/permission evidence |
| `ST-03-API-003` | #14 | See source contract excerpt | Source event IDs are preserved in [Events](02-events.md) | See source auth/permission evidence |

## 2. Contract / source detail

- API refs trong inventory: #04, #13, #14
- Orchestration/data notes: GET #4 → nếu đổi avatar thì POST #13 → nhận tham chiếu chưa xác định → PUT #14 → GET #4 để đồng bộ; chặn khi mapping chưa chốt.
- BE/source status và gate: **M**; **BLOCK:** API #13/#14 chưa wired; avatar, bio, phone contract xung đột
- Contract sources and discrepancies are preserved in the source excerpts below.

### Trích từ DD nguồn: API và field mapping

| API | Current backend contract/source | Success | Lỗi / side effect | UI status |
|---|---|---|---|---|
| #04 GET /api/v1/users/me | Bearer JWT; role STUDENT; không path/query/body. Query theo JWT sub. | 200 DESIGN_RESOURCE_RETRIEVED; safe UserProfile (không bio). | 401 authentication, 403 access denied, 500 internal. Không mutation. | Source-backed; Study Web không gọi. |
| #13 POST /api/v1/users/me/avatar | Bearer JWT; JSON {image: Data URL}; PNG/JPEG/WebP; decoded ≤5 MiB; model cấm extra fields. | 201 DESIGN_RESOURCE_CREATED; data.avatar_url. | 401/403; 422 DESIGN_VALIDATION_ERROR; 500 storage/config. Ghi object avatars/{user_id}, không DB. | Source-backed; không có client caller hoặc live storage verification. |
| #14 PUT /api/v1/users/me/profile | Bearer JWT; JSON required fields full_name, phone, avatar_url; nullable phone/avatar; extra bio bị ignore. | 200 DESIGN_RESOURCE_UPDATED; data=UserProfile. | 401/403; 422 request validation hoặc DESIGN_VALIDATION_ERROR; 500 rollback/internal. UPDATE users và commit. | Source-backed; payload catalog/AC khác source; không có client caller. |

### Envelope và mapping nguồn

Success response hiện dùng các khóa success, businessCode, message, data, meta, traceId; lỗi dùng cùng nhóm khóa với success=false, data=null mặc định, meta.fieldErrors khi validator trả lỗi và header X-Trace-Id.

- #04 trả id, full_name, email, role, avatar_url, phone, status, created_at, updated_at. Không có bio hoặc permissions.
- #13 trả avatar_url trong data; không trả UserProfile và không thay đổi users.avatar_url.
- #14 trả UserProfile nhưng không có bio; source không xác thực avatar URL là URI hoặc URL do #13 trả.
- DDL candidate users có full_name VARCHAR(150) NOT NULL, avatar_url TEXT NULL, phone VARCHAR(20) NULL, status VARCHAR(20) DEFAULT 'ACTIVE' nullable; không có bio. Live DB/schema chưa được xác minh. UserProfile yêu cầu status non-null nên row status null có thể gây lỗi mapping 500.
- list_screen.md gắn #13/#14 nhãn D/not wired; current backend router/modules/tests có source. Đây là discrepancy inventory/backend. Study Web vẫn UNWIRED.

### Trích từ DD nguồn: I. Nguồn truy vết

- [Inventory màn hình và G-03](../../list_screen.md)
- [API catalog](../../../../../docs/lists/list_api.md)
- [API #13 DD](../../../../study-server/docs/dd/13_users_me_avatar/00_Cover.md) and [verification report](../../../../study-server/docs/dd/13_users_me_avatar/VERIFICATION_REPORT.md)
- [API #14 DD](../../../../study-server/docs/dd/14_users_me_profile/00_Cover.md)
- [AC-11 API index](../../../../study-server/docs/diagrams/AC_UNICA/00_AC_API_INDEX.md)
- [AC student flow diagram](../../../../study-server/docs/diagrams/AC_UNICA/AC_02_STUDENT_LEARNING.drawio)
- [Study API router](../../../../study-server/app/api/v1.py)
- [API #04 models/view/query](../../../../study-server/app/modules/guest/api_04_users_me/models.py)
- [API #13 request/validation/view](../../../../study-server/app/modules/guest/api_13_users_me_avatar/models.py)
- [API #13 storage provider](../../../../study-server/app/service/object_storage/avatar.py)
- [API #14 models/validation/view/query](../../../../study-server/app/modules/guest/api_14_users_me_profile/models.py)
- [Shared auth guard](../../../../study-server/app/utils/auth.py)
- [Shared response envelope](../../../../study-server/app/core/responses.py)
- [Checked-in Study DDL](../../../../../infra/postgres/study-server/DB.sql)
- [ST-02 preceding screen DD](../../screen_stitch/03_student/ST-02_ho-so-ca-nhan/ST-02.md)
- [Source screen image](../../screen_stitch/03_student/ST-03_chinh-sua-ho-so-avatar/screen.png); [static HTML](../../screen_stitch/03_student/ST-03_chinh-sua-ho-so-avatar/code.html)

## 3. API không sử dụng
- Không bổ sung API ngoài inventory và DD nguồn. Nếu screen không cần API, trạng thái phải được xác nhận từ source DD.

## 4. References
[Events](02-events.md) · [Data flow](03-data-flow.md) · [Tests](07-test-cases.md) · [Source DD](../../screen_stitch/03_student/ST-03_chinh-sua-ho-so-avatar/ST-03.md)

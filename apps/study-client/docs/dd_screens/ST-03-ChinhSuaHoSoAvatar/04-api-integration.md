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
- Orchestration/data notes: GET #04 → nếu đổi avatar thì POST #13 → PUT #14 với các trường source-backed → GET #04 lại để đồng bộ; Bio không được gửi.
- BE/source status and gate: Study Web callers #04/#13/#14 are wired through Student Bearer. **PARTIAL:** Bio is required by the screen inventory but absent from API #04/#14 and checked-in DB; live storage/database remain unverified.
- Contract sources and discrepancies are preserved in the source excerpts below.

### Trích từ DD nguồn: API và field mapping

| API | Current backend contract/source | Success | Lỗi / side effect | UI status |
|---|---|---|---|---|
| #04 GET /api/v1/users/me | Bearer JWT; role STUDENT; không path/query/body. Query theo JWT sub. | 200 DESIGN_RESOURCE_RETRIEVED; safe UserProfile (không bio). | 401 authentication, 403 access denied, 500 internal. Không mutation. | Caller: load form and refresh after #14; response shape is checked before binding. |
| #13 POST /api/v1/users/me/avatar | Bearer JWT; JSON `{image: Data URL}`; PNG/JPEG/WebP; decoded ≤5 MiB; model cấm extra fields. | 201 DESIGN_RESOURCE_CREATED; `data.avatar_url`. | 401/403; 422 DESIGN_VALIDATION_ERROR; 500 storage/config. Ghi object `avatars/{user_id}`, không DB. | Caller: explicit upload action. Client checks MIME and file size; backend verifies decoded bytes/signature. Live storage not verified. |
| #14 PUT /api/v1/users/me/profile | Bearer JWT; JSON required fields `full_name`, `phone`, `avatar_url`; nullable phone/avatar; extra bio bị ignore. | 200 DESIGN_RESOURCE_UPDATED; `data=UserProfile`. | 401/403; 422 request validation hoặc DESIGN_VALIDATION_ERROR; 500 rollback/internal. UPDATE users và commit. | Caller: explicit save action; client sends only supported fields, then refetches #04. |

### Envelope và mapping nguồn

Success response hiện dùng các khóa success, businessCode, message, data, meta, traceId; lỗi dùng cùng nhóm khóa với success=false, data=null mặc định, meta.fieldErrors khi validator trả lỗi và header X-Trace-Id.

- #04 trả id, full_name, email, role, avatar_url, phone, status, created_at, updated_at. Không có bio hoặc permissions.
- #13 trả avatar_url trong data; không trả UserProfile và không thay đổi users.avatar_url.
- #14 trả UserProfile nhưng không có bio; source không xác thực avatar URL là URI hoặc URL do #13 trả.
- DDL candidate users có full_name VARCHAR(150) NOT NULL, avatar_url TEXT NULL, phone VARCHAR(20) NULL, status VARCHAR(20) DEFAULT 'ACTIVE' nullable; không có bio. Live DB/schema chưa được xác minh. UserProfile yêu cầu status non-null nên row status null có thể gây lỗi mapping 500.
- list_screen.md gắn #13/#14 nhãn D/not wired; current backend router/modules/tests có source. Đây là discrepancy inventory/backend. Study Web callers are now source-wired; this does not verify live service behavior.

### Trích từ DD nguồn: I. Nguồn truy vết

- [Inventory màn hình và G-03](../../list_screen.md)
- [API catalog](../../../../../docs/lists/list_api.md)
- [API #13 DD](../../../../study-server/docs/dd/13_users_me_avatar/00_Cover.md) and [verification report](../../../../study-server/docs/dd/13_users_me_avatar/VERIFICATION_REPORT.md)
- [API #14 DD](../../../../study-server/docs/dd/14_users_me_profile/00_Cover.md)
- [AC-11 API index](../../../../study-server/docs/diagrams/AC_UNICA/00_AC_API_INDEX.md)
- [AC student flow diagram](../../../../study-server/docs/diagrams/AC_UNICA/AC_02_STUDENT_LEARNING.drawio)
- [Study API router](../../../../study-server/app/api/v1.py)
- [API #04 models/view/query](../../../../study-server/app/modules/student/api_04_users_me/models.py)
- [API #13 request/validation/view](../../../../study-server/app/modules/student/api_13_users_me_avatar/models.py)
- [API #13 storage provider](../../../../study-server/app/service/object_storage/avatar.py)
- [API #14 models/validation/view/query](../../../../study-server/app/modules/student/api_14_users_me_profile/models.py)
- [Shared auth guard](../../../../study-server/app/utils/auth.py)
- [Shared response envelope](../../../../study-server/app/core/responses.py)
- [Checked-in Study DDL](../../../../../infra/postgres/study-server/DB.sql)
- [ST-02 preceding screen DD](../../screen_stitch/03_student/ST-02_ho-so-ca-nhan/ST-02.md)
- [Source screen image](../../screen_stitch/03_student/ST-03_chinh-sua-ho-so-avatar/screen.png); [static HTML](../../screen_stitch/03_student/ST-03_chinh-sua-ho-so-avatar/code.html)

## 3. API không sử dụng
- Không bổ sung API ngoài inventory và DD nguồn. Nếu screen không cần API, trạng thái phải được xác nhận từ source DD.

## 4. References
[Events](02-events.md) · [Data flow](03-data-flow.md) · [Tests](07-test-cases.md) · [Source DD](../../screen_stitch/03_student/ST-03_chinh-sua-ho-so-avatar/ST-03.md)

## 5. Current Study Web source

The `/student/profile/edit` route assigns API IDs #04/#13/#14. `ST03ProfileService` calls all three through `StudentApiService`, which supplies the Student Bearer token. The page binds profile data from #04, uploads only a checked Data URL through #13, sends `full_name`, nullable `phone`, and nullable `avatar_url` to #14, then refetches #04 before navigating to ST-02. Bio stays disabled and is never included. Browser/live API/DB/object-storage runtime is not verified; the existing ST-03 page spec still asserts the old static gate and was not run or changed.

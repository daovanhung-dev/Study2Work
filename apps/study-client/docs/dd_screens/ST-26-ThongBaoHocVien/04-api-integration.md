# ST-26 — API Integration

> API/status dưới đây lấy từ inventory và DD nguồn. Package-local API IDs chỉ là alias truy vết cho API catalog reference; chúng không tạo contract mới. `R/S/D/M/UX` hoặc nhãn cục bộ là evidence status, không tự động xác nhận UI/runtime. Route/contract thiếu nguồn phải giữ `CẦN_XÁC_NHẬN`.

## 1. API usage matrix
| API ID (package-local usage alias) | Source catalog ref | Method/path | Event | Auth |
|---|---|---|---|---|
| `ST-26-API-001` | #43 | See source contract excerpt | Source event IDs are preserved in [Events](02-events.md) | See source auth/permission evidence |
| `ST-26-API-002` | #44 | See source contract excerpt | Source event IDs are preserved in [Events](02-events.md) | See source auth/permission evidence |
| `ST-26-API-003` | #45 | See source contract excerpt | Source event IDs are preserved in [Events](02-events.md) | See source auth/permission evidence |

## 2. Contract / source detail

- API refs trong inventory: #43, #44, #45
- Orchestration/data notes: GET #43 → khi user mở POST? Không, PATCH #44; PATCH #45 khi user bấm tất cả → refresh #43.
- BE/source status và gate: **D**; **BLOCK:** Payload deep-link thông báo chưa định nghĩa
- Contract sources and discrepancies are preserved in the source excerpts below.

### Trích từ DD nguồn: A.4. API DD status, data contract và blockers

| API | Catalog request/result | API DD hiện hành | UI implication |
|---|---|---|---|
| #43 | GET; optional `unread_only:boolean`, `page:int32`; `Page<Notification>`; 200/401/403/500. | `Draft — Needs Confirmation`; 7 open questions. | Chỉ hai query fields được khai báo; category filters và explicit unread count không có trong contract. |
| #44 | PATCH; `notification_id:int64!`; no body/query; `Page<Notification>`; 200/401/403/404/422/500. | `Draft — Needs Confirmation`; 7 open questions. | Principal/recipient rule, whether repeated mark is idempotent, 404 concealment, response page and read timestamp are unresolved. |
| #45 | PATCH; catalog `body{}`; `Page<Notification>`; 200/401/403/422/500. | `Draft — Needs Confirmation`; 8 open questions. | Body requiredness/validation, bulk response rows/Page, empty result, recipient scope and state storage are unresolved. |

- Reusable schema `Notification` yêu cầu `id:int64`, `title:string`, `content:string`, `channels:NotificationChannel[]`, `status:NotificationStatus`, `created_at:date-time`; `read_at` và `scheduled_at` optional. Schema không có `is_read`, `type/category`, sender, icon, unread count hay `action_url`.
- AC-20 gọi logical `NotificationRecipient.read_at`. Checked-in legacy Study DDL candidate có `notifications.id BIGSERIAL`, nullable `user_id`/`sender_id`, `title`, `content`, `type`, `is_read BOOLEAN DEFAULT FALSE`, `created_at TIMESTAMP`, `operation_id`; không có recipient table, `read_at`, `channels`, `status`, `scheduled_at` hoặc `action_url`. `is_read` không khai báo `NOT NULL`.
- V1-PILOT DDL khác: notification ID và `learner_id` là UUID; có `read_at`, `action_url`, expiry/payload và delivery model riêng. Nó không khớp int64 catalog/current numeric Student principal. Cả hai DDL chỉ là checked-in candidate; live schema/deployment chưa được xác minh.
- Không map `type` sang `channels`, `is_read` sang `status`, boolean thành `read_at`, hoặc `NotificationRecipient` sang `notifications.user_id` mà không có quyết định schema. Không coi `action_url` từ V1-PILOT là field của API catalog.
- API #43 response thiếu field để UI xác nhận unread/read từng row; unread filtering query có thể được yêu cầu nhưng count metadata semantics của Page là proposal trong API DD. Screenshot `5 mới` không được map từ sample count/Page total khi rule chưa duyệt.
- API #43 DD đề xuất page default 1, size 20, order `created_at DESC, id DESC`; các điểm này là `DERIVED`, không phải catalog. #44/#45 response Page cũng chưa có agreed projection/metadata semantics. #44 DD candidate dùng `is_read=TRUE` nhưng diagram yêu cầu `read_at`; #45 DD candidate bulk-updates only direct-recipient rows và trả all changed rows, đều chưa approved.
- API #44/#45 không khai báo `Idempotency-Key`; không tự thêm header. Error guideline `data:null` khác `error_response()` current fallback `data:{}`; Student endpoints chưa gọi helper này, nên đây là known shared discrepancy chứ không phải verified response của #43–#45.
- Safe deep-link requirement không có source field trong catalog Notification. Screenshot CTAs (ST-19, ST-25, ST-11, ST-22, Meet) không đủ để dựng URL, IDs hoặc trust policy. Không điều hướng dựa trên notification title/body hoặc raw URL.
- Sidebar preferences (Email/Web Push/SMS), weekly chart, help/contact và footer links không được #43–#45 cung cấp. Không gán API #48 hay thêm API/setting fields.

### Trích từ DD nguồn: A.5. Bảo mật và truy vết nguồn

- Principal phải đến từ Student Bearer/JWT theo catalog; không dùng user ID từ query/body, sample avatar/tên, notification payload không tin cậy hoặc URL token.
- Notification list/mutation phải được scope theo recipient hiện tại sau khi schema/access contract được duyệt. `user_id IS NULL` broadcast rows và per-Student read state chưa có physical model; không mở rộng tới broadcast bằng suy đoán.
- Destination chỉ được mở khi typed payload, allowed route list, parameter validation và external-link policy được source-backed. Nếu contract thiếu/sai, không route từ content text.
- Sources: [screen inventory](../../list_screen.md), [API catalog](../../../../../docs/lists/list_api.md), [AC-20 API index](../../../../study-server/docs/diagrams/AC_UNICA/00_AC_API_INDEX.md), [AC-20 activity diagram](../../../../study-server/docs/diagrams/AC_UNICA/AC_02_STUDENT_LEARNING.drawio), [API #43 overview/request/response/mapping/open questions](../../../../study-server/docs/dd/43_users_me_notifications/02_Overview.md), [API #44 overview/request/mapping/open questions](../../../../study-server/docs/dd/44_notifications_mark_read/02_Overview.md), [API #45 overview/request/mapping/open questions](../../../../study-server/docs/dd/45_notifications_read_all/02_Overview.md), [notification DB guide](../../../../study-server/docs/diagrams/DB_UNICA_TABLES.md), [legacy Study DDL candidate](../../../../../infra/postgres/study-server/DB.sql), [V1-PILOT DDL](../../../../../infra/postgres/02_study_db.sql), [Study Web visual/accessibility target](../../../../../.agents/web-study/design.md), current [Study router](../../../../study-server/app/api/v1.py).

### Trích từ DD nguồn: B.5. Các control ngoài contract

- Channel preferences, API #48 status strip, weekly totals/chart, emergency coordinator and footer contact/legal/navigation are visible screenshot content only. #43–#45 do not expose these operations; API #48 belongs to Mentor lecture detail. Do not send requests or persist toggle state.
- Header search/profile and cross-product links have no current Study Web handler. Their destination/history semantics are not part of API #43–#45.
- Footer/category/contact values are design samples; they do not establish current URLs or support services.

## 3. API không sử dụng
- Không bổ sung API ngoài inventory và DD nguồn. Nếu screen không cần API, trạng thái phải được xác nhận từ source DD.

## 4. References
[Events](02-events.md) · [Data flow](03-data-flow.md) · [Tests](07-test-cases.md) · [Source DD](../../screen_stitch/03_student/ST-26_thong-bao-hoc-vien/ST-26.md)

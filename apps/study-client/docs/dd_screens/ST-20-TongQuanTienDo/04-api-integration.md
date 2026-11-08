# ST-20 — API Integration

> API/status dưới đây lấy từ inventory và DD nguồn. Package-local API IDs chỉ là alias truy vết cho API catalog reference; chúng không tạo contract mới. `R/S/D/M/UX` hoặc nhãn cục bộ là evidence status, không tự động xác nhận UI/runtime. Route/contract thiếu nguồn phải giữ `CẦN_XÁC_NHẬN`.

## 1. API usage matrix
| API ID (package-local usage alias) | Source catalog ref | Method/path | Event | Auth |
|---|---|---|---|---|
| `ST-20-API-001` | #21 | See source contract excerpt | Source event IDs are preserved in [Events](02-events.md) | See source auth/permission evidence |
| `ST-20-API-002` | #38 | See source contract excerpt | Source event IDs are preserved in [Events](02-events.md) | See source auth/permission evidence |

## 2. Contract / source detail

- API refs trong inventory: #21, #38
- Orchestration/data notes: GET #21 và #38 độc lập; render từng widget theo trạng thái API riêng.
- BE/source status và gate: **D; DD BLOCKED; IMPLEMENTATION BLOCKED; RUNTIME NOT VERIFIED:** #21 catalog trả `UserProfile` nhưng query, progress DTO, aggregate/merge/empty semantics chưa chốt; #38 award policy/source, course filter, pagination/order/empty semantics chưa chốt; inventory độc lập #21/#38 mâu thuẫn AC-18 tuần tự #21→#37→#38; Student routes/modules/queries/tests #21/#38 NOT_FOUND; Study Web UNWIRED; PNG gốc trống phần body, HTML chỉ có static empty state; loaded dashboard chưa có nguồn thiết kế xác nhận; HTML prototype tải remote Tailwind/Plus Jakarta Sans, dùng 1440px và trộn primary token lệch Study Web guide
- Contract sources and discrepancies are preserved in the source excerpts below.

### Trích từ DD nguồn: Nguồn truy vết

- [Inventory / ST-20 / F07](../../list_screen.md)
- [Original PNG](../../screen_stitch/03_student/ST-20_tong-quan-tien-do/screen.png), [HTML companion](../../screen_stitch/03_student/ST-20_tong-quan-tien-do/code.html), [HTML render](../../screen_stitch/03_student/ST-20_tong-quan-tien-do/screen_rendered.png), [annotated image](../../screen_stitch/03_student/ST-20_tong-quan-tien-do/screen_annotated.png), [marker map](../../screen_stitch/03_student/ST-20_tong-quan-tien-do/ST-20_markers.json), [plan](../../screen_stitch/03_student/ST-20_tong-quan-tien-do/ST-20_PLAN.md)
- [API catalog](../../../../../docs/lists/list_api.md)
- [API #21 overview](../../../../study-server/docs/dd/21_users_me_progress/02_Overview.md), [open questions](../../../../study-server/docs/dd/21_users_me_progress/OPEN_QUESTIONS.md)
- [API #38 overview](../../../../study-server/docs/dd/38_users_me_achievements/02_Overview.md), [open questions](../../../../study-server/docs/dd/38_users_me_achievements/OPEN_QUESTIONS.md)
- [AC-18 diagram](../../../../study-server/docs/diagrams/AC_UNICA/AC_02_STUDENT_LEARNING.drawio), [AC/API index](../../../../study-server/docs/diagrams/AC_UNICA/00_AC_API_INDEX.md)
- [Progress table design](../../../../study-server/docs/diagrams/DB_UNICA_TABLES.md), [candidate DDL](../../../../../infra/postgres/study-server/DB.sql)
- [Current Study route inventory](../../../../../.agents/server-study/apis/declared-routes.md), [Study Web design target](../../../../../.agents/web-study/design.md)

### Trích từ DD nguồn: A.4. API contract và trạng thái source

| Thuộc tính | API #21 — user progress |
|---|---|
| Method / endpoint | `GET /api/v1/users/me/progress` |
| Authentication / authorization | Student Bearer JWT theo catalog; user scope phải lấy từ principal/token phía server, không nhận user ID do client tự chọn. Access policy chưa có runtime source. |
| Path / query | Không có path param. Query trong catalog: `course_id list hoặc aggregate?:string` — cú pháp, kiểu, cardinality và mutual exclusivity chưa được xác định. |
| Headers / body | Authorization Bearer theo thiết kế; không khai báo request body hoặc header nghiệp vụ khác. |
| Success | HTTP 200, `DESIGN_RESOURCE_RETRIEVED`, `ApiEnvelope<UserProfile>`. Không có progress fields trong `UserProfile` đã tra cứu; mapping đang bị chặn. |
| Errors | 401 `DESIGN_AUTHENTICATION_REQUIRED`; 403 `DESIGN_ACCESS_DENIED`; 500 `DESIGN_INTERNAL_ERROR`. Catalog không khai báo 404/422. |
| Source status | `DECLARED_NOT_RUNNABLE`: Student route/module/query/test không tìm thấy trong source hiện hành. API DD Draft. |

| Thuộc tính | API #38 — achievements |
|---|---|
| Method / endpoint | `GET /api/v1/users/me/achievements` |
| Authentication / authorization | Student Bearer JWT theo catalog; user scope phải do server suy ra từ principal. |
| Path / query | Không có path param. `course_id:int64` optional; semantics khóa không có trong danh sách/không thuộc user chưa được chốt. Không khai báo `page`, `size` hoặc `sort`. |
| Headers / body | Authorization Bearer theo thiết kế; không khai báo request body hoặc header nghiệp vụ khác. |
| Success | HTTP 200, `DESIGN_RESOURCE_RETRIEVED`, `ApiEnvelope<Page<Achievement>>`. Shape Page chi tiết và page defaults chưa được đặc tả tại request. |
| Errors | 401 `DESIGN_AUTHENTICATION_REQUIRED`; 403 `DESIGN_ACCESS_DENIED`; 500 `DESIGN_INTERNAL_ERROR`. Catalog không khai báo 404/422. |
| Source status | `DECLARED_NOT_RUNNABLE`: Student route/module/query/test không tìm thấy trong source hiện hành. API DD Draft; award rule/source chưa xác nhận. |

Không có bằng chứng về retry, timeout, cache TTL, deduplication hoặc parse-error business code cho hai API; không thêm hành vi mặc định vào contract.

## 3. API không sử dụng
- Không bổ sung API ngoài inventory và DD nguồn. Nếu screen không cần API, trạng thái phải được xác nhận từ source DD.

## 4. References
[Events](02-events.md) · [Data flow](03-data-flow.md) · [Tests](07-test-cases.md) · [Source DD](../../screen_stitch/03_student/ST-20_tong-quan-tien-do/ST-20.md)

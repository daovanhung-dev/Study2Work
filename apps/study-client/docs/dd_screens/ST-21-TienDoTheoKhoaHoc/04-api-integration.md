# ST-21 — API Integration

> API/status dưới đây lấy từ inventory và DD nguồn. Package-local API IDs chỉ là alias truy vết cho API catalog reference; chúng không tạo contract mới. `R/S/D/M/UX` hoặc nhãn cục bộ là evidence status, không tự động xác nhận UI/runtime. Route/contract thiếu nguồn phải giữ `CẦN_XÁC_NHẬN`.

## 1. API usage matrix
| API ID (package-local usage alias) | Source catalog ref | Method/path | Event | Auth |
|---|---|---|---|---|
| `ST-21-API-001` | #37 | See source contract excerpt | Source event IDs are preserved in [Events](02-events.md) | See source auth/permission evidence |

## 2. Contract / source detail

- API refs trong inventory: #37
- Orchestration/data notes: GET #37 theo course_id; liên kết lesson_id → ST-10/11 sau gate.
- BE/source status và gate: **D**
- Contract sources and discrepancies are preserved in the source excerpts below.

### Trích từ DD nguồn: Nguồn truy vết

- [Inventory / ST-21 / F07](../../list_screen.md)
- [Original PNG](../../screen_stitch/03_student/ST-21_tien-do-theo-khoa-hoc/screen.png), [HTML companion](../../screen_stitch/03_student/ST-21_tien-do-theo-khoa-hoc/code.html), [render tĩnh](../../screen_stitch/03_student/ST-21_tien-do-theo-khoa-hoc/screen_rendered.png), [annotated image](../../screen_stitch/03_student/ST-21_tien-do-theo-khoa-hoc/screen_annotated.png), [marker map](../../screen_stitch/03_student/ST-21_tien-do-theo-khoa-hoc/ST-21_markers.json), [plan](../../screen_stitch/03_student/ST-21_tien-do-theo-khoa-hoc/ST-21_PLAN.md)
- [API catalog](../../../../../docs/lists/list_api.md)
- [API #37 overview](../../../../study-server/docs/dd/37_users_me_progress_course/02_Overview.md), [request](../../../../study-server/docs/dd/37_users_me_progress_course/03_Request.md), [response](../../../../study-server/docs/dd/37_users_me_progress_course/04_Response.md), [data mapping](../../../../study-server/docs/dd/37_users_me_progress_course/05_Data_Mapping.md), [errors](../../../../study-server/docs/dd/37_users_me_progress_course/06_Error.md), [open questions](../../../../study-server/docs/dd/37_users_me_progress_course/OPEN_QUESTIONS.md)
- [AC/API index](../../../../study-server/docs/diagrams/AC_UNICA/00_AC_API_INDEX.md), [AC-18 diagram](../../../../study-server/docs/diagrams/AC_UNICA/AC_02_STUDENT_LEARNING.drawio)
- [DB table guide](../../../../study-server/docs/diagrams/DB_UNICA_TABLES.md), [legacy Study DDL](../../../../../infra/postgres/study-server/DB.sql), [V1-PILOT DDL](../../../../../infra/postgres/02_study_db.sql)
- [Current Study route inventory](../../../../../.agents/server-study/apis/declared-routes.md), [Study Web design target](../../../../../.agents/web-study/design.md)

### Trích từ DD nguồn: A.4. API và trạng thái source

| Thuộc tính | API #37 |
|---|---|
| Method / endpoint | `GET /api/v1/users/me/progress/{course_id}` |
| Authentication | Bearer JWT; role Student theo catalog. Claim-to-user mapping và route guard chưa được #37 xác định trong current source. |
| Path | `course_id:int64!`; min/max/domain, parse/range behavior chưa đặc tả. |
| Query / body | Không có query parameter hoặc request body trong catalog/DD request. |
| Success | HTTP 200, `DESIGN_RESOURCE_RETRIEVED`, `ApiEnvelope<UserProfile>`. `UserProfile` không có progress fields nên không map được expected course/lesson progress. |
| Errors | Chỉ 401 `DESIGN_AUTHENTICATION_REQUIRED`, 403 `DESIGN_ACCESS_DENIED`, 404 `DESIGN_RESOURCE_NOT_FOUND`, 500 `DESIGN_INTERNAL_ERROR`. Catalog không khai báo 400/422. |
| Current source | `DECLARED_NOT_RUNNABLE`: #37 route/module/query/test NOT_FOUND. API DD Draft; không có request chạy được để xác minh. |

## 3. API không sử dụng
- Không bổ sung API ngoài inventory và DD nguồn. Nếu screen không cần API, trạng thái phải được xác nhận từ source DD.

## 4. References
[Events](02-events.md) · [Data flow](03-data-flow.md) · [Tests](07-test-cases.md) · [Source DD](../../screen_stitch/03_student/ST-21_tien-do-theo-khoa-hoc/ST-21.md)

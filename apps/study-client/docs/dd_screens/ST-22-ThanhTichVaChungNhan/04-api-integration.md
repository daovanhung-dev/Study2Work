# ST-22 — API Integration

> API/status dưới đây lấy từ inventory và DD nguồn. Package-local API IDs chỉ là alias truy vết cho API catalog reference; chúng không tạo contract mới. `R/S/D/M/UX` hoặc nhãn cục bộ là evidence status, không tự động xác nhận UI/runtime. Route/contract thiếu nguồn phải giữ `CẦN_XÁC_NHẬN`.

## 1. API usage matrix
| API ID (package-local usage alias) | Source catalog ref | Method/path | Event | Auth |
|---|---|---|---|---|
| `ST-22-API-001` | #38 | See source contract excerpt | Source event IDs are preserved in [Events](02-events.md) | See source auth/permission evidence |

## 2. Contract / source detail

- API refs trong inventory: #38
- Orchestration/data notes: GET #38 (filter course_id optional); thành tích chỉ hiển thị khi backend xác nhận.
- BE/source status và gate: **D; DD BLOCKED; IMPLEMENTATION BLOCKED; RUNTIME NOT VERIFIED:** API #38 Draft còn sáu câu hỏi mở về award criteria/projection, filter/access, page/order/empty và query validation; Student route/module/query/test NOT_FOUND; Study Web UNWIRED; populated PNG có certificate/proof/GPA/metrics/competency/readiness không thuộc schema `Achievement`, còn HTML là static empty fallback; ERD/DDL chỉ có khái niệm logical/derived, không có physical registry/award table hoặc live-schema proof; AC-18 tuần tự #21→#37→#38 lệch inventory ST-20 gọi #21/#38 độc lập nên chưa suy luận timing; asset dùng remote CDN/font, 1440px và royal-blue/gradient lệch Study Web target
- Contract sources and discrepancies are preserved in the source excerpts below.

### Trích từ DD nguồn: A.2. Expected behavior — contract và thiết kế

- Inventory ST-22 khai báo route `/student/achievements`, AC-18, API #38, danh sách achievement theo course và state `loading/empty/earned/error`. Chỉ hiển thị thành tích backend xác nhận; không tự cấp chứng chỉ.
- API catalog #38 định nghĩa Student Bearer JWT, GET `/api/v1/users/me/achievements`, query tùy chọn `course_id:int64`, response `ApiEnvelope<Page<Achievement>>`; các logical fields của `Achievement` là `id:int64`, `code:string`, `title:string`, `awarded_at:datetime`, `course_id?:int64`. Catalog quy định 200 `DESIGN_RESOURCE_RETRIEVED`, 401 `DESIGN_AUTHENTICATION_REQUIRED`, 403 `DESIGN_ACCESS_DENIED`, 500 `DESIGN_INTERNAL_ERROR`.
- AC-18 và API #38 DD mô tả đọc achievement đã mở khóa; không có tiêu chí unlock, bảng/registry nguồn, projection, thu hồi, ý nghĩa lọc course hoặc ordering được phê duyệt. API #38 DD đang `Draft — Needs Confirmation` với sáu câu hỏi mở.
- **DISCREPANCY về thứ tự gọi:** inventory ST-20 yêu cầu #21 và #38 độc lập, trong khi AC-18 tuần tự #21 → #37 → #38. Giữ trách nhiệm #38 và các liên kết màn hình theo inventory; chưa suy luận thời điểm vào ST-22 hoặc thứ tự orchestration.
- API #38 là GET chỉ đọc, không tạo award/chứng chỉ và không có side effect mutation được khai báo.

### Trích từ DD nguồn: A.4. API #38 — contract và source status

| Thuộc tính | Giá trị được phép dùng trong DD |
|---|---|
| Method / endpoint | `GET /api/v1/users/me/achievements` |
| Authentication / actor | `Authorization: Bearer <Student JWT>` theo catalog. Mapping principal và course-level access chưa được API #38 source xác nhận. |
| Path / query | Không có path parameter. Query tùy chọn `course_id:int64`; miền, parse failure, filter semantics và access predicate chưa chốt. Không có `page`, `size` hoặc `sort` trong request catalog. |
| Body | Không khai báo request body. |
| Success | HTTP 200, `success=true`, `businessCode=DESIGN_RESOURCE_RETRIEVED`, `data: Page<Achievement>` theo catalog/guideline. `Page` có `items` và pagination metadata; nguồn/default của metadata chưa rõ khi request không có paging controls. |
| `Achievement` | `id:int64`, `code:string`, `title:string`, `awarded_at:datetime`, `course_id?:int64`. Không bao gồm file chứng chỉ, proof hash, GPA, rank, reputation, taxonomy, QR hoặc eligibility. |
| Catalog errors | HTTP 401 `DESIGN_AUTHENTICATION_REQUIRED`; 403 `DESIGN_ACCESS_DENIED`; 500 `DESIGN_INTERNAL_ERROR`. Không tự thêm 400/404/422 hoặc business code mới. |
| Current API source | API #38 DD `Draft — Needs Confirmation`; Study Server route/module/query/test `NOT_FOUND` trong source đã kiểm tra; runtime `UNWIRED / NOT VERIFIED`. |

### Trích từ DD nguồn: A.6. Nguồn truy vết

- [Screen inventory và F07](../../list_screen.md) — ST-22, liên kết ST-20/ST-09, state và nguyên tắc không tự cấp.
- [API catalog](../../../../../docs/lists/list_api.md) và [API #38 overview](../../../../study-server/docs/dd/38_users_me_achievements/02_Overview.md), [request](../../../../study-server/docs/dd/38_users_me_achievements/03_Request.md), [response](../../../../study-server/docs/dd/38_users_me_achievements/04_Response.md), [open questions](../../../../study-server/docs/dd/38_users_me_achievements/OPEN_QUESTIONS.md).
- [AC/API index](../../../../study-server/docs/diagrams/AC_UNICA/00_AC_API_INDEX.md), [AC-18 activity diagram](../../../../study-server/docs/diagrams/AC_UNICA/AC_02_STUDENT_LEARNING.drawio).
- [DB table guide](../../../../study-server/docs/diagrams/DB_UNICA_TABLES.md), [legacy Study DDL](../../../../../infra/postgres/study-server/DB.sql), [V1-PILOT DDL](../../../../../infra/postgres/02_study_db.sql).
- [Study Web design target](../../../../../.agents/web-study/design.md), [original screenshot](../../screen_stitch/03_student/ST-22_thanh-tich-va-chung-nhan/screen.png), [HTML companion](../../screen_stitch/03_student/ST-22_thanh-tich-va-chung-nhan/code.html), [marker map](../../screen_stitch/03_student/ST-22_thanh-tich-va-chung-nhan/ST-22_markers.json), [overlay](../../screen_stitch/03_student/ST-22_thanh-tich-va-chung-nhan/ST-22_markers_overlay.svg), [plan](../../screen_stitch/03_student/ST-22_thanh-tich-va-chung-nhan/ST-22_PLAN.md).

## 3. API không sử dụng
- Không bổ sung API ngoài inventory và DD nguồn. Nếu screen không cần API, trạng thái phải được xác nhận từ source DD.

## 4. References
[Events](02-events.md) · [Data flow](03-data-flow.md) · [Tests](07-test-cases.md) · [Source DD](../../screen_stitch/03_student/ST-22_thanh-tich-va-chung-nhan/ST-22.md)

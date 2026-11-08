# ST-01 — API Integration

> API/status dưới đây lấy từ inventory và DD nguồn. Package-local API IDs chỉ là alias truy vết cho API catalog reference; chúng không tạo contract mới. `R/S/D/M/UX` hoặc nhãn cục bộ là evidence status, không tự động xác nhận UI/runtime. Route/contract thiếu nguồn phải giữ `CẦN_XÁC_NHẬN`.

## 1. API usage matrix
| API ID (package-local usage alias) | Source catalog ref | Method/path | Event | Auth |
|---|---|---|---|---|
| `ST-01-API-001` | #20 | See source contract excerpt | Source event IDs are preserved in [Events](02-events.md) | See source auth/permission evidence |
| `ST-01-API-002` | #21 | See source contract excerpt | Source event IDs are preserved in [Events](02-events.md) | See source auth/permission evidence |
| `ST-01-API-003` | #38 | See source contract excerpt | Source event IDs are preserved in [Events](02-events.md) | See source auth/permission evidence |
| `ST-01-API-004` | #43 | See source contract excerpt | Source event IDs are preserved in [Events](02-events.md) | See source auth/permission evidence |

## 2. Contract / source detail

- API refs trong inventory: #20, #21, #38, #43
- Orchestration/data notes: Chỉ sau role STUDENT hợp lệ; load #20/#21; thành tích #38, thông báo #43 lazy/parallel.
- BE/source status và gate: **D; DD BLOCKED; IMPLEMENTATION BLOCKED; RUNTIME NOT VERIFIED:** #20/#21 Draft response UserProfile không biểu diễn Course/progress theo AC-13; nhánh EMPTY/HAS DATA cùng tới node render; #21 query/formula/merge, #38 award/projection/filter/page và #43 recipient/fields/order còn mở; API routes/modules/tests NOT_FOUND; AC-18 order lệch inventory widget độc lập; HTML endpoint paths sai, anchors chỉ là `#`; Study Web UNWIRED và visual target lệch design guide
- Contract sources and discrepancies are preserved in the source excerpts below.

### Trích từ DD nguồn: A.2. Expected behavior — inventory, AC và API catalog

- Inventory ST-01 khai báo `/student`, actor Student, widget khóa học/tiến độ/thành tích/thông báo; #20/#21 khi vào màn hình, #38/#43 lazy hoặc parallel; state labels `partial-widget/empty/loading/403`. Đây là target design, không xác nhận runtime.
- AC-13 yêu cầu #20 đọc danh sách Enrollment/Course, sau đó #21 đọc tiến độ và client ghép theo course. Activity diagram có nhánh `EMPTY` và `HAS DATA` cùng đi tới node “Hiển thị khóa học + % hoàn thành”. Đây là `DISCREPANCY`; không tự sửa nhánh hoặc chọn một order khác.
- AC-18 yêu cầu #21 aggregate, chọn một course, #37 detail progress, #38 achievement rồi render. Inventory ST-01 và ST-20 lại xem #21/#38 là các widget độc lập. Không suy luận thời điểm gọi #38 hoặc ép ST-01 theo chuỗi chi tiết AC-18.
- AC-20 định nghĩa #43 lấy notification list/unread badge; #44/#45 thực hiện mark-read ở luồng notification center. ST-01 chỉ có link tới ST-26, không có mutation event.
- API catalog contract được giữ nguyên: #20 GET `/api/v1/users/me/courses`; #21 GET `/api/v1/users/me/progress`; #38 GET `/api/v1/users/me/achievements`; #43 GET `/api/v1/users/me/notifications`. Không dùng các endpoint path khác xuất hiện trong HTML.
- [AC/API index](../../../../study-server/docs/diagrams/AC_UNICA/00_AC_API_INDEX.md) và [AC activity diagram](../../../../study-server/docs/diagrams/AC_UNICA/AC_02_STUDENT_LEARNING.drawio) là nguồn quy trình; API catalog/DD và current source là các bằng chứng riêng.

### Trích từ DD nguồn: A.4. Ma trận API và source status

| API | Request theo catalog | Response / statuses theo catalog | Current source và điểm chưa chốt |
|---|---|---|---|
| #20 | `GET /api/v1/users/me/courses`; Student Bearer; `status?:string`, `page?:int32`; body không khai báo. | `ApiEnvelope<UserProfile>`; 200 `DESIGN_RESOURCE_RETRIEVED`; 401/403/422/500 theo catalog. | `NOT_FOUND` route/module/query/test. Draft Q-20-01…05: catalog UserProfile khác danh sách Course của AC-13; status predicate/enum, page semantics, empty wire shape và JWT subject → Enrollment ownership chưa xác nhận. |
| #21 | `GET /api/v1/users/me/progress`; Student Bearer; query ghi `course_id list hoặc aggregate?:string`; body không khai báo. | `ApiEnvelope<UserProfile>`; 200 `DESIGN_RESOURCE_RETRIEVED`; 401/403/500. | `NOT_FOUND` route/module/query/test. Draft Q-21-01…05: selector grammar, nguồn/công thức progress, response schema/merge key, user binding và no-enrollment/no-progress shape chưa chốt. |
| #38 | `GET /api/v1/users/me/achievements`; Student Bearer; `course_id?:int64`; body không khai báo. | `ApiEnvelope<Page<Achievement>>`; catalog fields `id`, `code`, `title`, `awarded_at`, `course_id?`; 200/401/403/500. | `NOT_FOUND` route/module/query/test. Draft Q-01…06 về award criteria, projection/source, filter/access, pagination/order/empty và query validation. Không có contract cho certificate, proof, KPI hoặc signature. |
| #43 | `GET /api/v1/users/me/notifications`; Student Bearer; `unread_only?:boolean`, `page?:int32`; body không khai báo. | `ApiEnvelope<Page<Notification>>`; 200/401/403/500. | `NOT_FOUND` route/module/query/test. Draft Q-43-01…07: recipient/broadcast, channels/status, read timestamps, pagination/order, timezone/null behavior và error envelope chưa được chốt. |

Tài liệu từng API: [#20](../../../../study-server/docs/dd/20_users_me_courses/02_Overview.md) / [questions](../../../../study-server/docs/dd/20_users_me_courses/OPEN_QUESTIONS.md), [#21](../../../../study-server/docs/dd/21_users_me_progress/02_Overview.md) / [questions](../../../../study-server/docs/dd/21_users_me_progress/OPEN_QUESTIONS.md), [#38](../../../../study-server/docs/dd/38_users_me_achievements/02_Overview.md) / [questions](../../../../study-server/docs/dd/38_users_me_achievements/OPEN_QUESTIONS.md), [#43](../../../../study-server/docs/dd/43_users_me_notifications/02_Overview.md) / [questions](../../../../study-server/docs/dd/43_users_me_notifications/OPEN_QUESTIONS.md). DDL/ERD là design evidence, không phải live schema proof.

## 3. API không sử dụng
- Không bổ sung API ngoài inventory và DD nguồn. Nếu screen không cần API, trạng thái phải được xác nhận từ source DD.

## 4. References
[Events](02-events.md) · [Data flow](03-data-flow.md) · [Tests](07-test-cases.md) · [Source DD](../../screen_stitch/03_student/ST-01_tong-quan-hoc-vien/ST-01.md)

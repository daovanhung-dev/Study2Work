# ME-09 — API Integration

> API/status dưới đây lấy từ inventory và DD nguồn. Package-local API IDs chỉ là alias truy vết cho API catalog reference; chúng không tạo contract mới. `R/S/D/M/UX` hoặc nhãn cục bộ là evidence status, không tự động xác nhận UI/runtime. Route/contract thiếu nguồn phải giữ `CẦN_XÁC_NHẬN`.

## 1. API usage matrix
| API ID (package-local usage alias) | Source catalog ref | Method/path | Event | Auth |
|---|---|---|---|---|
| `ME-09-API-001` | #54 | See source contract excerpt | Source event IDs are preserved in [Events](02-events.md) | See source auth/permission evidence |

## 2. Contract / source detail

- API refs trong inventory: #54
- Orchestration/data notes: GET #54; click submission_id → ME-10; không khẳng định response Page khi contract chỉ Submission.
- BE/source status và gate: **D**; **BLOCK:** Response cardinality #54 sai kiểu
- Contract sources and discrepancies are preserved in the source excerpts below.

### Trích từ DD nguồn: Nguồn truy vết

- [Screen inventory](../../list_screen.md#L169), [F09 flow](../../list_screen.md#L277).
- [API #54 route](../../../../study-server/app/api/v1.py#L1033), [view](../../../../study-server/app/modules/mentor/api_54_mentor_submissions_list/view.py), [query](../../../../study-server/app/modules/mentor/api_54_mentor_submissions_list/query.py), [models](../../../../study-server/app/modules/mentor/api_54_mentor_submissions_list/models.py), [tests](../../../../study-server/tests/modules/mentor/api_54_mentor_submissions_list/test_mentor_submissions_list.py).
- [Declared routes](../../../../../.agents/server-study/apis/declared-routes.md#L339), [database context](../../../../../.agents/server-study/database.md#L77), [test context](../../../../../.agents/server-study/tests.md#L72).
- [API #54 overview](../../../../study-server/docs/dd/54_mentor_submissions_list/02_Overview.md), [response](../../../../study-server/docs/dd/54_mentor_submissions_list/04_Response.md), [open questions](../../../../study-server/docs/dd/54_mentor_submissions_list/OPEN_QUESTIONS.md), [AC-23 API index](../../../../study-server/docs/diagrams/AC_UNICA/00_AC_API_INDEX.md#L213), [AC diagram](../../../../study-server/docs/diagrams/AC_UNICA/AC_03_MENTOR_TEACHING.drawio).
- [Study Web design target](../../../../../.agents/web-study/design.md); [Study Web source status](../../../../../.agents/web-work/study/AGENTS.md).

### Trích từ DD nguồn: A.4. Contract API #54 và sai khác cardinality

| Hạng mục | Inventory/contract kỳ vọng | AC/API DD/current source |
|---|---|---|
| Cardinality | `list_screen.md` ghi “không khẳng định response Page khi contract chỉ Submission” và đánh dấu lỗi cardinality. | AC-23 diagram hiện ghi `ApiEnvelope<Page<Submission>>`; API #54 DD gọi collection response là fallback `DERIVED`; current route/model cũng trả Page. API DD vẫn `Draft — Needs Confirmation`. |
| Filter | Course/status theo inventory. | `course_id?: int64`, `status?: string`, `page?: int32=1`; không có `q`, sort hay size query. |
| Danh sách | Bài nộp cần chấm; inventory mong deadline/owner. | Response fields ở trên không cung cấp deadline, tên owner, course title hay assignment title. |
| Handoff ID | Inventory gọi `submission_id`. | List response dùng `id`; #55 nhận `{submission_id}` trên path. Mapping `id → submission_id` hợp lý về kỹ thuật nhưng cần thống nhất tên logical DTO. |

Đây là **DISCREPANCY** giữa inventory còn hiệu lực và API DD/diagram/current implementation. DD không coi source đã âm thầm phê duyệt contract. Chủ sở hữu API/schema cần xác nhận response Page và mapping ID trước khi gỡ blocker.

### Trích từ DD nguồn: A.5. API #54 hiện hành

| Thuộc tính | Current source behavior |
|---|---|
| Method/path | `GET /api/v1/mentor/submissions` |
| Authentication | `Authorization: Bearer <access token>`; shared guard yêu cầu role `MENTOR`. |
| Query | `course_id?: int64` dương; `status?: string` exact match; `page?: int32` dương, mặc định 1. `page` không thể lớn hơn `2^31-1`; `course_id` không thể lớn hơn `2^63-1`. |
| Pagination/order | Page size cố định `20`; stable order `submitted_at DESC, id DESC`; `data.pagination={page,size,total,total_pages}`. `total_pages=0` khi total là 0. Không có paging control trên screenshot/HTML. |
| Access scope | Count/list đều lọc `courses.mentor_id` bằng numeric JWT subject. Nếu truyền course thuộc Mentor khác, source trả 403. Course không tồn tại hoặc không có bài khớp trả 200 empty page. Assigned Mentor không được hỗ trợ trong fallback hiện tại. |
| Query source | `assignment_submissions` JOIN `assignments`, `courses`, `users`; optional `uploads` metadata dùng LATERAL lookup theo exact `file_url`, student owner, purpose `SUBMISSION` và course. Orphan required relations bị loại bởi inner join. |
| Item mapping | `id`, `assignment_id`, `user_id`, `content?`, `files[]`, `status`, `submitted_at`, `score?`, `feedback?`. `score` được stringify decimal; nullable fields bị bỏ khỏi JSON; file không khớp tạo `files: []`. File relation là fallback `DERIVED`, không có FK xác nhận. |
| Success | HTTP 200, `businessCode=DESIGN_RESOURCE_RETRIEVED`, envelope có `success`, `message`, `data`, `meta`, `traceId`. `meta` hiện `{}`; pagination nằm trong `data.pagination`. |
| Errors | 401 thiếu/sai Bearer/claims; 403 role hoặc direct-owner không hợp lệ; 422 query constraints; 500 `DESIGN_INTERNAL_ERROR` khi query/mapping lỗi. Catalog có 409 nhưng current source không có nhánh tạo 409. |
| Side effect | Read-only; không ghi hoặc commit. Nhánh lỗi có thể rollback transaction đang mở. |

Trace cụ thể: [route #54](../../../../study-server/app/api/v1.py#L1033) dựng `MentorSubmissionsQuery` → [view](../../../../study-server/app/modules/mentor/api_54_mentor_submissions_list/view.py) gọi shared MENTOR guard → nếu có course filter thì tra owner → [count/list SQL](../../../../study-server/app/modules/mentor/api_54_mentor_submissions_list/query.py) → [models](../../../../study-server/app/modules/mentor/api_54_mentor_submissions_list/models.py) map page/envelope → success/error response. [API #54 tests](../../../../study-server/tests/modules/mentor/api_54_mentor_submissions_list/test_mentor_submissions_list.py) bao phủ source behavior bằng fake DB. Không chạy test trong phiên này.

API #54 DD còn các câu hỏi mở về producer URL từ #35, assigned-Mentor policy, status lifecycle/409, FK nullability/timestamp timezone/live schema và xác nhận error catalog. Xem [API #54 open questions](../../../../study-server/docs/dd/54_mentor_submissions_list/OPEN_QUESTIONS.md). Context báo cáo các test/API checks trước đây; chúng không xác minh production schema/deployment. Xem [Study Server test status](../../../../../.agents/server-study/tests.md).

### Trích từ DD nguồn: D.1. Error/business code mapping cho #54

| HTTP | Current API behavior | Xử lý màn hình yêu cầu sau khi UI contract được duyệt |
|---:|---|---|
| 200 | `DESIGN_RESOURCE_RETRIEVED`; có items hoặc Page rỗng. | Empty/ready theo `items.length`, không dựa vào message text. |
| 401 | Bearer/token/claims không hợp lệ hoặc thiếu. | Hiển thị yêu cầu đăng nhập/hết phiên theo auth policy; policy/route chưa được source-backed. |
| 403 | Role không phải MENTOR hoặc course filter trỏ tới owner khác. | Hiển thị quyền bị từ chối, không lặp lại request vô hạn. |
| 422 | `course_id`/`page` sai range hoặc request query invalid theo route constraints. | Map field/query error; status string hiện không có enum validation. |
| 409 | Có khai báo trong catalog/AC node cũ nhưng không có nhánh 409 trong current view. | Không tạo UI conflict behavior cho #54 đến khi có trigger/business rule. |
| 500 | SQL/projection failure → `DESIGN_INTERNAL_ERROR`. | Hiển thị lỗi an toàn và giữ trace ID; retry policy/chính sách giữ dữ liệu cũ cần quyết định. |
| Network/timeout | Không phải business code; chưa có client source. | Chưa xác định timeout, cancel, retry hoặc stale data behavior. |

## 3. API không sử dụng
- Không bổ sung API ngoài inventory và DD nguồn. Nếu screen không cần API, trạng thái phải được xác nhận từ source DD.

## 4. References
[Events](02-events.md) · [Data flow](03-data-flow.md) · [Tests](07-test-cases.md) · [Source DD](../../screen_stitch/04_mentor/ME-09_danh-sach-bai-can-cham/ME-09.md)

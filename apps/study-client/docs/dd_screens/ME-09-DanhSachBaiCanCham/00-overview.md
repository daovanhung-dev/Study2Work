# ME-09 — Danh sách bài cần chấm · Tổng quan

| Trường | Giá trị |
|---|---|
| Screen ID | `ME-09` |
| Module | Mentor |
| Route | `/mentor/submissions` — route trong inventory, không phải xác nhận router runtime |
| Actor/role | Theo DD nguồn; xem overview/source trace bên dưới |
| DD status | Draft (package được chuyển đổi); source status: **DD status:** `DD BLOCKED` — the static specification is source-traced, but the row design, response contract approval, filter/search semantics and several API/schema decisions remain open.; **Implementation status:** `IMPLEMENTATION BLOCKED` — Study Web screen route/source is absent and the approved data/UI contract is incomplete.; **Runtime status:** `RUNTIME NOT VERIFIED` — no ME-09 Study Web runtime exists in the current checkout. API source and prior tests do not verify this screen at runtime. |
| Owner | Không được xác định trong inventory/DD nguồn đã chuyển; `CẦN_XÁC_NHẬN` |
| Version / last updated | 0.1 / 2026-11-08 |
| Nguồn đối chiếu | [ME-09.md](../../screen_stitch/04_mentor/ME-09_danh-sach-bai-can-cham/ME-09.md), [ME-09_PLAN.md](../../screen_stitch/04_mentor/ME-09_danh-sach-bai-can-cham/ME-09_PLAN.md), [ME-09_markers.json](../../screen_stitch/04_mentor/ME-09_danh-sach-bai-can-cham/ME-09_markers.json), [list_screen.md](../../list_screen.md) |

## 1. Mục tiêu & phạm vi
- Mục tiêu: Lọc course/status, danh sách bài nộp có deadline/owner.
- In-scope: GET #54; click submission_id → ME-10; không khẳng định response Page khi contract chỉ Submission.
- Out-of-scope: Xem gate bên dưới; không kết luận Study Web route/UI đã wired hoặc runtime đã chạy.

## 2. Use cases chính
| Use case / AC | Actor | Kết quả kỳ vọng theo inventory |
|---|---|---|
| AC-23 | Theo DD nguồn; `CẦN_XÁC_NHẬN` nếu nguồn chưa chốt | Lọc course/status, danh sách bài nộp có deadline/owner. |

## 3. Precondition / Entry / Dependencies
- Điều kiện vào, role guard và dependency: xem trích đoạn tổng quan nguồn; không bổ sung giả định.
- API references: #54
- Liên kết màn hình dự kiến: [ME-10](../ME-10-ChamDiemVaPhanHoi/00-overview.md)
- Links: [UI](01-ui-elements.md) · [Events](02-events.md) · [Navigation](06-navigation.md)

## 4. UI states
| State | Nguồn | Giá trị |
|---|---|---|
| Inventory states | `list_screen.md` | loading/empty/ready/error |
| Current runtime | Worklog/context Study Web | `UNWIRED` / `RUNTIME NOT VERIFIED` |

## 5. Luồng chính và hình ảnh
- Ảnh clean: [screen-clean.png](images/screen-clean.png) (copy từ [ME-09 source screen.png](../../screen_stitch/04_mentor/ME-09_danh-sach-bai-can-cham/screen.png))
- Ảnh numbered: [screen-numbered.png](images/screen-numbered.png) (copy từ [source annotated PNG](../../screen_stitch/04_mentor/ME-09_danh-sach-bai-can-cham/screen_annotated.png))
- Luồng: GET #54; click submission_id → ME-10; không khẳng định response Page khi contract chỉ Submission.
- Priority: P1; Gate/source status: **D**; **BLOCK:** Response cardinality #54 sai kiểu

## 6. Open questions / Change log
- `CẦN_XÁC_NHẬN`: các gate/source questions trong inventory và DD nguồn vẫn giữ nguyên; không tự đóng blocker.
- 2026-11-08 — Chuyển nội dung nguồn sang 8-file template; không chỉnh source, không xác minh runtime.

## Trạng thái và ranh giới bằng chứng

# ME-09 — Danh sách bài cần chấm

> **DD status:** `DD BLOCKED` — the static specification is source-traced, but the row design, response contract approval, filter/search semantics and several API/schema decisions remain open.
> **Implementation status:** `IMPLEMENTATION BLOCKED` — Study Web screen route/source is absent and the approved data/UI contract is incomplete.
> **Runtime status:** `RUNTIME NOT VERIFIED` — no ME-09 Study Web runtime exists in the current checkout. API source and prior tests do not verify this screen at runtime.

## Trích đoạn tổng quan từ DD nguồn

### Trích từ DD nguồn: A. Tổng quan màn hình

### A.1. Mục đích và phạm vi

| Thuộc tính | Mô tả |
|---|---|
| Screen ID | ME-09 |
| Tên | Danh sách bài cần chấm |
| Mục tiêu kỳ vọng | Giúp Mentor xem/lọc bài nộp và chọn một bài để mở ME-10. |
| Actor | Mentor có Bearer role `MENTOR`; đây là yêu cầu của AC-23 và API #54. |
| Route đề xuất | `/mentor/submissions`; route chưa được triển khai trong Study Web. |
| API chính | API #54 — `GET /api/v1/mentor/submissions`. |
| Màn hình trước/liên quan | ME-01 có thể mở danh sách từ widget theo inventory. Inventory không khai báo direct link ME-02 → ME-09. Route wiring chưa có. |
| Màn hình tiếp theo | ME-10 qua `GET /api/v1/mentor/submissions/{submission_id}` (#55). ME-10 mới gọi #56 chấm điểm và #57 lưu phản hồi theo yêu cầu riêng. |
| Dữ liệu ghi | Không có. API #54 hiện là read-only và không commit. |

Expected behavior lấy từ [inventory ME-09](../../list_screen.md#L169), F09 và AC-23. Inventory yêu cầu lọc course/status, hiển thị danh sách bài nộp có deadline/owner và mở ME-10 bằng `submission_id`. AC-23 xác định luồng list → chọn submission → detail; [F09](../../list_screen.md#L277) tách thao tác chấm điểm và feedback trên ME-10.

Current behavior lấy từ current source, asset và test source. `apps/study-client/` hiện có tài liệu/ảnh và ignored `dist`, nhưng không có editable source, `package.json`, feature router hay ME-09 route. Xem [Study Web context](../../../../../.agents/web-work/study/AGENTS.md) và [design target](../../../../../.agents/web-study/design.md); các tài liệu đó không chứng minh runtime.

### A.2. Điều kiện vào, dữ liệu và rời màn hình

- **Điều kiện truy cập server:** Bearer token hợp lệ, JWT subject là số và có role `MENTOR`. API #54 xác minh role trước truy vấn. Quyền client-side/session guard chưa có source.
- **Điều kiện dữ liệu:** `course_id` tùy chọn; nếu có thì phải là số nguyên dương trong miền signed int64. `status` tùy chọn là string khớp chính xác. `page` mặc định `1`, dương và không vượt signed int32. Kích thước trang hiện cố định `20`.
- **Kết quả đọc:** API #54 trả `data.items` và `data.pagination`; `items=[]` là kết quả thành công, không phải lỗi.
- **Rời màn hình:** Khi có row và lựa chọn hợp lệ, lấy `data.items[].id` làm giá trị path `submission_id` cho ME-10. Current response không có key `submission_id`; cách gọi tên ở inventory và tên field source là một điểm cần xác nhận khi khóa client model.
- **Không được xem là tiền điều kiện đã hoàn tất:** route/session guard, course options, state URL/cache, auto-refresh, deadline và rubric chưa có frontend hoặc API contract hoàn chỉnh.

### A.3. Expected behavior và current behavior

**Expected behavior:** Mentor truy cập danh sách bài nộp, lọc theo khóa học/trạng thái, xem các bài phù hợp và mở chi tiết một bài. Inventory muốn deadline/owner và route sang ME-10. Các trạng thái màn hình đề xuất trong inventory là `loading/empty/ready/error`.

**Current UI assets:** [ảnh gốc](../../screen_stitch/04_mentor/ME-09_danh-sach-bai-can-cham/screen.png) và [HTML](../../screen_stitch/04_mentor/ME-09_danh-sach-bai-can-cham/code.html) thể hiện duy nhất empty state. Không có table/card/hàng, không có trang loaded, không có biểu diễn deadline/owner, không có pagination hoặc lỗi. HTML có các lựa chọn khóa học/status tĩnh và ô search, không gửi request. Nút refresh chỉ animate/disable trong 750 ms; nút reset chỉ đặt lại giá trị cục bộ. Header, notification, profile và footer có `href="#"`.

**Current API source:** route/module/query/model của #54 hiện trả `ApiEnvelope<Page<Submission>>`, trong đó `Submission` có `id`, `assignment_id`, `user_id`, `content?`, `files[]`, `status`, `submitted_at`, `score?`, `feedback?`. API không trả due date, assignment title, course title, `course_id`, Student display name hay rubric. `user_id` không tương đương tên/nhãn “owner”.

### A.4. Contract API #54 và sai khác cardinality

| Hạng mục | Inventory/contract kỳ vọng | AC/API DD/current source |
|---|---|---|
| Cardinality | `list_screen.md` ghi “không khẳng định response Page khi contract chỉ Submission” và đánh dấu lỗi cardinality. | AC-23 diagram hiện ghi `ApiEnvelope<Page<Submission>>`; API #54 DD gọi collection response là fallback `DERIVED`; current route/model cũng trả Page. API DD vẫn `Draft — Needs Confirmation`. |
| Filter | Course/status theo inventory. | `course_id?: int64`, `status?: string`, `page?: int32=1`; không có `q`, sort hay size query. |
| Danh sách | Bài nộp cần chấm; inventory mong deadline/owner. | Response fields ở trên không cung cấp deadline, tên owner, course title hay assignment title. |
| Handoff ID | Inventory gọi `submission_id`. | List response dùng `id`; #55 nhận `{submission_id}` trên path. Mapping `id → submission_id` hợp lý về kỹ thuật nhưng cần thống nhất tên logical DTO. |

Đây là **DISCREPANCY** giữa inventory còn hiệu lực và API DD/diagram/current implementation. DD không coi source đã âm thầm phê duyệt contract. Chủ sở hữu API/schema cần xác nhận response Page và mapping ID trước khi gỡ blocker.

### A.5. API #54 hiện hành

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

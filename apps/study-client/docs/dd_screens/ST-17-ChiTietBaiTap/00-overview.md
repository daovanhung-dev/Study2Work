# ST-17 — Chi tiết bài tập · Tổng quan

| Trường | Giá trị |
|---|---|
| Screen ID | `ST-17` |
| Module | Student |
| Route | `/student/assignments/:assignmentId` — Study Client route; deployed runtime chưa xác minh |
| Actor/role | Student Bearer; API #33 currently checks role only |
| DD status | Eligibility/visual gaps open; **Implementation:** PARTIAL · **Runtime:** NOT VERIFIED. #33 source and client caller exist. |
| Owner | Không được xác định trong inventory/DD nguồn đã chuyển; `CẦN_XÁC_NHẬN` |
| Version / last updated | 0.2 / 2026-11-20 |
| Nguồn đối chiếu | [ST-17.md](../../screen_stitch/03_student/ST-17_chi-tiet-bai-tap/ST-17.md), [ST-17_PLAN.md](../../screen_stitch/03_student/ST-17_chi-tiet-bai-tap/ST-17_PLAN.md), [ST-17_markers.json](../../screen_stitch/03_student/ST-17_chi-tiet-bai-tap/ST-17_markers.json), [list_screen.md](../../list_screen.md) |

## 1. Mục tiêu & phạm vi
- Mục tiêu: Đề bài, hạn nộp, điểm tối đa, file liên quan và nút nộp.
- In-scope: GET #33 → server quyết định deadline/permission; không dùng clock UI làm nguồn quyền. CTA chỉ handoff `assignmentId` sang ST-18 khi eligibility contract được duyệt.
- Out-of-scope: Không dùng local clock làm quyền nộp; live runtime chưa được xác minh.

### Current implementation — 2026-11-20

- ST-17 follows assignment route changes, cancels stale #33 reads, validates `DESIGN_RESOURCE_RETRIEVED` plus response ID/shape, and offers retry. It renders only fields returned by #33 and links to ST-18.
- #33 authenticates Student and reads the assignment by ID, but does not check enrollment/ownership, publication/status, or deadline. The ST-18/#35 submission path later checks ACTIVE enrollment and deadline; that does not protect assignment-detail access. The eligibility gate remains open.
- The current page is a basic assignment/detail layout and does not implement the full Stitch content, attached-resource view, or other screenshot metrics. No browser/runtime or tests were run.

## 2. Use cases chính
| Use case / AC | Actor | Kết quả kỳ vọng theo inventory |
|---|---|---|
| AC-17 | Theo DD nguồn; `CẦN_XÁC_NHẬN` nếu nguồn chưa chốt | Đề bài, hạn nộp, điểm tối đa, file liên quan và nút nộp. |

## 3. Precondition / Entry / Dependencies
- Điều kiện vào, role guard và dependency: xem trích đoạn tổng quan nguồn; không bổ sung giả định.
- API references: #33
- Liên kết màn hình dự kiến: [ST-18](../ST-18-SoanVaNopBaiTap/00-overview.md), [ST-09](../ST-09-TongQuanKhoaDangHoc/00-overview.md)
- Links: [UI](01-ui-elements.md) · [Events](02-events.md) · [Navigation](06-navigation.md)

## 4. UI states
| State | Nguồn | Giá trị |
|---|---|---|
| Inventory states | `list_screen.md` | loading/open/closed/not-found |
| Current source | Study Client ST-17 | `loading / error+retry / loaded fields / ST-18 link`; deployed runtime NOT VERIFIED |

## 5. Luồng chính và hình ảnh
- Ảnh clean: [screen-clean.png](images/screen-clean.png) (copy từ [ST-17 source screen.png](../../screen_stitch/03_student/ST-17_chi-tiet-bai-tap/screen.png))
- Ảnh numbered: [screen-numbered.png](images/screen-numbered.png) (copy từ [source annotated PNG](../../screen_stitch/03_student/ST-17_chi-tiet-bai-tap/screen_annotated.png))
- Luồng: GET #33 → server quyết định deadline/permission; không dùng clock UI làm nguồn quyền. CTA chỉ handoff `assignmentId` sang ST-18 khi eligibility contract được duyệt.
- Priority: P1; Gate/source status: **DD BLOCKED; IMPLEMENTATION PARTIAL; RUNTIME NOT VERIFIED:** #33 caller/source exists but its lookup lacks owner/enrollment/status/deadline predicates; its response covers only assignment ID/course/title/description/due/max score. Stitch fields and eligibility are incomplete; legacy BIGINT assignment DDL differs from V1-PILOT; PNG/HTML state and visual target differ.

## 6. Open questions / Change log
- `CẦN_XÁC_NHẬN`: các gate/source questions trong inventory và DD nguồn vẫn giữ nguyên; không tự đóng blocker.
- 2026-11-08 — Chuyển nội dung nguồn sang 8-file template; không chỉnh source, không xác minh runtime.
- 2026-11-20 — Cập nhật caller #33 route/response validation và ghi rõ thiếu kiểm tra enrollment/visibility ở backend.

## Trạng thái và ranh giới bằng chứng

# ST-17 — Chi tiết bài tập

> Các đoạn “hiện trạng/current behavior” bên dưới được giữ từ source DD cũ để truy vết; trạng thái source hiện tại là phần **Current implementation — 2026-11-20** ở trên.

> **Trạng thái nguồn hiện tại:** DD BLOCKED; IMPLEMENTATION PARTIAL; RUNTIME NOT VERIFIED. API #33 and Study Client caller exist; assignment access policy remains open.

## Trích đoạn tổng quan từ DD nguồn

### Trích từ DD nguồn: A. Tổng quan màn hình

### A.1. Định danh và quyền truy cập

| Thuộc tính | Đặc tả |
|---|---|
| Screen ID / tên | ST-17 — Chi tiết bài tập (Page) |
| Mục tiêu | Cho Student xem đề bài, deadline và điểm tối đa trước khi chuyển sang luồng chuẩn bị/nộp bài tập. |
| Actor | Student có Bearer JWT theo API catalog #33. Predicate kiểm tra Student có quyền xem assignment/course chưa được chốt. |
| Route thiết kế | `/student/assignments/:assignmentId` — đề xuất trong inventory, không phải route runtime hiện hành. |
| Màn hình liên quan | ST-18 — Soạn và nộp bài tập; ST-09 — Tổng quan khóa đang học. Inventory chỉ ghi liên quan, không xác định ST-09 là đích của breadcrumb/CTA. |
| API chính | #33 `GET /api/v1/assignments/{assignment_id}`. API #34/#35/#36 thuộc các bước tiếp theo của AC-17, không phải request của ST-17. |
| Elements / events | 49 elements `ST17-EL-01`…`ST17-EL-49`; 7 events `ST17-EV-01`…`ST17-EV-07`. |
| Hiện trạng | Study Web `UNWIRED`; API #33 is catalog/Draft-only with Student route/module/test `NOT_FOUND`; downstream #34 upload is source-backed locally, while Student #35/#36 route/module/test are `NOT_FOUND`; no runtime verification. |

### A.2. Điều kiện vào, dữ liệu và rời màn hình

- Route nhận `assignmentId`; API #33 khai báo `assignment_id:int64` trong path. Quy tắc parse, miền giá trị dương, overflow và lỗi client chưa được chuẩn hóa.
- API catalog yêu cầu `Authorization: Bearer <JWT>` với role Student. Không gửi `user_id` trong path/query/body.
- API #33 không có query hoặc body; success là `200 DESIGN_RESOURCE_RETRIEVED` với `ApiEnvelope<Assignment>`; errors trong catalog là 401/403/404/500.
- Schema logic `Assignment` chỉ có `id`, `course_id`, `title`, optional `description`, optional `due_at`, và required `max_score`. `Assignment` không có submission rule, status nộp, rubric, resource list, video, mentor, course title hay lịch sử bài nộp.
- AC-17 yêu cầu đọc “Assignment + submission rule”, rồi xét permission/deadline; nhánh tiếp theo mới đi tới ST-18, #34 upload, #35 submit và #36 confirmation. “Submission rule” không có schema trong response #33.
- Inventory states: `loading/open/closed/not-found`. API #33 DD chưa chốt #33 có trả assignment sau deadline hay từ chối; AC-17 nêu 403/409 nhưng catalog #33 không khai báo 409. Không suy ra `open/closed` từ local clock.
- CTA “Soạn và Nộp bài tập ngay” trong PNG có thể liên quan tới ST-18. Route/design handoff còn cần xác nhận; nếu được duyệt, dữ liệu tối thiểu là `assignmentId` trong path ST-18. Không gọi #34/#35/#36 từ ST-17.

### A.3. Expected behavior và current behavior

**Expected behavior theo inventory/AC:** Student mở `/student/assignments/:assignmentId`, đọc #33, và server quyết định access/deadline; khi được phép thì tiếp tục flow AC-17. UI không dùng đồng hồ phía client làm nguồn quyền nộp duy nhất.

**Current behavior theo source:** `screen.png` là loaded Student mockup có trạng thái Open, tiến độ/điểm, deadline, rubric, tệp đính kèm, checklist, mentor, SLA, lịch sử và CTA; các giá trị/claims đó vẫn là mẫu thiết kế. Angular route hiện gọi #33, hiển thị title và description tùy chọn, cùng loading/error/retry states. Due date, max score, course identity và CTA ST-18 đang ẩn vì format/nullability và eligibility policy chưa được duyệt. `code.html` vẫn là companion prototype cũ, không phải runtime source.

Current Study Server source không có Student API #33 route/module/test. Frontend caller và local UI source không chứng minh deployed API, database, authenticated browser hoặc production runtime.

**Design-system discrepancy:** the 667px PNG remains a dense two-column loaded mockup with tightly packed header navigation and small copy; the companion HTML loads Plus Jakarta Sans and Material Symbols from Google Fonts plus Tailwind from a CDN and uses a 1440px content maximum. The Study Web target `.agents/web-study/design.md` calls for no remote font import, a content width around 1120px, reflow below 768px, and 44px minimum controls. The mockup/HTML are not aligned with that target and neither proves current implementation. Preserve both files and resolve the canonical state/layout before frontend work.

### A.4. API #33 contract và giới hạn

| Thuộc tính | Contract hiện có | Giới hạn |
|---|---|---|
| Method / endpoint | `GET /api/v1/assignments/{assignment_id}` | Catalog/design-only; route Student hiện hành không có. |
| Authentication | Bearer JWT; role Student | API #33 chưa gọi auth helper; direct assignment/course access predicate chưa chốt. |
| Path | `assignment_id:int64!` | Không có min/max/positivity/parse-failure mapping. |
| Query / body | Không khai báo | Không thêm filter, `user_id` hoặc request body. |
| Success | HTTP 200 `DESIGN_RESOURCE_RETRIEVED`; `ApiEnvelope<Assignment>` | API DD `Draft — Needs Confirmation`; exact optional/null serialization chưa chốt. |
| Errors | 401 `DESIGN_AUTHENTICATION_REQUIRED`; 403 `DESIGN_ACCESS_DENIED`; 404 `DESIGN_RESOURCE_NOT_FOUND`; 500 `DESIGN_INTERNAL_ERROR` | AC-17 403/409 nhánh quá hạn/không quyền khác catalog; không thêm 409. |
| Assignment fields | `id`, `course_id`, `title`, `description?`, `due_at?`, `max_score` | Không chứa những dữ liệu phụ trong mockup; logical `course_id`/`max_score` bắt buộc nhưng DDL cho nullable. |

API #33 DD questions Q-33-01…05 giữ mở: access/403-vs-404; deadline GET/rejection/boundary/403-vs-409; submission-rule ownership/schema; nullability/timezone/decimal serialization; path parsing/error mapping. Candidate `assignments` table là design evidence, không phải live schema.

### A.5. Bảo mật và dữ liệu

- Chỉ Student Bearer được yêu cầu #33 theo catalog. Server phải xác minh identity, role và assignment/course permission; client không tự gửi owner ID.
- Không hiển thị nội dung assignment của Student khác. Chính sách 403/404 masking chưa được duyệt.
- Deadline, assignment status và quyền nộp phải đến từ server-owned policy. Đồng hồ trình duyệt có thể sai lệch và không được dùng làm authorization.
- Không coi status “Chưa nộp”, lịch sử `0 lần nộp`, progress `20%`, score weight, mentor, rubric hoặc tài nguyên trong PNG là dữ liệu #33.
- Legacy Study Server DDL and table notes contain BIGINT `assignments` and `assignment_submissions` candidates; `course_id`/`max_score` are nullable, physical `name` maps to logical `title`, and `due_at` has no timezone in the DDL. V1-PILOT `infra/postgres/02_study_db.sql` contains no business `assignments` or `assignment_submissions` tables (`service_role_assignments` is a different identity relation). No live schema, migration deployment, or approved API #33 adapter is verified.

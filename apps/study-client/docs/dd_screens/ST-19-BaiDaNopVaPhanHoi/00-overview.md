# ST-19 — Bài đã nộp và phản hồi · Tổng quan

| Trường | Giá trị |
|---|---|
| Screen ID | `ST-19` |
| Module | Student |
| Route | `/student/submissions/:submissionId` — Study Client route; deployed runtime chưa xác minh |
| Actor/role | Student Bearer; API #36 queries by authenticated owner |
| DD status | Full feedback/visual contract remains open; **Implementation:** PARTIAL · **Runtime:** NOT VERIFIED. #36 and client caller exist. |
| Owner | Không được xác định trong inventory/DD nguồn đã chuyển; `CẦN_XÁC_NHẬN` |
| Version / last updated | 0.2 / 2026-11-20 |
| Nguồn đối chiếu | [ST-19.md](../../screen_stitch/03_student/ST-19_bai-da-nop-va-phan-hoi/ST-19.md), [ST-19_PLAN.md](../../screen_stitch/03_student/ST-19_bai-da-nop-va-phan-hoi/ST-19_PLAN.md), [ST-19_markers.json](../../screen_stitch/03_student/ST-19_bai-da-nop-va-phan-hoi/ST-19_markers.json), [list_screen.md](../../list_screen.md) |

## 1. Mục tiêu & phạm vi
- Mục tiêu: Hiển thị timestamp, file, trạng thái chấm, score/feedback khi có.
- In-scope: GET #36 cho Student; hiển thị receipt/status, score/feedback chỉ khi `GRADED`; không mở file URL khi policy truy cập chưa rõ.
- Out-of-scope: Không kết luận live runtime đã chạy.

### Current implementation — 2026-11-20

- ST-19 follows `submissionId` changes, cancels stale #36 reads, validates `DESIGN_RESOURCE_RETRIEVED` plus response identity/shape, and offers retry.
- #36 authenticates Student and queries by both `submission_id` and token-derived `user_id`; missing/foreign submissions return 404. The query only selects score/feedback when status is `GRADED`; it maps the legacy single `file_url` into a zero-or-one `files[]` result.
- The page currently renders the returned status and optional submitted text. It withholds timestamp, score, feedback and file metadata while timezone, disclosure and asset-mapping decisions remain open. It links back to assignment detail. It does not implement the full Stitch rubric, mentor/cohort/skills/next-assignment interactions or progress route because #36 does not supply those contracts.
- The page labels only `SUBMITTED` and `GRADED` as “Đã nộp” and “Đã chấm”; any other submission status uses a neutral unsupported-state label. File status is omitted because its full enum is not established.
- API #35 returns `data.id` while inventory names `submission_id`; the current ST-18 caller passes `data.id`. Runtime and tests were not verified.

## 2. Use cases chính
| Use case / AC | Actor | Kết quả kỳ vọng theo inventory |
|---|---|---|
| AC-17 | Theo DD nguồn; `CẦN_XÁC_NHẬN` nếu nguồn chưa chốt | Hiển thị timestamp, file, trạng thái chấm, score/feedback khi có. |

## 3. Precondition / Entry / Dependencies
- Điều kiện vào, role guard và dependency: xem trích đoạn tổng quan nguồn; không bổ sung giả định.
- API references: #36
- Liên kết màn hình dự kiến: [ST-17](../ST-17-ChiTietBaiTap/00-overview.md), [ST-20](../ST-20-TongQuanTienDo/00-overview.md)
- Links: [UI](01-ui-elements.md) · [Events](02-events.md) · [Navigation](06-navigation.md)

## 4. UI states
| State | Nguồn | Giá trị |
|---|---|---|
| Inventory states | `list_screen.md` | submitted/pending-review/graded/denied |
| Current source | Study Client ST-19 | `loading / error+retry / submitted-or-graded receipt / attachment metadata`; deployed runtime NOT VERIFIED |

## 5. Luồng chính và hình ảnh
- Ảnh clean: [screen-clean.png](images/screen-clean.png) (copy từ [ST-19 source screen.png](../../screen_stitch/03_student/ST-19_bai-da-nop-va-phan-hoi/screen.png))
- Ảnh numbered: [screen-numbered.png](images/screen-numbered.png) (copy từ [source annotated PNG](../../screen_stitch/03_student/ST-19_bai-da-nop-va-phan-hoi/screen_annotated.png))
- Luồng: GET #36 cho Student; inventory yêu cầu kiểm tra ownership nhưng predicate trong API #36 DD còn SOURCE_REQUIRED. Không tự hiển thị GRADED nếu response chỉ là SUBMITTED; score/feedback cần disclosure policy.
- Priority: P1; Gate/source status: **DD BLOCKED; IMPLEMENTATION PARTIAL; RUNTIME NOT VERIFIED:** #36 caller/source exists and enforces owner-scoped lookup; score/feedback are returned only for GRADED; one legacy `file_url` maps to a files array. File URL policy, status lifecycle/timezone, live schema, `data.id`/`submission_id`, detailed Stitch metrics and the screenshot/HTML visual discrepancy remain open.

## 6. Open questions / Change log
- `CẦN_XÁC_NHẬN`: các gate/source questions trong inventory và DD nguồn vẫn giữ nguyên; không tự đóng blocker.
- 2026-11-08 — Chuyển nội dung nguồn sang 8-file template; không chỉnh source, không xác minh runtime.
- 2026-11-20 — Ghi nhận caller #36, ownership/graded projection, safe file metadata, route validation and current design gaps.

## Trạng thái và ranh giới bằng chứng

# ST-19 — Bài đã nộp và phản hồi

> Các đoạn “hiện trạng/current behavior” bên dưới được giữ từ source DD cũ để truy vết; trạng thái source hiện tại là phần **Current implementation — 2026-11-20** ở trên.

> **Trạng thái nguồn hiện tại:** DD BLOCKED; IMPLEMENTATION PARTIAL; RUNTIME NOT VERIFIED. API #36 and Study Client caller exist; feedback/file policy and detailed design gaps remain.

## Trích đoạn tổng quan từ DD nguồn

### Trích từ DD nguồn: A. Tổng quan màn hình

### A.1. Định danh

| Thuộc tính | Đặc tả |
|---|---|
| Screen ID / tên | ST-19 — Bài đã nộp và phản hồi (Page) |
| Mục tiêu | Student xem biên nhận bài nộp, trạng thái chấm và thông tin phản hồi được phép công bố. |
| Actor | Student theo inventory và API catalog #36; quyền cụ thể trên từng submission chưa được chốt. |
| Route thiết kế | `/student/submissions/:submissionId` — route đề xuất trong inventory, chưa có Study Web router/runtime. |
| API dự kiến | GET API #36 `/api/v1/submissions/{submission_id}`. |
| Màn hình liên quan | ST-17 — Chi tiết bài tập; ST-18 — Soạn và nộp bài tập; ST-20 — Tổng quan tiến độ. |
| Elements / events | 58 elements `ST19-EL-01…ST19-EL-58`; 13 events `ST19-EV-01…ST19-EV-13`. |
| Trạng thái | DD BLOCKED; IMPLEMENTATION BLOCKED; RUNTIME NOT VERIFIED. |

### A.2. Điều kiện vào, dữ liệu và rời màn hình

- Theo F06, ST-18 gửi bài qua API #35 rồi chuyển submission ID sang ST-19; inventory gọi khóa này là `submission_id`. API #35 DD draft mô tả `data.id`. Đây là **DISCREPANCY**; chưa có quy tắc handoff để xác định `:submissionId`.
- Inventory ST-19 yêu cầu GET #36 theo owner, hiển thị timestamp, file, trạng thái chấm, điểm/feedback khi có và không tự nâng `SUBMITTED` thành `GRADED`.
- API catalog #36 khai báo `GET /api/v1/submissions/{submission_id}`, Student Bearer JWT, `submission_id:int64!`, response `ApiEnvelope<Submission>`, HTTP 200 `DESIGN_RESOURCE_RETRIEVED`, và đúng các lỗi 401 `DESIGN_AUTHENTICATION_REQUIRED`, 403 `DESIGN_ACCESS_DENIED`, 404 `DESIGN_RESOURCE_NOT_FOUND`, 500 `DESIGN_INTERNAL_ERROR`.
- API #36 DD là `Draft — Needs Confirmation`. Chưa có rule chốt Student chỉ đọc bài của mình hay thêm điều kiện enrollment/course; chưa chốt cách phân biệt 403 với 404 khi row thuộc người khác.
- Logical Submission có `id`, `assignment_id`, `user_id`, `content?`, `files: UploadAsset[]`, `status`, `submitted_at`, `score?` dạng decimal-string và `feedback?`. Candidate DDL `assignment_submissions` có một `file_url` đơn, score/feedback nullable và status string; không map đủ `files[]`, và DDL không xác nhận live schema.
- Screenshot có nhiều nội dung không thuộc logical Submission: tên course/assignment, rubric, thống kê lớp, điểm từng tiêu chí, skill index, link GitHub/deployment/report, ảnh preview, CTA comments/meeting/next assignment. Các nội dung này là design sample; không tạo mapping hoặc API phụ cho chúng.
- Screenshot `screen.png` là loaded, graded sample UI. `code.html` là Guest/unavailable fallback với copy “Chưa có thông tin bài nộp để hiển thị.” và link `/student/courses`. HTML tải Tailwind CDN, cấu hình Tailwind và remote Google Fonts; không có form, API call hoặc event handler cho nghiệp vụ ST-19, nên không đại diện cho loaded PNG.
- Visual source chưa khớp [Study Web design target](../../../../../.agents/web-study/design.md): HTML dùng Plus Jakarta Sans, remote fonts/CDN và max-width 1440px; guide yêu cầu Inter/system stack, không thêm remote font import và content width khoảng 1120px. PNG/HTML tiếp tục là design evidence, không phải runtime behavior.
- Study Web hiện không có editable app source/package/router/Student routes; ignored dist chỉ có `/`. Không có hành vi runtime ST-19 được xác minh.

### A.3. Expected behavior và current behavior

**Expected behavior:** nhận ID bài nộp từ ST-18, xác thực Student, gọi GET #36, kiểm tra envelope/business code và hiển thị đúng receipt/grade fields mà API được duyệt cho phép. `SUBMITTED` không tự biến thành `GRADED`; score/feedback chỉ được trình bày theo disclosure policy đã chốt. Các links quay lại ST-17/ST-20 theo route/data hợp lệ.

**Current behavior:** Study Web có ST-19 route/page và caller #36. The page renders the server status and optional submitted text only. It withholds timestamp formatting, score, feedback and file metadata because timezone, disclosure and asset-mapping rules remain unresolved. The Student #36 route/query are local source evidence; deployed API, live schema, browser session and production runtime remain unverified. Mentor API #55 is a separate endpoint and does not replace #36. PNG/HTML remain design references, not runtime.

### A.4. API contract và trạng thái source

| Thuộc tính | API #36 |
|---|---|
| Method / endpoint | `GET /api/v1/submissions/{submission_id}` |
| Authentication | Student Bearer JWT theo catalog; caller identity lấy từ token, không nhận user ID từ URL/body. |
| Path | `submission_id:int64!`; positivity, range và parse-failure response chưa được định nghĩa. |
| Query / body | Không khai báo query parameter hoặc request body. |
| Success | HTTP 200, `DESIGN_RESOURCE_RETRIEVED`, `ApiEnvelope<Submission>`. |
| Errors | Chỉ 401 `DESIGN_AUTHENTICATION_REQUIRED`, 403 `DESIGN_ACCESS_DENIED`, 404 `DESIGN_RESOURCE_NOT_FOUND`, 500 `DESIGN_INTERNAL_ERROR`. Không thêm 400/422 theo suy đoán. |
| Current source | Student API #36 route/module/query/test `NOT_FOUND`; không có runtime call để xác minh. Mentor API #55 là operation khác. |
| Open policy | Owner/access predicate; 403-vs-404 masking; score/feedback release; file association/URL; status lifecycle/timezone; malformed path; candidate schema vs live schema. |

### A.5. Bảo mật và giới hạn dữ liệu

- Không gửi `user_id` do client nhập; mọi quyết định truy cập phải dựa vào principal từ Bearer token ở server.
- Role Student không tự chứng minh row-level ownership. Không trả dữ liệu trước khi API #36 có access predicate được duyệt.
- Không dùng dữ liệu Mentor API #55 để lấp response Student #36; khác actor, path và authorization.
- Không render hoặc mở file từ candidate `file_url` khi chưa chốt asset association, URL type, access control và metadata mapping của `UploadAsset`.
- `score`, `feedback`, rubric breakdown, cohort percentile, mentor bio, skill progress và project links không được lấy từ mockup sample.
- DDL/diagrams/DD là thiết kế đã commit; live database, deployed API, client routing, signed URL behavior và production state đều `NOT VERIFIED`.
- Khi Study Web source được khôi phục, áp dụng target trong guide: semantic ocean tokens, content width khoảng 1120px, reflow theo mobile/tablet/desktop, control tối thiểu 44px, keyboard focus rõ, contrast và reduced-motion. PNG hiện không cung cấp bằng chứng responsive/accessibility; HTML mockup dùng max-width 1440px và remote font/CDN, chưa khớp target.

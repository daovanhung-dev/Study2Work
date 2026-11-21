# ME-03 — Data Flow & State

## 1. Nguồn dữ liệu
| Field / object | Type | Source | Destination | Cập nhật khi |
|---|---|---|---|---|
| Chỉ liệt kê theo bằng chứng trong excerpt bên dưới | Theo DD/API source | API/inventory/design; status phải giữ nguyên | UI/state nêu ở DD nguồn | Theo event source |

## 2. State model

> Không tạo DTO/ViewModel mới khi chưa có contract. State, DTO và mapping được trích nguyên ngữ cảnh từ DD nguồn bên dưới.

## 3. API DTO → ViewModel mapping

### Trích từ DD nguồn: 2. Luồng tổng thể và ranh giới dữ liệu

```mermaid
flowchart TD
  A[ME-02 chọn course] -->|courseId, route đề xuất| B[ME-03 Workspace]
  B --> C[GET #49 Content[]]
  B --> D[GET #65 progress roster]
  C --> E[Cây Content phẳng]
  D --> F[Tiến độ tổng hợp từng Student]
  B --> G[ME-04 tạo lecture]
  B --> H[ME-06 quản lý content]
  B --> I[ME-16 báo cáo tiến độ]
```

ME-02/#46 là expected source nhận diện course; #49 và #65 đều tự xác thực Mentor và kiểm tra direct owner phía server. Không coi `courseId`, title hay permission trong client state là bằng chứng truy cập. #46 hiện cũng chỉ liệt kê course có `courses.mentor_id = JWT sub`; AC-21 nói course có thể được sở hữu **hoặc phân công**, nên assigned-course flow chưa được thể hiện trong các API hiện tại.

### 2.1 API #49 — cây Content

| Thành phần | Contract/source hiện tại |
|---|---|
| Route | `GET /api/v1/mentor/courses/{course_id}/content` |
| Auth | `Authorization: Bearer <JWT>`; shared guard yêu cầu `MENTOR`, lấy numeric JWT `sub`, chạy trước truy vấn. |
| Input | `course_id` path theo signed-int64; không query/body. Sai định dạng/range hoặc course không tồn tại → 404. |
| Access | Đọc `courses.id`, so `courses.mentor_id` với JWT `sub`; khác owner → 403. Quan hệ assignment không được kiểm tra. |
| Read | `contents` cùng course, `deleted_at IS NULL`, không lọc `status`, không phân trang; order `parent_id NULLS FIRST, content_order ASC, id ASC`. Không ghi/commit. |
| Response 200 | `businessCode=DESIGN_RESOURCE_RETRIEVED`; `data` là mảng phẳng. Mỗi item có `id:int64`, `course_id:int64`, `content_type:string`, `title:string`, `payload:object`, `status:string`, `parent_id?:int64`, `order:int32`. Root có `parent_id=null` bị omit. Empty tree vẫn 200 với `data: []`. |
| Mapping guard | Payload phải là JSON object; ID phải unique; mọi parent phải nằm trong response; course ID phải khớp; cycle/invalid projection làm hỏng toàn response. |
| Errors | 401 `DESIGN_AUTHENTICATION_REQUIRED`; 403 `DESIGN_ACCESS_DENIED`; 404 `DESIGN_RESOURCE_NOT_FOUND`; 500 `DESIGN_INTERNAL_ERROR`. SQL/projection/tree detail không trả cho client. |
| Giới hạn dùng cho ME-03 | Flat Content nodes không tự chứng minh cấu trúc `chapter/module/lesson`. `content_type`, `status`, payload subtype, revision và publish rules chưa chốt. Không suy số bài giảng đã duyệt từ status mẫu. |

### 2.2 API #65 — tiến độ toàn lớp

| Thành phần | Catalog trực tiếp | Current source cục bộ |
|---|---|---|
| Route | `GET /api/v1/mentor/courses/{course_id}/progress` | Đã đăng ký tại router và gọi module #65. |
| Auth/input | Bearer JWT, role Mentor; `course_id:int64!`; không query/body. | Shared Mentor guard; signed-int64 parser; direct owner check. |
| Response | `ApiEnvelope<Page<Course>>` theo [catalog #65](../../../../../docs/lists/list_api.md#L175). | `ApiEnvelope<Page<MentorStudentProgress>>`; local shape là DERIVED và đang DISCREPANCY. |
| Roster | Không có progress schema trong `Page<Course>`. | Distinct Student thuộc enrollment ACTIVE; người dùng phải có role `STUDENT`. Một item/Student. |
| Denominator | Không có lesson/progress rule trong catalog. | Chỉ `lessons.status='PUBLISHED'`; chọn progress row mới nhất theo `last_accessed_at DESC NULLS LAST, id DESC`. |
| Tính toán | Chưa định nghĩa. | `completed_lessons` đếm status `COMPLETED`; `progress_percent = floor(sum(progress_percent)/total_published_lessons)`. Không có lesson thì bằng 0. Missing row/percent được tính 0; projection với status/range không hợp lệ trả safe 500. |
| Pagination | Catalog không khai báo page/size input. | Trả toàn bộ roster: `page=1`, `size=total`, `total=total`, `total_pages=1` khi có item, nếu rỗng thì `size=0`, `total_pages=0`. Không có bound. |
| Errors | 401/403/404/500 theo catalog. | Cùng status/business code; direct-owner mismatch 403, course/path không tồn tại/sai 404. |
| Giới hạn dùng cho ME-03 | Catalog chưa biểu diễn tiến độ. | Course-wide theo từng Student; không có tiến độ từng module, event feed, risk flag, quiz/lab score, review/rating hoặc thời điểm gần nhất. Response, eligibility, formula và full-roster page phải chờ owner/schema approval. |

API #65 và API #49 cùng dùng legacy BIGINT source artifacts; DDL/migrations đã kiểm tra tĩnh, live schema/deployment chưa xác minh. `#65` không gọi `#66`/`#67` phía server. AC-26 liệt kê #65, #67, #66 cho class progress, selected-Student detail và analytics riêng; inventory ME-03 chỉ chỉ định #65.

### 2.3 Course summary và mockup data

API #46 hiện có `Course` gồm id/title/optional description/thumbnail/price/status/Mentor summary. Query #46 phân trang và chỉ giới hạn trực tiếp theo `courses.mentor_id`; nó không có `courseCode`, cohort/term, academic standard, enrollment count, last-content-updated, course-average progress, rating hay group/submission metrics. #49/#65 cũng không trả Course summary. Direct route/refresh vì vậy chưa có source ổn định cho phần hero.

| Nhóm mockup | #49/#65 cung cấp | Kết luận cho DD |
|---|---|---|
| Code/status/cohort/last updated/owner/standard | #49 chỉ có Content rows; #65 có Student progress; #46 chỉ có Course cơ bản và Mentor summary. | Code, cohort, standard, timestamp và enrollment count là sample; chưa có field mapping đầy đủ. |
| Course completion KPI | #65 trả progress từng Student; #49 trả Content nodes. | Không lấy trung bình các student progress thành card KPI nếu chưa duyệt công thức/roster/rounding. |
| Chương/module/lecture counts, approved/draft | #49 trả Content tree, status/type open string; lessons là model/table riêng. | Không suy chapter hoặc lecture counts/status từ Content node; mapping cần owner xác nhận. |
| Module completion, submissions và Capstone | #65 chỉ có toàn course/Student summary trên published lessons. | Module-level progress, submission totals, lab/capstone completion không có nguồn. |
| At-risk learners/reminder/scheduling | #65 không có risk status, streak, quiz/lab score hay scheduling field. | Ngưỡng `>7 ngày`, risk score, danh sách/count và 1:1 scheduling đều chưa có contract. |
| Weekly feed/learning velocity | #65 không có event list/time series; per-Student summary không biểu diễn activity chronology. | 142 activities/week/submissions and dates in image are sample; endpoint/source/destination chưa xác định. |
| Satisfaction/drop-off/reviews | #49/#65 không có rating/review/drop-off data. | 9.4/10, 98 reviews, 6% drop-off và satisfaction bar không có API mapping. |
| Repository/assets and AI | API #49 payload is generic object; response does not guarantee external resource URLs or AI results. | Git/Figma/Sandbox links và “12 logic errors” là sample; URL allowlist, safe link and AI contract absent. |
| Excel export | Không có export API/file contract trong inventory. | Không thể tuyên bố file tải xuống từ nút hiện tại. |

### Trích từ DD nguồn: 2. Luồng tổng thể và ranh giới dữ liệu

```mermaid
flowchart TD
  A[ME-02 chọn course] -->|courseId, route đề xuất| B[ME-03 Workspace]
  B --> C[GET #49 Content[]]
  B --> D[GET #65 progress roster]
  C --> E[Cây Content phẳng]
  D --> F[Tiến độ tổng hợp từng Student]
  B --> G[ME-04 tạo lecture]
  B --> H[ME-06 quản lý content]
  B --> I[ME-16 báo cáo tiến độ]
```

ME-02/#46 là expected source nhận diện course; #49 và #65 đều tự xác thực Mentor và kiểm tra direct owner phía server. Không coi `courseId`, title hay permission trong client state là bằng chứng truy cập. #46 hiện cũng chỉ liệt kê course có `courses.mentor_id = JWT sub`; AC-21 nói course có thể được sở hữu **hoặc phân công**, nên assigned-course flow chưa được thể hiện trong các API hiện tại.

### 2.1 API #49 — cây Content

| Thành phần | Contract/source hiện tại |
|---|---|
| Route | `GET /api/v1/mentor/courses/{course_id}/content` |
| Auth | `Authorization: Bearer <JWT>`; shared guard yêu cầu `MENTOR`, lấy numeric JWT `sub`, chạy trước truy vấn. |
| Input | `course_id` path theo signed-int64; không query/body. Sai định dạng/range hoặc course không tồn tại → 404. |
| Access | Đọc `courses.id`, so `courses.mentor_id` với JWT `sub`; khác owner → 403. Quan hệ assignment không được kiểm tra. |
| Read | `contents` cùng course, `deleted_at IS NULL`, không lọc `status`, không phân trang; order `parent_id NULLS FIRST, content_order ASC, id ASC`. Không ghi/commit. |
| Response 200 | `businessCode=DESIGN_RESOURCE_RETRIEVED`; `data` là mảng phẳng. Mỗi item có `id:int64`, `course_id:int64`, `content_type:string`, `title:string`, `payload:object`, `status:string`, `parent_id?:int64`, `order:int32`. Root có `parent_id=null` bị omit. Empty tree vẫn 200 với `data: []`. |
| Mapping guard | Payload phải là JSON object; ID phải unique; mọi parent phải nằm trong response; course ID phải khớp; cycle/invalid projection làm hỏng toàn response. |
| Errors | 401 `DESIGN_AUTHENTICATION_REQUIRED`; 403 `DESIGN_ACCESS_DENIED`; 404 `DESIGN_RESOURCE_NOT_FOUND`; 500 `DESIGN_INTERNAL_ERROR`. SQL/projection/tree detail không trả cho client. |
| Giới hạn dùng cho ME-03 | Flat Content nodes không tự chứng minh cấu trúc `chapter/module/lesson`. `content_type`, `status`, payload subtype, revision và publish rules chưa chốt. Không suy số bài giảng đã duyệt từ status mẫu. |

### 2.2 API #65 — tiến độ toàn lớp

| Thành phần | Catalog trực tiếp | Current source cục bộ |
|---|---|---|
| Route | `GET /api/v1/mentor/courses/{course_id}/progress` | Đã đăng ký tại router và gọi module #65. |
| Auth/input | Bearer JWT, role Mentor; `course_id:int64!`; không query/body. | Shared Mentor guard; signed-int64 parser; direct owner check. |
| Response | `ApiEnvelope<Page<Course>>` theo [catalog #65](../../../../../docs/lists/list_api.md#L175). | `ApiEnvelope<Page<MentorStudentProgress>>`; local shape là DERIVED và đang DISCREPANCY. |
| Roster | Không có progress schema trong `Page<Course>`. | Distinct Student thuộc enrollment ACTIVE; người dùng phải có role `STUDENT`. Một item/Student. |
| Denominator | Không có lesson/progress rule trong catalog. | Chỉ `lessons.status='PUBLISHED'`; chọn progress row mới nhất theo `last_accessed_at DESC NULLS LAST, id DESC`. |
| Tính toán | Chưa định nghĩa. | `completed_lessons` đếm status `COMPLETED`; `progress_percent = floor(sum(progress_percent)/total_published_lessons)`. Không có lesson thì bằng 0. Missing row/percent được tính 0; projection với status/range không hợp lệ trả safe 500. |
| Pagination | Catalog không khai báo page/size input. | Trả toàn bộ roster: `page=1`, `size=total`, `total=total`, `total_pages=1` khi có item, nếu rỗng thì `size=0`, `total_pages=0`. Không có bound. |
| Errors | 401/403/404/500 theo catalog. | Cùng status/business code; direct-owner mismatch 403, course/path không tồn tại/sai 404. |
| Giới hạn dùng cho ME-03 | Catalog chưa biểu diễn tiến độ. | Course-wide theo từng Student; không có tiến độ từng module, event feed, risk flag, quiz/lab score, review/rating hoặc thời điểm gần nhất. Response, eligibility, formula và full-roster page phải chờ owner/schema approval. |

API #65 và API #49 cùng dùng legacy BIGINT source artifacts; DDL/migrations đã kiểm tra tĩnh, live schema/deployment chưa xác minh. `#65` không gọi `#66`/`#67` phía server. AC-26 liệt kê #65, #67, #66 cho class progress, selected-Student detail và analytics riêng; inventory ME-03 chỉ chỉ định #65.

### 2.3 Course summary và mockup data

API #46 hiện có `Course` gồm id/title/optional description/thumbnail/price/status/Mentor summary. Query #46 phân trang và chỉ giới hạn trực tiếp theo `courses.mentor_id`; nó không có `courseCode`, cohort/term, academic standard, enrollment count, last-content-updated, course-average progress, rating hay group/submission metrics. #49/#65 cũng không trả Course summary. Direct route/refresh vì vậy chưa có source ổn định cho phần hero.

| Nhóm mockup | #49/#65 cung cấp | Kết luận cho DD |
|---|---|---|
| Code/status/cohort/last updated/owner/standard | #49 chỉ có Content rows; #65 có Student progress; #46 chỉ có Course cơ bản và Mentor summary. | Code, cohort, standard, timestamp và enrollment count là sample; chưa có field mapping đầy đủ. |
| Course completion KPI | #65 trả progress từng Student; #49 trả Content nodes. | Không lấy trung bình các student progress thành card KPI nếu chưa duyệt công thức/roster/rounding. |
| Chương/module/lecture counts, approved/draft | #49 trả Content tree, status/type open string; lessons là model/table riêng. | Không suy chapter hoặc lecture counts/status từ Content node; mapping cần owner xác nhận. |
| Module completion, submissions và Capstone | #65 chỉ có toàn course/Student summary trên published lessons. | Module-level progress, submission totals, lab/capstone completion không có nguồn. |
| At-risk learners/reminder/scheduling | #65 không có risk status, streak, quiz/lab score hay scheduling field. | Ngưỡng `>7 ngày`, risk score, danh sách/count và 1:1 scheduling đều chưa có contract. |
| Weekly feed/learning velocity | #65 không có event list/time series; per-Student summary không biểu diễn activity chronology. | 142 activities/week/submissions and dates in image are sample; endpoint/source/destination chưa xác định. |
| Satisfaction/drop-off/reviews | #49/#65 không có rating/review/drop-off data. | 9.4/10, 98 reviews, 6% drop-off và satisfaction bar không có API mapping. |
| Repository/assets and AI | API #49 payload is generic object; response does not guarantee external resource URLs or AI results. | Git/Figma/Sandbox links và “12 logic errors” là sample; URL allowlist, safe link and AI contract absent. |
| Excel export | Không có export API/file contract trong inventory. | Không thể tuyên bố file tải xuống từ nút hiện tại. |

### Trích từ DD nguồn: 4. Sự kiện và xử lý dữ liệu

Mọi `API #49/#65` response được bảo vệ lại ở server. Không lộ Course/Student data dựa vào client-only route guard. Không thay response lỗi bằng sample data. Chính sách cache, stale-result, cancel/retry và partial rendering chưa có FE source; các đề xuất dưới đây giữ trạng thái `BLOCKED` khi cần quyết định.

### `ME03-EV-01` — Vào workspace theo course

- **Trigger/type:** Route enter / page load, marker #6/#8–#11.
- **Input/precondition:** `courseId` từ route đề xuất hoặc ME-02 navigation; Mentor access token do app shell quản lý. AC-22/AC-26 yêu cầu permission tương ứng. Route/client session chưa wired.
- **Processing:** Lấy path value đúng nguyên dạng; không tin title/role/assignment trong state là authorization. Inventory yêu cầu #49/#65 sau context #46; các API tự xác thực Bearer/MENTOR và direct ownership. Direct open/refresh không có source đầy đủ cho course hero.
- **Output/exceptions:** Loading state theo từng panel. #49/#65 có thể trả 401/403/404/500; map theo EV-04. Re-auth, denied route, retry và return-to-ME-02 policy cần chốt.

### `ME03-EV-02` — Tải cây nội dung (#49)

- **Trigger/type:** Route load hoặc approved refresh / GET.
- **Request:** `GET /api/v1/mentor/courses/{course_id}/content`, `Authorization: Bearer <JWT>`, không query/body.
- **Processing:** Server guard Mentor → parse signed-int64 → đọc course → direct-owner check → đọc active Content → validate projection/tree. Client chỉ nhận response khi toàn bộ tree hợp lệ.
- **Success:** 200 `DESIGN_RESOURCE_RETRIEVED`; `data: Content[]`; empty array là thành công. Map `id`, `course_id`, `content_type`, `title`, `payload`, `status`, optional `parent_id`, `order` để dựng flat/hierarchical content view theo contract được duyệt.
- **Errors:** 401 auth, 403 owner mismatch, 404 invalid/missing course, 500 DB/tree/mapping. Không render Content cũ như mới nếu request lỗi; stale/cache policy chưa xác định.

### `ME03-EV-03` — Tải tiến độ toàn lớp (#65)

- **Trigger/type:** Route load hoặc approved refresh / GET.
- **Request:** `GET /api/v1/mentor/courses/{course_id}/progress`, Bearer JWT, không query/body.
- **Current output:** Local source trả `data.items[]` với `student{id,full_name,avatar_url?}`, `completed_lessons`, `total_lessons`, `progress_percent`; `data.pagination` mô tả toàn roster trong một page. Catalog trực tiếp còn là `Page<Course>`.
- **Processing:** Server áp dụng direct-owner guard, lấy distinct ACTIVE Student roster và PUBLISHED lesson set, chọn latest progress mỗi Student/lesson, dùng floor-average. Client không tính lại cohort/module progress bằng tên/status mẫu.
- **Errors:** 401/403/404/500. Empty roster thành 200 `items:[]`; zero published lessons cho item có percent 0. Chưa có page/size bounds hoặc partial response theo module.

### `ME03-EV-04` — Ghép loading/ready/no-content/partial/error

- **Trigger/type:** Hai GET hoàn tất hoặc lỗi.
- **Input:** Kết quả #49 và #65; inventory states `loading/no-content/partial/error`.
- **Processing:** Giữ trạng thái dữ liệu riêng theo API. Trường hợp #49 thành công/#65 lỗi hoặc ngược lại là partial candidate theo inventory; exact message, retry button, stale panel, auth/403 isolation và thứ tự call chưa được duyệt. Với 401/403/404, không lấy mockup/sample thay data và không tiếp tục hiển thị phần course nhạy cảm theo một request success nếu hai guard cho kết quả xung đột.
- **Output:** Empty #49 và empty #65 được biểu diễn là successful empty data, không phải server error. Partial rendering policy cần product/security quyết định trước implementation.

### `ME03-EV-05` — Làm mới số liệu (#17)

- **Trigger/type:** Click refresh button.
- **Input:** `courseId`, current #49/#65 results.
- **Processing/output:** Prototype title gợi ý refresh. Đề xuất refetch hai GET read-only; quyết định parallel/sequential, cancel request, stale response ordering, loading indicator, retry/backoff và cache invalidation chưa có nguồn. Button không có handler trong HTML; blocked đến khi UI policy được duyệt.

### `ME03-EV-06` — Xuất Excel (#18)

- **Trigger/type:** Click download icon.
- **Input:** Workspace data.
- **Source/API:** ME-03 inventory không khai báo export API, report schema, file type, permission, operation ID hoặc generated-file URL.
- **Output:** Hiện chỉ là button mẫu; không tạo file hoặc thông báo “đã export”. Cần owner cung cấp contract trước khi enable.

### `ME03-EV-07` — Mở tạo lecture ME-04 (#12)

- **Trigger/type:** Click primary CTA.
- **Input:** `courseId` hiện tại.
- **Processing/output:** Navigation candidate tới `/mentor/courses/:courseId/lectures/new` theo ME-04 inventory. ME-04 tự chạy flow #46/#34/#47 theo contract của screen đó. ME-03 không gửi body hoặc tạo lecture. Server target phải kiểm tra quyền; assigned-course discrepancy còn mở.

### `ME03-EV-08` — Mở cây content ME-06 (#13)

- **Trigger/type:** Click CTA “Cây nội dung & bài học”.
- **Input:** `courseId`.
- **Processing/output:** Route candidate `/mentor/courses/:courseId/content`; ME-06 dùng #49. Inventory link xác nhận. Current app không có router; Content action/CRUD không được thực hiện trên ME-03.

### `ME03-EV-09` — Mở bảng chấm ME-09 (#14)

- **Trigger/type:** Click CTA “Bảng chấm bài”.
- **Input:** Course ID và badge 8 trong mockup.
- **Processing/output:** ME-09 không thuộc ME-03 inventory links. Badge và course-filter handoff chưa có mapping trong screen contract. Cần xác nhận direct route, Course context và permissions; không gán 8 vào #54 total.

### `ME03-EV-10` — Gửi nhắc nhở ME-14 (#15/#35–#37)

- **Trigger/type:** Click reminder button trong risk row.
- **Input:** Student/course/channel/message mẫu.
- **Processing/output:** ME-14 là screen riêng; ME-03 không có recipient selection, notification body, consent/channel, duplicate-send guard hay API orchestration. Nhãn “Gửi nhắc nhở” hiện không có handler. Không gửi notification từ ME-03.

### `ME03-EV-11` — Xếp lịch kèm 1-on-1 (#35–#37)

- **Trigger/type:** Click schedule button.
- **Input:** Student ID/time/mentor calendar candidate, tất cả hiện không có contract.
- **Processing/output:** Không có route, calendar API, time-zone rule hay availability model trong ME-03 inventory. Giữ action blocked; không tạo event hoặc lịch.

### `ME03-EV-12` — Xem danh sách at-risk (#38)

- **Trigger/type:** Click full-list CTA.
- **Input:** Risk count/student criteria sample.
- **Processing/output:** Không có target screen/API/risk threshold. #65 không trả risk flag/streak/quiz score. Cần xác nhận definition, eligibility, route và data source; count 6 không lấy từ API.

### `ME03-EV-13` — Mở rubric ME-09 (#27)

- **Trigger/type:** Click “Mở Rubric ME-09”.
- **Input:** Course/Capstone context sample.
- **Processing/output:** Không có rubric ID, destination parameter, permission hoặc rubric endpoint trong ME-03 contract. Destination cần product/BE xác nhận.

### `ME03-EV-14` — Mở activity feed hoặc một activity row (#31/#32)

- **Trigger/type:** Click activity link/row.
- **Input:** Student/activity IDs và timestamps mẫu.
- **Processing/output:** #65 không phải event feed; #49 là Content tree. Không có page/API đích hoặc exact event row schema. “142” và các timestamps không phải output current.

### `ME03-EV-15` — Mở repository/resource (#45–#47)

- **Trigger/type:** Click resource anchor.
- **Input:** URL/code repository candidate.
- **Current markup:** Anchor `href="#"`; visible domain/name không thành `href`.
- **Output/exceptions:** Không mở external page. Cần approved URL source, allowlist, safe-target/referrer behavior và resource permission trước khi tạo link.

### `ME03-EV-16` — AI Mentor Copilot (#48)

- **Trigger/type:** Callout hiển thị; prototype không có trigger/result handler.
- **Input/output:** Copy nói phát hiện 12 lỗi trong bài Lab 14; không có AI API, source document, confidence, student consent hay navigation.
- **Policy:** Không hiển thị sample như phân tích đã chạy. Tích hợp AI cần contract và review riêng.

### `ME03-EV-17` — Header search / notification (#3/#4)

- **Trigger/type:** Input/change hoặc click notification.
- **Source:** Không có search/unread API trong ME-03 inventory; HTML input không thuộc form và notification badge là tĩnh.
- **Output:** Không submit query/đánh dấu đã đọc. Destination và global-shell owner cần xác định.

### `ME03-EV-18` — Điều hướng toàn cục, breadcrumb và footer (#1/#2/#6/#16/#49–#53)

- **Trigger/type:** Click anchor/link.
- **Expected destinations:** ME-02 back; ME-04, ME-06, ME-16 forward theo `list_screen.md`. Truyền `courseId` cần thiết cho target route.
- **Current markup:** 12 anchors đều `href="#"`; không có browser history/router evidence. Footer legal/partner/contact destinations chưa có route source. Chỉ các handoff inventory xác nhận mới được thiết kế tiếp; wiring runtime chưa có.

### Trích từ DD nguồn: 5. Ma trận trạng thái

| State | Điều kiện | Dữ liệu/UI | Chuyển tiếp/lỗi |
|---|---|---|---|
| `LOADING` | Route context hiện hữu và #49/#65 đang chờ. | Loading theo panel; không dùng KPI mockup thay response. | Mỗi response chuyển state độc lập; chính sách thứ tự và timeout chưa có FE source. |
| `READY` | Hai GET thành công. | #49 trả cây active Content; #65 trả page roster theo local source shape nếu API owner duyệt. | Nút/card unsupported vẫn blocked. |
| `NO_CONTENT` | #49 trả `[]`, #65 trả `items=[]`, hoặc một section rỗng. | Empty response là HTTP 200; phần còn lại có thể có data. | Text/action cho empty state chưa được thiết kế trong source; không coi là error. |
| `PARTIAL` | Một GET success, một GET error. | Inventory yêu cầu state partial. Cách hiển thị/ẩn/safe-deny/retry chưa chốt. | Không suy ra missing panel là zero hoặc dùng sample. |
| `ERROR` | Cả hai call lỗi/network failure hoặc mapping không dùng được. | Show safe error; không lộ SQL/token/PII. | Retry/cancel/backoff/cache policy `SOURCE_REQUIRED`. |
| `UNAUTHENTICATED` | API trả 401. | Không hiển thị course/Student data sau lỗi auth. | Login/refresh/handoff route chưa có Study Web source. |
| `ACCESS_DENIED` | API trả 403. | Hủy nội dung nhạy cảm; server là authority. | UI destination/message và assigned-course handling cần quyết định. |
| `NOT_FOUND` | Invalid/missing course path trả 404. | Không render snapshot cũ như course hiện tại. | Return ME-02 candidate; exact navigation policy chưa chốt. |
| `RUNTIME NOT VERIFIED` | Không có frontend route/deployment/live verification. | Trạng thái kiểm chứng cho toàn screen hiện nay. | Chỉ đổi bằng bằng chứng chạy thực tế, không bằng screenshot hoặc test double. |

## 4. Luồng đọc (Read)
- Orchestration từ inventory: GET #49 và #65 sau khi course thuộc #46; render module theo permissions.
- Chi tiết current/source mapping: xem [API Integration](04-api-integration.md) và DD nguồn.

## 5. Luồng ghi (Write)
- Chỉ mô tả mutation được DD/API source nêu; không thêm endpoint hoặc side effect.
- Source trace: [ME-03](../../screen_stitch/04_mentor/ME-03_workspace-khoa-hoc-cua-mentor/ME-03.md)

## 6. Cache / concurrency / lifecycle
- Cache, race, cleanup, pagination: xem các section source bên dưới; nếu không có bằng chứng thì để `CẦN_XÁC_NHẬN`.

## 7. Data errors & security
- Theo error/security/source-status section của DD nguồn; không coi state trong mockup là runtime behavior.

## 8. Trace
[Events](02-events.md) · [API](04-api-integration.md) · [Rules](05-business-rules.md)

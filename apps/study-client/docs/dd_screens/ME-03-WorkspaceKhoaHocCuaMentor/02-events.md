# ME-03 — Events (đặc tả xử lý)

## 1. Event index
| Event ID trong package | Source Event ID / heading | Chi tiết |
|---|---|---|
| `ME-03-EV-001` | `ME03-EV-01` / `ME03-EV-01` — Vào workspace theo course | See source event detail below |
| `ME-03-EV-002` | `ME03-EV-02` / `ME03-EV-02` — Tải cây nội dung (#49) | See source event detail below |
| `ME-03-EV-003` | `ME03-EV-03` / `ME03-EV-03` — Tải tiến độ toàn lớp (#65) | See source event detail below |
| `ME-03-EV-004` | `ME03-EV-04` / `ME03-EV-04` — Ghép loading/ready/no-content/partial/error | See source event detail below |
| `ME-03-EV-005` | `ME03-EV-05` / `ME03-EV-05` — Làm mới số liệu (#17) | See source event detail below |
| `ME-03-EV-006` | `ME03-EV-06` / `ME03-EV-06` — Xuất Excel (#18) | See source event detail below |
| `ME-03-EV-007` | `ME03-EV-07` / `ME03-EV-07` — Mở tạo lecture ME-04 (#12) | See source event detail below |
| `ME-03-EV-008` | `ME03-EV-08` / `ME03-EV-08` — Mở cây content ME-06 (#13) | See source event detail below |
| `ME-03-EV-009` | `ME03-EV-09` / `ME03-EV-09` — Mở bảng chấm ME-09 (#14) | See source event detail below |
| `ME-03-EV-010` | `ME03-EV-10` / `ME03-EV-10` — Gửi nhắc nhở ME-14 (#15/#35–#37) | See source event detail below |
| `ME-03-EV-011` | `ME03-EV-11` / `ME03-EV-11` — Xếp lịch kèm 1-on-1 (#35–#37) | See source event detail below |
| `ME-03-EV-012` | `ME03-EV-12` / `ME03-EV-12` — Xem danh sách at-risk (#38) | See source event detail below |
| `ME-03-EV-013` | `ME03-EV-13` / `ME03-EV-13` — Mở rubric ME-09 (#27) | See source event detail below |
| `ME-03-EV-014` | `ME03-EV-14` / `ME03-EV-14` — Mở activity feed hoặc một activity row (#31/#32) | See source event detail below |
| `ME-03-EV-015` | `ME03-EV-15` / `ME03-EV-15` — Mở repository/resource (#45–#47) | See source event detail below |
| `ME-03-EV-016` | `ME03-EV-16` / `ME03-EV-16` — AI Mentor Copilot (#48) | See source event detail below |
| `ME-03-EV-017` | `ME03-EV-17` / `ME03-EV-17` — Header search / notification (#3/#4) | See source event detail below |
| `ME-03-EV-018` | `ME03-EV-18` / `ME03-EV-18` — Điều hướng toàn cục, breadcrumb và footer (#1/#2/#6/#16/#49–#53) | See source event detail below |

> Event IDs trong package là alias để theo template; Source Event IDs, steps và API links giữ theo DD nguồn. Alias không chứng minh event runtime.

## 2. Chi tiết event từ DD nguồn

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

## Trace links
- [UI Elements](01-ui-elements.md) · [API Integration](04-api-integration.md) · [Business Rules](05-business-rules.md) · [Navigation](06-navigation.md) · [Test Cases](07-test-cases.md)

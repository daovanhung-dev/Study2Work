# ST-20 — Tổng quan tiến độ · Tổng quan

| Trường | Giá trị |
|---|---|
| Screen ID | `ST-20` |
| Module | Student |
| Route | `/student/progress` — route trong inventory, không phải xác nhận router runtime |
| Actor/role | Theo DD nguồn; xem overview/source trace bên dưới |
| DD status | Draft (package được chuyển đổi); source status: **Trạng thái:** DD BLOCKED; IMPLEMENTATION BLOCKED; RUNTIME NOT VERIFIED. API #21/#38 và route Study Web của Student chưa có runtime source; progress/achievement contracts và thứ tự AC-18 chưa thống nhất. |
| Owner | Không được xác định trong inventory/DD nguồn đã chuyển; `CẦN_XÁC_NHẬN` |
| Version / last updated | 0.1 / 2026-11-08 |
| Nguồn đối chiếu | [ST-20.md](../../screen_stitch/03_student/ST-20_tong-quan-tien-do/ST-20.md), [ST-20_PLAN.md](../../screen_stitch/03_student/ST-20_tong-quan-tien-do/ST-20_PLAN.md), [ST-20_markers.json](../../screen_stitch/03_student/ST-20_tong-quan-tien-do/ST-20_markers.json), [list_screen.md](../../list_screen.md) |

## 1. Mục tiêu & phạm vi
- Mục tiêu: Tổng số bài học, tiến độ theo course và achievements thực tế.
- In-scope: GET #21 và #38 độc lập; render từng widget theo trạng thái API riêng.
- Out-of-scope: Xem gate bên dưới; không kết luận Study Web route/UI đã wired hoặc runtime đã chạy.

## 2. Use cases chính
| Use case / AC | Actor | Kết quả kỳ vọng theo inventory |
|---|---|---|
| AC-18 | Theo DD nguồn; `CẦN_XÁC_NHẬN` nếu nguồn chưa chốt | Tổng số bài học, tiến độ theo course và achievements thực tế. |

## 3. Precondition / Entry / Dependencies
- Điều kiện vào, role guard và dependency: xem trích đoạn tổng quan nguồn; không bổ sung giả định.
- API references: #21, #38
- Liên kết màn hình dự kiến: [ST-21](../ST-21-TienDoTheoKhoaHoc/00-overview.md), [ST-22](../ST-22-ThanhTichVaChungNhan/00-overview.md)
- Links: [UI](01-ui-elements.md) · [Events](02-events.md) · [Navigation](06-navigation.md)

## 4. UI states
| State | Nguồn | Giá trị |
|---|---|---|
| Inventory states | `list_screen.md` | loading/partial/empty/error |
| Current runtime | Worklog/context Study Web | `UNWIRED` / `RUNTIME NOT VERIFIED` |

## 5. Luồng chính và hình ảnh
- Ảnh clean: [screen-clean.png](images/screen-clean.png) (copy từ [ST-20 source screen.png](../../screen_stitch/03_student/ST-20_tong-quan-tien-do/screen.png))
- Ảnh numbered: [screen-numbered.png](images/screen-numbered.png) (copy từ [source annotated PNG](../../screen_stitch/03_student/ST-20_tong-quan-tien-do/screen_annotated.png))
- Luồng: GET #21 và #38 độc lập; render từng widget theo trạng thái API riêng.
- Priority: P2; Gate/source status: **D; DD BLOCKED; IMPLEMENTATION BLOCKED; RUNTIME NOT VERIFIED:** #21 catalog trả `UserProfile` nhưng query, progress DTO, aggregate/merge/empty semantics chưa chốt; #38 award policy/source, course filter, pagination/order/empty semantics chưa chốt; inventory độc lập #21/#38 mâu thuẫn AC-18 tuần tự #21→#37→#38; Student routes/modules/queries/tests #21/#38 NOT_FOUND; Study Web UNWIRED; PNG gốc trống phần body, HTML chỉ có static empty state; loaded dashboard chưa có nguồn thiết kế xác nhận; HTML prototype tải remote Tailwind/Plus Jakarta Sans, dùng 1440px và trộn primary token lệch Study Web guide

## 6. Open questions / Change log
- `CẦN_XÁC_NHẬN`: các gate/source questions trong inventory và DD nguồn vẫn giữ nguyên; không tự đóng blocker.
- 2026-11-08 — Chuyển nội dung nguồn sang 8-file template; không chỉnh source, không xác minh runtime.

## Trạng thái và ranh giới bằng chứng

# ST-20 — Tổng quan tiến độ

> **Trạng thái:** DD BLOCKED; IMPLEMENTATION BLOCKED; RUNTIME NOT VERIFIED. API #21/#38 và route Study Web của Student chưa có runtime source; progress/achievement contracts và thứ tự AC-18 chưa thống nhất.

## Trích đoạn tổng quan từ DD nguồn

### Trích từ DD nguồn: A. Tổng quan màn hình

### A.1. Định danh

| Thuộc tính | Đặc tả |
|---|---|
| Screen ID / tên | ST-20 — Tổng quan tiến độ (Page) |
| Mục tiêu | Cho Student xem tổng số bài học, tiến độ từng khóa và các achievement đã được hệ thống xác nhận. |
| Actor | Student đã xác thực theo inventory và API design; route guard hiện chưa có trong Study Web source. |
| Route thiết kế | `/student/progress` — route đề xuất trong inventory, chưa có router/runtime hiện hành. |
| API dự kiến | GET API #21 `/api/v1/users/me/progress`; GET API #38 `/api/v1/users/me/achievements`. |
| Màn hình liên quan | ST-01 dashboard, ST-08 Khóa học của tôi, ST-19 Bài đã nộp và phản hồi; đi tới ST-21 Tiến độ theo khóa học và ST-22 Thành tích và chứng nhận. CTA empty state HTML trỏ tới ST-08. |
| Elements / events | 16 marker groups `ST20-EL-01…ST20-EL-16`; 11 events `ST20-EV-01…ST20-EV-11`. |
| Trạng thái | DD BLOCKED; IMPLEMENTATION BLOCKED; RUNTIME NOT VERIFIED. |

### A.2. Điều kiện vào, dữ liệu và rời màn hình

- Inventory đặt route `/student/progress`, actor Student, AC-18, API #21/#38, tổng số bài học, tiến độ theo course và achievements thực tế; yêu cầu gọi #21/#38 độc lập, render widget theo trạng thái API riêng; links tới ST-21/ST-22; states `loading/partial/empty/error`.
- API catalog #21 khai báo `GET /api/v1/users/me/progress`, Student Bearer JWT, query ghi nguyên văn `course_id list hoặc aggregate?:string`, response `ApiEnvelope<UserProfile>`, HTTP 200 `DESIGN_RESOURCE_RETRIEVED`, 401 `DESIGN_AUTHENTICATION_REQUIRED`, 403 `DESIGN_ACCESS_DENIED`, 500 `DESIGN_INTERNAL_ERROR`. `UserProfile` không định nghĩa các số liệu tiến độ cần cho màn hình. DD API #21 là Draft/Needs Confirmation.
- API catalog #38 khai báo `GET /api/v1/users/me/achievements`, Student Bearer JWT, `course_id:int64` optional, response `ApiEnvelope<Page<Achievement>>`, cùng success 200 và errors 401/403/500 ở trên. Request không khai báo pagination/sort dù response là Page. DD API #38 là Draft/Needs Confirmation.
- Candidate logical Achievement fields gồm `id`, `code`, `title`, `awarded_at`, `course_id?`; đây chưa phải rule cấp thành tích. Chưa có award registry/rule/source table được xác nhận. Không tự dựng achievement được cấp/chưa cấp hoặc chứng nhận.
- `screen.png` (1280×1123) là ảnh nguyên trạng: header, footer và dải nội dung chính trống; không có page title, biểu đồ, danh sách tiến độ hoặc achievement. Hash gốc: `a308a1e1739b155f20abbb6d9269f132a0125997cf06a4f08caf15818559a135`.
- `code.html` là prototype tĩnh với breadcrumb, tiêu đề/mô tả, card empty state “Chưa có dữ liệu tiến độ để hiển thị.” và link `/student/courses`; có script Tailwind CDN/config nhưng không có script nghiệp vụ/API, form handler, auth guard hoặc route handler. Hash gốc: `0d1cf1f32505c59a712956ff1a11b28355755d0d410658fb9621d2c8f02b5e3e`.
- `screen_rendered.png` được render từ HTML tĩnh bằng Chrome headless, 1280×1079, SHA256 `00b273505d7982eb92477d076d5e60b923d30209e4510d504cc55785b1c688ea`; không phải application/API runtime. `screen_annotated.png` dùng render này làm nền để marker trỏ được tới thành phần body mà PNG gốc không chứa. `screen.png` và `code.html` được giữ nguyên. Empty state HTML không chứng minh shape/điều kiện dữ liệu rỗng của API.
- Current Study Web không có editable app source/package/router/Student route; API Student #21/#38 không có route/module/query/test trong current Study Server source. Mentor progress APIs #65/#67 khác actor/path, không thay thế #21/#37. DB guide đánh dấu #21/#37 query `DESIGN_ONLY`; DDL candidate có `lesson_progress` nhưng không có achievements table và không chứng minh live schema.
- AC-18 diagram mô tả chuỗi #21 → tổng hợp → chọn course → #37 detail → tổng hợp lesson/quiz/assignment → #38 achievements → render. Inventory lại yêu cầu #21/#38 độc lập và đặt #37 tại ST-21. Đây là **DISCREPANCY**; DD giữ nguyên cả hai bằng chứng, không tự quyết định orchestration.

### A.3. Expected behavior và current behavior

**Expected behavior:** Student được xác thực mở trang; tiến độ (#21) và achievement (#38) được lấy theo contract đã duyệt, hiển thị độc lập theo widget. Student chọn một khóa để tới ST-21 hoặc mở danh sách achievement ST-22. Tổng bài học, phần trăm, danh sách khóa và award chỉ được hiển thị nếu response/rule nguồn định nghĩa rõ.

**Current behavior:** Không có Study Web route để mở ST-20 và không có Student API #21/#38 runtime route/module/query/test. PNG gốc không có body; HTML chỉ có static no-data fallback. Không có hành vi tải, tính toán, render widget hoặc điều hướng nào được xác minh runtime.

**Visual design target / prototype discrepancy:** `.agents/web-study/design.md` đặt intended target dùng semantic `ocean-primary=#0B5F8A`, Inter/system sans-serif, content width khoảng 1120px và không thêm remote font/CDN. Prototype `code.html` tải Tailwind từ CDN và Google Font Plus Jakarta Sans, dùng `max-w-[1440px]`, đồng thời có `primary=#004AC6` trong config nhưng hardcode `#0B5F8A` ở một số control. Giữ đây là sai khác giữa design asset hiện có và intended target; không xem ảnh render là xác nhận thiết kế loaded-state hoặc runtime.

### A.4. API contract và trạng thái source

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

### A.5. Quy tắc nghiệp vụ và bảo mật

- Chỉ backend được xác nhận có thể quyết định user progress/award; client không tự tính lesson completion hoặc cấp achievement/chứng nhận.
- Không truyền user ID để lấy `/me`; không coi role ở giao diện là thay cho authorization tại API.
- Không lấy dữ liệu Mentor #65/#67 để thay cho Student #21/#37.
- Không suy ra `completed lessons / total lessons`, mẫu số, phần trăm, rounding, course merge key, phạm vi khóa, thời gian cập nhật hoặc trạng thái chưa ghi nhận từ candidate `lesson_progress`.
- Chưa chốt phân biệt không ghi danh, chưa có progress, progress rỗng, dữ liệu đang đồng bộ và lỗi một widget. Không gán các trạng thái đó về cùng empty state.
- Không tạo award ID/code/title/time, locked badge, cấp chứng chỉ hoặc loại achievement từ hình minh họa/tài liệu UI.
- Không áp đặt HTTP 404/422, query parsing response, fallback auth navigation, retry hoặc cache invalidation ngoài catalog.

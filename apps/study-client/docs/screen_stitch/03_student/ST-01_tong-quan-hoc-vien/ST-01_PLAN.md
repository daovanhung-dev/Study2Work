# ST-01 — Kế hoạch Detailed Design

- **Screen ID:** ST-01
- **Tên:** Tổng quan học viên (Page)
- **Route trong inventory:** `/student` (đề xuất; Study Web chưa có route source)
- **Actor:** Student
- **Kế hoạch:** PLAN FIRST — hoàn thành source/contract trace và kế hoạch này trước marker JSON, ảnh chú thích hoặc DD.
- **Trạng thái dự kiến:** DD BLOCKED; IMPLEMENTATION BLOCKED; RUNTIME NOT VERIFIED.

## 1. Mục tiêu và phạm vi

- Đặc tả riêng dashboard Student ST-01 theo inventory, ảnh và HTML hiện có.
- Giữ nguyên `screen.png` và `code.html`; dùng PNG gốc 1067×1600 làm nguồn đánh dấu vì ảnh hợp lệ, đầy đủ và biểu thị đúng layout hand-off đang có.
- Tạo marker theo thứ tự đọc cho toàn bộ component/nhóm component hiển thị. Mỗi marker có một element row trong DD và một entry trong marker JSON; giữ SVG overlay làm nguồn chú thích tái dựng được.
- Ghi riêng thiết kế dự kiến, trạng thái hiện hành của prototype, contract Draft và source runtime. Bốn widget/API được mô tả độc lập; không giả lập dữ liệu hay kết quả.
- Không sửa URL/API/business behavior. Các URL sai trong endpoint matrix của prototype chỉ là discrepancy, không phải contract.

## 2. Source và trạng thái hiện hành cần giữ

- `screen.png`: 1067×1600; SHA-256 `8ac0708a12c0221ef529b26c3fc601d46405003476225fdc492475df8ed6b9cd`.
- `code.html`: 24,459 bytes; SHA-256 `f9870e9e6ec797ee96f340d663efaa9904ae1c5b5f3300be140575c50244770f`.
- HTML là static hand-off với status gate, zero-synthetic-data copy, bốn widget trạng thái DESIGN_ONLY và Developer Hand-off Matrix. Có Tailwind CDN/config cùng ba Google Fonts imports; 13 anchor đều `href="#"`; không có fetch/XHR, form/input/button, app event handler hoặc API data binding.
- Endpoint matrix trong HTML ghi `/api/v1/courses/enrolled`, `/api/v1/students/progress`, `/api/v1/achievements`, `/api/v1/notifications/latest`; catalog tương ứng là `/api/v1/users/me/courses`, `/api/v1/users/me/progress`, `/api/v1/users/me/achievements`, `/api/v1/users/me/notifications`.
- Study Web hiện không có editable app source/package/router. Không coi screenshot, HTML hoặc ignored `dist` là route/runtime evidence.

## 3. Expected behavior — inventory và activity contracts

- Inventory ST-01: Student overview tại route đề xuất `/student`; AC-13, AC-18, AC-20; APIs #20/#21/#38/#43; hiển thị khóa học, tiến độ, thành tích và thông báo; widget độc lập; #20/#21 khi khởi tạo, #38/#43 lazy hoặc parallel theo inventory; liên kết ST-08, ST-20, ST-26, ST-02; state labels `partial-widget/empty/loading/403`.
- AC-13: Student đã đăng nhập; gọi #20 để lấy course/enrollment rồi #21 lấy progress, ghép ở client. Diagram có `EMPTY` và `HAS DATA` edge cùng đi tới “Hiển thị khóa học + % hoàn thành”; không tự chọn nhánh sửa.
- AC-18: Student đã đăng nhập; #21 aggregate → chọn course → #37 progress chi tiết → #38 achievements → render. Đây là chuỗi khác với yêu cầu inventory ST-01 gọi các widget #21/#38 độc lập. Ghi `DISCREPANCY`; không suy timing hoặc đổi flow.
- AC-20: #43 đọc notification list; quyết định read-one/read-all và #44/#45 nằm trong activity của notification center, không phải thao tác ST-01. ST-01 chỉ có handoff sang ST-26 theo inventory.
- Mockup giới hạn màn hình ở trạng thái không có dữ liệu: không tạo course, progress, award hoặc notification mẫu. Tên “Nguyễn Văn A”, nhãn WCAG 2.1 AA và status copy là nội dung static, không phải response/identity/audit claim đã xác minh.

## 4. Contract/source trace và blockers

| API | Catalog request/response | Current source | Mở/blocker cần giữ |
|---|---|---|---|
| #20 | `GET /api/v1/users/me/courses`; Student Bearer; `status?:string`, `page?:int32`; `ApiEnvelope<UserProfile>`; 200/401/403/422/500. | Không có route/module/query/test. | AC-13 cần Enrollment/Course list; response hiện là UserProfile. Status target, enum, pagination, empty wire shape và JWT→Enrollment ownership đều mở. |
| #21 | `GET /api/v1/users/me/progress`; Student Bearer; query ghi `course_id list hoặc aggregate?:string`; `ApiEnvelope<UserProfile>`; 200/401/403/500. | Không có route/module/query/test. | Selector grammar, aggregate source/formula, response schema/merge key, identity và no-enrollment/no-progress shape đều mở. |
| #38 | `GET /api/v1/users/me/achievements`; Student Bearer; `course_id?:int64`; `ApiEnvelope<Page<Achievement>>`; 200/401/403/500. | Không có route/module/query/test. | Award criteria/projection, filter/access, page/order/empty và query validation mở; Achievement không xác nhận certificate/proof/metric fields trong mockup. |
| #43 | `GET /api/v1/users/me/notifications`; Student Bearer; `unread_only?:boolean`, `page?:int32`; `ApiEnvelope<Page<Notification>>`; 200/401/403/500. | Không có route/module/query/test. | Recipient, `channels`/`status`, read timestamps, page/order/timezone và error-envelope mapping mở; “latest” chưa có order contract. |

API DD #20/#21/#38/#43 đều `Draft — Needs Confirmation`. API indexes catalog chúng là design-only; catalog và DD không chứng minh API đã chạy. API #43's endpoint body/Notification design has source gaps; các module Notification khác không phải API #43.

## 5. Marker và coverage plan

Đánh số theo thứ tự đọc từ trên xuống, trái sang phải. Dự kiến 37 marker, bao phủ header, gate/breadcrumb, page heading, bốn widget, developer matrix, checklist, navigation note và footer. Badge đặt trong side gutter; footer badges đặt ở bottom gutter của annotated canvas. Leader target thuộc đúng vùng component và không che nội dung chính. Nhóm nhiều item chỉ khi chúng cùng một component, trạng thái và nguồn dữ liệu.

1. Logo/brand.
2. Primary navigation group (Trang chủ, Khóa học của tôi, Tiến độ, Thảo luận, Thông báo).
3. Static learner name/role/avatar.
4. Specification gate / zero-synthetic-data banner.
5. Breadcrumb.
6. Screen ID và DESIGN_ONLY tags.
7. Page title và introduction.
8. Gate status card.
9–11. Course widget header, empty/gated panel, ST-08 CTA.
12–14. Progress widget header, no-data panel, ST-20 CTA.
15–16. Achievement widget header và gated/no-certificate panel.
17–19. Notification widget header, gateway-blocked panel, ST-26 CTA.
20–26. Developer hand-off heading/copy, API list heading, API #20/#21/#38/#43 rows.
27–31. Accessibility/design checklist heading và bốn criteria rows.
32. Safe navigation note.
33–34. Footer copyright và WCAG badge.
35–37. Terms, privacy, support links.

## 6. Event plan

Mỗi event trong DD sẽ ghi trigger/type, element hoặc page/response lifecycle, precondition, input, xử lý, output và ngoại lệ. Các action chỉ tồn tại trong ảnh/HTML là design-only; không giả vờ click/route/API hiện hoạt.

1. Page entry và Student session guard.
2. Nạp widget khóa học bằng #20, nếu API contract và route được chốt.
3. Nạp #21 và merge course/progress theo AC-13 chỉ sau khi response, key, formula, empty branch và orchestration được thống nhất.
4. Nạp achievements qua #38; chỉ render backend-confirmed records khi projection và award rules được chốt.
5. Nạp notification page qua #43; không khẳng định `latest` khi ordering chưa có contract.
6. Course CTA → ST-08 theo route inventory, không truyền filter/ID chưa được phê duyệt.
7. Progress CTA → ST-20 theo route inventory, không tự chuyển dữ liệu progress.
8. Notification CTA → ST-26 theo route inventory; mark-read actions thuộc ST-26/AC-20, không chạy ở ST-01.
9. Header/breadcrumb/footer navigation: chỉ ghi destination được inventory hoặc route map xác nhận; `href="#"` hiện tại không phải route.
10. Partial-widget, empty, auth/access, API/transport failure: tách từng widget; recovery/retry không xác định thay cho behavior chưa có contract.

## 7. State, security, design alignment

- Inventory labels `loading`, `empty`, `partial-widget`, `403` được ghi là expected. Static HTML có trạng thái gated/unavailable; không có runtime transition. `earned`, loaded course data và notification cards chưa được thiết kế/contract đầy đủ.
- Không gửi `user_id`; `/me` actor phải gắn với Student session theo contract backend. Shared Study `/users/me` hiện Student-only nhưng không chứng minh guard của các API #20/#21/#38/#43 khi chúng chưa có source.
- Không chuyển API error thành empty. Không gán lỗi ngoài status catalog từng API; giữ distinct 401/403 và status 422 chỉ cho #20 theo catalog.
- Study Web guide yêu cầu semantic ocean tokens, system/Inter font không tải remote, content width khoảng 1120px và accessibility/focus/reflow. Prototype dùng Plus Jakarta Sans/Material Symbols từ Google Fonts, Tailwind CDN, `max-w-[1440px]`, cobalt `#004AC6`/`#2563EB` và claims WCAG chưa được kiểm chứng. Ghi discrepancy, không sửa asset nguồn.

## 8. No-invention rules

- Không thêm schema/course/progress fields, progress formulas, widget ordering, cache/retry, paging defaults, achievement criteria, unread semantics, notification sorting, route params hoặc error codes.
- Không dùng các endpoint sai trong HTML làm API contract; không biến API #44/#45 thành thao tác ở ST-01.
- Không coi static text, lock icon, status badge hoặc sample identity là runtime response, authorization, signature/proof hoặc WCAG audit.
- Giữ `DD BLOCKED`, `IMPLEMENTATION BLOCKED`, `RUNTIME NOT VERIFIED` nếu contract/source vẫn thiếu; không nâng readiness chỉ vì ảnh và DD đủ marker.

## 9. Verification plan

- Kiểm tra source hashes/dimensions giữ nguyên; visual inspect ảnh gốc và ảnh chú thích.
- Kiểm tra JSON/SVG parse, marker #1–#37 liên tục/duy nhất/in-bounds, 37 IDs ↔ 37 DD rows, không che nội dung, SVG labels và connector geometry tương ứng.
- Kiểm tra DD A–F, 10 event sections đầy đủ trường, API catalog/errors, AC discrepancies, local links, global inventory/status/pointers, 83 folder count/core-bundle count.
- Chạy `git diff --check` trên tracked files và trailing-whitespace scan trên authored files. Không chạy application tests, app runtime hay live DB query trong docs task.

## 10. Sources

- [Screen inventory](../../../list_screen.md)
- [Source screenshot](./screen.png), [static HTML companion](./code.html)
- [API catalog](../../../../../../docs/lists/list_api.md)
- [API #20](../../../../../../apps/study-server/docs/dd/20_users_me_courses/02_Overview.md), [API #21](../../../../../../apps/study-server/docs/dd/21_users_me_progress/02_Overview.md), [API #38](../../../../../../apps/study-server/docs/dd/38_users_me_achievements/02_Overview.md), [API #43](../../../../../../apps/study-server/docs/dd/43_users_me_notifications/02_Overview.md)
- [AC/API index](../../../../../../apps/study-server/docs/diagrams/AC_UNICA/00_AC_API_INDEX.md), [Student learning activity diagram](../../../../../../apps/study-server/docs/diagrams/AC_UNICA/AC_02_STUDENT_LEARNING.drawio)
- [Study Web design target](../../../../../../.agents/web-study/design.md), [Study route inventory](../../../../../../.agents/server-study/apis/declared-routes.md)

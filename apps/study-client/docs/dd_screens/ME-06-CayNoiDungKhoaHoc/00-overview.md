# ME-06 — Cây nội dung khóa học · Tổng quan

| Trường | Giá trị |
|---|---|
| Screen ID | `ME-06` |
| Module | Mentor |
| Route | `/mentor/courses/:courseId/content` — route trong inventory, không phải xác nhận router runtime |
| Actor/role | Theo DD nguồn; xem overview/source trace bên dưới |
| DD status | Draft (package được chuyển đổi); source status: **Trạng thái DD:** `DD BLOCKED` — tài liệu đã ghi rõ current behavior và các quyết định còn mở; chưa đủ căn cứ chốt toàn bộ loại node, schema payload và hành vi chỉnh sửa cây.; **Trạng thái triển khai:** `IMPLEMENTATION BLOCKED` — Study Web chưa được wire; một số thao tác mockup không có API tương ứng hoặc không tương thích với API source hiện tại.; **Trạng thái runtime:** `RUNTIME NOT VERIFIED` — chưa có Study Web runtime/live DB evidence trong checkout. |
| Owner | Không được xác định trong inventory/DD nguồn đã chuyển; `CẦN_XÁC_NHẬN` |
| Version / last updated | 0.1 / 2026-11-08 |
| Nguồn đối chiếu | [ME-06.md](../../screen_stitch/04_mentor/ME-06_cay-noi-dung-khoa-hoc/ME-06.md), [ME-06_PLAN.md](../../screen_stitch/04_mentor/ME-06_cay-noi-dung-khoa-hoc/ME-06_PLAN.md), [ME-06_markers.json](../../screen_stitch/04_mentor/ME-06_cay-noi-dung-khoa-hoc/ME-06_markers.json), [list_screen.md](../../list_screen.md) |

## 1. Mục tiêu & phạm vi
- Mục tiêu: Tree sections/contents và thứ tự; mở editor/publish/delete khi được phép.
- In-scope: GET #49; preserve ids/version, tránh render draft như published.
- Out-of-scope: Xem gate bên dưới; không kết luận Study Web route/UI đã wired hoặc runtime đã chạy.

## 2. Use cases chính
| Use case / AC | Actor | Kết quả kỳ vọng theo inventory |
|---|---|---|
| AC-22 | Theo DD nguồn; `CẦN_XÁC_NHẬN` nếu nguồn chưa chốt | Tree sections/contents và thứ tự; mở editor/publish/delete khi được phép. |

## 3. Precondition / Entry / Dependencies
- Điều kiện vào, role guard và dependency: xem trích đoạn tổng quan nguồn; không bổ sung giả định.
- API references: #49
- Liên kết màn hình dự kiến: [ME-07](../ME-07-TaoChinhSuaNoiDung/00-overview.md), [ME-08](../ME-08-XuatBanXoaNoiDung/00-overview.md)
- Links: [UI](01-ui-elements.md) · [Events](02-events.md) · [Navigation](06-navigation.md)

## 4. UI states
| State | Nguồn | Giá trị |
|---|---|---|
| Inventory states | `list_screen.md` | loading/empty/ready/error |
| Current runtime | Worklog/context Study Web | `UNWIRED` / `RUNTIME NOT VERIFIED` |

## 5. Luồng chính và hình ảnh
- Ảnh clean: [screen-clean.png](images/screen-clean.png) (copy từ [ME-06 source screen.png](../../screen_stitch/04_mentor/ME-06_cay-noi-dung-khoa-hoc/screen.png))
- Ảnh numbered: [screen-numbered.png](images/screen-numbered.png) (copy từ [source annotated PNG](../../screen_stitch/04_mentor/ME-06_cay-noi-dung-khoa-hoc/screen_annotated.png))
- Luồng: GET #49; preserve ids/version, tránh render draft như published.
- Priority: P1; Gate/source status: **D**; **BLOCK:** Content không nằm trong 18 bảng DB.sql

## 6. Open questions / Change log
- `CẦN_XÁC_NHẬN`: các gate/source questions trong inventory và DD nguồn vẫn giữ nguyên; không tự đóng blocker.
- 2026-11-08 — Chuyển nội dung nguồn sang 8-file template; không chỉnh source, không xác minh runtime.

## Trạng thái và ranh giới bằng chứng

# ME-06 — Cây nội dung khóa học

> **Trạng thái DD:** `DD BLOCKED` — tài liệu đã ghi rõ current behavior và các quyết định còn mở; chưa đủ căn cứ chốt toàn bộ loại node, schema payload và hành vi chỉnh sửa cây.
> **Trạng thái triển khai:** `IMPLEMENTATION BLOCKED` — Study Web chưa được wire; một số thao tác mockup không có API tương ứng hoặc không tương thích với API source hiện tại.
> **Trạng thái runtime:** `RUNTIME NOT VERIFIED` — chưa có Study Web runtime/live DB evidence trong checkout.

## Trích đoạn tổng quan từ DD nguồn

### Trích từ DD nguồn: 1. Tổng quan

| Thuộc tính | Đặc tả |
|---|---|
| Screen ID / tên | ME-06 — Cây nội dung khóa học |
| Mục tiêu | Cho Mentor xem cấu trúc nội dung của một course, giữ liên kết node và trạng thái do server trả về, rồi mở các flow tạo/chỉnh sửa hoặc publish/xóa đã được duyệt. |
| Actor | Mentor đã xác thực. API #49 yêu cầu Bearer JWT role `MENTOR` và current source kiểm tra direct owner của course. |
| Route đề xuất | `/mentor/courses/:courseId/content`; đây là route trong inventory, chưa có Study Web router/runtime để xác nhận. `courseId` API là signed int64. |
| API đọc | `GET /api/v1/mentor/courses/{course_id}/content` — API #49; không query/body. |
| API thao tác liên quan | #50 create, #51 update → ME-07; #52 publish/unpublish, #53 delete → ME-08. Đây là handoff, không phải mọi thao tác đã sẵn sàng trên ME-06. |
| Screen links | ME-07 ([editor mockup](../../screen_stitch/04_mentor/ME-07_tao-chinh-sua-noi-dung/code.html)), ME-08 ([action mockup](../../screen_stitch/04_mentor/ME-08_xuat-ban-xoa-noi-dung/code.html)) theo inventory; mockup còn ghi Xem ME-05 ([detail DD](../../screen_stitch/04_mentor/ME-05_xem-bai-giang-mentor/ME-05.md)) và Thêm bài học ME-04 ([mockup](../../screen_stitch/04_mentor/ME-04_tai-len-va-tao-bai-giang/code.html)). |
| Trạng thái theo inventory | `loading/empty/ready/error`; thêm `denied/not-found` để phản ánh response #49 hiện tại. |
| Tài liệu kế hoạch | [ME-06_PLAN.md](../../screen_stitch/04_mentor/ME-06_cay-noi-dung-khoa-hoc/ME-06_PLAN.md). |
| Ảnh đánh dấu | [screen_annotated.png](../../screen_stitch/04_mentor/ME-06_cay-noi-dung-khoa-hoc/screen_annotated.png); JSON chuẩn [ME-06_markers.json](../../screen_stitch/04_mentor/ME-06_cay-noi-dung-khoa-hoc/ME-06_markers.json); lớp SVG [ME-06_markers_overlay.svg](../../screen_stitch/04_mentor/ME-06_cay-noi-dung-khoa-hoc/ME-06_markers_overlay.svg). |

### Expected behavior

`list_screen.md` yêu cầu GET #49 để hiển thị tree sections/contents theo thứ tự; phải giữ ID/version, không thể hiện draft như published; các thao tác mở editor/publish/delete chỉ bật khi được phép. Success rỗng là empty state; trạng thái tải/lỗi là riêng. Flow liên quan được nêu ở [F08](../../list_screen.md#L61) và dòng [ME-06](../../list_screen.md#L166).

### Current behavior — client/source

- Ảnh nguồn là mockup desktop populated: course summary, 4 KPI cards, tab lọc/search/expand-collapse, cây gồm chapter/lesson/lab/quiz/draft, distribution, LMS quality rules, audit timeline và footer.
- `code.html` là HTML tĩnh. Có 33 button, 10 anchor và 2 input; không có form, `fetch`, XHR hay binding tới API. Các anchor điều hướng đều `href="#"`.
- JavaScript chỉ thao tác DOM local: accordion, expand/collapse, filter row theo `data-status`, search theo `innerText`, và toast. Filter và search đặt `display` độc lập nên một thao tác có thể ghi đè kết quả của thao tác kia. Nút save order chỉ hiện toast có nhắc `API #52 PUT /mentor/courses/reorder`; không gửi request. Nút publish đổi chữ và `data-status` trên row hiện tại, không gọi server.
- Study Web trong context hiện tại là `UNWIRED`; không có app source/router trong checkout để xác nhận route, auth client, cache hay runtime behavior. Hash của `screen.png` và `code.html` được ghi trong plan/worklog; hai file nguồn không bị sửa.

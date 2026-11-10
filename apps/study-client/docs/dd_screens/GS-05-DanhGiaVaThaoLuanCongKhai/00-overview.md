# GS-05 — Đánh giá và thảo luận công khai · Tổng quan

| Trường | Giá trị |
|---|---|
| Screen ID | `GS-05` |
| Module | Guest / Discovery |
| Route | `/courses/:courseId?tab=reviews` — route trong inventory, không phải xác nhận router runtime |
| Actor/role | Theo DD nguồn; xem overview/source trace bên dưới |
| DD status | Draft (package được chuyển đổi); source status: **DD status:** `DD BLOCKED` — API #10 has no executable source; review title, rating/aggregate and public-visibility contract remain unresolved.; **Implementation status:** `IMPLEMENTATION BLOCKED` — Study Web is unwired and loaded/error/pagination UI has no approved design.; **Runtime status:** `RUNTIME NOT VERIFIED` — HTML render is a static asset preview, not an application runtime. |
| Owner | Không được xác định trong inventory/DD nguồn đã chuyển; `CẦN_XÁC_NHẬN` |
| Version / last updated | 0.1 / 2026-11-08 |
| Nguồn đối chiếu | [GS-05.md](../../screen_stitch/02_guest_discovery/GS-05_danh-gia-va-thao-luan-cong-khai/GS-05.md), [GS-05_PLAN.md](../../screen_stitch/02_guest_discovery/GS-05_danh-gia-va-thao-luan-cong-khai/GS-05_PLAN.md), [GS-05_markers.json](../../screen_stitch/02_guest_discovery/GS-05_danh-gia-va-thao-luan-cong-khai/GS-05_markers.json), [list_screen.md](../../list_screen.md) |

## 1. Mục tiêu & phạm vi
- Mục tiêu: Danh sách review/reply; không hiển thị sao trung bình khi không có rating contract.
- In-scope: Tái dùng #8 → GET #10 phân trang; 404 course riêng với empty reviews.
- Out-of-scope: Xem gate bên dưới; không kết luận Study Web route/UI đã wired hoặc runtime đã chạy.

## 2. Use cases chính
| Use case / AC | Actor | Kết quả kỳ vọng theo inventory |
|---|---|---|
| AC-05 | Theo DD nguồn; `CẦN_XÁC_NHẬN` nếu nguồn chưa chốt | Danh sách review/reply; không hiển thị sao trung bình khi không có rating contract. |

## 3. Precondition / Entry / Dependencies
- Điều kiện vào, role guard và dependency: xem trích đoạn tổng quan nguồn; không bổ sung giả định.
- API references: #08, #10
- Liên kết màn hình dự kiến: [GS-03](../GS-03-ChiTietKhoaHoc/00-overview.md)
- Links: [UI](01-ui-elements.md) · [Events](02-events.md) · [Navigation](06-navigation.md)

## 4. UI states
| State | Nguồn | Giá trị |
|---|---|---|
| Inventory states | `list_screen.md` | loading/empty/ready/error |
| Current runtime | Worklog/context Study Web | `UNWIRED` / `RUNTIME NOT VERIFIED` |

## 5. Luồng chính và hình ảnh
- Ảnh clean: [screen-clean.png](images/screen-clean.png) (copy từ [GS-05 source screen.png](../../screen_stitch/02_guest_discovery/GS-05_danh-gia-va-thao-luan-cong-khai/screen.png))
- Ảnh numbered: [screen-numbered.png](images/screen-numbered.png) (copy từ [source annotated PNG](../../screen_stitch/02_guest_discovery/GS-05_danh-gia-va-thao-luan-cong-khai/screen_annotated.png))
- Luồng: Tái dùng #8 → GET #10 phân trang; 404 course riêng với empty reviews.
- Priority: P2; Gate/source status: **D (#10 declared; no current route/module/test)**; **BLOCK:** #08 catalog `course_id:int64` lệch route `str`/parser không giới hạn signed int64; API #10 Draft yêu cầu `Discussion.title` nhưng không có source; không có course-rating/aggregate source, literal rating-filter key/semantics hoặc public root/reply visibility approval; legacy `discussions` thiếu title/rating và V1-PILOT assessment reviews là model khác; AC-05 aggregate/eager #08→#09→#10 lệch F02 lazy tab, inventory yêu cầu #08 cache reuse; loaded review/reply/page/loading/error UI thiếu; live schema và Study Web UNWIRED

## 6. Open questions / Change log
- `CẦN_XÁC_NHẬN`: các gate/source questions trong inventory và DD nguồn vẫn giữ nguyên; không tự đóng blocker.
- 2026-11-08 — Chuyển nội dung nguồn sang 8-file template; không chỉnh source, không xác minh runtime.

## Trạng thái và ranh giới bằng chứng

# GS-05 — Đánh giá và thảo luận công khai

> **DD status:** `DD BLOCKED` — API #10 has no executable source; review title, rating/aggregate and public-visibility contract remain unresolved.
> **Implementation status:** `IMPLEMENTATION BLOCKED` — Study Web is unwired and loaded/error/pagination UI has no approved design.
> **Runtime status:** `RUNTIME NOT VERIFIED` — HTML render is a static asset preview, not an application runtime.
> **Phạm vi phiên:** chỉ GS-05; chưa xử lý GS-06.

## Trích đoạn tổng quan từ DD nguồn

### Trích từ DD nguồn: A. Tổng quan màn hình

| Thuộc tính | Đặc tả |
|---|---|
| Screen ID / tên | GS-05 — Đánh giá và thảo luận công khai (tab) |
| Mục tiêu expected | Guest đọc review và reply công khai của một khóa học. Inventory yêu cầu phân trang, tách lỗi khóa học 404 khỏi reviews rỗng, và không hiển thị sao trung bình khi chưa có rating contract. |
| Actor | `Guest`; API catalog và API #10 Draft DD đều mô tả endpoint public. Không có auth/session logic trong HTML. |
| Route đề xuất | `/courses/:courseId?tab=reviews` theo `apps/study-client/docs/list_screen.md`; chưa có Study Web route đã xác minh. `courseId` được truyền từ GS-03 theo proposal. |
| API liên quan | #08 `GET /api/v1/courses/{course_id}` — current route/module source `SOURCE_BACKED`; #10 `GET /api/v1/courses/{course_id}/reviews` — catalog/Draft DD only, `DECLARED_NOT_RUNNABLE`. |
| Màn hình liên quan | GS-03 là course detail/tab owner và nguồn `courseId`; expected back/route handoff giữ nguyên ID. Không có luồng viết review/reply trong inventory hoặc HTML GS-05 hiện tại. |
| Side effect | Expected read-only. #08 current source là GET/read-only. #10 Draft DD mô tả GET/read-only; chưa có executable #10 để xác minh. |
| Điều kiện course | F02 chỉ mở detail/tab khi #08 xác nhận course PUBLISHED. API #08 source hiện trả 404 cho invalid, missing hoặc unpublished course. API #10 Draft DD cũng dự kiến gate PUBLISHED. |

### Expected behavior và current behavior

| Expected theo inventory/AC | Current evidence trong checkout |
|---|---|
| Hiển thị reviews/replies và pagination; loading/empty/ready/error; phân biệt course 404 với reviews rỗng. | HTML chỉ có empty-like copy “Chưa có nội dung để hiển thị.”; không có review item, reply, pagination, API call hoặc state binding. |
| Reuse #08 course result rồi GET #10. F02 quy định lazy load theo tab. | Không có Study Web router, API client, cache hoặc handler. AC-05 diagram gọi #08, #09, #10 tuần tự trước khi render. Đây là discrepancy; timing chưa được chốt. |
| Review list được trả bởi public #10. | #10 chỉ xuất hiện trong `docs/lists/list_api.md` và Draft API DD; không tìm thấy route/module/test trong current Study Server `app/` và `tests/`. |
| Có title/rating/aggregate nếu được xác định bởi contract. | API #10 Draft DD yêu cầu `Discussion.title` nhưng ghi source missing; response không có rating/aggregate. DDL legacy `discussions` không có `title` hoặc rating field/table. AC-05 aggregate rating và GS-05/G-06 thiếu rating contract đang xung đột. |
| Điều hướng về cùng course trong GS-03. | Breadcrumb detail, CTA và mọi header/footer anchors dùng `href="#"`; không chứa course ID. |

# GS-05 — Đánh giá và thảo luận công khai · Tổng quan

| Trường | Giá trị |
|---|---|
| Screen ID | `GS-05` |
| Module | Guest / Discovery |
| Route | `/courses/:courseId?tab=reviews` — GS03 route/query tab đã wired; GS05 là child panel, không phải route độc lập |
| Actor/role | Theo DD nguồn; xem overview/source trace bên dưới |
| DD / implementation / runtime status | `DD BLOCKED` — API #10 remains Draft; title/rating/aggregate/query-key/public-visibility rules remain unresolved. `PARTIAL SOURCE-WIRED` — GS03 query tab mounts GS05, which reads source-backed #10. `STUB-BROWSER-VERIFIED` — local in-memory API fixture only; live API/DB/deployment remain `NOT VERIFIED`. |
| Owner | Không được xác định trong inventory/DD nguồn đã chuyển; `CẦN_XÁC_NHẬN` |
| Version / last updated | 0.2 / 2026-11-17 |
| Nguồn đối chiếu | [GS-05.md](../../screen_stitch/02_guest_discovery/GS-05_danh-gia-va-thao-luan-cong-khai/GS-05.md), [GS-05_PLAN.md](../../screen_stitch/02_guest_discovery/GS-05_danh-gia-va-thao-luan-cong-khai/GS-05_PLAN.md), [GS-05_markers.json](../../screen_stitch/02_guest_discovery/GS-05_danh-gia-va-thao-luan-cong-khai/GS-05_markers.json), [list_screen.md](../../list_screen.md) |

## 1. Mục tiêu & phạm vi
- Mục tiêu: Danh sách review/reply; không hiển thị sao trung bình khi không có rating contract.
- In-scope: Tái dùng #8 → GET #10 phân trang; 404 course riêng với empty reviews.
- Out-of-scope: Không kết luận API #10 Draft đã được duyệt, không thêm title/rating/aggregate/filter hoặc mutation, không xem local stub demo là live API/DB/deployment verification.

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
| Current source/runtime | GS03/GS05 Angular source, tests and T021 demo | `PARTIAL SOURCE-WIRED`; tests/build pass; browser was checked against an in-memory local stub; live API/DB/deployment `NOT VERIFIED` |

## 5. Luồng chính và hình ảnh
- Ảnh clean: [screen-clean.png](images/screen-clean.png) (copy từ [GS-05 source screen.png](../../screen_stitch/02_guest_discovery/GS-05_danh-gia-va-thao-luan-cong-khai/screen.png))
- Ảnh numbered: [screen-numbered.png](images/screen-numbered.png) (copy từ [source annotated PNG](../../screen_stitch/02_guest_discovery/GS-05_danh-gia-va-thao-luan-cong-khai/screen_annotated.png))
- Luồng: Tái dùng #8 → GET #10 phân trang; 404 course riêng với empty reviews.
- Priority: P2; Gate/source status: **#10 SOURCE_BACKED LOCALLY; Web caller WIRED; API DD Draft**; **BLOCK:** API #10 Draft vẫn yêu cầu `Discussion.title` không có source; không có course-rating/aggregate source, literal rating-filter key/semantics hoặc public root/reply visibility approval; legacy `discussions` thiếu title/rating và V1-PILOT assessment reviews là model khác; AC-05 aggregate/eager #08→#09→#10 lệch F02 lazy tab; no client cache; loaded projection chưa được DD duyệt; live schema/deployment chưa xác minh.

## 6. Open questions / Change log
- `CẦN_XÁC_NHẬN`: các gate/source questions trong inventory và DD nguồn vẫn giữ nguyên; không tự đóng blocker.
- 2026-11-08 — Chuyển nội dung nguồn sang 8-file template; không chỉnh source, không xác minh runtime.
- 2026-11-17 — T021 wired GS05 to source-backed #10 and added focused tests; desktop/mobile browser screenshots used a temporary in-memory API stub. API DD and live DB/deployment gates remain open.

## Trạng thái và ranh giới bằng chứng

# GS-05 — Đánh giá và thảo luận công khai

> **DD status:** `DD BLOCKED` — API #10 remains Draft; title, rating/aggregate, query-key and public-visibility contract remain unresolved.
> **Implementation status:** `PARTIAL SOURCE-WIRED` — GS03 exposes the reviews query tab and mounts GS05 only after #08 confirms a published course; GS05 calls #10 with the page parameter and renders source-backed author/content/replies/pagination.
> **Runtime status:** `STUB-BROWSER-VERIFIED` — desktop/mobile Chrome render used a temporary in-memory local API stub. Live API, DB schema and deployment remain `NOT VERIFIED`.
> **Phạm vi cập nhật:** T021, 2026-11-17; do not treat static Stitch HTML as Angular runtime.

## Trích đoạn tổng quan từ DD nguồn

### Trích từ DD nguồn: A. Tổng quan màn hình

| Thuộc tính | Đặc tả |
|---|---|
| Screen ID / tên | GS-05 — Đánh giá và thảo luận công khai (tab) |
| Mục tiêu expected | Guest đọc review và reply công khai của một khóa học. Inventory yêu cầu phân trang, tách lỗi khóa học 404 khỏi reviews rỗng, và không hiển thị sao trung bình khi chưa có rating contract. |
| Actor | `Guest`; API catalog và API #10 Draft DD đều mô tả endpoint public. Không có auth/session logic trong HTML. |
| Route đề xuất | `/courses/:courseId?tab=reviews` theo inventory; current GS03 route/query tab mounts GS05 as a child after #08 succeeds. `courseId` remains a route string. |
| API liên quan | #08 `GET /api/v1/courses/{course_id}` is source-backed; #10 `GET /api/v1/courses/{course_id}/reviews` has current route/module/tests, while its DD remains Draft. |
| Màn hình liên quan | GS-03 là course detail/tab owner và nguồn `courseId`; expected back/route handoff giữ nguyên ID. Không có luồng viết review/reply trong inventory hoặc HTML GS-05 hiện tại. |
| Side effect | Read-only GET requests; no review/reply mutation is wired. API #10 source locally returns review/reply content and pagination; deployment/live data remain unverified. |
| Điều kiện course | F02 chỉ mở detail/tab khi #08 xác nhận course PUBLISHED. API #08 source hiện trả 404 cho invalid, missing hoặc unpublished course. API #10 Draft DD cũng dự kiến gate PUBLISHED. |

### Expected behavior và current behavior

| Expected theo inventory/AC | Current evidence trong checkout |
|---|---|
| Hiển thị reviews/replies và pagination; loading/empty/ready/error; phân biệt course 404 với reviews rỗng. | Current GS05 Angular panel maps loading, response-backed empty/ready, #10 404 and safe error states; tests cover each. |
| Reuse #08 course result rồi GET #10. F02 quy định lazy load theo tab. | Current GS03 confirms the course with #08, then mounts GS05 only for `tab=reviews`; #10 is lazy. There is no cross-screen cache. AC-05 eager #08→#09→#10 + aggregate remains a discrepancy. |
| Review list được trả bởi public #10. | Current Study Server route/module/test exist; FE #10 descriptor and GS05 caller are wired locally. Focused API suite passes with fake DB; no live DB/deployment evidence. |
| Có title/rating/aggregate nếu được xác định bởi contract. | API #10 Draft DD yêu cầu `Discussion.title` nhưng ghi source missing; response không có rating/aggregate. DDL legacy `discussions` không có `title` hoặc rating field/table. AC-05 aggregate rating và GS-05/G-06 thiếu rating contract đang xung đột. |
| Điều hướng về cùng course trong GS-03. | Breadcrumb detail, CTA và mọi header/footer anchors dùng `href="#"`; không chứa course ID. |

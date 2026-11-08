# ME-07 — Tạo/chỉnh sửa nội dung · Tổng quan

| Trường | Giá trị |
|---|---|
| Screen ID | `ME-07` |
| Module | Mentor |
| Route | `/mentor/courses/:courseId/content/:contentId?` — route trong inventory, không phải xác nhận router runtime |
| Actor/role | Theo DD nguồn; xem overview/source trace bên dưới |
| DD status | Draft (package được chuyển đổi); source status: **Trạng thái DD:** `DD BLOCKED` — editor payload/type, order write, route mode and #51 request approval are unresolved.; **Trạng thái triển khai:** `IMPLEMENTATION BLOCKED` — Study Web is `UNWIRED`; the mockup editor is a placeholder and current APIs do not persist every visible field.; **Trạng thái runtime:** `RUNTIME NOT VERIFIED` — local API source and DDL artifacts do not verify Study Web, deployed APIs or live database. |
| Owner | Không được xác định trong inventory/DD nguồn đã chuyển; `CẦN_XÁC_NHẬN` |
| Version / last updated | 0.1 / 2026-11-08 |
| Nguồn đối chiếu | [ME-07.md](../../screen_stitch/04_mentor/ME-07_tao-chinh-sua-noi-dung/ME-07.md), [ME-07_PLAN.md](../../screen_stitch/04_mentor/ME-07_tao-chinh-sua-noi-dung/ME-07_PLAN.md), [ME-07_markers.json](../../screen_stitch/04_mentor/ME-07_tao-chinh-sua-noi-dung/ME-07_markers.json), [list_screen.md](../../list_screen.md) |

## 1. Mục tiêu & phạm vi
- Mục tiêu: Editor theo content_type/payload, xác thực dirty state.
- In-scope: GET #49 tìm content hiện hữu → POST #50 hoặc PUT #51 → refresh #49.
- Out-of-scope: Xem gate bên dưới; không kết luận Study Web route/UI đã wired hoặc runtime đã chạy.

## 2. Use cases chính
| Use case / AC | Actor | Kết quả kỳ vọng theo inventory |
|---|---|---|
| AC-22 | Theo DD nguồn; `CẦN_XÁC_NHẬN` nếu nguồn chưa chốt | Editor theo content_type/payload, xác thực dirty state. |

## 3. Precondition / Entry / Dependencies
- Điều kiện vào, role guard và dependency: xem trích đoạn tổng quan nguồn; không bổ sung giả định.
- API references: #49, #50, #51
- Liên kết màn hình dự kiến: [ME-06](../ME-06-CayNoiDungKhoaHoc/00-overview.md), [ME-08](../ME-08-XuatBanXoaNoiDung/00-overview.md)
- Links: [UI](01-ui-elements.md) · [Events](02-events.md) · [Navigation](06-navigation.md)

## 4. UI states
| State | Nguồn | Giá trị |
|---|---|---|
| Inventory states | `list_screen.md` | draft/dirty/validating/saving/conflict |
| Current runtime | Worklog/context Study Web | `UNWIRED` / `RUNTIME NOT VERIFIED` |

## 5. Luồng chính và hình ảnh
- Ảnh clean: [screen-clean.png](images/screen-clean.png) (copy từ [ME-07 source screen.png](../../screen_stitch/04_mentor/ME-07_tao-chinh-sua-noi-dung/screen.png))
- Ảnh numbered: [screen-numbered.png](images/screen-numbered.png) (copy từ [source annotated PNG](../../screen_stitch/04_mentor/ME-07_tao-chinh-sua-noi-dung/screen_annotated.png))
- Luồng: GET #49 tìm content hiện hữu → POST #50 hoặc PUT #51 → refresh #49.
- Priority: P1; Gate/source status: **D**; **BLOCK:** PUT #51 chưa mô tả body rõ trong catalog

## 6. Open questions / Change log
- `CẦN_XÁC_NHẬN`: các gate/source questions trong inventory và DD nguồn vẫn giữ nguyên; không tự đóng blocker.
- 2026-11-08 — Chuyển nội dung nguồn sang 8-file template; không chỉnh source, không xác minh runtime.

## Trạng thái và ranh giới bằng chứng

# ME-07 — Tạo/chỉnh sửa nội dung

> **Trạng thái DD:** `DD BLOCKED` — editor payload/type, order write, route mode and #51 request approval are unresolved.
> **Trạng thái triển khai:** `IMPLEMENTATION BLOCKED` — Study Web is `UNWIRED`; the mockup editor is a placeholder and current APIs do not persist every visible field.
> **Trạng thái runtime:** `RUNTIME NOT VERIFIED` — local API source and DDL artifacts do not verify Study Web, deployed APIs or live database.

## Trích đoạn tổng quan từ DD nguồn

### Trích từ DD nguồn: 1. Tổng quan màn hình

| Thuộc tính | Đặc tả |
|---|---|
| Screen ID / tên | ME-07 — Tạo/chỉnh sửa nội dung |
| Mục tiêu | Tạo Content mới hoặc sửa một Content đã tải trong course của Mentor; form chỉ được gửi khi data schema được duyệt. |
| Actor | Mentor. #49–#51 require Bearer JWT role `MENTOR`; current server code additionally requires direct course owner. |
| Route đề xuất | `/mentor/courses/:courseId/content/:contentId?`; route là inventory design, chưa có client router. Absent `contentId` candidate create mode; present ID candidate edit mode. |
| API đọc | GET `/api/v1/mentor/courses/{course_id}/content` (#49), returns collection `Content[]`, not a detail resource. |
| API create | POST `/api/v1/mentor/content` (#50), request requires `course_id`, `content_type`, `title`, `payload`. |
| API update | PUT `/api/v1/mentor/content/{content_id}` (#51), current source requires `content_type`, `title`, `payload`; body is not listed in the API catalog and API DD calls it DERIVED. |
| Màn hình liên quan | ME-06 ([cây nội dung DD](../../screen_stitch/04_mentor/ME-06_cay-noi-dung-khoa-hoc/ME-06.md)) opens the editor; ME-08 ([action mockup](../../screen_stitch/04_mentor/ME-08_xuat-ban-xoa-noi-dung/code.html)) handles publish/delete. |
| States trong inventory | `draft/dirty/validating/saving/conflict`; this DD adds loading/ready/empty/not-found/denied/saved/error to map current API outcomes. |
| Plan/ảnh chú thích | [ME-07_PLAN.md](../../screen_stitch/04_mentor/ME-07_tao-chinh-sua-noi-dung/ME-07_PLAN.md), [screen_annotated.png](../../screen_stitch/04_mentor/ME-07_tao-chinh-sua-noi-dung/screen_annotated.png), [ME-07_markers.json](../../screen_stitch/04_mentor/ME-07_tao-chinh-sua-noi-dung/ME-07_markers.json), [SVG overlay](../../screen_stitch/04_mentor/ME-07_tao-chinh-sua-noi-dung/ME-07_markers_overlay.svg). |

### Expected behavior

The inventory row [ME-07](../../list_screen.md#L167) says editor fields follow `content_type/payload`, track dirty state, load with #49, create with #50 or update with #51, then refresh #49. AC-22 says Mentor must have course-management permission, reads the tree and chooses CRUD/publish/delete; its diagram represents five API branches (#49–#53). F08 orders ME-06 → ME-07 → ME-08 and says enable actions only when server confirms ownership/allowed transition.

### Current behavior

- The screenshot shows blank title/type/order controls and a placeholder editor marked “Đang chờ kết nối giao thức”; media input is visibly locked. “Lưu bản nháp” is disabled. Side panels show static data-quality/security text, a static “Đang đối soát” session status/progress, a promotional image and footer links.
- `code.html` contains 14 anchors (all `href="#"`), two inputs, one select, one disabled button and one image. There is no `<form>`, no custom event script, no fetch/XHR, no route binding and no API request. The two scripts are Tailwind config/loading only.
- The title has a visual required marker, but the input has no `required`/length rule. The select has sample options `theory`, `reading`, `practice`, but no `required` attribute. Order uses `type=number,min=1`. None of these controls has save/dirty validation logic.
- Study Web is `UNWIRED` in the current context and checkout; no runtime route, auth state, form state, cache or navigation is verified.

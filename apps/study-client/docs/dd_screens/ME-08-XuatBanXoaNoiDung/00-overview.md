# ME-08 — Xuất bản/xóa nội dung · Tổng quan

| Trường | Giá trị |
|---|---|
| Screen ID | `ME-08` |
| Module | Mentor |
| Route | `/mentor/content/:contentId/actions` — route trong inventory, không phải xác nhận router runtime |
| Actor/role | Theo DD nguồn; xem overview/source trace bên dưới |
| DD status | Draft (package được chuyển đổi); source status: **DD status:** `DD BLOCKED` — publish request/transition, readiness, delete dependency policy and target hydration are unresolved.; **Implementation status:** `IMPLEMENTATION BLOCKED` — Study Web is `UNWIRED`; current screen source has no selected Content or working controls; server fallbacks contain unapproved policies.; **Runtime status:** `RUNTIME NOT VERIFIED` — local API source, fake-session test source and checked-in migrations do not establish deployed APIs or live database behavior. |
| Owner | Không được xác định trong inventory/DD nguồn đã chuyển; `CẦN_XÁC_NHẬN` |
| Version / last updated | 0.1 / 2026-11-08 |
| Nguồn đối chiếu | [ME-08.md](../../screen_stitch/04_mentor/ME-08_xuat-ban-xoa-noi-dung/ME-08.md), [ME-08_PLAN.md](../../screen_stitch/04_mentor/ME-08_xuat-ban-xoa-noi-dung/ME-08_PLAN.md), [ME-08_markers.json](../../screen_stitch/04_mentor/ME-08_xuat-ban-xoa-noi-dung/ME-08_markers.json), [list_screen.md](../../list_screen.md) |

## 1. Mục tiêu & phạm vi
- Mục tiêu: Review cảnh báo dependency, xác nhận publish/unpublish hoặc xóa.
- In-scope: PATCH #52 hay DELETE #53 theo action → GET #49 refresh; không tự đặt soft-delete policy.
- Out-of-scope: Xem gate bên dưới; không kết luận Study Web route/UI đã wired hoặc runtime đã chạy.

## 2. Use cases chính
| Use case / AC | Actor | Kết quả kỳ vọng theo inventory |
|---|---|---|
| AC-22 | Theo DD nguồn; `CẦN_XÁC_NHẬN` nếu nguồn chưa chốt | Review cảnh báo dependency, xác nhận publish/unpublish hoặc xóa. |

## 3. Precondition / Entry / Dependencies
- Điều kiện vào, role guard và dependency: xem trích đoạn tổng quan nguồn; không bổ sung giả định.
- API references: #52, #53, #49
- Liên kết màn hình dự kiến: [ME-06](../ME-06-CayNoiDungKhoaHoc/00-overview.md)
- Links: [UI](01-ui-elements.md) · [Events](02-events.md) · [Navigation](06-navigation.md)

## 4. UI states
| State | Nguồn | Giá trị |
|---|---|---|
| Inventory states | `list_screen.md` | confirm/processing/success/blocked |
| Current runtime | Worklog/context Study Web | `UNWIRED` / `RUNTIME NOT VERIFIED` |

## 5. Luồng chính và hình ảnh
- Ảnh clean: [screen-clean.png](images/screen-clean.png) (copy từ [ME-08 source screen.png](../../screen_stitch/04_mentor/ME-08_xuat-ban-xoa-noi-dung/screen.png))
- Ảnh numbered: [screen-numbered.png](images/screen-numbered.png) (copy từ [source annotated PNG](../../screen_stitch/04_mentor/ME-08_xuat-ban-xoa-noi-dung/screen_annotated.png))
- Luồng: PATCH #52 hay DELETE #53 theo action → GET #49 refresh; không tự đặt soft-delete policy.
- Priority: P2; Gate/source status: **D**; **BLOCK:** Publish state machine và delete dependency cần chốt

## 6. Open questions / Change log
- `CẦN_XÁC_NHẬN`: các gate/source questions trong inventory và DD nguồn vẫn giữ nguyên; không tự đóng blocker.
- 2026-11-08 — Chuyển nội dung nguồn sang 8-file template; không chỉnh source, không xác minh runtime.

## Trạng thái và ranh giới bằng chứng

# ME-08 — Xuất bản/xóa nội dung

> **DD status:** `DD BLOCKED` — publish request/transition, readiness, delete dependency policy and target hydration are unresolved.
> **Implementation status:** `IMPLEMENTATION BLOCKED` — Study Web is `UNWIRED`; current screen source has no selected Content or working controls; server fallbacks contain unapproved policies.
> **Runtime status:** `RUNTIME NOT VERIFIED` — local API source, fake-session test source and checked-in migrations do not establish deployed APIs or live database behavior.

## Trích đoạn tổng quan từ DD nguồn

### Trích từ DD nguồn: 1. Tổng quan màn hình

| Thuộc tính | Đặc tả |
|---|---|
| Screen ID / tên | ME-08 — Xuất bản/xóa nội dung |
| Mục tiêu | Hiển thị một Content được chọn từ cây ME-06, cho Mentor xem trạng thái/tác động rồi yêu cầu publish, unpublish hoặc xóa nếu được phép. Đây là mục tiêu theo inventory/AC-22, chưa được UI/API owner chốt. |
| Actor | Mentor. API #49/#52/#53 yêu cầu Bearer JWT, role `MENTOR`; source hiện tại còn kiểm tra direct owner `courses.mentor_id`, không có assigned-Mentor policy. |
| Route đề xuất | `/mentor/content/:contentId/actions` theo inventory. Route chưa tồn tại trong Study Web; route không mang `courseId` dù #49 refresh cần `course_id`. |
| Màn hình trước/sau | ME-06 ([cây nội dung](../../screen_stitch/04_mentor/ME-06_cay-noi-dung-khoa-hoc/ME-06.md)) chọn Content và là điểm quay lại. `list_screen.md` liên kết ME-08 với ME-06. |
| APIs theo inventory | GET #49 để hydrate/refresh cây; PATCH #52 publish/unpublish; DELETE #53 xóa. AC-22 nói GET cây → rẽ nhánh thao tác → reload cây. |
| Trạng thái mong đợi | Inventory: `confirm/processing/success/blocked`. DD tách các trạng thái chờ tải, sẵn sàng, mutation, kết quả refresh, lỗi quyền, không tìm thấy và lỗi mạng/500. |
| Plan và artifacts | [ME-08_PLAN.md](../../screen_stitch/04_mentor/ME-08_xuat-ban-xoa-noi-dung/ME-08_PLAN.md), [screen_annotated.png](../../screen_stitch/04_mentor/ME-08_xuat-ban-xoa-noi-dung/screen_annotated.png), [ME-08_markers.json](../../screen_stitch/04_mentor/ME-08_xuat-ban-xoa-noi-dung/ME-08_markers.json), [SVG overlay](../../screen_stitch/04_mentor/ME-08_xuat-ban-xoa-noi-dung/ME-08_markers_overlay.svg). |

### Expected behavior

`list_screen.md` mô tả action dialog cho thao tác publish/unpublish hoặc delete, có cảnh báo dependency, xác nhận trước mutation, sau đó refresh #49. AC-22 tiền điều kiện là Mentor có quyền quản lý course; flow của AC đọc Content tree, chọn CRUD/publish/delete rồi reload cây. F08 ghi ME-06 → ME-07 → ME-08 và yêu cầu chỉ bật action khi server gửi ownership/allowed transition. Tuy nhiên #49 chỉ trả `Content[]`, không có cờ permission hay danh sách transition được phép.

### Current behavior của asset và Study Web

- `screen.png`/`code.html` là một trang đầy đủ header/footer chứ không phải modal phủ lên ME-06 như phân loại `Dialog` trong inventory. Nội dung mục tiêu vẫn ghi “Chưa chọn nội dung thao tác”; không có Content ID, course ID, picker hay data binding.
- Hai action `Xuất bản bài học` và `Xóa nội dung` đều `disabled` + `aria-disabled="true"`. Chỉ có action publish; không có control unpublish hoặc hộp xác nhận. Link quay lại ME-06 cùng các anchor điều hướng đều `href="#"`.
- `code.html` có 15 anchors, hai disabled buttons, không có input/form/API call/custom event. Scripts chỉ nạp/cấu hình Tailwind; HTML không gửi request.
- Các giá trị “Bản nháp (Chưa xuất bản)”, “Cấp độ thấp”, audit “Hôm nay, 08:30”, tỷ lệ chứng chỉ, điểm danh/bài nộp, production, vùng Châu Á–Thái Bình Dương và Safe Mode là copy mẫu. Chúng không được trả bởi #49/#52/#53.
- Study Web hiện `UNWIRED`: không có editable source, package manifest hoặc feature route. Không suy ra route, session, cache, xác nhận dialog hay trạng thái runtime từ asset.

### Sơ đồ liên kết màn hình

```mermaid
flowchart LR
    ME06[ME-06: chọn Content trong course] -->|contentId + course context cần được giữ| ME08[ME-08: xem và xác nhận action]
    ME08 -->|GET #49: hydrate/refresh| C[(active Content[])]
    ME08 -->|PATCH #52: publish/unpublish, body DERIVED| C
    ME08 -->|DELETE #53: soft-delete, guards DERIVED| C
    C -->|sau mutation, dùng courseId| ME06
```

Sơ đồ là expected interaction nối với current API source. Không có client navigation/cache thực thi trong checkout hiện tại. Route ME-08 chỉ mang `contentId`; #49 yêu cầu `course_id`. #52 response có `course_id`, còn #53 `DeleteResult` không có. Vì vậy phải giữ `courseId` từ ME-06 trước khi DELETE nếu muốn làm bước refresh bắt buộc. Cách truyền state/route này chưa được xác nhận.

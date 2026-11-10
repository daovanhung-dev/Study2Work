# ME-04 — Tải lên và tạo bài giảng · Tổng quan

| Trường | Giá trị |
|---|---|
| Screen ID | `ME-04` |
| Module | Mentor |
| Route | `/mentor/courses/:courseId/lectures/new` — route trong inventory, không phải xác nhận router runtime |
| Actor/role | Theo DD nguồn; xem overview/source trace bên dưới |
| DD status | Draft (package được chuyển đổi); source status: **DD status:** `DD BLOCKED` — chưa đủ contract để chuyển sang DD READY.; **Implementation status:** `IMPLEMENTATION BLOCKED`.; **Runtime status:** `RUNTIME NOT VERIFIED` — Study Web route/source/serving không có trong checkout. |
| Owner | Không được xác định trong inventory/DD nguồn đã chuyển; `CẦN_XÁC_NHẬN` |
| Version / last updated | 0.1 / 2026-11-08 |
| Nguồn đối chiếu | [ME-04.md](../../screen_stitch/04_mentor/ME-04_tai-len-va-tao-bai-giang/ME-04.md), [ME-04_PLAN.md](../../screen_stitch/04_mentor/ME-04_tai-len-va-tao-bai-giang/ME-04_PLAN.md), [ME-04_markers.json](../../screen_stitch/04_mentor/ME-04_tai-len-va-tao-bai-giang/ME-04_markers.json), [list_screen.md](../../list_screen.md) |

## 1. Mục tiêu & phạm vi
- Mục tiêu: Form lecture metadata, sắp xếp thứ tự, đính kèm media.
- In-scope: GET #46 xác minh course context → POST #34 cho asset → POST #47; không nhận content:int64 như rich-text nếu chưa chốt.
- Out-of-scope: Xem gate bên dưới; không kết luận Study Web route/UI đã wired hoặc runtime đã chạy.

## 2. Use cases chính
| Use case / AC | Actor | Kết quả kỳ vọng theo inventory |
|---|---|---|
| AC-21 | Theo DD nguồn; `CẦN_XÁC_NHẬN` nếu nguồn chưa chốt | Form lecture metadata, sắp xếp thứ tự, đính kèm media. |

## 3. Precondition / Entry / Dependencies
- Điều kiện vào, role guard và dependency: xem trích đoạn tổng quan nguồn; không bổ sung giả định.
- API references: #46, #34, #47
- Liên kết màn hình dự kiến: [ME-05](../ME-05-XemBaiGiangMentor/00-overview.md), [ME-03](../ME-03-WorkspaceKhoaHocCuaMentor/00-overview.md)
- Links: [UI](01-ui-elements.md) · [Events](02-events.md) · [Navigation](06-navigation.md)

## 4. UI states
| State | Nguồn | Giá trị |
|---|---|---|
| Inventory states | `list_screen.md` | draft/uploading/creating/422/error |
| Current runtime | Worklog/context Study Web | `UNWIRED` / `RUNTIME NOT VERIFIED` |

## 5. Luồng chính và hình ảnh
- Ảnh clean: [screen-clean.png](images/screen-clean.png) (copy từ [ME-04 source screen.png](../../screen_stitch/04_mentor/ME-04_tai-len-va-tao-bai-giang/screen.png))
- Ảnh numbered: [screen-numbered.png](images/screen-numbered.png) (copy từ [source annotated PNG](../../screen_stitch/04_mentor/ME-04_tai-len-va-tao-bai-giang/screen_annotated.png))
- Luồng: GET #46 xác minh course context → POST #34 cho asset → POST #47; không nhận content:int64 như rich-text nếu chưa chốt.
- Priority: P1; Gate/source status: **D**; **BLOCK:** Schema lecture.content và asset refs còn ambiguity

## 6. Open questions / Change log
- `CẦN_XÁC_NHẬN`: các gate/source questions trong inventory và DD nguồn vẫn giữ nguyên; không tự đóng blocker.
- 2026-11-08 — Chuyển nội dung nguồn sang 8-file template; không chỉnh source, không xác minh runtime.

## Trạng thái và ranh giới bằng chứng

# ME-04 — Tải lên và tạo bài giảng

> **DD status:** `DD BLOCKED` — chưa đủ contract để chuyển sang DD READY.
> **Implementation status:** `IMPLEMENTATION BLOCKED`.
> **Runtime status:** `RUNTIME NOT VERIFIED` — Study Web route/source/serving không có trong checkout.
> **Scope phiên:** chỉ Screen ID ME-04.

## Trích đoạn tổng quan từ DD nguồn

### Trích từ DD nguồn: 1. Tổng quan

| Thuộc tính | Đặc tả |
|---|---|
| Screen ID | ME-04 |
| Tên | Tải lên và tạo bài giảng |
| Mục tiêu | Tạo lecture trong course, tải media/tài liệu qua API #34 rồi gửi metadata và asset references qua API #47. |
| Actor dự kiến | Mentor đã đăng nhập. AC-21 cho phép sở hữu hoặc được phân công course; current APIs chỉ chấp nhận trực tiếp owner. |
| Route đề xuất | `/mentor/courses/:courseId/lectures/new`; route chưa được wire. `courseId` phải tương thích signed int64 của #34/#47. |
| Trước màn hình | ME-03 workspace/course context hoặc deep link; authenticated MENTOR session; quyền truy cập course cần được xác minh. |
| Sau thành công | ME-05 `/mentor/lectures/:lectureId`; ME-05 dùng GET #48 để đọc lại lecture và asset links. Quay lại ME-03 dùng course context hiện tại. |
| API | GET #46 context; POST #34 upload; POST #47 create; GET #48 downstream read. |
| Thiết kế được cung cấp | `screen.png` và `code.html`; đây là sample/mockup, không phải runtime. |

### 1.1 Trạng thái bằng chứng

| Nhóm | Kết luận | Bằng chứng |
|---|---|---|
| Expected behavior | Form metadata, thứ tự, media, tạo lecture; inventory nêu #46 → #34 → #47 và trạng thái draft/uploading/creating/422/error. | [`list_screen.md` ME-04](../../list_screen.md#L164), AC-21. |
| Current UI | Không có Study Web `src/`, package manifest hoặc router; HTML không có file input/form/contenteditable/API. CTA chỉ hiển thị giả lập thành công sau 900 ms. | Checkout hiện tại; [code.html](../../screen_stitch/04_mentor/ME-04_tai-len-va-tao-bai-giang/code.html). |
| Current backend source | #34, #46, #47, #48 có route/module source; #34/#47 side effects và response được ghi ở dưới. | [`app/api/v1.py`](../../../../study-server/app/api/v1.py#L697), module source liên kết ở §10. |
| API tests | Test source có cho các nhánh chính; đã đọc nhưng **không chạy trong phiên này**. Test DB/provider giả không xác minh live deployment. | Test files ở §10; `.agents/server-study/tests.md`. |
| Persistence/runtime | SQL legacy BIGINT và migrations 004/005 có trong repo; live DB, migration deployment, object storage credentials/network chưa xác minh. | `infra/postgres/study-server/DB.sql`, migrations 004/005. |

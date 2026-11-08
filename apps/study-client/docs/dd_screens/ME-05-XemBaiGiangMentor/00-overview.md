# ME-05 — Xem bài giảng mentor · Tổng quan

| Trường | Giá trị |
|---|---|
| Screen ID | `ME-05` |
| Module | Mentor |
| Route | `/mentor/lectures/:lectureId` — route trong inventory, không phải xác nhận router runtime |
| Actor/role | Theo DD nguồn; xem overview/source trace bên dưới |
| DD status | Draft (package được chuyển đổi); source status: **Trạng thái:** `DD BLOCKED`; `IMPLEMENTATION BLOCKED`; `RUNTIME NOT VERIFIED`. |
| Owner | Không được xác định trong inventory/DD nguồn đã chuyển; `CẦN_XÁC_NHẬN` |
| Version / last updated | 0.1 / 2026-11-08 |
| Nguồn đối chiếu | [ME-05.md](../../screen_stitch/04_mentor/ME-05_xem-bai-giang-mentor/ME-05.md), [ME-05_PLAN.md](../../screen_stitch/04_mentor/ME-05_xem-bai-giang-mentor/ME-05_PLAN.md), [ME-05_markers.json](../../screen_stitch/04_mentor/ME-05_xem-bai-giang-mentor/ME-05_markers.json), [list_screen.md](../../list_screen.md) |

## 1. Mục tiêu & phạm vi
- Mục tiêu: Thông tin bài giảng vừa tạo, file, trạng thái và link về course.
- In-scope: GET #48; không tự bổ sung edit lecture endpoint nếu không có contract.
- Out-of-scope: Xem gate bên dưới; không kết luận Study Web route/UI đã wired hoặc runtime đã chạy.

## 2. Use cases chính
| Use case / AC | Actor | Kết quả kỳ vọng theo inventory |
|---|---|---|
| AC-21 | Theo DD nguồn; `CẦN_XÁC_NHẬN` nếu nguồn chưa chốt | Thông tin bài giảng vừa tạo, file, trạng thái và link về course. |

## 3. Precondition / Entry / Dependencies
- Điều kiện vào, role guard và dependency: xem trích đoạn tổng quan nguồn; không bổ sung giả định.
- API references: #48
- Liên kết màn hình dự kiến: [ME-03](../ME-03-WorkspaceKhoaHocCuaMentor/00-overview.md), [ME-06](../ME-06-CayNoiDungKhoaHoc/00-overview.md)
- Links: [UI](01-ui-elements.md) · [Events](02-events.md) · [Navigation](06-navigation.md)

## 4. UI states
| State | Nguồn | Giá trị |
|---|---|---|
| Inventory states | `list_screen.md` | loading/ready/not-found |
| Current runtime | Worklog/context Study Web | `UNWIRED` / `RUNTIME NOT VERIFIED` |

## 5. Luồng chính và hình ảnh
- Ảnh clean: [screen-clean.png](images/screen-clean.png) (copy từ [ME-05 source screen.png](../../screen_stitch/04_mentor/ME-05_xem-bai-giang-mentor/screen.png))
- Ảnh numbered: [screen-numbered.png](images/screen-numbered.png) (copy từ [source annotated PNG](../../screen_stitch/04_mentor/ME-05_xem-bai-giang-mentor/screen_annotated.png))
- Luồng: GET #48; không tự bổ sung edit lecture endpoint nếu không có contract.
- Priority: P1; Gate/source status: **D**

## 6. Open questions / Change log
- `CẦN_XÁC_NHẬN`: các gate/source questions trong inventory và DD nguồn vẫn giữ nguyên; không tự đóng blocker.
- 2026-11-08 — Chuyển nội dung nguồn sang 8-file template; không chỉnh source, không xác minh runtime.

## Trạng thái và ranh giới bằng chứng

# ME-05 — Xem bài giảng Mentor

> **Trạng thái:** `DD BLOCKED`; `IMPLEMENTATION BLOCKED`; `RUNTIME NOT VERIFIED`.
> API #48 có route/module/test source local; điều đó không xác nhận Study Web route, API deployment, live DB/migration hay UI behavior.

## Trích đoạn tổng quan từ DD nguồn

### Trích từ DD nguồn: 1. Tổng quan

| Thuộc tính | Đặc tả |
|---|---|
| Screen ID / tên | ME-05 — Xem bài giảng Mentor |
| Mục tiêu | Sau khi có lecture ID, đọc lại lecture đã lưu và hiển thị dữ liệu server; cho Mentor thấy trạng thái và tài nguyên được gắn nếu contract/UI được chốt. |
| Actor | Mentor đã xác thực. API #48 yêu cầu Bearer JWT role `MENTOR`; client route guard/session flow chưa có source. |
| Route kỳ vọng | `/mentor/lectures/:lectureId` — route đề xuất trong inventory, chưa được Study Web implement/wire. |
| API | `GET /api/v1/mentor/lectures/{lecture_id}` (API #48), path `lecture_id:int64!`; không body/query. |
| Màn hình liên quan | ME-04 tạo lecture → ME-05 đọc lại; breadcrumb/course context dự kiến về ME-03; nội dung course ở ME-06. Inventory chỉ liên kết ME-03/ME-06. |
| Trạng thái DD | BLOCKED bởi các field/action trong mockup chưa có contract, quyền assigned-course chưa khớp source, API DD #48 còn Draft và Study Web UNWIRED. |

### Expected behavior

`list_screen.md` yêu cầu Mentor mở lecture qua ID, gọi #48, hiển thị `loading/ready/not-found`, liên kết ME-03 và ME-06, và không tự thêm endpoint chỉnh sửa. AC-21 mô tả luồng tạo lecture rồi đọc lại. ME-04 dự kiến dùng `data.id` từ #47 làm `lectureId`; giá trị trả về từ server là nguồn cho màn chi tiết.

### Current behavior

- Ảnh nguồn là mockup populated. HTML tĩnh không có route binding, API call, `<video>`, form, event handler hay link đích (mọi `href` là `#`). Nội dung cụ thể trong ảnh là dữ liệu mẫu.
- Study Web checkout không có `src/`, package manifest hoặc router có thể wire màn hình. `dist/` là artifact ignored; serving/provenance không xác nhận runtime.
- Study Server có route/module API #48. Route gọi shared MENTOR JWT guard trước path parse/DB; handler chỉ đọc `lessons`, `courses`, `lesson_uploads`, `uploads`.
- API #48 local response không có author, video stream, analytics, discussion, chapter list, course outline hay link bài trước/sau. #48 không sửa lecture/status.
- API DD #48 vẫn `Draft — Needs Confirmation`; local DDL/migrations và fake-DB tests không chứng minh schema/deployment live.

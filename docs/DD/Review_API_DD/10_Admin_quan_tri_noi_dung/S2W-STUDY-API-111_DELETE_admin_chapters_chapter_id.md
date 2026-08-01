# Review API DD — S2W-STUDY-API-111

- DD source: `docs/DD/Study2Work_DD_API/10_Admin_quan_tri_noi_dung/S2W-STUDY-API-111_DELETE_admin_chapters_chapter_id.xlsx`
- Method + endpoint: `DELETE /api/v1/admin/chapters/{chapter_id}`
- Kết luận: **CẦN SỬA**

## Findings

| Severity | Sheet + cell | Mô tả cụ thể | Căn cứ BD | Cách sửa |
|---|---|---|---|---|
| P1 | `00.Hướng dẫn!A4:B4`, `Cover!B19` | Inventory 44 file/không schema đã stale. | SQL `:1-31`; `docs/BD/base/0. Study2Work_System_Architecture.md:632-700` | Cập nhật source inventory/precedence. |
| P0 | `2.Response!D9:D11`, `2.Response!A33` | Envelope/error không canonical. | `docs/BD/base/0. Study2Work_System_Architecture.md:632-700` | Dùng canonical envelope nếu có body. |
| P0 | `2.Response!B9:E9`, `2.Response!A22` | DD chọn `204` nhưng vẫn định nghĩa JSON `data.deleted/affected_items_count/audit_id` và pagination mẫu. HTTP 204 không có body. | Chính DD `2.Response!E9`; canonical meta `docs/BD/base/0. Study2Work_System_Architecture.md:693-700` | Chọn `200` với canonical body hoặc `204` không body; bỏ pagination. |
| P1 | `3.Data mapping!A20`, `00.Hướng dẫn!A13:B18` | SOFT_DELETE còn `<mapping>` và predicate generic dù checklist đã tick. | `docs/BD/base/0. Study2Work_System_Architecture.md:601-628,738-752` | Viết rõ archive/reject/delete algorithm, locks và audit. |
| P0 | `5.DB_Update_Main!B8:I10`, `3.Data mapping!E14` | DD update `status/deleted_at/updated_*`, nhưng `chapters` không có bất kỳ cột soft-delete/lifecycle nào. | SQL `:446-456` | Bổ sung migration cho archival metadata hoặc từ chối delete khi không thể xóa vật lý; không giả định cột tồn tại. |
| P0 | `3.Data mapping!D12:D14` | Xóa vật lý chapter sẽ cascade lessons, materials/progress và có thể exercises; trái mục tiêu bảo toàn lịch sử của nội dung đã học. | SQL `:446-505,539-555`; BD-10 `:91,163-167,181` | Với published/used content chỉ archive/version; kiểm tra descendants/enrollments trước, tuyệt đối không cascade lịch sử. |
| P1 | `1.Request!D22:E22`, `6.DB_Update_Related!A12:I12` | `reason` optional và audit generic dù delete/archive là thao tác rủi ro. | Audit rule BD-10 `:182-193`; audit schema `:691-719` | Bắt buộc reason; ghi actor/action/target/before/after/reason trong cùng transaction. |

## Checklist duyệt lại

- [ ] Source/envelope đã sửa.
- [ ] Status `200`+body hoặc `204` no-body nhất quán.
- [ ] Không còn pagination ở DELETE.
- [ ] Soft-delete schema/migration thật được chốt.
- [ ] Không cascade dữ liệu lịch sử learner.
- [ ] Kiểm tra descendant/enrollment/parent lifecycle.
- [ ] Reason + audit atomic.
- [ ] Test published/unused/used chapter, retry và race.

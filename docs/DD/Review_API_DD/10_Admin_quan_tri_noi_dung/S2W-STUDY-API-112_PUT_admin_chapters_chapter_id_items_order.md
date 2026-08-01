# Review API DD — S2W-STUDY-API-112

- DD source: `docs/DD/Study2Work_DD_API/10_Admin_quan_tri_noi_dung/S2W-STUDY-API-112_PUT_admin_chapters_chapter_id_items_order.xlsx`
- Method + endpoint: `PUT /api/v1/admin/chapters/{chapter_id}/items/order`
- Kết luận: **CẦN SỬA**

## Findings

| Severity | Sheet + cell | Mô tả cụ thể | Căn cứ BD | Cách sửa |
|---|---|---|---|---|
| P1 | `00.Hướng dẫn!A4:B4`, `Cover!B19` | Nguồn 44 file/không schema đã stale. | SQL `:1-31`; canonical `docs/BD/base/0. Study2Work_System_Architecture.md:632-700` | Cập nhật 48 file/schema. |
| P0 | `2.Response!D9:D11`, `2.Response!A34` | Envelope/error cũ trái canonical. | `docs/BD/base/0. Study2Work_System_Architecture.md:632-700` | Dùng canonical envelope. |
| P1 | `2.Response!A22` | Mutation response có pagination mẫu thừa. | `docs/BD/base/0. Study2Work_System_Architecture.md:693-700` | Bỏ pagination. |
| P1 | `3.Data mapping!A20`, `00.Hướng dẫn!A13:B18` | UPDATE `<mapping>` không mô tả batch reorder dù checklist tự tick hoàn tất. | `docs/BD/base/0. Study2Work_System_Architecture.md:601-628,738-752` | Đặc tả full replace, lock siblings và batch update cụ thể. |
| P0 | `1.Request!D23:I25` | `items[].type/id/order` đều là String; không có enum LESSON/EXERCISE, UUID, integer, uniqueness hay ownership validation. | BD-10 `:94,136-145`; SQL `:458-505` | Dùng discriminated items `{type: LESSON|EXERCISE,id:UUID,orderIndex:int}`; validate unique, cùng chapter và complete set. |
| P0 | `5.DB_Update_Main!B8:I10`, `3.Data mapping!D14:E14` | DD ghi `chapters.items` JSON nhưng schema không có; lesson có `order_index`, exercise không có `order_index`, nên schema hiện tại không thể biểu diễn thứ tự hợp nhất lesson+bài tập. | SQL `:446-505` | Chọn mô hình `chapter_items(type,target_id,order_index)` hoặc thêm compatible ordering model; migration trước khi duyệt API. |
| P0 | `2.Response!C17:C18`, `3.Data mapping!C13:G15` | Không mô tả tác động khi chèn nội dung bắt buộc trước tiến độ đã hoàn thành; impact/audit chỉ placeholder. | BD-10 `:136-167,177-182` | Tính affected learners/progress risk, yêu cầu reason/acknowledgement, audit before/after order và notify nếu important. |

## Checklist duyệt lại

- [ ] Source/envelope/pagination đã sửa.
- [ ] Item discriminator, UUID và integer order đúng.
- [ ] Full/partial replace semantics rõ.
- [ ] Có data model ordering chung được migration.
- [ ] Validate ownership, duplicate và missing item.
- [ ] Lock/atomic reorder tránh race.
- [ ] Impact/audit/notification được đặc tả.
- [ ] OpenAPI/test bao phủ mixed items và published chapter.

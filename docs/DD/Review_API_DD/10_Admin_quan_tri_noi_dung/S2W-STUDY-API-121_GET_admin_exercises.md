# Review API DD — S2W-STUDY-API-121

- DD source: `docs/DD/Study2Work_DD_API/10_Admin_quan_tri_noi_dung/S2W-STUDY-API-121_GET_admin_exercises.xlsx`
- Method + endpoint: `GET /api/v1/admin/exercises`
- Kết luận: **CẦN SỬA**

## Findings

| Severity | Sheet + cell | Mô tả cụ thể | Căn cứ BD | Cách sửa |
|---|---|---|---|---|
| P1 | `00.Hướng dẫn!A4:B4`, `Cover!B19` | Inventory 44 file/không schema đã stale. | SQL `:1-31`; canonical `docs/BD/base/0. Study2Work_System_Architecture.md:632-700` | Cập nhật 48 file/schema/precedence. |
| P0 | `2.Response!D9:D11`, `2.Response!A35` | Envelope/error không canonical. | `docs/BD/base/0. Study2Work_System_Architecture.md:632-700` | Dùng canonical success/error. |
| P1 | `2.Response!A23`, `2.Response!C17:C20` | List pagination sai shape, dùng `page_size`, thiếu `totalPages`, request ID đặt trong meta. | `docs/BD/base/0. Study2Work_System_Architecture.md:652-721` | Dùng `data.items` + `meta.pagination`; `traceId` top-level. |
| P1 | `3.Data mapping!A20`, `00.Hướng dẫn!A13:B18` | SQL có `<FK condition>` và virtual column dù checklist đã tick không placeholder. | `docs/BD/base/0. Study2Work_System_Architecture.md:738-752`; SQL `:486-506` | Viết query/JOIN thực thi được. |
| P0 | `1.Request!D22:I23`, `3.Data mapping!F12` | `type/status` là free String; query dùng `exercises.status` thay vì `publish_status`, cùng `search_document/order_index/created_at` không tồn tại. | SQL `:134-141,486-506` | Dùng enum exercise type/publish status; bỏ hoặc migrate FTS/order/timestamp fields. |
| P0 | `2.Response!C16:H16`, `3.Data mapping!A20` | List chỉ trả `assignment: String` và SELECT cột `assignment` không tồn tại; không đủ ID/title/type/scope/status để dùng. | BD-10 `:123-135`; SQL `:486-506` | Định nghĩa exercise summary cụ thể và derive structured scope từ course/chapter/lesson IDs. |
| P1 | `4.Error!A13:H14` | `SUBMISSION_NOT_ALLOWED` và `REVIEW_ALREADY_FINALIZED` không thể phát sinh khi admin chỉ đọc danh sách. | Chức năng admin exercise BD-10 `:123-135` | Bỏ lỗi learner submission/review; giữ authn/RBAC/filter validation/system. |

## Checklist duyệt lại

- [ ] Source/envelope/list pagination đã sửa.
- [ ] Type/status có enum đúng.
- [ ] Query chỉ dùng cột thật.
- [ ] Exercise summary có schema cụ thể.
- [ ] Scope filter/response có semantics rõ.
- [ ] Không còn placeholder.
- [ ] Error catalog đúng API list.
- [ ] OpenAPI/test bao phủ filter scope và paging.

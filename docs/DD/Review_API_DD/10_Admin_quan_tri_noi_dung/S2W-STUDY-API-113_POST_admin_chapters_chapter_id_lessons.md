# Review API DD — S2W-STUDY-API-113

- DD source: `docs/DD/Study2Work_DD_API/10_Admin_quan_tri_noi_dung/S2W-STUDY-API-113_POST_admin_chapters_chapter_id_lessons.xlsx`
- Method + endpoint: `POST /api/v1/admin/chapters/{chapter_id}/lessons`
- Kết luận: **CẦN SỬA**

## Findings

| Severity | Sheet + cell | Mô tả cụ thể | Căn cứ BD | Cách sửa |
|---|---|---|---|---|
| P1 | `00.Hướng dẫn!A4:B4`, `Cover!B19` | Source 44 file/không schema đã stale; hiện có 48 file và SQL. | SQL `:1-31`; canonical `docs/BD/base/0. Study2Work_System_Architecture.md:632-700` | Cập nhật inventory/schema/precedence. |
| P0 | `2.Response!D9:D11`, `2.Response!A33` | Envelope/error không canonical. | `docs/BD/base/0. Study2Work_System_Architecture.md:632-700` | Chuyển sang canonical envelope. |
| P1 | `2.Response!A21` | Create response có pagination mẫu thừa và ví dụ `status: ACTIVE` thay vì lesson DRAFT. | Lifecycle BD-10 `:35-51`; canonical `docs/BD/base/0. Study2Work_System_Architecture.md:693-700` | Bỏ `meta`; trả `publishStatus: DRAFT`. |
| P1 | `3.Data mapping!A20`, `00.Hướng dẫn!A13:B18` | SQL `INSERT ... SET <mapping>` là placeholder/không hợp PostgreSQL dù checklist đã tick. | SQL `:1-25`; `docs/BD/base/0. Study2Work_System_Architecture.md:738-752` | Viết INSERT/RETURNING cụ thể. |
| P0 | `3.Data mapping!D14:E14`, `7.DB_Insert_Main!A6:I17` | Endpoint tạo lesson nhưng target main là `study.chapters`; không insert `chapter_id`. Đây là mapping sai bảng nghiêm trọng. | SQL `:446-470`; BD-10 `:98-110` | Target `lessons`, bắt buộc `chapter_id=:chapterId`; trả lesson ID/object. |
| P0 | `1.Request!D23:I29`, `7.DB_Insert_Main!B9:I17` | `description`, `objectives[]`, `content_blocks`, `video`, `completion_conditions[]`, `order`, `created_*` không khớp schema; schema có `objective`, `order_index`, `sample_public`, `completion_condition` enum, `publish_status`. | SQL `:106-113,458-470` | Map field thật; content/video cần model/material riêng; dùng một enum `completionCondition`; bổ sung migration nếu giữ blocks. |
| P1 | `4.Error!A13:H14` | Tạo lesson lại dùng `CONTENT_NOT_PUBLISHED` và `HIGH_RISK_REASON_REQUIRED` dù request không có reason; không có lỗi parent-not-found/order-conflict. | BD-10 `:91-110`; SQL `:458-470` | Dùng `CHAPTER_NOT_FOUND`, `PARENT_STATE_NOT_EDITABLE`, `ORDER_CONFLICT`; chỉ yêu cầu reason khi policy thực sự áp dụng. |

## Checklist duyệt lại

- [ ] Source/envelope/non-list meta đã sửa.
- [ ] Target là `lessons`, có `chapter_id`.
- [ ] New lesson trả `DRAFT`.
- [ ] Field/type/enum khớp schema hoặc migration.
- [ ] Content/video/resource model được chốt.
- [ ] Order allocation/concurrency/idempotency rõ.
- [ ] Error catalog đúng endpoint.
- [ ] OpenAPI/test bao phủ parent state, order conflict và retry.

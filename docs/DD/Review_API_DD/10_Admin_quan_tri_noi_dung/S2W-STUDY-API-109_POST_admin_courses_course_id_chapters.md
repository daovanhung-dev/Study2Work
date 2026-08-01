# Review API DD — S2W-STUDY-API-109

- DD source: `docs/DD/Study2Work_DD_API/10_Admin_quan_tri_noi_dung/S2W-STUDY-API-109_POST_admin_courses_course_id_chapters.xlsx`
- Method + endpoint: `POST /api/v1/admin/courses/{course_id}/chapters`
- Kết luận: **CẦN SỬA**
- Quy ước căn cứ: “BD-10”, “SEQ-11” và “SQL/schema” lần lượt là `docs/BD/10. Study2Work_Study_BasicDesign_Admin_Quan_Tri_Noi_Dung.md`, `docs/BD/diagram/SEQUENCE/11. Study2Work_Study_SEQ_Admin_Quan_Tri_Noi_Dung.md` và `docs/BD/diagram/CLASS/study2work_study_full_schema_seed.sql`; dải `:n-m` trong bảng là số dòng.

## Findings

| Severity | Sheet + cell | Mô tả cụ thể | Căn cứ BD | Cách sửa |
|---|---|---|---|---|
| P1 | `00.Hướng dẫn!A4:B4`, `Cover!B19` | DD ghi 44 nguồn/không có schema, nhưng hiện có 48 file và SQL schema. | `docs/BD/diagram/CLASS/study2work_study_full_schema_seed.sql:1-31`; `docs/BD/base/0. Study2Work_System_Architecture.md:632-700` | Cập nhật inventory/schema/precedence. |
| P0 | `2.Response!D9:D11`, `2.Response!A32` | Envelope `{data,meta}`/`{error}` không canonical. | `docs/BD/base/0. Study2Work_System_Architecture.md:632-700` | Chuyển sang canonical envelope và camelCase. |
| P1 | `2.Response!A21` | Create response chứa pagination mẫu thừa. | `docs/BD/base/0. Study2Work_System_Architecture.md:693-700` | Bỏ `meta`; trả chapter vừa tạo và `traceId`. |
| P1 | `3.Data mapping!A20`, `00.Hướng dẫn!A13:B18` | `INSERT ... SET <mapping>` và điều kiện placeholder chưa thực thi được, trái checklist đã tick. | SQL target PostgreSQL `:1-25`; contract `docs/BD/base/0. Study2Work_System_Architecture.md:738-752` | Viết INSERT PostgreSQL + lock/allocation order cụ thể. |
| P0 | `3.Data mapping!D14:E14`, `7.DB_Insert_Main!A6:I15` | Endpoint tạo chapter nhưng target/main mapping là `study.courses`; không insert `course_id`. Nếu triển khai sẽ ghi nhầm bảng cha. | SQL `:361-374,446-456`; BD-10 `:87-97` | Target `chapters`; insert bắt buộc `course_id=:courseId`, `title`, `objective`, `order_index`, `required`, `unlock_condition`. |
| P0 | `1.Request!D23:I27`, `7.DB_Insert_Main!B9:I13` | DD dùng `objectives[]`, `estimated_duration`, `unlock_conditions[]`, `completion_conditions[]`, `order`; schema dùng `objective TEXT`, `unlock_condition ENUM`, `order_index` và không có duration/completion column. | SQL `:99-113,446-456` | Sửa kiểu/tên theo schema; completion chapter cần quyết định/migration riêng vì schema `completion_rules` hiện chỉ cho PATH/COURSE. |
| P1 | `1.Request!D27:I27`, `3.Data mapping!G14` | `order` optional nhưng không định nghĩa server append hay insert-and-shift; unique `(course_id,order_index)` dễ race. | SQL `:454-456`; reorder rule BD-10 `:136-145` | Chốt semantics; lock course siblings, tính/order shift atomically và trả conflict khi stale. |

## Checklist duyệt lại

- [ ] Source/envelope/non-list meta đã sửa.
- [ ] Main target là `chapters`, có `course_id`.
- [ ] Field/type/enum khớp schema.
- [ ] Completion chapter có data model được phê duyệt.
- [ ] Order append/insert semantics rõ.
- [ ] Lock/unique conflict/idempotency được xử lý.
- [ ] SQL không còn placeholder.
- [ ] OpenAPI/test bao phủ foreign course, duplicate order và retry.

# Review API DD — S2W-STUDY-API-106

- DD source: `docs/DD/Study2Work_DD_API/10_Admin_quan_tri_noi_dung/S2W-STUDY-API-106_PUT_admin_courses_course_id_chapters_order.xlsx`
- Method + endpoint: `PUT /api/v1/admin/courses/{course_id}/chapters/order`
- Kết luận: **CẦN SỬA**
- Quy ước căn cứ: “BD-10”, “SEQ-11” và “SQL/schema” lần lượt là `docs/BD/10. Study2Work_Study_BasicDesign_Admin_Quan_Tri_Noi_Dung.md`, `docs/BD/diagram/SEQUENCE/11. Study2Work_Study_SEQ_Admin_Quan_Tri_Noi_Dung.md` và `docs/BD/diagram/CLASS/study2work_study_full_schema_seed.sql`; dải `:n-m` trong bảng là số dòng.

## Findings

| Severity | Sheet + cell | Mô tả cụ thể | Căn cứ BD | Cách sửa |
|---|---|---|---|---|
| P1 | `00.Hướng dẫn!A4:B4`, `Cover!B19` | Nguồn 44 file/không schema đã stale. | SQL `:1-31`; canonical `docs/BD/base/0. Study2Work_System_Architecture.md:632-700` | Cập nhật inventory/preference. |
| P0 | `2.Response!D9:D11`, `2.Response!A33` | Envelope/error cũ trái canonical. | `docs/BD/base/0. Study2Work_System_Architecture.md:632-700` | Dùng canonical response. |
| P1 | `2.Response!A22` | Non-list mutation có pagination mẫu thừa. | `docs/BD/base/0. Study2Work_System_Architecture.md:693-700` | Bỏ pagination/meta rỗng. |
| P1 | `3.Data mapping!A20`, `00.Hướng dẫn!A13:B18` | UPDATE `<mapping>` không xác định thuật toán reorder nhưng checklist đã tick. | `docs/BD/base/0. Study2Work_System_Architecture.md:601-628,738-752` | Mô tả lock course+chapters và batch update cụ thể. |
| P0 | `1.Request!D22:I22` | `chapter_ids_in_order` chỉ là Array chung, min 0; không khai item UUID, uniqueness, phải chứa toàn bộ chapter hay cho phép subset. | BD-10 `:80,92,140-145`; SQL `:446-456` | Dùng `chapterIdsInOrder: UUID[]`, min 1 (trừ khi course rỗng), unique, tất cả phải thuộc course; chốt full-replace hay partial. |
| P0 | `3.Data mapping!D14:E14`, `5.DB_Update_Main!B8:I10` | DD cập nhật JSON `courses.chapter_ids_in_order`, trong khi thứ tự nằm ở `chapters.order_index`; `courses.updated_*` cũng không tồn tại. | SQL `:361-374,446-456` | Update từng `chapters.order_index` trong transaction; không ghi JSON vào course. |
| P0 | `3.Data mapping!G14`, `2.Response!C17:C18` | Unique `(course_id,order_index)` có thể làm batch reorder lỗi do collision tạm thời; impact/audit chỉ là placeholder và không cảnh báo learner cụ thể. | SQL `:454-456`; BD-10 `:136-145,177-182` | Dùng two-phase temporary indices hoặc deferrable constraint/migration; tính impact, audit before/after order, test swap/race. |

## Checklist duyệt lại

- [ ] Source/envelope/non-list meta đã sửa.
- [ ] Array item UUID, unique và ownership được validate.
- [ ] Full/partial reorder semantics được chốt.
- [ ] Update `chapters.order_index`, không ghi JSON.
- [ ] Thuật toán tránh unique collision được mô tả.
- [ ] Lock/concurrency/rollback đảm bảo atomic.
- [ ] Impact/audit cho course published có thật.
- [ ] OpenAPI/test bao phủ missing/duplicate/foreign chapter và swap.

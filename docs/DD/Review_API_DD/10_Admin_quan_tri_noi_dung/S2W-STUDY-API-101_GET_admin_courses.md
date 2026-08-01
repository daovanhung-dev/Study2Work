# Review API DD — S2W-STUDY-API-101

- DD source: `docs/DD/Study2Work_DD_API/10_Admin_quan_tri_noi_dung/S2W-STUDY-API-101_GET_admin_courses.xlsx`
- Method + endpoint: `GET /api/v1/admin/courses`
- Kết luận: **CẦN SỬA**
- Quy ước căn cứ: “BD-10”, “SEQ-11” và “SQL/schema” lần lượt là `docs/BD/10. Study2Work_Study_BasicDesign_Admin_Quan_Tri_Noi_Dung.md`, `docs/BD/diagram/SEQUENCE/11. Study2Work_Study_SEQ_Admin_Quan_Tri_Noi_Dung.md` và `docs/BD/diagram/CLASS/study2work_study_full_schema_seed.sql`; dải `:n-m` trong bảng là số dòng.

## Findings

| Severity | Sheet + cell | Mô tả cụ thể | Căn cứ BD | Cách sửa |
|---|---|---|---|---|
| P1 | `00.Hướng dẫn!A4:B4`, `Cover!B19` | DD dùng inventory 44 file và nói chưa có schema, nhưng `docs/BD` có 48 file và SQL schema. | `docs/BD/diagram/CLASS/study2work_study_full_schema_seed.sql:1-31`; canonical `docs/BD/base/0. Study2Work_System_Architecture.md:632-700` | Cập nhật inventory, schema và thứ tự ưu tiên nguồn. |
| P0 | `2.Response!D9:D11`, `2.Response!A35` | Envelope `{data,meta}`/`{error}` và snake_case không canonical. | `docs/BD/base/0. Study2Work_System_Architecture.md:632-700` | Dùng `success/businessCode/message/data|errors/traceId`. |
| P1 | `2.Response!A26`, `2.Response!C20:C23` | List pagination sai shape: đặt thẳng trong `meta`, dùng `page_size`, thiếu `totalPages`, và trộn request ID vào meta. | `docs/BD/base/0. Study2Work_System_Architecture.md:652-721` | Trả `data.items` + `meta.pagination.{page,pageSize,total,totalPages}`. |
| P1 | `3.Data mapping!A20`, `00.Hướng dẫn!A13:B18` | SQL có `<FK condition>` và virtual columns nhưng checklist tự tick không còn placeholder. | `docs/BD/base/0. Study2Work_System_Architecture.md:693-700,738-752`; SQL `:361-456` | Viết JOIN/aggregate PostgreSQL cụ thể và chỉ tick sau review thực tế. |
| P0 | `3.Data mapping!F12`, `3.Data mapping!A20` | Query dùng `courses.status`, `courses.learning_path_id`, `search_document`, `order_index`, `created_at`; bảng `courses` chỉ có `publish_status`, không có FK trực tiếp đến path hay các cột sort/FTS đó. | SQL `:361-385` | Filter `publishStatus`; join `learning_path_courses` cho `pathId`; thêm migration/index nếu thực sự cần FTS/sort khác. |
| P0 | `2.Response!C16:H19` | `admin`, `path_count`, `chapter_count`, `learner_impact_count` bị khai như cột `courses`; các count sai kiểu `String`. | SQL `:361-456`; impact rule BD-10 `:159-167,180-181` | Trả course summary thực; count là integer tính qua relation/enrollment với query và semantics rõ. |
| P1 | `4.Error!A13:H14` | `SUBMISSION_NOT_ALLOWED`/`REVIEW_ALREADY_FINALIZED` (hoặc nhóm lỗi learner tương đương trong template) không thuộc API admin list course. | Chức năng course BD-10 `:72-85` | Chỉ giữ authn/RBAC/filter validation/system; bỏ lỗi bài nộp/learner không thể phát sinh. |

## Checklist duyệt lại

- [ ] Source inventory và canonical envelope đã sửa.
- [ ] List dùng `data.items` + `meta.pagination`.
- [ ] Filter dùng enum/cột thật và join path qua relation.
- [ ] Summary/count có kiểu và công thức rõ.
- [ ] SQL không placeholder/virtual column.
- [ ] Error catalog đúng endpoint.
- [ ] Permission được map tới RBAC vật lý.
- [ ] OpenAPI/test bao phủ paging, filter kết hợp và aggregate.

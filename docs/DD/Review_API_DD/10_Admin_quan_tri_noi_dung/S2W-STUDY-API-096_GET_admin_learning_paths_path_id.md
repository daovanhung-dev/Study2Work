# Review API DD — S2W-STUDY-API-096

- DD source: `docs/DD/Study2Work_DD_API/10_Admin_quan_tri_noi_dung/S2W-STUDY-API-096_GET_admin_learning_paths_path_id.xlsx`
- Method + endpoint: `GET /api/v1/admin/learning-paths/{path_id}`
- Kết luận: **CẦN SỬA**
- Quy ước căn cứ: “BD-10”, “SEQ-11” và “SQL/schema” lần lượt là `docs/BD/10. Study2Work_Study_BasicDesign_Admin_Quan_Tri_Noi_Dung.md`, `docs/BD/diagram/SEQUENCE/11. Study2Work_Study_SEQ_Admin_Quan_Tri_Noi_Dung.md` và `docs/BD/diagram/CLASS/study2work_study_full_schema_seed.sql`; dải `:n-m` trong bảng là số dòng.

## Findings

| Severity | Sheet + cell | Mô tả cụ thể | Căn cứ BD | Cách sửa |
|---|---|---|---|---|
| P1 | `00.Hướng dẫn!A4:B4`, `Cover!B19` | Inventory 44 file và tuyên bố thiếu schema không còn đúng; `docs/BD` có 48 file và SQL. | SQL `:1-31`; canonical source `docs/BD/base/0. Study2Work_System_Architecture.md:632-700` | Cập nhật nguồn và precedence. |
| P0 | `2.Response!D9:D11`, `2.Response!A37` | Envelope/error mẫu không canonical. | `docs/BD/base/0. Study2Work_System_Architecture.md:632-700` | Dùng canonical success/error và `traceId`. |
| P1 | `2.Response!A25` | Detail response không phải list nhưng vẫn chứa `meta.page/page_size`; pagination hoàn toàn thừa. | `docs/BD/base/0. Study2Work_System_Architecture.md:693-700` | Bỏ `meta`; chỉ để `traceId` top-level. |
| P1 | `3.Data mapping!A20`, `00.Hướng dẫn!A13:B18` | SQL dùng `<FK condition>` và các “cột” tổng hợp chưa tồn tại, trái checkbox “không placeholder”. | `docs/BD/base/0. Study2Work_System_Architecture.md:693-700,738-752`; SQL `:323-385` | Viết query cụ thể theo `learning_paths.id` và các relation; cập nhật checklist trung thực. |
| P0 | `2.Response!C16:H21` | Các field `full`, `courses`, `lifecycle`, `validation_summary`, `impact_summary`, `audit_summary` chỉ có kiểu String/Array chung chung và bị gán như cột `learning_paths`; contract không xác định cấu trúc. | Cấu trúc lộ trình BD-10 `:57-70`; schema `:323-385,691-719` | Định nghĩa object lộ trình và nested course/validation/impact/audit summary với field, enum, nullability cụ thể. |
| P0 | `3.Data mapping!F12`, `3.Data mapping!A20` | WHERE dùng `learning_paths.learning_path_id`, nhưng khóa chính là `learning_paths.id`; SELECT các cột `full/lifecycle/...` không tồn tại. | SQL `:323-338` | Dùng `lp.id=:pathId`; JOIN `learning_path_courses`, `courses`, aggregate impact/audit bằng query/view rõ ràng. |
| P1 | `4.Error!A14:H17` | Error onboarding/active-path/published-path của learner không liên quan việc admin đọc chi tiết mọi trạng thái. | BD-10 `:24-31,57-70` | Bỏ error không thể phát sinh; thêm `RESOURCE_NOT_FOUND` và permission scope đúng. |

## Checklist duyệt lại

- [ ] Nguồn 48 file và schema SQL được ghi nhận.
- [ ] Envelope canonical; detail response không có pagination.
- [ ] Response object có schema cụ thể, không dùng “full” String.
- [ ] WHERE dùng `learning_paths.id`.
- [ ] JOIN course, impact, audit có nguồn và aggregate rõ.
- [ ] Không còn placeholder/virtual column.
- [ ] Error catalog đúng ngữ cảnh admin.
- [ ] OpenAPI/test bao phủ not-found, RBAC và dữ liệu mọi lifecycle.

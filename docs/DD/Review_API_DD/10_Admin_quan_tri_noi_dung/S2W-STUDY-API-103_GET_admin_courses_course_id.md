# Review API DD — S2W-STUDY-API-103

- DD source: `docs/DD/Study2Work_DD_API/10_Admin_quan_tri_noi_dung/S2W-STUDY-API-103_GET_admin_courses_course_id.xlsx`
- Method + endpoint: `GET /api/v1/admin/courses/{course_id}`
- Kết luận: **CẦN SỬA**
- Quy ước căn cứ: “BD-10”, “SEQ-11” và “SQL/schema” lần lượt là `docs/BD/10. Study2Work_Study_BasicDesign_Admin_Quan_Tri_Noi_Dung.md`, `docs/BD/diagram/SEQUENCE/11. Study2Work_Study_SEQ_Admin_Quan_Tri_Noi_Dung.md` và `docs/BD/diagram/CLASS/study2work_study_full_schema_seed.sql`; dải `:n-m` trong bảng là số dòng.

## Findings

| Severity | Sheet + cell | Mô tả cụ thể | Căn cứ BD | Cách sửa |
|---|---|---|---|---|
| P1 | `00.Hướng dẫn!A4:B4`, `Cover!B19` | Inventory nguồn 44 file/không schema đã lỗi thời. | SQL `:1-31`; canonical `docs/BD/base/0. Study2Work_System_Architecture.md:632-700` | Ghi nhận đủ 48 file, SQL và precedence. |
| P0 | `2.Response!D9:D11`, `2.Response!A38` | Envelope/error mẫu không canonical. | `docs/BD/base/0. Study2Work_System_Architecture.md:632-700` | Dùng canonical envelope và `traceId`. |
| P1 | `2.Response!A26` | Detail response có `meta.page/page_size`; pagination mẫu thừa. | `docs/BD/base/0. Study2Work_System_Architecture.md:693-700` | Bỏ `meta` khỏi non-list response. |
| P1 | `3.Data mapping!A20`, `00.Hướng dẫn!A13:B18` | SELECT có `<FK condition>` và virtual columns mặc dù checklist nói không còn placeholder. | `docs/BD/base/0. Study2Work_System_Architecture.md:738-752`; SQL `:361-470` | Viết query cụ thể từ course→chapters→lessons và path relation. |
| P0 | `3.Data mapping!F12`, `3.Data mapping!A20` | WHERE dùng `courses.course_id`; PK thật là `courses.id`. SELECT `full/lifecycle/validation/impact` như cột vật lý không tồn tại. | SQL `:361-374` | Dùng `c.id=:courseId`; map core columns và aggregate riêng. |
| P0 | `2.Response!C16:H22` | `full`, `lifecycle`, `impact` là String mơ hồ; chapters/paths/sample lessons không có item schema, nên frontend không thể code an toàn. | BD-10 `:72-85,159-167`; SQL `:376-470` | Định nghĩa nested DTO cụ thể, enum lifecycle, structured impact/validation và source từng field. |
| P1 | `3.Data mapping!D12:G12` | Không mô tả query `sample_lessons` theo `lessons.sample_public`, cũng không kiểm tra sample scope/resource public. | BD-10 `:82,108,157,179`; SQL `:458-480` | Query `sample_public=true`; trả cấu hình public tối thiểu và không lộ raw private resource URL. |

## Checklist duyệt lại

- [ ] Source/envelope/non-list meta đã sửa.
- [ ] WHERE dùng `courses.id`.
- [ ] Core/nested response có schema cụ thể.
- [ ] Chapters/path/sample lessons dùng JOIN thật.
- [ ] Lifecycle/impact có enum và công thức.
- [ ] Sample lesson không lộ tài nguyên riêng tư.
- [ ] Không còn placeholder/virtual columns.
- [ ] OpenAPI/test bao phủ not-found, RBAC và full graph.

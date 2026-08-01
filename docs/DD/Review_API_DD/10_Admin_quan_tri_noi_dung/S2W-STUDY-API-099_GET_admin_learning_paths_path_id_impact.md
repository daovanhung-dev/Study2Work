# Review API DD — S2W-STUDY-API-099

- DD source: `docs/DD/Study2Work_DD_API/10_Admin_quan_tri_noi_dung/S2W-STUDY-API-099_GET_admin_learning_paths_path_id_impact.xlsx`
- Method + endpoint: `GET /api/v1/admin/learning-paths/{path_id}/impact`
- Kết luận: **CẦN SỬA**
- Quy ước căn cứ: “BD-10”, “SEQ-11” và “SQL/schema” lần lượt là `docs/BD/10. Study2Work_Study_BasicDesign_Admin_Quan_Tri_Noi_Dung.md`, `docs/BD/diagram/SEQUENCE/11. Study2Work_Study_SEQ_Admin_Quan_Tri_Noi_Dung.md` và `docs/BD/diagram/CLASS/study2work_study_full_schema_seed.sql`; dải `:n-m` trong bảng là số dòng.

## Findings

| Severity | Sheet + cell | Mô tả cụ thể | Căn cứ BD | Cách sửa |
|---|---|---|---|---|
| P1 | `00.Hướng dẫn!A4:B4`, `Cover!B19` | Nguồn 44 file/không schema đã stale so với 48 file và SQL. | SQL `:1-31`; `docs/BD/base/0. Study2Work_System_Architecture.md:632-700` | Cập nhật inventory và precedence. |
| P0 | `2.Response!D9:D11`, `2.Response!A36` | Envelope/error không canonical. | `docs/BD/base/0. Study2Work_System_Architecture.md:632-700` | Chuyển sang canonical envelope/camelCase. |
| P1 | `2.Response!A24` | Impact detail không phải list nhưng có pagination mẫu `page/page_size`. | `docs/BD/base/0. Study2Work_System_Architecture.md:693-700` | Bỏ `meta`; dùng `traceId` top-level. |
| P1 | `3.Data mapping!A20`, `00.Hướng dẫn!A13:B18` | SELECT dùng `<FK condition>` và “cột” tổng hợp chưa định nghĩa dù checklist đánh dấu không placeholder. | `docs/BD/base/0. Study2Work_System_Architecture.md:738-752`; SQL `:376-437` | Viết CTE/JOIN/aggregate cụ thể và test đối soát counts. |
| P0 | `1.Request!D22:I22`, `3.Data mapping!F12` | `proposed_change_type` là free String rồi bị lọc như cột `learning_paths.proposed_change_type`, cột này không tồn tại; impact phải được tính từ giả định thay đổi, không phải filter DB. | BD-10 `:159-167`; SQL `:323-338` | Chốt enum `changeType` và schema chi tiết của proposed change, hoặc bỏ query param và trả current-impact thuần. |
| P0 | `2.Response!C16:H20` | `active_learners`, `completed_learners`, `related_courses`, `notification_recommended` đều khai String và như cột vật lý; count/boolean/list sai kiểu. | BD-10 `:159-167`; SQL `:376-437` | Dùng integer counts, boolean/enum recommendation, structured risk summary và course list; mô tả công thức/denominator. |
| P1 | `3.Data mapping!D12:G12` | Mapping không chỉ ra cách tránh double-count khi join path-course-course enrollment, không nêu trạng thái nào là active/completed hay snapshot time. | SQL `:387-437`; rule impact BD-10 `:163-167` | Aggregate từng nguồn trước khi join, dùng `COUNT(DISTINCT enrollment.id)`, định nghĩa status/time boundary và consistency level. |

## Checklist duyệt lại

- [ ] Source/envelope/pagination đã sửa.
- [ ] `changeType` có enum và semantics rõ hoặc được loại bỏ.
- [ ] Mọi count/boolean/list có kiểu đúng.
- [ ] Công thức active/completed/risk được định nghĩa.
- [ ] Query không dùng cột ảo và không double-count.
- [ ] Recommendation notification/versioning có rule quyết định.
- [ ] Permission và privacy của aggregate được xác nhận.
- [ ] OpenAPI/test đối soát số liệu và trường hợp không có enrollment.

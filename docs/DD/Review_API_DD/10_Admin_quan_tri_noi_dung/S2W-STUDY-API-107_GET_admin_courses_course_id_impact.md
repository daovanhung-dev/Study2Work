# Review API DD — S2W-STUDY-API-107

- DD source: `docs/DD/Study2Work_DD_API/10_Admin_quan_tri_noi_dung/S2W-STUDY-API-107_GET_admin_courses_course_id_impact.xlsx`
- Method + endpoint: `GET /api/v1/admin/courses/{course_id}/impact`
- Kết luận: **CẦN SỬA**
- Quy ước căn cứ: “BD-10”, “SEQ-11” và “SQL/schema” lần lượt là `docs/BD/10. Study2Work_Study_BasicDesign_Admin_Quan_Tri_Noi_Dung.md`, `docs/BD/diagram/SEQUENCE/11. Study2Work_Study_SEQ_Admin_Quan_Tri_Noi_Dung.md` và `docs/BD/diagram/CLASS/study2work_study_full_schema_seed.sql`; dải `:n-m` trong bảng là số dòng.

## Findings

| Severity | Sheet + cell | Mô tả cụ thể | Căn cứ BD | Cách sửa |
|---|---|---|---|---|
| P1 | `00.Hướng dẫn!A4:B4`, `Cover!B19` | Source inventory 44 file/không schema đã stale. | SQL `:1-31`; `docs/BD/base/0. Study2Work_System_Architecture.md:632-700` | Cập nhật 48 file/schema/precedence. |
| P0 | `2.Response!D9:D11`, `2.Response!A36` | Envelope/error không canonical. | `docs/BD/base/0. Study2Work_System_Architecture.md:632-700` | Dùng canonical envelope/camelCase. |
| P1 | `2.Response!A24` | Impact detail có pagination mẫu thừa. | `docs/BD/base/0. Study2Work_System_Architecture.md:693-700` | Bỏ `meta`; `traceId` top-level. |
| P1 | `3.Data mapping!A20`, `00.Hướng dẫn!A13:B18` | SELECT có `<FK condition>`/virtual columns dù checklist nói không placeholder. | `docs/BD/base/0. Study2Work_System_Architecture.md:738-752`; SQL `:376-437` | Viết CTE/JOIN aggregate thực thi được. |
| P0 | `1.Request!A20:A24`, `2.Response!C19:C20` | API không nhận loại/thay đổi dự kiến, nên không thể kết luận `progress_risk_summary` hay `versioning_recommended` theo thay đổi cụ thể. | BD-10 `:159-167` | Hoặc định nghĩa đây là current exposure thuần, hoặc nhận `changeType` + structured proposed change để mô phỏng impact. |
| P0 | `2.Response!C16:H20` | `active_learners`, `completed_learners`, `versioning_recommended` đều là String; related paths không có item schema; tất cả bị map như cột `courses`. | BD-10 `:163-167,180`; SQL `:376-437` | Dùng integer counts, boolean/enum recommendation, structured paths/risk; ghi công thức và snapshot time. |
| P1 | `3.Data mapping!D12:G12` | Không chỉ ra cách join `course_enrollments` với path context và tránh double-count course nằm trong nhiều path. | SQL `:376-437`; ADM-CONT-06 tại BD-10 `:180` | Aggregate theo enrollment ID/context trước; trả breakdown theo path và tổng `COUNT(DISTINCT ...)`. |

## Checklist duyệt lại

- [ ] Source/envelope/non-list meta đã sửa.
- [ ] Current-impact hay proposed-change semantics được chốt.
- [ ] Count/boolean/list có kiểu chuẩn.
- [ ] Query không double-count multi-path enrollment.
- [ ] Risk/version recommendation có rule.
- [ ] Snapshot time/consistency được mô tả.
- [ ] Aggregate không lộ PII.
- [ ] OpenAPI/test đối soát course ở nhiều path.

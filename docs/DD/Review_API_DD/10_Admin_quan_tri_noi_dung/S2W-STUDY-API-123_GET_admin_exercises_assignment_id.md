# Review API DD — S2W-STUDY-API-123

- DD source: `docs/DD/Study2Work_DD_API/10_Admin_quan_tri_noi_dung/S2W-STUDY-API-123_GET_admin_exercises_assignment_id.xlsx`
- Method + endpoint: `GET /api/v1/admin/exercises/{assignment_id}`
- Kết luận: **CẦN SỬA**

## Findings

| Severity | Sheet + cell | Mô tả cụ thể | Căn cứ BD | Cách sửa |
|---|---|---|---|---|
| P1 | `00.Hướng dẫn!A4:B4`, `Cover!B19` | Inventory 44 file/không schema đã stale. | SQL `:1-31`; canonical `docs/BD/base/0. Study2Work_System_Architecture.md:632-700` | Cập nhật source inventory/precedence. |
| P0 | `2.Response!D9:D11`, `2.Response!A36` | Envelope/error không canonical. | `docs/BD/base/0. Study2Work_System_Architecture.md:632-700` | Dùng canonical response. |
| P1 | `2.Response!A24` | Detail response có pagination mẫu thừa. | `docs/BD/base/0. Study2Work_System_Architecture.md:693-700` | Bỏ `meta`. |
| P1 | `3.Data mapping!A20`, `00.Hướng dẫn!A13:B18` | SELECT có `<FK condition>` và virtual fields, trái checklist. | `docs/BD/base/0. Study2Work_System_Architecture.md:738-752`; SQL `:486-537` | Viết JOIN/aggregate cụ thể. |
| P0 | `3.Data mapping!F12`, `3.Data mapping!A20` | WHERE dùng `exercises.exercise_id`; PK thật là `exercises.id`. SELECT `full/linkage/lifecycle/impact` như cột vật lý không tồn tại. | SQL `:486-506` | Dùng `e.id=:assignmentId`; map core exercise columns và aggregate submissions riêng. |
| P0 | `2.Response!C16:H20` | `full`, submissions summary, lifecycle, impact đều là String; `linkage` bị khai URI dù linkage thực là course/chapter/lesson IDs. | BD-10 `:123-135`; SQL `:486-529` | Trả structured exercise config, scope object, publishStatus enum và typed submission counts/impact. |
| P1 | `2.Response!C16:H18`, `1.Request!D21:I21` | Contract không nói rõ quyền field-level đối với quiz answers/rubric; generic `study.content.manage` có thể làm lộ answer key cho role chỉ cần xem metadata. | Vai trò BD-10 `:24-31`; nội dung đáp án/rubric `:131-132` | Tách permission xem/edit answer key hoặc redaction theo permission; audit truy cập nhạy cảm nếu cần. |

## Checklist duyệt lại

- [ ] Source/envelope/non-list meta đã sửa.
- [ ] WHERE dùng `exercises.id`.
- [ ] Response DTO structured, không `full` String.
- [ ] Scope là object FK, không URI.
- [ ] Submission summary/impact có kiểu và query.
- [ ] Answer/rubric có field-level permission/redaction.
- [ ] Không còn placeholder/virtual columns.
- [ ] OpenAPI/test not-found, RBAC và answer-key redaction.

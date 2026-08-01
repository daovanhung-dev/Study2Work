# Review API DD — S2W-STUDY-API-104

- DD source: `docs/DD/Study2Work_DD_API/10_Admin_quan_tri_noi_dung/S2W-STUDY-API-104_PATCH_admin_courses_course_id.xlsx`
- Method + endpoint: `PATCH /api/v1/admin/courses/{course_id}`
- Kết luận: **CẦN SỬA**
- Quy ước căn cứ: “BD-10”, “SEQ-11” và “SQL/schema” lần lượt là `docs/BD/10. Study2Work_Study_BasicDesign_Admin_Quan_Tri_Noi_Dung.md`, `docs/BD/diagram/SEQUENCE/11. Study2Work_Study_SEQ_Admin_Quan_Tri_Noi_Dung.md` và `docs/BD/diagram/CLASS/study2work_study_full_schema_seed.sql`; dải `:n-m` trong bảng là số dòng.

## Findings

| Severity | Sheet + cell | Mô tả cụ thể | Căn cứ BD | Cách sửa |
|---|---|---|---|---|
| P1 | `00.Hướng dẫn!A4:B4`, `Cover!B19` | Nguồn 44 file/không schema đã stale. | SQL `:1-31`; canonical `docs/BD/base/0. Study2Work_System_Architecture.md:632-700` | Cập nhật 48 file, schema và precedence. |
| P0 | `2.Response!D9:D11`, `2.Response!A35` | Envelope/error cũ trái canonical. | `docs/BD/base/0. Study2Work_System_Architecture.md:632-700` | Dùng canonical envelope/camelCase. |
| P1 | `2.Response!A23` | Mutation response có pagination mẫu thừa. | `docs/BD/base/0. Study2Work_System_Architecture.md:693-700` | Bỏ `meta`; trả `traceId` top-level. |
| P1 | `3.Data mapping!A20`, `00.Hướng dẫn!A13:B18` | UPDATE còn `<mapping>` và điều kiện tiếng Việt, trái checklist “không placeholder”. | `docs/BD/base/0. Study2Work_System_Architecture.md:738-752` | Đặc tả field-by-field UPDATE và version predicate. |
| P0 | `1.Request!D22:F22`, `5.DB_Update_Main!B8:I10` | PATCH chỉ có `reason`; không nhận title/description/level/duration/goals/prerequisites/completion/community như chính Overview mô tả. Sau đó lại ghi `reason`, `updated_at`, `updated_by` vào các cột không tồn tại ở `courses`. | BD-10 `:72-85`; SQL `:361-374` | Thêm các field patchable có kiểu/enum; map core columns, relations/completion rule; reason lưu trong audit. |
| P0 | `1.Request!B11`, `3.Data mapping!E13:G14` | Tuyên bố idempotent theo resource/version nhưng request/bảng không có version, nên lost update chưa được giải quyết. | Transaction `docs/BD/base/0. Study2Work_System_Architecture.md:601-628`; SQL `:361-374` | Thêm ETag/version hoặc row lock + explicit state predicate; trả conflict khi stale. |
| P0 | `2.Response!C16:H19`, `3.Data mapping!C15:H15` | Impact warning/audit chỉ là field ảo; không có phân loại minor/important, learner count hay notify rule khi sửa course đã publish. | BD-10 `:159-167,177-182`; SEQ-11 `:28-35` | Tính impact qua course/path enrollments, yêu cầu changeType/reason, audit before/after và outbox notification cho important update. |

## Checklist duyệt lại

- [ ] Source/envelope/pagination đã chuẩn hóa.
- [ ] PATCH có field nghiệp vụ thực, không chỉ `reason`.
- [ ] Mapping dùng cột/relations đúng.
- [ ] Empty patch và immutable fields được từ chối.
- [ ] Có ETag/version/lock chống lost update.
- [ ] Minor/important impact rule được định nghĩa.
- [ ] Audit/reason/notification atomic và dedupe.
- [ ] OpenAPI/test bao phủ published-course update và race.

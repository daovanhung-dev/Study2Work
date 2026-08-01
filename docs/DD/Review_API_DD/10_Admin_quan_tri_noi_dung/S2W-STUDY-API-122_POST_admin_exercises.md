# Review API DD — S2W-STUDY-API-122

- DD source: `docs/DD/Study2Work_DD_API/10_Admin_quan_tri_noi_dung/S2W-STUDY-API-122_POST_admin_exercises.xlsx`
- Method + endpoint: `POST /api/v1/admin/exercises`
- Kết luận: **CẦN SỬA**

## Findings

| Severity | Sheet + cell | Mô tả cụ thể | Căn cứ BD | Cách sửa |
|---|---|---|---|---|
| P1 | `00.Hướng dẫn!A4:B4`, `Cover!B19` | Source 44 file/không schema đã stale. | SQL `:1-31`; `docs/BD/base/0. Study2Work_System_Architecture.md:632-700` | Cập nhật inventory/schema. |
| P0 | `2.Response!D9:D11`, `2.Response!A34` | Envelope/error cũ trái canonical. | `docs/BD/base/0. Study2Work_System_Architecture.md:632-700` | Dùng canonical envelope/camelCase. |
| P1 | `2.Response!A22` | Create response có pagination mẫu thừa và ví dụ `status: ACTIVE` thay vì DRAFT. | Lifecycle BD-10 `:35-51`; canonical `docs/BD/base/0. Study2Work_System_Architecture.md:693-700` | Bỏ `meta`; trả `publishStatus: DRAFT`. |
| P1 | `3.Data mapping!A20`, `00.Hướng dẫn!A13:B18` | `INSERT ... SET <mapping>` còn placeholder/không hợp PostgreSQL dù checklist đã tick. | SQL `:1-25`; `docs/BD/base/0. Study2Work_System_Architecture.md:738-752` | Viết INSERT/RETURNING cụ thể. |
| P0 | `1.Request!D22:I23`, `7.DB_Insert_Main!B9:I10` | `type`/`scope` là free String. Schema cần enum type và các FK `course_id/chapter_id/lesson_id`; DD lưu một cột `scope` text nên không tạo được liên kết. | SQL `:134-141,486-505`; BD-10 `:123-135` | Dùng structured/discriminated scope và map FK; validate hierarchy consistency và exactly-one/approved multi-anchor semantics. |
| P0 | `1.Request!D24:I36`, `7.DB_Insert_Main!B11:I25` | Phần lớn field (`objectives`, requirements, criteria, hints, resources, submission methods, quiz answers, created_*) không có trong schema; `max_score` cho phép 0 nhưng DB bắt `>0`. | SQL `:486-500` | Thu hẹp DTO theo schema hoặc bổ sung normalized/config schema; đặt `maxScore >=1`; conditional validation theo exercise type. |
| P0 | `3.Data mapping!C13:G15`, `4.Error!A13:H15` | Không kiểm tra rubric/quiz answer/submission method tương thích type; error lại là lỗi learner submit/review, không phải create. Idempotency chỉ “khuyến nghị”. | BD-10 `:127-134`; idempotency pattern `docs/BD/base/0. Study2Work_System_Architecture.md:723-736` | Thêm validation/error codes create-specific; bảo vệ answer data; đặc tả idempotency storage/hash/replay. |

## Checklist duyệt lại

- [ ] Source/envelope/pagination/status DRAFT đã sửa.
- [ ] Type và scope là enum/object có FK rõ.
- [ ] Scope hierarchy/exactly-one invariant được chốt.
- [ ] Field mở rộng có schema được duyệt.
- [ ] `maxScore >= 1` và conditional validation đúng type.
- [ ] SQL PostgreSQL không placeholder.
- [ ] Idempotency/audit được đặc tả.
- [ ] OpenAPI/test bao phủ từng exercise type, invalid scope và retry.

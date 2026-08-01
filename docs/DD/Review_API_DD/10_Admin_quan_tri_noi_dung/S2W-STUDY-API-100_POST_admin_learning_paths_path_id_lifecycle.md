# Review API DD — S2W-STUDY-API-100

- DD source: `docs/DD/Study2Work_DD_API/10_Admin_quan_tri_noi_dung/S2W-STUDY-API-100_POST_admin_learning_paths_path_id_lifecycle.xlsx`
- Method + endpoint: `POST /api/v1/admin/learning-paths/{path_id}/lifecycle`
- Kết luận: **CẦN SỬA**
- Quy ước căn cứ: “BD-10”, “SEQ-11” và “SQL/schema” lần lượt là `docs/BD/10. Study2Work_Study_BasicDesign_Admin_Quan_Tri_Noi_Dung.md`, `docs/BD/diagram/SEQUENCE/11. Study2Work_Study_SEQ_Admin_Quan_Tri_Noi_Dung.md` và `docs/BD/diagram/CLASS/study2work_study_full_schema_seed.sql`; dải `:n-m` trong bảng là số dòng.

## Findings

| Severity | Sheet + cell | Mô tả cụ thể | Căn cứ BD | Cách sửa |
|---|---|---|---|---|
| P1 | `00.Hướng dẫn!A4:B4`, `Cover!B19` | Inventory 44 file/không schema đã stale; hiện có 48 file và SQL schema. | SQL `:1-31`; canonical `docs/BD/base/0. Study2Work_System_Architecture.md:632-700` | Cập nhật source inventory và precedence. |
| P0 | `2.Response!D9:D11`, `2.Response!A36` | Envelope/error cũ và snake_case trái canonical. | `docs/BD/base/0. Study2Work_System_Architecture.md:632-700` | Dùng canonical envelope, machine-readable business code và `traceId`. |
| P1 | `2.Response!A24` | Mutation response có `meta.page/page_size`; pagination mẫu thừa. | `docs/BD/base/0. Study2Work_System_Architecture.md:693-700` | Bỏ pagination; trả transition result top-level trong `data`. |
| P1 | `3.Data mapping!A20`, `00.Hướng dẫn!A13:B18` | UPDATE_ACTION vẫn là placeholder, điều kiện status/version không cụ thể nhưng checklist đã tick. | `docs/BD/base/0. Study2Work_System_Architecture.md:601-628,738-752` | Đặc tả transition matrix, lock/version predicate, UPDATE và audit trong một transaction. |
| P0 | `1.Request!D22:I24`, `5.DB_Update_Main!B8:I12` | `action` bị khai `Object` dù format liệt kê enum; DD lại ghi `action`, `reason`, `effective_at`, `updated_at`, `updated_by` vào `learning_paths`, trong khi bảng chỉ có `publish_status` và `published_at`. | Lifecycle BD-10 `:35-51`; SQL `:70-76,323-338` | Dùng `action`/`targetStatus` enum; map transition sang `publish_status`, đặt/giữ `published_at`; lưu reason/actor trong audit log. |
| P0 | `3.Data mapping!C13:G15`, `4.Error!A12:H18` | Không có transition matrix hiện trạng→hành động, không chạy checklist nguồn/quyền/completion trước publish, và error lại chứa `ACTIVE_PATH_EXISTS` của learner. | BD-10 `:146-157,173-182` | Liệt kê allowed transitions và error riêng (`INVALID_CONTENT_TRANSITION`, `PRE_PUBLISH_CHECK_FAILED`, `USAGE_RIGHT_UNKNOWN`); bỏ error learner. |
| P0 | `3.Data mapping!D15:H15`, `6.DB_Update_Related!A12:I12` | Audit/notification chỉ mô tả generic; chưa bảo đảm before/after cùng transaction và notification sau commit/outbox khi update quan trọng. | SEQ-11 `docs/BD/diagram/SEQUENCE/11. Study2Work_Study_SEQ_Admin_Quan_Tri_Noi_Dung.md:28-36,114-117`; base architecture `:601-628` | Persist status + audit + outbox atomically; worker gửi notification sau commit, có dedupe/idempotency. |

## Checklist duyệt lại

- [ ] Source/envelope/pagination canonical.
- [ ] `action`/`targetStatus` là enum, không phải Object.
- [ ] Có transition matrix DRAFT→IN_REVIEW→PUBLISHED→UPDATED→ARCHIVED.
- [ ] Mapping cập nhật `publish_status/published_at` thật.
- [ ] Publish chạy checklist nguồn/quyền/cấu trúc/completion.
- [ ] Lock/version và idempotency được đặc tả.
- [ ] Audit before/after/reason và outbox notification atomic.
- [ ] OpenAPI/test bao phủ transition sai, concurrent publish và retry.

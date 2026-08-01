# Review API DD — S2W-STUDY-API-097

- DD source: `docs/DD/Study2Work_DD_API/10_Admin_quan_tri_noi_dung/S2W-STUDY-API-097_PATCH_admin_learning_paths_path_id.xlsx`
- Method + endpoint: `PATCH /api/v1/admin/learning-paths/{path_id}`
- Kết luận: **CẦN SỬA**
- Quy ước căn cứ: “BD-10”, “SEQ-11” và “SQL/schema” lần lượt là `docs/BD/10. Study2Work_Study_BasicDesign_Admin_Quan_Tri_Noi_Dung.md`, `docs/BD/diagram/SEQUENCE/11. Study2Work_Study_SEQ_Admin_Quan_Tri_Noi_Dung.md` và `docs/BD/diagram/CLASS/study2work_study_full_schema_seed.sql`; dải `:n-m` trong bảng là số dòng.

## Findings

| Severity | Sheet + cell | Mô tả cụ thể | Căn cứ BD | Cách sửa |
|---|---|---|---|---|
| P1 | `00.Hướng dẫn!A4:B4`, `Cover!B19` | Nguồn 44 file/không schema đã stale so với 48 file và SQL hiện có. | SQL `:1-31`; `docs/BD/base/0. Study2Work_System_Architecture.md:632-700` | Cập nhật inventory và source precedence. |
| P0 | `2.Response!D9:D11`, `2.Response!A35` | Envelope cũ, error object và `request_id` trái canonical. | `docs/BD/base/0. Study2Work_System_Architecture.md:632-700` | Dùng canonical envelope/camelCase. |
| P1 | `2.Response!A23` | Mutation detail vẫn kèm `meta.page/page_size`; pagination mẫu thừa. | `docs/BD/base/0. Study2Work_System_Architecture.md:693-700` | Bỏ `meta`; trả resource/version và `traceId`. |
| P1 | `3.Data mapping!A20`, `00.Hướng dẫn!A13:B18` | UPDATE còn `<mapping>` và điều kiện bằng câu tiếng Việt; checklist lại tick “không placeholder”. | `docs/BD/base/0. Study2Work_System_Architecture.md:738-752` | Viết SQL/pseudocode xác định cột, precondition và affected-row check. |
| P0 | `1.Request!D22:F23`, `5.DB_Update_Main!B8:I11` | PATCH chỉ nhận `mutable: String` và `reason`, không có bất kỳ field nghiệp vụ nào dù mục tiêu là sửa tên/slug/mô tả/ảnh/đối tượng/đầu vào/đầu ra. `mutable`, `reason`, `updated_at`, `updated_by` đều không tồn tại trong schema. | BD-10 `:57-70`; SQL `:323-338` | Khai rõ từng field patchable và kiểu; map sang `title,slug,summary,description,level,estimated_hours,unlock_mode`; thuộc tính mới cần migration/relations. |
| P0 | `1.Request!B11`, `3.Data mapping!E13:G14` | Ghi “idempotent theo resource/version” nhưng request không có version/ETag và bảng không có version; do đó không thể phát hiện lost update. | Transaction rule `docs/BD/base/0. Study2Work_System_Architecture.md:601-628`; SQL `:323-338` | Thêm `If-Match`/version và cột version, hoặc lock row + state precondition được đặc tả; trả `409` khi conflict. |
| P1 | `2.Response!C16:H19` | `updated_path`, `changed_fields`, `impact_warning`, `audit_id` bị gán như cột của `learning_paths`; impact/audit không có query và reason optional dù thay đổi quan trọng cần truy vết. | BD-10 `:159-167,175-182`; audit schema `:691-719` | Trả object thực, tính impact từ enrollments, ghi audit before/after cho thay đổi quan trọng và yêu cầu reason theo policy. |

## Checklist duyệt lại

- [ ] Nguồn và canonical envelope đã sửa.
- [ ] Không còn pagination ở mutation response.
- [ ] PATCH liệt kê field thực, kiểu/enum/nullability rõ.
- [ ] Mapping chỉ dùng cột thật hoặc migration đã duyệt.
- [ ] Có version/ETag hoặc chiến lược lock chống lost update.
- [ ] Impact học viên được tính trước thay đổi quan trọng.
- [ ] Audit before/after/reason cùng transaction.
- [ ] OpenAPI/test bao phủ empty patch, duplicate slug, state conflict và race.

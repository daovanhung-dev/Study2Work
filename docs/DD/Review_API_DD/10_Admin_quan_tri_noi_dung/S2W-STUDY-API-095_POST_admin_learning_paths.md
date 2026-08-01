# Review API DD — S2W-STUDY-API-095

- DD source: `docs/DD/Study2Work_DD_API/10_Admin_quan_tri_noi_dung/S2W-STUDY-API-095_POST_admin_learning_paths.xlsx`
- Method + endpoint: `POST /api/v1/admin/learning-paths`
- Kết luận: **CẦN SỬA**
- Quy ước căn cứ: “BD-10”, “SEQ-11” và “SQL/schema” lần lượt là `docs/BD/10. Study2Work_Study_BasicDesign_Admin_Quan_Tri_Noi_Dung.md`, `docs/BD/diagram/SEQUENCE/11. Study2Work_Study_SEQ_Admin_Quan_Tri_Noi_Dung.md` và `docs/BD/diagram/CLASS/study2work_study_full_schema_seed.sql`; dải `:n-m` trong bảng là số dòng.

## Findings

| Severity | Sheet + cell | Mô tả cụ thể | Căn cứ BD | Cách sửa |
|---|---|---|---|---|
| P1 | `00.Hướng dẫn!A4:B4`, `Cover!B19` | Nguồn “44 file/không có schema” đã stale; hiện có 48 file và SQL schema. | `docs/BD/diagram/CLASS/study2work_study_full_schema_seed.sql:1-31`; `docs/BD/base/0. Study2Work_System_Architecture.md:632-700` | Cập nhật source inventory và precedence trước khi duyệt DD. |
| P0 | `2.Response!D9:D11`, `2.Response!A34` | Response dùng envelope cũ `{data,meta}` / `{error}` và snake_case. | `docs/BD/base/0. Study2Work_System_Architecture.md:632-700` | Chuyển toàn bộ schema/ví dụ sang canonical envelope và `traceId`. |
| P1 | `2.Response!A22` | Response tạo một resource nhưng vẫn có `meta.page/page_size`; đây là pagination mẫu thừa. Ví dụ còn trả `status: ACTIVE` trái với mục tiêu tạo DRAFT. | `docs/BD/base/0. Study2Work_System_Architecture.md:693-700`; lifecycle BD-10 `:35-51` | Bỏ `meta`; trả `publishStatus: DRAFT` cùng ID/path vừa tạo. |
| P1 | `3.Data mapping!A20`, `00.Hướng dẫn!A13:B18` | Pseudocode `INSERT ... SET <mapping>` không phải PostgreSQL hợp lệ và còn placeholder dù checklist đã tick hoàn tất. | `docs/BD/base/0. Study2Work_System_Architecture.md:738-752`; schema target PostgreSQL tại SQL `:1-25` | Viết `INSERT INTO ... (columns) VALUES (...) RETURNING ...`; loại mọi placeholder. |
| P0 | `1.Request!D21:I34`, `7.DB_Insert_Main!B8:I23` | Contract/mapping không khớp schema: `name`/`short_description`/`difficulty`/`estimated_duration` map sang nhiều cột không tồn tại; thời lượng là String nhưng schema là `estimated_hours INTEGER`. | SQL `:323-338`; chức năng lộ trình BD-10 `:57-70` | Chốt DTO theo `title,slug,summary,description,level,estimatedHours,unlockMode`; các thuộc tính mới phải có migration/mô hình quan hệ riêng. |
| P0 | `7.DB_Insert_Main!B14:B21`, `3.Data mapping!E14` | `target_users`, `excluded_users`, `prerequisites`, `outcomes`, `completion_conditions`, `next_path_id`, `community_group_ids` bị lưu JSON/cột trực tiếp nhưng schema không có. Completion rule đã có bảng riêng. | SQL `:323-338,560-580`; BD-10 `:63-69` | Thiết kế bảng/quan hệ có FK; ghi `completion_rules` trong cùng transaction, không “nhét” JSON vào `learning_paths` nếu chưa có quyết định schema. |
| P1 | `1.Request!B11`, `3.Data mapping!G15` | Header idempotency chỉ “khuyến nghị”, không định nghĩa key scope, request hash, replay response hay TTL cho create. | Mẫu idempotency `docs/BD/base/0. Study2Work_System_Architecture.md:723-736`; transaction `:601-628` | Chốt hỗ trợ `Idempotency-Key` cho create, uniqueness `(actor,endpoint,key)`, request hash và response snapshot. |

## Checklist duyệt lại

- [ ] Source inventory và precedence đã cập nhật.
- [ ] Envelope/ví dụ canonical; tạo mới trả `DRAFT`, không có pagination.
- [ ] DTO khớp schema hoặc kèm migration được phê duyệt.
- [ ] Completion/community/next-path có mô hình quan hệ và FK rõ.
- [ ] PostgreSQL INSERT/RETURNING thực thi được, không placeholder.
- [ ] Transaction gồm bản ghi chính, quan hệ và audit cần thiết.
- [ ] Idempotency và duplicate slug được đặc tả/test.
- [ ] OpenAPI thể hiện enum, required, conflict và response `201`.

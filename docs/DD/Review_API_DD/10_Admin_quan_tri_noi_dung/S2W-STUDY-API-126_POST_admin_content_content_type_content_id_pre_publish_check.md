# Review API DD — S2W-STUDY-API-126

- DD source: `docs/DD/Study2Work_DD_API/10_Admin_quan_tri_noi_dung/S2W-STUDY-API-126_POST_admin_content_content_type_content_id_pre_publish_check.xlsx`
- Method + endpoint: `POST /api/v1/admin/content/{content_type}/{content_id}/pre-publish-check`
- Kết luận: **CẦN SỬA**

## Diff bắt buộc với SEQ-11

SEQ-11 định nghĩa đúng một target qua `POST /api/v1/admin/content/{type}/{id}/pre-publish-check`, request chỉ có path `{type,id}`, và response `data.{passed,issues,affectedLearnerCount}`. DD đổi tên path param, tự thêm batch `items[]`, đổi toàn bộ response và biến một check đọc thành UPDATE trên `users`; vì vậy trạng thái “TRỰC TIẾP/VERIFIED” là không có căn cứ.

## Findings

| Severity | Sheet + cell | Mô tả cụ thể | Căn cứ BD | Cách sửa |
|---|---|---|---|---|
| P1 | `00.Hướng dẫn!A4:B4`, `Cover!B19` | DD ghi 44 nguồn/không schema, trong khi `docs/BD` có 48 file và SQL. | `docs/BD/diagram/CLASS/study2work_study_full_schema_seed.sql:1-31`; canonical `docs/BD/base/0. Study2Work_System_Architecture.md:632-700` | Cập nhật inventory/schema/precedence; bỏ trạng thái VERIFIED cho tới khi sửa contract. |
| P0 | `2.Response!D9:D11`, `2.Response!A35` | Envelope `{data,meta}`/`{error}` và `request_id` không canonical. | `docs/BD/base/0. Study2Work_System_Architecture.md:632-700` | Dùng `success,businessCode,message,data|errors,traceId` và camelCase. |
| P1 | `2.Response!A23` | Non-list check vẫn có `meta.page/page_size`; pagination mẫu thừa. SEQ-11 cũng có `meta:{}`, nhưng canonical mới hơn quy định meta pagination chỉ cho list. | `docs/BD/base/0. Study2Work_System_Architecture.md:632-700`; SEQ-11 `docs/BD/diagram/SEQUENCE/11. Study2Work_Study_SEQ_Admin_Quan_Tri_Noi_Dung.md:54-74` | Bỏ `meta` khỏi response, giữ `traceId` top-level. |
| P1 | `3.Data mapping!A20`, `00.Hướng dẫn!A13:B18` | SQL còn `<current_columns>/<mapping>` và checklist tự tick “không placeholder/đã review schema”. | `docs/BD/base/0. Study2Work_System_Architecture.md:738-752`; SQL `:323-580` | Viết content-type dispatch/read queries cụ thể; để checklist chưa đạt cho tới khi OpenAPI/query/test tồn tại. |
| P1 | `Cover!B10`, `1.Request!D21:D22` | URI/param của DD là `{content_type}/{content_id}`, khác contract trực tiếp SEQ-11 `{type}/{id}`. Đây là breaking mismatch về tên parameter trong OpenAPI/generated client. | SEQ-11 `:22-26,39-52`; contract versioning `docs/BD/base/0. Study2Work_System_Architecture.md:738-751` | Giữ đúng `{type}/{id}` hoặc cập nhật nguồn contract qua review/migration đồng bộ; chốt enum type. |
| P0 | `Overview!A8:A12`, `1.Request!D23:I25`, `1.Request!A28` | SEQ-11 check một target từ path; DD tự thêm required batch `items[]`, cho phép array rỗng, item ID lại là String không UUID và tuyên bố “một hoặc nhiều nội dung”. | SEQ-11 `:41-52`; BD-10 checklist `docs/BD/10. Study2Work_Study_BasicDesign_Admin_Quan_Tri_Noi_Dung.md:146-157` | Bỏ body `items[]` khỏi API trực tiếp. Nếu cần batch, thiết kế endpoint khác với contract/idempotency/partial-failure riêng. |
| P0 | `2.Response!C16:H19`, `2.Response!A23` | SEQ-11 trả `passed: boolean`, `issues[{code,message}]`, `affectedLearnerCount: integer`; DD trả `valid: String`, `errors`, `warnings`, `checks` và bỏ affected count. Diff contract hoàn toàn. | SEQ-11 `:54-74` | Khôi phục đúng typed fields của SEQ-11; có thể mở rộng issue severity/entity theo versioned contract nhưng không thay im lặng. |
| P0 | `3.Data mapping!D12:H16`, `5.DB_Update_Main!A6:I10`, `6.DB_Update_Related!A8:I8` | Pre-publish check bị map vào `study.users`, lọc `users.content_type/content_id`, UPDATE `items`, và ghi audit. `users` không có các cột này; SEQ yêu cầu load content graph + affected learners, không mutate. | SEQ-11 `:22-26`; SQL content tables `:323-580`; users SQL `:239-249` | Dispatch theo type tới `learning_paths/courses/lessons/exercises` và relations; API read-only, không UPDATE/audit trừ khi có policy logging riêng. |
| P0 | `3.Data mapping!C13:F13`, `2.Response!C19:H19` | “Áp dụng mục 4.8” chỉ là câu chung, không liệt kê đủ 8 checks: tên/mô tả, mục tiêu, cấu trúc, completion bắt buộc, link/resource, nguồn/quyền, required lesson, preview scope. | BD-10 `:146-157,175-180`; SEQ-11 `:18-26,114-117` | Định nghĩa stable issue codes và traversal cho từng content type; `passed=false` khi lỗi blocking, warnings tách rõ; tính affected learners. |
| P1 | `4.Error!A13:H16` | `CONTENT_NOT_PUBLISHED` cho 404 là nghịch lý ở API kiểm tra trước publish; `HIGH_RISK_REASON_REQUIRED` không có request reason và check không phải mutation. | BD-10 `:146-157`; SEQ-11 `:22-26` | Dùng `CONTENT_NOT_FOUND`, `UNSUPPORTED_CONTENT_TYPE`, validation error; failed checklist vẫn có thể là HTTP 200 với `passed=false` như SEQ, không dùng lỗi transport cho kết quả check. |

## Checklist duyệt lại

- [ ] Source inventory là 48 file; trạng thái VERIFIED được gỡ tới khi re-review.
- [ ] URI/path param khớp chính xác SEQ-11 hoặc có contract migration.
- [ ] Bỏ batch `items[]`; request chỉ xác định một target.
- [ ] Response đúng `passed/issues/affectedLearnerCount` và canonical envelope.
- [ ] Non-list response không có pagination/meta rỗng.
- [ ] Check là read-only, không UPDATE `users`.
- [ ] Đủ tám rule pre-publish với stable issue codes.
- [ ] OpenAPI/test diff contract, mọi content type, missing rights và affected count.

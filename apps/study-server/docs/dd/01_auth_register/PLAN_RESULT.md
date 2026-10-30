# PLAN_RESULT — Study API #01

**API:** `POST /api/v1/auth/register` — Tạo tài khoản mới
**Trạng thái:** `Draft — Needs Confirmation`; package DD được bổ sung đủ artifacts, còn câu hỏi contract/source
**Output folder:** `apps/study-server/docs/dd/01_auth_register/`

## Cơ sở

Catalog #01 là contract trực tiếp: endpoint public, không yêu cầu Bearer; body gồm `email`, `password`, `full_name`; response `ApiEnvelope<UserProfile>`; HTTP `201 DESIGN_RESOURCE_CREATED`; errors `422 DESIGN_VALIDATION_ERROR`, `409 DESIGN_STATE_CONFLICT`, `500 DESIGN_INTERNAL_ERROR`. AC-01 mô tả validation, kiểm tra email trùng, hash mật khẩu, tạo user và hồ sơ mặc định, rồi gọi API #02 để gửi email xác thực.

Package giữ nguyên tám sheet thiết kế đang có. Ba report này bổ sung kế hoạch/kết quả, câu hỏi còn mở, và bằng chứng verification; không thay contract bằng hành vi hiện tại.

## Nguồn đã đối chiếu

- [Catalog API #01 và schema dùng chung](../../../../../docs/lists/list_api.md).
- [Index AC-01](../../diagrams/AC_UNICA/00_AC_API_INDEX.md) và [diagram AC-01](../../diagrams/AC_UNICA/AC_01_GUEST_ACCOUNT.drawio).
- [DB table guide — `users`](../../diagrams/DB_UNICA_TABLES.md) và [DB ERD](../../diagrams/DB_UNICA_ERD.drawio).
- Legacy candidate [Study `DB.sql`](../../../../../infra/postgres/study-server/DB.sql) và V1-PILOT schema [02_study_db.sql](../../../../../infra/postgres/02_study_db.sql); không nguồn nào tự chứng minh live schema.
- Current route `app/api/v1.py`, module `api_01_auth_register/{models,validate,query,view}.py`, shared email/password/response/middleware source, API #01 tests.
- DD/API #02 cùng current verify-email view/provider để rà điểm nối AC-01.
- Registry-wired `createDD-markdown`, registered template 8 sheets, và Study Markdown-only workflow.

## Tables read/write và side effect

| Hạng mục | Expected/design | Current source evidence |
|---|---|---|
| Read | AC-01 và DD #01 đề xuất đọc `users.id` theo email để phát hiện trùng. | `CHECK_DUPLICATE` chọn `id` từ `users` với email đã chuẩn hóa. |
| Write | AC-01 ghi user và hồ sơ mặc định trong transaction; ERD V1 chỉ xác nhận `users`. | `INSERT_USER` chỉ ghi `users`, role `STUDENT`, avatar/phone NULL và timestamps; status dựa vào DB default. |
| Verify email | AC-01 nối sang API #02 sau khi tạo tài khoản; lỗi provider sau acceptance được ghi log/retry. | API #01 hiện chỉ ghi log `verification_dispatch_pending`; không gọi API #02 hoặc provider, không có retry worker trong handler. API #02 dùng default stub không gửi email thật. |
| Response | `UserProfile` reusable gồm các field khai báo trong catalog. | Query trả profile an toàn nhưng không có `bio`; `bio` cũng không có trong ERD V1. |

Không suy ra bảng `profiles`, email verification state, token hoặc retry table từ diagram. Không map DB Work/Identity sang Study. Live database metadata chưa được kiểm tra.

## Giả định giữ lại

- Các min/max/policy của password chưa được contract chốt. Hành vi validator hiện tại được báo ở `VERIFICATION_REPORT.md`, không nâng thành business rule đã duyệt.
- Email unique theo ERD/legacy DDL và constraint hiện được source xử lý; semantics phân biệt hoa/thường và trạng thái constraint trong live DB chưa được xác nhận.
- `created_at`/`updated_at` hiện được SQL gán `CURRENT_TIMESTAMP`; đây là current source behavior, không phải cam kết live schema.
- Profile mặc định và dispatch verification tiếp tục là expected AC-01 cho đến khi contract owner điều chỉnh.

## Conflicts cần giữ

1. AC-01 kỳ vọng API #02/provider dispatch; current API #01 chỉ log marker sau commit. API #02 hiện trả accepted từ stub, không gửi email thật.
2. AC-01 nói “user + hồ sơ mặc định”; ERD/runtime mapping chỉ có `users`, không có profile table được xác nhận.
3. `UserProfile.bio` có trong catalog nhưng không có column trong ERD và không có trong API #01 current response.
4. Catalog để validation policy tổng quát; runtime có một số rule cụ thể. Chúng không tự trở thành approved design policy.
5. Legacy Study `BIGSERIAL users` khác V1-PILOT identity/profile model; live schema chưa được xác nhận.

## Kết quả

Tạo ba report tiếng Việt và sửa hai đường dẫn nguồn, whitespace đầu file, cùng bốn appendix tail để khớp template hiện đăng ký. Không sửa nội dung runtime, tests, schema, catalog, diagram hoặc client. Static verification được ghi tại [VERIFICATION_REPORT.md](./VERIFICATION_REPORT.md); các quyết định còn thiếu nằm tại [OPEN_QUESTIONS.md](./OPEN_QUESTIONS.md).

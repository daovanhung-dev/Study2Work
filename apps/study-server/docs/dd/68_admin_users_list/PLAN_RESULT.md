# Kết quả plan — API #68

## Phạm vi

Tạo DD Markdown cho GET /api/v1/admin/users theo catalog và AC-31. Chỉ tạo tài liệu; không sửa source, schema, catalog hoặc diagram; không tạo ZIP. Khi tạo #68, macro-review nhóm #68–#72 được để pending tới khi đủ DD; review document-level đã hoàn tất sau khi tạo #72.

## Plan đã thực hiện

| Bước | Kết quả |
|---|---|
| Phân loại task | docs; scope server-study; không có dependency cross-scope. |
| Worklog preflight | Selector chọn #48/#49/#50; đọc đủ cả ba trước khi inspect sâu. |
| Diagram/catalog | Đọc AC-31 index và toàn page AC-31 trong drawio; exact contract API #68 được giữ nguyên. |
| Source/schema | Không tìm thấy route/module/test/Admin guard; so sánh current API #4/#14 profile projection, API #07 page precedent, legacy và V1-PILOT schema. |
| Plan-before-authoring | API Requirement, Request Usage, Query, Mutation, Response Source matrices được ghi vào worklog trước khi tạo folder DD. |
| Authoring | Tạo 8 template sheets và 3 reports trong folder API #68; mọi suy luận được tách khỏi direct contract. |
| Macro-review | Đã rà nhóm #68–#72 ở mức tài liệu sau khi tạo #72; các câu hỏi chưa có nguồn vẫn mở. |

## Quyết định tài liệu

- Direct response giữ ApiEnvelope<UserProfile> như catalog, dù không thể biểu diễn danh sách/pagination.
- Page<UserProfile>, filter keyword, page mặc định 1, size 20 và order id ASC chỉ là proposal DERIVED, cần owner duyệt và sửa contract.
- Legacy users là candidate mapping; V1-PILOT UUID model và live schema được giữ riêng.
- Response candidate không lấy password_hash; bio có trong reusable schema nhưng thiếu source hiện tại.
- Response role/status giữ đúng UserRole/UserStatus của reusable schema; enum members chưa được catalog liệt kê và API #4 current model vẫn dùng str.
- Error set trực tiếp chỉ gồm 401/403/500; không tự thêm 404/422.
- 07_table.md là N/A — READ-ONLY API.

## Trạng thái

Draft — Needs Confirmation. API #68 chưa implementation-ready cho tới khi quyết định response cardinality, page rules, Admin guard, schema, bio/null semantics và PII visibility.

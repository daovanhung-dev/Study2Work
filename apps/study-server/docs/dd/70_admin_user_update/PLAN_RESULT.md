# Kết quả plan — API #70

## Phạm vi

Tạo DD Markdown cho `PUT /api/v1/admin/users/{user_id}` theo catalog và AC-31. Chỉ tạo tài liệu; không sửa source, schema, catalog hoặc diagram; không tạo ZIP. Khi tạo #70, macro-review AC-31 chờ DD #71–#72; document-level review đã hoàn tất sau khi tạo #72.

## Plan đã thực hiện

| Bước | Kết quả |
|---|---|
| Phân loại task | docs; scope server-study; không có dependency cross-scope. |
| Worklog preflight | Selector chọn #48/#49/#50; đọc đủ ba worklog trước khi inspect sâu. |
| Context và skill | Đọc router/context-map, server-study scope, manifest registry và createDD-markdown resources; workflow Study yêu cầu Markdown. |
| Catalog/diagram | Đối chiếu row #70, reusable UserProfile, AC-31 index và flow update/status/delete. |
| Source/schema | Không có route/module/test/Admin guard; so sánh API #14 profile mutation, legacy BIGINT users và V1-PILOT UUID model. |
| Plan-before-authoring | Requirement, Request Usage, Query, Mutation và Response Source matrices được ghi vào worklog trước khi tạo DD folder. |
| Authoring | Tạo 8 template sheets và 3 reports; giữ body/query/mutation ngoài contract là DERIVED hoặc SOURCE_REQUIRED. |
| Macro-review | Đã rà document-level nhóm #68–#72; role/status/delete boundaries được giữ riêng. |

## Quyết định tài liệu

- Giữ direct method/path/auth/path type/response/status/error set chính xác theo catalog.
- Body chưa được đặc tả; candidate `full_name`, `phone`, `avatar_url`, `role` gắn nhãn DERIVED; requiredness/nullability/enum values vẫn mở.
- Candidate UPDATE trên legacy `users` không phải runtime SQL; không đọc password_hash, không persist bio.
- Status update thuộc API #71; không tự thêm delete, audit, session revoke hoặc role transition policy.
- `UserProfile.bio` source gap; UserRole/UserStatus members chưa được định nghĩa.
- Admin authorization, live schema, error envelope và PUT semantics còn mở.

## Trạng thái

Draft — Needs Confirmation. Chưa implementation-ready cho đến khi request body/role policy/Admin guard/schema và side effects được chốt.

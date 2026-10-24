# Kết quả plan — API #72

## Phạm vi

Tạo DD Markdown cho `DELETE /api/v1/admin/users/{user_id}` theo catalog và AC-31. Chỉ thay đổi tài liệu; không sửa source, schema, catalog hoặc diagram; không tạo ZIP. Sau khi authoring, macro-review nhóm AC-31 #68–#72.

## Plan đã thực hiện

| Bước | Kết quả |
|---|---|
| Phân loại task | docs; scope server-study; không có dependency cross-scope. |
| Worklog preflight | Deno selector chọn #48/#49/#50; đọc đủ ba worklog trước khi inspect sâu. |
| Context/skill | Đọc root/context router, server-study scope/index/workflow, manifest wiring và createDD-markdown; Study output là Markdown-only. |
| Catalog/diagram | Đối chiếu API #72, DeleteResult và toàn bộ node/edge AC-31; xác nhận DELETE → policy soft-delete/anonymize → reload. |
| Prior DDs | Rà #68 list, #69 detail, #70 update, #71 status và open questions để giữ đúng boundaries. |
| Source/schema | Không có route/module/test/Admin guard; legacy DDL có user FK relations nhưng không có delete timestamp; pilot UUID model tách riêng. |
| Plan-before-authoring | Requirement, Request Usage, Query, Mutation và Response Source matrices đã ghi trong worklog trước khi tạo folder. |
| Authoring | Tạo 8 template sheets và 3 reports; không tạo physical delete/policy/schema ngoài nguồn. |
| Macro-review | Rà document-level nhóm #68–#72; findings và open gaps được cập nhật trong cả năm DD. |

## Quyết định tài liệu

- Giữ exact method/path/auth/path/error/response contract theo catalog.
- Giữ `DeleteResult.status = "deleted"`; `deleted_at` bắt buộc trong contract nhưng physical source chưa có.
- Xem soft-delete/anonymize là intent trực tiếp từ diagram; không chọn policy hoặc physical column thay owner.
- Legacy FK references chỉ là dependency context; không suy ra blanket block/cascade/hard delete.
- API #70 profile/role, #71 account status, #72 delete lifecycle là các mutation tách biệt.
- API #68 list cardinality mismatch và #69–#71 field/schema/security gaps vẫn được nêu riêng.
- Status DD: Draft — Needs Confirmation; chưa implementation-ready.

## AC-31 macro-review

**Status: VERIFIED_WITH_OPEN_QUESTIONS — document-level only.**

- #68 list response `ApiEnvelope<UserProfile>` không khớp list/pagination intent; #72 không sửa contract này.
- #69 detail và #68 list cùng cần policy về user đã xóa/anonymized và PII projection.
- #70 chỉ cập nhật profile/role; #71 chỉ cập nhật ACTIVE/SUSPENDED candidate; không gộp xóa vào các endpoint này.
- #72 giữ `DeleteResult` và soft-delete/anonymize intent, nhưng physical policy/schema/`deleted_at`/dependency mapping chưa có nguồn.
- Shared issues: Admin guard chưa có; user schema BIGINT legacy vs UUID pilot và live schema chưa xác minh; UserRole/UserStatus enum, bio/null, PII/audit và error data null-vs-empty còn mở.
- Không có application tests; không khẳng định runtime behavior.

## Trạng thái

Draft — Needs Confirmation. Cần policy/schema/authorization owner chốt các câu hỏi trong [OPEN_QUESTIONS.md](./OPEN_QUESTIONS.md) trước implementation.

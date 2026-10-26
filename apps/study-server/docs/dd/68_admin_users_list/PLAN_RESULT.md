# Kết quả plan — API #68

## Phạm vi

Triển khai `GET /api/v1/admin/users`, đồng bộ contract list/pagination theo AC-31, cập nhật DD Markdown và server-study context. Không sửa API #69–#72 runtime, không thêm migration, không stage/commit.

## Plan đã thực hiện

| Bước | Kết quả |
|---|---|
| Context/preflight | Đọc router, context map, scope server-study, manifest và 3 worklog coding do selector chọn; đọc thêm worklog DD #68. |
| Source trace | Đối chiếu AC-31, API catalog, legacy/V1-PILOT DDL, API #04/#14 profile và API #07 pagination; lưu discrepancy/DERIVED rules trong worklog trước code. |
| Contract | API #68 catalog và AC-31 node dùng `ApiEnvelope<Page<UserProfile>>`; thêm 422 cho `page` lỗi theo precedent #07. |
| Runtime | Thêm module Admin list, SQL-only COUNT/LIST constants, shared ADMIN JWT guard, filters, fixed pagination, response projection và route/OpenAPI. |
| HTTP tests | Thêm 15 focused TestClient cases cho auth, filter/page, empty/malformed/query failure, response safety và OpenAPI. |
| DD | Đồng bộ 8 sheet chính cùng OPEN_QUESTIONS/PLAN_RESULT/VERIFICATION_REPORT; giữ nguyên appendix Excel byte-for-byte. DD vẫn Draft do live schema/policy còn mở. |
| AC-31 macro-review | Sửa các #69–#72 references bị stale về #68 response; giữ các vấn đề visibility, PII/audit, schema và lifecycle còn mở. |
| Context | Cập nhật route/runtime/database/security/module/test/source-status pages và manifest API #68 paths/counts. |

## Fallback contract/runtime

- Query dùng checked-in legacy BIGINT `users`; V1-PILOT UUID model không được join.
- Page mặc định 1, kích thước cố định 20, sort `id ASC`; optional `role`/`status` exact match; keyword literal case-insensitive substring trên `full_name`/`email`.
- Reuse API #04 `UserProfile`; bỏ `bio` vì không có source column/current model, không select `password_hash`.
- Shared JWT guard yêu cầu `ADMIN` trước DB access. Không có Admin permission table trong DDL.
- Toàn bộ semantics ngoài method/path/query/role/200/code đã khai báo được đánh dấu DERIVED; không migration hoặc live-schema claim.

## Trạng thái

DD: Draft — Needs Confirmation. Implementation có source/tests local; live schema, Admin permission policy, PII/audit và delete visibility chưa xác nhận.

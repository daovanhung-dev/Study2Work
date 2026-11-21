# Kết quả plan — API #71

## Phạm vi

Triển khai `PATCH /api/v1/admin/users/{user_id}/status` theo catalog và nhánh STATUS AC-31; đồng bộ DD Markdown, context server-study, worklog và báo cáo macro-review liên quan. Không đổi catalog, diagram, DDL hoặc thêm migration. Giữ nguyên các thay đổi worktree đã có.

## Plan đã thực hiện

| Bước | Kết quả |
|---|---|
| Phân loại và preflight | `coding` / `test` / `docs`, scope `server-study`; selector chọn và đã đọc đủ worklog #34/#47/#48. |
| Context/skill | Đọc root router, context map, server-study scope/workflow, machine-readable registry và `createDD-markdown`; Study DD output là Markdown-only. |
| Source/contract trace | Đối chiếu API #71 catalog, AC-31 STATUS branch, legacy/V1-PILOT DDL, API #03 session logic, API #04 safe profile, APIs #68–#70, middleware và response helper. |
| Plan trước code | Ghi source trace, discrepancy table, transaction/response behavior và implementation plan vào worklog trước khi sửa runtime. |
| Runtime | Tạo module status với shared ADMIN guard, signed-int64 validation, strict request model, locked status update, conditional refresh-token revoke và caller-owned transaction. |
| Route/OpenAPI | Wire PATCH route và `DESIGN_CONTRACT_PATHS`; khai báo body/path/header và đúng 200/401/403/404/422/500. |
| HTTP regression | Thêm 21 test API #71; linked API #03/#68–#71 regression đạt 80 tests; full Study suite đạt 791 tests. |
| Static/source checks | Ruff pass; OpenAPI/import kiểm tra 40 path templates, 42 operations; DD Markdown/JSON/link và `git diff --check` được kiểm tra trong verification report. |
| DD/context | Cập nhật DD và context; đăng ký 6 source/test paths trong manifest; cập nhật macro-review claim hiện trạng cho #68–#72. |

## Các quyết định triển khai còn DERIVED

- Giữ method/path/auth/path type/response/status/error set của catalog. Body bắt buộc `{status}` với `ACTIVE`/`SUSPENDED` là fallback vì catalog/diagram không định nghĩa request body hoặc enum đầy đủ.
- Chỉ cho phép chuyển từ trạng thái hiện tại ACTIVE/SUSPENDED; trạng thái lifecycle khác trả 422 để endpoint khóa/mở khóa không kích hoạt nhầm verification/deletion state.
- Khi đích là SUSPENDED, revoke refresh-token rows chưa revoke và chưa hết hạn trong cùng transaction; ACTIVE không phục hồi token đã revoke. Access JWT đã cấp có thể còn dùng đến expiry.
- Dùng shared ADMIN claim theo pattern #68–#70; không thêm audit, tenant/MFA, self/last-admin, access-token blacklist hay migration.
- Legacy BIGINT `users`/`refresh_tokens` chỉ là checked-in candidate; live schema và deployment chưa xác minh.

## Trạng thái

Runtime có source và HTTP test evidence local. DD vẫn `Draft — Needs Confirmation` vì body/status policy, Admin authorization policy, live schema và token effects chưa được owner xác nhận. Xem [VERIFICATION_REPORT.md](./VERIFICATION_REPORT.md) và [OPEN_QUESTIONS.md](./OPEN_QUESTIONS.md).

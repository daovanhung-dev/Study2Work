# Kết quả plan — API #70

## Phạm vi

Triển khai `PUT /api/v1/admin/users/{user_id}` trong AC-31, đồng bộ DD và server-study context. Không sửa API #71/#72 runtime, catalog, diagram hoặc DDL; không thêm migration. Giữ mọi thay đổi worktree có sẵn.

## Plan đã thực hiện

| Bước | Kết quả |
|---|---|
| Context/preflight | Đọc router/context map, server-study AGENTS/INDEX/workflow, selector coding logs #34/#47/#48, manifest và các API/DD liên kết. |
| Contract/source trace | Đối chiếu AC-31 node, catalog #70, legacy DDL, API #14 profile mutation, API #68/#69 auth/profile, #71/#72 boundaries và current response/middleware. |
| Fallback decision | Direct contract không có body. Chọn full-replacement body bốn field, ba role hiện có, API #14 normalization, legacy BIGINT UPDATE RETURNING, invalid path 422; ghi rõ DERIVED trước code. |
| Runtime | Thêm module #70, shared ADMIN guard, path/body validation, một bound UPDATE, response mapping, commit/rollback và safe errors. |
| Route/OpenAPI | Wire PUT cùng path template GET #69, required Authorization, int64 path, JSON request model và 200/401/403/404/422/500. Middleware template đã tồn tại từ #69. |
| HTTP tests | Thêm focused TestClient coverage auth, body/path validation, normalized update, role/field boundaries, 404/500/rollback, trace và OpenAPI. |
| DD | Đồng bộ tám sheets và ba reports với runtime; giữ Appendix Excel của tám sheets nguyên byte. |
| AC-31 macro-review | Cập nhật #71/#72 report summaries để ghi #70 đã wired; giữ status/delete và policy gaps tách riêng. |
| Context | Cập nhật route/runtime/security/database/architecture/module/tests/entry/source-status và manifest theo source/test/API operation mới. |

## Quyết định fallback

- Giữ method/path/auth/response/status/error set trực tiếp theo catalog và diagram.
- Body là `full_name`, `phone`, `avatar_url`, `role`, tất cả required; nullable phone/avatar được xóa bằng null; extra fields bị từ chối.
- Dùng `STUDENT`, `MENTOR`, `ADMIN` làm role allowlist local; giá trị/transition chính thức vẫn cần owner xác nhận.
- Dùng shared ADMIN claim, legacy BIGINT `users`, API #14 profile normalization; không nối V1-PILOT UUID model.
- Invalid/out-of-range signed-int64 path trả 422 vì #70 khai báo validation error; no-row trả 404.
- Không đổi `status`, email, password, bio; không thêm audit hoặc token revocation. Những policy này còn mở.

## Trạng thái

Runtime có source và HTTP tests local. DD giữ `Draft — Needs Confirmation` vì body/role/Admin policy và live schema chưa được owner xác nhận; fake DB tests không chứng minh deployment.

# Kết quả plan — API #69

## Phạm vi

Triển khai `GET /api/v1/admin/users/{user_id}` theo catalog và AC-31, đồng bộ DD #69 và server-study context. Không sửa API #70–#72 runtime, không thêm migration, không đổi catalog/diagram, không stage/commit.

## Plan đã thực hiện

| Bước | Kết quả |
|---|---|
| Context/preflight | Đọc router/context map, scope server-study, manifest/registry và 3 worklog coding do selector chọn; đọc thêm worklog #68 và worklog thiết kế #69. |
| Source trace | Đối chiếu AC-31, catalog #69, API #68 guard/list, API #04 UserProfile projection, API #48 raw-path fallback, current middleware/error helper và legacy/V1-PILOT schema. Plan được ghi trước code. |
| Runtime | Thêm module detail với shared ADMIN guard, raw signed-int64 path, safe legacy users SELECT, 404 no-row/invalid-path, safe 500 projection/query và read-only response. |
| Route/OpenAPI | Wire GET path với int64 metadata và đúng responses 200/401/403/404/500; thêm route template vào `DESIGN_CONTRACT_PATHS`. |
| HTTP tests | Thêm TestClient coverage auth-before-query, successful profile/nulls, 404, invalid int64, SQL/projection failure, rollback, trace, read-only và OpenAPI. |
| DD | Cập nhật 8 sheets và 3 reports theo runtime; sửa stale Student-only, UNWIRED, error-data claims; giữ nguyên appendix Excel của 8 sheets. |
| AC-31 macro-review | Xác nhận #69 chỉ đọc; #68 list và #70/#71/#72 mutation boundary không overlap. Cập nhật report #72 về runtime #69; policy/schema/lifecycle gaps vẫn mở. |
| Context | Cập nhật route/runtime/security/database/architecture/module/test/source-status và manifest với API #69 paths/counts. |

## Fallback runtime

- Dùng shared JWT guard với role `ADMIN` trước path parsing và DB access; quyền user-management mapping là DERIVED theo API #68.
- Parse path thành signed int64; malformed/out-of-range và no-row trả `404 DESIGN_RESOURCE_NOT_FOUND`, không thêm 422 ngoài catalog.
- Query checked-in legacy BIGINT `users` bằng `id`, chọn đúng API #04 safe profile fields; không join V1-PILOT UUID tables và không select `password_hash`.
- Reuse API #04 `UserProfile`: avatar/phone null được serialize thành null; bio bị omit vì không có source.
- Các quyết định trên là DERIVED local behavior; live schema, Admin policy, PII/audit và visibility sau #71/#72 chưa xác minh.

## Trạng thái

DD vẫn `Draft — Needs Confirmation`. Runtime có source và HTTP tests local; fake DB không xác minh live schema/deployment hoặc policy owner.

# PLAN_RESULT — Study API #04

**API:** `GET /api/v1/users/me` — Lấy hồ sơ người dùng hiện tại

**Trạng thái DD:** `Draft — Needs Confirmation`; package tài liệu hoàn chỉnh, các quyết định contract/policy còn mở
**Output folder:** `apps/study-server/docs/dd/04_users_me/`

## Cơ sở contract và nguồn

- [Catalog API #04 và reusable schemas](../../../../../docs/lists/list_api.md): Bearer JWT, role Student, `ApiEnvelope<UserProfile>`, HTTP 200 `DESIGN_RESOURCE_RETRIEVED`, lỗi 401/403/500.
- [AC-02 index](../../diagrams/AC_UNICA/00_AC_API_INDEX.md) và [diagram AC-02](../../diagrams/AC_UNICA/AC_01_GUEST_ACCOUNT.drawio): login phát hành token, sau đó client gọi API #04 để lấy hồ sơ/role/permissions.
- [AC-11 index](../../diagrams/AC_UNICA/00_AC_API_INDEX.md) và [diagram AC-11](../../diagrams/AC_UNICA/AC_02_STUDENT_LEARNING.drawio): đọc hồ sơ, upload avatar qua API #13, cập nhật profile qua API #14, rồi tải lại hồ sơ.
- Current source: [router](../../../app/api/v1.py), [API #04 view](../../../app/modules/guest/api_04_users_me/view.py), [query](../../../app/modules/guest/api_04_users_me/query.py), [model](../../../app/modules/guest/api_04_users_me/models.py), [auth helper](../../../app/utils/auth.py), [trace helper](../../../app/core/trace.py), [response helpers](../../../app/core/responses.py).
- Focused [API #04 test source](../../../tests/modules/guest/api_04_users_me/test_users_me.py) đã được đọc; tests không chạy trong task DD.
- [DB.sql candidate](../../../../../infra/postgres/study-server/DB.sql) và [DB ERD](../../../docs/diagrams/DB_UNICA_ERD.drawio) là artifacts trong repo; live schema không được kiểm tra.
- Template được manifest đăng ký qua `createDD-markdown`; Study workflow yêu cầu folder Markdown, không tạo ZIP mới.

## Kết quả theo kế hoạch

| Hạng mục | Kết quả |
|---|---|
| Catalog contract | Giữ nguyên method/path, Student Bearer, response `ApiEnvelope<UserProfile>`, HTTP 200 và đúng error set 401/403/500. Ký hiệu auth lặp được biểu diễn thành một header. |
| Expected/current behavior | Ghi riêng AC-02 claim wording `user_id`/`role` và current source `sub`/`roles`; ghi riêng source mapping user không tồn tại thành 401. |
| Data mapping | Mô tả auth guard, SELECT allowlist từ `users`, branches 401/403/500, response serialization, không có mutation. Không thêm permissions hoặc `bio` source giả. |
| AC-02 macro-review (#03 → #04) | #03 current source đã trả profile cùng token; #04 được AC gọi để tải profile/role/permissions lần nữa. Claim naming khác diagram; permissions không có schema/source. Giữ các điểm này mở. |
| AC-11 macro-review (#04/#13/#14) | #13 upload Object Storage và chỉ trả URL; #14 cập nhật `full_name`, `phone`, `avatar_url`; source #14 bỏ qua `bio`; lần reload #04 không trả `bio`. Tách upload side effect khỏi DB transaction và giữ bù trừ/cleanup là câu hỏi. |
| API #14 report status | Sửa duy nhất các claim `NOT_FOUND/UNWIRED` cũ trong `PLAN_RESULT.md` và `VERIFICATION_REPORT.md`: route/module/test source hiện tồn tại; task này không chạy tests nên không nâng runtime status. |
| Package | Giữ 8 sheet lõi, thêm `PLAN_RESULT.md`, `OPEN_QUESTIONS.md`, `VERIFICATION_REPORT.md`; không tạo API DD thứ hai. |
| Scope | Chỉ sửa API #04 Markdown, API #14 hai report trạng thái source, và worklogs liên quan. Không sửa runtime, tests, schema, catalog hoặc diagram. |

## Expected behavior và current source

| Chủ đề | Expected behavior | Current source |
|---|---|---|
| Authentication | Catalog yêu cầu Bearer JWT và role Student; claim names không được khóa. | Guard giải mã access JWT, dùng numeric `sub` và list `roles`; yêu cầu có `STUDENT`. |
| Profile | Catalog trả `UserProfile`, trong đó `bio` optional; AC-02 còn nhắc permissions. | Query/model trả allowlist từ `users`; `bio` và permissions không có trong model/query. |
| Role/status | API chỉ cho Student theo catalog/diagram. | Quyền dựa trên JWT roles; query không đối chiếu `users.role` và không lọc `users.status`. |
| `users.status` nullability | `UserProfile.status` là `UserStatus` bắt buộc. | Model yêu cầu string; checked-in DDL candidate chỉ có `DEFAULT 'ACTIVE'`, không `NOT NULL`; NULL row sẽ vào nhánh mapping 500. Live schema chưa xác minh. |
| Missing user | Catalog có 401 nhưng không nêu điều kiện cụ thể; không khai báo 404. | Nếu JWT subject không có row trong `users`, view trả 401, không rollback. |
| Response | HTTP 200 `DESIGN_RESOURCE_RETRIEVED`, `ApiEnvelope<UserProfile>`. | HTTP 200 cùng code; `avatar_url`/`phone` None được serialize `null`, `bio` bị omit; trace ID đi trong envelope. |
| Side effect | AC-11 nối API #13 upload và API #14 persist URL; API #04 là read. | API #04 chỉ SELECT; không có mutation hay external call. |

## Source trace

```text
GET /api/v1/users/me -> Authorization + DB Session + trace ID -> validate_current_user_request -> decode access JWT -> validate positive numeric sub and roles -> require STUDENT -> SELECT users by id=:user_id LIMIT 1 -> 401 if row missing / rollback+500 on SQLAlchemyError / safe 500 on UserProfile ValidationError -> serialize allowlisted profile -> 200 DESIGN_RESOURCE_RETRIEVED
```

## Bảng và side effects

- Current query chỉ đọc `users.id`, `full_name`, `email`, `role`, `avatar_url`, `phone`, `status`, `created_at`, `updated_at`.
- Không đọc `password_hash`; không có bảng permissions/profile được source xác nhận; không ghi DB hoặc gọi external provider.
- DDL trong repository không chứng minh schema đang triển khai.
- Các quyết định còn mở được liệt kê tại [OPEN_QUESTIONS.md](./OPEN_QUESTIONS.md).

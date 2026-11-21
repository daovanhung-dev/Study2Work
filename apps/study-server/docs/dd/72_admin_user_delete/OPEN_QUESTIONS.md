# Câu hỏi còn mở — API #72

Trạng thái tài liệu: Draft — Needs Confirmation. API đã có implementation local theo các fallback DERIVED được liệt kê dưới đây; các quyết định cần owner xác nhận vẫn chưa được coi là policy đã duyệt.

## Đã triển khai theo fallback DERIVED

- `users.status='DELETED'` là marker soft-delete trong checked-in legacy BIGINT `users`; không hard-delete, anonymize hoặc xóa row liên quan.
- `users.updated_at` được cập nhật bằng `CURRENT_TIMESTAMP` và trả về như `DeleteResult.deleted_at`; không có cột thời gian xóa riêng.
- User không tồn tại hoặc đã có status `DELETED` trả 404. Không thêm idempotent success hay 409.
- Shared JWT guard yêu cầu role `ADMIN` trước path parsing/DB access; chưa có policy permission/tenant/MFA riêng.
- `status='DELETED'` làm API #03 login/refresh từ chối tài khoản. Access JWT đã phát hành không bị revoke bởi API #72 và có thể dùng đến khi hết hạn.
- Các fallback này giữ DD ở trạng thái Draft và không chứng minh live schema/deployment.

## Cần owner xác nhận

1. **Delete và PII policy:** Có chấp thuận `DELETED` marker không; user nào cần anonymization, field nào được giữ/ẩn và thời điểm áp dụng?
2. **Timestamp persistence:** Có cần cột/quan hệ `deleted_at` được lưu riêng? Hiện response chỉ dùng `updated_at` của mutation.
3. **Dependency/retention:** Quan hệ nào phải bảo tồn, chặn hoặc xóa theo retention? Hiện tất cả dependent rows được giữ nguyên.
4. **Retry behavior:** Có chấp thuận 404 cho lần DELETE lặp lại? Hiện missing và already-`DELETED` cùng trả 404 theo catalog.
5. **Admin safeguards:** Có cần chặn self-delete/last-Admin, tenant scope, permission riêng, MFA hoặc audit actor/reason không?
6. **Session revocation:** Có cần thu hồi refresh-token và/hoặc access-token đang tồn tại ngay khi đánh dấu DELETED? Runtime hiện không sửa token rows; login/refresh mới bị chặn theo API #03.
7. **Read/mutation visibility:** #68/#69 hiện không lọc status; #70 không đổi status; #71 từ chối current status ngoài ACTIVE/SUSPENDED. Có cần thay đổi behavior sau delete không?
8. **Schema approval:** Checked-in legacy DDL là candidate cục bộ; live schema và migration state chưa được xác minh. V1-PILOT UUID identity không được ghép với API int64 này.
9. **AC-31 reload:** Sau DELETE, UI/list/detail có nên hiển thị marker DELETED hay ẩn record theo policy?

## Ranh giới

Không có thay đổi catalog, diagram, DDL hoặc migration trong implementation này. Không suy luận hard-delete/cascade từ HTTP method hoặc legacy FK list. Xem [PLAN_RESULT.md](./PLAN_RESULT.md), [VERIFICATION_REPORT.md](./VERIFICATION_REPORT.md), và open questions của [#68](../68_admin_users_list/OPEN_QUESTIONS.md), [#69](../69_admin_user_detail/OPEN_QUESTIONS.md), [#70](../70_admin_user_update/OPEN_QUESTIONS.md), [#71](../71_admin_user_status/OPEN_QUESTIONS.md).

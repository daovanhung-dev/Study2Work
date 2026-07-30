# Kết quả Plan 02 — Authentication Core

- Phạm vi: API 007–015.
- Hoàn thành workbook: 9/9.
- Trạng thái: Draft; API suy dẫn cần xác nhận.
- Naming contract: camelCase cho JSON/query; path placeholder giữ nguyên catalog; DB dùng snake_case.
- Lưu ý nguồn: bundle hiện tại thiếu System Architecture, Study Architecture, schema seed SQL và API catalog CSV được plan viện dẫn.

| API | Method | Endpoint | Basis | Status | Workbook | DB ghi |
|---:|---|---|---|---|---|---|
| 007 | POST | `/api/v1/auth/register` | TRỰC TIẾP | Draft | `API_007_POST_auth_register.xlsx` | users, user_profiles, user_consents, verification_requests, outbox_events |
| 008 | POST | `/api/v1/auth/login` | TRỰC TIẾP | Draft | `API_008_POST_auth_login.xlsx` | sessions |
| 009 | POST | `/api/v1/auth/logout` | SUY DẪN | Draft — Needs Confirmation | `API_009_POST_auth_logout.xlsx` | sessions |
| 010 | POST | `/api/v1/auth/verification/send` | SUY DẪN | Draft — Needs Confirmation | `API_010_POST_auth_verification_send.xlsx` | verification_requests, outbox_events |
| 011 | POST | `/api/v1/auth/verify-contact` | TRỰC TIẾP | Draft | `API_011_POST_auth_verify_contact.xlsx` | verification_requests |
| 012 | GET | `/api/v1/auth/account-status` | SUY DẪN | Draft — Needs Confirmation | `API_012_GET_auth_account_status.xlsx` | Không |
| 013 | POST | `/api/v1/auth/password/forgot` | SUY DẪN | Draft — Needs Confirmation | `API_013_POST_auth_password_forgot.xlsx` | password_reset_tokens, outbox_events |
| 014 | POST | `/api/v1/auth/password/reset` | SUY DẪN | Draft — Needs Confirmation | `API_014_POST_auth_password_reset.xlsx` | password_reset_tokens, outbox_events |
| 015 | PUT | `/api/v1/auth/password` | SUY DẪN | Draft — Needs Confirmation | `API_015_PUT_auth_password.xlsx` | users |

## Reviewer notes

- Đối chiếu endpoint/contract suy dẫn với PO/BA trước khi đổi trạng thái Final.
- Đối chiếu logical table/column với schema seed SQL khi được cung cấp.

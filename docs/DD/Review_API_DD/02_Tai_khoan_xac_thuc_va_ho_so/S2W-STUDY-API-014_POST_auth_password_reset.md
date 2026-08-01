# Review API DD — S2W-STUDY-API-014

- DD nguồn: `docs/DD/Study2Work_DD_API/02_Tai_khoan_xac_thuc_va_ho_so/S2W-STUDY-API-014_POST_auth_password_reset.xlsx`
- Endpoint: `POST /api/v1/auth/password/reset`
- Verdict: **CẦN SỬA**

## Findings

| Mức | Sheet/cell | Finding | Căn cứ BD | Cách sửa |
|---|---|---|---|---|
| P0 | `2.Response!A7:H11` và ví dụ thành công/lỗi | Envelope `{data, meta}` / `{error}`, `meta.request_id`, snake_case và pagination giả không khớp contract chuẩn. | `docs/BD/base/0. Study2Work_System_Architecture.md:632-700` | Đổi sang `success`, `businessCode`, `message`, `data`, `errors`, `traceId`; chỉ có `meta.pagination` cho API danh sách và dùng camelCase. |
| P0 | `3.Data mapping!A12:H16`, các sheet DB | Flow chỉ update `password_reset_tokens` và còn map `new_password/confirm_password` như field DB; không cập nhật credential hash, không consume token atomically, không revoke session. | `docs/BD/base/0. Study2Work_System_Architecture.md:61-75,150-220,294-301`; `docs/BD/diagram/CLASS/study2work_study_full_schema_seed.sql:260-281` | Tại Identity: lock token, verify hash/TTL/unused, validate password, update Argon2id hash, mark consumed, revoke sessions trong transaction/saga. |
| P0 | `2.Response!A15:H19` | `password_reset` là String(enum), `sessions_revoked` là String; type và semantics không thực thi được. | `docs/BD/02. Study2Work_Study_BasicDesign_Tai_Khoan_Xac_Thuc_Ho_So.md:88-102` | Dùng Boolean/count rõ ràng, `loginRequired`; không trả dữ liệu token. |
| P0 | `4.Error` | Thiếu token invalid/expired/used, password mismatch/policy/reuse, attempt limit và race/replay errors. | `docs/BD/02. Study2Work_Study_BasicDesign_Tai_Khoan_Xac_Thuc_Ho_So.md:37-145,163-186` | Bổ sung businessCode ổn định và atomic one-time-use behavior. |
| P1 | `Cover!B15:G19`, `Lịch sử!A4:F4`, `00.Hướng dẫn!A4:B18` | Tài liệu được đánh dấu `VERIFIED` dù reviewer/approver chưa chỉ định; hướng dẫn còn tuyên bố gói nguồn không có schema và không còn placeholder. | `docs/BD/diagram/CLASS/study2work_study_full_schema_seed.sql:1-30` | Cập nhật inventory nguồn, loại bỏ placeholder, chuyển về `IN REVIEW` cho đến khi contract và mapping được duyệt. |

## Điều kiện duyệt lại

- [ ] Contract request/response và error catalog khớp BD/sequence hoặc có Change Request được phê duyệt.
- [ ] Mapping DB/service dùng owner, bảng, cột, khóa và transaction có thật; không còn placeholder.
- [ ] Envelope/casing/trace/pagination tuân theo kiến trúc chuẩn.
- [ ] Reviewer và approver được chỉ định; trạng thái chỉ chuyển `VERIFIED` sau khi đóng toàn bộ finding P0/P1.

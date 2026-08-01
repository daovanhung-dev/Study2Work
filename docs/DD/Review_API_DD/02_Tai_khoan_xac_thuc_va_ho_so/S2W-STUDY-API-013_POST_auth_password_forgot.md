# Review API DD — S2W-STUDY-API-013

- DD nguồn: `docs/DD/Study2Work_DD_API/02_Tai_khoan_xac_thuc_va_ho_so/S2W-STUDY-API-013_POST_auth_password_forgot.xlsx`
- Endpoint: `POST /api/v1/auth/password/forgot`
- Verdict: **CẦN SỬA**

## Findings

| Mức | Sheet/cell | Finding | Căn cứ BD | Cách sửa |
|---|---|---|---|---|
| P0 | `2.Response!A7:H11` và ví dụ thành công/lỗi | Envelope `{data, meta}` / `{error}`, `meta.request_id`, snake_case và pagination giả không khớp contract chuẩn. | `docs/BD/base/0. Study2Work_System_Architecture.md:632-700` | Đổi sang `success`, `businessCode`, `message`, `data`, `errors`, `traceId`; chỉ có `meta.pagination` cho API danh sách và dùng camelCase. |
| P0 | `3.Data mapping!A10:H16`, sheet DB | Password reset thuộc Platform Identity nhưng DD dùng các bảng không tồn tại `study.password_reset_tokens` và `study.user_sessions`. | `docs/BD/base/0. Study2Work_System_Architecture.md:61-75,150-220,294-301`; `docs/BD/diagram/CLASS/study2work_study_full_schema_seed.sql:19-30,239-301,323-385,446-481` | Route sang Identity; định nghĩa token hash, TTL, consumed/revoked status, delivery/outbox và không lưu plaintext. |
| P0 | `1.Request!A20:J24`, `2.Response!A15:H20` | `identifier` bị khai báo String(enum) `email\|phone` dù giá trị thực là email/phone; `accepted` là String(enum) và response `masked_destination/expires_at` có thể làm lộ account existence. | `docs/BD/02. Study2Work_Study_BasicDesign_Tai_Khoan_Xac_Thuc_Ho_So.md:88-102` | Khai báo String với oneOf format email/phone; response luôn chung cho tồn tại/không tồn tại, cân nhắc không trả channel/destination/TTL. |
| P0 | `3.Data mapping`, `4.Error` | Thiếu anti-enumeration timing, rate limit theo IP/identifier, token invalidation cũ, retry/dedup và delivery failure. | `docs/BD/02. Study2Work_Study_BasicDesign_Tai_Khoan_Xac_Thuc_Ho_So.md:88-102,176-186` | Bổ sung security rules/businessCode và kiểm thử abuse; không dùng `DATA_CONFLICT` chung. |
| P1 | `Cover!B15:G19`, `Lịch sử!A4:F4`, `00.Hướng dẫn!A4:B18` | Tài liệu được đánh dấu `VERIFIED` dù reviewer/approver chưa chỉ định; hướng dẫn còn tuyên bố gói nguồn không có schema và không còn placeholder. | `docs/BD/diagram/CLASS/study2work_study_full_schema_seed.sql:1-30` | Cập nhật inventory nguồn, loại bỏ placeholder, chuyển về `IN REVIEW` cho đến khi contract và mapping được duyệt. |

## Điều kiện duyệt lại

- [ ] Contract request/response và error catalog khớp BD/sequence hoặc có Change Request được phê duyệt.
- [ ] Mapping DB/service dùng owner, bảng, cột, khóa và transaction có thật; không còn placeholder.
- [ ] Envelope/casing/trace/pagination tuân theo kiến trúc chuẩn.
- [ ] Reviewer và approver được chỉ định; trạng thái chỉ chuyển `VERIFIED` sau khi đóng toàn bộ finding P0/P1.

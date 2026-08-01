# Review API DD — S2W-STUDY-API-007

- DD nguồn: `docs/DD/Study2Work_DD_API/02_Tai_khoan_xac_thuc_va_ho_so/S2W-STUDY-API-007_POST_auth_register.xlsx`
- Endpoint: `POST /api/v1/auth/register`
- Verdict: **CẦN SỬA**

## Findings

| Mức | Sheet/cell | Finding | Căn cứ BD | Cách sửa |
|---|---|---|---|---|
| P0 | `2.Response!A7:H11` và ví dụ thành công/lỗi | Envelope `{data, meta}` / `{error}`, `meta.request_id`, snake_case và pagination giả không khớp contract chuẩn. | `docs/BD/base/0. Study2Work_System_Architecture.md:632-700` | Đổi sang `success`, `businessCode`, `message`, `data`, `errors`, `traceId`; chỉ có `meta.pagination` cho API danh sách và dùng camelCase. |
| P0 | `1.Request!A20:J28`, `2.Response!A15:H24` | Contract không khớp sequence: thiếu `phone`; dùng snake_case; `accepted_terms_version` lại là Boolean; ví dụ thành công trả `account_status=ACTIVE` thay vì pending verification. | `docs/BD/diagram/SEQUENCE/03. Study2Work_Study_SEQ_Tai_Khoan_Xac_Thuc_Dang_Nhap.md:46-75` | Dùng `displayName`, `email`, `phone`, `password`, `acceptedTerms`; quy định exactly-one/at-least-one contact; response pending verification và `nextAction`. |
| P0 | `3.Data mapping!A12:H14`, sheet DB insert | DD ghi `password` trực tiếp vào `study.users`; kiến trúc quy định Platform Identity sở hữu credential/session và bảng `users` không có cột password. | `docs/BD/base/0. Study2Work_System_Architecture.md:61-75,150-220,294-301`; `docs/BD/diagram/CLASS/study2work_study_full_schema_seed.sql:19-30,239-301,323-385,446-481` | Gọi Platform Identity/Account Service; chỉ lưu projection user/profile cục bộ khi cần. Không lưu plaintext password. |
| P0 | `3.Data mapping`, `4.Error` | Chưa có persistence/version cho chấp thuận điều khoản, unique email/phone flow, password policy, rate-limit và dispatch verification/outbox. | `docs/BD/02. Study2Work_Study_BasicDesign_Tai_Khoan_Xac_Thuc_Ho_So.md:37-73` | Chốt terms acceptance model; transaction/saga với Identity; thêm duplicate contact, terms denied, weak password, throttling và delivery failure. |
| P1 | `Cover!B15:G19`, `Lịch sử!A4:F4`, `00.Hướng dẫn!A4:B18` | Tài liệu được đánh dấu `VERIFIED` dù reviewer/approver chưa chỉ định; hướng dẫn còn tuyên bố gói nguồn không có schema và không còn placeholder. | `docs/BD/diagram/CLASS/study2work_study_full_schema_seed.sql:1-30` | Cập nhật inventory nguồn, loại bỏ placeholder, chuyển về `IN REVIEW` cho đến khi contract và mapping được duyệt. |

## Điều kiện duyệt lại

- [ ] Contract request/response và error catalog khớp BD/sequence hoặc có Change Request được phê duyệt.
- [ ] Mapping DB/service dùng owner, bảng, cột, khóa và transaction có thật; không còn placeholder.
- [ ] Envelope/casing/trace/pagination tuân theo kiến trúc chuẩn.
- [ ] Reviewer và approver được chỉ định; trạng thái chỉ chuyển `VERIFIED` sau khi đóng toàn bộ finding P0/P1.

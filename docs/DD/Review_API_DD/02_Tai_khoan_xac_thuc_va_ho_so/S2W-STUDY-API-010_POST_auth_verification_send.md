# Review API DD — S2W-STUDY-API-010

- DD nguồn: `docs/DD/Study2Work_DD_API/02_Tai_khoan_xac_thuc_va_ho_so/S2W-STUDY-API-010_POST_auth_verification_send.xlsx`
- Endpoint: `POST /api/v1/auth/verification/send`
- Verdict: **CẦN SỬA**

## Findings

| Mức | Sheet/cell | Finding | Căn cứ BD | Cách sửa |
|---|---|---|---|---|
| P0 | `2.Response!A7:H11` và ví dụ thành công/lỗi | Envelope `{data, meta}` / `{error}`, `meta.request_id`, snake_case và pagination giả không khớp contract chuẩn. | `docs/BD/base/0. Study2Work_System_Architecture.md:632-700` | Đổi sang `success`, `businessCode`, `message`, `data`, `errors`, `traceId`; chỉ có `meta.pagination` cho API danh sách và dùng camelCase. |
| P0 | `3.Data mapping!A12:H14`, sheet DB | `study.contact_verifications` không tồn tại; verification/token thuộc Platform Identity. | `docs/BD/base/0. Study2Work_System_Architecture.md:61-75,150-220,294-301`; `docs/BD/diagram/CLASS/study2work_study_full_schema_seed.sql:19-30,239-301,323-385,446-481` | Thiết kế qua Identity service hoặc bổ sung schema owner chính thức; lưu token hash, TTL, status, attempts và consumed_at. |
| P0 | `1.Request!A20:J25`, `3.Data mapping!A10:H13` | API vừa yêu cầu bearer vừa cho client truyền `destination` tùy ý; chưa xác định resend cho pending user hay đổi contact, tạo nguy cơ gửi OTP tới đích ngoài tài khoản. | `docs/BD/02. Study2Work_Study_BasicDesign_Tai_Khoan_Xac_Thuc_Ho_So.md:56-73` | Tách/respecify use case; destination phải lấy từ pending identity hoặc change-request đã xác thực. |
| P0 | `4.Error`, `3.Data mapping` | BD yêu cầu chống spam nhưng DD thiếu cooldown, per-user/per-destination/IP limit, max attempts, resend semantics và delivery/outbox failure. | `docs/BD/02. Study2Work_Study_BasicDesign_Tai_Khoan_Xac_Thuc_Ho_So.md:56-73,176-186` | Định nghĩa rate limits, TTL, retry/dedup, businessCode và observability không lộ PII. |
| P1 | `Cover!B15:G19`, `Lịch sử!A4:F4`, `00.Hướng dẫn!A4:B18` | Tài liệu được đánh dấu `VERIFIED` dù reviewer/approver chưa chỉ định; hướng dẫn còn tuyên bố gói nguồn không có schema và không còn placeholder. | `docs/BD/diagram/CLASS/study2work_study_full_schema_seed.sql:1-30` | Cập nhật inventory nguồn, loại bỏ placeholder, chuyển về `IN REVIEW` cho đến khi contract và mapping được duyệt. |

## Điều kiện duyệt lại

- [ ] Contract request/response và error catalog khớp BD/sequence hoặc có Change Request được phê duyệt.
- [ ] Mapping DB/service dùng owner, bảng, cột, khóa và transaction có thật; không còn placeholder.
- [ ] Envelope/casing/trace/pagination tuân theo kiến trúc chuẩn.
- [ ] Reviewer và approver được chỉ định; trạng thái chỉ chuyển `VERIFIED` sau khi đóng toàn bộ finding P0/P1.

# Review API DD — S2W-STUDY-API-011

- DD nguồn: `docs/DD/Study2Work_DD_API/02_Tai_khoan_xac_thuc_va_ho_so/S2W-STUDY-API-011_POST_auth_verify_contact.xlsx`
- Endpoint: `POST /api/v1/auth/verify-contact`
- Verdict: **CẦN SỬA**

## Findings

| Mức | Sheet/cell | Finding | Căn cứ BD | Cách sửa |
|---|---|---|---|---|
| P0 | `2.Response!A7:H11` và ví dụ thành công/lỗi | Envelope `{data, meta}` / `{error}`, `meta.request_id`, snake_case và pagination giả không khớp contract chuẩn. | `docs/BD/base/0. Study2Work_System_Architecture.md:632-700` | Đổi sang `success`, `businessCode`, `message`, `data`, `errors`, `traceId`; chỉ có `meta.pagination` cho API danh sách và dùng camelCase. |
| P0 | `1.Request!A20:J25`, `2.Response!A15:H23` | Contract trực tiếp không khớp sequence: sequence dùng `userId`, `channel`, `verificationCode`; DD dùng `verification_id`, `token_or_otp`; response thiếu `userId`, dùng `next_route`, ví dụ status `ACTIVE`. | `docs/BD/diagram/SEQUENCE/03. Study2Work_Study_SEQ_Tai_Khoan_Xac_Thuc_Dang_Nhap.md:78-104` | Dùng contract sequence hoặc lập CR phê duyệt thay đổi; response `accountStatus=VERIFIED`, `nextAction=START_ONBOARDING`. |
| P0 | `3.Data mapping!A12:H14`, sheet DB | `contact_verifications` không có trong DDL và verification thuộc Platform Identity; flow update chưa thể triển khai. | `docs/BD/base/0. Study2Work_System_Architecture.md:61-75,150-220,294-301`; `docs/BD/diagram/CLASS/study2work_study_full_schema_seed.sql:19-30,239-301,323-385,446-481` | Thực hiện atomic verify/consume token và cập nhật identity status tại owner; Study nhận event/projection. |
| P0 | `2.Response!A16:H19`, `4.Error` | `verified` là String(enum) thay vì Boolean; thiếu invalid/expired/used code, max attempts, anti-replay và uniqueness/race handling. | `docs/BD/02. Study2Work_Study_BasicDesign_Tai_Khoan_Xac_Thuc_Ho_So.md:56-73` | Sửa type và thêm state machine/error codes; token chỉ consume một lần trong transaction. |
| P1 | `Cover!B15:G19`, `Lịch sử!A4:F4`, `00.Hướng dẫn!A4:B18` | Tài liệu được đánh dấu `VERIFIED` dù reviewer/approver chưa chỉ định; hướng dẫn còn tuyên bố gói nguồn không có schema và không còn placeholder. | `docs/BD/diagram/CLASS/study2work_study_full_schema_seed.sql:1-30` | Cập nhật inventory nguồn, loại bỏ placeholder, chuyển về `IN REVIEW` cho đến khi contract và mapping được duyệt. |

## Điều kiện duyệt lại

- [ ] Contract request/response và error catalog khớp BD/sequence hoặc có Change Request được phê duyệt.
- [ ] Mapping DB/service dùng owner, bảng, cột, khóa và transaction có thật; không còn placeholder.
- [ ] Envelope/casing/trace/pagination tuân theo kiến trúc chuẩn.
- [ ] Reviewer và approver được chỉ định; trạng thái chỉ chuyển `VERIFIED` sau khi đóng toàn bộ finding P0/P1.

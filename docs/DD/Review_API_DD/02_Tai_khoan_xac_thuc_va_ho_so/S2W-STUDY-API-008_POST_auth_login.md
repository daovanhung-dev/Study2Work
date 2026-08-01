# Review API DD — S2W-STUDY-API-008

- DD nguồn: `docs/DD/Study2Work_DD_API/02_Tai_khoan_xac_thuc_va_ho_so/S2W-STUDY-API-008_POST_auth_login.xlsx`
- Endpoint: `POST /api/v1/auth/login`
- Verdict: **CẦN SỬA**

## Findings

| Mức | Sheet/cell | Finding | Căn cứ BD | Cách sửa |
|---|---|---|---|---|
| P0 | `2.Response!A7:H11` và ví dụ thành công/lỗi | Envelope `{data, meta}` / `{error}`, `meta.request_id`, snake_case và pagination giả không khớp contract chuẩn. | `docs/BD/base/0. Study2Work_System_Architecture.md:632-700` | Đổi sang `success`, `businessCode`, `message`, `data`, `errors`, `traceId`; chỉ có `meta.pagination` cho API danh sách và dùng camelCase. |
| P0 | `2.Response!A9:E11`, `A15:H24` | Login thành công khai báo HTTP 201; response khác sequence, nhiều object/count dùng String và trả refresh token trong JSON. | `docs/BD/diagram/SEQUENCE/03. Study2Work_Study_SEQ_Tai_Khoan_Xac_Thuc_Dang_Nhap.md:107-136` | Dùng HTTP 200; trả `accessToken`, object `user`, `nextAction`; chốt refresh token qua secure HttpOnly cookie hoặc contract bảo mật rõ. |
| P0 | `3.Data mapping!A12:H14`, sheet DB | DD tạo session trong `study.user_sessions` không tồn tại và đưa `identifier/password` vào mapping ghi; Identity mới là owner credential/session. | `docs/BD/base/0. Study2Work_System_Architecture.md:61-75,150-220,294-301`; `docs/BD/diagram/CLASS/study2work_study_full_schema_seed.sql:19-30,239-301,323-385,446-481` | Ủy quyền login/session cho Platform Identity; Study chỉ compose profile/onboarding/active path sau khi xác thực. |
| P0 | `4.Error` | Error catalog thiếu invalid credentials, locked account, suspended account, unverified action và rate limit; dùng `DATA_CONFLICT` chung không đủ. | `docs/BD/02. Study2Work_Study_BasicDesign_Tai_Khoan_Xac_Thuc_Ho_So.md:75-86,124-145` | Bổ sung businessCode ổn định và HTTP mapping; không tiết lộ email/phone tồn tại. |
| P1 | `Cover!B15:G19`, `Lịch sử!A4:F4`, `00.Hướng dẫn!A4:B18` | Tài liệu được đánh dấu `VERIFIED` dù reviewer/approver chưa chỉ định; hướng dẫn còn tuyên bố gói nguồn không có schema và không còn placeholder. | `docs/BD/diagram/CLASS/study2work_study_full_schema_seed.sql:1-30` | Cập nhật inventory nguồn, loại bỏ placeholder, chuyển về `IN REVIEW` cho đến khi contract và mapping được duyệt. |

## Điều kiện duyệt lại

- [ ] Contract request/response và error catalog khớp BD/sequence hoặc có Change Request được phê duyệt.
- [ ] Mapping DB/service dùng owner, bảng, cột, khóa và transaction có thật; không còn placeholder.
- [ ] Envelope/casing/trace/pagination tuân theo kiến trúc chuẩn.
- [ ] Reviewer và approver được chỉ định; trạng thái chỉ chuyển `VERIFIED` sau khi đóng toàn bộ finding P0/P1.

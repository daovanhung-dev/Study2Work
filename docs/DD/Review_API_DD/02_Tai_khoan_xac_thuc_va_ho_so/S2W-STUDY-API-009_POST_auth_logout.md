# Review API DD — S2W-STUDY-API-009

- DD nguồn: `docs/DD/Study2Work_DD_API/02_Tai_khoan_xac_thuc_va_ho_so/S2W-STUDY-API-009_POST_auth_logout.xlsx`
- Endpoint: `POST /api/v1/auth/logout`
- Verdict: **CẦN SỬA**

## Findings

| Mức | Sheet/cell | Finding | Căn cứ BD | Cách sửa |
|---|---|---|---|---|
| P0 | `2.Response!A7:H11` và ví dụ thành công/lỗi | Envelope `{data, meta}` / `{error}`, `meta.request_id`, snake_case và pagination giả không khớp contract chuẩn. | `docs/BD/base/0. Study2Work_System_Architecture.md:632-700` | Đổi sang `success`, `businessCode`, `message`, `data`, `errors`, `traceId`; chỉ có `meta.pagination` cho API danh sách và dùng camelCase. |
| P0 | `1.Request!A8:J25`, `3.Data mapping!A10:H14` | Logout yêu cầu permission `study.admin.manage`/RBAC không phù hợp; mọi session đã xác thực phải tự logout được, kể cả khi tài khoản bị hạn chế. | `docs/BD/02. Study2Work_Study_BasicDesign_Tai_Khoan_Xac_Thuc_Ho_So.md:75-86`; `docs/BD/base/0. Study2Work_System_Architecture.md:61-75,150-220,294-301` | Chỉ yêu cầu session/access token hợp lệ; route tới Platform Identity để revoke đúng session/all sessions theo contract. |
| P0 | `3.Data mapping!A12:H14`, sheet DB | `study.user_sessions` không tồn tại và session/revocation không thuộc Study. | `docs/BD/base/0. Study2Work_System_Architecture.md:61-75,150-220,294-301`; `docs/BD/diagram/CLASS/study2work_study_full_schema_seed.sql:19-30,239-301,323-385,446-481` | Loại mapping DB Study; định nghĩa IdP endpoint, token identifier/hash, idempotent revoke và audit. |
| P1 | `1.Request!A21:J25` | Nhận raw refresh token trong body mâu thuẫn phương án cookie bảo mật và không nói rõ logout current/all devices. | `docs/BD/base/0. Study2Work_System_Architecture.md:203-219` | Chốt một cơ chế token, CSRF nếu cookie, và tham số scope rõ; không log token. |
| P1 | `Cover!B15:G19`, `Lịch sử!A4:F4`, `00.Hướng dẫn!A4:B18` | Tài liệu được đánh dấu `VERIFIED` dù reviewer/approver chưa chỉ định; hướng dẫn còn tuyên bố gói nguồn không có schema và không còn placeholder. | `docs/BD/diagram/CLASS/study2work_study_full_schema_seed.sql:1-30` | Cập nhật inventory nguồn, loại bỏ placeholder, chuyển về `IN REVIEW` cho đến khi contract và mapping được duyệt. |

## Điều kiện duyệt lại

- [ ] Contract request/response và error catalog khớp BD/sequence hoặc có Change Request được phê duyệt.
- [ ] Mapping DB/service dùng owner, bảng, cột, khóa và transaction có thật; không còn placeholder.
- [ ] Envelope/casing/trace/pagination tuân theo kiến trúc chuẩn.
- [ ] Reviewer và approver được chỉ định; trạng thái chỉ chuyển `VERIFIED` sau khi đóng toàn bộ finding P0/P1.

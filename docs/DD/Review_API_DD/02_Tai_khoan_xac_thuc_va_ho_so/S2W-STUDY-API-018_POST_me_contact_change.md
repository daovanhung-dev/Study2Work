# Review API DD — S2W-STUDY-API-018

- DD nguồn: `docs/DD/Study2Work_DD_API/02_Tai_khoan_xac_thuc_va_ho_so/S2W-STUDY-API-018_POST_me_contact_change.xlsx`
- Endpoint: `POST /api/v1/me/contact-change`
- Verdict: **CẦN SỬA**

## Findings

| Mức | Sheet/cell | Finding | Căn cứ BD | Cách sửa |
|---|---|---|---|---|
| P0 | `2.Response!A7:H11` và ví dụ thành công/lỗi | Envelope `{data, meta}` / `{error}`, `meta.request_id`, snake_case và pagination giả không khớp contract chuẩn. | `docs/BD/base/0. Study2Work_System_Architecture.md:632-700` | Đổi sang `success`, `businessCode`, `message`, `data`, `errors`, `traceId`; chỉ có `meta.pagination` cho API danh sách và dùng camelCase. |
| P0 | `3.Data mapping!A12:H16`, sheet DB | `contact_verifications` không có trong schema và đổi email/phone thuộc Platform Identity. | `docs/BD/base/0. Study2Work_System_Architecture.md:61-75,150-220,294-301`; `docs/BD/diagram/CLASS/study2work_study_full_schema_seed.sql:19-30,239-301,323-385,446-481` | Tạo change request tại Identity với new contact normalized, token hash, TTL, attempts, status; Study chỉ nhận projection/event. |
| P0 | `1.Request!A20:J26` | `new_value` không có validation phụ thuộc `contact_type`; `current_password` optional nhưng không có step-up rule cho local/social/phone-only account. | `docs/BD/02. Study2Work_Study_BasicDesign_Tai_Khoan_Xac_Thuc_Ho_So.md:104-123` | Định nghĩa oneOf email/phone, normalization, duplicate check và step-up authentication theo credential type. |
| P0 | `3.Data mapping`, `4.Error` | Thiếu nguyên tắc không thay contact hiện tại trước confirm, cooldown/rate-limit, duplicate contact, token security và delivery failure. | `docs/BD/02. Study2Work_Study_BasicDesign_Tai_Khoan_Xac_Thuc_Ho_So.md:37-145,163-186` | Giữ contact cũ active; thêm state machine/error codes, outbox và audit PII-safe. |
| P1 | `Cover!B15:G19`, `Lịch sử!A4:F4`, `00.Hướng dẫn!A4:B18` | Tài liệu được đánh dấu `VERIFIED` dù reviewer/approver chưa chỉ định; hướng dẫn còn tuyên bố gói nguồn không có schema và không còn placeholder. | `docs/BD/diagram/CLASS/study2work_study_full_schema_seed.sql:1-30` | Cập nhật inventory nguồn, loại bỏ placeholder, chuyển về `IN REVIEW` cho đến khi contract và mapping được duyệt. |

## Điều kiện duyệt lại

- [ ] Contract request/response và error catalog khớp BD/sequence hoặc có Change Request được phê duyệt.
- [ ] Mapping DB/service dùng owner, bảng, cột, khóa và transaction có thật; không còn placeholder.
- [ ] Envelope/casing/trace/pagination tuân theo kiến trúc chuẩn.
- [ ] Reviewer và approver được chỉ định; trạng thái chỉ chuyển `VERIFIED` sau khi đóng toàn bộ finding P0/P1.

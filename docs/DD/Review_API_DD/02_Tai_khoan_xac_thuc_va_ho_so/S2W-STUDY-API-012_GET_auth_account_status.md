# Review API DD — S2W-STUDY-API-012

- DD nguồn: `docs/DD/Study2Work_DD_API/02_Tai_khoan_xac_thuc_va_ho_so/S2W-STUDY-API-012_GET_auth_account_status.xlsx`
- Endpoint: `GET /api/v1/auth/account-status`
- Verdict: **CẦN SỬA**

## Findings

| Mức | Sheet/cell | Finding | Căn cứ BD | Cách sửa |
|---|---|---|---|---|
| P0 | `2.Response!A7:H11` và ví dụ thành công/lỗi | Envelope `{data, meta}` / `{error}`, `meta.request_id`, snake_case và pagination giả không khớp contract chuẩn. | `docs/BD/base/0. Study2Work_System_Architecture.md:632-700` | Đổi sang `success`, `businessCode`, `message`, `data`, `errors`, `traceId`; chỉ có `meta.pagination` cho API danh sách và dùng camelCase. |
| P0 | `2.Response!A15:H22`, `3.Data mapping!A12:H16` | `verification_status`, `onboarding_status`, `active_path`, `restrictions`, `next_route` bị map như cột của `users`; schema chỉ có `account_status` và `contact_verified`. | `docs/BD/diagram/CLASS/study2work_study_full_schema_seed.sql:239-301,340-359` | Compose từ Identity account state + `onboarding_records` + active enrollment; định nghĩa object/array schema và precedence. |
| P1 | `Overview`, `3.Data mapping`, API-020 | Endpoint suy dẫn trùng trách nhiệm đáng kể với `/api/v1/me/navigation-context`; chưa rõ consumer, thời điểm gọi và source of truth. | `docs/BD/02. Study2Work_Study_BasicDesign_Tai_Khoan_Xac_Thuc_Ho_So.md:75-86,163-172` | Gộp hoặc tách rõ: account-status thuần Identity và navigation-context cho routing; PO/API owner phê duyệt. |
| P1 | `3.Data mapping!A12:H14` | WHERE còn `Theo phạm vi...`, ORDER BY generic và không có join/key cụ thể. | `docs/BD/diagram/CLASS/study2work_study_full_schema_seed.sql:19-30,239-301,323-385,446-481` | Viết truy vấn/composition cụ thể theo `users.id`, `onboarding_records.user_id`, enrollment ACTIVE. |
| P1 | `Cover!B15:G19`, `Lịch sử!A4:F4`, `00.Hướng dẫn!A4:B18` | Tài liệu được đánh dấu `VERIFIED` dù reviewer/approver chưa chỉ định; hướng dẫn còn tuyên bố gói nguồn không có schema và không còn placeholder. | `docs/BD/diagram/CLASS/study2work_study_full_schema_seed.sql:1-30` | Cập nhật inventory nguồn, loại bỏ placeholder, chuyển về `IN REVIEW` cho đến khi contract và mapping được duyệt. |

## Điều kiện duyệt lại

- [ ] Contract request/response và error catalog khớp BD/sequence hoặc có Change Request được phê duyệt.
- [ ] Mapping DB/service dùng owner, bảng, cột, khóa và transaction có thật; không còn placeholder.
- [ ] Envelope/casing/trace/pagination tuân theo kiến trúc chuẩn.
- [ ] Reviewer và approver được chỉ định; trạng thái chỉ chuyển `VERIFIED` sau khi đóng toàn bộ finding P0/P1.

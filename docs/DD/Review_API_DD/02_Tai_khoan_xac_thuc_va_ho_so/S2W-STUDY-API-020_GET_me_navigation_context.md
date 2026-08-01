# Review API DD — S2W-STUDY-API-020

- DD nguồn: `docs/DD/Study2Work_DD_API/02_Tai_khoan_xac_thuc_va_ho_so/S2W-STUDY-API-020_GET_me_navigation_context.xlsx`
- Endpoint: `GET /api/v1/me/navigation-context`
- Verdict: **CẦN SỬA**

## Findings

| Mức | Sheet/cell | Finding | Căn cứ BD | Cách sửa |
|---|---|---|---|---|
| P0 | `2.Response!A7:H11` và ví dụ thành công/lỗi | Envelope `{data, meta}` / `{error}`, `meta.request_id`, snake_case và pagination giả không khớp contract chuẩn. | `docs/BD/base/0. Study2Work_System_Architecture.md:632-700` | Đổi sang `success`, `businessCode`, `message`, `data`, `errors`, `traceId`; chỉ có `meta.pagination` cho API danh sách và dùng camelCase. |
| P0 | `2.Response!A15:H23`, `3.Data mapping!A12:H16` | `verification_required`, `onboarding_required`, `active_path`, `can_activate_path`, `next_route` bị map như cột `users`; `users.user_id` trong WHERE cũng sai vì PK là `users.id`. | `docs/BD/diagram/CLASS/study2work_study_full_schema_seed.sql:239-301,340-359` | Compose từ Identity status, onboarding và active enrollment; dùng khóa thật và định nghĩa object/Boolean đúng type. |
| P0 | `2.Response!A19:H22`, `3.Data mapping!A13:H13` | `active_path`/`can_activate_path` dùng String; routing precedence chưa rõ cho suspended, pending verification, onboarding chưa xong, có/không active path. | `docs/BD/02. Study2Work_Study_BasicDesign_Tai_Khoan_Xac_Thuc_Ho_So.md:75-86,124-145,163-172` | Định nghĩa decision table/enum `nextAction` ổn định và thứ tự ưu tiên; không để frontend suy đoán route. |
| P1 | `Overview`, API-012 | Endpoint suy dẫn chồng lấn `/api/v1/auth/account-status`; chưa chốt source of truth, cache/staleness và consistency khi Identity/local projection lệch. | `docs/BD/base/0. Study2Work_System_Architecture.md:61-75,150-220,294-301` | Tách rõ account state và navigation composition hoặc gộp; định nghĩa timeout/fallback, freshness/version và PO/API owner phê duyệt. |
| P1 | `Cover!B15:G19`, `Lịch sử!A4:F4`, `00.Hướng dẫn!A4:B18` | Tài liệu được đánh dấu `VERIFIED` dù reviewer/approver chưa chỉ định; hướng dẫn còn tuyên bố gói nguồn không có schema và không còn placeholder. | `docs/BD/diagram/CLASS/study2work_study_full_schema_seed.sql:1-30` | Cập nhật inventory nguồn, loại bỏ placeholder, chuyển về `IN REVIEW` cho đến khi contract và mapping được duyệt. |

## Điều kiện duyệt lại

- [ ] Contract request/response và error catalog khớp BD/sequence hoặc có Change Request được phê duyệt.
- [ ] Mapping DB/service dùng owner, bảng, cột, khóa và transaction có thật; không còn placeholder.
- [ ] Envelope/casing/trace/pagination tuân theo kiến trúc chuẩn.
- [ ] Reviewer và approver được chỉ định; trạng thái chỉ chuyển `VERIFIED` sau khi đóng toàn bộ finding P0/P1.

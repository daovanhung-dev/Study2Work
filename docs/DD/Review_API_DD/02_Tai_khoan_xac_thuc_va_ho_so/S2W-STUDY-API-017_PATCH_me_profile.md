# Review API DD — S2W-STUDY-API-017

- DD nguồn: `docs/DD/Study2Work_DD_API/02_Tai_khoan_xac_thuc_va_ho_so/S2W-STUDY-API-017_PATCH_me_profile.xlsx`
- Endpoint: `PATCH /api/v1/me/profile`
- Verdict: **CẦN SỬA**

## Findings

| Mức | Sheet/cell | Finding | Căn cứ BD | Cách sửa |
|---|---|---|---|---|
| P0 | `2.Response!A7:H11` và ví dụ thành công/lỗi | Envelope `{data, meta}` / `{error}`, `meta.request_id`, snake_case và pagination giả không khớp contract chuẩn. | `docs/BD/base/0. Study2Work_System_Architecture.md:632-700` | Đổi sang `success`, `businessCode`, `message`, `data`, `errors`, `traceId`; chỉ có `meta.pagination` cho API danh sách và dùng camelCase. |
| P0 | `1.Request!A20:J31`, `3.Data mapping!A12:H16` | Field không khớp schema: `display_name` thuộc `users`; `province` phải map/chốt với `city`; `primary_goal` với `learning_goal`; `preferred_time_slots` không tồn tại; thiếu `known_technologies`. | `docs/BD/02. Study2Work_Study_BasicDesign_Tai_Khoan_Xac_Thuc_Ho_So.md:104-123`; `docs/BD/diagram/CLASS/study2work_study_full_schema_seed.sql:239-301` | Đồng bộ contract với data dictionary; update `users` và `user_profiles` theo transaction hoặc tách endpoint; bổ sung migration cho field mới. |
| P0 | `1.Request!A20:J31` | Mọi field đều optional nhưng không yêu cầu ít nhất một field; chưa có semantics cho absent/null/empty và xóa giá trị. | `docs/BD/02. Study2Work_Study_BasicDesign_Tai_Khoan_Xac_Thuc_Ho_So.md:37-145,163-186` | Định nghĩa PATCH merge semantics, at-least-one field, validation per field và explicit clear behavior. |
| P1 | `3.Data mapping`, `2.Response!A15:H19` | Thiếu optimistic concurrency/version; `updated_profile`/`updated_fields` chưa có schema; chưa nói đồng bộ với onboarding. | `docs/BD/02. Study2Work_Study_BasicDesign_Tai_Khoan_Xac_Thuc_Ho_So.md:104-123` | Chốt source of truth/profile-onboarding sync, ETag/version hoặc last-write policy, response schema đầy đủ. |
| P1 | `Cover!B15:G19`, `Lịch sử!A4:F4`, `00.Hướng dẫn!A4:B18` | Tài liệu được đánh dấu `VERIFIED` dù reviewer/approver chưa chỉ định; hướng dẫn còn tuyên bố gói nguồn không có schema và không còn placeholder. | `docs/BD/diagram/CLASS/study2work_study_full_schema_seed.sql:1-30` | Cập nhật inventory nguồn, loại bỏ placeholder, chuyển về `IN REVIEW` cho đến khi contract và mapping được duyệt. |

## Điều kiện duyệt lại

- [ ] Contract request/response và error catalog khớp BD/sequence hoặc có Change Request được phê duyệt.
- [ ] Mapping DB/service dùng owner, bảng, cột, khóa và transaction có thật; không còn placeholder.
- [ ] Envelope/casing/trace/pagination tuân theo kiến trúc chuẩn.
- [ ] Reviewer và approver được chỉ định; trạng thái chỉ chuyển `VERIFIED` sau khi đóng toàn bộ finding P0/P1.

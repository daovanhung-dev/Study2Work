# Review API DD — S2W-STUDY-API-016

- DD nguồn: `docs/DD/Study2Work_DD_API/02_Tai_khoan_xac_thuc_va_ho_so/S2W-STUDY-API-016_GET_me_profile.xlsx`
- Endpoint: `GET /api/v1/me/profile`
- Verdict: **CẦN SỬA**

## Findings

| Mức | Sheet/cell | Finding | Căn cứ BD | Cách sửa |
|---|---|---|---|---|
| P0 | `2.Response!A7:H11` và ví dụ thành công/lỗi | Envelope `{data, meta}` / `{error}`, `meta.request_id`, snake_case và pagination giả không khớp contract chuẩn. | `docs/BD/base/0. Study2Work_System_Architecture.md:632-700` | Đổi sang `success`, `businessCode`, `message`, `data`, `errors`, `traceId`; chỉ có `meta.pagination` cho API danh sách và dùng camelCase. |
| P0 | `2.Response!A15:H21` | `basic_profile`, `verified_contacts`, `learning_profile`, notification/path summaries thiếu nested schema; một số field khai báo String dù là object/list. | `docs/BD/02. Study2Work_Study_BasicDesign_Tai_Khoan_Xac_Thuc_Ho_So.md:104-123` | Định nghĩa từng field con, type, nullability, masking contact, permissions và examples. |
| P0 | `3.Data mapping!A12:H16` | DD map tất cả vào `user_profiles`, nhưng dữ liệu thực nằm ở `users`, `user_profiles`, `onboarding_records`, enrollments; notification preferences chưa có nguồn trong schema. | `docs/BD/diagram/CLASS/study2work_study_full_schema_seed.sql:239-301,340-359` | Viết mapping/join cụ thể; bỏ summary không có nguồn hoặc bổ sung schema/service owner. |
| P1 | `3.Data mapping!A12:H15` | ORDER BY/side-effect template không liên quan API profile singleton; thiếu field-level PII minimization và cache/no-store. | `docs/BD/02. Study2Work_Study_BasicDesign_Tai_Khoan_Xac_Thuc_Ho_So.md:104-123` | Bỏ template thừa; chỉ trả profile của chính user, mask contact, đặt cache policy phù hợp. |
| P1 | `Cover!B15:G19`, `Lịch sử!A4:F4`, `00.Hướng dẫn!A4:B18` | Tài liệu được đánh dấu `VERIFIED` dù reviewer/approver chưa chỉ định; hướng dẫn còn tuyên bố gói nguồn không có schema và không còn placeholder. | `docs/BD/diagram/CLASS/study2work_study_full_schema_seed.sql:1-30` | Cập nhật inventory nguồn, loại bỏ placeholder, chuyển về `IN REVIEW` cho đến khi contract và mapping được duyệt. |

## Điều kiện duyệt lại

- [ ] Contract request/response và error catalog khớp BD/sequence hoặc có Change Request được phê duyệt.
- [ ] Mapping DB/service dùng owner, bảng, cột, khóa và transaction có thật; không còn placeholder.
- [ ] Envelope/casing/trace/pagination tuân theo kiến trúc chuẩn.
- [ ] Reviewer và approver được chỉ định; trạng thái chỉ chuyển `VERIFIED` sau khi đóng toàn bộ finding P0/P1.

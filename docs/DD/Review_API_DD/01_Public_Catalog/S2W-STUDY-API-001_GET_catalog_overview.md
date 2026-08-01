# Review API DD — S2W-STUDY-API-001

- DD nguồn: `docs/DD/Study2Work_DD_API/01_Public_Catalog/S2W-STUDY-API-001_GET_catalog_overview.xlsx`
- Endpoint: `GET /api/v1/catalog/overview`
- Verdict: **CẦN SỬA**

## Findings

| Mức | Sheet/cell | Finding | Căn cứ BD | Cách sửa |
|---|---|---|---|---|
| P0 | `2.Response!A7:H11` và ví dụ thành công/lỗi | Envelope `{data, meta}` / `{error}`, `meta.request_id`, snake_case và pagination giả không khớp contract chuẩn. | `docs/BD/base/0. Study2Work_System_Architecture.md:632-700` | Đổi sang `success`, `businessCode`, `message`, `data`, `errors`, `traceId`; chỉ có `meta.pagination` cho API danh sách và dùng camelCase. |
| P0 | `2.Response!A15:H23`, `3.Data mapping!A12:H14` | API suy dẫn `catalog/overview` ánh xạ toàn bộ payload vào `study.vw_catalog_overview`, nhưng schema không có view này; các cột `value_proposition`, `target_users`, `featured_*` cũng không tồn tại. | `docs/BD/01. Study2Work_Study_BasicDesign_Public_Catalog.md:16-32`; `docs/BD/diagram/CLASS/study2work_study_full_schema_seed.sql:19-30,239-301,323-385,446-481` | Chốt endpoint/payload với Product Owner; tạo nguồn cấu hình/CMS thật hoặc định nghĩa view/migration cụ thể, không dùng cột ảo. |
| P1 | `2.Response!A15:H23` | Các mảng/khối nội dung của trang giới thiệu chưa có item schema, required/nullability, thứ tự và quy tắc locale/fallback. | `docs/BD/01. Study2Work_Study_BasicDesign_Public_Catalog.md:16-32` | Định nghĩa object schema cho từng section, locale enum/default/fallback và thứ tự hiển thị. |
| P1 | `3.Data mapping!A10:H13`, `4.Error` | Endpoint public vẫn kéo `users/user_roles` và chứa lỗi 401/403/RBAC không gắn với hành vi guest. | `docs/BD/01. Study2Work_Study_BasicDesign_Public_Catalog.md:169-179` | Cho phép guest; chỉ đọc learner context tùy chọn khi token hợp lệ, không biến token thiếu thành lỗi. |
| P1 | `Cover!B15:G19`, `Lịch sử!A4:F4`, `00.Hướng dẫn!A4:B18` | Tài liệu được đánh dấu `VERIFIED` dù reviewer/approver chưa chỉ định; hướng dẫn còn tuyên bố gói nguồn không có schema và không còn placeholder. | `docs/BD/diagram/CLASS/study2work_study_full_schema_seed.sql:1-30` | Cập nhật inventory nguồn, loại bỏ placeholder, chuyển về `IN REVIEW` cho đến khi contract và mapping được duyệt. |

## Điều kiện duyệt lại

- [ ] Contract request/response và error catalog khớp BD/sequence hoặc có Change Request được phê duyệt.
- [ ] Mapping DB/service dùng owner, bảng, cột, khóa và transaction có thật; không còn placeholder.
- [ ] Envelope/casing/trace/pagination tuân theo kiến trúc chuẩn.
- [ ] Reviewer và approver được chỉ định; trạng thái chỉ chuyển `VERIFIED` sau khi đóng toàn bộ finding P0/P1.

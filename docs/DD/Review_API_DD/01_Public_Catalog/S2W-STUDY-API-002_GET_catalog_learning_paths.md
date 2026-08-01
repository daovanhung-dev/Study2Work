# Review API DD — S2W-STUDY-API-002

- DD nguồn: `docs/DD/Study2Work_DD_API/01_Public_Catalog/S2W-STUDY-API-002_GET_catalog_learning_paths.xlsx`
- Endpoint: `GET /api/v1/catalog/learning-paths`
- Verdict: **CẦN SỬA**

## Findings

| Mức | Sheet/cell | Finding | Căn cứ BD | Cách sửa |
|---|---|---|---|---|
| P0 | `2.Response!A7:H11` và ví dụ thành công/lỗi | Envelope `{data, meta}` / `{error}`, `meta.request_id`, snake_case và pagination giả không khớp contract chuẩn. | `docs/BD/base/0. Study2Work_System_Architecture.md:632-700` | Đổi sang `success`, `businessCode`, `message`, `data`, `errors`, `traceId`; chỉ có `meta.pagination` cho API danh sách và dùng camelCase. |
| P0 | `1.Request!A20:J29` | Tên query khác contract trực tiếp: DD dùng `q`, `difficulty`, `duration_min`, `duration_max`, `page_size`; sequence quy định `keyword`, `goal`, `level`, `durationMaxHours`, `page`, `pageSize`. | `docs/BD/diagram/SEQUENCE/02. Study2Work_Study_SEQ_Public_Catalog.md:46-60` | Đồng bộ chính xác tên, kiểu, default/range và ví dụ request theo sequence. |
| P0 | `2.Response!A15:H28` | Response dùng `name`, `short_description`, `estimated_duration`, `difficulty`, `publication_status` thay vì `title`, `summary`, `estimatedHours`, `level`, `publicStatus`, `learnerState`. | `docs/BD/diagram/SEQUENCE/02. Study2Work_Study_SEQ_Public_Catalog.md:63-91` | Thay contract response theo payload sequence; định nghĩa enum `learnerState` và object list rõ. |
| P0 | `3.Data mapping!A12:H14`, các sheet DB | SQL/cột đề xuất không khớp DDL: `short_description`, `outcomes`, `target_users`, `course_count`, `difficulty`, `image_url`, `labels`, `publication_status`, `search_document`, `goal`, `admin_order`, `updated_at` không có trong `learning_paths`. | `docs/BD/diagram/CLASS/study2work_study_full_schema_seed.sql:19-30,239-301,323-385,446-481` | Map sang `title`, `summary`, `level`, `estimated_hours`, `publish_status`; tính `courseCount` từ `learning_path_courses`; bổ sung migration nếu thật sự cần field mới. |
| P1 | `4.Error` | Lỗi account/onboarding/active-path được áp cho danh sách public; BD yêu cầu vẫn hiển thị catalog và chỉ bổ sung trạng thái cá nhân khi đăng nhập. | `docs/BD/diagram/SEQUENCE/02. Study2Work_Study_SEQ_Public_Catalog.md:15-40,46-134` | Bỏ lỗi chặn catalog; token/learner context lỗi phải degrade an toàn hoặc được đặc tả riêng. |
| P1 | `Cover!B15:G19`, `Lịch sử!A4:F4`, `00.Hướng dẫn!A4:B18` | Tài liệu được đánh dấu `VERIFIED` dù reviewer/approver chưa chỉ định; hướng dẫn còn tuyên bố gói nguồn không có schema và không còn placeholder. | `docs/BD/diagram/CLASS/study2work_study_full_schema_seed.sql:1-30` | Cập nhật inventory nguồn, loại bỏ placeholder, chuyển về `IN REVIEW` cho đến khi contract và mapping được duyệt. |

## Điều kiện duyệt lại

- [ ] Contract request/response và error catalog khớp BD/sequence hoặc có Change Request được phê duyệt.
- [ ] Mapping DB/service dùng owner, bảng, cột, khóa và transaction có thật; không còn placeholder.
- [ ] Envelope/casing/trace/pagination tuân theo kiến trúc chuẩn.
- [ ] Reviewer và approver được chỉ định; trạng thái chỉ chuyển `VERIFIED` sau khi đóng toàn bộ finding P0/P1.

# Review API DD — S2W-STUDY-API-003

- DD nguồn: `docs/DD/Study2Work_DD_API/01_Public_Catalog/S2W-STUDY-API-003_GET_catalog_learning_paths_slug.xlsx`
- Endpoint: `GET /api/v1/catalog/learning-paths/{slug}`
- Verdict: **CẦN SỬA**

## Findings

| Mức | Sheet/cell | Finding | Căn cứ BD | Cách sửa |
|---|---|---|---|---|
| P0 | `2.Response!A7:H11` và ví dụ thành công/lỗi | Envelope `{data, meta}` / `{error}`, `meta.request_id`, snake_case và pagination giả không khớp contract chuẩn. | `docs/BD/base/0. Study2Work_System_Architecture.md:632-700` | Đổi sang `success`, `businessCode`, `message`, `data`, `errors`, `traceId`; chỉ có `meta.pagination` cho API danh sách và dùng camelCase. |
| P0 | `2.Response!A15:H26` | `data.path` được khai báo `String`; danh sách course/outcome/target-user không có item schema, nên frontend không thể triển khai ổn định. | `docs/BD/01. Study2Work_Study_BasicDesign_Public_Catalog.md:74-97` | Định nghĩa object `path`, course summary item, CTA/learner state, required/nullability và ví dụ đầy đủ. |
| P0 | `3.Data mapping!A12:H14`, các sheet DB | Mapping dựa trên nhiều cột/quan hệ ảo và `<FK condition>`; không map được trực tiếp với `learning_paths`, `learning_path_courses`, `courses` trong DDL. | `docs/BD/diagram/CLASS/study2work_study_full_schema_seed.sql:19-30,239-301,323-385,446-481` | Viết SQL cụ thể theo PK/FK thật, lọc `publish_status` và sắp xếp theo `learning_path_courses.order_index`. |
| P1 | `2.Response` và `4.Error` | API singleton có pagination giả và lỗi account/onboarding/active-path không phù hợp với trang chi tiết public. | `docs/BD/01. Study2Work_Study_BasicDesign_Public_Catalog.md:48-139,169-179` | Bỏ pagination; unpublished/not-public nên trả 404 an toàn, learner state chỉ là dữ liệu bổ sung. |
| P1 | `Cover!B15:G19`, `Lịch sử!A4:F4`, `00.Hướng dẫn!A4:B18` | Tài liệu được đánh dấu `VERIFIED` dù reviewer/approver chưa chỉ định; hướng dẫn còn tuyên bố gói nguồn không có schema và không còn placeholder. | `docs/BD/diagram/CLASS/study2work_study_full_schema_seed.sql:1-30` | Cập nhật inventory nguồn, loại bỏ placeholder, chuyển về `IN REVIEW` cho đến khi contract và mapping được duyệt. |

## Điều kiện duyệt lại

- [ ] Contract request/response và error catalog khớp BD/sequence hoặc có Change Request được phê duyệt.
- [ ] Mapping DB/service dùng owner, bảng, cột, khóa và transaction có thật; không còn placeholder.
- [ ] Envelope/casing/trace/pagination tuân theo kiến trúc chuẩn.
- [ ] Reviewer và approver được chỉ định; trạng thái chỉ chuyển `VERIFIED` sau khi đóng toàn bộ finding P0/P1.

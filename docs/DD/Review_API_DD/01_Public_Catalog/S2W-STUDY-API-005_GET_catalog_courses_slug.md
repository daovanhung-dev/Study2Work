# Review API DD — S2W-STUDY-API-005

- DD nguồn: `docs/DD/Study2Work_DD_API/01_Public_Catalog/S2W-STUDY-API-005_GET_catalog_courses_slug.xlsx`
- Endpoint: `GET /api/v1/catalog/courses/{slug}`
- Verdict: **CẦN SỬA**

## Findings

| Mức | Sheet/cell | Finding | Căn cứ BD | Cách sửa |
|---|---|---|---|---|
| P0 | `2.Response!A7:H11` và ví dụ thành công/lỗi | Envelope `{data, meta}` / `{error}`, `meta.request_id`, snake_case và pagination giả không khớp contract chuẩn. | `docs/BD/base/0. Study2Work_System_Architecture.md:632-700` | Đổi sang `success`, `businessCode`, `message`, `data`, `errors`, `traceId`; chỉ có `meta.pagination` cho API danh sách và dùng camelCase. |
| P0 | `2.Response!A15:H31` | `data.course` và các `counts` khai báo String; curriculum/sample lessons/materials thiếu object schema. | `docs/BD/01. Study2Work_Study_BasicDesign_Public_Catalog.md:99-139` | Định nghĩa course detail, chapter summary, sample lesson item, material item và CTA/learner state. |
| P0 | `3.Data mapping!A12:H14`, các sheet DB | Mapping dùng cột ảo và join placeholder; chưa thể thực thi với `courses → chapters → lessons → course_materials` trong schema. | `docs/BD/diagram/CLASS/study2work_study_full_schema_seed.sql:19-30,239-301,323-385,446-481` | Viết join cụ thể, lọc `courses/lessons.publish_status`, sort `chapters/lessons.order_index`. |
| P0 | `3.Data mapping`, `4.Error` | Chưa thực thi rule chỉ trả bài `sample_public` và tài nguyên được phép public; DDL hiện chưa có cờ visibility riêng cho material. | `docs/BD/01. Study2Work_Study_BasicDesign_Public_Catalog.md:129-139`; `docs/BD/diagram/SEQUENCE/02. Study2Work_Study_SEQ_Public_Catalog.md:24-40` | Bổ sung policy/cột public visibility cho material hoặc quy tắc dựa trên `usage_right_status`; không trả nội dung private. |
| P1 | `4.Error` | Chi tiết public không nên trả `CONTENT_LOCKED`; nội dung không public nên được che bằng 404. | `docs/BD/01. Study2Work_Study_BasicDesign_Public_Catalog.md:48-139,169-179` | Chuẩn hóa error catalog theo public resource visibility. |
| P1 | `Cover!B15:G19`, `Lịch sử!A4:F4`, `00.Hướng dẫn!A4:B18` | Tài liệu được đánh dấu `VERIFIED` dù reviewer/approver chưa chỉ định; hướng dẫn còn tuyên bố gói nguồn không có schema và không còn placeholder. | `docs/BD/diagram/CLASS/study2work_study_full_schema_seed.sql:1-30` | Cập nhật inventory nguồn, loại bỏ placeholder, chuyển về `IN REVIEW` cho đến khi contract và mapping được duyệt. |

## Điều kiện duyệt lại

- [ ] Contract request/response và error catalog khớp BD/sequence hoặc có Change Request được phê duyệt.
- [ ] Mapping DB/service dùng owner, bảng, cột, khóa và transaction có thật; không còn placeholder.
- [ ] Envelope/casing/trace/pagination tuân theo kiến trúc chuẩn.
- [ ] Reviewer và approver được chỉ định; trạng thái chỉ chuyển `VERIFIED` sau khi đóng toàn bộ finding P0/P1.

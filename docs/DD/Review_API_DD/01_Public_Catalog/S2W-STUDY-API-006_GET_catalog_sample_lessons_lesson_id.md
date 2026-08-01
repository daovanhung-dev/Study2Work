# Review API DD — S2W-STUDY-API-006

- DD nguồn: `docs/DD/Study2Work_DD_API/01_Public_Catalog/S2W-STUDY-API-006_GET_catalog_sample_lessons_lesson_id.xlsx`
- Endpoint: `GET /api/v1/catalog/sample-lessons/{lesson_id}`
- Verdict: **CẦN SỬA**

## Findings

| Mức | Sheet/cell | Finding | Căn cứ BD | Cách sửa |
|---|---|---|---|---|
| P0 | `2.Response!A7:H11` và ví dụ thành công/lỗi | Envelope `{data, meta}` / `{error}`, `meta.request_id`, snake_case và pagination giả không khớp contract chuẩn. | `docs/BD/base/0. Study2Work_System_Architecture.md:632-700` | Đổi sang `success`, `businessCode`, `message`, `data`, `errors`, `traceId`; chỉ có `meta.pagination` cho API danh sách và dùng camelCase. |
| P0 | `1.Request!A20:J22`, `2.Response!A15:H23` | Path/response không khớp sequence: DD dùng `{lesson_id}` và `lesson_id`, `objectives`, `preview_content`, `public_resources`; sequence dùng `{lessonId}`, `lessonId`, `samplePublic`, `contentBlocks`, `materials`. | `docs/BD/diagram/SEQUENCE/02. Study2Work_Study_SEQ_Public_Catalog.md:32-40,94-128` | Đồng bộ exact contract và camelCase; định nghĩa item schema cho content block/material. |
| P0 | `3.Data mapping!A12:H14` | SQL lọc `lessons.lesson_id` trong khi PK là `lessons.id`, đồng thời thiếu điều kiện `sample_public = true`. | `docs/BD/diagram/CLASS/study2work_study_full_schema_seed.sql:458-470` | Dùng `lessons.id=:lessonId AND sample_public=true AND publish_status='PUBLISHED'`. |
| P0 | `3.Data mapping!A12:H15` | Mapping join `lesson_progress`/`exercises` trái rule guest không tạo progress và không được lộ bài tập private. | `docs/BD/01. Study2Work_Study_BasicDesign_Public_Catalog.md:129-139`; `docs/BD/diagram/SEQUENCE/02. Study2Work_Study_SEQ_Public_Catalog.md:131-134` | Loại progress/private exercise khỏi query và side effect; chỉ trả content/material public. |
| P1 | `3.Data mapping`, sheet DB | Material chưa có tiêu chí public triển khai được; `course_materials` chỉ có `usage_right_status`. | `docs/BD/diagram/CLASS/study2work_study_full_schema_seed.sql:472-481` | Chốt policy visibility hoặc bổ sung cột/migration; tài nguyên không xác định phải mặc định không public. |
| P1 | `Cover!B15:G19`, `Lịch sử!A4:F4`, `00.Hướng dẫn!A4:B18` | Tài liệu được đánh dấu `VERIFIED` dù reviewer/approver chưa chỉ định; hướng dẫn còn tuyên bố gói nguồn không có schema và không còn placeholder. | `docs/BD/diagram/CLASS/study2work_study_full_schema_seed.sql:1-30` | Cập nhật inventory nguồn, loại bỏ placeholder, chuyển về `IN REVIEW` cho đến khi contract và mapping được duyệt. |

## Điều kiện duyệt lại

- [ ] Contract request/response và error catalog khớp BD/sequence hoặc có Change Request được phê duyệt.
- [ ] Mapping DB/service dùng owner, bảng, cột, khóa và transaction có thật; không còn placeholder.
- [ ] Envelope/casing/trace/pagination tuân theo kiến trúc chuẩn.
- [ ] Reviewer và approver được chỉ định; trạng thái chỉ chuyển `VERIFIED` sau khi đóng toàn bộ finding P0/P1.

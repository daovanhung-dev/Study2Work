# Review API DD — S2W-STUDY-API-041

- DD nguồn: `docs/DD/Study2Work_DD_API/05_Khoa_hoc_chuong_bai_hoc_va_tai_nguyen/S2W-STUDY-API-041_GET_chapters_chapter_id.xlsx`
- Endpoint: `GET /api/v1/chapters/{chapter_id}`
- Verdict: **CẦN SỬA**

## Findings

| Mức | Sheet/cell | Finding | Căn cứ BD | Cách sửa |
|---|---|---|---|---|
| P0 | `3.Data mapping!A12:H12`, `A20` | Predicate `chapters.chapter_id` sai; PK thật là `id`. Query không nối course enrollment/lesson progress để kiểm owner/unlock. | SQL `docs/BD/diagram/CLASS/study2work_study_full_schema_seed.sql:416-469,539-555` | Query `chapters.id`, traverse course/enrollment/actor và tính unlock trước khi trả nội dung. |
| P0 | `2.Response!A16:H21` | `chapter/course_summary/items/completion/missing` là aggregate giả gán cho `chapters`; schema object/type/cardinality không được định nghĩa. | `docs/BD/05. Study2Work_Study_BasicDesign_Khoa_Hoc_Noi_Dung_Hoc.md:62-72,115-125` | Định nghĩa chapter fields thật và ordered lessons/exercises; source derived conditions rõ. |
| P1 | `4.Error!A13:H15` | `CONTENT_NOT_PUBLISHED` bị lặp hai dòng/cùng message ID; error `resource_id` không khớp `chapter_id`. | `docs/BD/base/0. Study2Work_System_Architecture.md:693-700` | Dedupe error, dùng đúng field/business code cho not-found/not-visible/locked. |
| P1 | `3.Data mapping!A13:H13` | Chỉ chép “PUBLISHED/ownership”, chưa thực thi unlock condition của chapter (`ALWAYS`, sequential...) và prerequisite missing action. | `docs/BD/05. Study2Work_Study_BasicDesign_Khoa_Hoc_Noi_Dung_Hoc.md:198-205`; SQL `:446-455` | Mô tả transition/access algorithm và response locked reason/required predecessor. |
| P0 | `2.Response!A9:E11`, `A22:H22` | Envelope/pagination mẫu thừa không canonical. | `docs/BD/base/0. Study2Work_System_Architecture.md:632-700` | Canonical singleton envelope. |

## Điều kiện duyệt lại

- [ ] Query owner/unlock-safe và dùng PK thật.
- [ ] Nested chapter/items/conditions schema đầy đủ.
- [ ] Error catalog không lặp, đúng field/state.
- [ ] Endpoint suy dẫn được duyệt.

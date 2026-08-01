# Review API DD — S2W-STUDY-API-044

- DD nguồn: `docs/DD/Study2Work_DD_API/05_Khoa_hoc_chuong_bai_hoc_va_tai_nguyen/S2W-STUDY-API-044_GET_lessons_lesson_id_resources.xlsx`
- Endpoint: `GET /api/v1/lessons/{lesson_id}/resources`
- Verdict: **CẦN SỬA**

## Findings

| Mức | Sheet/cell | Finding | Căn cứ BD | Cách sửa |
|---|---|---|---|---|
| P0 | `2.Response!A15:H23`, `3.Data mapping!A12:H12`, `A20` | Resources bị gán nguồn `lessons`; nguồn thật là `course_materials`. `resource_id`, description, usage summary/access action không phải columns; cột thật là `id`, `resource_url`, `usage_right_status`. | SQL `docs/BD/diagram/CLASS/study2work_study_full_schema_seed.sql:458-484` | Query materials theo `lesson_id`, map đúng fields; derived access action có nguồn rõ. |
| P0 | `3.Data mapping!A12:H12` | Predicate `lessons.lesson_id` sai PK và không check course enrollment/unlock trước khi liệt kê private resources. | SQL `:416-484`; `docs/BD/05. Study2Work_Study_BasicDesign_Khoa_Hoc_Noi_Dung_Hoc.md:159-169` | Dùng `lessons.id`; authorize actor qua course/path state trước query material. |
| P1 | `2.Response!A22:H23` | `usage_rights_summary` và raw access URL không có policy; tài liệu chỉ được hiện khi quyền sử dụng hợp lệ và quyền learner phù hợp. | `docs/BD/05. Study2Work_Study_BasicDesign_Khoa_Hoc_Noi_Dung_Hoc.md:159-169,211-219` | Không expose internal rights detail quá mức; trả signed access/action sau authorization. |
| P1 | `4.Error!A13:H15` | Error dùng `resource_id` dù route nhận `lesson_id` và lặp `CONTENT_NOT_PUBLISHED`. | `docs/BD/base/0. Study2Work_System_Architecture.md:693-700` | Đúng field, dedupe errors, thêm lesson locked/not-owned semantics. |
| P0 | `2.Response!A9:E11`, `A24:H24` | Envelope/pagination mẫu thừa không canonical. | `docs/BD/base/0. Study2Work_System_Architecture.md:632-700` | Canonical list response; pagination chỉ nếu thật sự áp dụng. |

## Điều kiện duyệt lại

- [ ] Query material đúng bảng/cột và owner/unlock check.
- [ ] Resource/rights/signed-access contract được khóa.
- [ ] Error đúng route và không lặp.
- [ ] Endpoint suy dẫn được duyệt.

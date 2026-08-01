# Review API DD — S2W-STUDY-API-043

- DD nguồn: `docs/DD/Study2Work_DD_API/05_Khoa_hoc_chuong_bai_hoc_va_tai_nguyen/S2W-STUDY-API-043_GET_courses_course_id_continue.xlsx`
- Endpoint: `GET /api/v1/courses/{course_id}/continue`
- Verdict: **CẦN SỬA**

## Findings

| Mức | Sheet/cell | Finding | Căn cứ BD | Cách sửa |
|---|---|---|---|---|
| P0 | `3.Data mapping!A12:H12`, `A20` | Predicate `courses.course_id` sai; query không lọc owner/course enrollment và SELECT next/resume fields như cột course. | SQL `docs/BD/diagram/CLASS/study2work_study_full_schema_seed.sql:361-469,539-555` | Query `courses.id`, owner enrollment, lesson progress `last_accessed_at` và ordered unlocked items. |
| P0 | `2.Response!A16:H21` | `next_item_type/id`, reason, resume position, route không có nguồn/algorithm; DD không định nghĩa ưu tiên “đang học”, “bài kế tiếp”, hay completed review. | `docs/BD/05. Study2Work_Study_BasicDesign_Khoa_Hoc_Noi_Dung_Hoc.md:150-157` | Định nghĩa deterministic continuation matrix, null/completed/archived behavior và typed `nextItem`. |
| P1 | `3.Data mapping!A12:H13` | Không xử lý yêu cầu BD: lesson cũ archived/updated phải chuyển tới nội dung hiện hành phù hợp; schema không có version/replacement mapping. | `docs/BD/05. Study2Work_Study_BasicDesign_Khoa_Hoc_Noi_Dung_Hoc.md:150-157` | Chốt version/replacement model hoặc trả explicit unavailable/review action. |
| P1 | `4.Error!A13:H15` | `CONTENT_NOT_PUBLISHED` lặp; thiếu no-enrollment/no-progress/completed-course semantics. | `docs/BD/05. Study2Work_Study_BasicDesign_Khoa_Hoc_Noi_Dung_Hoc.md:150-157` | Thiết kế stable endpoint-specific outcomes/errors. |
| P0 | `2.Response!A9:E11`, `A22:H22` | Envelope/pagination mẫu thừa không canonical. | `docs/BD/base/0. Study2Work_System_Architecture.md:632-700` | Canonical singleton response. |

## Điều kiện duyệt lại

- [ ] Continue algorithm/owner/query/order được đặc tả và test.
- [ ] Completed/no-progress/archived behavior rõ.
- [ ] Không còn cột giả/lỗi lặp; envelope canonical.
- [ ] Endpoint suy dẫn được duyệt.

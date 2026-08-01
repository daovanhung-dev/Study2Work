# Review API DD — S2W-STUDY-API-040

- DD nguồn: `docs/DD/Study2Work_DD_API/05_Khoa_hoc_chuong_bai_hoc_va_tai_nguyen/S2W-STUDY-API-040_GET_courses_course_id_curriculum.xlsx`
- Endpoint: `GET /api/v1/courses/{course_id}/curriculum`
- Verdict: **CẦN SỬA**

## Findings

| Mức | Sheet/cell | Finding | Căn cứ BD | Cách sửa |
|---|---|---|---|---|
| P0 | `1.Request!A10:D10`, `2.Response!A16:H17` | Endpoint Public nhưng trả `unlock_state`, completion state và `next_item` learner-specific; không có optional-auth/field gating. | `docs/BD/05. Study2Work_Study_BasicDesign_Khoa_Hoc_Noi_Dung_Hoc.md:24-30,115-125` | Public chỉ nhận curriculum summary/sample visibility; authenticated owner mới nhận progress/unlock/next item. |
| P0 | `3.Data mapping!A12:H12`, `A20` | `courses.course_id` sai PK; `chapters` và `next_item` bị SELECT như cột của course thay vì JOIN chapters/lessons/exercises/progress. | SQL `docs/BD/diagram/CLASS/study2work_study_full_schema_seed.sql:361-374,446-505,539-555` | Query `courses.id`; ordered JOIN và derived learner state có ownership. |
| P1 | `2.Response!A16:H17` | Nested chapter contract chỉ nằm trong Remarks, không định nghĩa lesson/exercise fields, enum/nullability/required-vs-optional; `next_item` là String. | `docs/BD/05. Study2Work_Study_BasicDesign_Khoa_Hoc_Noi_Dung_Hoc.md:115-125` | Mở rộng schema chính thức cho chapter/items/unlock/completion/next action. |
| P1 | `4.Error!A12:H13` | Không mô tả behavior khi course public nhưng một lesson private/unpublished; một lỗi toàn endpoint dễ làm lộ/ẩn sai curriculum. | `docs/BD/05. Study2Work_Study_BasicDesign_Khoa_Hoc_Noi_Dung_Hoc.md:198-219` | Chốt per-item visibility/redaction, archived content và safe errors. |
| P0 | `2.Response!A9:E11`, `A18:H18` | Envelope/pagination mẫu thừa không canonical. | `docs/BD/base/0. Study2Work_System_Architecture.md:632-700` | Canonical envelope/camelCase. |

## Điều kiện duyệt lại

- [ ] Public và owner curriculum projections được khóa.
- [ ] Nested schema/query/order/access thật, không dùng cột giả.
- [ ] Per-item visibility/error có test.
- [ ] Endpoint suy dẫn được duyệt.

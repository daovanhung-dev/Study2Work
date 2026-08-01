# Review S2W-STUDY-API-130 — GET learner progress

- DD nguồn: `docs/DD/Study2Work_DD_API/11_Admin_quan_ly_hoc_vien_va_ho_tro_ngoai_le/S2W-STUDY-API-130_GET_admin_learners_learner_id_progress.xlsx`
- Endpoint: `GET /api/v1/admin/learners/{learner_id}/progress`
- Kết luận: **CẦN SỬA — chưa đủ điều kiện VERIFIED**

## Các điểm cần sửa

| ID | Mức độ | Vị trí DD | Nhận xét và căn cứ BD | Cách sửa |
|---|---|---|---|---|
| 130-01 | P0 | `2.Response!A9:E11`, `A15:H25` | Envelope, `request_id` và pagination mẫu không đúng chuẩn `/api/v1` tại `System_Architecture.md:632-700`; đây là singleton nên không có pagination. | Chuyển sang success/businessCode/message/data/traceId camelCase và bỏ pagination. |
| 130-02 | P0 | `3.Data mapping!A12:H20` | DD SELECT `path_progress`, `courses`, `assignments_by_status`, `dropout_risk_indicators` như cột của `lesson_progress`; schema thật chỉ có tiến độ theo bài với các cột tại `schema_seed.sql:539-555`. JOIN vẫn là `<FK condition>`. | Định nghĩa phép tổng hợp từ enrollment, lesson progress và submission; viết JOIN/CTE cụ thể và tiêu chí “dropout risk”, hoặc bỏ field suy diễn chưa có căn cứ. |
| 130-03 | P1 | `2.Response!A16:H21` | `path_progress` và `assignments_by_status` khai báo String dù phải là object/map; `last_learning_at` không map tới `last_accessed_at`; không có cấu trúc course/chapter/lesson. BD yêu cầu xem rõ các cấp và trạng thái bài tập (`BD-11:74-85`). | Thiết kế schema phân cấp, enum và kiểu number/date-time; nêu cách tránh double-count và quy tắc tính phần trăm. |
| 130-04 | P1 | `3.Data mapping!A13:H17`, `4.Error!A9:H13` | Rule PUBLISHED/one-ACTIVE và lỗi conflict là template không liên quan API đọc; thiếu quy tắc chỉ xem để hỗ trợ, không sửa trực tiếp (`BD-11:85`, `BD-11:174-176`). | Ghi rõ read-only invariant, scope permission, 404-vs-403 chống enumeration và lỗi filter/target thực tế. |
| 130-05 | P1 | `Cover!B19`, `00.Hướng dẫn!A4:B18` | Tuyên bố “không có schema” và “không còn placeholder” không đúng hiện trạng nguồn/mapping. | Cập nhật căn cứ 48 BD + SQL và bỏ VERIFIED tới khi query được kiểm chứng. |

## Điều kiện duyệt lại

- Công thức tiến độ và cấu trúc response được Product/API Owner chốt.
- Query có execution plan/test fixture và không có placeholder.

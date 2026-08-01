# Review S2W-STUDY-API-145 — GET learning-path report

- DD nguồn: `docs/DD/Study2Work_DD_API/12_Bao_cao_van_hanh/S2W-STUDY-API-145_GET_admin_reports_learning_paths.xlsx`
- Endpoint: `GET /api/v1/admin/reports/learning-paths`
- Kết luận: **CẦN SỬA — chưa có query/metric contract khả thi**

## Các điểm cần sửa

| ID | Mức độ | Vị trí DD | Nhận xét và căn cứ BD | Cách sửa |
|---|---|---|---|---|
| 145-01 | P0 | `3.Data mapping!A12:H20` | `vw_report_learning_paths` không tồn tại; các aggregate được SELECT như cột mà không có định nghĩa cohort/JOIN. | Viết semantic view/SQL từ path enrollments, course enrollments và support requests; nêu công thức từng count/rate/time. |
| 145-02 | P1 | `2.Response!A16:H23` | Counts và completion rate là String; `avg_completion_time` là date-time thay vì duration; dropout course item không có schema. | Dùng integer/decimal/duration và định nghĩa item `{courseId, entrants, dropouts, dropoutRate}`. |
| 145-03 | P0 | `4.Error!A13:H16` | Các lỗi account verification/onboarding/active path/path published là của API kích hoạt, không phải report read. | Bỏ lỗi copy-paste; thêm invalid range/filter/report source unavailable. |
| 145-04 | P1 | `Overview!A19:B20`, `3.Data mapping!A13:H13` | RPT-06 yêu cầu phân biệt nội dung published và archived (`BD-12:186-195`), nhưng response/filter không thể hiện content status hoặc aggregation rule lịch sử. | Chốt snapshot/as-of semantics và status dimension; không loại lịch sử chỉ vì path hiện archived. |
| 145-05 | P0 | `2.Response!A9:E11` | Envelope/pagination cũ trái `System_Architecture.md:632-700`. | Chuyển sang envelope chuẩn và `meta.pagination` chỉ nếu endpoint thực sự phân trang list. |

## Điều kiện duyệt lại

- Có metric dictionary + view/query chạy được và status/as-of semantics.
- Có test tỷ lệ, duration và no-data/zero-denominator.

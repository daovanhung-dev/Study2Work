# Review S2W-STUDY-API-143 — GET registration report

- DD nguồn: `docs/DD/Study2Work_DD_API/12_Bao_cao_van_hanh/S2W-STUDY-API-143_GET_admin_reports_registrations.xlsx`
- Endpoint: `GET /api/v1/admin/reports/registrations`
- Kết luận: **CẦN SỬA — thiếu nguồn dữ liệu authoritative và định nghĩa metric**

## Các điểm cần sửa

| ID | Mức độ | Vị trí DD | Nhận xét và căn cứ BD | Cách sửa |
|---|---|---|---|---|
| 143-01 | P0 | `3.Data mapping!A12:H20` | DD dựa vào `vw_report_registrations` và `contact_verifications`, nhưng cả hai không có trong schema hiện hành. Hơn nữa Platform Identity sở hữu đăng ký/xác thực (`System_Architecture.md:61-75`, `201-301`), nên Study DB không mặc nhiên là nguồn sự thật. | Chốt nguồn event/read model từ Platform Identity, schema projection và freshness; sau đó viết view/query thật. |
| 143-02 | P1 | `2.Response!A16:H20` | Count/rate/series đều để String; `avg_verification_time` bị khai báo date-time trong khi đây là duration. BD yêu cầu số đăng ký, tỷ lệ, pending và thời gian trung bình (`BD-12:80-88`). | Dùng integer, decimal rate, array time-series và durationSeconds/ISO duration; nêu denominator và cohort. |
| 143-03 | P1 | `1.Request!A21:J23` | `granularity` là String tự do, chưa kiểm `from < to`, max range, timezone hay fill bucket thiếu. | Chốt enum DAY/WEEK/MONTH, inclusive/exclusive boundary, timezone và giới hạn khoảng. |
| 143-04 | P1 | `1.Request!A10:D10` | Permission `study.learners.support` chưa phản ánh báo cáo đăng ký/xác thực; BD chỉ nêu Support xem chỉ số onboarding/support, còn Admin xem tổng quan (`BD-12:24-31`). | Chốt permission `reports.registration.read` và role mapping tối thiểu cần thiết. |
| 143-05 | P0 | `2.Response!A9:E11`, sample success | Envelope cũ, snake_case và pagination giả cho singleton trái `System_Architecture.md:632-700`. | Chuẩn hóa envelope/camelCase, bỏ pagination. |

## Điều kiện duyệt lại

- Có nguồn authoritative hoặc projection contract từ Platform Identity.
- Metric dictionary và test cohort/time-bucket được phê duyệt.

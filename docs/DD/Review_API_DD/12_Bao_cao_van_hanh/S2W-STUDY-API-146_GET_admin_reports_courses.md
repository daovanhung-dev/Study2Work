# Review S2W-STUDY-API-146 — GET course report

- DD nguồn: `docs/DD/Study2Work_DD_API/12_Bao_cao_van_hanh/S2W-STUDY-API-146_GET_admin_reports_courses.xlsx`
- Endpoint: `GET /api/v1/admin/reports/courses`
- Kết luận: **CẦN SỬA — nguồn và kiểu metric không đúng**

## Các điểm cần sửa

| ID | Mức độ | Vị trí DD | Nhận xét và căn cứ BD | Cách sửa |
|---|---|---|---|---|
| 146-01 | P0 | `3.Data mapping!A12:H20` | `vw_report_courses` không tồn tại; metric “issue count by lesson” cần nguồn content issue nhưng schema không có relation đó. Query chỉ SELECT tên aggregate giả. | Bổ sung read model/migration cho content issue hoặc bỏ metric; viết view/query và khóa nối thật. |
| 146-02 | P1 | `2.Response!A16:H22` | `course`, rates, issue count khai báo String; `avg_learning_time` khai báo date-time thay vì duration; các array không có item schema. | Dùng course summary object, decimal rates, map/array count và duration; nêu nullable khi chưa thu thập watch time. |
| 146-03 | P1 | `3.Data mapping!A13:H13` | RPT-06 yêu cầu tách published/archived (`BD-12:186-195`) nhưng filter/response không cho biết status/as-of. | Thêm contentStatus/asOf hoặc mô tả cách thống kê lịch sử theo trạng thái tại thời điểm học. |
| 146-04 | P1 | `1.Request!A21:J29` | Bộ filter copy chung gồm learner group/account/path status mà không nêu effect lên course start/completion denominator. | Viết filter semantics và validation; giới hạn range/granularity/timezone. |
| 146-05 | P0 | `2.Response!A9:E11` | Envelope/pagination cũ trái `System_Architecture.md:632-700`. | Dùng envelope chuẩn camelCase; pagination chỉ khi trả list có page contract. |

## Điều kiện duyệt lại

- Có nguồn content issue và công thức start/dropout/revisit được chốt.
- Kiểu dữ liệu, status dimension và zero-denominator có test.

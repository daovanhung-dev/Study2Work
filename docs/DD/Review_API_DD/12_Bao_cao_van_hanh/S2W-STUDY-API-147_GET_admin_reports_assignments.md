# Review S2W-STUDY-API-147 — GET assignment/exercise report

- DD nguồn: `docs/DD/Study2Work_DD_API/12_Bao_cao_van_hanh/S2W-STUDY-API-147_GET_admin_reports_assignments.xlsx`
- Endpoint: `GET /api/v1/admin/reports/assignments`
- Kết luận: **CẦN SỬA — có metric không thể tính từ schema hiện tại**

## Các điểm cần sửa

| ID | Mức độ | Vị trí DD | Nhận xét và căn cứ BD | Cách sửa |
|---|---|---|---|---|
| 147-01 | P0 | `3.Data mapping!A12:H20` | `vw_report_assignments` không tồn tại. `avg_open_to_submit_time` không tính được vì `exercise_submissions` không lưu thời điểm mở, chỉ có `submitted_at/reviewed_at` (`schema_seed.sql:508-529`). | Bổ sung event/fact `exercise_opened_at` hoặc loại metric; viết aggregate query/read model thật. |
| 147-02 | P1 | `2.Response!A16:H23` | Count/rate đều String; hai duration bị khai báo date-time. | Dùng integer, decimal và duration; định nghĩa denominator cho pass/fail/revision (attempt hay learner/latest submission). |
| 147-03 | P1 | toàn workbook | DD dùng “assignment” trong route/field nhưng BD và schema dùng “exercise”. Việc trộn tên làm mơ hồ ID/domain enum. | Chọn một ubiquitous language; nếu giữ route legacy phải ghi rõ `assignmentId == exercise.id` và dùng nhất quán trong OpenAPI. |
| 147-04 | P1 | `3.Data mapping!A13:H17` | Rule one-ACTIVE/PUBLISHED/ownership là template; thiếu định nghĩa review backlog/age và phân quyền Content Admin theo nội dung (`BD-12:145-158`). | Thêm backlog cutoff, latest state, manual-review scope và privacy aggregate. |
| 147-05 | P0 | `2.Response!A9:E11` | Envelope/pagination cũ trái `System_Architecture.md:632-700`. | Chuẩn hóa envelope, camelCase và pagination contract nếu list. |

## Điều kiện duyệt lại

- Có nguồn timestamp mở bài hoặc metric được bỏ/phê duyệt lại.
- Formula theo attempt/learner và queue review được kiểm bằng fixtures.

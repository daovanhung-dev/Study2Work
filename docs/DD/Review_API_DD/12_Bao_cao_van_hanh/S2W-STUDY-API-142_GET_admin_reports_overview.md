# Review S2W-STUDY-API-142 — GET reports overview

- DD nguồn: `docs/DD/Study2Work_DD_API/12_Bao_cao_van_hanh/S2W-STUDY-API-142_GET_admin_reports_overview.xlsx`
- Endpoint: `GET /api/v1/admin/reports/overview`
- Kết luận: **CẦN SỬA — lệch contract SEQ-13 và chưa có metric specification**

## Các điểm cần sửa

| ID | Mức độ | Vị trí DD | Nhận xét và căn cứ BD | Cách sửa |
|---|---|---|---|---|
| 142-01 | P0 | `1.Request!A21:J29`, `2.Response!A15:H25` | SEQ-13 dùng `learningPathId/courseId` và trả `newAccounts`, `verificationRate`, `onboardingCompletionRate`, `activatedLearners`, `pathCompletionRate`, `zaloLinkOpenCount` dạng số (`SEQ-13:31-68`). DD dùng snake_case và khai báo phần lớn metric là String. | Đồng bộ camelCase và kiểu integer/decimal; nếu mở rộng contract phải ghi rõ thay đổi và version. |
| 142-02 | P0 | `1.Request!A10:D10`, `4.Error!A11:H11` | Permission là `study.rbac.manage`, không liên quan xem báo cáo. BD phân quyền báo cáo theo Admin/Content Admin/Learner Support (`BD-12:24-31`, `186-195`). | Tạo/dùng permission report-read theo scope; không buộc người xem báo cáo phải quản trị RBAC. |
| 142-03 | P0 | `3.Data mapping!A12:H20` | `vw_report_overview` không có trong schema và DD lọc các tên `from/to/granularity` như cột view. Không có công thức tử số/mẫu số, timezone, khoảng thời gian hay dữ liệu trễ. | Viết metric dictionary + SQL/semantic view thực tế; dùng điều kiện trên timestamp fact, chốt `[from,to)`, timezone và freshness. |
| 142-04 | P1 | `3.Data mapping!A13:H17` | Rule one-ACTIVE/PUBLISHED/ownership và side effect idempotency là template, không mô tả privacy của báo cáo. BD yêu cầu aggregate không lộ PII (`BD-12:186-195`, `SEQ-13:105-108`). | Bỏ rule không liên quan; thêm minimum aggregation, suppression/field allowlist và role scope. |
| 142-05 | P0 | `2.Response!A9:E11`, sample success | Envelope `{data,meta}` / `{error}`, `request_id` và pagination giả trái chuẩn `/api/v1` (`System_Architecture.md:632-700`). | Dùng envelope chuẩn, traceId top-level; overview singleton không có pagination. |

## Điều kiện duyệt lại

- Contract khớp SEQ-13, permission report-read đúng scope.
- Mỗi metric có type, formula, denominator, timezone, freshness và test fixture.

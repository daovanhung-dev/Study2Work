# Review S2W-STUDY-API-148 — GET community report

- DD nguồn: `docs/DD/Study2Work_DD_API/12_Bao_cao_van_hanh/S2W-STUDY-API-148_GET_admin_reports_community.xlsx`
- Endpoint: `GET /api/v1/admin/reports/community`
- Kết luận: **CẦN SỬA — thiếu nguồn report và có kiểu dữ liệu sai**

## Các điểm cần sửa

| ID | Mức độ | Vị trí DD | Nhận xét và căn cứ BD | Cách sửa |
|---|---|---|---|---|
| 148-01 | P0 | `3.Data mapping!A12:H20` | `vw_report_community` và `community_reports` không tồn tại trong schema; chỉ có group và link-open events. Vì vậy report/broken/spam count chưa có nguồn. | Bổ sung persistence/read model cho community report hoặc thu hẹp response; viết JOIN/aggregate thật. |
| 148-02 | P0 | `2.Response!A16:H22` | `broken_link_count` bị khai báo `String(URI)` dù là count; opens/report/spam count là String; breakdown không có schema. | Dùng integer và item schema; map `community_group_id` đúng. |
| 148-03 | P1 | `Overview!A19:B20`, `2.Response` | BD cảnh báo số lượt mở link không đồng nghĩa đã tham gia nhóm (`BD-12:160-169`, `RPT-03` tại `190-193`). Tên `opens_count` chưa kèm semantic/unique-vs-total và có thể bị diễn giải sai. | Đặt rõ `linkOpenEventCount`, định nghĩa dedupe/bot/retry; thêm chú thích machine-readable/documentation. |
| 148-04 | P1 | `1.Request!A21:J29` | Filter course/path/status/granularity copy chung nhưng không nêu group scope hoặc group gắn cả path/course thì đếm thế nào. | Chốt attribution rule và tránh double-count; validate date range/timezone. |
| 148-05 | P0 | `2.Response!A9:E11` | Envelope/pagination cũ trái `System_Architecture.md:632-700`. | Dùng envelope chuẩn, camelCase và pagination nếu list. |

## Điều kiện duyệt lại

- Có source cho report/broken/spam và attribution/dedupe rule.
- Kiểu dữ liệu và test “open ≠ joined member” được xác nhận.

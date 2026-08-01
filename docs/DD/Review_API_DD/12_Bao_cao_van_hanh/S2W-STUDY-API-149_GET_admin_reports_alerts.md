# Review S2W-STUDY-API-149 — GET operational alerts

- DD nguồn: `docs/DD/Study2Work_DD_API/12_Bao_cao_van_hanh/S2W-STUDY-API-149_GET_admin_reports_alerts.xlsx`
- Endpoint: `GET /api/v1/admin/reports/alerts`
- Kết luận: **CẦN SỬA — contract/persistence của alert chưa được chốt**

## Các điểm cần sửa

| ID | Mức độ | Vị trí DD | Nhận xét và căn cứ BD | Cách sửa |
|---|---|---|---|---|
| 149-01 | P0 | `1.Request!A21:J27`, `2.Response!A15:H25` | SEQ-13 mẫu dùng filter `severity`, `learningPathId` và item `{type,severity,targetId,targetTitle,metricValue}` (`SEQ-13:71-102`). DD bỏ learningPathId, đổi sang alertId/category/metric/observedValue/threshold/scope/status mà không ghi quyết định thay contract. | Đồng bộ sequence hoặc cập nhật BD/version có phê duyệt; chốt enum và item schema. |
| 149-02 | P0 | `3.Data mapping!A12:H20` | `vw_operational_alerts` không tồn tại; DD lọc `from/to` như cột và dùng `alert_id/status`, ngụ ý alert persisted trong khi BD mô tả tính threshold hỗ trợ quyết định (`SEQ-13:22-26`, `BD-12:171-182`). | Quyết định alert là computed hay persisted. Nếu computed, bỏ lifecycle ID/status; nếu persisted, bổ sung table, unique fingerprint, detected/resolved lifecycle và migration. |
| 149-03 | P1 | `1.Request!A21:J23`, `2.Response!A17:H23` | severity/category/status là String tự do; `observed_value` String, `threshold` Integer dù metric có thể là rate decimal. | Chốt enum/catalog alert; dùng numeric value + unit/denominator và threshold cùng type. |
| 149-04 | P1 | `3.Data mapping!A13:H17` | Rule one-ACTIVE/PUBLISHED/ownership và idempotency side effect không liên quan API đọc; thiếu nguyên tắc “alert không tự đổi nội dung” (`BD-12:171-182`). | Ghi rõ API read-only/advisory, freshness, calculation window và permission report-alert-read. |
| 149-05 | P0 | `2.Response!A9:E11` | Envelope/pagination cũ trái `System_Architecture.md:632-721`. | Dùng envelope chuẩn và `meta.pagination`; traceId top-level. |

## Điều kiện duyệt lại

- Có quyết định computed-vs-persisted và contract khớp SEQ-13.
- Alert catalog, threshold/window/freshness và pagination có test.

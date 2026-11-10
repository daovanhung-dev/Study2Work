# AD-01 — Business Rules

## 1. Rule index
| Rule ID (package alias) | Tên / source ID | Áp dụng | Thực thi | Tests |
|---|---|---|---|---|
| `AD-01-BR-001` | Source rules/gates bundle (alias only) | See source DD | Not re-inferred | See source acceptance |

## 2. Rules, security, discrepancy và gate từ source
- Inventory purpose: Tổng quan hệ thống theo khoảng ngày: học viên, khóa, tác động và các KPI.
- Gate/status (giữ nguyên): **D**; **BLOCK:** #101 chưa có route/module/query/model/test; thiếu Admin self-profile endpoint; KPI/date semantics và status/audit sources chưa xác nhận; Study Web UNWIRED
- BR IDs trong file này chỉ là alias trỏ tới source rule/gate bundles; không thêm business rule. Không khẳng định rule FE/BE mới khi source chưa xác nhận.

### Trích từ DD nguồn: F. Tiêu chí nghiệm thu và blockers

### Static acceptance checklist

- [x] Có ảnh nguồn nguyên trạng và ảnh chú thích; ảnh nguồn được giữ nguyên.
- [x] 35 marker tuần tự/duy nhất/in-bounds và có 35 element row tương ứng.
- [x] Các event trong HTML được mô tả đúng gồm disabled, no-op, placeholder navigation và timer-only refresh.
- [x] API #101 được đối chiếu với catalog, AC-38, Draft DD, route composition và current auth/profile code.
- [x] Expected behavior, current behavior, `DERIVED`, `UNWIRED`, `NOT_FOUND` và `DISCREPANCY` được tách riêng.
- [x] Error codes, state candidates và handoff được truy vết; chưa suy diễn lỗi 422, KPI formula, identity source hoặc service health.
- [ ] Được owner duyệt KPI keys/formulas/population/unit/order và mapping tới bốn card.
- [ ] Được owner duyệt date defaults, timezone, boundaries, partial/no-data và invalid-range behavior.
- [ ] Có API #101 implementation/test và report-specific authorization; xác định Admin profile source.
- [ ] Có Study Web app route/client mapping, audit/status endpoints nếu các panel này phải là dữ liệu live, và xử lý đúng Study Web design tokens.
- [ ] Xác minh schema/runtime/deployment trước khi đánh dấu `RUNTIME VERIFIED`.

### Open blockers

1. **API #101 `DESIGN_ONLY`:** catalog và Draft DD có, nhưng current router/module/query/model/test không có. Không thể xác nhận request thực thi/response thật.
2. **KPI:** bốn card là total users, active courses, pending moderation và system load. API #101 contract chỉ có `ImpactMetric[]`; các count proposal trong DD API có nghĩa khác và chưa được phê duyệt.
3. **Date range:** optional query bounds nhưng response period bắt buộc; các button disabled và default/inclusive/timezone/invalid range chưa rõ.
4. **Identity/authorization:** current Admin APIs có `ADMIN` role guard, nhưng #101 report permission không có source. Không có Admin self-profile route; API #04 hiện chỉ Student.
5. **Audit/service status:** activity, DB/auth/queue status, “System Normal”, readiness và compliance copy không được #101 trả; `/health/ready` chỉ kiểm tra cấu hình dependency, không probe DB.
6. **Study Web:** thiếu source/package/router nên không có route, API caller, loading/error mapping hoặc link destination runtime.
7. **Design system:** palette/font của screenshot khác Study Web visual target; chưa có approval cho ngoại lệ.

**Kết luận:** `DD BLOCKED`; tài liệu truy vết rõ phần có thể xác nhận và phần cần quyết định, nhưng chưa đủ để frontend triển khai KPI/range/identity mà không tự suy đoán. `IMPLEMENTATION BLOCKED`; `RUNTIME NOT VERIFIED`.

## 3. Quy tắc chưa xác nhận
- `CẦN_XÁC_NHẬN`: các quyết định/blocker trong inventory và DD nguồn chưa được giải quyết.
- Related IDs/source refs: Không có BR ID nguồn được chuẩn hóa.; xem [API](04-api-integration.md), [Events](02-events.md), [Tests](07-test-cases.md).

# ST-20 — Business Rules

## 1. Rule index
| Rule ID (package alias) | Tên / source ID | Áp dụng | Thực thi | Tests |
|---|---|---|---|---|
| `ST-20-BR-001` | Source rules/gates bundle (alias only) | See source DD | Not re-inferred | See source acceptance |

## 2. Rules, security, discrepancy và gate từ source
- Inventory purpose: Tổng số bài học, tiến độ theo course và achievements thực tế.
- Gate/status (giữ nguyên): **D; DD BLOCKED; IMPLEMENTATION BLOCKED; RUNTIME NOT VERIFIED:** #21 catalog trả `UserProfile` nhưng query, progress DTO, aggregate/merge/empty semantics chưa chốt; #38 award policy/source, course filter, pagination/order/empty semantics chưa chốt; inventory độc lập #21/#38 mâu thuẫn AC-18 tuần tự #21→#37→#38; Student routes/modules/queries/tests #21/#38 NOT_FOUND; Study Web UNWIRED; PNG gốc trống phần body, HTML chỉ có static empty state; loaded dashboard chưa có nguồn thiết kế xác nhận; HTML prototype tải remote Tailwind/Plus Jakarta Sans, dùng 1440px và trộn primary token lệch Study Web guide
- BR IDs trong file này chỉ là alias trỏ tới source rule/gate bundles; không thêm business rule. Không khẳng định rule FE/BE mới khi source chưa xác nhận.

### Trích từ DD nguồn: F. Tiêu chí nghiệm thu và blockers

### F.1. Checklist

- [x] 16 nhóm element đang nhìn thấy trên HTML-derived screenshot được đánh số, có mapping một-một trong DD và marker JSON.
- [x] PNG gốc và HTML gốc được giữ nguyên; ảnh render bổ sung ghi rõ provenance và giới hạn static-only.
- [x] Expected inventory, AC-18/API design và current source được tách riêng; conflict inventory vs AC-18 được ghi rõ.
- [x] API #21/#38 method/path/auth/query/body/response/success/errors và `DECLARED_NOT_RUNNABLE` status được ghi theo catalog/source.
- [x] 11 event có trigger, input, processing, output và ngoại lệ; không tạo API/schema/metric/award rule chưa được xác nhận.
- [x] Mỗi event ghi element/lifecycle kích hoạt và loại event; CTA #9 được mô tả theo đúng semantic anchor link của HTML.
- [x] State matrix, điều hướng ST-08/ST-21/ST-22 và session/access constraints được ghi.
- [ ] API #21 có query grammar, progress DTO, aggregate formula/scope/denominator/rounding, user binding và empty semantics được duyệt.
- [ ] API #38 có award criteria, response projection, course filter, pagination/order và empty policy được duyệt.
- [ ] Inventory/API orchestration được reconciled với AC-18 sequencing qua #37.
- [ ] Study Web route/runtime và Student API #21/#38 được triển khai/wire, sau đó mới có thể xác minh runtime.
- [ ] Loaded-state UI cho progress/achievements và phân biệt partial/empty/error được thiết kế.
- [ ] Prototype/loaded-state visual được đối chiếu và thống nhất với Study Web design target.

### F.2. Blockers

1. API #21 Student route/module/query/test `NOT_FOUND`; response `UserProfile` không biểu diễn progress. Query selector syntax, aggregate source/formula/scope, merge key, owner binding và no-enrollment/no-progress shape chưa chốt.
2. API #38 Student route/module/query/test `NOT_FOUND`; không có award policy/registry/table được xác nhận. Projection, course filter/access, pagination/order, duplicate/empty semantics chưa chốt.
3. Inventory yêu cầu #21/#38 độc lập; AC-18 diagram mô tả #21 → tổng hợp → #37 → tổng hợp → #38 → render. Thứ tự orchestration/partial timing chưa được reconcile.
4. Original PNG thiếu toàn bộ main content; HTML chỉ có static empty state. Loaded dashboard design chưa có trong tài sản hiện hành.
5. Study Web route/auth guard/runtime cho ST-20 chưa có; ST-21/ST-22 route/data handoff chưa được wire.
6. Candidate DDL `lesson_progress` không xác nhận live schema và không có achievements table; không đủ căn cứ để tính progress hoặc awards.
7. Prototype HTML tải remote CDN/font, dùng layout 1440px và trộn primary token khác intended Study Web design target; loaded-state design chưa được duyệt.

**Kết luận:** DD BLOCKED vì còn quyết định nghiệp vụ/API cần xác nhận; IMPLEMENTATION BLOCKED; RUNTIME NOT VERIFIED. Không chạy tests hoặc gọi runtime trong phiên tài liệu này.

## 3. Quy tắc chưa xác nhận
- `CẦN_XÁC_NHẬN`: các quyết định/blocker trong inventory và DD nguồn chưa được giải quyết.
- Related IDs/source refs: Không có BR ID nguồn được chuẩn hóa.; xem [API](04-api-integration.md), [Events](02-events.md), [Tests](07-test-cases.md).

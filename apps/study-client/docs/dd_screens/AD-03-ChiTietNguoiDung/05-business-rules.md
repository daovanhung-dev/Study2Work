# AD-03 — Business Rules

## 1. Rule index
| Rule ID (package alias) | Tên / source ID | Áp dụng | Thực thi | Tests |
|---|---|---|---|---|
| `AD-03-BR-001` | Source rules/gates bundle (alias only) | See source DD | Not re-inferred | See source acceptance |

## 2. Rules, security, discrepancy và gate từ source
- Inventory purpose: Hiển thị profile/status/role theo #69; nhật ký chỉ khi có API audit được duyệt.
- Gate/status (giữ nguyên): **R**; **DD BLOCKED; IMPLEMENTATION BLOCKED:** #69 source-backed locally, nhưng ADMIN permission mapping, legacy/live schema, PII/enum/lifecycle và audit/retention policy còn mở; Study Web UNWIRED; prototype 204/audit/sync claims không được API #69 hỗ trợ; RUNTIME NOT VERIFIED
- BR IDs trong file này chỉ là alias trỏ tới source rule/gate bundles; không thêm business rule. Không khẳng định rule FE/BE mới khi source chưa xác nhận.

### Trích từ DD nguồn: F. Tiêu chí nghiệm thu và blockers

### Checklist nghiệm thu

- [x] AD-03 inventory, AC-31, API catalog/DD, backend route/module/query/model/auth/response, test source và UI assets đã được đối chiếu.
- [x] Có plan trước marker/annotation/DD; ảnh nguồn `screen.png` và `code.html` được giữ nguyên.
- [x] Tất cả thành phần nhìn thấy được đánh số; marker JSON/SVG có thứ tự và ánh xạ sang element ID trong mục C.
- [x] A–F mô tả tổng quan, flow, từng element, event/API/errors, states/navigation và checklist.
- [x] API #69 phân biệt contract trực tiếp, local source behavior và fallback `DERIVED`; response fields/error set không bị nhầm với prototype `204`.
- [x] Test source được đọc để truy vết, nhưng không tuyên bố chạy hoặc xác minh runtime/live DB.
- [ ] Admin user-management permission, tenant/MFA/policy được owner duyệt.
- [ ] Live legacy schema/grants/deployment hoặc schema UUID target được xác định.
- [ ] PII masking/visibility, enum labels và lifecycle status được duyệt.
- [ ] Audit API/event source, empty/count semantics, retention và compliance claims được xác nhận hoặc loại bỏ khỏi thiết kế.
- [ ] Study Web route/auth/client và visual design được wire theo `.agents/web-study/design.md`.
- [ ] Back/edit/action/footer destinations và disabled/enabled behavior được xác nhận xuyên AD-02/AD-04/AD-05.

### Open blockers

1. **Admin permission:** local `ADMIN` JWT claim là fallback cho AC-31 user-management permission; policy/tenant/MFA chưa được xác nhận.
2. **Schema:** local query nhắm legacy BIGINT `users`; live DB/deployment chưa xác minh, V1-PILOT dùng UUID model khác.
3. **PII and lifecycle:** email/phone masking, role/status enum, deleted/anonymized user visibility và audit requirements chưa chốt.
4. **Audit panel:** không có nguồn history/log/count/retention trong #69; các claim “0 bản ghi”, 180 ngày, automatic monitoring, RBAC Strict Audit và Nghị định cần nguồn/owner.
5. **Frontend/runtime:** Study Web `UNWIRED`; không có editable source/router/client để implement hoặc runtime-verify route.
6. **Visual consistency:** prototype dùng Plus Jakarta Sans/cobalt treatment; Study Web guide yêu cầu semantic ocean-blue tokens và Inter/system sans-serif. Cần design review khi wire.

**Kết quả:** API #69 `SOURCE-BACKED LOCALLY (R)`; screen `DD BLOCKED`; `IMPLEMENTATION BLOCKED`; `RUNTIME NOT VERIFIED`. Chỉ xử lý AD-03 trong phiên này.

## 3. Quy tắc chưa xác nhận
- `CẦN_XÁC_NHẬN`: các quyết định/blocker trong inventory và DD nguồn chưa được giải quyết.
- Related IDs/source refs: Không có BR ID nguồn được chuẩn hóa.; xem [API](04-api-integration.md), [Events](02-events.md), [Tests](07-test-cases.md).

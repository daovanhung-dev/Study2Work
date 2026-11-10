# AD-02 — Business Rules

## 1. Rule index
| Rule ID (package alias) | Tên / source ID | Áp dụng | Thực thi | Tests |
|---|---|---|---|---|
| `AD-02-BR-001` | Source rules/gates bundle (alias only) | See source DD | Not re-inferred | See source acceptance |

## 2. Rules, security, discrepancy và gate từ source
- Inventory purpose: Bảng users, keyword, status, role, pagination; chọn user để mở AD-03/AD-04; API #68 chỉ đọc.
- Gate/status (giữ nguyên): **R**; **DD BLOCKED; IMPLEMENTATION BLOCKED:** Study Web UNWIRED; role/status options và ID-search mismatch; Add/export/audit/sync unsupported; Admin permission, PII/lifecycle, live schema còn mở; RUNTIME NOT VERIFIED
- BR IDs trong file này chỉ là alias trỏ tới source rule/gate bundles; không thêm business rule. Không khẳng định rule FE/BE mới khi source chưa xác nhận.

### Trích từ DD nguồn: F. Tiêu chí nghiệm thu và blocker

### Static acceptance checklist

- [ ] Route, Admin permission và caller identity được xác nhận; claim `ADMIN` có được dùng làm user-management permission hay không đã được owner duyệt.
- [ ] API #68 query state trong URL khớp inventory; submit/debounce, page reset, empty page display và back/forward behavior được chốt.
- [ ] Search hint phản ánh đúng full_name/email; nếu cần search ID phải có API contract/source cập nhật.
- [ ] Role/status options dùng đúng values được duyệt; không gửi các alias prototype chưa map.
- [ ] Page size/order/total dùng response API; không thêm `size/sort`; không hiển thị page 0 như response page 1.
- [ ] PII email/phone, suspended/deleted visibility, audit access và logging policy được duyệt; list không hiển thị field ngoài contract.
- [ ] Add/export/help/health/sync/audit controls chỉ hoạt động khi có endpoint/route/permission cụ thể; không fake kết quả.
- [ ] Study Web implementation tuân `.agents/web-study/design.md` (ocean semantic tokens, typography, responsive reflow, keyboard/focus, honest loading/error/empty copy); screenshot hiện có discrepancy cần review.
- [ ] `screen.png` và `code.html` gốc giữ nguyên; marker 1–38 khớp một-một với 38 element rows.

### Open blockers

1. `ADMIN` JWT claim hiện là fallback cho AC-31 user-management permission; permission/tenant policy chưa được owner duyệt.
2. UI role/status values không có enum contract. Không tự map `instructor→MENTOR`, `locked→SUSPENDED`, hoặc chữ thường sang uppercase.
3. Search-by-ID trong placeholder không được API #68 hỗ trợ; API chỉ tìm full_name/email.
4. PII email/phone, audit access, lifecycle/deleted visibility và null/omit policy còn mở trong API #68 Draft DD.
5. Add-user, user export, guide target, server sync và audit/health claims không được #68/AC-31 hỗ trợ.
6. Local #68 truy vấn legacy BIGINT `users`; live schema/migration/deployment chưa xác minh và V1-PILOT UUID model khác cấu trúc.
7. Study Web editable source/package/router absent; `/admin/users` chưa wired. API tests có fake DB sessions và không xác minh frontend/runtime/deployment.
8. Screenshot palette/typeface khác Study Web guide; review/approval trước khi làm UI.

**Kết quả:** `DD BLOCKED`; `IMPLEMENTATION BLOCKED`; `RUNTIME NOT VERIFIED`. API #68 local source/test tồn tại nhưng các blocker về contract/policy, schema và frontend vẫn mở.

## 3. Quy tắc chưa xác nhận
- `CẦN_XÁC_NHẬN`: các quyết định/blocker trong inventory và DD nguồn chưa được giải quyết.
- Related IDs/source refs: Không có BR ID nguồn được chuẩn hóa.; xem [API](04-api-integration.md), [Events](02-events.md), [Tests](07-test-cases.md).

# AD-02 — Test Cases

> Các mã `TC` bên dưới là planning references được tạo cho file DD; chúng không phải test suite, không được chạy và không chứng minh implementation/runtime.

## 1. Coverage matrix
| Test ID | Type | Event | Rule/API | Priority |
|---|---|---|---|---|
| `AD-02-TC-001` | Planning ref / not run | `AC-31` | See source acceptance section | P1 |

## 2. Test planning references

### AD-02-TC-001 — Acceptance planning reference (AC-31)
- **Mục tiêu:** Giữ truy vết tới yêu cầu/acceptance đã ghi; đây là test planning reference, không phải test code hoặc kết quả chạy.
- **Precondition:** Đọc nguồn [AD-02](../../screen_stitch/05_admin/AD-02_danh-sach-nguoi-dung/AD-02.md) và gỡ blocker áp dụng trước khi implementation.
- **Mock/test data:** Nguồn không cung cấp fixture dùng để chạy test ở package này; không đưa dữ liệu thật.
- **Steps:**
  1. Đối chiếu acceptance và event tương ứng trong DD nguồn.
  2. Khi runtime/test implementation tồn tại, viết test riêng theo contract đã xác nhận.
- **Expected UI/state:** Theo acceptance/state trong nguồn; chưa được xác minh trên runtime.
- **Expected API/data:** Theo [API Integration](04-api-integration.md); không phát sinh request trong lần tạo tài liệu.
- **Failure / edge assertion:** Không đánh dấu pass cho `UNWIRED`, `IMPLEMENTATION BLOCKED` hoặc `RUNTIME NOT VERIFIED`.
- **References:** `AC-31`, [Events](02-events.md), [Business Rules](05-business-rules.md), [source DD](../../screen_stitch/05_admin/AD-02_danh-sach-nguoi-dung/AD-02.md).

## 3. Source acceptance / test plan (not run)

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

#### Kế hoạch kiểm chứng từ source PLAN

### Trích từ DD nguồn: 7. Tiêu chí kết thúc phiên

- `screen.png` and `code.html` hashes unchanged; original plus annotated PNG present.
- 38 ordered unique markers are in bounds and match exactly 38 DD element rows.
- DD has A–F, source trace, events, API/error mapping, states/navigation, and unresolved decisions clearly separated from approved behavior.
- Inventory/tracker/worklog agree on `R` for source-backed API #68 while screen result remains `DD BLOCKED`, `IMPLEMENTATION BLOCKED`, `RUNTIME NOT VERIFIED` where blockers remain.
- This session handles only AD-02; no other Screen ID is started.

- Runtime status: `RUNTIME NOT VERIFIED` (the generated DD does not claim otherwise).
- Không chạy app test trong task chuyển đổi tài liệu.

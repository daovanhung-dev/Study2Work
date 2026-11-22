# AD-02 — Business Rules

## 1. Rule index
| Rule ID (package alias) | Tên / source ID | Áp dụng | Thực thi | Tests |
|---|---|---|---|---|
| `AD-02-BR-001` | Source rules/gates bundle (alias only) | See source DD | Not re-inferred | See source acceptance |

## 2. Rules, security, discrepancy và gate từ source
- Inventory purpose: Bảng users, keyword, status, role, pagination; chọn user để mở AD-03/AD-04; API #68 đọc danh sách. API #105 là extension được duyệt riêng cho Add user.
- Gate/status: **R**; **DD BLOCKED; IMPLEMENTATION PARTIAL SOURCE:** route/page/#68 caller and approved #105 create flow are wired locally; role/status options và ID-search mismatch; export/audit/sync unsupported; Admin permission, PII/lifecycle, live schema còn mở; authenticated runtime NOT VERIFIED.
- BR IDs trong file này chỉ là alias trỏ tới source rule/gate bundles; không thêm business rule. Không khẳng định rule FE/BE mới khi source chưa xác nhận.

### Trích từ DD nguồn: F. Tiêu chí nghiệm thu và blocker

### Approved Admin create extension — API #105 (2026-11-22)

- Roles: `STUDENT`, `MENTOR`, `ADMIN`; Admin supplies an initial password; new account status is `ACTIVE`.
- The API requires an authenticated `ADMIN` Bearer, trims and validates name/email under the existing server helpers, rejects duplicate email, hashes the submitted nonblank password with the shared Argon2id helper, and returns only the existing safe UserProfile projection. No password or password hash is returned.
- The password rule rejects only empty/all-whitespace input; nonblank password bytes are preserved for hashing. This is a user-approved creation flow and a new API #105 extension; API #68 remains a read-only list API.
- This decision does not resolve the broader AC-31 permission/tenant model, email lifecycle, audit requirements or live database/deployment status.

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
5. User creation is implemented through the approved API #105 extension; user export, guide target, server sync và audit/health claims remain unsupported.
6. Local #68/#105 query legacy BIGINT `users`; live schema/migration/deployment chưa xác minh và V1-PILOT UUID model khác cấu trúc.
7. Focused AD-02 tests cover local #105 form/error/success behavior; browser reached the login gate only. API #105 tests use fake DB sessions and do not verify authenticated frontend, live schema, or deployment.
8. Screenshot palette/typeface khác Study Web guide; review/approval trước khi làm UI.

**Kết quả (2026-11-17):** `DD BLOCKED`; `IMPLEMENTATION PARTIAL SOURCE`; authenticated `RUNTIME NOT VERIFIED`. Local frontend/API source and focused tests exist, while contract/policy, schema, live API/DB and deployment blockers remain.

**Current implementation evidence (2026-11-22):** AD-02 posts through #105, handles success by refreshing the current #68 query and retains the draft on safe errors. Focused Angular tests pass 11/11 and API #105 fake-session tests pass 15/15. Other listed policy/schema/runtime blockers remain open.

## 3. Quy tắc chưa xác nhận
- `CẦN_XÁC_NHẬN`: các quyết định/blocker trong inventory và DD nguồn chưa được giải quyết.
- Related IDs/source refs: Không có BR ID nguồn được chuẩn hóa.; xem [API](04-api-integration.md), [Events](02-events.md), [Tests](07-test-cases.md).

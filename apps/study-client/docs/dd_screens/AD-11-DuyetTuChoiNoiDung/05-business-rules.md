# AD-11 — Business Rules

## 1. Rule index
| Rule ID (package alias) | Tên / source ID | Áp dụng | Thực thi | Tests |
|---|---|---|---|---|
| `AD-11-BR-001` | Source rules/gates bundle (alias only) | See source DD | Not re-inferred | See source acceptance |

## 2. Rules, security, discrepancy và gate từ source
- Inventory purpose: Preview Content được chọn; metadata chỉ hiển thị field có contract; form reason theo #81 sau khi thống nhất validation.
- Gate/status (giữ nguyên): **R** local route/module/test source #79–#81; API DD Draft. **DD BLOCKED; IMPLEMENTATION BLOCKED:** AC `APPROVED/PUBLISHED` vs #80 `APPROVED`; reason required vs optional/disabled; author/version/media/rubric source thiếu; revision/stale policy, moderation permission, live schema/migration và Study Web `UNWIRED` còn mở; **RUNTIME NOT VERIFIED**
- BR IDs trong file này chỉ là alias trỏ tới source rule/gate bundles; không thêm business rule. Không khẳng định rule FE/BE mới khi source chưa xác nhận.

### Trích từ DD nguồn: F. Tiêu chí nghiệm thu và blockers

- [x] Giữ nguyên `screen.png` và `code.html`; có plan được tạo trước marker/DD.
- [x] Annotated PNG 2× từ ảnh gốc; 48 JSON/SVG markers ordered, unique và in-bounds.
- [x] Phần C có một hàng duy nhất cho từng marker #1–#48.
- [x] Expected AC/catalog và current prototype/server source được tách riêng.
- [x] EV-01…EV-08 có trigger, input, processing, output/error và source boundary.
- [x] Mô tả #79 direct eight-field Content; #80 `APPROVED`; #81 `REJECTED`/reason; auth/error/transaction behavior; không gán publish hoặc renderer không có nguồn.
- [x] Có state matrix, handoff AD-10/#78 và unresolved navigation/revision behavior.
- [ ] Owner đồng bộ AC `APPROVED/PUBLISHED` với #80 `APPROVED` và quyết định semantics CTA/publish owner.
- [ ] Owner đồng bộ reason required/empty/whitespace/length/format với UI; mở textarea sau khi policy duyệt.
- [ ] Quyết định source cho author, course title, submitted date, version/revision identity; xác định stale/deleted state và decision concurrency.
- [ ] Quyết định moderation-specific permission; xác nhận live schema/migration 011, grants và retention/access.
- [ ] Cung cấp Content payload/media preview contract và secure renderer nếu còn yêu cầu; xác nhận rubric source/version/applicability/result semantics.
- [ ] Wire Study Web route/API/auth/UI; chốt loading/error/duplicate-submit/retry/success navigation và #78 refresh policy.
- [ ] Reconcile queue/#79/#80/#81 identity và ensure displayed revision is decision revision, hoặc phê duyệt rõ current-logical-row semantics.

**Trạng thái hiện tại:** `DD BLOCKED` · `IMPLEMENTATION BLOCKED` · `RUNTIME NOT VERIFIED`. Route/modules/test source của #79–#81 tồn tại local và được inventory đánh dấu `R`; API DD vẫn Draft. Test files được đọc làm source evidence nhưng không chạy trong phiên này. Fake DB tests không chứng minh live PostgreSQL/schema/deployment/authorization policy.

## 3. Quy tắc chưa xác nhận
- `CẦN_XÁC_NHẬN`: các quyết định/blocker trong inventory và DD nguồn chưa được giải quyết.
- Related IDs/source refs: Không có BR ID nguồn được chuẩn hóa.; xem [API](04-api-integration.md), [Events](02-events.md), [Tests](07-test-cases.md).

# AD-11 — Test Cases

> Các mã `TC` bên dưới là planning references được tạo cho file DD; chúng không phải test suite, không được chạy và không chứng minh implementation/runtime.

## 1. Coverage matrix
| Test ID | Type | Event | Rule/API | Priority |
|---|---|---|---|---|
| `AD-11-TC-001` | Planning ref / not run | `AC-33` | See source acceptance section | P1 |

## 2. Test planning references

### AD-11-TC-001 — Acceptance planning reference (AC-33)
- **Mục tiêu:** Giữ truy vết tới yêu cầu/acceptance đã ghi; đây là test planning reference, không phải test code hoặc kết quả chạy.
- **Precondition:** Đọc nguồn [AD-11](../../screen_stitch/05_admin/AD-11_duyet-tu-choi-noi-dung/AD-11.md) và gỡ blocker áp dụng trước khi implementation.
- **Mock/test data:** Nguồn không cung cấp fixture dùng để chạy test ở package này; không đưa dữ liệu thật.
- **Steps:**
  1. Đối chiếu acceptance và event tương ứng trong DD nguồn.
  2. Khi runtime/test implementation tồn tại, viết test riêng theo contract đã xác nhận.
- **Expected UI/state:** Theo acceptance/state trong nguồn; chưa được xác minh trên runtime.
- **Expected API/data:** Theo [API Integration](04-api-integration.md); không phát sinh request trong lần tạo tài liệu.
- **Failure / edge assertion:** Không đánh dấu pass cho `UNWIRED`, `IMPLEMENTATION BLOCKED` hoặc `RUNTIME NOT VERIFIED`.
- **References:** `AC-33`, [Events](02-events.md), [Business Rules](05-business-rules.md), [source DD](../../screen_stitch/05_admin/AD-11_duyet-tu-choi-noi-dung/AD-11.md).

## 3. Source acceptance / test plan (not run)

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

#### Kế hoạch kiểm chứng từ source PLAN

### Trích từ DD nguồn: 7. Execution and verification order

1. [x] Docs preflight, exact-type worklog selection/review, context map and scope routing.
2. [x] Inspect AD-11 assets/DOM, AC-33, API catalog/DD, route/modules/query/model/validator, focused test source, DB/migration context and Mentor #52 publication path.
3. [x] Save this plan before marker JSON/SVG, annotated PNG or screen DD.
4. [ ] Create ordered 48 JSON/SVG markers and 2× annotated PNG; visually review.
5. [ ] Author A–F DD, 48 element rows, EV-01…EV-08, API/error trace, states/navigation and blockers.
6. [ ] Update inventory AD-11 and reverse API #079–#081 source status; update global tracker/checkpoint and worklog.
7. [ ] Static audit: source hashes/dimensions, JSON/XML, order/coordinates/stroke bounds, C-row bijection, local links, 83 IDs/folders/core-artifact count, whitespace and annotated image. Do not run app tests/runtime.
8. [ ] Finalize worklog and stop after AD-11; AD-12 remains a separate session.

- Runtime status: `RUNTIME NOT VERIFIED` (the generated DD does not claim otherwise).
- Không chạy app test trong task chuyển đổi tài liệu.

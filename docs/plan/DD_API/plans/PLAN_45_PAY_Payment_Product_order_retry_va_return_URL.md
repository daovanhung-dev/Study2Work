# PLAN 45 — Payment — Product, order, retry và return URL

## 1. Thông tin kế hoạch

| Thuộc tính | Giá trị |
|---|---|
| Plan ID | `PLAN-45` |
| API trong phạm vi | `API-PAY-001`, `API-PAY-002`, `API-PAY-003`, `API-PAY-004`, `API-PAY-016` |
| Số API | 5 |
| Read-only / Mutation | 3 / 2 |
| Khối lượng lõi | 40 file template trước khi duplicate DB Mapping |
| Mức rủi ro | Rất cao |
| Trạng thái plan | `READY — SOURCE-GROUNDED`; API có source gap phải giữ Draft |

## 2. Mục tiêu và nghiệp vụ

Tạo DD cho product catalog, tạo/order status/retry và browser return.

**Luồng nghiệp vụ trọng tâm:** Catalog active price; create order snapshot items and payment attempt then redirect; GET source of truth; retry không tạo entitlement; return chỉ hiển thị status, không settle.

**Điểm cần khóa:** Amount integer VND, idempotency, provider state/out-of-order, no entitlement before verified settlement.

**Dependency:** Plan 49 provider webhooks.

## 3. Phạm vi

**In-scope**

- `API-PAY-001` — `GET /api/v1/billing/products`.
- `API-PAY-002` — `POST /api/v1/billing/orders`.
- `API-PAY-003` — `GET /api/v1/billing/orders/{orderId}`.
- `API-PAY-004` — `POST /api/v1/billing/orders/{orderId}/retry`.
- `API-PAY-016` — `GET /api/v1/billing/returns/{provider}`.

**Out-of-scope**

- Không tạo DD cho API ngoài danh sách trên.
- Không sửa BD, template hoặc DD đã approved ngoài phạm vi.
- Không tự tạo endpoint, request/response field, table/column, role, business code, transaction hoặc business rule.
- Không triển khai source code, OpenAPI hoặc migration trong plan này.

## 4. Nguồn bắt buộc và truy vết

- `04_DAC_TA_API.md`: contract HTTP/internal/realtime, quy ước dùng chung, endpoint row, error và transaction matrix.
- `03_THIET_KE_CO_SO_DU_LIEU.md`: table/column/constraint/index/transaction/retention.
- `02_BIEU_DO_HE_THONG.md`: activity, sequence, class, lỗi và cạnh tranh.
- `01_TONG_QUAN_DU_AN.md`: capability, use case, rule, permission, NFR, state machine và acceptance.
- `05_DAC_TA_MAN_HINH.md`: consumer/screen/CTA/validation để kiểm coverage, không thay API source.

**Dòng traceability liên quan**

- `01_TONG_QUAN_DU_AN.md:L776` — `CAP-WRK-009` / `UC-WRK-009`; rules ``BR-WRK-017`, `BR-PAY-006`, `BR-AIX-002–003`, `PERM-WRK-060``; diagrams ``AC-WRK-001`, `AC-PAY-001`, `SEQ-WRK-001`, `SEQ-PAY-001``; data ``CLS-WRK-001`, `CLS-PAY-001`, `CLS-AIX-001`; `TBL-WRK-010–011`, `TBL-PAY-010–013``; screens ``SCR-WRK-013`, `SCR-WRK-022`, `SCR-WRK-034`, `SCR-WRK-043``; test ``TC-WRK-009``.
- `01_TONG_QUAN_DU_AN.md:L781` — `CAP-PAY-001` / `UC-PAY-001`; rules ``BR-PAY-001–004`, `BR-PAY-007`, `NFR-OPS-003``; diagrams ``AC-PAY-001`, `SEQ-PAY-001``; data ``CLS-PAY-001`; `TBL-PAY-001–005``; screens ``SCR-WRK-022–023`, `SCR-WRK-043–044``; test ``TC-PAY-001``.
- `01_TONG_QUAN_DU_AN.md:L782` — `CAP-PAY-002` / `UC-PAY-002`; rules ``BR-PAY-004–007`, `BR-OPS-003`, `NFR-OPS-006``; diagrams ``AC-PAY-001`, `SEQ-PAY-001``; data ``CLS-PAY-001`; `TBL-PAY-003`, `TBL-PAY-005–006`, `TBL-PAY-010–011``; screens ``SCR-WRK-022`, `SCR-WRK-043`; webhook là `SYSTEM``; test ``TC-PAY-002``.

**Diagram/Class cần đọc toàn bộ section**

- `AC-WRK-001` — `02_BIEU_DO_HE_THONG.md:L548` — AC-WRK-001 — Candidate privacy, search, invitation và opt-out.
- `AC-PAY-001` — `02_BIEU_DO_HE_THONG.md:L729` — AC-PAY-001 — Checkout, callback, entitlement và reversal.
- `SEQ-WRK-001` — `02_BIEU_DO_HE_THONG.md:L2080` — SEQ-WRK-001 — Candidate opt-in/search, sponsored label và opt-out SLA.
- `SEQ-PAY-001` — `02_BIEU_DO_HE_THONG.md:L2415` — SEQ-PAY-001 — Checkout VNPAY/MoMo, IPN/webhook và entitlement once.
- `CLS-WRK-001` — `02_BIEU_DO_HE_THONG.md:L1266` — CLS-WRK-001 — Candidate, tenant, job, application và ATS snapshots.
- `CLS-PAY-001` — `02_BIEU_DO_HE_THONG.md:L1501` — CLS-PAY-001 — Order, provider event, ledger, entitlement và promotion.
- `CLS-AIX-001` — `02_BIEU_DO_HE_THONG.md:L1584` — CLS-AIX-001 — AI job, provenance, review và human-applied revision.

**Bảng dữ liệu liên quan theo traceability**

- `TBL-WRK-010` — `cvs` — `03_THIET_KE_CO_SO_DU_LIEU.md:L768 `.
- `TBL-WRK-011` — `cv_versions` — `03_THIET_KE_CO_SO_DU_LIEU.md:L775 `.
- `TBL-PAY-010` — `entitlements` — `03_THIET_KE_CO_SO_DU_LIEU.md:L1235 `.
- `TBL-PAY-011` — `credit_ledger_entries` — `03_THIET_KE_CO_SO_DU_LIEU.md:L1242 `.
- `TBL-PAY-012` — `promotion_campaigns` — `03_THIET_KE_CO_SO_DU_LIEU.md:L1249 `.
- `TBL-PAY-013` — `sponsored_placements` — `03_THIET_KE_CO_SO_DU_LIEU.md:L1256 `.
- `TBL-PAY-001` — `products` — `03_THIET_KE_CO_SO_DU_LIEU.md:L1172 `.
- `TBL-PAY-002` — `product_prices` — `03_THIET_KE_CO_SO_DU_LIEU.md:L1179 `.
- `TBL-PAY-003` — `orders` — `03_THIET_KE_CO_SO_DU_LIEU.md:L1186 `.
- `TBL-PAY-004` — `order_items` — `03_THIET_KE_CO_SO_DU_LIEU.md:L1193 `.
- `TBL-PAY-005` — `payment_attempts` — `03_THIET_KE_CO_SO_DU_LIEU.md:L1200 `.
- `TBL-PAY-006` — `payment_webhook_events` — `03_THIET_KE_CO_SO_DU_LIEU.md:L1207 `.

**Screen và acceptance**

- Screens: `SCR-WRK-013`, `SCR-WRK-022`, `SCR-WRK-034`, `SCR-WRK-043`, `SCR-WRK-023`, `SCR-WRK-044`.
- Acceptance: `TC-WRK-009`, `TC-PAY-001`, `TC-PAY-002`.

**Rule/permission/NFR IDs phải reconcile**

- `BR-WRK-017` — `01_TONG_QUAN_DU_AN.md:L389` — Sponsored profile/job luôn có nhãn, slot/rank riêng và trường `organicScore` không đổi. Payment không được tăng match score, ATS score hoặc quyền xem field riêng tư..
- `BR-PAY-006` — `01_TONG_QUAN_DU_AN.md:L425` — Chỉ `SETTLED` tạo entitlement/credit ledger đúng một lần trong cùng transaction. Entitlement không được âm; mọi consume/refund/expire là ledger append-only..
- `BR-AIX-002` — `01_TONG_QUAN_DU_AN.md:L436` — AI chỉ tạo CV/JD draft, writing suggestion, match explanation và shortlist suggestion. Output không tự publish, gửi, apply, thay đổi ATS, reject, offer hoặc hire..
- `BR-AIX-003` — `01_TONG_QUAN_DU_AN.md:L437` — Người dùng phải nhìn thấy nhãn AI, review và chủ động accept/edit/reject. Bản accept lưu nội dung người dùng xác nhận, không giả định AI đúng..
- `PERM-WRK-060` — `01_TONG_QUAN_DU_AN.md:L179` — `work.promotions.manage` — Enterprise Owner/Admin có entitlement.
- `BR-PAY-001` — `01_TONG_QUAN_DU_AN.md:L420` — V1 chỉ hỗ trợ gói/credit trả trước bằng VND qua VNPAY và MoMo cho Student hoặc Enterprise; số tiền là integer VND, không auto-renew..
- `BR-PAY-002` — `01_TONG_QUAN_DU_AN.md:L421` — Hệ thống không thu/lưu PAN, CVV, tài khoản ngân hàng hoặc credential provider; không có ví nội bộ, escrow, payout hay số dư rút tiền..
- `BR-PAY-003` — `01_TONG_QUAN_DU_AN.md:L422` — Order giữ immutable snapshot package, giá, thuế/giảm giá nếu có, buyer type/ID và policy version. Đổi catalog không sửa order cũ..
- `BR-PAY-004` — `01_TONG_QUAN_DU_AN.md:L423` — Webhook/IPN đã xác thực chữ ký và đối chiếu merchant/order/amount/currency là nguồn xác nhận. Return URL không được cấp entitlement hoặc tự đánh dấu thanh toán thành công..
- `BR-PAY-007` — `01_TONG_QUAN_DU_AN.md:L426` — Order chưa xác nhận quá thời hạn provider chuyển `EXPIRED`. `CANCELLED` chỉ được commit khi provider/chưa khởi tạo attempt xác nhận chưa thu tiền; verified success thắng trong cùng row lock. Callback success hợp lệ đến muộn được reconciliation xử lý và không cấp trùng..
- `NFR-OPS-003` — `01_TONG_QUAN_DU_AN.md:L650` — p95 server latency: read đồng bộ ≤ 800 ms, mutation đồng bộ ≤ 1,5 giây; không tính phần việc đã công bố async. Query report lớn bắt buộc async/export..
- `BR-PAY-005` — `01_TONG_QUAN_DU_AN.md:L424` — Callback duplicate/out-of-order được lưu raw payload đã bảo vệ, xử lý idempotent và theo state precedence; late failure không hạ `SETTLED`. Amount/order mismatch vào review, không cấp quyền lợi..
- `BR-OPS-003` — `01_TONG_QUAN_DU_AN.md:L450` — Notification và side effect ngoài transaction được tạo qua outbox với dedupe key. Retry exponential có giới hạn; hết retry vào DLQ và cảnh báo..
- `NFR-OPS-006` — `01_TONG_QUAN_DU_AN.md:L653` — Outbox/event projection p95 ≤ 60 giây khi bình thường; evidence export p95 ≤ 2 phút. Backlog, oldest age, retry và DLQ có alert..

## 5. Chi tiết từng API

### API-PAY-001 — `GET /api/v1/billing/products`

- **Nguồn contract:** `04_DAC_TA_API.md:L375`.
- **Actor/quyền:** Authenticated.
- **Input/validation → output:** Audience STUDENT/ENTERPRISE → active products/prices/benefits.
- **Xử lý và dữ liệu:** R versioned catalog; enterprise price still VND integer.
- **Vận hành:** Cache 5m, ETag.
- **Lỗi đặc thù:** `AUDIENCE_INVALID`.
- **Màn hình/consumer:** `SCR-WRK-022`, `SCR-WRK-043`.
- **Capability/use case:** `CAP-WRK-009`, `UC-WRK-009`, `CAP-PAY-001`, `UC-PAY-001`.

**Tác vụ khi tạo DD cho API này**

1. Tách riêng từng header, path, query, body field và token/session-derived input; không suy diễn field từ UI nếu API source không nêu.
2. Lập Request Usage Matrix: mỗi field phải trỏ tới validation, query, branch, loop, mutation hoặc response usage.
3. Phân rã `Xử lý và dữ liệu` thành step Data Mapping theo đúng thứ tự: auth → permission/tenant → validation → query/check → branch/loop → mutation/TX → outbox → response.
4. Với mọi `R:`/query: xác nhận table ID/name/cột/index tại `03_THIET_KE_CO_SO_DU_LIEU.md`; mỗi selected column, JOIN và condition một dòng.
5. Với mọi `W:`/mutation: tạo Mutation Matrix và một DB Mapping file cho từng table/operation khác bản chất; mỗi DB column một row.
6. Map từng response path về DB/query/generated/fixed/calculated source. Field chưa có nguồn phải ghi `SOURCE_REQUIRED`, không tự tạo.
7. Tạo từng Error row từ lỗi đặc thù và lỗi dùng chung thực sự có branch; không đưa toàn bộ catalog lỗi vào API một cách máy móc.
8. Kiểm tra idempotency, `If-Match`, lock, transaction boundary, rollback, audit, event/outbox, cache và rate limit đúng nguồn.
9. Đối chiếu screen/consumer để kiểm coverage, nhưng không dùng UI âm thầm thay đổi API contract.

### API-PAY-002 — `POST /api/v1/billing/orders`

- **Nguồn contract:** `04_DAC_TA_API.md:L376`.
- **Actor/quyền:** Student or tenant billing member.
- **Input/validation → output:** Product/price version, quantity, provider VNPAY/MOMO, tenant context optional, return path allowlist → order + provider redirect/deeplink.
- **Xử lý và dữ liệu:** TX validate price/audience/permission; compute amount server-side; create order/attempt`CREATED`, idempotency/outbox. Adapter call after commit; update order/attempt `PENDING` trong follow-up TX.
- **Vận hành:** Idempotency required; audit; 10/hour.
- **Lỗi đặc thù:** `PRICE_VERSION_STALE`, `BILLING_PERMISSION_REQUIRED`, `PROVIDER_UNAVAILABLE`, `ORDER_ALREADY_ACTIVE`.
- **Màn hình/consumer:** `SCR-WRK-022`, `SCR-WRK-043`.
- **Capability/use case:** `CAP-WRK-009`, `UC-WRK-009`, `CAP-PAY-001`, `UC-PAY-001`.

**Tác vụ khi tạo DD cho API này**

1. Tách riêng từng header, path, query, body field và token/session-derived input; không suy diễn field từ UI nếu API source không nêu.
2. Lập Request Usage Matrix: mỗi field phải trỏ tới validation, query, branch, loop, mutation hoặc response usage.
3. Phân rã `Xử lý và dữ liệu` thành step Data Mapping theo đúng thứ tự: auth → permission/tenant → validation → query/check → branch/loop → mutation/TX → outbox → response.
4. Với mọi `R:`/query: xác nhận table ID/name/cột/index tại `03_THIET_KE_CO_SO_DU_LIEU.md`; mỗi selected column, JOIN và condition một dòng.
5. Với mọi `W:`/mutation: tạo Mutation Matrix và một DB Mapping file cho từng table/operation khác bản chất; mỗi DB column một row.
6. Map từng response path về DB/query/generated/fixed/calculated source. Field chưa có nguồn phải ghi `SOURCE_REQUIRED`, không tự tạo.
7. Tạo từng Error row từ lỗi đặc thù và lỗi dùng chung thực sự có branch; không đưa toàn bộ catalog lỗi vào API một cách máy móc.
8. Kiểm tra idempotency, `If-Match`, lock, transaction boundary, rollback, audit, event/outbox, cache và rate limit đúng nguồn.
9. Đối chiếu screen/consumer để kiểm coverage, nhưng không dùng UI âm thầm thay đổi API contract.

### API-PAY-003 — `GET /api/v1/billing/orders/{orderId}`

- **Nguồn contract:** `04_DAC_TA_API.md:L377`.
- **Actor/quyền:** Purchaser or tenant finance member.
- **Input/validation → output:** → order/provider/payment/entitlement/refund state.
- **Xử lý và dữ liệu:** Owner/tenant composite predicate; R projections built from ledger/webhook.
- **Vận hành:** Private no-store.
- **Lỗi đặc thù:** `ORDER_NOT_FOUND`.
- **Màn hình/consumer:** `SCR-WRK-022`, `SCR-WRK-043`.
- **Capability/use case:** `CAP-WRK-009`, `UC-WRK-009`, `CAP-PAY-001`, `UC-PAY-001`, `CAP-PAY-002`, `UC-PAY-002`.

**Tác vụ khi tạo DD cho API này**

1. Tách riêng từng header, path, query, body field và token/session-derived input; không suy diễn field từ UI nếu API source không nêu.
2. Lập Request Usage Matrix: mỗi field phải trỏ tới validation, query, branch, loop, mutation hoặc response usage.
3. Phân rã `Xử lý và dữ liệu` thành step Data Mapping theo đúng thứ tự: auth → permission/tenant → validation → query/check → branch/loop → mutation/TX → outbox → response.
4. Với mọi `R:`/query: xác nhận table ID/name/cột/index tại `03_THIET_KE_CO_SO_DU_LIEU.md`; mỗi selected column, JOIN và condition một dòng.
5. Với mọi `W:`/mutation: tạo Mutation Matrix và một DB Mapping file cho từng table/operation khác bản chất; mỗi DB column một row.
6. Map từng response path về DB/query/generated/fixed/calculated source. Field chưa có nguồn phải ghi `SOURCE_REQUIRED`, không tự tạo.
7. Tạo từng Error row từ lỗi đặc thù và lỗi dùng chung thực sự có branch; không đưa toàn bộ catalog lỗi vào API một cách máy móc.
8. Kiểm tra idempotency, `If-Match`, lock, transaction boundary, rollback, audit, event/outbox, cache và rate limit đúng nguồn.
9. Đối chiếu screen/consumer để kiểm coverage, nhưng không dùng UI âm thầm thay đổi API contract.

### API-PAY-004 — `POST /api/v1/billing/orders/{orderId}/retry`

- **Nguồn contract:** `04_DAC_TA_API.md:L378`.
- **Actor/quyền:** Owner/billing member.
- **Input/validation → output:** Provider optional → new attempt.
- **Xử lý và dữ liệu:** TX L order; only unpaid/nonexpired; create new provider attempt; old callback can settle order only if amount/order valid and none settled.
- **Vận hành:** Idempotency; audit.
- **Lỗi đặc thù:** `ORDER_NOT_RETRYABLE`, `ORDER_ALREADY_SETTLED`.
- **Màn hình/consumer:** `SCR-WRK-022`, `SCR-WRK-043`.
- **Capability/use case:** `CAP-WRK-009`, `UC-WRK-009`, `CAP-PAY-001`, `UC-PAY-001`.

**Tác vụ khi tạo DD cho API này**

1. Tách riêng từng header, path, query, body field và token/session-derived input; không suy diễn field từ UI nếu API source không nêu.
2. Lập Request Usage Matrix: mỗi field phải trỏ tới validation, query, branch, loop, mutation hoặc response usage.
3. Phân rã `Xử lý và dữ liệu` thành step Data Mapping theo đúng thứ tự: auth → permission/tenant → validation → query/check → branch/loop → mutation/TX → outbox → response.
4. Với mọi `R:`/query: xác nhận table ID/name/cột/index tại `03_THIET_KE_CO_SO_DU_LIEU.md`; mỗi selected column, JOIN và condition một dòng.
5. Với mọi `W:`/mutation: tạo Mutation Matrix và một DB Mapping file cho từng table/operation khác bản chất; mỗi DB column một row.
6. Map từng response path về DB/query/generated/fixed/calculated source. Field chưa có nguồn phải ghi `SOURCE_REQUIRED`, không tự tạo.
7. Tạo từng Error row từ lỗi đặc thù và lỗi dùng chung thực sự có branch; không đưa toàn bộ catalog lỗi vào API một cách máy móc.
8. Kiểm tra idempotency, `If-Match`, lock, transaction boundary, rollback, audit, event/outbox, cache và rate limit đúng nguồn.
9. Đối chiếu screen/consumer để kiểm coverage, nhưng không dùng UI âm thầm thay đổi API contract.

### API-PAY-016 — `GET /api/v1/billing/returns/{provider}`

- **Nguồn contract:** `04_DAC_TA_API.md:L395`.
- **Actor/quyền:** Browser redirect.
- **Input/validation → output:** Provider order/reference only → sanitized status page payload.
- **Xử lý và dữ liệu:** Never trust success query; lookup internal order for authenticated owner or opaque return nonce; return PENDING until webhook/reconcile.
- **Vận hành:** No entitlement; no-store.
- **Lỗi đặc thù:** `RETURN_REFERENCE_INVALID`.
- **Màn hình/consumer:** `SCR-WRK-023`, `SCR-WRK-044`.
- **Capability/use case:** `CAP-PAY-001`, `UC-PAY-001`.

**Tác vụ khi tạo DD cho API này**

1. Tách riêng từng header, path, query, body field và token/session-derived input; không suy diễn field từ UI nếu API source không nêu.
2. Lập Request Usage Matrix: mỗi field phải trỏ tới validation, query, branch, loop, mutation hoặc response usage.
3. Phân rã `Xử lý và dữ liệu` thành step Data Mapping theo đúng thứ tự: auth → permission/tenant → validation → query/check → branch/loop → mutation/TX → outbox → response.
4. Với mọi `R:`/query: xác nhận table ID/name/cột/index tại `03_THIET_KE_CO_SO_DU_LIEU.md`; mỗi selected column, JOIN và condition một dòng.
5. Với mọi `W:`/mutation: tạo Mutation Matrix và một DB Mapping file cho từng table/operation khác bản chất; mỗi DB column một row.
6. Map từng response path về DB/query/generated/fixed/calculated source. Field chưa có nguồn phải ghi `SOURCE_REQUIRED`, không tự tạo.
7. Tạo từng Error row từ lỗi đặc thù và lỗi dùng chung thực sự có branch; không đưa toàn bộ catalog lỗi vào API một cách máy móc.
8. Kiểm tra idempotency, `If-Match`, lock, transaction boundary, rollback, audit, event/outbox, cache và rate limit đúng nguồn.
9. Đối chiếu screen/consumer để kiểm coverage, nhưng không dùng UI âm thầm thay đổi API contract.


## 6. Quy trình thực thi chi tiết

### Bước 0 — Nạp baseline bắt buộc

1. Đọc toàn bộ `createDD_MARKDOWN_SKILL.md` trước khi thao tác.
2. Mở đủ 8 file trong `DD_API_Template_MD/`; ghi fingerprint và heading/table/link baseline.
3. Đọc hai bộ mẫu chỉ để học style; không sao chép nghiệp vụ, table, column, role, error hoặc SQL.
4. Xác nhận 5 tài liệu BD đều đọc được; nếu thiếu một nguồn liên quan thì dừng API bị ảnh hưởng với `BLOCKED — MISSING SOURCE`.

### Bước 1 — Khóa phạm vi và source of truth

1. Tạo API Requirement Matrix chỉ cho các API trong plan.
2. Ghi rõ API ID, method/path, actor, auth, permission, input/output, screen, business rules, tables, transaction và event.
3. Phân loại từng dữ kiện `DIRECT`, `DERIVED`, `ASSUMPTION`, `CONFLICT` hoặc `UNSUPPORTED`.
4. API name canonical chưa có nguồn phải để `SOURCE_REQUIRED`; không biến endpoint slug thành tên approved.
5. Bất kỳ khác biệt giữa API, diagram, DB và screen phải vào `OPEN_QUESTIONS.md`; không chọn âm thầm.

### Bước 2 — Tạo bốn ma trận trước authoring

1. **Request Usage Matrix:** một row cho từng request/header/path/query/body/token field.
2. **Query Matrix:** một row cho từng query; liệt kê base table, alias, từng column, JOIN/ON, WHERE, GROUP/HAVING, ORDER, pagination, lock và result variable.
3. **Mutation Matrix:** một row cho từng INSERT/UPDATE/DELETE/UPSERT; ghi target table, record condition, field/value source, audit, TX và failure behavior.
4. **Response Source Matrix:** một row cho từng response path, kể cả nested/array; ghi source, transform và null/empty/omit rule.
5. Không điền template khi còn gap chưa được đánh dấu.

### Bước 3 — Tạo folder DD từ template

1. Copy nguyên folder template; không sửa template gốc.
2. Đặt folder theo `<API_ID>_<API_NAME>` khi có approved name; nếu chưa có, dùng working name có nhãn `DERIVED` và giữ trạng thái Draft.
3. Giữ `00_Cover.md` đến `07_table.md`, prefix, YAML, heading và table header.
4. Duplicate `07_table.md` thành `07+_<table>_<operation>.md` đúng từng mutation; read-only ghi `N/A — READ-ONLY API` theo template.

### Bước 4 — Thiết kế `05_Data_Mapping.md` trước

1. Nhận header/token/request, normalize và tạo biến; mỗi biến một dòng.
2. Xác thực JWT/service JWT, account projection, MFA/step-up và tenant scope.
3. Validate required/type/length/range/enum/format/unknown field; mỗi điều kiện một dòng.
4. Mô tả business check, state machine, permission, consent, entitlement và concurrency bằng branch cụ thể.
5. Viết từng query với mục đích, table/alias, từng cột, JOIN/ON, WHERE, ORDER/GROUP/HAVING, pagination/index/lock.
6. Viết transaction boundary, mutation order, audit column, outbox, commit/rollback và retry/failure behavior.
7. Map từng response field cụ thể; không dùng câu “map response” hoặc “truy vấn dữ liệu”.
8. Mỗi error branch liên kết tới anchor cụ thể trong `06_Error.md`; mỗi mutation liên kết hai chiều với DB Mapping.

### Bước 5 — Điền các file còn lại

1. `02_Overview.md`: mục đích, actor, auth, permission, source, tables read/write, TX, side effect, assumption/conflict, security/performance.
2. `03_Request.md`: mỗi input field một row, location rõ, validation/default/constraint và Data Mapping reference; JSON hợp lệ.
3. DB Mapping: mỗi column một row, source/value/audit/condition/step/TX; không thêm column không có schema.
4. `04_Response.md`: mỗi response path một row, source/transform/null rule; JSON success hợp lệ và không lộ dữ liệu nhạy cảm.
5. `06_Error.md`: mỗi lỗi một row, HTTP/business code/condition/handling/rollback/response/step.
6. `00_Cover.md` và `01_Lich_su.md`: metadata một hàng; unknown owner/version/date ghi `TBD — Cần xác nhận`.

### Bước 6 — Review chéo và kiểm chứng

1. Request → Data Mapping: 100% field được dùng hoặc giải thích.
2. Data Mapping → DB: table/column/alias/index/constraint tồn tại và đúng owner database.
3. DB/query → Response: 100% response field có source hoặc gap rõ.
4. Data Mapping → Error: 100% error branch có row; code/HTTP thống nhất.
5. Mutation → DB Mapping: mọi changed table/operation được bao phủ; transaction/rollback nhất quán.
6. Validate YAML, Markdown table, code fence, JSON, relative link/anchor, Unicode và one-field-per-line.
7. Chỉ báo `DONE` khi toàn bộ gate đạt; còn source gap dùng `PARTIALLY COMPLETED`, `BLOCKED` hoặc `NEEDS USER DECISION`.

## 7. Quality Gate riêng của plan

- [ ] Đủ DD folder cho toàn bộ API trong phạm vi, không thừa/thiếu API.
- [ ] Method/path/actor/permission khớp `04_DAC_TA_API.md`.
- [ ] Mọi source gap được ghi `SOURCE_REQUIRED`, `DERIVED` hoặc `CONFLICT`; không silently fill.
- [ ] Mỗi request/response/error/column/condition một row hoặc một dòng.
- [ ] Mỗi query có table, columns, JOIN/ON, WHERE, sort/group/pagination/index/lock khi áp dụng.
- [ ] Mỗi mutation có DB Mapping, audit, transaction, rollback và failure behavior.
- [ ] Request ↔ Data Mapping ↔ DB ↔ Response ↔ Error liên kết và nhất quán.
- [ ] JSON parse được; Markdown table/code fence/link/anchor hợp lệ.
- [ ] Có `PLAN_RESULT.md`, `VERIFICATION_REPORT.md`; có `OPEN_QUESTIONS.md` khi còn gap.

## 8. Deliverables của plan

1. 5 folder API DD tương ứng.
2. `PLAN_RESULT.md` cập nhật trạng thái từng API.
3. `VERIFICATION_REPORT.md` cho scope của plan.
4. `OPEN_QUESTIONS.md` nếu còn ảnh hưởng contract/DB/security/transaction.
5. `BUSINESS_CODE_DELTA.md` chỉ khi có code mới được nguồn approved xác nhận.

## 9. Điều kiện dừng

- Dừng API cụ thể nếu không xác định được request/response contract, target DB table/column, permission, transaction hoặc business code bắt buộc.
- Không được báo `DONE` cho API còn `SOURCE_REQUIRED`, conflict chưa quyết định hoặc validation chưa đạt.

Quay lại: [00_API_DD_PLAN_INDEX.md](../00_API_DD_PLAN_INDEX.md)

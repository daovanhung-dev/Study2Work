# ME-13 — Test Cases

> Các mã `TC` bên dưới là planning references được tạo cho file DD; chúng không phải test suite, không được chạy và không chứng minh implementation/runtime.

## 1. Coverage matrix
| Test ID | Type | Event | Rule/API | Priority |
|---|---|---|---|---|
| `ME-13-TC-001` | Planning ref / not run | `AC-25` | See source acceptance section | P2 |

## 2. Test planning references

### ME-13-TC-001 — Acceptance planning reference (AC-25)
- **Mục tiêu:** Giữ truy vết tới yêu cầu/acceptance đã ghi; đây là test planning reference, không phải test code hoặc kết quả chạy.
- **Precondition:** Đọc nguồn [ME-13](../../screen_stitch/04_mentor/ME-13_chon-nguoi-nhan-thong-bao/ME-13.md) và gỡ blocker áp dụng trước khi implementation.
- **Mock/test data:** Nguồn không cung cấp fixture dùng để chạy test ở package này; không đưa dữ liệu thật.
- **Steps:**
  1. Đối chiếu acceptance và event tương ứng trong DD nguồn.
  2. Khi runtime/test implementation tồn tại, viết test riêng theo contract đã xác nhận.
- **Expected UI/state:** Theo acceptance/state trong nguồn; chưa được xác minh trên runtime.
- **Expected API/data:** Theo [API Integration](04-api-integration.md); không phát sinh request trong lần tạo tài liệu.
- **Failure / edge assertion:** Không đánh dấu pass cho `UNWIRED`, `IMPLEMENTATION BLOCKED` hoặc `RUNTIME NOT VERIFIED`.
- **References:** `AC-25`, [Events](02-events.md), [Business Rules](05-business-rules.md), [source DD](../../screen_stitch/04_mentor/ME-13_chon-nguoi-nhan-thong-bao/ME-13.md).

## 3. Source acceptance / test plan (not run)

### Trích từ DD nguồn: F. Tiêu chí nghiệm thu

- [x] Source screenshot and HTML were inventoried; original files are preserved.
- [x] Annotated image exists, with sequential 1–49 markers.
- [x] Marker JSON, SVG, plan and this document use the same 49-element order.
- [x] Every visible numbered marker has one element row with type, location/purpose, data/properties, visibility/state and event mapping.
- [x] Eight events describe input, prerequisites, processing, output and applicable API/errors; E04 is explicitly absent from the prototype.
- [x] #46/#62 route/query/auth/ownership/response/error behavior was traced to local source and test files.
- [x] #63 was traced as a downstream dependency; direct contract, derived mapping, transaction, response IDs and delivery limits remain separate.
- [x] Expected claims and current behavior are separate; slugs, semester, support criteria, anonymity, channel, WCAG and handoff gaps are explicit.
- [x] Proposed routes and navigation are labeled as unimplemented; no runtime claim is made.
- [ ] Product/API decisions listed in A and D are approved; until then DD remains BLOCKED and frontend implementation remains BLOCKED.
- [ ] Runtime behavior verified in a wired Study Web app; NOT VERIFIED in this session.

### Static acceptance result

DD is BLOCKED because course ID/eligibility mapping, support-needed semantics, recipient UI/handoff, #63 course/content contract and unsupported privacy/channel claims prevent implementation without product/API inference. IMPLEMENTATION BLOCKED. RUNTIME NOT VERIFIED. API files/tests are local source evidence only; tests and runtime were not run in this documentation session.

#### Kế hoạch kiểm chứng từ source PLAN

### Trích từ DD nguồn: 8. Static review gate

- Confirm source screenshot and HTML hashes are unchanged.
- Confirm marker IDs are exactly 1..49, unique, within 1600×1546, and align with 49 DD element rows.
- Confirm SVG parses and marker count/order/titles match JSON.
- Inspect the annotated image at full size for clipping or text obstruction.
- Confirm all API/event errors, empty states, navigation destinations, unresolved contract points and implementation/runtime statuses are stated.
- Do not run application tests or claim runtime verification for this documentation-only task.

- Runtime status: `RUNTIME NOT VERIFIED` (the generated DD does not claim otherwise).
- Không chạy app test trong task chuyển đổi tài liệu.

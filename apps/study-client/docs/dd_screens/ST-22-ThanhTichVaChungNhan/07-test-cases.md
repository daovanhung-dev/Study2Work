# ST-22 — Test Cases

> Các mã `TC` bên dưới là planning references được tạo cho file DD; chúng không phải test suite, không được chạy và không chứng minh implementation/runtime.

## 1. Coverage matrix
| Test ID | Type | Event | Rule/API | Priority |
|---|---|---|---|---|
| `ST-22-TC-001` | Planning ref / not run | `AC-18` | See source acceptance section | P2 |

## 2. Test planning references

### ST-22-TC-001 — Acceptance planning reference (AC-18)
- **Mục tiêu:** Giữ truy vết tới yêu cầu/acceptance đã ghi; đây là test planning reference, không phải test code hoặc kết quả chạy.
- **Precondition:** Đọc nguồn [ST-22](../../screen_stitch/03_student/ST-22_thanh-tich-va-chung-nhan/ST-22.md) và gỡ blocker áp dụng trước khi implementation.
- **Mock/test data:** Nguồn không cung cấp fixture dùng để chạy test ở package này; không đưa dữ liệu thật.
- **Steps:**
  1. Đối chiếu acceptance và event tương ứng trong DD nguồn.
  2. Khi runtime/test implementation tồn tại, viết test riêng theo contract đã xác nhận.
- **Expected UI/state:** Theo acceptance/state trong nguồn; chưa được xác minh trên runtime.
- **Expected API/data:** Theo [API Integration](04-api-integration.md); không phát sinh request trong lần tạo tài liệu.
- **Failure / edge assertion:** Không đánh dấu pass cho `UNWIRED`, `IMPLEMENTATION BLOCKED` hoặc `RUNTIME NOT VERIFIED`.
- **References:** `AC-18`, [Events](02-events.md), [Business Rules](05-business-rules.md), [source DD](../../screen_stitch/03_student/ST-22_thanh-tich-va-chung-nhan/ST-22.md).

## 3. Source acceptance / test plan (not run)

### Trích từ DD nguồn: F. Tiêu chí nghiệm thu

- [x] Screen ID, actor, inventory route, AC/API and linked screens are recorded with source links.
- [x] Original `screen.png` and `code.html` are preserved; the loaded PNG vs static empty HTML discrepancy is explicit.
- [x] All 46 visual groups have unique ordered markers and one corresponding element row.
- [x] Fifteen recognized event groups have trigger/type, explicit marker or lifecycle element, preconditions, inputs, ordered handling, result and exceptions; unsupported actions are explicitly blocked.
- [x] API #38 method/path/auth/query/body/response/statuses are transcribed without adding fields/statuses/paging controls.
- [x] Loading/empty/earned/error states, navigation relationships and current implementation status are separated.
- [x] Screenshot claims unsupported by #38 are marked sample/UI-only; no award, certificate, proof, metric, filter or eligibility rules are invented.
- [ ] **DD READY:** blocked until award definition/projection/empty/page/filter policy and decision on certificate/proof/metric/competency/next-certificate claims are approved; route/visual source target also needs confirmation.
- [ ] **IMPLEMENTATION READY:** blocked until Study Web route/components and API #38 runtime contract/source are wired and verified.
- [ ] **RUNTIME VERIFIED:** no runtime UI or API call was available/attempted in this documentation task.

#### Kế hoạch kiểm chứng từ source PLAN

### Trích từ DD nguồn: 7. Verification plan

- Record PNG/HTML source hashes/dimensions and preserve both byte-for-byte.
- Use original PNG for annotation because it is a valid, complete image; document HTML mismatch. Check marker order/uniqueness/bounds, exact DD row mapping, SVG parse and visual readability/non-obscuration.
- Verify DD A–F, event sequence and element/type/precondition mapping, API method/path/auth/fields/statuses, no unauthorized query fields, link resolution, tracker counts/pointers and `git diff --check`.
- No tests or runtime API calls unless requested; run context validator only if a context page/manifest is changed.

- Runtime status: `RUNTIME NOT VERIFIED` (the generated DD does not claim otherwise).
- Không chạy app test trong task chuyển đổi tài liệu.

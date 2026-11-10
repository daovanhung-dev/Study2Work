# AD-22 — Test Cases

> Các mã `TC` bên dưới là planning references được tạo cho file DD; chúng không phải test suite, không được chạy và không chứng minh implementation/runtime.

## 1. Coverage matrix
| Test ID | Type | Event | Rule/API | Priority |
|---|---|---|---|---|
| `AD-22-TC-001` | Planning ref / not run | `AC-37` | See source acceptance section | P1 |

## 2. Test planning references

### AD-22-TC-001 — Acceptance planning reference (AC-37)
- **Mục tiêu:** Giữ truy vết tới yêu cầu/acceptance đã ghi; đây là test planning reference, không phải test code hoặc kết quả chạy.
- **Precondition:** Đọc nguồn [AD-22](../../screen_stitch/05_admin/AD-22_danh-sach-thao-luan-bi-bao-cao/AD-22.md) và gỡ blocker áp dụng trước khi implementation.
- **Mock/test data:** Nguồn không cung cấp fixture dùng để chạy test ở package này; không đưa dữ liệu thật.
- **Steps:**
  1. Đối chiếu acceptance và event tương ứng trong DD nguồn.
  2. Khi runtime/test implementation tồn tại, viết test riêng theo contract đã xác nhận.
- **Expected UI/state:** Theo acceptance/state trong nguồn; chưa được xác minh trên runtime.
- **Expected API/data:** Theo [API Integration](04-api-integration.md); không phát sinh request trong lần tạo tài liệu.
- **Failure / edge assertion:** Không đánh dấu pass cho `UNWIRED`, `IMPLEMENTATION BLOCKED` hoặc `RUNTIME NOT VERIFIED`.
- **References:** `AC-37`, [Events](02-events.md), [Business Rules](05-business-rules.md), [source DD](../../screen_stitch/05_admin/AD-22_danh-sach-thao-luan-bi-bao-cao/AD-22.md).

## 3. Source acceptance / test plan (not run)

### Trích từ DD nguồn: F. Tiêu chí nghiệm thu

- [x] Inventory row 80, AC-37 and direct #97/#98 catalog reviewed; expected and current evidence separated.
- [x] Current #97 route, guard, validator, query, projection, errors and read-only effect documented; local `DERIVED` choices labeled.
- [x] Prototype search/status/reason/severity/refresh/pagination/navigation behavior documented from HTML.
- [x] All visible component groups are mapped by 48 unique sequential marker IDs and §C rows.
- [x] All recognized events EV-01…EV-10 include trigger, input, processing, API/current behavior and output or blocker.
- [x] State and navigation matrices identify handoff and authorization/source gaps.
- [x] Candidate report table/migration, report ingestion, live schema, API #97 response gaps, #98 discrepancy and Study Web UNWIRED status are explicit.
- [ ] Confirm approved report writer and verify migration/live schema before claiming populated runtime queue.
- [ ] Approve #97 fields needed for count/reason/severity/reporter/time or revise the visible columns.
- [ ] Decide search, status semantics, taxonomy/sentinel mapping, pending priority, metrics, refresh cadence and report policy-card copy.
- [ ] Confirm AC-37 fine-grained permission/tenant behavior and reconcile current #98 source with its DD/AC report-detail requirement.
- [ ] Wire and verify Study Web route/client, loading/empty/ready/error mapping and AD-23 handoff.
- [x] Static asset/marker/links/checksum/tracker audit completed for this session; no application tests/runtime claimed.

**Acceptance status:** design artifact set is complete for review; `DD BLOCKED` until the unchecked contract/source decisions are resolved. `IMPLEMENTATION BLOCKED`; `RUNTIME NOT VERIFIED`.

#### Kế hoạch kiểm chứng từ source PLAN

### Trích từ DD nguồn: 5. DD authoring and static verification

1. Write `AD-22.md` sections A–F with 48 element rows and EV-01…EV-10.
2. Separate expected AC/catalog behavior, prototype behavior, current Study Server source, and unresolved assumptions.
3. Record #97's direct catalog response/errors separately from local DERIVED page/filter/order/422 details; identify missing report fields and writer/live-schema gates.
4. Record #98 ID handoff as technically type-compatible (`int64`) but report details as unavailable in current response/source. Keep #99/#100 outside this screen.
5. Create `AD-22_markers.json`, `AD-22_markers_overlay.svg`, and `screen_annotated.png` after this plan. Review annotation visually and move any marker that obscures meaningful copy.
6. Update inventory row 80 and API reverse-index row #097 from D to R, keeping #97 DD Draft and AD-22 DD blocked. Append the global progress checkpoint; do not start AD-23.
7. Static audit: sequential/unique IDs 1–48; in-bounds coordinates; coordinate agreement across JSON/SVG/DD; all A–F sections and events; relative links resolve; annotated dimensions 2560×2296; source image/HTML hashes unchanged; inventory/folders 83/83; core artifacts 75/83; `git diff --check`.

- Runtime status: `RUNTIME NOT VERIFIED` (the generated DD does not claim otherwise).
- Không chạy app test trong task chuyển đổi tài liệu.

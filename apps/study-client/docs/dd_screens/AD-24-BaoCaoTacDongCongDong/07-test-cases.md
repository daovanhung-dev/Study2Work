# AD-24 — Test Cases

> Các mã `TC` bên dưới là planning references được tạo cho file DD; chúng không phải test suite, không được chạy và không chứng minh implementation/runtime.

## 1. Coverage matrix
| Test ID | Type | Event | Rule/API | Priority |
|---|---|---|---|---|
| `AD-24-TC-001` | Planning ref / not run | `AC-38` | See source acceptance section | P2 |

## 2. Test planning references

### AD-24-TC-001 — Acceptance planning reference (AC-38)
- **Mục tiêu:** Giữ truy vết tới yêu cầu/acceptance đã ghi; đây là test planning reference, không phải test code hoặc kết quả chạy.
- **Precondition:** Đọc nguồn [AD-24](../../screen_stitch/05_admin/AD-24_bao-cao-tac-dong-cong-dong/AD-24.md) và gỡ blocker áp dụng trước khi implementation.
- **Mock/test data:** Nguồn không cung cấp fixture dùng để chạy test ở package này; không đưa dữ liệu thật.
- **Steps:**
  1. Đối chiếu acceptance và event tương ứng trong DD nguồn.
  2. Khi runtime/test implementation tồn tại, viết test riêng theo contract đã xác nhận.
- **Expected UI/state:** Theo acceptance/state trong nguồn; chưa được xác minh trên runtime.
- **Expected API/data:** Theo [API Integration](04-api-integration.md); không phát sinh request trong lần tạo tài liệu.
- **Failure / edge assertion:** Không đánh dấu pass cho `UNWIRED`, `IMPLEMENTATION BLOCKED` hoặc `RUNTIME NOT VERIFIED`.
- **References:** `AC-38`, [Events](02-events.md), [Business Rules](05-business-rules.md), [source DD](../../screen_stitch/05_admin/AD-24_bao-cao-tac-dong-cong-dong/AD-24.md).

## 3. Source acceptance / test plan (not run)

### Trích từ DD nguồn: F. Tiêu chí nghiệm thu và quyết định còn mở

### Static DD acceptance checklist

- [x] 42 numbered markers map to 42 unique element rows in §C.
- [x] Eight events distinguish prototype behavior, AC/catalog expectation and current source status.
- [x] API #101/#102 method/path/auth/query/response/catalog codes are recorded with `date` vs `string` discrepancy.
- [x] Metric-card/segment mapping, date behavior, empty/partial states and data-source gaps are explicit; no formulas are invented.
- [x] AC-38 order, optional export branch and AD-25 filter handoff are linked with #103/Operation discrepancy retained.
- [x] Original source image/HTML are preserved; annotation is separate.
- [ ] DD READY: **not met**; unresolved contract decisions affect implementability.
- [ ] IMPLEMENTATION READY: **not met**; Study Web and #101/#102 are unwired.
- [ ] RUNTIME VERIFIED: **not met**; no application tests/runtime were run.

### Blockers requiring contract decisions

1. Approve KPI keys, labels, unit, population, formula, date column, status predicates, denominator/uniqueness, ordering and empty/partial semantics for the four summary cards and chart.
2. Reconcile prototype's four planned metric cards with the displayed KPI cards and candidate #101/#102 metric sets; approve whether those text cards are explanatory requirements or static placeholders.
3. Align #101 `from/to:date` and #102 `from/to:string`; define date parsing, timezone, inclusive/exclusive boundaries, defaults, maximum period and approved invalid-range response (catalog currently declares no 400/422).
4. Define segment meaning and allowed values. Resolve screenshot `all/interns/graduates/alumni` versus #102 Draft `learning/community`; define blank/unknown/case behavior without adding unapproved values.
5. Clarify AC-38 order: it places date/report-permission validation after the #102 request; specify which layer validates before data access and how both endpoints share authorization.
6. Choose executable aggregate relations or report snapshot contract, writer/freshness and consistency requirements; verify live schema/deployment. Resolve AC-19 Comment storage versus legacy `discussions.parent_id` candidate.
7. Approve report permission, Admin claim mapping and access policy; current shared ADMIN helper capability does not secure endpoints that do not exist.
8. Specify Apply behavior, URL filter representation, reset/default period, reload/cancellation/partial-failure, network retry and cache/freshness rules.
9. Reconcile AD-24 → AD-25 filter transfer and API #103 response (`Report` vs `Operation`) with `/api/v1/operations/{operation_id}` before designing export status/download flow.
10. Implement Study Web route/client and #101/#102 backend/query/tests, then verify actual runtime separately.

Until these decisions are backed by approved contract and source, retain `DD BLOCKED`, `IMPLEMENTATION BLOCKED`, and `RUNTIME NOT VERIFIED`.

#### Kế hoạch kiểm chứng từ source PLAN

### Trích từ DD nguồn: 6. DD authoring and static verification

1. Write `AD-24.md` sections A–F with 42 element rows and EV-01…EV-08.
2. Separate expected AC/catalog flow, current static HTML behavior, Draft API-DD proposals, current server source absence, and candidate DB artifacts.
3. Explicitly show that the screenshot's four KPI cards and four proposed metric-description cards have no approved mapping to generic #101/#102 `Report.metrics[]`; leave placeholders/claims static.
4. Record #101 `date` vs #102 `string`, screen taxonomy vs Draft segment proposal, AC validation ordering, no source-backed report permission/endpoint, and AD-25 export-filter handoff gaps.
5. Create `AD-24_markers.json`, `AD-24_markers_overlay.svg`, and `screen_annotated.png` after this plan. Inspect the final image and move any marker that obscures meaningful copy.
6. Update inventory row 82 and API reverse-index #101/#102 with current evidence while retaining `D`; update the AD-24 global plan row/checkpoint. Do not edit AD-25 artifacts.
7. Static audit: IDs 1–42 sequential/unique/in-bounds and aligned across plan/JSON/SVG/DD; no marker overlap; all A–F/events present; local links resolve; JSON/SVG parse; annotation is 2704×3200; original hashes unchanged; inventory/folders remain 83/83; recalculate core artifacts; scoped `git diff --check`.

- Runtime status: `RUNTIME NOT VERIFIED` (the generated DD does not claim otherwise).
- Không chạy app test trong task chuyển đổi tài liệu.

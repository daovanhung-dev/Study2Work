# AD-24 — Business Rules

> **T041 approved-policy update (2026-11-19):** The metric keys, inclusive UTC date bounds with trailing-30-day default, and `learning|community` segment tokens are approved at high level. This supersedes blocker wording below only for those values; formulas, population, source columns, access policy and empty/partial semantics remain open.

## 1. Rule index
| Rule ID (package alias) | Tên / source ID | Áp dụng | Thực thi | Tests |
|---|---|---|---|---|
| `AD-24-BR-001` | Source rules/gates bundle (alias only) | See source DD | Not re-inferred | See source acceptance |

## 2. Rules, security, discrepancy và gate từ source
- Inventory purpose: Date range, phân khúc, KPI và biểu đồ tác động.
- Gate/status (giữ nguyên): **D**; #101/#102 catalog/Draft-only, không có Study Server route/query/model/test; Study Client route/page/Admin session gate source-wired nhưng chưa có caller. **DD BLOCKED; IMPLEMENTATION PARTIAL:** KPI formula/population/source; date type/default/validation; segment vocabulary; AC-38 validation order; report permission/live schema; AD-25 filter handoff/#103 response mismatch; report actions remain disabled; **RUNTIME NOT VERIFIED**
- BR IDs trong file này chỉ là alias trỏ tới source rule/gate bundles; không thêm business rule. Không khẳng định rule FE/BE mới khi source chưa xác nhận.

### Trích từ DD nguồn: F. Tiêu chí nghiệm thu và quyết định còn mở

### Static DD acceptance checklist

- [x] 42 numbered markers map to 42 unique element rows in §C.
- [x] Eight events distinguish prototype behavior, AC/catalog expectation and current source status.
- [x] API #101/#102 method/path/auth/query/response/catalog codes are recorded with `date` vs `string` discrepancy.
- [x] Metric-card/segment mapping, date behavior, empty/partial states and data-source gaps are explicit; no formulas are invented.
- [x] AC-38 order, optional export branch and AD-25 filter handoff are linked with #103/Operation discrepancy retained.
- [x] Original source image/HTML are preserved; annotation is separate.
- [ ] DD READY: **not met**; unresolved contract decisions affect implementability.
- [ ] IMPLEMENTATION READY: **not met**; route/page/session gate exist, but the report data flow and #101/#102 APIs are unavailable, so actions remain gated.
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
10. Complete the AD-24 report behavior and implement #101/#102 backend/query/tests under approved contracts, then verify actual runtime separately.

Until these decisions are backed by approved contract and source, retain `DD BLOCKED`, `IMPLEMENTATION BLOCKED`, and `RUNTIME NOT VERIFIED`.

## 3. Quy tắc chưa xác nhận
- `CẦN_XÁC_NHẬN`: các quyết định/blocker trong inventory và DD nguồn chưa được giải quyết.
- Related IDs/source refs: Không có BR ID nguồn được chuẩn hóa.; xem [API](04-api-integration.md), [Events](02-events.md), [Tests](07-test-cases.md).

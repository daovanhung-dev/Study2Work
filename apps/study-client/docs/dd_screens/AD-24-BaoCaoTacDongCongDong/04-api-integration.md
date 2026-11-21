# AD-24 — API Integration

> API/status dưới đây lấy từ inventory và DD nguồn. Package-local API IDs chỉ là alias truy vết cho API catalog reference; chúng không tạo contract mới. `R/S/D/M/UX` hoặc nhãn cục bộ là evidence status, không tự động xác nhận UI/runtime. Route/contract thiếu nguồn phải giữ `CẦN_XÁC_NHẬN`.

> **T041 approved-policy update (2026-11-19):** Approved metric keys are `unique_learners`, `completions`, `discussion_topics`, and `discussion_replies`; date bounds are inclusive UTC with a trailing-30-day default; accepted segment tokens are `learning` and `community`. The older Draft-only note below is superseded for these high-level choices. Metric formulas/populations/date columns, permission, concrete #101/#102 mapping, validation/error rules, and export filter serialization remain open. The Study Client page/route exists, but no report API caller or Study Server #101/#102 route/query/model/test source exists locally.

## 1. API usage matrix
| API ID (package-local usage alias) | Source catalog ref | Method/path | Event | Auth |
|---|---|---|---|---|
| `AD-24-API-001` | #101 | See source contract excerpt | Source event IDs are preserved in [Events](02-events.md) | See source auth/permission evidence |
| `AD-24-API-002` | #102 | See source contract excerpt | Source event IDs are preserved in [Events](02-events.md) | See source auth/permission evidence |

## 2. Contract / source detail

- API refs trong inventory: #101, #102
- Orchestration/data notes: GET #101 tổng quan, GET #102 theo from/to/segment; giữ filter URL cho export.
- BE/source status và gate: **D**; #101/#102 catalog/Draft-only, không có Study Server route/query/model/test; Study Client route/page/Admin session gate source-wired, không có caller. **DD BLOCKED; IMPLEMENTATION PARTIAL:** KPI formula/population/source; date type/default/validation; segment vocabulary; AC-38 validation order; report permission/live schema; AD-25 filter handoff/#103 response mismatch; report actions disabled; **RUNTIME NOT VERIFIED**
- Contract sources and discrepancies are preserved in the source excerpts below.

### Trích từ DD nguồn: Blockers requiring contract decisions

1. Approve KPI keys, labels, unit, population, formula, date column, status predicates, denominator/uniqueness, ordering and empty/partial semantics for the four summary cards and chart.
2. Reconcile prototype's four planned metric cards with the displayed KPI cards and candidate #101/#102 metric sets; approve whether those text cards are explanatory requirements or static placeholders.
3. Align #101 `from/to:date` and #102 `from/to:string`; define date parsing, timezone, inclusive/exclusive boundaries, defaults, maximum period and approved invalid-range response (catalog currently declares no 400/422).
4. Define segment meaning and allowed values. Resolve screenshot `all/interns/graduates/alumni` versus #102 Draft `learning/community`; define blank/unknown/case behavior without adding unapproved values.
5. Clarify AC-38 order: it places date/report-permission validation after the #102 request; specify which layer validates before data access and how both endpoints share authorization.
6. Choose executable aggregate relations or report snapshot contract, writer/freshness and consistency requirements; verify live schema/deployment. Resolve AC-19 Comment storage versus legacy `discussions.parent_id` candidate.
7. Approve report permission, Admin claim mapping and access policy; current shared ADMIN helper capability does not secure endpoints that do not exist.
8. Specify Apply behavior, URL filter representation, reset/default period, reload/cancellation/partial-failure, network retry and cache/freshness rules.
9. Reconcile AD-24 → AD-25 filter transfer and API #103 response (`Report` vs `Operation`) with `/api/v1/operations/{operation_id}` before designing export status/download flow.
10. Complete the gated AD-24 report behavior and implement #101/#102 backend/query/tests under approved contracts, then verify actual runtime separately.

Until these decisions are backed by approved contract and source, retain `DD BLOCKED`, `IMPLEMENTATION BLOCKED`, and `RUNTIME NOT VERIFIED`.

## 3. API không sử dụng
- Không bổ sung API ngoài inventory và DD nguồn. Nếu screen không cần API, trạng thái phải được xác nhận từ source DD.

## 4. References
[Events](02-events.md) · [Data flow](03-data-flow.md) · [Tests](07-test-cases.md) · [Source DD](../../screen_stitch/05_admin/AD-24_bao-cao-tac-dong-cong-dong/AD-24.md)

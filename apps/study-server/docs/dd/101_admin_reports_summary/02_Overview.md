---
title: "Overview"
order: 2
dd_id: "101"
api_name: "Lấy KPI tổng quan"
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "Overview"
format: markdown
status: "Draft — Needs Confirmation"
---

# Overview

## Khái quát

| Thuộc tính | Giá trị |
|---|---|
| API ID | #101 |
| Module | ADMIN / SYSTEM MANAGEMENT — AC-38 |
| Method | GET |
| Endpoint | `/api/v1/admin/reports/summary` |
| Purpose | Tổng hợp KPI để Admin xem Dashboard báo cáo. |
| Consumer/Actor | Admin |
| Authentication | Bearer JWT |
| Authorization | Role Admin theo catalog; quyền/claim chưa có trong Study source. |
| Direct query | `from?:date`, `to?:date`; không body. |
| Direct response | HTTP 200 `ApiEnvelope<Report>`. |
| Direct errors | 401 `DESIGN_AUTHENTICATION_REQUIRED`; 403 `DESIGN_ACCESS_DENIED`; 500 `DESIGN_INTERNAL_ERROR`. |
| AC-38 position | Mở dashboard → #101 aggregate KPI summary → #102 community impact → optional #103 export. |
| Runtime state | `UNWIRED / NOT_FOUND`; không có route/module/query/test #101. |
| Side effects | Read-only; không ghi report snapshot trong API DD này. |
| Transaction | Không có write; read isolation/consistency giữa metric queries chưa được chỉ định. |

## Sources

- [API catalog và reusable schemas](../../../../../docs/lists/list_api.md) — row #101, `ApiEnvelope`, `Report`, `DateRange`, `ImpactMetric`.
- [AC/API index, AC-38](../../diagrams/AC_UNICA/00_AC_API_INDEX.md) — actor, precondition, postcondition và API #101–#103.
- [AC-38 activity diagram](../../diagrams/AC_UNICA/AC_04_ADMIN_MANAGEMENT.drawio) — #101 aggregate KPI summary → #102 validate/aggregate learning-community metrics → optional #103 export.
- [DB table guide](../../diagrams/DB_UNICA_TABLES.md), [legacy Study DDL](../../../../../infra/postgres/study-server/DB.sql) — candidate timestamps trên users/courses/enrollments/discussions; không chứng minh live schema.
- [V1-PILOT DDL](../../../../../infra/postgres/02_study_db.sql) — `report_snapshots` design candidate; không chứng minh live schema hoặc API wiring.
- [API #91 quiz statistics](../91_admin_quizzes_statistics/00_Cover.md) và [API #66 mentor analytics](../66_mentor_course_analytics/00_Cover.md) — precedent về metric gaps; metric definitions không được tái sử dụng cho #101.
- [Current router](../../../app/api/v1.py), [auth helper](../../../app/utils/auth.py), [middleware](../../../app/core/middleware.py), [response helper](../../../app/core/responses.py) — current route/auth/error boundary.
- [API guidelines](../../../../../contracts/api-guidelines/README.md) — common envelope/date-time convention.

## Tables read

| Relation/source | Purpose | Basis/status |
|---|---|---|
| Legacy `users` | Candidate count registrations by `created_at` | DDL candidate; population/role inclusion DERIVED; live schema unverified. |
| Legacy `courses` | Candidate count course rows by `created_at` | DDL candidate; status inclusion DERIVED; live schema unverified. |
| Legacy `enrollments` | Candidate count records by `enrolled_at` | DDL candidate; status/duplicate semantics DERIVED; live schema unverified. |
| Legacy `discussions` | Candidate count discussion rows by `created_at` | DDL candidate; includes topic/reply unless approved otherwise; live schema unverified. |
| Pilot `report_snapshots` | Alternative precomputed report source | Immutable UUID snapshot model; `report_code`, period and JSON mapping to API #101 are SOURCE_REQUIRED. Not selected. |

## Tables write

N/A — API #101 is read-only. No `report_snapshots` insert/cache write is specified by catalog or AC-38.

## Mục chú ý

- `Report` directly requires `period:{from,to}`, `metrics[]`, and `generated_at`; catalog does not define metric keys, labels, formulas, units, or empty-result behavior.
- Query dates are optional, while the response `DateRange` requires both dates. The rolling 30-day completion rule in this draft is only a `DERIVED` proposal.
- The four proposed metrics count rows, not unique people/courses or status-based active entities.
- Catalog API #102 uses `from?:string`, `to?:string`, `segment?:string`, unlike #101 date fields. API #103 row returns `Report`, while the catalog Operation-tracking paragraph says export returns `Operation`; keep this group discrepancy for review after #103 DD.
- `report_snapshots` stores JSONB and uses a UUID key in the pilot schema; no approved report code or metrics JSON mapping exists.

## Assumptions

- MVP proposal: count user, course, enrollment and discussion records created in the effective date window with four independent count queries; no status/role/root filters.
- An empty source count is represented by value `"0"`; metric list remains the same four proposed keys.
- `generated_at` is the report assembly time in UTC.
- All assumptions are `DERIVED`; none is runtime behavior or an approved business rule.

## Conflicts

| Conflict | Expected behavior | Current/source evidence | Status |
|---|---|---|---|
| KPI set | AC-38 asks for summary | No metric list/formulas in diagram/catalog | `SOURCE_REQUIRED`; count set is DERIVED |
| Date period | Response requires both dates | Both query bounds are optional | `DISCREPANCY / DERIVED` |
| Persistence | Summary must be assembled | Legacy has no report table; pilot snapshot has no API/report-code mapping | `DISCREPANCY / SOURCE_REQUIRED` |
| Admin access | Catalog requires Admin | Current Study shared guard validates Student | `DISCREPANCY / SOURCE_REQUIRED` |
| AC-38 response integration | #103 export | Endpoint row says Report; operation note says Operation | `GROUP_REVIEW_PENDING` |

## Security note

Authorize Admin/report permission before reading aggregate data. Current Study source has no Admin guard/claim policy; do not claim this endpoint is secured at runtime.

## Performance note

Independent `COUNT` queries avoid row multiplication from cross-domain joins. Their execution strategy, consistency snapshot, indexes, caching and maximum date range are not established by evidence.
---
## Phụ lục đối chiếu nguồn Excel
- Workbook nguồn: `DD_API_Template(1).xlsx`
- Sheet nguồn: `Overview`
- Dimension: `A1:BA10`
- Trạng thái: `visible`
- Số ô có dữ liệu/công thức: `4`
- Số vùng merge: `0`

<details>
<summary>Bản ghi từng ô có dữ liệu hoặc công thức</summary>

| Hàng | Ô | Giá trị nguồn | Công thức nguồn |
|---:|---|---|---|
| 1 | `A1` | 【Khái quát】 |  |
| 3 | `B3` | Get thông tin…. |  |
| 5 | `A5` | 【Mục chú ý】 |  |
| 7 | `B7` | Không có |  |

</details>

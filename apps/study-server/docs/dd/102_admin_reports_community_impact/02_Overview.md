---
title: "Overview"
order: 2
dd_id: "102"
api_name: "Lấy dữ liệu tác động cộng đồng"
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "Overview"
format: markdown
status: "Draft — Needs Confirmation"
---

# Overview

## Khái quát

| Thuộc tính | Giá trị |
|---|---|
| API ID | #102 |
| Module | ADMIN / SYSTEM MANAGEMENT — AC-38 |
| Method | GET |
| Endpoint | `/api/v1/admin/reports/community-impact` |
| Purpose | Tổng hợp metric học tập/cộng đồng cho dashboard báo cáo, lọc theo kỳ và segment tùy chọn. |
| Consumer/Actor | Admin |
| Authentication | Bearer JWT |
| Authorization | Admin có quyền xem report/analytics theo catalog và AC-38; guard/claim hiện chưa có trong Study source. |
| Direct query | `from?:string`, `to?:string`, `segment?:string`; không body. |
| Direct response | HTTP 200 `ApiEnvelope<Report>`. |
| Direct errors | 401 `DESIGN_AUTHENTICATION_REQUIRED`; 403 `DESIGN_ACCESS_DENIED`; 500 `DESIGN_INTERNAL_ERROR`. |
| AC-38 position | #101 KPI summary → #102 validate date range/quyền, aggregate metric và render/filter dashboard → optional #103 export. |
| Runtime state | `UNWIRED / NOT_FOUND`; không có route/module/query/test #102. |
| Side effects | Read-only; không tạo snapshot hoặc mutation theo catalog/diagram. |
| Transaction | Không có write; consistency giữa các aggregate query chưa được chỉ định. |

## Sources

- [API catalog và reusable schemas](../../../../../docs/lists/list_api.md) — row #102, `ApiEnvelope`, `Report`, `DateRange`, `ImpactMetric`.
- [AC/API index, AC-38](../../diagrams/AC_UNICA/00_AC_API_INDEX.md) — Admin precondition, report postcondition và API #101–#103/operations.
- [AC-38 activity diagram](../../diagrams/AC_UNICA/AC_04_ADMIN_MANAGEMENT.drawio) — thứ tự summary → validate range/permission → aggregate learning/community metrics → dashboard/filter → optional export/view-only.
- [AC-18 activity diagram](../../diagrams/AC_UNICA/AC_02_STUDENT_LEARNING.drawio) — progress dashboard aggregate lesson/quiz/assignment state; không định nghĩa report metric/API #102.
- [AC-19 activity diagram](../../diagrams/AC_UNICA/AC_02_STUDENT_LEARNING.drawio) — topic/comment flow; diagram mô tả insert Comment riêng.
- [DB ERD](../../diagrams/DB_UNICA_ERD.drawio), [table guide](../../diagrams/DB_UNICA_TABLES.md) — legacy `enrollments`, `lesson_progress`, self-referential `discussions`; design evidence, không phải live schema.
- [Legacy Study DDL](../../../../../infra/postgres/study-server/DB.sql) — `enrollments.enrolled_at/completed_at`; `discussions.parent_id/created_at`; nullable/status details.
- [V1-PILOT Study DDL](../../../../../infra/postgres/02_study_db.sql) — UUID `course_enrollments`/progress facts and `report_snapshots`; separate model, no #102 mapping.
- [API #101 overview](../101_admin_reports_summary/02_Overview.md), [data mapping](../101_admin_reports_summary/05_Data_Mapping.md), [open questions](../101_admin_reports_summary/OPEN_QUESTIONS.md) — preceding summary, shared date proposal and unresolved metric semantics.
- [API #66 analytics](../66_mentor_course_analytics/02_Overview.md) — progress state is not an event ledger; do not reuse its missing-event assumptions as #102 query source.
- [Current router](../../../app/api/v1.py), [auth helper](../../../app/utils/auth.py), [middleware](../../../app/core/middleware.py), [response helper](../../../app/core/responses.py) — current route/auth/error boundary.
- [API guidelines](../../../../../contracts/api-guidelines/README.md) — common envelope, error `data:null`, trace convention.

## Tables read

| Relation/source | Purpose | Basis/status |
|---|---|---|
| Legacy `enrollments` | Candidate distinct learner and completion counts | `user_id`, `enrolled_at`, `completed_at`; DDL candidate, live schema unverified. |
| Legacy `discussions` | Candidate root topic/reply counts | `parent_id`, `created_at`; root/reply split is DERIVED; status/visibility policy unresolved. |
| Pilot `report_snapshots` | Alternative precomputed source | No approved report code, segment dimensions or JSON mapping for #102; not selected. |
| `lesson_progress` / quiz / assignment state | Not selected as event-history query | AC-18 is a learner progress flow; API #66 records no approved event ledger. |

## Tables write

N/A — API #102 is read-only; no snapshot INSERT or other mutation is specified.

## Mục chú ý

- Reusable `Report` requires `period:{from,to}`, `metrics[]` and `generated_at`; it does not define metric names/formulas or segment representation.
- #102 accepts date bounds as strings, unlike #101's `date` query types. This draft proposes ISO calendar-date parsing and reuses #101's date-window proposal for continuity; neither is approved.
- `segment=learning`/`community` is a simple `DERIVED` grouping proposal; output contains only the selected `ImpactMetric[]` and adds no response field.
- Metric proposal counts enrollment/completion records and root/reply discussion rows. It does not claim all learning events or unique community people beyond distinct enrollment `user_id`.
- AC-19's Comment storage does not match legacy self-referential discussion rows. The candidate reply mapping is not proof of runtime persistence.
- Unknown segment/date error mapping, Admin claims, status visibility and snapshot freshness remain open. Do not add error code or assume pilot DDL is live.
- AC-38 #103 row declares `ApiEnvelope<Report>`/202, while operation tracking says `Operation`; retain that group conflict for macro-review after #103.

## Assumptions

- If segment is omitted, return all four proposed metrics; `learning` selects the first two and `community` the last two. Allowed values/unknown-value behavior require confirmation.
- `unique_enrolled_learners` counts distinct non-null `user_id` values for enrollments whose `enrolled_at` is in period.
- `course_completions` counts enrollment rows whose `completed_at` is in period; it is not deduplicated by user/course and does not infer a status enum.
- Root/reply discussion counts use `parent_id IS NULL`/`IS NOT NULL`; no status filter is proposed, so moderated/deleted visibility semantics remain open.
- Counts serialize as decimal strings and zero as `"0"`; `generated_at` is report assembly time in UTC.
- Same 30-calendar-day default/effective-window proposal as #101 is used for coherent report period; all items above are `DERIVED`, not runtime behavior.

## Conflicts

| Conflict | Expected behavior | Current/source evidence | Status |
|---|---|---|---|
| Metric contract | AC-38 says aggregate learning/community metrics | No metric keys/formulas in catalog or diagram | `SOURCE_REQUIRED`; four counts are DERIVED |
| Query dates | #102 takes optional strings; Report requires date range | #101 takes optional `date`; parser/defaults absent | `DISCREPANCY / DERIVED` |
| Segment | Optional string filter | No allowed values or `ImpactMetric.segment` field | `SOURCE_REQUIRED / DERIVED` |
| Comment persistence | AC-19 says insert Comment | Legacy DDL/ERD model topic/reply through `discussions.parent_id` | `DISCREPANCY` |
| Authorization | Catalog/AC requires Admin/report permission | Current shared helper is Student-only | `DISCREPANCY / SOURCE_REQUIRED` |
| Snapshot | Pilot report snapshot available in DDL | No #102 code/dimension/writer/API mapping; live status unverified | `SOURCE_REQUIRED` |
| AC-38 export response | #103 endpoint row says Report; operation tracking says Operation | Two source sections disagree | `GROUP_REVIEW_PENDING` |

## Security note

Require Admin/report authorization before reading aggregate data. Candidate output contains aggregate values only; do not select discussion content, email, or user-identifying rows for response.

## Performance note

The four candidates use independent count queries with no cross-domain join, avoiding fan-out. Indexes, maximum date span, caching and consistent-read behavior are not established by source evidence.
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

---
task_id: "2026-10-24-create-study-api102-dd"
date: "2026-10-24"
primary_task_type: "docs"
secondary_task_types: []
project_scopes: ["server-study"]
cross_scope_dependencies: []
status: "VERIFIED"
---

# Worklog: Tạo DD Study API #102 — Lấy dữ liệu tác động cộng đồng

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `deno run --allow-read --allow-env scripts/select-worklogs.mjs --type docs --limit 3`
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-10-24/create-study-api100-dd.md`
    - carry_forward: Giữ catalog contract riêng với `DERIVED`; lưu plan trước folder; source route+matching view không đồng nghĩa runtime; nhóm AC chỉ macro-review khi đủ API.
  - path: `.agents/worklog/2026-10-24/create-study-api101-dd.md`
    - carry_forward: #101 là bước KPI tổng quan trước #102; `Report` shape không xác định metric semantics; cùng AC-38 có query date type khác nhau và #103 operation/Report conflict; date default của #101 chỉ là proposal.
  - path: `.agents/worklog/2026-10-24/create-study-api48-dd.md`
    - carry_forward: 8 sheets + 3 reports Markdown-only; dùng `DIRECT`, `DERIVED`, `SOURCE_REQUIRED`; không coi legacy/pilot DDL là live schema; giữ ma trận request/query/mutation/response.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Tiếp tục một API DD mỗi phiên; tạo DD tiếng Việt #102 sau khi ghi plan; đọc diagram AC-38 và các flow learning/community liên quan; kiểm tra DD ngay sau authoring. Macro-review liên kết AC-38 #101–#103 sau khi DD #103 hoàn tất.
- Canonical sources: `docs/lists/list_api.md` row #102 and reusable `ApiEnvelope`, `Report`, `DateRange`, `ImpactMetric`; AC-38 trong `00_AC_API_INDEX.md` và `AC38` page của `AC_04_ADMIN_MANAGEMENT.drawio`; AC-18/AC-19 diagrams; registered `createDD-markdown` templates; server-study Markdown-only workflow.
- Direct contract: `GET /api/v1/admin/reports/community-impact`; Bearer JWT, role Admin; query `from?:string`, `to?:string`, `segment?:string`; không body/path; `ApiEnvelope<Report>`; HTTP 200 `DESIGN_RESOURCE_RETRIEVED`; errors đúng 401 `DESIGN_AUTHENTICATION_REQUIRED`, 403 `DESIGN_ACCESS_DENIED`, 500 `DESIGN_INTERNAL_ERROR`.
- Direct reusable `Report`: `period:DateRange`, `metrics:ImpactMetric[]`, `generated_at:date-time`; `DateRange={from:date,to:date}`; `ImpactMetric={key:string,value:decimal-string,label:string}`.
- AC-38 step: #101 KPI summary → #102 validate date range + report permission → aggregate learning/community metrics → render dashboard/filter → optional #103 export or view-only end.

## CURRENT_BEHAVIOR

- Baseline: 103 unique catalog IDs; 101 DD folders (#01–#101), all with 8 core sheet roles; 89 have 3 standard reports; #102–#103 are absent. Route marker plus matching Study module `view.py` still covers #01–#09 and #12–#14 (12); 91 IDs have no pair.
- Runtime/source: no #102 route, module, query, handler, or focused test under `apps/study-server`; `UNWIRED / NOT_FOUND`.
- Auth: current `app/utils/auth.py` validates Study access claims but exposes only a Student guard; no Admin/report permission guard is present in the reviewed source. Catalog/AC requirement remains expected behavior, not current wiring.
- Legacy DDL candidate: `enrollments` has `user_id`, `status`, `enrolled_at`, nullable `completed_at`; `discussions` has `parent_id`, `status`, `created_at`. DB guide describes `parent_id IS NULL` as root topic and non-NULL as reply. These are legacy design artifacts, not live-schema proof.
- Diagram/schema discrepancy: AC-19 depicts `INSERT Comment`, while legacy DDL/ERD represent discussion/replies as a self-referential `discussions` table and contain no separate comment table. Proposed reply counts use that legacy candidate only and remain `DERIVED`.
- Pilot schema: V1-PILOT uses UUID course-enrollment/progress entities and `report_snapshots`; it is a separate design model with no #102 report/segment mapping. Do not mix it with legacy BIGINT IDs/timestamps or call it live.
- Runnable tests: no focused #102 test; docs-only, application tests not planned/run.

## SOURCE_TRACE

```text
Admin Bearer principal -> GET /admin/reports/community-impact?from&to&segment -> validate permission and date range -> normalize effective period and optional segment -> aggregate candidate enrollment/completion and topic/reply counts -> map Report(period, metrics, generated_at) -> 200 DESIGN_RESOURCE_RETRIEVED or catalog 401/403/500 -> dashboard filter, then optional #103 export
```

## PLAN BEFORE DD AUTHORING

1. Preserve exact #102 catalog method/path, Admin Bearer, optional string query fields `from`, `to`, `segment`, no body/path, `ApiEnvelope<Report>`, HTTP 200 and exactly 401/403/500 codes. Do not import #103 `filters`/`format` or add 400/422.
2. Parse AC-38 node/edge flow and retain the distinct logical boundary: #101 summary; #102 range/permission validation and learning/community metrics; #103 optional export. Read AC-18 progress and AC-19 topic/reply diagrams, DB ERD/table guide and legacy/pilot DDL. Keep AC-19 comment-vs-discussions storage discrepancy explicit.
3. Keep direct `Report` schema; no new response field. `period`, each `ImpactMetric` member, `generated_at`, envelope fields and exact errors get separate rows.
4. Propose a simple four-metric MVP, all marked `DERIVED`, using legacy candidates only: (a) `unique_enrolled_learners` = distinct non-null `enrollments.user_id` in period by `enrolled_at`; (b) `course_completions` = enrollment rows with `completed_at` in period; (c) `discussion_topics_created` = `discussions` rows with null `parent_id` and `created_at` in period; (d) `discussion_replies_created` = rows with non-null `parent_id` and `created_at` in period. Do not read text/PII; do not filter `status` because the complete enum/visibility rule is not specified. Record hidden/deleted population as an open question.
5. Propose `segment` values `learning` (first two metrics), `community` (last two), omitted (all four) as `DERIVED`; output remains `ImpactMetric[]`, with no segment property added. Empty/unknown segment behavior and any other dimension values remain unresolved; do not invent a 422 response.
6. For date coherence with #101, propose ISO `YYYY-MM-DD` parsing from the direct string values and the same effective range: both supplied → inclusive bounds; neither → rolling 30 calendar days through today; only `from` → through today; only `to` → 30 calendar days ending at `to`. `from > to`, invalid date mapping, timestamp boundary/timezone and range maximum remain `SOURCE_REQUIRED`; diagram says validate but catalog exposes no 400/422.
7. Keep candidate `generated_at` as report assembly time in UTC and `COUNT` values as decimal strings; zero counts as `"0"`. These are `DERIVED`, not approved runtime behavior.
8. Do not use `lesson_progress`/quiz/assignment state as learning-event history; API #66 and AC-18 distinguish progress state from event analytics, and no event ledger is approved. Do not select pilot `report_snapshots` without #102 report code, dimensions/segment JSON contract, writer and live-schema evidence.
9. Build all four matrices before folder authoring: Request Usage, Query, Mutation (read-only/N/A), Response Source. Candidate queries must list each selected field/predicate; no joins are needed for these four counts.
10. Only after this plan is saved, create `apps/study-server/docs/dd/102_admin_reports_community_impact/` with 8 registered sheets and 3 reports. Markdown-only; no runtime, DB, catalog, diagram or client changes.
11. Immediately validate exact 11-file manifest, front matter, all 8 template suffixes, exact catalog/error set, Report fields, metric/request/query matrix coverage, valid JSON, local links/anchors, table widths, fences, whitespace, fingerprints and `git diff --check`.
12. Update this worklog and inventory after checks. Leave AC-38 group macro-review pending until #103 DD exists; do not resolve the #103 Report-versus-Operation discrepancy in this DD.

### API Requirement Matrix

| API ID | Contract item | Value | Basis/status |
|---|---|---|---|
| #102 | Method/path | `GET /api/v1/admin/reports/community-impact` | Catalog + AC-38; DIRECT |
| #102 | Actor/auth | Admin; Bearer JWT; report/analytics permission | Catalog + AC-38; DIRECT; Admin policy SOURCE_REQUIRED |
| #102 | Query | `from?:string`, `to?:string`, `segment?:string` | Catalog; DIRECT types; date/segment semantics DERIVED |
| #102 | Body/path | None | Catalog; DIRECT |
| #102 | Success | 200 `DESIGN_RESOURCE_RETRIEVED`; `ApiEnvelope<Report>` | Catalog; DIRECT |
| #102 | Report shape | `period`, `metrics[]`, `generated_at` | Reusable schema; DIRECT shape; semantics incomplete |
| #102 | Errors | 401 authentication, 403 access denied, 500 internal | Catalog; DIRECT exact codes |
| #102 | Logical effect | Validate date range + permission; aggregate learning/community metrics | AC-38; DIRECT logical flow; metric definitions DERIVED |

### Request Usage Matrix

| Request item | Source/use | Mapping use | Rule/status |
|---|---|---|---|
| `Authorization` | Bearer JWT | Authenticate Admin and authorize analytics before aggregation | DIRECT; current Admin guard SOURCE_REQUIRED |
| `from` | Optional string query | Lower bound for all candidate queries | DIRECT field; ISO date parsing/default DERIVED |
| `to` | Optional string query | Upper bound for all candidate queries | DIRECT field; ISO date parsing/default DERIVED |
| `segment` | Optional string query | Select learning/community metric subset | DIRECT field; allowed values/behavior DERIVED/SOURCE_REQUIRED |
| Body/path | None | None | DIRECT |

### Query Matrix

| Query | Purpose | Candidate source/columns | Predicate/result | Status |
|---|---|---|---|---|
| Q1 | Distinct learners enrolled | legacy `enrollments.user_id`, `enrolled_at` | `COUNT(DISTINCT user_id)` for period; ignore null user IDs | DERIVED; legacy/live gap |
| Q2 | Course completion records | legacy `enrollments.completed_at` | Count non-null completion timestamps in period | DERIVED; completion/status semantics need confirmation |
| Q3 | Root community topics | legacy `discussions.parent_id`, `created_at` | `parent_id IS NULL` and created in period | DERIVED; AC-19 storage discrepancy |
| Q4 | Community replies | legacy `discussions.parent_id`, `created_at` | `parent_id IS NOT NULL` and created in period | DERIVED; AC-19 storage discrepancy |

### Mutation Matrix

| Mutation ID | Operation | Target | Fields | Status |
|---|---|---|---|---|
| — | None | N/A | API #102 is read-only; no INSERT/UPDATE/DELETE | N/A — READ-ONLY API |

### Response Source Matrix

| Response field | Type | Candidate source/transform | Status |
|---|---|---|---|
| `success` | boolean | Envelope | Shared convention |
| `businessCode` | string | `DESIGN_RESOURCE_RETRIEVED` | DIRECT catalog |
| `message` | string | Safe application text | Exact literal unspecified |
| `data.period.from/to` | date | Effective parsed range | DIRECT schema; normalization/default DERIVED |
| `data.metrics[]` | `ImpactMetric[]` | Metric set selected by `segment` | DIRECT collection; keys/formulas DERIVED |
| `data.metrics[].key` | string | Four proposed stable keys | DIRECT type; values DERIVED |
| `data.metrics[].value` | decimal-string | COUNT result | DIRECT type; formula DERIVED; zero-as-`"0"` proposal |
| `data.metrics[].label` | string | Vietnamese metric label | DIRECT type; text DERIVED |
| `data.generated_at` | date-time | Report assembly clock | DIRECT type; UTC proposal |
| `meta` | object | Envelope | Endpoint fields unspecified |
| `traceId` | uuid | Request trace | Shared API guideline |

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| API #102 runtime | No router/module/test | `UNWIRED / NOT_FOUND` | Design-only; no runtime claim |
| String dates vs `DateRange` | Catalog input is `string`; reusable response uses `date` | `DIRECT / DERIVED` | Date parsing and invalid input mapping need review |
| Segment semantics | Query is optional `string`; no values/enum or response segment field | `SOURCE_REQUIRED / DERIVED` | Proposal uses `learning` and `community`; unknown values unresolved |
| Learning source | Legacy enrollment timestamps are candidates; no metric definitions approved | `DERIVED / SOURCE_REQUIRED` | Counts do not claim full learner-event history |
| Community storage | AC-19 says Comment insert; legacy ERD/DDL use self-referential `discussions` | `DISCREPANCY` | Root/reply counts are legacy-only proposal |
| Admin access | Catalog/AC require Admin/report permission; current guard is Student-only | `DISCREPANCY / SOURCE_REQUIRED` | No runtime Admin authorization proof |
| AC-38 response tracking | #103 catalog row says Report while operation tracking says Operation | `GROUP_REVIEW_PENDING` | Leave for macro-review after #103 |

## CHANGES

- Files changed: this plan-first worklog, API #102 Markdown DD package, and inventory worklog recheck; corrected the template fingerprint label in the immediate prior #101 report/worklog after recomputation.
- CONTEXT_UPDATES: None planned; no runtime/schema/catalog/diagram/context-page change.
- Assumptions: Metric formulas, segment vocabulary, date parsing/default, zero behavior and UTC generation time are `DERIVED` proposals; not runtime behavior or approved business rules.

## VERIFICATION

| Check | Result | Status |
|---|---|---|
| Classification/preflight | `docs`, `server-study`, no cross-scope; selector returned #100/#101/#48 and all were read. | VERIFIED |
| Context/skill registry | Server scope and `createDD-markdown` are wired; Study workflow requires Markdown-only output. | VERIFIED_STATIC_ONLY |
| AC diagrams | AC-38, AC-18, AC-19 and DB ERD/table guide reviewed; relevant nodes/edges and schema gap recorded. | VERIFIED_STATIC_ONLY |
| Catalog/schema candidates | #102 exact row, Report/DateRange/ImpactMetric fields and legacy/pilot distinction reviewed. | VERIFIED_STATIC_ONLY |
| Current source | No #102 route/module/query/test; current shared helper only checks Student. | VERIFIED_STATIC_ONLY |
| Pre-authoring inventory | 101 DD folders, 89 full 11-file packs, 2 absent (#102–#103), 12 source route+view pairs. | VERIFIED_STATIC_ONLY |
| DD package and static checks | 11/11 files; 8/8 front matters and template suffixes; exact contract/error set; 3 JSON examples; 23 local links, 0 anchors; 523 table rows; 5 fence pairs; whitespace and `git diff --check` pass. | VERIFIED_STATIC_ONLY |

## HANDOFF

- Remaining blockers: Metric/segment approval, invalid date mapping, timestamp timezone, completion meaning, moderated/deleted content inclusion, Admin permission policy, and separate Comment-vs-Discussion physical mapping.
- Next action: Create API #103 DD; perform AC-38 macro-review after #103 is complete.


## POSTFLIGHT — API #102 DD — 2026-10-24

- DD package: `apps/study-server/docs/dd/102_admin_reports_community_impact/` contains exactly 11 Markdown files (8 sheets + 3 reports); all 8 front matters and registered template appendix suffixes pass.
- Static validation: exact #102 method/path/query/response/error set retained; three JSON examples parse; 23 local links resolve with no anchors; 523 table rows are width-consistent; five code-fence pairs balance; final newlines and whitespace pass; `git diff --check` has no diagnostics.
- Fingerprints: template `3dc7fd2242dd1ed1bd9faba50aadad913a31b97ebf1392d6144bb905c5208137`; output `0dc8424254b7b7c0a250a4555388203c86e313f045d4226859c87640d2c50b9b`.
- Inventory after #102: catalog 103; 102 numbered DD folders all have the 8 core sheets; 90 have the full 11-file package; the 12 legacy folders #01–#12 lack standard reports; only #103 lacks a DD.
- Source inventory: route marker plus matching module `view.py` exists for #01–#09 and #12–#14 (12); 91 catalog IDs have no route+view pair. This is source/wiring evidence, not runtime verification. No application tests were run.
- API #102 remains `UNWIRED / NOT_FOUND`; AC-38 macro-review #101–#103 remains pending until #103 DD is present.
- Scope: Markdown and worklogs only; no runtime, tests, DB schema, catalog, diagram or context page changed.

## POSTFLIGHT ADDENDUM — AC-38 macro-review after API #103 — 2026-10-24

- Macro-review completed for #101–#103 and polling boundary API #18. Flow continuity is #101 summary → #102 community dashboard/filter → optional #103 export/view-only.
- Retained discrepancies: #101 date queries use `date` while #102 uses `string`; #103 row payload is `Report` while Operation tracking says `Operation`; API #18 has int64/UUID ID, owner/Admin policy, `Payment`/ExportAsset result and missing Study persistence/lifecycle decisions.
- Diagram formats CSV/XLSX/PDF and conditional temporary file storage are documented; defaults, filters, queue/storage mapping, download/expiry, retry and worker error rules remain open. #101–#103 remain `UNWIRED / NOT_FOUND`; no application tests were run.
- Updated connected DD plan/open-question/verification reports. No catalog, schema, diagram, runtime source or client changes.

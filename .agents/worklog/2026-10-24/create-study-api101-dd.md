---
task_id: "2026-10-24-create-study-api101-dd"
date: "2026-10-24"
primary_task_type: "docs"
secondary_task_types: []
project_scopes: ["server-study"]
cross_scope_dependencies: []
status: "VERIFIED"
---

# Worklog: Tạo DD Study API #101 — Lấy KPI tổng quan

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `deno run --allow-read --allow-env scripts/select-worklogs.mjs --type docs --limit 3`
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-10-24/create-study-api100-dd.md`
    - carry_forward: Lập plan trước folder; giữ direct contract riêng với candidate `DERIVED`; macro-review AC chỉ hoàn tất sau khi đủ API trong nhóm.
  - path: `.agents/worklog/2026-10-24/create-study-api48-dd.md`
    - carry_forward: Dùng 8 template sheet + 3 reports Markdown-only; không coi DDL candidate/live schema là một; giữ field chưa có nguồn là `SOURCE_REQUIRED`.
  - path: `.agents/worklog/2026-10-24/create-study-api49-dd.md`
    - carry_forward: Giữ expected/current tách biệt, dùng đủ bốn ma trận; metric đề xuất phải ghi `DERIVED` và không lấy current-state progress thay event history.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Tiếp tục chuỗi một API DD mỗi phiên; tạo DD tiếng Việt cho API #101, lập plan trước khi tạo folder, review ngay sau authoring. AC-38 có #101–#103; macro-review cả nhóm để sau khi đủ #103.
- Canonical sources: `docs/lists/list_api.md` row #101 và reusable `ApiEnvelope`, `Report`, `DateRange`, `ImpactMetric`; AC-38 trong `00_AC_API_INDEX.md` và page AC38 của `AC_04_ADMIN_MANAGEMENT.drawio`; registered `createDD-markdown` skill/template; server-study Markdown-only workflow.
- Direct contract: `GET /api/v1/admin/reports/summary`; Bearer JWT, role Admin; query `from?:date`, `to?:date`; không body; response `ApiEnvelope<Report>`; HTTP 200 `DESIGN_RESOURCE_RETRIEVED`; errors đúng 401 `DESIGN_AUTHENTICATION_REQUIRED`, 403 `DESIGN_ACCESS_DENIED`, 500 `DESIGN_INTERNAL_ERROR`.
- Direct `Report`: `period:DateRange`, `metrics:ImpactMetric[]`, `generated_at:date-time`; `DateRange={from:date,to:date}`; `ImpactMetric={key:string,value:decimal-string,label:string}`.
- AC-38 logical step: Dashboard → #101 aggregate KPI summary → #102 community impact → optional #103 export.

## CURRENT_BEHAVIOR

- Baseline: catalog có 103 unique API ID; 100 numbered DD folders (#01–#100), cả 100 có 8 sheet lõi; 88 có 3 report chuẩn; #101–#103 chưa có DD. Router plus matching module `view.py` có 12 API (#01–#09, #12–#14); 91 chưa có cặp route/view.
- Runtime/source: không có route, module, query, handler hoặc test cho `/api/v1/admin/reports/summary`; API #101 là `UNWIRED / NOT_FOUND`.
- Authorization: catalog yêu cầu Admin; helper Study hiện xác minh Student; chưa có Admin guard/claim policy. Middleware `DESIGN_CONTRACT_PATHS` không có #101; chỉ ghi như discrepancy nếu route tương lai được wire.
- Legacy schema candidate: `users.created_at`, `courses.created_at`, `enrollments.enrolled_at`, `discussions.created_at` có trong `infra/postgres/study-server/DB.sql`; không có reporting view/table trong legacy DDL. DDL này không chứng minh live schema.
- Pilot schema: `report_snapshots` là immutable, PK UUID, có `report_code`, period timestamps, `dimensions`, `metrics` JSONB, `generated_at`, uniqueness/version fields và retention 13 tháng. Chưa thấy report-code contract, JSON schema, writer hoặc API mapping; đây là design candidate riêng, không tự trộn vào legacy BIGINT model.
- Reusable `Report` định nghĩa shape nhưng không định nghĩa metric keys/formulas, date defaults, effective period hoặc rounding. AC-38 chỉ nói “Aggregate KPI summary”.
- Related DDs: #91 đề xuất quiz metrics theo `DERIVED` nhưng thuộc quiz domain và có response discrepancy; #66 ghi rõ current progress không phải learning-event history. Không chuyển metric của hai API này sang #101.
- Runnable tests: không có test #101; task docs-only, không chạy application tests.

## SOURCE_TRACE

```text
Admin Bearer principal -> GET /admin/reports/summary?from&to -> authorize report access -> derive effective date window -> aggregate candidate KPI counts from source relations or read an approved report snapshot -> map Report(period, metrics, generated_at) -> 200 DESIGN_RESOURCE_RETRIEVED or exact 401/403/500 errors -> dashboard then #102 / optional #103
```

## PLAN BEFORE DD AUTHORING

1. Giữ đúng API #101 catalog: method/path, Admin Bearer, query `from?:date`/`to?:date`, no body, `ApiEnvelope<Report>`, HTTP 200 và đúng ba error codes. Không thêm 404/422 hay thay response schema.
2. Đọc AC-38 đầy đủ: #101 aggregate KPI summary; #102 validate date range + quyền rồi aggregate learning/community metrics; #103 là nhánh export. Ghi #102/#103 contract khác nhau vào group watchlist, chưa macro-review nhóm cho tới sau #103.
3. Giữ `Report` schema trực tiếp và liệt kê đủ envelope/DateRange/ImpactMetric fields; catalog không đặt tên hoặc công thức metric.
4. Đề xuất MVP đơn giản, gắn `DERIVED`: bốn metric record-count độc lập theo cùng effective period — `user_records_created` từ `users.created_at`, `course_records_created` từ `courses.created_at`, `enrollment_records_created` từ `enrollments.enrolled_at`, `discussion_records_created` từ `discussions.created_at`. Đếm row, không join để tránh fan-out; không lọc status/role/root trong proposal. Giá trị `COUNT` serialize decimal-string; empty count là `"0"`. Tên/semantics vẫn cần xác nhận.
5. Đề xuất date window `DERIVED` để `Report.period` luôn có đủ `from/to`: không truyền hai bound thì rolling 30 ngày tới hôm nay; chỉ truyền `from` thì tới hôm nay; chỉ truyền `to` thì 30 ngày kết thúc ở ngày đó; truyền cả hai thì dùng inclusive range. `from > to`, calendar/timezone boundary và exact behavior chưa được contract chốt; không gán thêm error code.
6. Đề xuất `generated_at` là thời điểm tạo report theo UTC; metric value là số đếm dạng decimal string. Giữ đây là proposal, không ghi thành behavior runtime.
7. Đánh giá `report_snapshots` như alternative physical candidate. Do thiếu `report_code` được duyệt, writer, metrics JSON schema và live-schema proof, không chọn nó làm executable mapping; không invent report code hoặc JSON keys.
8. Tạo Request Usage, Query, Mutation (read-only/N/A), Response Source matrices trước khi điền 8 sheet. Dùng candidate mapping legacy riêng từng bảng; `07_table.md` liệt kê từng column; pilot snapshot là discrepancy riêng.
9. Tạo `apps/study-server/docs/dd/101_admin_reports_summary/` với 8 template sheets và 3 reports; exact template suffixes; Markdown-only; không sửa runtime, DDL, catalog, diagram hoặc client.
10. Validate ngay: manifest/front matter, exact contract/error set, every request/response field and candidate column, JSON, links/anchors, tables/fences/whitespace, fingerprints và `git diff --check`.
11. Sau DD #101 chỉ cập nhật inventory và ghi group AC-38 macro-review pending tới khi #103 DD hoàn tất.

### API Requirement Matrix

| API ID | Contract item | Giá trị | Basis/status |
|---|---|---|---|
| #101 | Method/path | `GET /api/v1/admin/reports/summary` | Catalog + AC-38; DIRECT |
| #101 | Actor/auth | Admin; Bearer JWT | Catalog + AC-38; DIRECT; guard SOURCE_REQUIRED |
| #101 | Query | `from?:date`, `to?:date` | Catalog; DIRECT |
| #101 | Body | Không khai báo | Catalog; DIRECT |
| #101 | Success | HTTP 200 `DESIGN_RESOURCE_RETRIEVED`; `ApiEnvelope<Report>` | Catalog; DIRECT |
| #101 | Report schema | `period`, `metrics[]`, `generated_at` | Reusable schema; DIRECT shape, metric semantics unspecified |
| #101 | Errors | 401 `DESIGN_AUTHENTICATION_REQUIRED`; 403 `DESIGN_ACCESS_DENIED`; 500 `DESIGN_INTERNAL_ERROR` | Catalog; DIRECT |
| #101 | Aggregate | KPI summary | AC-38 logical effect DIRECT; KPI set/formula SOURCE_REQUIRED; MVP proposal DERIVED |

### Request Usage Matrix

| Request item | Source/use | Data Mapping use | Rule/status |
|---|---|---|---|
| `Authorization` | Bearer JWT | Authenticate and authorize Admin | DIRECT role; claim/permission guard SOURCE_REQUIRED |
| `from` | Optional query date | Lower bound for all metric queries | DIRECT field; default/window semantics DERIVED proposal |
| `to` | Optional query date | Upper bound for all metric queries | DIRECT field; default/window semantics DERIVED proposal |
| Request body | None | None | DIRECT |

### Query Matrix

| Query ID | Purpose | Type | Candidate source/columns | Predicate/result | Status |
|---|---|---|---|---|---|
| Q1 | Count user records created | SELECT COUNT | legacy `users.created_at` | Effective period; no role/status filter | DERIVED metric proposal; legacy/live gap |
| Q2 | Count course records created | SELECT COUNT | legacy `courses.created_at` | Effective period; no status filter | DERIVED metric proposal; legacy/live gap |
| Q3 | Count enrollment records created | SELECT COUNT | legacy `enrollments.enrolled_at` | Effective period; no status filter | DERIVED metric proposal; legacy/live gap |
| Q4 | Count discussion records created | SELECT COUNT | legacy `discussions.created_at` | Effective period; includes root/reply rows | DERIVED metric proposal; legacy/live gap |
| Q5 | Read persisted summary snapshot | SELECT candidate | pilot `report_snapshots` fields | `report_code`/dimensions/period match not approved | SOURCE_REQUIRED; no executable query chosen |

### Mutation Matrix

| Mutation ID | Operation | Target | Fields | Status |
|---|---|---|---|---|
| — | None | N/A | API #101 is read-only; no INSERT/UPDATE/DELETE | N/A — READ-ONLY API |

### Response Source Matrix

| Response field | Type | Candidate source/transform | Status |
|---|---|---|---|
| `success` | boolean | Envelope branch | Shared convention |
| `businessCode` | string | `DESIGN_RESOURCE_RETRIEVED` | DIRECT catalog |
| `message` | string | Safe application message | Exact literal unspecified |
| `data.period.from` | date | Effective lower bound | DIRECT type; default/window DERIVED |
| `data.period.to` | date | Effective upper bound | DIRECT type; default/window DERIVED |
| `data.metrics[]` | `ImpactMetric[]` | Four candidate count metrics | DIRECT collection shape; keys/formulas DERIVED |
| `data.metrics[].key` | string | Stable proposed metric key | DIRECT type; key value DERIVED |
| `data.metrics[].value` | decimal-string | `COUNT(*)` result converted to decimal string | DIRECT type; formula DERIVED |
| `data.metrics[].label` | string | Vietnamese display label | DIRECT type; exact labels DERIVED |
| `data.generated_at` | date-time | Report generation clock | DIRECT type; UTC clock DERIVED |
| `meta` | object | Envelope | Endpoint fields unspecified |
| `traceId` | uuid | Request trace | Shared API guideline |

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| API #101 runtime | No route/module/query/test | `UNWIRED / NOT_FOUND` | DD only; no runtime claim |
| Metric contract | AC-38 says aggregate KPI; `Report` has generic metrics but no keys/formulas | `DERIVED / SOURCE_REQUIRED` | Candidate counts require owner confirmation |
| Date range | Both query bounds optional; response `DateRange` requires both | `DISCREPANCY / DERIVED` | Need approved effective-range/default/invalid-range rule |
| Persistence | Legacy tables have timestamp columns; pilot has UUID `report_snapshots` with unbound report code/metrics schema | `DISCREPANCY / SOURCE_REQUIRED` | Do not assume live schema or combine models |
| Admin access | Catalog requires Admin; shared helper only Student | `DISCREPANCY / SOURCE_REQUIRED` | Auth policy absent in current source |
| AC-38 contract consistency | #101 uses date query; #102 uses string query; #103 row returns Report while operation tracking says Operation | `DISCREPANCY / GROUP_REVIEW_PENDING` | Keep row contracts; macro-review after #103 |

## CHANGES

- Files changed: this plan-first worklog, the 11-file API #101 DD package, and the inventory worklog recheck.
- CONTEXT_UPDATES: None planned; no runtime/schema/catalog/diagram/context page changes.
- Assumptions: Four independent count metrics and rolling date window are `DERIVED` proposals only; no report code or snapshot JSON structure is invented.

## VERIFICATION

| Command/check | Result | Status |
|---|---|---|
| Worklog preflight | Selector chose #100/#48/#49; all three read fully. | VERIFIED |
| Catalog and schemas | #101 exact row and `Report`/`DateRange`/`ImpactMetric` schemas read; AC38 group rows #102/#103 and Operation tracking read. | VERIFIED_STATIC_ONLY |
| Diagram | Parsed AC38 nodes and edges: #101 aggregate summary → #102 date/access validation and community metrics → optional #103 export. | VERIFIED_STATIC_ONLY |
| Schema candidates | Legacy timestamp columns and pilot `report_snapshots` fields reviewed; live schema not verified. | VERIFIED_STATIC_ONLY |
| Current source | No #101 route/module/query/test; Student-only guard and middleware allowlist reviewed. | VERIFIED_STATIC_ONLY |
| Pre-authoring inventory | 100 DD folders; 3 absent (#101–#103); 12 route+view pairs. | VERIFIED_STATIC_ONLY |
| DD authoring/static validation | 11 Markdown files; exact contract/errors; 8/8 template suffixes; JSON, local links, 513 table rows, fences and whitespace passed. | VERIFIED_STATIC_ONLY |
| AC-38 macro-review #101–#103 | Deferred until DD #102 and #103 exist; contract differences remain explicit. | PENDING |
| Runtime tests | Docs-only; not run | NOT_RUN |

## HANDOFF

- Remaining blockers: Confirm metric set/formulas, date default/effective range, `report_snapshots` mapping or live aggregate source, Admin authorization, timezone, invalid range behavior, and AC-38 #103 response conflict.
- Next owner/action: Continue with API #102 DD; perform AC-38 macro-review after API #103 is authored.


## POSTFLIGHT — API #101 DD — 2026-10-24

- DD package: `apps/study-server/docs/dd/101_admin_reports_summary/` contains exactly 11 Markdown files (8 sheets + 3 reports); all 8 front matters and registered template appendix suffixes pass.
- Static validation: exact #101 method/path/query/response/error set retained; one JSON example parses; 18 local links resolve; 513 Markdown table rows are width-consistent; 3 code-fence pairs balance; final newlines and whitespace pass; `git diff --check` has no diagnostics.
- Fingerprints: template `3dc7fd2242dd1ed1bd9faba50aadad913a31b97ebf1392d6144bb905c5208137`; output `0019402aa57505c9a83e59af1693267c0296f97463f44681ea7267308fd823de`.
- Inventory after #101: catalog 103; 101 numbered DD folders and all have the core sheet roles; 89 have the full 11-file pack; the 12 legacy folders #01–#12 lack standard reports; #102–#103 are the 2 missing DDs.
- Source inventory: route marker plus matching module `view.py` exists for #01–#09 and #12–#14 (12); 91 catalog IDs have no route+view pair. This is source/wiring evidence, not runtime verification. No application tests were run.
- API #101 remains `UNWIRED / NOT_FOUND`; AC-38 macro-review #101–#103 remains pending until #102 and #103 DDs are present.
- Scope: Markdown and worklogs only; no runtime, tests, DB schema, catalog, diagram or context page changed.

## POSTFLIGHT ADDENDUM — AC-38 macro-review after API #103 — 2026-10-24

- Macro-review completed for #101–#103 and polling boundary API #18. Flow continuity is #101 summary → #102 community dashboard/filter → optional #103 export/view-only.
- Retained discrepancies: #101 date queries use `date` while #102 uses `string`; #103 row payload is `Report` while Operation tracking says `Operation`; API #18 has int64/UUID ID, owner/Admin policy, `Payment`/ExportAsset result and missing Study persistence/lifecycle decisions.
- Diagram formats CSV/XLSX/PDF and conditional temporary file storage are documented; defaults, filters, queue/storage mapping, download/expiry, retry and worker error rules remain open. #101–#103 remain `UNWIRED / NOT_FOUND`; no application tests were run.
- Updated connected DD plan/open-question/verification reports. No catalog, schema, diagram, runtime source or client changes.

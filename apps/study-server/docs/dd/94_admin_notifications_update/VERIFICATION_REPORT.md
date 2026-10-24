# Báo cáo kiểm chứng — API #94 Admin cập nhật notification

## Phạm vi
- DD folder: apps/study-server/docs/dd/94_admin_notifications_update/.
- Status: Draft — Needs Confirmation.
- Current source: UNWIRED / NOT_FOUND by scoped static scan.
- Application tests, runtime and live DB were not checked; docs-only task.
- AC-36 macro-review #92–#96: `VERIFIED_WITH_OPEN_QUESTIONS`; see [AC-36_MACRO_REVIEW.md](../96_admin_notifications_status/AC-36_MACRO_REVIEW.md).

## Nguồn đã đối chiếu
- Catalog #94 and Notification-related reusable schemas.
- AC/API index and AC-36 diagram UPDATE edge and reload node.
- DD #92/#93, PUT Admin precedents #75/#89, legacy table guide/DDL and separate V1-PILOT DDL.
- Current Study route/middleware source, API Guidelines, registered skill and template pack.
- Selector worklogs #48–#50; all three read before authoring.

## Template and package
- Baseline: eight Markdown files in .agents/skills/create_dd_api/docs/dd/DD_API_Template_MD/.
- Template manifest SHA-256: 541b6ea0c36c5781c1b62574e1aba4e2fab5fde2f949a54129a123c63b78b9c2.
- Study output: Markdown folder; no ZIP.
- Package target: 12 files — 8 standard sheets, one supplementary recipient mapping, 3 reports.

## Static verification

| Check | Result | Status |
|---|---|---|
| Package file count | 12 Markdown files: 8 standard sheets, one supplementary mapping, and 3 reports | PASS |
| Template appendix | 9/9 sheet appendix suffixes match template-backed #93 sheets byte-for-byte | PASS |
| Front matter | 9/9 sheets have dd_id 94 and Draft — Needs Confirmation status | PASS |
| Direct contract | Method/path/path type/response/status and five error codes preserved | PASS — static |
| JSON examples | 2/2 JSON examples parse | PASS |
| Tables/fences | 33 tables have consistent row widths; all tilde fences balanced | PASS |
| Links/anchors | 34 local links and anchors resolve | PASS |
| Whitespace/newlines | No trailing whitespace; all files end with newline | PASS |
| Mutation coverage | Notification and logical recipient update have separate mapping files; physical targets marked SOURCE_REQUIRED | PASS — design boundary |
| Source scan | No #94 route/module/test found in scoped scan | STATIC ONLY |
| Runtime/tests | Not run | NOT_RUN |

## Preserved discrepancies
- Catalog and diagram do not define a request body.
- Draft/scheduled wording does not define enum values, editability rules or scheduler side effects.
- Legacy BIGINT and V1-PILOT UUID schemas remain separate and neither is approved for Admin campaign persistence.
- #93 Notification-vs-Operation response and identifier bridge remain open after AC-36 macro-review.

## Kết quả

- Catalog contains 103 endpoint IDs; DD folders #01–#94 contain all 8 core sheet roles. Nine IDs (#95–#103) remain without DD.
- 82/94 DD folders contain all 3 standard reports; legacy #01–#12 remain core-only.
- Static source route-plus-view count remains 12/103 (#01–#09, #12–#14); 91 lack the matching pair. This is not runtime verification.
- No application tests, runtime, deployment or live database checks were run.

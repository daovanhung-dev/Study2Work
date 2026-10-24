# Báo cáo kiểm chứng — API #95 Admin xóa hoặc hủy notification

## Phạm vi
- DD folder: apps/study-server/docs/dd/95_admin_notifications_delete/.
- Status: Draft — Needs Confirmation.
- Current source: UNWIRED / NOT_FOUND by scoped static scan.
- Application tests, runtime and live DB were not checked; docs-only task.
- AC-36 macro-review #92–#96: `VERIFIED_WITH_OPEN_QUESTIONS`; see [AC-36_MACRO_REVIEW.md](../96_admin_notifications_status/AC-36_MACRO_REVIEW.md).

## Nguồn đã đối chiếu
- Catalog #95/#96 and reusable DeleteResult/Notification schemas.
- AC/API index and AC-36 diagram DELETE/mark cancelled branch.
- DD #92–#94 and DELETE precedents #77/#90.
- Legacy Study notifications DDL and separate V1-PILOT notification/delivery DDL.
- Current Study route/middleware, API Guidelines, registered skill and template pack.
- Selector worklogs #48–#50 and current #94 task worklog; all selected worklogs were read.

## Template and package
- Baseline: eight Markdown files in .agents/skills/create_dd_api/docs/dd/DD_API_Template_MD/.
- Template manifest SHA-256: 541b6ea0c36c5781c1b62574e1aba4e2fab5fde2f949a54129a123c63b78b9c2.
- Study output: Markdown folder; no ZIP.
- Package target: 12 files — 8 standard sheets, one supplementary logical delivery-cancellation mapping, 3 reports.

## Static verification

| Check | Result | Status |
|---|---|---|
| Package file count | 12 Markdown files: 8 standard sheets, one supplementary mapping, and 3 reports | PASS |
| Template appendix | 9/9 sheet appendix suffixes match template-backed #94 sheets byte-for-byte | PASS |
| Front matter | 9/9 sheets have dd_id 95 and Draft — Needs Confirmation status | PASS |
| Direct contract | Method/path/path type/no body/query/DeleteResult/status and five error codes preserved | PASS — static |
| JSON examples | 1/1 JSON example parses | PASS |
| Tables/fences | 32 tables have consistent row widths; all tilde fences balanced | PASS |
| Links/anchors | 32 local links and anchors resolve | PASS |
| Whitespace/newlines | No trailing whitespace; all files end with newline | PASS |
| Mutation coverage | Logical notification delete and scheduler boundary have separate mapping files; no physical target invented | PASS — design boundary |
| Source scan | No #95 route/module/test found in scoped Study source | STATIC ONLY |
| Runtime/tests | Not run | NOT_RUN |

## Preserved discrepancies
- Catalog says delete draft/cancel conditionally; diagram says DELETE/mark cancelled without a state machine.
- DeleteResult literal deleted does not distinguish cancellation.
- Legacy BIGINT and V1-PILOT UUID notification/delivery schemas remain separate.
- API #96 response lacks delivery aggregate fields needed by the proposed cancellation guard.
- #93 Operation response and identifier bridge remain open after AC-36 macro-review.

## Kết quả

- Catalog contains 103 endpoint IDs; DD folders #01–#95 contain all eight core sheet roles. Eight IDs (#96–#103) remain without DD.
- 83/95 DD folders contain all three standard reports; legacy #01–#12 remain core-only.
- Static route-plus-view count remains 12/103 (#01–#09, #12–#14); 91 lack the matching source pair. This is not runtime verification.
- No application tests, runtime, deployment or live database checks were run.

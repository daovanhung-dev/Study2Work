# Báo cáo kiểm chứng — API #93 Tạo/phát notification

## Phạm vi

- DD folder: apps/study-server/docs/dd/93_admin_notifications_create/.
- Status: Draft — Needs Confirmation.
- Current source: UNWIRED / NOT_FOUND by static scan.
- Application tests, runtime and live DB were not checked; docs-only task.
- AC-36 macro-review #92–#96: `VERIFIED_WITH_OPEN_QUESTIONS`; see [AC-36_MACRO_REVIEW.md](../96_admin_notifications_status/AC-36_MACRO_REVIEW.md).

## Nguồn đã đối chiếu

- Catalog #93, Notification/Operation schemas and Operation tracking summary.
- AC-36 index and diagram; CREATE/SEND nodes and conditional Push/Email edge.
- Legacy Study table guide/DDL and separate V1-PILOT notification/delivery DDL.
- DD #92, #63, #64 and #18.
- Current Study router/test scan, API Guidelines, registered skill, template pack and Study workflow.
- Selector worklogs #48–#50; all three were reviewed before authoring.

## Template and package

- Baseline: eight Markdown files in .agents/skills/create_dd_api/docs/dd/DD_API_Template_MD/.
- Template manifest SHA-256: 541b6ea0c36c5781c1b62574e1aba4e2fab5fde2f949a54129a123c63b78b9c2.
- Output manifest SHA-256 over 9 sheets plus PLAN_RESULT.md and OPEN_QUESTIONS.md: 431dca80bb04bbcbb0abe3525e351b094e4ece5fcab47cd5a73756a41e3908ed.
- Study workflow requires a Markdown folder; no ZIP.
- Package target: 12 files: 8 standard sheets, 1 supplementary recipient mapping, 3 reports.

## Static verification

| Check | Result | Status |
|---|---|---|
| Package file count | 12 files: 8 standard sheets, one extra mapping, and 3 reports | PASS |
| Template appendix | 9/9 sheets (8 standard + 1 extra mapping) match template appendix suffix byte-for-byte | PASS |
| Front matter | 9/9 sheets have front matter and dd_id: 93 | PASS |
| Direct contract | Method/path/body/response/status and exact five error codes match catalog | PASS — static |
| JSON examples | 2/2 JSON examples parse | PASS |
| Tables/fences | 30 tables / 453 table lines have consistent widths; 3 fence pairs balanced | PASS |
| Links/anchors | 49/49 local links and anchors resolve | PASS |
| Whitespace/newlines | No trailing whitespace; all Markdown files end with newline | PASS |
| Mutation coverage | Notification candidate and recipient association have separate mapping files | PASS — gaps labeled SOURCE_REQUIRED |
| Source scan | No #93 route/module/test found in scoped Study source | PASS — static |
| Runtime/tests | Not run | NOT_RUN |

## Preserved discrepancies

- Catalog/diagram Notification response conflicts with Operation tracking summary.
- Request lacks action/schedule while diagram dispatch is conditional; immediate send stays DERIVED.
- No approved Admin campaign/recipient schema; legacy and V1-PILOT models remain separate.
- API #18 UUID/int64 conflict and handoff to #96 remain open.
- Audience/channel enums, validation, permission, acceptance and failure triggers remain unconfirmed.

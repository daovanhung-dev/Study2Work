# Báo cáo kiểm chứng — API #95 Admin xóa hoặc hủy notification

## Phạm vi
- DD folder: `apps/study-server/docs/dd/95_admin_notifications_delete/`.
- Status: Draft — Needs Confirmation.
- Runtime: API #95 route/module is wired locally and fake-DB tested; live DB/deployment is not verified.
- AC-36 macro-review #92–#96: `VERIFIED_WITH_OPEN_QUESTIONS`; see [AC-36_MACRO_REVIEW.md](../96_admin_notifications_status/AC-36_MACRO_REVIEW.md).

## Nguồn đã đối chiếu
- Catalog #95/#96 and reusable DeleteResult/Notification schemas.
- AC/API index and parsed AC-36 diagram DELETE/mark cancelled branch.
- DD #92–#94, current #93/#94 code and Admin DELETE precedent #90.
- Legacy Study notifications DDL and migration 009 cascade FK; separate V1-PILOT notification/delivery DDL.
- Current Study router/middleware, shared ADMIN auth, API Guidelines, registered skill/template pack.
- Selector coding worklogs #74/#75/#76 and API #94 worklog; all three selected coding worklogs were read.

## Template and package
- Baseline: eight Markdown files in `.agents/skills/create_dd_api/docs/dd/DD_API_Template_MD/`.
- Study output: Markdown folder; no ZIP.
- Package target: 12 files — 8 standard sheets, one supplementary delivery/scheduler mapping, 3 reports.
- The 9 sheet appendix suffixes must remain byte-identical to the original template-backed #94 layout.

## Verification status

| Check | Result | Status |
|---|---|---|
| Package file count | 12 Markdown files: 8 standard sheets, one supplementary mapping, 3 reports | PASS |
| Template appendix | 9/9 appendix suffixes match canonical Markdown templates byte-for-byte | PASS |
| Front matter | All 9 sheets retain dd_id 95 and Draft — Needs Confirmation | PASS |
| Direct contract | Method/path/no body/query/DeleteResult/status and five catalog errors retained | PASS — source/docs review |
| JSON examples | 1/1 fenced JSON example parses | PASS |
| Tables/fences | Consistent table column counts; all fences balanced | PASS |
| Links/anchors | 33 local Markdown links and anchors resolve | PASS |
| Whitespace/newlines | No trailing whitespace; all files end with newline | PASS |
| Source tests | API #95 focused: 21; linked #92–#95: 87; full Study suite: 1284 passed | PASS — fake DB |
| Ruff/OpenAPI | `ruff check app tests`; scoped format check; 55 paths / 66 operations | PASS |
| Runtime/live DB | No live environment verification | NOT_VERIFIED |
| Context validation | Validator reports only existing missing db-admin context/source roots outside this task scope | PARTIAL — repository baseline |

## Preserved discrepancies
- Catalog says delete draft/cancel conditionally; diagram says DELETE/mark cancelled without lifecycle states.
- Local queued-only hard-delete/cascade is DERIVED; it removes the selected notification's outbox rows.
- DeleteResult literal `deleted` does not prove external cancellation.
- Legacy BIGINT and V1-PILOT UUID notification/delivery models remain separate.
- API #96 response lacks delivery aggregate; #93 Operation/ID bridge remains open.
- Live schema, migration deployment, worker/scheduler/provider and dedicated permission are unverified.

## Kết quả

API #95 is wired and locally verified. This is source/test evidence only; it does not establish PostgreSQL locking/cascade, live deployment, scheduler behavior, provider delivery, fine-grained permission or owner approval. The context validator reports a pre-existing db-admin context/source gap outside Study; no Study Server error was reported.

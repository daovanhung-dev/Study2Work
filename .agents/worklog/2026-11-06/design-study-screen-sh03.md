---
task_id: "2026-11-06-design-study-screen-sh03"
date: "2026-11-06"
primary_task_type: "docs"
secondary_task_types: []
project_scopes: ["web-work", "server-study"]
cross_scope_dependencies: ["SH-03 registration UI -> API #01; SH-04 email handoff/API #02; account activation and registration route policy"]
status: "VERIFIED"
---

# Worklog: Rà soát Detailed Design màn hình Study SH-03

## PRIOR_WORKLOG_REVIEW

- primary_task_type: docs
- selector_command: `node scripts/select-worklogs.mjs --type docs --limit 3`
- selector_result: READY; selected 3 of 155 docs worklogs and read all selected files.
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-11-06/design-study-screen-sh01.md`
    - carry_forward: Keep DD/implementation/runtime statuses separate; trace APIs and preserve user source assets; stable element/event IDs and acceptance evidence matter.
  - path: `.agents/worklog/2026-11-06/design-study-screen-sh02.md`
    - carry_forward: UI-only DD has no canonical registered skill; source/API/runtime claims must stay distinct; SH-03 is the next W0 screen.
  - path: `.agents/worklog/2026-11-05/check-study-screen-stitch-coverage.md`
    - carry_forward: 83 screen IDs are represented in the inventory; asset presence is static evidence only, not proof of visual quality or runtime.
- shortage: none
- Additional related worklog reviewed: `.agents/worklog/2026-10-27/design-study-screen-sh03.md` (prior SH-03 trace and handoff; all claims to be revalidated against current source).

## EXPECTED_BEHAVIOR

- Requirement: Complete SH-03 only in this session; review/update its plan before modifying DD/assets; preserve original PNG/HTML; ensure annotated markers map one-to-one to DD elements; trace all events and API behavior to current source; update the global tracker and this worklog.
- Canonical contract: `apps/study-client/docs/list_screen.md` SH-03, AC-01, F01, API #01/#02, API catalog, current Study Server source; `.agents/web-study/design.md` is intended UI target, not runtime evidence.

## CURRENT_BEHAVIOR

- SH-03 folder contains original `screen.png` and `code.html`, annotated image, marker JSON, plan, and DD. Original PNG/HTML hashes rechecked: `67eef666cf7ebf48db44b2b721b13a40632237a165ff11ca6b5a2040a32d079e` and `bd0123dee4571caff1920804b4ce8508d2f20f53ce8e113afcb766874c8334a3`.
- `apps/study-client/src` and `.agents/web-work/study/` are absent. The HTML mock intercepts form submission with `preventDefault()` and has no network call.
- API #01 route/source validates fields, checks duplicates, hashes with Argon2id, inserts the STUDENT profile, commits, returns public profile data, and maps duplicate/validation/internal errors to 409/422/500. SQL does not explicitly set `status`; checked-in DDL's ACTIVE default is not proof of live schema.
- API #02 is a separate public endpoint with a default `StubVerificationEmailProvider`; accepted means only stub acceptance. API #01 logs pending dispatch and does not call #02. AC-01/F01 placement differs and remains explicitly documented as a discrepancy.

## SOURCE_TRACE

- `apps/study-client/docs/list_screen.md`: SH-03 is public `/register` (proposed), AC-01, API #01, next SH-04/SH-02; F01 places API #02 at SH-04.
- `apps/study-server/app/api/v1.py` and `app/modules/guest/api_01_auth_register/{models.py,validate.py,query.py,view.py}`: route, request schema, normalization/validation, SQL effects, transaction owner, response, and errors.
- `app/modules/guest/api_02_auth_verify_email_send/{validate.py,view.py}` and `app/service/email/provider.py`: separate API #02 behavior and stub provider; no actual delivery or verification side effect.
- Read API #01/#02 tests and DD open questions; tests were not run. Read AC-01 drawio, API catalog, checked-in DDL, and Study Web design guide. No claim is made that DB.sql is the live schema.
- `UserProfile.bio` catalog schema is optional but not included in the current API #01 INSERT response; SH-03 only consumes `id` and `email`.

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| Source image and HTML | Both originals retained; annotated image has seven visible markers; source hashes match preflight. | VERIFIED | Stable marker IDs are being mapped one-to-one to DD rows. |
| Study Web wiring | Client source and child context absent; HTML mock only prevents default submit. | NOT_FOUND | DD can be ready while implementation remains blocked; runtime is unverified. |
| API #01/#02 | #01 source-backed; #02 default provider is stub; #01 does not call #02; AC/F01 placement discrepancy recorded. | DISCREPANCY | Keep SH-04 handoff separate; do not claim email delivery/verification. |
| Account activation | SQL insert omits status; checked-in DDL defaults ACTIVE; API #03 requires ACTIVE; live schema and verification gate unresolved. | IMPLEMENTATION BLOCKED | Product/server must resolve activation and live schema before release. |

## CHANGES

- Files changed: `SH-03_PLAN.md` completed after plan-first review; `SH-03.md` updated with separate statuses, source links, seven stable element IDs and eight event contracts; `SH-03_markers.json` updated with one-to-one IDs and coordinate provenance; global `dd_screens/PLAN.md` updated with SH-03 status and SH-04 handoff; this worklog completed.
- `screen.png` and `code.html` hashes are unchanged. Existing `screen_annotated.png` was retained after prior visual review; its 2560×2112 size is 2× the 1280×1056 original.
- CONTEXT_UPDATES: None; no runtime contract, architecture, or DB schema pages changed.
- Context pages changed: None.
- Skill registry was checked before authoring; it does not provide a canonical skill for Web UI-only DD, so source-traced documentation and explicit blockers were used.

## VERIFICATION

| Command/read | Result | Status |
|---|---|---|
| `node scripts/select-worklogs.mjs --type docs --limit 3` | Selected 3 exact-type worklogs of 155; all selected files read. | VERIFIED |
| SH-03 source/API review | API #01/#02 boundaries and account-status source findings verified by reading source/contracts; no application execution. | VERIFIED |
| SH-03 static artifact audit | PNG header dimensions 1280×1056 and 2560×2112; source SHA-256 values match plan; 7 markers map in order to 7 unique DD Element IDs; 8 sequential Event IDs; all local Markdown links resolve; tracker and handoff consistent. | VERIFIED |
| `git diff --check` (task files) | No whitespace errors. | VERIFIED |
| Tests/runtime | Not run. | NOT_RUN |

## HANDOFF

- Remaining blockers: Study Web/router absent; API #02 stub/no real email; account activation and live schema unresolved; HTML password helper says 8 characters but API has no such rule. DD READY does not clear these implementation blockers.
- Final screen status: DD READY; IMPLEMENTATION BLOCKED; RUNTIME NOT VERIFIED.
- Next owner/action: SH-04 in a separate session; trace its handoff contract from SH-03 and API #02, and do not begin another Screen ID in this session.

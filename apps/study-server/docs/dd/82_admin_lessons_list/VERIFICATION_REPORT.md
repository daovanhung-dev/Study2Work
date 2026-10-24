# Verification Report — API #82 Lấy danh sách lesson

## Scope

- DD output: `apps/study-server/docs/dd/82_admin_lessons_list/`.
- Task: Markdown DD, one API only; no runtime, database, catalog, router or diagram edits.
- DD status: Draft — Needs Confirmation.
- Application tests: `NOT_RUN`; current source has no API #82 route.

## Static checks

| Check | Result | Status |
|---|---|---|
| Expected package | 11 Markdown files: eight template sheets and three standard reports | PASS |
| Template appendix parity | All eight sheet appendix suffixes match registered templates byte-for-byte | PASS |
| Catalog contract | Method/path/query, direct response type, success and exact 401/403/500 codes retained | PASS |
| JSON examples | 3/3 JSON blocks parse | PASS |
| Tables and fences | 29 tables / 372 data rows have consistent column counts; 14 fenced blocks are balanced | PASS |
| Relative links/anchors | 34 local links and anchors resolve | PASS |
| Whitespace | Final newlines present; no trailing whitespace; `git diff --check` clean | PASS |
| Inventory at AC-34 review | 86 DD folders / 17 missing; 74 full 11-file packages; 12 core-only legacy packs | PASS — STATIC |
| Source inventory | 12 route-plus-view API IDs / 91 without pair | PASS — STATIC |
| Runtime behavior | Route absent; tests not run | NOT_RUN / UNWIRED |

## Fingerprints

| Fingerprint | Scope | SHA-256 |
|---|---|---|
| Registered template pack | Eight sorted template names + NUL + raw bytes + NUL | `3dc7fd2242dd1ed1bd9faba50aadad913a31b97ebf1392d6144bb905c5208137` |
| DD output payload | Eight sheets, `OPEN_QUESTIONS.md`, and `PLAN_RESULT.md`; verification report excluded | `f1ff97512117606a697e3c94850a021b89495c90b5573f87f174aa4933ea7e0f` |

## Findings and limits

- Catalog #82 declares `ApiEnvelope<Lesson>` while the endpoint name and AC-34 flow describe a list. The DD preserves the direct contract and labels `ApiEnvelope<Lesson[]>` only as a derived proposal.
- The `type` query has no compatible Lesson field in the reusable schema or inspected DDL. The filter remains `SOURCE_REQUIRED`.
- Legacy BIGINT and V1-PILOT UUID lesson models are not interchangeable. Legacy `course_id` is nullable, while the reusable Lesson contract requires it.
- Admin guard/permission, LessonStatus members/casing, malformed-query errors and error-envelope `data` behavior remain unresolved.
- Source inventory counts router declaration plus matching module `view.py`; it does not prove runtime behavior. The current route is absent and application tests were not run.
- AC-34 macro-review #82–#86 is complete at document level with unresolved contract/schema questions retained; see the section below.

## AC-34 macro-review

- Status: `VERIFIED_WITH_OPEN_QUESTIONS`; this is a document-level consistency review, not owner approval or runtime verification.
- API #82 remains the list/reload endpoint. Its direct `ApiEnvelope<Lesson>` conflicts with list intent; #86 soft-delete visibility cannot be filtered until a marker and policy are selected.
- See the [consolidated review matrix](../86_admin_lesson_delete/VERIFICATION_REPORT.md#ac-34-macro-review) for cross-API findings and remaining decisions.

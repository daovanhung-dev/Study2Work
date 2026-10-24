# Verification Report — API #83 Lấy lesson detail

## Scope

- DD output: `apps/study-server/docs/dd/83_admin_lesson_detail/`.
- Task: Markdown DD for one API; no router, module, test, schema, catalog or diagram edits.
- DD status: Draft — Needs Confirmation.
- Application tests: `NOT_RUN`; current Study source has no API #83 route.

## Static checks

| Check | Result | Status |
|---|---|---|
| Expected package | Exact 11 Markdown files: eight template sheets and three standard reports | PASS |
| Template appendix parity | All eight sheet appendix suffixes match registered templates byte-for-byte | PASS |
| Catalog contract | Exact GET/path/Admin/path parameter/single Lesson response/200 and 401/403/404/500 codes retained | PASS |
| JSON examples | 3/3 JSON blocks parse | PASS |
| Tables and fences | 29 tables / 377 data rows have consistent column counts; 12 fenced blocks are balanced | PASS |
| Relative links/anchors | 37 local links and anchors resolve | PASS |
| Whitespace | Final newlines present; no trailing whitespace; `git diff --check` clean | PASS |
| DD inventory at AC-34 review | 86 folders / 17 missing; 74 complete 11-file packages; 12 core-only legacy packs | PASS — STATIC |
| Source inventory | 12 route-plus-view API IDs / 91 without pair | PASS — STATIC |
| Runtime behavior | API #83 route absent; tests not run | NOT_RUN / UNWIRED |

## Fingerprints

| Fingerprint | Scope | SHA-256 |
|---|---|---|
| Registered template pack | Eight sorted template names + NUL + raw bytes + NUL | `3dc7fd2242dd1ed1bd9faba50aadad913a31b97ebf1392d6144bb905c5208137` |
| DD output payload | Eight sheets, `OPEN_QUESTIONS.md`, and `PLAN_RESULT.md`; verification report excluded | `af712de020be17c7cf6a25b4fc723a55fa408cfd655bafadc63216b96397e4dc` |

## Findings and limits

- AC-34 n5 says to read the lesson and dependencies, but the catalog response is only `Lesson` and the diagram does not define dependency fields, counts or output location. The DD does not add unused queries or fields; this remains an owner clarification.
- The candidate legacy BIGINT mapping is not live-schema proof. `course_id` is nullable in legacy DDL but required in the reusable response; V1-PILOT lessons use a different UUID/versioned model.
- Admin authorization, LessonStatus values/casing, malformed-path mapping, soft-delete visibility, error `data` behavior and middleware path allowlisting remain unresolved.
- The source inventory criterion is a route declaration plus matching module `view.py`. This is source-presence evidence, not runtime verification. No application tests were run.
- AC-34 macro-review #82–#86 is complete at document level with dependency and deletion visibility questions retained; see the section below.

## AC-34 macro-review

- Status: `VERIFIED_WITH_OPEN_QUESTIONS`; this is a document-level consistency review, not owner approval or runtime verification.
- API #83 returns only the declared `Lesson`; dependency reads remain undefined. API #86 independently checks current references/progress before a proposed delete and does not rely on the earlier detail response.
- See the [consolidated review matrix](../86_admin_lesson_delete/VERIFICATION_REPORT.md#ac-34-macro-review) for cross-API findings and remaining decisions.

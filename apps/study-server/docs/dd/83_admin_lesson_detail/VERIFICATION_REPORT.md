# Verification Report — API #83 Lấy lesson detail

## Scope

- DD output: `apps/study-server/docs/dd/83_admin_lesson_detail/`.
- Task: implement API #83 runtime, focused tests, and synchronize the source-backed Markdown DD/context; no schema, catalog or diagram changes.
- DD status: Draft — Needs Confirmation.
- Runtime status: API #83 route/module/test are locally wired. No live database/deployment check was performed.
- Application tests: focused API #83 15 passed; linked #09/#74/#82 regression 54 passed; full Study suite 1027 passed.

## Static checks

| Check | Result | Status |
|---|---|---|
| Expected package | Exact 11 Markdown files: eight template sheets and three standard reports | PASS |
| Template appendix parity | All eight sheet appendix suffixes match registered templates byte-for-byte | PASS |
| Catalog contract | Exact GET/path/Admin/path parameter/single Lesson response/200 and 401/403/404/500 codes retained; malformed ID -> 404 is locally DERIVED | PASS |
| JSON examples | 3/3 JSON blocks parse | PASS |
| Tables and fences | 29 tables / 377 data rows have consistent column counts; 12 fence markers (6 code blocks) are balanced | PASS |
| Relative links/anchors | 39 local references including 21 anchors resolve | PASS |
| Whitespace | Final newlines present; no trailing whitespace; `git diff --check` clean | PASS |
| DD inventory at AC-34 review | Historical document review checkpoint: 86 folders / 17 missing; 74 complete 11-file packages; 12 core-only legacy packs | PASS — HISTORICAL STATIC |
| Source/OpenAPI | API #83 route/module/test present; 49 unique `/api/v1` paths / 54 operations | PASS — LOCAL SOURCE |
| Runtime behavior | Focused API #83 suite 15; linked #09/#74/#82 regression 54; full Study suite 1027 | PASS — LOCAL TESTS |

## Fingerprints

| Fingerprint | Scope | SHA-256 |
|---|---|---|
| Registered template pack | Eight sorted template names + NUL + raw bytes + NUL | `3dc7fd2242dd1ed1bd9faba50aadad913a31b97ebf1392d6144bb905c5208137` |
| DD output payload | Eight sheets, `OPEN_QUESTIONS.md`, and `PLAN_RESULT.md`; verification report excluded | `2bffbab72a536f230a89ff3506e183145e2f4e2a403f8389ed063f4b7f6dd8bd` |

## Findings and limits

- AC-34 n5 says to read the lesson and dependencies, but the catalog response is only `Lesson` and the diagram does not define dependency fields, counts or output location. The DD does not add unused queries or fields; this remains an owner clarification.
- The candidate legacy BIGINT mapping is not live-schema proof. `course_id` is nullable in legacy DDL but required in the reusable response; V1-PILOT lessons use a different UUID/versioned model.
- Shared `ADMIN` role auth is locally wired; AC-34's fine-grained permission, LessonStatus values/casing, dependency output and soft-delete visibility remain unresolved. Malformed-path 404 and optional-null serialization are local DERIVED behavior covered by tests.
- Focused and full tests use fake DB sessions; they verify local route/error/mapping orchestration, not PostgreSQL compatibility, live schema, deployment or runtime permissions.
- AC-34 macro-review #82–#86 is complete at document level with dependency and deletion visibility questions retained; see the section below.

## AC-34 macro-review

- Status: `VERIFIED_WITH_OPEN_QUESTIONS`; this is a document-level consistency review, not owner approval or runtime verification.
- API #83 returns only the declared `Lesson`; dependency reads remain undefined. API #86 independently checks current references/progress before a proposed delete and does not rely on the earlier detail response.
- See the [consolidated review matrix](../86_admin_lesson_delete/VERIFICATION_REPORT.md#ac-34-macro-review) for cross-API findings and remaining decisions.

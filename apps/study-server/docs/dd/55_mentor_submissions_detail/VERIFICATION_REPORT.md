# Verification Report — Study API #55 Lấy bài làm và rubric Mentor

**Result:** `PARTIALLY_VERIFIED_WITH_OPEN_QUESTIONS`

**DD status:** `Draft — Needs Confirmation`

**Route:** `GET /api/v1/mentor/submissions/{submission_id}`

## Source coverage

| Source | Evidence and decision |
|---|---|
| API catalog | `GET`, Mentor Bearer auth, signed int64 path, `ApiEnvelope<Submission>`, and the 200/401/403/404/500 status set are implemented. |
| AC-23 diagram | Read the #54 → #55 → #56 → #57 sequence. The #55 action mentions rubric, while its response node is `ApiEnvelope<Submission>`. Record the mismatch; do not invent a rubric response field. |
| Legacy DDL and ERD | The legacy BIGINT submission model has `file_url` and no assignment-to-rubric relation. Nullable relation columns differ from the required-parent interpretation in the guide; live schema was not queried. |
| V1-PILOT DDL | UUID assessments/rubrics have no source-backed relationship to legacy BIGINT assignment submissions; no cross-model join is used. |
| Linked API contracts | Compared #34 upload metadata, #35 producer, #36 student submission detail, #46/#47 Mentor ownership, #48 path handling, #54 list, and #56/#57 follow-up. API #35 file URL compatibility and rubric linkage remain unresolved. |
| Current runtime | API #55 is wired in `app/api/v1.py`, its route template is registered in middleware, and its view/query/models/validation and TestClient module exist. The view uses the shared MENTOR guard, numeric JWT subject and direct `courses.mentor_id` fallback. |

## Implemented behavior

- Read one submission with LEFT JOINs to assignment/course and a constrained lookup for at most one upload matching exact URL, owner, `SUBMISSION` purpose, and course. No match yields `files: []`.
- Reject malformed or out-of-range raw path values with catalog 404, following API #48. Missing rows return 404; direct-owner mismatch returns 403; missing required parent relations return safe 500.
- Reuse API #54's `SubmissionResponse`; map score to string, omit null optional fields, and return the shared success envelope. The endpoint performs no commit.
- Do not query or return rubric because neither the catalog response type nor inspected legacy schema supplies a supported field/relation.

The direct-owner rule, malformed-path behavior, parent-integrity response, and upload matching are `DERIVED` fallbacks, not approved business or live-schema facts.

## Verification

| Check | Result | Status |
|---|---|---|
| Focused API #55 TestClient suite | 22 passed; one upstream Starlette/httpx deprecation warning | `VERIFIED_LOCAL` |
| Full Study Server suite | 483 passed; same upstream warning | `VERIFIED_LOCAL` |
| Ruff | Passed for the API #55 module, route, middleware, and tests | `VERIFIED_LOCAL` |
| OpenAPI | 26 `/api/v1` operation declarations and 25 unique path templates; #55 is GET with int64 `submission_id` and `GetMentorSubmissionEnvelope` | `VERIFIED_LOCAL` |
| DD static check | Eight expected template sheets present; Excel appendix suffixes byte-match templates; JSON examples parse; local links, fences, and whitespace pass | `VERIFIED_STATIC` |
| `git diff --check` | Passed | `VERIFIED_STATIC` |
| Context validator | `deno run -A scripts/validate-agent-context.mjs` fails on pre-existing repository context drift and missing `db-admin` scope. With `--skip-drift`, reported structural findings are confined to missing `db-admin` pages/roots and their links. The checkout contains unrelated dirty source changes, so drift cannot be represented as API #55-only. | `BLOCKED_BY_REPOSITORY_BASELINE` |
| Live database, schema, or deployment | Not checked | `NOT_VERIFIED` |

## Remaining questions

- AC-23 requests a rubric projection, but the catalog `Submission` schema and inspected legacy DDL provide no rubric field or relationship.
- The direct course-owner fallback does not establish assigned-Mentor access. Confirm the intended ownership rule.
- Confirm whether the #35 upload producer writes URLs compatible with the lookup and whether `file_url` can represent more than one asset.
- Confirm live submission/assignment/course nullability, timestamp zone, and score/status semantics with the schema/contract owner.

## Linked API review

- #54 selects the submission list; #55 returns one `Submission`; #56 owns grade/status mutation; #57 owns feedback mutation. #55 does not change grade or feedback.
- The shared file lookup is consistent between #54 and #55 at source level. Runtime compatibility with #35 and client behavior remain unverified.
- The rubric mismatch and access/schema questions remain open for the linked #54–#57 flow; no end-to-end or deployed behavior is claimed.

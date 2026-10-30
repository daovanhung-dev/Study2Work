# Plan Result — API #88 Tạo quiz mới

## Kết quả

- API: `POST /api/v1/admin/quizzes`.
- Scope: `server-study`; implementation API #88, local legacy BIGINT schema support, tests, Draft DD và context pages liên quan.
- Direct outer request/response contract giữ nguyên catalog; lựa chọn embedded schema và hai schema extensions được đánh dấu DERIVED.
- DD remains `Draft — Needs Confirmation`; không tạo ZIP.

## Plan gate

- `primary_task_type`: `coding`; secondary: `test`, `docs`; scope: `server-study`.
- Coding selector chọn 3/81 worklogs; đọc đủ `.agents/worklog/2026-10-26/implement-api74-admin-course-detail.md`, `implement-api75-admin-course-update.md`, và `implement-api76-admin-course-status.md`; shortage `none`.
- Related source reviewed: API #87 (Admin quiz list), API #50 (transactional create pattern), API #28 (Student Quiz response boundary), API #89 (quiz update dependency).
- Registered `createDD-markdown` template pack contains the ordered 8-sheet Markdown baseline; API #88 keeps its existing 10 sheets + 3 reports and Excel appendix tails.
- Existing dirty worktree is preserved; no staging/commit/cleanup.

## Source priority and choices

| Priority | Evidence | Finding / choice |
|---|---|---|
| 1. AC-35 diagram | Create branch calls API #88, “INSERT Quiz + Questions”; direct success/error contract and Admin actor. | Create parent and children in one transaction; insert choices follows `QuizQuestion.choices[]` and is DERIVED. |
| 2. Infrastructure | Legacy BIGINT schema/ERD initially lacked question type and choice ordering; migration 013 and local DDL/diagram now add candidate columns. V1-PILOT uses incompatible UUID relations but lists three type labels. | Keep the additions as local DERIVED candidates on legacy child tables only. Reuse pilot labels as vocabulary, never mix IDs/tables. |
| 3. Catalog | Body strings `config` and `questions`, `ApiEnvelope<Quiz>`, logical `QuizQuestion.type`; no nested schema or QuizChoice shape. | Keep outer body direct; derive embedded config/questions shape and local Admin choice projection from logical fields + physical columns. |
| 4. Simplest fallback | No answer-count/course-lifecycle rule; no fine-grained permission source. | Enforce shared ADMIN only, check course existence, preserve order, default absent `is_correct=false`, avoid type-specific answer rules, use status DRAFT database default. |

## Local implementation contract (DERIVED unless labeled DIRECT)

- `config` JSON: `course_id`, `title`, optional `duration_minutes`, `passing_score` decimal-string.
- `questions` JSON: ordered array of `text`, `type`, and `choices`.
- QuestionType vocabulary: `SINGLE_CHOICE`, `MULTIPLE_CHOICE`, `TRUE_FALSE`.
- Choice input: `text`, optional `is_correct=false`.
- Local Admin choice response: `{id,text,is_correct}`; Student API #28 must omit answer keys.
- Migration 013 adds `quiz_questions.question_type` (nullable for old rows; API #88 always writes one of the allowed values) and `quiz_choices.sort_order` (zero-based request index).
- Course absence returns 422 because API #88 catalog has no 404.
- Atomic parent/question/choice insert; response mapping precedes commit; failures roll back the transaction.

## Verification results

- API #88 focused HTTP suite: 21 passed. Combined #87/#88 quiz regression: 41 passed.
- Full Study suite: 1134 passed; one upstream Starlette/httpx deprecation warning.
- Ruff: `All checks passed!` across `app tests`.
- Application OpenAPI: 51 `/api/v1` path templates and 59 operations; POST `/api/v1/admin/quizzes` is present.
- Migration/bootstrap/table-guide parity and Draw.io XML parse: passed.
- Ten source-sheet Markdown files: balanced code fences, consistent table widths, valid local links, and Excel appendix tails. Three authored reports are checked separately.
- `git diff --check`: passed after removing trailing whitespace in the new DD header.
- Deno context validation: no Study Server manifest/path finding; repository-wide validation still reports pre-existing missing DB Admin scope files/source paths, and default drift mode cannot find its pinned baseline commit. No DB Admin files are added in this task.

## Limits

The fine-grained AC-35 permission, owner approval of DERIVED decisions, old-row question type backfill, live schema, applied migration, deployment and physical PostgreSQL behavior remain unverified until an authoritative runtime source is available.

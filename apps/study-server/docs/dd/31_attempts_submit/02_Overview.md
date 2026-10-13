---
title: "Overview"
order: 2
dd_id: "31"
api_name: "Khóa attempt và bắt đầu chấm"
source_sheet: "Overview"
status: "Draft — Needs Confirmation"
---

# Overview

## Khái quát

| Thuộc tính | Giá trị |
|---|---|
| API ID | 31 |
| Module | Student / Assessment |
| Method | POST |
| Endpoint | /api/v1/attempts/{attempt_id}/submit |
| Purpose | Student nộp một quiz attempt; flow AC-16 khóa attempt, chấm tự động và xác định trạng thái chờ chấm tay hoặc đã chấm. |
| Consumer/Actor | Student |
| Authentication | Bearer JWT. |
| Authorization | Role Student theo API catalog; ownership và trạng thái attempt được phép submit chưa được đặc tả. |
| Basis | DIRECT — API catalog là APPROVED_DESIGN_CONTRACT; AC-16 là flow design. |
| Status | Draft — Needs Confirmation |
| Transaction | TBD — transaction boundary, locking và rollback chưa được nguồn chốt. |
| Side effects | Candidate UPDATE quiz_attempts; candidate grading UPDATE quiz_answers. Physical mapping design-only. |

## Sources

- [API catalog](../../../../../docs/lists/list_api.md) — API #31, QuizAttempt, QuizAnswer và business-code contract.
- [AC/API index](../../diagrams/AC_UNICA/00_AC_API_INDEX.md) — actor, precondition, postcondition và AC-16 API sequence.
- [AC-16 activity diagram](../../diagrams/AC_UNICA/AC_02_STUDENT_LEARNING.drawio) — submit, automatic grading và manual-grading branch.
- [DB table design](../../diagrams/DB_UNICA_TABLES.md) — candidate quiz_attempts, quiz_answers, quiz_questions và quiz_choices mappings.
- [DB ERD](../../diagrams/DB_UNICA_ERD.drawio) — candidate relations for attempt, answer, question and choice.
- [Checked-in DB DDL](../../../../../infra/postgres/study-server/DB.sql) — design DDL; does not verify live schema.
- [Shared API guidelines](../../../../../contracts/api-guidelines/README.md) — envelope, error data and trace conventions.
- [API #29 DD](../29_quizzes_attempts/00_Cover.md) and [API #30 DD](../30_attempts_answers/00_Cover.md) — preceding AC-16 drafts and unresolved lifecycle/answer mapping.
- [Current Study router](../../../app/api/v1.py) — current runtime wiring scan.

## Tables read

- quiz_attempts — candidate attempt identity, owner, status and timestamps.
- quiz_answers — candidate submitted answers and grading fields.
- quiz_questions — candidate question score and quiz relationship.
- quiz_choices — candidate correctness values for choice-based answers.

## Tables write

- quiz_attempts — candidate status, submitted_at and aggregate score update.
- quiz_answers — candidate correctness and per-answer score update for automatic grading.

## Mục chú ý

- API catalog defines no request body; only path attempt_id:int64! is required.
- Success is HTTP 200 DESIGN_RESOURCE_UPDATED with ApiEnvelope<QuizAttempt>.
- AC-16 explicitly names SUBMITTED, automatic grading, and PENDING_GRADE versus GRADED.
- AC-16 does not define grading formula, manual-question detection, status enum, or repeat-submit semantics.
- API #31 is absent from current Study route/module/test wiring; this DD describes expected design only.

## Assumptions

- Study API DD status is Draft — Needs Confirmation while material rules remain open.
- application/json is the response media type under the shared envelope convention; no request body or request Content-Type is defined.
- Database fields and writes below are candidate design mappings only; live metadata is not verified.
- No ZIP is produced, following the Study Server DD workflow.

## Conflicts

- AC-16 places grading at API #31, while checked-in quiz_answers.is_correct is NOT NULL and API #30 has no source-defined correctness value before submission.
- Logical QuizAnswer allows choice_ids or text_answer, while the physical table design stores one choice_id per row and has no text answer column.
- DB_UNICA_TABLES.md describes quiz FKs as required; checked-in DB.sql permits nullable foreign keys. Live schema is unverified.
- The activity diagram names PENDING_GRADE and GRADED, but the complete AttemptStatus enum is not defined in the catalog.

## Security note

- Do not accept Student identity from request data; the contract supplies Student Bearer JWT.
- Attempt ownership lookup and foreign-owner behavior (403 versus masked 404) are unresolved.
- Do not expose answer correctness or score unless the submitted-result disclosure policy is confirmed.

## Performance note

- Candidate grading reads the attempt and its answer/question/choice relations.
- Question count, answer count, query strategy, transaction duration and concurrency limits are not specified.
---
## Phụ lục đối chiếu nguồn Excel
- Workbook nguồn: `DD_API_Template(1).xlsx`
- Sheet nguồn: `Overview`
- Dimension: `A1:BA10`
- Trạng thái: `visible`
- Số ô có dữ liệu/công thức: `4`
- Số vùng merge: `0`

<details>
<summary>Bản ghi từng ô có dữ liệu hoặc công thức</summary>

| Hàng | Ô | Giá trị nguồn | Công thức nguồn |
|---:|---|---|---|
| 1 | `A1` | 【Khái quát】 |  |
| 3 | `B3` | Get thông tin…. |  |
| 5 | `A5` | 【Mục chú ý】 |  |
| 7 | `B7` | Không có |  |

</details>

---
title: "Data Mapping"
order: 5
dd_id: "91"
api_name: "Xem thống kê quiz"
source_sheet: "3. Data mapping"
format: markdown
status: "Draft — Needs Confirmation"
---

# Data Mapping

## Flow xử lý data

### Mục lục

1. [Step 0 — Authentication and authorization](#step-0-authentication-and-authorization)
2. [Step 1 — Read and aggregate](#step-1-read-and-aggregate)
3. [Step 2 — Map response](#step-2-map-response)
4. [Step 3 — Return result or catalog error](#step-3-return-result-or-catalog-error)

<a id="step-0-authentication-and-authorization"></a>

## Step 0 — Authentication and authorization

| Check | Source | Rule | Basis/status |
|---|---|---|---|
| Bearer token | API catalog #91 | Request phải có Bearer JWT | DIRECT |
| Role | API catalog #91 | Actor là Admin | DIRECT |
| Quiz permission | AC-35 | Admin có quiz-management permission | DIRECT intent; claim/policy SOURCE_REQUIRED |
| Current guard | Study router/auth source | Chưa có Admin guard hoặc route #91 | CURRENT_BEHAVIOR: UNWIRED / NOT_FOUND |

- Authorize trước khi đọc quiz/attempt data.
- Không nhận user_id/role từ request và không dùng Student guard thay Admin policy.

<a id="step-1-read-and-aggregate"></a>

## Step 1 — Read and aggregate

### Request usage matrix

| Request item | Source/use | Query/response use | Rule/status |
|---|---|---|---|
| Authorization | Header | Authenticate Bearer; authorize Admin | Role DIRECT; permission mapping SOURCE_REQUIRED |
| quiz_id | Required path int64 | quizzes.id predicate; quiz_attempts.quiz_id join | Type DIRECT; schema candidate |
| Body | None | None | DIRECT |
| Query | None | None | DIRECT |

### Q1 — Candidate aggregate query

> Logical PostgreSQL candidate over legacy design only; live schema and runtime query are unverified.

~~~sql
SELECT
    q.id AS quiz_id,
    q.passing_score,
    COUNT(a.id)::bigint AS attempt_count,
    COUNT(a.submitted_at)::bigint AS submitted_attempt_count,
    COUNT(a.score)::bigint AS graded_attempt_count,
    AVG(a.score) AS average_score,
    CASE
        WHEN q.passing_score IS NULL THEN NULL
        ELSE COUNT(a.id) FILTER (
            WHERE a.score IS NOT NULL AND a.score >= q.passing_score
        )::bigint
    END AS passed_attempt_count,
    CASE
        WHEN q.passing_score IS NULL OR COUNT(a.score) = 0 THEN NULL
        ELSE 100.0 * COUNT(a.id) FILTER (
            WHERE a.score IS NOT NULL AND a.score >= q.passing_score
        ) / NULLIF(COUNT(a.score), 0)
    END AS pass_rate_percent
FROM quizzes AS q
LEFT JOIN quiz_attempts AS a ON a.quiz_id = q.id
WHERE q.id = :quiz_id
GROUP BY q.id, q.passing_score;
~~~

### Q1 source and predicate matrix

| Query | Type | Candidate source | Column/expression | Predicate/transform | Purpose/status |
|---|---|---|---|---|---|
| Q1 | SELECT | quizzes q | q.id | q.id = :quiz_id | Existence and quiz ID; legacy candidate. |
| Q1 | SELECT | quizzes q | q.passing_score | GROUP BY q.id, q.passing_score | Pass threshold; nullable DDL discrepancy. |
| Q1 | LEFT JOIN | quiz_attempts a | a.quiz_id = q.id | Include linked rows | Candidate 1:N relation; live FK unverified. |
| Q1 | COUNT | quiz_attempts a | a.id | COUNT(a.id) | All linked attempts; zero if none. |
| Q1 | COUNT | quiz_attempts a | a.submitted_at | COUNT(non-NULL) | Submitted signal; not status enum. |
| Q1 | COUNT/AVG | quiz_attempts a | a.score | COUNT and AVG non-NULL | Graded count and average candidate. |
| Q1 | FILTER | a.score, q.passing_score | score >= threshold | Require both non-NULL | Passed count candidate. |
| Q1 | FILTER | aggregate | passed / graded × 100 | Threshold non-NULL; denominator > 0 | Pass percentage candidate. |
| Q1 | WHERE | quizzes q | q.id | No row → candidate 404 | Exact 404 code is DIRECT. |
| Q1 | FILTER | quizzes q | No status predicate | Include retained tombstone row | DERIVED history proposal. |
| Q1 | FILTER | quiz_attempts a | No status predicate | Include every status string | DERIVED; enum incomplete. |
| Q1 | READ | quiz_answers | None | No answer-level query | Not required for attempt-level stats. |

- LEFT JOIN giữ quiz chưa có attempt; COUNT(a.id) tránh đếm row giả của join.
- PENDING_GRADE có thể đã submitted nhưng score vẫn NULL; đề xuất submitted tăng, graded/average không tăng.
- Không coi score NULL là 0; average không có mẫu trả NULL.
- Attempt có quiz_id NULL/orphan không join được; guide và DDL khác nullability, live constraint chưa xác minh.
- Tombstone không bị lọc để giữ statistics history theo proposal; không có quiz row thì 404.
- Không query status, answers, user IDs, pagination, date range hoặc per-student breakdown.

### Query outcome matrix

| Outcome | Proposed result | Status |
|---|---|---|
| Quiz có 0 attempt | Counts 0; average NULL; passed count 0 nếu threshold biết; rate NULL | DERIVED |
| Quiz có attempts | Aggregate các row liên kết | DERIVED |
| passing_score NULL | Passed count/rate NULL | DERIVED |
| Quiz row không tồn tại | 404 DESIGN_RESOURCE_NOT_FOUND | Code DIRECT; interpretation DERIVED |
| Query/mapping failure | 500 DESIGN_INTERNAL_ERROR | Code DIRECT; route chưa có |

<a id="step-2-map-response"></a>

## Step 2 — Map response

### Direct Quiz response source matrix

| Field | Candidate source | Mapping/null rule | Status |
|---|---|---|---|
| data.id | quizzes.id | Direct ID | Legacy candidate |
| data.course_id | quizzes.course_id | Logical required; DDL permits NULL | DISCREPANCY |
| data.title | quizzes.name | name → title | Candidate |
| data.duration_minutes | quizzes.time_limit_minutes | Nullable optional alias | Candidate |
| data.passing_score | quizzes.passing_score | Numeric → decimal-string; DDL permits NULL | DISCREPANCY |
| data.questions[].id | quiz_questions.id | Direct candidate | Candidate |
| data.questions[].text | quiz_questions.question_text | question_text → text | Candidate |
| data.questions[].type | No legacy source | Do not map Pilot UUID value | SOURCE_REQUIRED |
| data.questions[].choices[] | quiz_choices | QuizChoice schema missing | SOURCE_REQUIRED |
| meta | Envelope | No pagination contract | Direct type; content unspecified |
| traceId | Request context | Propagate trace | Reusable envelope |

Direct Quiz schema cannot carry the proposed statistics and its nested projection has unresolved source fields. Do not fabricate fields or an empty question array in implementation.

### Proposed QuizStatistics response matrix — DERIVED

| Field | Candidate source/expression | Rule | Status |
|---|---|---|---|
| data.quiz_id | quizzes.id | Echo matched quiz ID | DERIVED |
| data.attempt_count | COUNT(quiz_attempts.id) | All linked attempts | DERIVED |
| data.submitted_attempt_count | COUNT(submitted_at) | submitted_at non-NULL | DERIVED |
| data.graded_attempt_count | COUNT(score) | score non-NULL | DERIVED |
| data.average_score | AVG(score) | NULL with no scored attempt; decimal scale open | DERIVED |
| data.passed_attempt_count | score >= passing_score | NULL if threshold missing | DERIVED |
| data.pass_rate_percent | passed / graded × 100 | NULL if threshold missing or graded=0 | DERIVED |
| meta | Envelope | No page fields | DERIVED content |
| traceId | Request context | Propagate request trace | Reusable envelope |

### Mutation matrix

| Operation | Target | Condition | Fields | Status |
|---|---|---|---|---|
| None | N/A | Read-only statistics | No INSERT/UPDATE/DELETE | N/A — READ-ONLY API |

<a id="step-3-return-result-or-catalog-error"></a>

## Step 3 — Return result or catalog error

- Direct success contract: HTTP 200 DESIGN_RESOURCE_RETRIEVED, ApiEnvelope<Quiz>.
- AC-35 statistics requires a schema change or approved response decision before implementation; QuizStatistics remains a separate proposal.
- Error set is exactly 401/403/404/500 with catalog DESIGN_* codes.
- Current helper/middleware do not prove #91 behavior because no route is registered.
- Không trả SQL, answer rows, answer key hoặc Student identifiers.
---
## Phụ lục đối chiếu nguồn Excel
- Workbook nguồn: `DD_API_Template(1).xlsx`
- Sheet nguồn: `3. Data mapping`
- Dimension: `B1:BB61`
- Trạng thái: `visible`
- Số ô có dữ liệu/công thức: `63`
- Số vùng merge: `0`

<details>
<summary>Bản ghi từng ô có dữ liệu hoặc công thức</summary>

| Hàng | Ô | Giá trị nguồn | Công thức nguồn |
|---:|---|---|---|
| 2 | `B2` | Flow xử lý data |  |
| 4 | `D4` | 0. |  |
| 4 | `E4` | Check quyền |  |
| 5 | `E5` | ・ |  |
| 5 | `F5` | Thực hiện check quyền |  |
| 6 | `E6` | ・ |  |
| 6 | `F6` | Get count khi get data từ … |  |
| 7 | `G7` | Table get |  |
| 7 | `K7` | : |  |
| 8 | `G8` | Conditions |  |
| 8 | `K8` | : |  |
| 10 | `E10` | ・ |  |
| 10 | `F10` | Trường hợp giá trị get được lớn hơn 0, thực hiện các xử lý tiếp theo |  |
| 11 | `E11` | ・ |  |
| 11 | `F11` | Trường hợp giá trị get được bằng 0, trả về status 2 |  |
| 13 | `D13` | 1. |  |
| 13 | `E13` | validate data input |  |
| 14 | `F14` | refer sheet [４．Error] |  |
| 16 | `D16` | 2. |  |
| 16 | `E16` | Get thông tin… |  |
| 18 | `F18` | Table get |  |
| 18 | `K18` | Column get |  |
| 18 | `P18` | Chú thích |  |
| 18 | `U18` | Remarks |  |
| 29 | `F29` | Target table / join condition |  |
| 30 | `F30` | Target table |  |
| 30 | `N30` | Join condition |  |
| 30 | `AL30` | 結合種類 |  |
| 31 | `F31` | txn_ams_t0320 AS a |  |
| 32 | `F32` | txn_amm_v0002 AS b |  |
| 32 | `N32` | ON a . chy_typ = b . kbn_typ AND b . dmin_cd = A AND b . kbnknr_cd = 001 |  |
| 32 | `AL32` | LEFT JOIN |  |
| 33 | `F33` | txn_amm_v0002 AS c |  |
| 33 | `N33` | ON a . chy_typ = c . kbn_typ AND c . dmin_cd = A AND c . kbnknr_cd = Z02 |  |
| 33 | `AL33` | LEFT JOIN |  |
| 35 | `F35` | ・ |  |
| 35 | `G35` | Điều kiện get data |  |
| 37 | `F37` | ・ |  |
| 37 | `G37` | Điều kiện sort |  |
| 41 | `D41` | 3. |  |
| 41 | `E41` | Insert/Update thông tin … |  |
| 42 | `E42` | Update table…. |  |
| 43 | `E43` | ・ |  |
| 43 | `F43` | Items update |  |
| 44 | `F44` | ・ |  |
| 44 | `G44` | Refer sheet [xxxx] |  |
| 45 | `E45` | ・ |  |
| 45 | `F45` | Điều kiện get data |  |
| 46 | `F46` | ・ |  |
| 46 | `G46` | auth_user. id = user hiện tại theo token |  |
| 48 | `D48` | 4. |  |
| 48 | `E48` | check kết quả execute query  |  |
| 49 | `E49` | 1. Thành công |  |
| 50 | `F50` | HTTPStatus = 200 |  |
| 51 | `F51` | Trả về kết quả status = 1 |  |
| 52 | `E52` | 2. Lỗi hệ thống phát sinh |  |
| 53 | `F53` | HTTPStatus = 500 |  |
| 54 | `F54` | Trả về kết quả status = 2 |  |
| 55 | `E55` | 3. Validate lỗi |  |
| 56 | `F56` | HTTPStatus = 400 |  |
| 57 | `F57` | Trả về kết quả status = 2 |  |
| 58 | `E58` | 4. Ngoài trường hợp trên |  |
| 59 | `F59` | Trả về kết quả status = 2 |  |

</details>

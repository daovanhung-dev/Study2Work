# PLAN_RESULT

## API result

| Thuộc tính | Giá trị |
|---|---|
| API ID | 21 |
| API name | Lấy tiến độ tổng hợp |
| Endpoint | GET /api/v1/users/me/progress |
| Document status | Draft — Needs Confirmation |
| Completion status | PARTIALLY COMPLETED |
| Decision status | NEEDS USER DECISION |
| Output folder | apps/study-server/docs/dd/21_users_me_progress/ |
| Basis | DIRECT — approved design contract + AC-13/AC-18 + checked-in DB design |
| Runtime status | UNWIRED / NOT_FOUND — chưa có route/module/query/test API #21 |
| Tables read | lesson_progress; lessons/courses relationship evidence — DESIGN_ONLY |
| Tables write | N/A — read-only |
| Business code delta | N/A — giữ nguyên codes đã có trong catalog |
| Packaging | Markdown folder only; Study workflow không yêu cầu ZIP |

## Sources

- [list_api.md](../../../../../docs/lists/list_api.md) — API #21 request/response/status/error contract and reusable schemas.
- [00_AC_API_INDEX.md](../../diagrams/AC_UNICA/00_AC_API_INDEX.md) — API mapping for AC-13/AC-18.
- [AC_02_STUDENT_LEARNING.drawio](../../diagrams/AC_UNICA/AC_02_STUDENT_LEARNING.drawio) — AC-13 client merge; AC-18 aggregate, API #37 detail and API #38 achievements.
- [DB_UNICA_TABLES.md](../../diagrams/DB_UNICA_TABLES.md) — lesson_progress design query and table relationships.
- [DB.sql](../../../../../infra/postgres/study-server/DB.sql) — checked-in DDL, not live database proof.
- [v1.py](../../../app/api/v1.py), [auth.py](../../../app/utils/auth.py), [responses.py](../../../app/core/responses.py) — current route/auth/envelope source; API #21 is absent.
- [OPEN_QUESTIONS.md](./OPEN_QUESTIONS.md) — unresolved query, aggregate, response, identity and empty-result questions.

## Locked decisions

- Endpoint, Student Bearer JWT requirement, raw query phrase, response type and 200/401/403/500 business codes match the catalog.
- AC-13 keeps API #20 and #21 separate; client merges Course + progress.
- AC-18 keeps API #37 course detail and API #38 achievements as separate calls.
- Use lesson_progress as design evidence only; do not invent query projection, aggregation formula, ownership predicate or empty response shape.
- Include eight template sheets and the three reports; 07_table.md is N/A — READ-ONLY API.
- No runtime, API catalog, diagram, DB schema or migration changes; no ZIP.

## Open gaps

- Query grammar and type/optionality: [Q-21-01](./OPEN_QUESTIONS.md#q-21-01).
- Aggregate source, scope and formula: [Q-21-02](./OPEN_QUESTIONS.md#q-21-02).
- UserProfile versus progress payload: [Q-21-03](./OPEN_QUESTIONS.md#q-21-03).
- JWT subject to progress ownership binding: [Q-21-04](./OPEN_QUESTIONS.md#q-21-04).
- Empty progress/no-enrollment wire shape: [Q-21-05](./OPEN_QUESTIONS.md#q-21-05).

## Verification result

- Static DD structure, request/response contract, code examples and relative links are recorded in [VERIFICATION_REPORT.md](./VERIFICATION_REPORT.md).
- Runtime tests: NOT_RUN — documentation-only scope and API #21 is not wired.
- Context validator: NOT_REQUIRED — no canonical context page or manifest changed.

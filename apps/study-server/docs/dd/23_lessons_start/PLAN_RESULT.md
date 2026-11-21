# PLAN_RESULT

## API result

| Thuộc tính | Giá trị |
|---|---|
| API ID | 23 |
| API name | Khởi tạo/lưu lần bắt đầu học |
| Endpoint | POST /api/v1/lessons/{lesson_id}/start |
| Document status | Draft — Needs Confirmation |
| Completion status | PARTIALLY COMPLETED |
| Decision status | NEEDS CONFIRMATION |
| Output folder | apps/study-server/docs/dd/23_lessons_start/ |
| Basis | DIRECT — API catalog + AC-14; checked-in DB schema is design evidence |
| Runtime status | UNWIRED / NOT_FOUND — chưa có route/module/query/focused test API #23 |
| Tables read | lessons, lesson_progress — candidate design only; query chưa xác nhận |
| Tables write | lesson_progress — AC-14 says UPSERT status IN_PROGRESS; exact mapping unresolved |
| Business code delta | N/A — giữ nguyên codes catalog |
| Packaging | Markdown folder only; no ZIP per Study Server workflow |

## Sources

- [list_api.md](../../../../../docs/lists/list_api.md) — API #23 contract, reusable Lesson and ApiEnvelope schemas.
- [00_AC_API_INDEX.md](../../diagrams/AC_UNICA/00_AC_API_INDEX.md) — AC-14 actor, precondition, postcondition and endpoint sequence.
- [AC_02_STUDENT_LEARNING.drawio](../../diagrams/AC_UNICA/AC_02_STUDENT_LEARNING.drawio) — API #23 and UPSERT lesson progress = IN_PROGRESS.
- [DB_UNICA_TABLES.md](../../diagrams/DB_UNICA_TABLES.md) and [DB.sql](../../../../../infra/postgres/study-server/DB.sql) — candidate lesson/progress schema; live schema not verified.
- [v1.py](../../../app/api/v1.py) and Study source/tests — current route/module/query/test inventory.
- [OPEN_QUESTIONS.md](./OPEN_QUESTIONS.md) — persistence, repeated-start, response, access, error and transaction decisions.

## Locked decisions

- Giữ method, endpoint, Student Bearer JWT, lesson_id:int64!, ApiEnvelope<Lesson> và các mã 201/401/403/404/422/500 theo catalog.
- Ghi UPSERT status IN_PROGRESS theo AC-14; không tự chọn conflict key, extra updated columns, timestamp, state preservation hoặc transaction.
- Checked-in DDL và ERD chỉ là design evidence; không khẳng định live schema.
- Giữ API #22 access, API #23 start, API #24 lesson detail và API #25 progress update là các API riêng.
- Tách expected/current behavior; runtime API #23 là UNWIRED / NOT_FOUND.
- Tạo đủ 8 sheet và 3 report; không tạo ZIP theo Study Server workflow.

## Open gaps

- UPSERT key/uniqueness and concurrent-start behavior: [Q-23-01](./OPEN_QUESTIONS.md#q-23-01).
- Fields, state transition and preservation: [Q-23-02](./OPEN_QUESTIONS.md#q-23-02).
- Repeat call, idempotency and HTTP 201 semantics: [Q-23-03](./OPEN_QUESTIONS.md#q-23-03).
- ApiEnvelope<Lesson> versus diagram payload and response source: [Q-23-04](./OPEN_QUESTIONS.md#q-23-04).
- Direct-call access, enrollment/prerequisite and 403: [Q-23-05](./OPEN_QUESTIONS.md#q-23-05).
- 404 and 422 semantics: [Q-23-06](./OPEN_QUESTIONS.md#q-23-06).
- Transaction/failure behavior and live schema: [Q-23-07](./OPEN_QUESTIONS.md#q-23-07).

## Verification result

- Template fingerprints, artifact structure, examples, links and contract checks are recorded in [VERIFICATION_REPORT.md](./VERIFICATION_REPORT.md).
- Application tests: NOT_RUN — documentation-only scope and API #23 is not wired.
- Context validator: NOT_REQUIRED — no canonical context page or manifest changed.

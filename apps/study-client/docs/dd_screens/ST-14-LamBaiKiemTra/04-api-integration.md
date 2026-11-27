# ST-14 — API Integration

> API/status dưới đây lấy từ inventory và DD nguồn. Package-local API IDs chỉ là alias truy vết cho API catalog reference; chúng không tạo contract mới. `R/S/D/M/UX` hoặc nhãn cục bộ là evidence status, không tự động xác nhận UI/runtime. Route/contract thiếu nguồn phải giữ `CẦN_XÁC_NHẬN`.

## Current caller status — 2026-11-27

ST-14 calls #28 for quiz/question details and #30 after a choice change; ST-13
owns #29 in current source. ST-14 follows both route IDs, cancels stale #28
reads, serializes #30 writes, validates exact business code and attempt
identity/state/answer response, and uses the API's returned answer set as the
current client state. #30's body uses `choice_ids[]`, while catalog says
`answer(s):string`; this remains a discrepancy. No GET attempt/answers endpoint
or authoritative timer exists, so reload cannot restore answers and no
countdown is run. The focused client service spec verifies #28/#30 path/body
mapping; the routed page spec verifies quiz load/retry, no #29 creation in this
screen, pending/success response handling, and rollback after a mismatched
attempt response. The full local Study Web suite passes 91 spec files/325 tests.
These are mocked/local checks; browser, live API, database, and deployment
behavior remain unverified. The original DD excerpt below remains expected
design evidence and is not reconciled to current source behavior.

## 1. API usage matrix
| API ID (package-local usage alias) | Source catalog ref | Method/path | Event | Auth |
|---|---|---|---|---|
| `ST-14-API-001` | #28 | See source contract excerpt | Source event IDs are preserved in [Events](02-events.md) | See source auth/permission evidence |
| `ST-14-API-002` | #29 | See source contract excerpt | Source event IDs are preserved in [Events](02-events.md) | See source auth/permission evidence |
| `ST-14-API-003` | #30 | See source contract excerpt | Source event IDs are preserved in [Events](02-events.md) | See source auth/permission evidence |

## 2. Contract / source detail

- API refs trong inventory: #28, #29, #30
- Orchestration/data notes: current ST-14 calls #28 and #30; ST-13 calls #29 after explicit Start. Expected design still lists #29 in the ST-14 flow and remains unresolved.
- BE/source status and gate: **DD BLOCKED; IMPLEMENTATION PARTIAL; RUNTIME NOT VERIFIED:** no answer restore/timer; catalog/body mismatch remains; #28/#29 lack enrollment and quiz-open checks; screen design claims beyond current API source remain unsupported.
- Contract sources and discrepancies are preserved in the source excerpts below.

### Trích từ DD nguồn: A.4. API contract liên quan

| API | Contract catalog | Request/response và lỗi | Bằng chứng current runtime |
|---|---|---|---|
| #28 | `GET /api/v1/quizzes/{quiz_id}`; Student Bearer; `path{quiz_id:int64!}`; source `QuizDetail`. | Study Server route/view/query/model and ST-14 caller exist. | Checks Student role; current query returns quiz/questions without enrollment or quiz-status eligibility. |
| #29 | `POST /api/v1/quizzes/{quiz_id}/attempts`; Student Bearer; no body/query; source `QuizAttemptDetail`. | Study Server route/view/query/model and ST-13 caller exist; not called from ST-14. | Creates and commits an `IN_PROGRESS` attempt; checks existing active attempt; does not check course enrollment or quiz published/open state. |
| #30 | `PUT /api/v1/attempts/{attempt_id}/answers`; Student Bearer; current request supports `question_id` and `choice_ids[]` (catalog says `answer(s):string`). | Study Server route/view/query/model and ST-14 caller exist. | Checks attempt owner/status and question/choice membership; replaces that question's choice rows in a transaction and returns all stored answers. |
| #31/#32 | #31 POST submit, #32 GET result theo inventory/API catalog; nằm ở ST-15/ST-16. | #31 có 200/401/403/404/422/409/500; #32 có 200/401/403/404/500. Không gọi ở ST-14. | Student runtime source không có các endpoint này. |

## 3. API không sử dụng
- Không bổ sung API ngoài inventory và DD nguồn. Nếu screen không cần API, trạng thái phải được xác nhận từ source DD.

## 4. References
[Events](02-events.md) · [Data flow](03-data-flow.md) · [Tests](07-test-cases.md) · [Source DD](../../screen_stitch/03_student/ST-14_lam-bai-kiem-tra/ST-14.md)

# Overview - LEARN-PROGRESS-001

| Field | Value |
|---|---|
| API code | `LEARN-PROGRESS-001` |
| API name | `Record start, position or completion event for a lesson` |
| Module | `LEARNING` |
| Method | `POST` |
| Endpoint | `/api/v1/lessons/{lessonId}/progress` |
| Primary actor | `Student` |
| Caller app | `Study client phù hợp với actor Student` |
| Auth scheme | `Bearer JWT.` |
| Permission | `learn.learn.progress` |
| Status | `DRAFT` |
| Version | `v0.1` |
| Updated | `2026-07-02` |

## Business Goal

API này dùng để record start, position or completion event for a lesson.. Bản DD này là draft từ BD, API checklist và diagrams; chi tiết chưa đủ nguồn được ghi thành `OPEN_QUESTION`.

## Study Scope

In scope:

- Thực hiện đúng capability Study của module `LEARNING` cho actor `Student`.
- Tuân thủ rule/focus: Enforce `BR-LEARN-002`; server-side completion threshold; no client-forced completion.
- Trả response envelope chuẩn có `businessCode`, `timestamp`, `traceId`, `data` hoặc `errors`.

Out of scope:

- Employer, recruitment, job, CV, interview, matching, shortlist, offer và hiring workflows.
- Bất kỳ contract nào chưa có trong BD/checklist hoặc chưa được review trong DD này.

## Source Trace

| Source | Link / ID | Note |
|---|---|---|
| BD | `docs/BD/Study2Work_Study_BD_Codex_Ready.md` | Sections 5.2, 10.4, business rules và API catalogue. |
| API checklist | `docs/checklists/API.md` | `LEARN-PROGRESS-001` canonical row. |
| Activity diagram | `docs/diagrams/02_activity/06_Tien_do_bookmark_comment_live.puml` | Flow hành vi liên quan. |
| Sequence diagram | `docs/diagrams/04_sequence/06_Lesson_Progress.puml` | Tương tác runtime liên quan. |
| Class diagram | `docs/diagrams/03_class/02_Learning_Journey.puml` | Aggregate/read model liên quan. |
| Architecture | `docs/architecture/PROJECT_ARCHITECTURE.md` | Server/client boundary và API DD gate. |

## Preconditions

- DD đang ở trạng thái `DRAFT`, chưa được phê duyệt để implement official business API.
- Caller đáp ứng auth scheme và permission nếu endpoint không public.
- Resource liên quan tồn tại và nằm trong ownership/scope của actor.

## Postconditions

- Thành công: response trả envelope với `businessCode` `LEARN-PROGRESS-001-SUCCESS`.
- Nếu có ghi dữ liệu, transaction chỉ commit khi validation, authorization và business rule đều pass.
- Failed requests must not create partial business state unless explicitly documented.

## Authorization And Scope

| Actor | Permission | Ownership/scope rule |
|---|---|---|
| `Student` | `learn.learn.progress` | Actor chỉ được xem/ghi dữ liệu của chính mình hoặc scope học tập/team được cấp quyền. |

## Data Ownership

| Table / aggregate | Read | Write | Owner module | Note |
|---|---:|---:|---|---|
| `learning_progress` | Y | Y | `LEARNING` | Lấy từ API checklist và BD data dictionary. |
| `audit_log` | Y | Y | `LEARNING` | Lấy từ API checklist và BD data dictionary. |

## Events And Async Work

| Event/job | When emitted | Delivery | Consumer | Retry rule |
|---|---|---|---|---|
| `LessonStarted` | Sau khi transaction nguồn commit. | after_commit/outbox/Celery | Consumer liên quan. | Retry theo worker/outbox policy. |
| `LessonCompleted` | Sau khi transaction nguồn commit. | after_commit/outbox/Celery | Consumer liên quan. | Retry theo worker/outbox policy. |

## Open Questions

| ID | Owner | Status | Question |
|---|---|---|---|
| LEARN-PROGRESS-001-OQ-001 | BA/PO + Tech Lead | OPEN | Xác nhận schema request/response chi tiết trước khi chuyển DD sang IN_REVIEW hoặc APPROVED. |

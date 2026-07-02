# Overview - LEARN-LESSON-001

| Field | Value |
|---|---|
| API code | `LEARN-LESSON-001` |
| API name | `Read an unlocked lesson and its content` |
| Module | `LEARNING` |
| Method | `GET` |
| Endpoint | `/api/v1/lessons/{lessonId}` |
| Primary actor | `Student` |
| Caller app | `Study client phù hợp với actor Student` |
| Auth scheme | `Bearer JWT.` |
| Permission | `learn.learn.lesson` |
| Status | `DRAFT` |
| Version | `v0.1` |
| Updated | `2026-07-02` |

## Business Goal

API này dùng để read an unlocked lesson and its content.. Bản DD này là draft từ BD, API checklist và diagrams; chi tiết chưa đủ nguồn được ghi thành `OPEN_QUESTION`.

## Study Scope

In scope:

- Thực hiện đúng capability Study của module `LEARNING` cho actor `Student`.
- Tuân thủ rule/focus: Enforce `BR-LEARN-001`; enrollment ownership and unlock rule; no draft content to student.
- Trả response envelope chuẩn có `businessCode`, `timestamp`, `traceId`, `data` hoặc `errors`.

Out of scope:

- Employer, recruitment, job, CV, interview, matching, shortlist, offer và hiring workflows.
- Bất kỳ contract nào chưa có trong BD/checklist hoặc chưa được review trong DD này.

## Source Trace

| Source | Link / ID | Note |
|---|---|---|
| BD | `docs/BD/Study2Work_Study_BD_Codex_Ready.md` | Sections 5.2, 10.4, business rules và API catalogue. |
| API checklist | `docs/checklists/API.md` | `LEARN-LESSON-001` canonical row. |
| Activity diagram | `docs/diagrams/02_activity/05_Enroll_va_hoc_lesson.puml` | Flow hành vi liên quan. |
| Sequence diagram | `docs/diagrams/04_sequence/06_Lesson_Progress.puml` | Tương tác runtime liên quan. |
| Class diagram | `docs/diagrams/03_class/02_Learning_Journey.puml` | Aggregate/read model liên quan. |
| Architecture | `docs/architecture/PROJECT_ARCHITECTURE.md` | Server/client boundary và API DD gate. |

## Preconditions

- DD đang ở trạng thái `DRAFT`, chưa được phê duyệt để implement official business API.
- Caller đáp ứng auth scheme và permission nếu endpoint không public.
- Resource liên quan tồn tại và nằm trong ownership/scope của actor.

## Postconditions

- Thành công: response trả envelope với `businessCode` `LEARN-LESSON-001-SUCCESS`.
- Nếu có ghi dữ liệu, transaction chỉ commit khi validation, authorization và business rule đều pass.
- Failed requests must not create partial business state unless explicitly documented.

## Authorization And Scope

| Actor | Permission | Ownership/scope rule |
|---|---|---|
| `Student` | `learn.learn.lesson` | Actor chỉ được xem/ghi dữ liệu của chính mình hoặc scope học tập/team được cấp quyền. |

## Data Ownership

| Table / aggregate | Read | Write | Owner module | Note |
|---|---:|---:|---|---|
| `lesson` | Y | N | `LEARNING` | Lấy từ API checklist và BD data dictionary. |
| `lesson_content` | Y | N | `LEARNING` | Lấy từ API checklist và BD data dictionary. |
| `learning_path_enrollment` | Y | N | `LEARNING` | Lấy từ API checklist và BD data dictionary. |
| `learning_progress` | Y | N | `LEARNING` | Lấy từ API checklist và BD data dictionary. |

## Events And Async Work

| Event/job | When emitted | Delivery | Consumer | Retry rule |
|---|---|---|---|---|
| `none` | Không có event/job bắt buộc trong source hiện tại. | N/A | N/A | Không retry. |

## Open Questions

| ID | Owner | Status | Question |
|---|---|---|---|
| LEARN-LESSON-001-OQ-001 | BA/PO + Tech Lead | OPEN | Xác nhận schema request/response chi tiết trước khi chuyển DD sang IN_REVIEW hoặc APPROVED. |

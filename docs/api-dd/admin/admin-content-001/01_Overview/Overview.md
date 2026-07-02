# Overview - ADMIN-CONTENT-001

| Field | Value |
|---|---|
| API code | `ADMIN-CONTENT-001` |
| API name | `Create or modify the learning content tree` |
| Module | `ADMIN` |
| Method | `POST` |
| Endpoint | `/api/v1/admin/learning-paths` |
| Primary actor | `Admin` |
| Caller app | `Study client phù hợp với actor Admin` |
| Auth scheme | `Bearer JWT.` |
| Permission | `admin.admin.content` |
| Status | `DRAFT` |
| Version | `v0.1` |
| Updated | `2026-07-02` |

## Business Goal

API này dùng để create or modify the learning content tree.. Bản DD này là draft từ BD, API checklist và diagrams; chi tiết chưa đủ nguồn được ghi thành `OPEN_QUESTION`.

## Study Scope

In scope:

- Thực hiện đúng capability Study của module `ADMIN` cho actor `Admin`.
- Tuân thủ rule/focus: Enforce `BR-ADMIN-001`; content publish state, audit, no student access to draft content.
- Trả response envelope chuẩn có `businessCode`, `timestamp`, `traceId`, `data` hoặc `errors`.

Out of scope:

- Employer, recruitment, job, CV, interview, matching, shortlist, offer và hiring workflows.
- Bất kỳ contract nào chưa có trong BD/checklist hoặc chưa được review trong DD này.

## Source Trace

| Source | Link / ID | Note |
|---|---|---|
| BD | `docs/BD/Study2Work_Study_BD_Codex_Ready.md` | Sections 5.7, 10.4, business rules và API catalogue. |
| API checklist | `docs/checklists/API.md` | `ADMIN-CONTENT-001` canonical row. |
| Activity diagram | `docs/diagrams/02_activity/16_Admin_content_rubric_publish.puml` | Flow hành vi liên quan. |
| Sequence diagram | `docs/diagrams/04_sequence/19_Admin_Content_Rubric.puml` | Tương tác runtime liên quan. |
| Class diagram | `docs/diagrams/03_class/06_Platform_Community_Notification_Admin.puml` | Aggregate/read model liên quan. |
| Architecture | `docs/architecture/PROJECT_ARCHITECTURE.md` | Server/client boundary và API DD gate. |

## Preconditions

- DD đang ở trạng thái `DRAFT`, chưa được phê duyệt để implement official business API.
- Caller đáp ứng auth scheme và permission nếu endpoint không public.
- Resource liên quan tồn tại và nằm trong ownership/scope của actor.

## Postconditions

- Thành công: response trả envelope với `businessCode` `ADMIN-CONTENT-001-SUCCESS`.
- Nếu có ghi dữ liệu, transaction chỉ commit khi validation, authorization và business rule đều pass.
- Failed requests must not create partial business state unless explicitly documented.

## Authorization And Scope

| Actor | Permission | Ownership/scope rule |
|---|---|---|
| `Admin` | `admin.admin.content` | Admin phải có permission phù hợp; mọi thao tác nhạy cảm phải có audit. |

## Data Ownership

| Table / aggregate | Read | Write | Owner module | Note |
|---|---:|---:|---|---|
| `learning_path` | Y | Y | `ADMIN` | Lấy từ API checklist và BD data dictionary. |
| `module` | Y | Y | `ADMIN` | Lấy từ API checklist và BD data dictionary. |
| `lesson` | Y | Y | `ADMIN` | Lấy từ API checklist và BD data dictionary. |
| `audit_log` | Y | Y | `ADMIN` | Lấy từ API checklist và BD data dictionary. |

## Events And Async Work

| Event/job | When emitted | Delivery | Consumer | Retry rule |
|---|---|---|---|---|
| `LearningContentPublished` | Sau khi transaction nguồn commit. | after_commit/outbox/Celery | Consumer liên quan. | Retry theo worker/outbox policy. |

## Open Questions

| ID | Owner | Status | Question |
|---|---|---|---|
| ADMIN-CONTENT-001-OQ-001 | BA/PO + Tech Lead | OPEN | Xác nhận schema request/response chi tiết trước khi chuyển DD sang IN_REVIEW hoặc APPROVED. |
| ADMIN-CONTENT-001-OQ-003 | BA/PO | OPEN | Xác nhận điều kiện phát sinh side effect tùy chọn trong flow này. |

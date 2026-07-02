# Overview - PROJECT-TEAM-002

| Field | Value |
|---|---|
| API code | `PROJECT-TEAM-002` |
| API name | `Join or add a team member according to policy` |
| Module | `PROJECT` |
| Method | `POST` |
| Endpoint | `/api/v1/teams/{teamId}/members` |
| Primary actor | `Student/Mentor` |
| Caller app | `Study client phù hợp với actor Student/Mentor` |
| Auth scheme | `Bearer JWT.` |
| Permission | `project.project.team` |
| Status | `DRAFT` |
| Version | `v0.1` |
| Updated | `2026-07-02` |

## Business Goal

API này dùng để join or add a team member according to policy.. Bản DD này là draft từ BD, API checklist và diagrams; chi tiết chưa đủ nguồn được ghi thành `OPEN_QUESTION`.

## Study Scope

In scope:

- Thực hiện đúng capability Study của module `PROJECT` cho actor `Student/Mentor`.
- Tuân thủ rule/focus: Enforce `BR-PROJECT-001`; duplicate membership and mentor scope checks.
- Trả response envelope chuẩn có `businessCode`, `timestamp`, `traceId`, `data` hoặc `errors`.

Out of scope:

- Employer, recruitment, job, CV, interview, matching, shortlist, offer và hiring workflows.
- Bất kỳ contract nào chưa có trong BD/checklist hoặc chưa được review trong DD này.

## Source Trace

| Source | Link / ID | Note |
|---|---|---|
| BD | `docs/BD/Study2Work_Study_BD_Codex_Ready.md` | Sections 5.4, 10.4, business rules và API catalogue. |
| API checklist | `docs/checklists/API.md` | `PROJECT-TEAM-002` canonical row. |
| Activity diagram | `docs/diagrams/02_activity/11_Project_team_join.puml` | Flow hành vi liên quan. |
| Sequence diagram | `docs/diagrams/04_sequence/13_Project_Team.puml` | Tương tác runtime liên quan. |
| Class diagram | `docs/diagrams/03_class/04_Project_Teamwork.puml` | Aggregate/read model liên quan. |
| Architecture | `docs/architecture/PROJECT_ARCHITECTURE.md` | Server/client boundary và API DD gate. |

## Preconditions

- DD đang ở trạng thái `DRAFT`, chưa được phê duyệt để implement official business API.
- Caller đáp ứng auth scheme và permission nếu endpoint không public.
- Resource liên quan tồn tại và nằm trong ownership/scope của actor.

## Postconditions

- Thành công: response trả envelope với `businessCode` `PROJECT-TEAM-002-SUCCESS`.
- Nếu có ghi dữ liệu, transaction chỉ commit khi validation, authorization và business rule đều pass.
- Failed requests must not create partial business state unless explicitly documented.

## Authorization And Scope

| Actor | Permission | Ownership/scope rule |
|---|---|---|
| `Student/Mentor` | `project.project.team` | Actor chỉ được xem/ghi dữ liệu của chính mình hoặc scope học tập/team được cấp quyền. |

## Data Ownership

| Table / aggregate | Read | Write | Owner module | Note |
|---|---:|---:|---|---|
| `team_member` | Y | Y | `PROJECT` | Lấy từ API checklist và BD data dictionary. |
| `audit_log` | Y | Y | `PROJECT` | Lấy từ API checklist và BD data dictionary. |

## Events And Async Work

| Event/job | When emitted | Delivery | Consumer | Retry rule |
|---|---|---|---|---|
| `TeamMemberJoined` | Sau khi transaction nguồn commit. | after_commit/outbox/Celery | Consumer liên quan. | Retry theo worker/outbox policy. |

## Open Questions

| ID | Owner | Status | Question |
|---|---|---|---|
| PROJECT-TEAM-002-OQ-001 | BA/PO + Tech Lead | OPEN | Xác nhận schema request/response chi tiết trước khi chuyển DD sang IN_REVIEW hoặc APPROVED. |

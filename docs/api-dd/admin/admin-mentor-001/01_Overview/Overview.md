# Overview - ADMIN-MENTOR-001

| Field | Value |
|---|---|
| API code | `ADMIN-MENTOR-001` |
| API name | `Assign mentor scope for learner/team/project review access` |
| Module | `ADMIN` |
| Method | `PATCH` |
| Endpoint | `/api/v1/admin/mentors/{mentorId}/scope` |
| Primary actor | `Admin` |
| Caller app | `Study client phù hợp với actor Admin` |
| Auth scheme | `Bearer JWT.` |
| Permission | `admin.admin.mentor` |
| Status | `DRAFT` |
| Version | `v0.1` |
| Updated | `2026-07-02` |

## Business Goal

API này dùng để assign mentor scope for learner/team/project review access.. Bản DD này là draft từ BD, API checklist và diagrams; chi tiết chưa đủ nguồn được ghi thành `OPEN_QUESTION`.

## Study Scope

In scope:

- Thực hiện đúng capability Study của module `ADMIN` cho actor `Admin`.
- Tuân thủ rule/focus: Enforce `BR-ADMIN-001`, mentor scope boundaries and audit.
- Trả response envelope chuẩn có `businessCode`, `timestamp`, `traceId`, `data` hoặc `errors`.

Out of scope:

- Employer, recruitment, job, CV, interview, matching, shortlist, offer và hiring workflows.
- Bất kỳ contract nào chưa có trong BD/checklist hoặc chưa được review trong DD này.

## Source Trace

| Source | Link / ID | Note |
|---|---|---|
| BD | `docs/BD/Study2Work_Study_BD_Codex_Ready.md` | Sections 5.7, 10.4, business rules và API catalogue. |
| API checklist | `docs/checklists/API.md` | `ADMIN-MENTOR-001` canonical row. |
| Activity diagram | `docs/diagrams/02_activity/15_Admin_user_mentor_scope.puml` | Flow hành vi liên quan. |
| Sequence diagram | `docs/diagrams/04_sequence/20_Admin_Mentor_Scope.puml` | Tương tác runtime liên quan. |
| Class diagram | `docs/diagrams/03_class/06_Platform_Community_Notification_Admin.puml` | Aggregate/read model liên quan. |
| Architecture | `docs/architecture/PROJECT_ARCHITECTURE.md` | Server/client boundary và API DD gate. |

## Preconditions

- DD đang ở trạng thái `DRAFT`, chưa được phê duyệt để implement official business API.
- Caller đáp ứng auth scheme và permission nếu endpoint không public.
- Resource liên quan tồn tại và nằm trong ownership/scope của actor.

## Postconditions

- Thành công: response trả envelope với `businessCode` `ADMIN-MENTOR-001-SUCCESS`.
- Nếu có ghi dữ liệu, transaction chỉ commit khi validation, authorization và business rule đều pass.
- Failed requests must not create partial business state unless explicitly documented.

## Authorization And Scope

| Actor | Permission | Ownership/scope rule |
|---|---|---|
| `Admin` | `admin.admin.mentor` | Admin phải có permission phù hợp; mọi thao tác nhạy cảm phải có audit. |

## Data Ownership

| Table / aggregate | Read | Write | Owner module | Note |
|---|---:|---:|---|---|
| `mentor_profile` | Y | Y | `ADMIN` | Lấy từ API checklist và BD data dictionary. |
| `audit_log` | Y | Y | `ADMIN` | Lấy từ API checklist và BD data dictionary. |

## Events And Async Work

| Event/job | When emitted | Delivery | Consumer | Retry rule |
|---|---|---|---|---|
| `none` | Không có event/job bắt buộc trong source hiện tại. | N/A | N/A | Không retry. |

## Open Questions

| ID | Owner | Status | Question |
|---|---|---|---|
| ADMIN-MENTOR-001-OQ-001 | BA/PO + Tech Lead | OPEN | Xác nhận schema request/response chi tiết trước khi chuyển DD sang IN_REVIEW hoặc APPROVED. |

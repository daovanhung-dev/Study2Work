# Overview - USER-PROFILE-002

| Field | Value |
|---|---|
| API code | `USER-PROFILE-002` |
| API name | `Update own profile fields and role-specific profile extension` |
| Module | `USER` |
| Method | `PATCH` |
| Endpoint | `/api/v1/me/profile` |
| Primary actor | `Student/Mentor` |
| Caller app | `Study client phù hợp với actor Student/Mentor` |
| Auth scheme | `Bearer JWT.` |
| Permission | `user.user.profile` |
| Status | `DRAFT` |
| Version | `v0.1` |
| Updated | `2026-07-02` |

## Business Goal

API này dùng để update own profile fields and role-specific profile extension.. Bản DD này là draft từ BD, API checklist và diagrams; chi tiết chưa đủ nguồn được ghi thành `OPEN_QUESTION`.

## Study Scope

In scope:

- Thực hiện đúng capability Study của module `USER` cho actor `Student/Mentor`.
- Tuân thủ rule/focus: Self-only update, whitelisted fields, PII classification, audit meaningful profile changes.
- Trả response envelope chuẩn có `businessCode`, `timestamp`, `traceId`, `data` hoặc `errors`.

Out of scope:

- Employer, recruitment, job, CV, interview, matching, shortlist, offer và hiring workflows.
- Bất kỳ contract nào chưa có trong BD/checklist hoặc chưa được review trong DD này.

## Source Trace

| Source | Link / ID | Note |
|---|---|---|
| BD | `docs/BD/Study2Work_Study_BD_Codex_Ready.md` | Sections 5.1, 10.4, business rules và API catalogue. |
| API checklist | `docs/checklists/API.md` | `USER-PROFILE-002` canonical row. |
| Activity diagram | `docs/diagrams/02_activity/03_Cap_nhat_ho_so_va_ky_nang_nen.puml` | Flow hành vi liên quan. |
| Sequence diagram | `docs/diagrams/04_sequence/03_Profile_Skills.puml` | Tương tác runtime liên quan. |
| Class diagram | `docs/diagrams/03_class/01_Identity_Profile.puml` | Aggregate/read model liên quan. |
| Architecture | `docs/architecture/PROJECT_ARCHITECTURE.md` | Server/client boundary và API DD gate. |

## Preconditions

- DD đang ở trạng thái `DRAFT`, chưa được phê duyệt để implement official business API.
- Caller đáp ứng auth scheme và permission nếu endpoint không public.
- Resource liên quan tồn tại và nằm trong ownership/scope của actor.

## Postconditions

- Thành công: response trả envelope với `businessCode` `USER-PROFILE-002-SUCCESS`.
- Nếu có ghi dữ liệu, transaction chỉ commit khi validation, authorization và business rule đều pass.
- Failed requests must not create partial business state unless explicitly documented.

## Authorization And Scope

| Actor | Permission | Ownership/scope rule |
|---|---|---|
| `Student/Mentor` | `user.user.profile` | Actor chỉ được xem/ghi dữ liệu của chính mình hoặc scope học tập/team được cấp quyền. |

## Data Ownership

| Table / aggregate | Read | Write | Owner module | Note |
|---|---:|---:|---|---|
| `profile` | Y | Y | `USER` | Lấy từ API checklist và BD data dictionary. |
| `student_profile` | Y | Y | `USER` | Lấy từ API checklist và BD data dictionary. |
| `mentor_profile` | Y | Y | `USER` | Lấy từ API checklist và BD data dictionary. |
| `audit_log` | Y | Y | `USER` | Lấy từ API checklist và BD data dictionary. |

## Events And Async Work

| Event/job | When emitted | Delivery | Consumer | Retry rule |
|---|---|---|---|---|
| `none` | Không có event/job bắt buộc trong source hiện tại. | N/A | N/A | Không retry. |

## Open Questions

| ID | Owner | Status | Question |
|---|---|---|---|
| USER-PROFILE-002-OQ-001 | BA/PO + Tech Lead | OPEN | Xác nhận schema request/response chi tiết trước khi chuyển DD sang IN_REVIEW hoặc APPROVED. |

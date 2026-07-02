# Overview - MENTOR-REVIEW-002

| Field | Value |
|---|---|
| API code | `MENTOR-REVIEW-002` |
| API name | `Update a draft or pending review before finalization` |
| Module | `MENTOR` |
| Method | `PATCH` |
| Endpoint | `/api/v1/reviews/{reviewId}` |
| Primary actor | `Mentor` |
| Caller app | `Study client phù hợp với actor Mentor` |
| Auth scheme | `Bearer JWT.` |
| Permission | `mentor.mentor.review` |
| Status | `DRAFT` |
| Version | `v0.1` |
| Updated | `2026-07-02` |

## Business Goal

API này dùng để update a draft or pending review before finalization.. Bản DD này là draft từ BD, API checklist và diagrams; chi tiết chưa đủ nguồn được ghi thành `OPEN_QUESTION`.

## Study Scope

In scope:

- Thực hiện đúng capability Study của module `MENTOR` cho actor `Mentor`.
- Tuân thủ rule/focus: Mentor assigned scope, review editable state, optimistic concurrency and immutable finalized review.
- Trả response envelope chuẩn có `businessCode`, `timestamp`, `traceId`, `data` hoặc `errors`.

Out of scope:

- Employer, recruitment, job, CV, interview, matching, shortlist, offer và hiring workflows.
- Bất kỳ contract nào chưa có trong BD/checklist hoặc chưa được review trong DD này.

## Source Trace

| Source | Link / ID | Note |
|---|---|---|
| BD | `docs/BD/Study2Work_Study_BD_Codex_Ready.md` | Sections 5.5, 10.4, business rules và API catalogue. |
| API checklist | `docs/checklists/API.md` | `MENTOR-REVIEW-002` canonical row. |
| Activity diagram | `docs/diagrams/02_activity/09_Mentor_review_skill_evidence.puml` | Flow hành vi liên quan. |
| Sequence diagram | `docs/diagrams/04_sequence/11_Mentor_Review.puml` | Tương tác runtime liên quan. |
| Class diagram | `docs/diagrams/03_class/03_Practice_Assessment.puml` | Aggregate/read model liên quan. |
| Architecture | `docs/architecture/PROJECT_ARCHITECTURE.md` | Server/client boundary và API DD gate. |

## Preconditions

- DD đang ở trạng thái `DRAFT`, chưa được phê duyệt để implement official business API.
- Caller đáp ứng auth scheme và permission nếu endpoint không public.
- Resource liên quan tồn tại và nằm trong ownership/scope của actor.

## Postconditions

- Thành công: response trả envelope với `businessCode` `MENTOR-REVIEW-002-SUCCESS`.
- Nếu có ghi dữ liệu, transaction chỉ commit khi validation, authorization và business rule đều pass.
- Failed requests must not create partial business state unless explicitly documented.

## Authorization And Scope

| Actor | Permission | Ownership/scope rule |
|---|---|---|
| `Mentor` | `mentor.mentor.review` | Mentor chỉ được xem/ghi dữ liệu trong scope được phân công. |

## Data Ownership

| Table / aggregate | Read | Write | Owner module | Note |
|---|---:|---:|---|---|
| `review` | Y | Y | `MENTOR` | Lấy từ API checklist và BD data dictionary. |
| `feedback` | Y | Y | `MENTOR` | Lấy từ API checklist và BD data dictionary. |
| `audit_log` | Y | Y | `MENTOR` | Lấy từ API checklist và BD data dictionary. |

## Events And Async Work

| Event/job | When emitted | Delivery | Consumer | Retry rule |
|---|---|---|---|---|
| `none` | Không có event/job bắt buộc trong source hiện tại. | N/A | N/A | Không retry. |

## Open Questions

| ID | Owner | Status | Question |
|---|---|---|---|
| MENTOR-REVIEW-002-OQ-001 | BA/PO + Tech Lead | OPEN | Xác nhận schema request/response chi tiết trước khi chuyển DD sang IN_REVIEW hoặc APPROVED. |

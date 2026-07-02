# Overview - AUTH-REGISTER-001

| Field | Value |
|---|---|
| API code | `AUTH-REGISTER-001` |
| API name | `Create a pending Study account, assign default role and request email verification` |
| Module | `AUTH` |
| Method | `POST` |
| Endpoint | `/api/v1/auth/register` |
| Primary actor | `Guest` |
| Caller app | `Study client phù hợp với actor Guest` |
| Auth scheme | `None for public entry; vẫn áp dụng rate limit và anti-abuse.` |
| Permission | `public` |
| Status | `DRAFT` |
| Version | `v0.1` |
| Updated | `2026-07-02` |

## Business Goal

API này dùng để create a pending Study account, assign default role and request email verification.. Bản DD này là draft từ BD, API checklist và diagrams; chi tiết chưa đủ nguồn được ghi thành `OPEN_QUESTION`.

## Study Scope

In scope:

- Thực hiện đúng capability Study của module `AUTH` cho actor `Guest`.
- Tuân thủ rule/focus: Enforce `BR-AUTH-001`, `BR-AUTH-002`, `BR-AUTH-003`; define duplicate email/phone behavior without account enumeration; never return password/token secrets.
- Trả response envelope chuẩn có `businessCode`, `timestamp`, `traceId`, `data` hoặc `errors`.

Out of scope:

- Employer, recruitment, job, CV, interview, matching, shortlist, offer và hiring workflows.
- Bất kỳ contract nào chưa có trong BD/checklist hoặc chưa được review trong DD này.

## Source Trace

| Source | Link / ID | Note |
|---|---|---|
| BD | `docs/BD/Study2Work_Study_BD_Codex_Ready.md` | Sections 5.1, 10.4, business rules và API catalogue. |
| API checklist | `docs/checklists/API.md` | `AUTH-REGISTER-001` canonical row. |
| Activity diagram | `docs/diagrams/02_activity/01_Dang_ky_va_kich_hoat_tai_khoan.puml` | Flow hành vi liên quan. |
| Sequence diagram | `docs/diagrams/04_sequence/01_Register_Verify_Email.puml` | Tương tác runtime liên quan. |
| Class diagram | `docs/diagrams/03_class/01_Identity_Profile.puml` | Aggregate/read model liên quan. |
| Architecture | `docs/architecture/PROJECT_ARCHITECTURE.md` | Server/client boundary và API DD gate. |

## Preconditions

- DD đang ở trạng thái `DRAFT`, chưa được phê duyệt để implement official business API.
- Caller đáp ứng auth scheme và permission nếu endpoint không public.
- Resource liên quan tồn tại và nằm trong ownership/scope của actor.

## Postconditions

- Thành công: response trả envelope với `businessCode` `AUTH-REGISTER-001-SUCCESS`.
- Nếu có ghi dữ liệu, transaction chỉ commit khi validation, authorization và business rule đều pass.
- Failed requests must not create partial business state unless explicitly documented.

## Authorization And Scope

| Actor | Permission | Ownership/scope rule |
|---|---|---|
| `Guest` | `public` | Chỉ thao tác trong public/auth flow hiện tại; không được đọc dữ liệu riêng tư. |

## Data Ownership

| Table / aggregate | Read | Write | Owner module | Note |
|---|---:|---:|---|---|
| `user` | Y | Y | `AUTH` | Lấy từ API checklist và BD data dictionary. |
| `user_role` | Y | Y | `AUTH` | Lấy từ API checklist và BD data dictionary. |
| `verification_token` | Y | Y | `AUTH` | Lấy từ API checklist và BD data dictionary. |
| `audit_log` | Y | Y | `AUTH` | Lấy từ API checklist và BD data dictionary. |

## Events And Async Work

| Event/job | When emitted | Delivery | Consumer | Retry rule |
|---|---|---|---|---|
| `UserRegistered` | Sau khi transaction nguồn commit. | after_commit/outbox/Celery | Consumer liên quan. | Retry theo worker/outbox policy. |
| `NotificationRequested` | Sau khi transaction nguồn commit. | after_commit/outbox/Celery | Consumer liên quan. | Retry theo worker/outbox policy. |

## Open Questions

| ID | Owner | Status | Question |
|---|---|---|---|
| AUTH-REGISTER-001-OQ-001 | BA/PO + Tech Lead | OPEN | Xác nhận schema request/response chi tiết trước khi chuyển DD sang IN_REVIEW hoặc APPROVED. |

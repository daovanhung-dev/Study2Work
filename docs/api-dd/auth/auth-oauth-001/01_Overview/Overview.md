# Overview - AUTH-OAUTH-001

| Field | Value |
|---|---|
| API code | `AUTH-OAUTH-001` |
| API name | `Start and complete Google/GitHub OAuth sign-in for Study identity` |
| Module | `AUTH` |
| Method | `GET/POST` |
| Endpoint | `/api/v1/auth/oauth/{provider}` |
| Primary actor | `Guest` |
| Caller app | `Study client phù hợp với actor Guest` |
| Auth scheme | `None for public entry; vẫn áp dụng rate limit và anti-abuse.` |
| Permission | `public` |
| Status | `DRAFT` |
| Version | `v0.1` |
| Updated | `2026-07-02` |

## Business Goal

API này dùng để start and complete Google/GitHub OAuth sign-in for Study identity.. Bản DD này là draft từ BD, API checklist và diagrams; chi tiết chưa đủ nguồn được ghi thành `OPEN_QUESTION`.

## Study Scope

In scope:

- Thực hiện đúng capability Study của module `AUTH` cho actor `Guest`.
- Tuân thủ rule/focus: Provider allowlist, callback validation, state/nonce, identity linking and no raw OAuth secret logging.
- Trả response envelope chuẩn có `businessCode`, `timestamp`, `traceId`, `data` hoặc `errors`.

Out of scope:

- Employer, recruitment, job, CV, interview, matching, shortlist, offer và hiring workflows.
- Bất kỳ contract nào chưa có trong BD/checklist hoặc chưa được review trong DD này.

## Source Trace

| Source | Link / ID | Note |
|---|---|---|
| BD | `docs/BD/Study2Work_Study_BD_Codex_Ready.md` | Sections 5.1, 10.4, business rules và API catalogue. |
| API checklist | `docs/checklists/API.md` | `AUTH-OAUTH-001` canonical row. |
| Activity diagram | `docs/diagrams/02_activity/README.txt` | Flow hành vi liên quan. |
| Sequence diagram | `docs/diagrams/04_sequence/02_Login_Refresh_Logout.puml` | Tương tác runtime liên quan. |
| Class diagram | `docs/diagrams/03_class/01_Identity_Profile.puml` | Aggregate/read model liên quan. |
| Architecture | `docs/architecture/PROJECT_ARCHITECTURE.md` | Server/client boundary và API DD gate. |

## Preconditions

- DD đang ở trạng thái `DRAFT`, chưa được phê duyệt để implement official business API.
- Caller đáp ứng auth scheme và permission nếu endpoint không public.
- Resource liên quan tồn tại và nằm trong ownership/scope của actor.

## Postconditions

- Thành công: response trả envelope với `businessCode` `AUTH-OAUTH-001-SUCCESS`.
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
| `session` | Y | Y | `AUTH` | Lấy từ API checklist và BD data dictionary. |
| `refresh_token` | Y | Y | `AUTH` | Lấy từ API checklist và BD data dictionary. |

## Events And Async Work

| Event/job | When emitted | Delivery | Consumer | Retry rule |
|---|---|---|---|---|
| `none` | Không có event/job bắt buộc trong source hiện tại. | N/A | N/A | Không retry. |

## Open Questions

| ID | Owner | Status | Question |
|---|---|---|---|
| AUTH-OAUTH-001-OQ-001 | BA/PO + Tech Lead | OPEN | Xác nhận schema request/response chi tiết trước khi chuyển DD sang IN_REVIEW hoặc APPROVED. |
| AUTH-OAUTH-001-OQ-002 | Tech Lead | OPEN | Xác nhận có tách OAuth start và callback thành hai API riêng hay giữ theo catalogue hiện tại. |

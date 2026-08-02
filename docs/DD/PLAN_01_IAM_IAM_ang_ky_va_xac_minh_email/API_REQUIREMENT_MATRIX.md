# API Requirement Matrix — PLAN-01

| API ID | Method | Endpoint | Actor | Auth | Input baseline | Output baseline | Rules | Tables | Transaction | Event | Status |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `API-IAM-001` | `POST` | `/api/v1/auth/register` | Anonymous | HTTPS, no bearer | email, password 12–128, agreement versions, locale, Idempotency-Key | pending registration + `verificationExpiresAt`; exact envelope values missing | BR-IAM-001/002/008 | users, user_emails, password_credentials, email_verification_tokens, idempotency, audit, outbox; agreement table missing | Single identity_db TX | `identity.user.registered` unversioned; catalog gap | NEEDS USER DECISION |
| `API-IAM-002` | `POST` | `/api/v1/auth/verify-email` | Anonymous | One-time token possession | token 32–512, Idempotency-Key | access/refresh token + ACTIVE; exact field names missing | BR-IAM-002/003 | token, users, user_emails, sessions, refresh, idempotency, outbox | Row lock token + single identity_db TX | `identity.user.verified.v1` | NEEDS USER DECISION |
| `API-IAM-003` | `POST` | `/api/v1/auth/resend-verification` | Anonymous | Ownership proof only for cooldown error, but contract missing | email | always generic accepted; exact status/code/data missing | BR-IAM-008 | user_emails, users, verification tokens, outbox | Conditional single identity_db TX | Email delivery event missing | NEEDS USER DECISION |

## Batch conventions locked

- JSON camelCase; DB snake_case; UUID v7; ISO-8601 UTC `Z`.
- Canonical envelope has `success`, `businessCode`, `message`, `data`, `meta`, `traceId`.
- `meta` always object; no stack trace, SQL, raw token, secret or account enumeration.
- External side effects use transactional outbox and occur after COMMIT.
- One field/column/condition/error per line or table row.

# OPEN QUESTIONS — PLAN-01

## Q-PLAN01-001 — Canonical API display names and document metadata

**Evidence**
- Plan provides scope labels and API IDs, but canonical API name/version/owner/reviewer/approver are not defined.

**Impact**
- Cover metadata and folder display names remain Draft/DERIVED.

**Decision required**
- Confirm canonical names, DD version, document owner, reviewer and approver.

<a id="q-plan01-002"></a>
## Q-PLAN01-002 — Register request field-level schema

**Evidence**
- API row states `email`, password 12–128, “agreement versions”, locale.
- Exact JSON shape, required flags, agreement item structure, locale allowlist/default are not defined.

**Impact**
- OpenAPI/validation and request example cannot be Final.

**Recommendation**
- Approve exact JSON Schema, including whether `agreementVersions` is an array of strings or objects.

<a id="q-plan01-003"></a>
## Q-PLAN01-003 — Missing agreement acceptance physical schema

**Evidence**
- API/sequence/class require `user_agreement_acceptances` / `AgreementAcceptance`.
- Canonical DB document has no IAM agreement acceptance table or columns.

**Impact**
- Register transaction and DB Mapping are incomplete; API-IAM-001 cannot be DONE.

**Decision required**
- Add approved table definition/migration contract or remove the mutation from API contract.

## Q-PLAN01-004 — API table names vs DB canonical names

**Evidence**
- API row uses `platform_users`, `one_time_tokens`, `identity_outbox_events`.
- DB canonical uses `users`, `email_verification_tokens`, `outbox_events`, and separates `user_emails`.

**Impact**
- Document–implementation/data-model drift.

**Recommendation**
- Update API row to canonical table IDs/names or add an explicit alias mapping.

## Q-PLAN01-005 — Exact success response contract for all three APIs

**Evidence**
- Envelope is canonical, but success HTTP status, businessCode, localized message and full `data` schema are not defined.
- Verify semantic output names access/refresh token, but exact field names/transport are missing.

**Impact**
- Client contract, idempotency replay and tests cannot be frozen.

**Decision required**
- Approve field-level response schemas and success codes/messages/statuses.

## Q-PLAN01-006 — Endpoint-specific HTTP status/message mapping

**Evidence**
- Codes `EMAIL_ALREADY_REGISTERED`, `PASSWORD_POLICY_FAILED`, `AGREEMENT_VERSION_INVALID`, `TOKEN_INVALID_OR_EXPIRED`, `TOKEN_ALREADY_USED`, `RESEND_COOLDOWN`, `REQUEST_IN_PROGRESS` are referenced but not fully mapped in the central error catalog.

**Impact**
- `06_Error.md` retains `TBD` for affected HTTP statuses/message IDs.

**Decision required**
- Add these codes to canonical error catalog with HTTP, retryability and public message policy.

## Q-PLAN01-007 — Duplicate email enumeration conflict

**Evidence**
- API row lists `EMAIL_ALREADY_REGISTERED`.
- BR-IAM-008, AC and sequence require generic accepted response without revealing email existence.

**Impact**
- Security behavior and client contract conflict.

**Recommendation**
- Prefer indistinguishable accepted response; retain duplicate reason only in redacted security audit.

## Q-PLAN01-008 — Registration event and secure raw-token delivery

**Evidence**
- Endpoint mentions `identity.user.registered`; event catalog has no corresponding versioned event.
- Sequence requires raw token to reach email provider, while DB/outbox must not persist raw token.

**Impact**
- Outbox event type/payload/dataschema and secure delivery handoff are undefined.

**Decision required**
- Define versioned delivery/domain event(s), payload and secret handoff mechanism.

## Q-PLAN01-009 — Verification token TTL and hash algorithm

**Evidence**
- Token input length is 32–512 and DB stores `char(64)` hash, but generation length, TTL and keyed hash algorithm/key management are absent.

**Impact**
- Token issuance/validation security and `verificationExpiresAt` cannot be implemented exactly.

**Decision required**
- Approve TTL, random entropy, encoding and keyed hash/KMS policy.

## Q-PLAN01-010 — `authVersion` / `session_epoch` data-model gap

**Evidence**
- Class/business rules reference `authVersion`.
- `auth_sessions.session_epoch` is required.
- Canonical `users` table does not define `auth_version` or session epoch source.

**Impact**
- API-IAM-002 session creation and JWT claims are blocked.

**Decision required**
- Add canonical `auth_version`/epoch column and transition rule, or define another authoritative source.

## Q-PLAN01-011 — Verified event naming drift

**Evidence**
- API row uses `identity.user.verified`.
- Event catalog defines `identity.user.verified.v1`.

**Impact**
- Producer/consumer schema matching.

**Recommendation**
- Use versioned event type `identity.user.verified.v1` and update endpoint row.

## Q-PLAN01-012 — Verify idempotency replay with raw tokens

**Evidence**
- Verify endpoint requires idempotency.
- Idempotency table stores response body, while raw access/refresh tokens are sensitive.

**Impact**
- Replaying same result safely may require encrypted response storage or token issuance indirection.

**Decision required**
- Approve encrypted idempotency response design or alternative replay contract.

## Q-PLAN01-013 — Resend ownership proof and cooldown error

**Evidence**
- API is Anonymous and request only contains email.
- `RESEND_COOLDOWN` may be returned only when a session proves ownership.

**Impact**
- The conditional error branch is not implementable from current request contract.

**Recommendation**
- Either always return generic accepted for anonymous endpoint, or define a separate authenticated/session-bound resend contract.

## Q-PLAN01-014 — Resend event schema and dedupe implementation

**Evidence**
- API requires email delivery/outbox and 10-minute dedupe.
- No event type/payload, token expiry, or explicit dedupe storage contract is defined.

**Impact**
- Outbox mapping remains SOURCE_REQUIRED and cooldown query/index is provisional.

**Decision required**
- Define email-delivery event and whether dedupe uses token `created_at`, Redis, or a dedicated delivery table.

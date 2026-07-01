# API DD Checklist

| Field | Value |
|---|---|
| API code | `{{API_CODE}}` |
| Module | `{{MODULE_CODE}}` |
| Status | `DRAFT` |
| Updated | `{{YYYY-MM-DD}}` |

## Business Readiness

- [ ] API exists in `docs/checklists/API.md` or has explicit approval.
- [ ] BD section, business rules, state machine, and diagrams are linked.
- [ ] Study-only scope is explicit.
- [ ] Open questions are listed with owner/date.

## Contract Readiness

- [ ] Method and endpoint are final.
- [ ] Auth scheme, role, permission, and ownership/scope are explicit.
- [ ] Request fields cover path, query, header, body, file, and auth context.
- [ ] Response examples are valid JSON.
- [ ] Success and error envelopes include `businessCode`, `timestamp`, and `traceId`.

## Runtime Readiness

- [ ] DataMapping lists all read/write tables.
- [ ] Transaction boundary is explicit.
- [ ] Idempotency and concurrency are defined where relevant.
- [ ] Audit log and outbox/event/job behavior are defined where relevant.
- [ ] Retry/DLQ behavior is defined for async work.

## Test Readiness

- [ ] Happy path test is defined.
- [ ] Validation failure tests are defined.
- [ ] Authentication/authorization/ownership tests are defined.
- [ ] State transition tests are defined where relevant.
- [ ] Dependency failure and retry tests are defined where relevant.

## Approval

| Role | Reviewer | Status | Date | Note |
|---|---|---|---|---|
| BA/PO | `{{NAME}}` | `PENDING` | `{{YYYY-MM-DD}}` | Business scope and rules |
| Tech Lead | `{{NAME}}` | `PENDING` | `{{YYYY-MM-DD}}` | Architecture and data mapping |
| QA | `{{NAME}}` | `PENDING` | `{{YYYY-MM-DD}}` | Testability and negative cases |

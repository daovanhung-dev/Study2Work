# Plan result — API #93 Tạo/phát notification

## Status

- Result: IMPLEMENTED AND LOCALLY VERIFIED with a DERIVED fallback; owner decisions remain open.
- DD status: Draft — Needs Confirmation.
- Runtime status: WIRED; HTTP behavior is covered by fake-DB tests only.
- Live DB schema, deployment, notification worker/provider delivery, and owner approval were not verified.
- AC-36 macro-review: `VERIFIED_WITH_OPEN_QUESTIONS`; see #92–#96 report.

## Direct API requirement

- API #93: POST `/api/v1/admin/notifications`.
- Auth: Bearer JWT; role Admin; AC-36 notification-management permission.
- Body: recipients?:int64[], segment?:AudienceSegment, title:string!, content:string!, channels:NotificationChannel[].
- Response: ApiEnvelope<Notification>.
- Success: HTTP 202 `DESIGN_OPERATION_ACCEPTED`.
- Errors: 401 `DESIGN_AUTHENTICATION_REQUIRED`; 403 `DESIGN_ACCESS_DENIED`; 422 `DESIGN_VALIDATION_ERROR`; 503 `DESIGN_DEPENDENCY_UNAVAILABLE`; 500 `DESIGN_INTERNAL_ERROR`.

## Implemented local fallback

- Shared ADMIN auth precedes body parsing and all recipient DB queries.
- Explicit recipients only; segment is rejected until its enum/predicate is defined. Recipient IDs must be positive, unique int64 values and exist in `users`.
- Runtime accepts unique `PUSH`/`EMAIL`, rejects blank title/content, and applies the legacy candidate title limit of 200 characters.
- Writes one legacy BIGINT notification per recipient with a shared UUID `operation_id`, plus one `QUEUED` delivery row per recipient/channel. One transaction commits the entire batch.
- `data` contains the first notification; derived `meta` contains the shared UUID and all notification IDs.
- No provider/worker call is made. 202 reports local durable outbox acceptance only.
- These persistence, validation, channel, status, response-metadata, and failure-mapping choices are DERIVED and remain unapproved.

## Sources reviewed

- Catalog #93, reusable Notification/Operation schemas, Operation tracking summary.
- AC-36 index and diagram nodes/edges.
- Legacy Study table guide/DDL and separate V1-PILOT notification/delivery DDL.
- DD #92, #63, #64 and #18.
- Current Study router, Admin auth/database/response helpers, and linked regression tests.
- API Guidelines, registered createDD-markdown skill, eight templates, and Study workflow.
- Three coding worklogs selected and reviewed before the implementation plan.

## Output

- Eight standard sheets `00_Cover.md` through `07_table.md`.
- Two supplementary mappings: recipient grain and delivery outbox.
- Three reports: `OPEN_QUESTIONS.md`, `PLAN_RESULT.md`, and `VERIFICATION_REPORT.md`.
- Study scope delivers a Markdown folder; no ZIP.

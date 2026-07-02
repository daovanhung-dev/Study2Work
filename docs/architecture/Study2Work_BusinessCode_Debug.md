# Study2Work Business Code And Debug Map

This document defines Study-only business code conventions for support and debugging. API-specific codes are finalized in each approved API DD.

## Business Code Format

Use stable uppercase codes:

```text
<MODULE>-<ACTION>-<RESULT>
```

Examples:

- `SYSTEM-HEALTH-SUCCESS`
- `AUTH-REGISTER-SUCCESS`
- `AUTH-REGISTER-DUPLICATE`
- `LEARNING-LESSON-LOCKED`
- `ASSESSMENT-SUBMISSION-LATE`
- `PROJECT-TASK-INVALID-TRANSITION`
- `AI-REQUEST-RATE-LIMITED`

## Module Prefixes

| Prefix | Module |
|---|---|
| `SYSTEM` | Platform and health |
| `AUTH` | Identity and access |
| `PROFILE` | Profile and baseline skills |
| `LEARNING` | Learning path, lesson, progress |
| `ASSESSMENT` | Quiz, assignment, grading, skill matrix |
| `MENTOR` | Mentor review and scope |
| `PROJECT` | Teamwork, task and project submission |
| `AI` | AI learning support |
| `COMMUNITY` | Events and community participation |
| `NOTIFICATION` | Notification feed and dispatch |
| `ADMIN` | Administration, settings, moderation and audit |
| `FILE` | File asset upload/download boundary |

## Debug Trace Fields

Every server log and support payload should preserve:

| Field | Meaning |
|---|---|
| `traceId` | Request correlation ID from `X-Trace-Id` or server-generated UUID. |
| `businessCode` | Stable client/support code. |
| `actorId` | Authenticated actor when available. |
| `moduleCode` | Study module handling the request. |
| `apiCode` | API checklist/DD code when available. |
| `resourceId` | Target resource when safe to log. |

## Safe Error Policy

- Client messages must be safe and non-enumerating where required.
- Never log plaintext passwords, tokens, provider secrets, hidden tests or private PII.
- AI request logs must use redacted input snapshots when sensitive data may be present.
- Debug details belong in structured logs, not client-facing messages.

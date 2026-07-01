# Study2Work API Detail Design Template

This Markdown template describes exactly one Study2Work API operation. It must be filled before official API implementation unless the user explicitly requests a prototype.

## Folder Structure

```text
Study2Work_API_DD_Template/
├── README.md
├── HUONG_DAN_NHAP_LIEU_DD.md
├── API_DD_CHECKLIST.md
├── 01_Overview/Overview.md
├── 02_History/History.md
├── 03_Request/Request.md
├── 04_Response/Response.md
├── 05_DataMapping/DataMapping.md
└── 06_Error/Error.md
```

Copy the whole folder to:

```text
docs/api-dd/<module-code-lowercase>/<api-code-lowercase>/
```

## Study Module Codes

| Module code | Scope | Example API code |
|---|---|---|
| `AUTH` | Authentication, session, token, RBAC | `AUTH-LOGIN-001` |
| `USER` | Profile and declared baseline skills | `USER-PROFILE-001` |
| `LEARN` | Learning path, lesson, progress, bookmark, comment, live session | `LEARN-PROGRESS-001` |
| `ASSESS` | Quiz, assignment, submission, auto grading, skill matrix | `ASSESS-SUBMISSION-001` |
| `MENTOR` | Review, rubric feedback, mentor scope | `MENTOR-REVIEW-001` |
| `PROJECT` | Team, sprint, task, work log, Git/PR evidence | `PROJECT-TASK-002` |
| `AI` | Roadmap suggestion, code explanation, learning insight | `AI-ROADMAP-001` |
| `NOTI` | Notification template, feed, dispatch | `NOTI-FEED-001` |
| `ADMIN` | Content, rubric, mentor scope, setting, moderation, analytics | `ADMIN-CONTENT-001` |
| `SYSTEM` | Health, audit, internal worker operations | `SYSTEM-HEALTH-001` |

Do not add employer, recruitment, job, CV, interview, matching, shortlist, offer, or hiring APIs to this template.

## API Contract Standards

| Item | Standard |
|---|---|
| API prefix | `/api/v1` |
| JSON property names | `camelCase` |
| Database names | `snake_case` |
| ID format | UUID string |
| Timestamp | ISO-8601 UTC |
| Response envelope | `businessCode`, `message`, `timestamp`, `traceId`, `data` or `errors` |
| Trace header | `X-Trace-Id` |
| Auth | Bearer JWT for protected APIs |
| Pagination | Required for list endpoints |

## Required Fill Order

1. `01_Overview/Overview.md`
2. `03_Request/Request.md`
3. `04_Response/Response.md`
4. `05_DataMapping/DataMapping.md`
5. `06_Error/Error.md`
6. `02_History/History.md`
7. `API_DD_CHECKLIST.md`

## Definition Of Done

An API DD is complete only when:

- No placeholder remains.
- Request and response examples are valid JSON.
- Permission and ownership/scope checks are explicit.
- Table reads/writes and transaction boundaries are explicit.
- Success and error envelopes include stable business codes and trace behavior.
- Error cases include validation, auth, business, state, dependency, and system failures where relevant.
- QA can derive tests without asking BE/BA to guess the contract.

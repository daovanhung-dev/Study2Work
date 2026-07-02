# Study2Work Study Domain Model

This document is a Study-only domain summary. The canonical project architecture is `PROJECT_ARCHITECTURE.md`; the server layer rules are in `SERVER_ARCHITECTURE.md`.

## Domain Principles

- `User` owns identity only; business state belongs to its bounded context.
- Each bounded context owns its data and invariants.
- Derived data such as progress, score and skill level is updated from evidence and events.
- AI output is guidance only and never overwrites source-of-truth data directly.
- Administrative and sensitive actions must produce audit evidence.

## Bounded Contexts

| Context | Aggregate roots | Responsibility |
|---|---|---|
| Identity and Access | `User`, `Session`, `Role` | Registration, verification, login, token/session lifecycle and RBAC. |
| Profile | `Profile`, `StudentProfile`, `MentorProfile` | User-facing profile, role extension and baseline skills. |
| Learning Journey | `LearningPath`, `Module`, `Lesson`, `LiveSession` | Learning content tree, unlock rules, comments, bookmarks and progress. |
| Practice and Assessment | `Quiz`, `Assignment`, `Submission`, `SkillAssessment` | Attempts, submissions, grading evidence, rubric review and skill matrix. |
| Project Teamwork | `Project`, `Team`, `Sprint`, `Task` | Team membership, task workflow, work evidence and project submission. |
| Mentor Workflow | `Review`, `Feedback`, `MentorScope` | Assigned review scope, rubric feedback and learner/team review operations. |
| AI Learning Support | `AIRequest`, `AIInsight`, `RoadmapSuggestion` | Roadmap suggestions, code explanations and non-authoritative learning insights. |
| Community | `CommunityEvent`, `EventRegistration` | Workshops, events and Study community participation. |
| Notification | `Notification`, `NotificationTemplate` | In-app feed, read state, templates and async dispatch. |
| Admin and Platform | `SystemSetting`, `FeatureFlag`, `AuditLog`, `AnalyticsSnapshot` | Settings, flags, analytics, moderation and audit. |

## Important State Machines

| Object | State flow |
|---|---|
| User | `PENDING -> ACTIVE -> SUSPENDED -> DELETED` |
| Lesson progress | `LOCKED -> AVAILABLE -> STARTED -> COMPLETED` |
| Submission | `DRAFT -> SUBMITTED -> IN_REVIEW -> GRADED` |
| Review | `DRAFT -> SUBMITTED -> DONE` |
| Task | `TODO -> IN_PROGRESS -> IN_REVIEW -> DONE`; `BLOCKED` is an exception branch. |
| Notification | `UNREAD -> READ` |

## Domain Events

Events describe facts that already happened:

- `UserRegistered`
- `EmailVerified`
- `LearningPathAssigned`
- `LessonCompleted`
- `QuizSubmitted`
- `AssignmentSubmitted`
- `AutoGradingCompleted`
- `SubmissionReviewed`
- `SkillLevelUpdated`
- `TeamCreated`
- `TeamMemberJoined`
- `TaskAssigned`
- `TaskStatusChanged`
- `ProjectSubmitted`
- `AIInsightGenerated`
- `NotificationRequested`
- `NotificationDispatched`
- `SystemSettingChanged`

## Consistency Rules

- Use strong consistency inside one aggregate.
- Use event/outbox-style handoff across contexts.
- Avoid long transactions across multiple contexts.
- Read models can be optimized for dashboards, filters and analytics but cannot become the source of truth.

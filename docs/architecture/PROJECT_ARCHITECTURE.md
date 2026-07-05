# Study2Work Project Architecture

| Field | Value |
|---|---|
| Status | Canonical foundation |
| Scope | Study + Work + Platform contracts |
| Runtime model | Polyglot monorepo |

## Summary

Study2Work is rebuilt as a monorepo with independent Study and Work runtimes. Study remains the learning system. Work remains the career and recruitment system. They do not share databases or runtime business code.

## Ownership

| Path | Owner | Responsibility |
|---|---|---|
| `apps/study-web` | Study frontend | Vue learning experience. |
| `apps/study-api` | Study backend | FastAPI learning API, Study evidence issuance, Study persistence. |
| `apps/work-web` | Work frontend | React career, CV, job, and recruiter experience. |
| `apps/work-api` | Work backend | NestJS Work API, enterprise/job/application domain, Study evidence snapshot consumer. |
| `apps/platform-identity` | Platform | Local identity/JWKS scaffold and future identity deployment notes. |
| `contracts` | Platform contracts | OpenAPI placeholders, Study-to-Work event schemas, skill taxonomy, API conventions. |
| `infra` | Platform/DevOps | Local and deployment infrastructure scaffolding. |

## Dependency Rules

```text
Web apps -> their own API -> application/domain -> infrastructure adapters
Study API -> signed event contract -> Work API integration module
```

Invalid dependencies:

- Study API querying Work database.
- Work API querying Study database.
- Frontend calling internal integration endpoints directly.
- Shared Python/TypeScript business runtime packages across Study and Work.

## Integration

Study emits minimal verified evidence events through `contracts/events/study-work`. Work stores local `StudyEvidenceSnapshot` data and controls career visibility by user consent.

## Foundation Goals

- Runnable Study API, Work API, Study web, and Work web skeletons.
- Standard API envelope and trace propagation.
- Local Docker services for separate Study and Work databases/caches.
- Versioned contracts that can grow into generated clients and contract tests.

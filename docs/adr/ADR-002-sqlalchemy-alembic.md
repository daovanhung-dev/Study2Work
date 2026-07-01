# ADR-002: SQLAlchemy 2.0 And Alembic

| Field | Value |
|---|---|
| Status | `ACCEPTED` |
| Date | `2026-07-01` |
| Decision owner | Backend Lead |
| Scope | Study backend persistence |

## Context

The Study BD requires PostgreSQL, typed domain data, migration discipline, transaction boundaries, and database constraints for uniqueness and referential integrity.

## Decision

Use SQLAlchemy 2.0 async ORM for persistence and Alembic for database migrations.

## Consequences

- Infrastructure repositories own SQLAlchemy usage.
- Domain/application layers depend on repository ports, not SQLAlchemy sessions.
- Every schema change requires an Alembic migration.
- Migrations must include unique, FK, and index constraints from BD/API DD.


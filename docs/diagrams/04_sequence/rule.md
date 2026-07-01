# PlantUML Rule - Study2Work Study Scope

## Source of truth

Use `docs/BD/Study2Work_Study_BD_Codex_Ready.md` as the canonical source.

## Required sections for sequence diagrams

- API DETAIL
- VALIDATION
- BUSINESS FLOW
- DATABASE FLOW
- SIDE EFFECTS
- SUCCESS FLOW

## Required controls

- `traceId` on every flow.
- Authentication, RBAC and ownership/scope on protected flows.
- Server-side state transition validation.
- PostgreSQL transaction boundary for writes.
- Audit for sensitive/admin/review/content actions.
- Outbox/worker for cross-context side effects.
- Standard response envelope and stable error codes.

## Scope guard

Do not add flows outside Study BD v1.0. Learning evidence remains Study evidence. AI is advisory and never overwrites source-of-truth records.

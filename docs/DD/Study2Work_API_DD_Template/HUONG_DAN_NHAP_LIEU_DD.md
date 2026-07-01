# API DD Input Guide

This guide explains how to fill a Study2Work API DD package.

## Global Rules

1. Start from `docs/BD/Study2Work_Study_BD_Codex_Ready.md`.
2. Use one DD package for one API operation only.
3. Link the related row in `docs/checklists/API.md`.
4. Link related diagrams in `docs/diagrams/`.
5. Use the standard response envelope.
6. Do not write real secrets, tokens, passwords, OTPs, OAuth secrets, hidden test cases, raw private PII, or raw learner source code containing secrets.
7. Mark unclear items as `OPEN_QUESTION`; do not invent business rules.
8. Do not include out-of-scope recruitment/employer/job/CV/interview behavior.

## Overview

Fill:

- API code, method, endpoint, module, actor, caller app.
- Business goal and Study-only scope.
- Preconditions and postconditions.
- Related BD section, business rules, state machine, tables, events, diagrams, and ADRs.
- Sync/async behavior and timeout target.

## Request

Define every input source:

- path parameter
- query parameter
- header
- body
- file/multipart
- auth context

For each field, define type, required flag, nullable flag, validation, enum/range/format, default, example, sensitive classification, and failure code.

## Response

Define:

- HTTP status.
- Business code.
- Envelope fields.
- `data` shape.
- Empty response behavior.
- Pagination if a list is returned.
- Async accepted behavior if returning `202`.

## Data Mapping

Write the runtime sequence:

```text
parse -> schema validation -> authentication -> authorization/scope -> entity load
-> business validation/state transition -> transaction -> write/read -> audit
-> outbox/event/job/cache -> response envelope
```

Each step must name tables, repository methods, rules, errors, and whether a database write occurs.

## Error

For each error, define:

- HTTP status.
- Stable business code.
- Safe client message.
- Field-level detail if relevant.
- Retry policy.
- Log level and alert owner.
- Test case ID.

## History

Append a row for every contract or rule change. Do not remove old history rows.

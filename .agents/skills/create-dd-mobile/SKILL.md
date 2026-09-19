---
name: create-dd-from-bd
description: Create implementation-ready NanoBio module DDs from BD, BRD, product flow, or business requests with strict traceability, status separation, review gates, and safe assumptions.
metadata:
  short-description: Create NanoBio DD modules from business sources
---

# Create DD From BD

Use this skill when creating, scaffolding, updating, or reviewing a NanoBio
module DD from a BD/BRD/product-flow source. Do not use it to implement runtime
code; switch to the coding workflow after the DD is accepted.

## Required output

Create one stable module folder with:

- `README.md`
- `Overall.md`
- `List_Features.md`
- `Function_List.md`
- `Views.md`
- `Import_File.md`
- `diagrams/README.md`
- `assets/README.md`
- `history/CHANGELOG.md`

Every important item must use stable IDs and follow:

```text
BD evidence → Feature → Function/API/Rule → View → Source/Import → Test
```

## Non-negotiable rules

- Read the source BD before writing DD facts.
- Never invent missing business behavior. Mark it `OPEN QUESTION`, `ASSUMPTION`,
  or `PROPOSAL` and identify the owner or decision needed.
- Keep `Lifecycle`, `DD decision`, `Implementation`, and `Verification` as
  independent axes. `Approved` never proves runtime, device, production, or
  Supabase verification.
- Keep user-facing copy Vietnamese; preserve technical IDs, filenames, and
  contracts used by the project.
- Do not place secrets, production PII, raw health data, raw payment evidence,
  or raw webhook payloads in DD files.
- Do not modify runtime code as part of DD authoring unless explicitly requested.

## Read progressively

Read [references/INDEX.md](references/INDEX.md) first. It routes the detailed
references, template, examples, checklists, and validator without requiring all
resources to be loaded for every task.

## Completion gate

Before review, run the static validator, complete the review checklist, update
the DD changelog and worklog, then run the project docs/context validation and
`git diff --check`. Report open questions, assumptions, evidence level, and
unverified runtime/sandbox work separately.

# Module Checklists

Module checklists track changing DD, coding, test, bug, worklog, and evidence status. Do not duplicate the full BD/DD here.

Canonical architecture starts at `docs/architecture/PROJECT_ARCHITECTURE.md`.

## Rules

- Each module has exactly one checklist: `docs/checklists/<MODULE_CODE>.md`.
- Every item must have an ID, status, updated date, and link to BD/DD/worklog/issue/evidence when available.
- Use status values from `.agent/context/STATUS_MODEL.md`.
- Update test status only when concrete evidence exists in a worklog or test output.
- Do not create checklists for removed non-Study modules unless a separate approved BD/DD expands scope.

## Study Module Checklists

| Module | Checklist | Initial status |
|---|---|---|
| `AUTH` | `docs/checklists/AUTH.md` | Bootstrapped |
| `LEARNING` | `docs/checklists/LEARNING.md` | Bootstrapped |
| `ASSESSMENT` | `docs/checklists/ASSESSMENT.md` | Bootstrapped |
| `PROJECT` | `docs/checklists/PROJECT.md` | Bootstrapped |
| `AI` | `docs/checklists/AI.md` | Bootstrapped |
| `ADMIN` | `docs/checklists/ADMIN.md` | Bootstrapped |
| `COMMUNITY` | `docs/checklists/COMMUNITY.md` | Bootstrapped |
| `NOTIFICATION` | `docs/checklists/NOTIFICATION.md` | Bootstrapped |

## Template

Use `docs/checklists/_TEMPLATE.md` when creating a new approved Study module checklist.

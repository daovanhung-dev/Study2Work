# Study2Work Agent Context Map

Đây là bản đồ human-readable của agent context. Nguồn xác thực máy là
[`.agents/context-manifest.json`](context-manifest.json); file này mô tả cách
agent đi từ router tới context page, source, contract, test và worklog.

## Legend

- `→` — thứ tự đọc hoặc load bắt buộc.
- `⇢` — registry/wiring reference được khai báo trong manifest.
- `↔` — boundary hoặc dependency giữa các scope.
- `VERIFIED`, `SOURCE_BACKED`, `UNWIRED`, `NOT_FOUND`, `DISCREPANCY`,
  `CONTEXT_STALE` — trạng thái theo registry; không suy ra runtime chỉ từ file
  tồn tại.
- `AGENTS.md` — router/rule của node.
- `INDEX.md` — page graph của node.
- `README.md` dưới `workflows/`, `apis/`, `modules/` — context page theo chủ đề.

## Canonical load flow

```text
[AGENTS.md]
  → [.agents/AGENTS.md]
  → [.agents/context-map.md]
  → classify primary_task_type + project_scopes
  → worklog preflight: select/read up to 3 same-type worklogs
  → [.agents/project/INDEX.md] when cross-scope/boundary context is needed
  → [.agents/<scope>/AGENTS.md]
  → [.agents/<scope>/INDEX.md] or subcontext/INDEX.md
  → page đúng task
  → exact source + contract/config/test
  → update context/worklog
  → focused verification + context validator
```

The selector is a routing aid; the active worklog records which files were
actually read in `PRIOR_WORKLOG_REVIEW`. `primary_task_type` is matched exactly.

## Physical context tree

```text
Study2Work/
├── AGENTS.md
├── .agents/
│   ├── AGENTS.md
│   ├── context-map.md                         ← this map
│   ├── context-manifest.json                  ← machine-readable registry
│   ├── project/
│   │   ├── INDEX.md
│   │   ├── architecture.md
│   │   ├── business-code.md
│   │   ├── conventions.md
│   │   ├── database.md
│   │   ├── dependencies.md
│   │   ├── design.md
│   │   ├── source-status.md
│   │   ├── contracts.md
│   │   └── workflows.md
│   ├── skills/
│   │   ├── INDEX.md
│   │   ├── create-dd-mobile/                   ← Mobile DD skill pack
│   │   └── create_dd_api/                      ← Web/API DD skill pack
│   ├── worklog/
│   │   ├── README.md
│   │   ├── TEMPLATE.md
│   │   └── YYYY-MM-DD/*.md                     ← historical/current entries
│   ├── server-study/
│   ├── server-work/
│   ├── server-ai/
│   ├── web-work/
│   │   └── study/                              ← Study Web subcontext
│   ├── mobile-work/
│   └── db-admin/
└── scripts/
    ├── select-worklogs.mjs
    └── validate-agent-context.mjs
```

## Root and global registry

- [`AGENTS.md`](../AGENTS.md) ⇢ entry router, task classification, scope
  routing, expected/current behavior rules and mandatory verification.
- [`.agents/AGENTS.md`](AGENTS.md) ⇢ global context index, status vocabulary,
  maintenance rules and canonical page graph boundary.
- [`.agents/context-manifest.json`](context-manifest.json) ⇢ machine registry
  for project pages, scopes, subcontexts, skills, workflows, contracts and
  worklog preflight.
- [`.agents/context-map.md`](context-map.md) ⇢ this human-readable map; it does
  not replace the manifest.
- [`scripts/select-worklogs.mjs`](../scripts/select-worklogs.mjs) ⇢ selects
  same-type worklogs before deep inspection.
- [`scripts/validate-agent-context.mjs`](../scripts/validate-agent-context.mjs)
  ⇢ validates registry, page graph, links, resources, worklog contract and
  source drift.

## Project context tree

- [`.agents/project/INDEX.md`](project/INDEX.md) ⇢ conditional cross-scope
  entry. It points to:
  - [`.agents/project/architecture.md`](project/architecture.md) — ownership
    and deployable boundaries.
  - [`.agents/project/business-code.md`](project/business-code.md) — business
    code and HTTP mapping.
  - [`.agents/project/conventions.md`](project/conventions.md) — shared
    repository conventions.
  - [`.agents/project/database.md`](project/database.md) — database evidence
    and status.
  - [`.agents/project/dependencies.md`](project/dependencies.md) — app,
    contract and external dependency graph.
  - [`.agents/project/design.md`](project/design.md) — Work Web/Mobile design
    source.
  - [`.agents/project/source-status.md`](project/source-status.md) — repository
    snapshot, discrepancies and blockers.
  - [`.agents/project/contracts.md`](project/contracts.md) — producer,
    consumer and status of shared/local contracts.
  - [`.agents/project/workflows.md`](project/workflows.md) — workflow registry
    and verification order.

## Scope context trees

### `server-study`

- Source root: `apps/study-server/`
- Status: `SOURCE_BACKED`
- Entry: [`.agents/server-study/AGENTS.md`](server-study/AGENTS.md)
- Index: [`.agents/server-study/INDEX.md`](server-study/INDEX.md)
- Skill ⇢ `createDD-markdown`
- Pages:
  - [`.agents/server-study/architecture.md`](server-study/architecture.md)
  - [`.agents/server-study/apis/declared-routes.md`](server-study/apis/declared-routes.md)
  - [`.agents/server-study/core/runtime.md`](server-study/core/runtime.md)
  - [`.agents/server-study/core/database-security.md`](server-study/core/database-security.md)
  - [`.agents/server-study/database.md`](server-study/database.md)
  - [`.agents/server-study/modules/README.md`](server-study/modules/README.md)
  - [`.agents/server-study/modules/register-account.md`](server-study/modules/register-account.md)
  - [`.agents/server-study/services/ai.md`](server-study/services/ai.md)
  - [`.agents/server-study/tests.md`](server-study/tests.md)
  - [`.agents/server-study/workflows/README.md`](server-study/workflows/README.md)

### `server-work`

- Source root: `apps/work-server/`
- Status: `SOURCE_CHANGED`
- Entry: [`.agents/server-work/AGENTS.md`](server-work/AGENTS.md)
- Index: [`.agents/server-work/INDEX.md`](server-work/INDEX.md)
- Skill ⇢ `createDD-markdown`
- Pages:
  - [`.agents/server-work/architecture.md`](server-work/architecture.md)
  - [`.agents/server-work/apis/foundation.md`](server-work/apis/foundation.md)
  - [`.agents/server-work/core/auth-config-db.md`](server-work/core/auth-config-db.md)
  - [`.agents/server-work/core/runtime-http.md`](server-work/core/runtime-http.md)
  - [`.agents/server-work/database.md`](server-work/database.md)
  - [`.agents/server-work/modules/foundation.md`](server-work/modules/foundation.md)
  - [`.agents/server-work/tests.md`](server-work/tests.md)
  - [`.agents/server-work/workflows/README.md`](server-work/workflows/README.md)

### `server-ai`

- Source root: `apps/ai-server/`
- Status: `VERIFIED_WITH_UNWIRED_COMPONENTS`
- Entry: [`.agents/server-ai/AGENTS.md`](server-ai/AGENTS.md)
- Index: [`.agents/server-ai/INDEX.md`](server-ai/INDEX.md)
- Skill ⇢ `createDD-markdown`
- Pages:
  - [`.agents/server-ai/architecture.md`](server-ai/architecture.md)
  - [`.agents/server-ai/apis/chat.md`](server-ai/apis/chat.md)
  - [`.agents/server-ai/core/copied-core.md`](server-ai/core/copied-core.md)
  - [`.agents/server-ai/database.md`](server-ai/database.md)
  - [`.agents/server-ai/modules/chat.md`](server-ai/modules/chat.md)
  - [`.agents/server-ai/services/ollama.md`](server-ai/services/ollama.md)
  - [`.agents/server-ai/tests.md`](server-ai/tests.md)
  - [`.agents/server-ai/workflows/README.md`](server-ai/workflows/README.md)

### `web-work`

- Source roots: `apps/study-client/`, `apps/work-client/web/`
- Status: `VERIFIED_REACT_EXPRESS_SPLIT`
- Entry: [`.agents/web-work/AGENTS.md`](web-work/AGENTS.md)
- Index: [`.agents/web-work/INDEX.md`](web-work/INDEX.md)
- Skill ⇢ `createDD-markdown`
- Parent pages:
  - [`.agents/web-work/architecture.md`](web-work/architecture.md)
  - [`.agents/web-work/conventions.md`](web-work/conventions.md)
  - [`.agents/web-work/dependencies.md`](web-work/dependencies.md)
  - [`.agents/web-work/modules/README.md`](web-work/modules/README.md)
  - [`.agents/web-work/workflows/README.md`](web-work/workflows/README.md)

#### `web-work/study-web` subcontext

- Source root: `apps/study-client/`
- Status: `SOURCE_BACKED_SKELETON`
- Entry: [`.agents/web-work/study/AGENTS.md`](web-work/study/AGENTS.md)
- Index: [`.agents/web-work/study/INDEX.md`](web-work/study/INDEX.md)
- Stack: Vue 3 + Vite + Vue Router + Pinia + Vue Query + Zod.
- Pages:
  - [`.agents/web-work/study/architecture.md`](web-work/study/architecture.md)
  - [`.agents/web-work/study/api.md`](web-work/study/api.md)
  - [`.agents/web-work/study/tests.md`](web-work/study/tests.md)
  - [`.agents/web-work/study/workflows/README.md`](web-work/study/workflows/README.md)

#### `web-work/work-web` subcontext

- Source root: `apps/work-client/web/`
- Status: `VERIFIED_REACT_EXPRESS_SPLIT`
- Entry/index/pages reuse the parent Web graph:
  [`.agents/web-work/AGENTS.md`](web-work/AGENTS.md),
  [`.agents/web-work/INDEX.md`](web-work/INDEX.md), and the parent pages above.
- Stack: React + React Query + Zod; do not apply Study Vue patterns.

### `mobile-work`

- Source root: `apps/work-client/mobile/`
- Status: `SOURCE_BACKED`
- Entry: [`.agents/mobile-work/AGENTS.md`](mobile-work/AGENTS.md)
- Index: [`.agents/mobile-work/INDEX.md`](mobile-work/INDEX.md)
- Skill ⇢ `create-dd-from-bd-mobile`
- Pages:
  - [`.agents/mobile-work/architecture.md`](mobile-work/architecture.md)
  - [`.agents/mobile-work/dependencies.md`](mobile-work/dependencies.md)
  - [`.agents/mobile-work/conventions.md`](mobile-work/conventions.md)
  - [`.agents/mobile-work/file-inventory.md`](mobile-work/file-inventory.md)
  - [`.agents/mobile-work/flutter-student.md`](mobile-work/flutter-student.md)
  - [`.agents/mobile-work/flutter-business.md`](mobile-work/flutter-business.md)
  - [`.agents/mobile-work/data-flow.md`](mobile-work/data-flow.md)
  - [`.agents/mobile-work/modules/README.md`](mobile-work/modules/README.md)
  - [`.agents/mobile-work/workflows/README.md`](mobile-work/workflows/README.md)
- The two Flutter apps are independent; select only the affected app page unless
  the task crosses the mobile data-flow boundary.

### `db-admin`

- Source roots: `apps/db-admin-web/`, `apps/db-admin-server/`
- Status: `VERIFIED`
- Entry: [`.agents/db-admin/AGENTS.md`](db-admin/AGENTS.md)
- Index: [`.agents/db-admin/INDEX.md`](db-admin/INDEX.md)
- Pages:
  - [`.agents/db-admin/architecture.md`](db-admin/architecture.md)
  - [`.agents/db-admin/apis/README.md`](db-admin/apis/README.md)
  - [`.agents/db-admin/core/security-audit.md`](db-admin/core/security-audit.md)
  - [`.agents/db-admin/database.md`](db-admin/database.md)
  - [`.agents/db-admin/tests.md`](db-admin/tests.md)
  - [`.agents/db-admin/workflows/README.md`](db-admin/workflows/README.md)
- DB Admin is a separate deployable and must not import Study/Work/AI business
  modules or schemas.

## Skill graph

- [`.agents/skills/INDEX.md`](skills/INDEX.md) ⇢ skill registry and boundary
  rules.
- `create-dd-from-bd-mobile`
  - Entry: [`.agents/skills/create-dd-mobile/SKILL.md`](skills/create-dd-mobile/SKILL.md)
  - Scope ⇢ `mobile-work`.
  - Workflow ⇢ `docs-dd-mobile`.
  - Resource pack: [`.agents/skills/create-dd-mobile`](skills/create-dd-mobile).
    Its references, checklists, templates, examples and validator are one
    canonical Mobile DD resource tree.
- `createDD-markdown`
  - Entry: [`.agents/skills/create_dd_api/docs/dd/createDD_MARKDOWN_SKILL.md`](skills/create_dd_api/docs/dd/createDD_MARKDOWN_SKILL.md)
  - Scope ⇢ `server-study`, `server-work`, `server-ai`, `web-work`.
  - Workflows ⇢ `docs-dd`, `cross-scope-contract`.
  - Template resource: [`.agents/skills/create_dd_api/docs/dd/DD_API_Template_MD`](skills/create_dd_api/docs/dd/DD_API_Template_MD).
  - Example resources: [`.agents/skills/create_dd_api/docs/dd/Examples/HOKAN_K00GetLabelInfo`](skills/create_dd_api/docs/dd/Examples/HOKAN_K00GetLabelInfo), [`.agents/skills/create_dd_api/docs/dd/Examples/VQ2T_PARAM_I01SaveRemovalPart`](skills/create_dd_api/docs/dd/Examples/VQ2T_PARAM_I01SaveRemovalPart).
- Web UI-only DD has no canonical skill.

## Workflow graph

All workflow keys below are registered in the manifest. Their implementation
entry is [`.agents/project/workflows.md`](project/workflows.md), except the
worklog contract which is implemented by [`.agents/worklog/README.md`](worklog/README.md).

| Workflow key | Trigger/boundary | Entry | Main result |
|---|---|---|---|
| `coding` | coding task | `project/workflows.md` | scoped implementation + tests |
| `fix` | bug/regression | `project/workflows.md` | reproduce → trace → smallest fix → regression test |
| `test` | test/verification | `project/workflows.md` | focused then scope verification |
| `docs-dd` | Web/API DD | `project/workflows.md` | source-backed API DD validation |
| `docs-dd-mobile` | Mobile DD | `project/workflows.md` | Mobile DD validator + context validation |
| `cross-scope-contract` | shared API/event boundary | `project/workflows.md` | producer/consumer/status verification |
| `worklog` | every task/context update/handoff | `worklog/README.md` | preflight + evidence + handoff |

Scope workflow pages refine the common workflow and side effects:

- Mobile: [`mobile-work/workflows/README.md`](mobile-work/workflows/README.md)
- Web: [`web-work/workflows/README.md`](web-work/workflows/README.md) and
  [`web-work/study/workflows/README.md`](web-work/study/workflows/README.md)
- Work Server: [`server-work/workflows/README.md`](server-work/workflows/README.md)
- Study Server: [`server-study/workflows/README.md`](server-study/workflows/README.md)
- AI Server: [`server-ai/workflows/README.md`](server-ai/workflows/README.md)
- DB Admin: [`db-admin/workflows/README.md`](db-admin/workflows/README.md)

## Contract and cross-scope graph

Contracts are external to `.agents`; their producer, consumers and status are
registered in the manifest and summarized here:

| Contract | Producer ↔ consumers | Status | Context consumers |
|---|---|---|---|
| [`contracts/api-guidelines/README.md`](../contracts/api-guidelines/README.md) | repository conventions ↔ Study Server, Work Server, Web Work | `VERIFIED` | API pages/workflows |
| [`contracts/events/study-work`](../contracts/events/study-work) | Study ↔ Work | `DECLARED_NOT_RUNNABLE` | project dependencies/contracts |
| [`contracts/openapi/work`](../contracts/openapi/work) | Work API ↔ Work Server, Web Work | `DISCREPANCY` | Work API/client pages |
| [`contracts/openapi/study`](../contracts/openapi/study) | Study API ↔ Study Server, Study Web | `NOT_FOUND` | Study pages record the gap |
| [`contracts/skill-taxonomy`](../contracts/skill-taxonomy) | repository taxonomy ↔ future domain modules | `VERIFIED` | skill registry |
| [`apps/db-admin-server/app/core/contracts.py`](../apps/db-admin-server/app/core/contracts.py) | DB Admin Server ↔ DB Admin Web | `VERIFIED` | DB Admin API/security pages |

Important boundaries:

- `Study Web` ↔ `Study Server`: Study OpenAPI is currently `NOT_FOUND`;
  do not copy Work request/response fields.
- `Work Web` ↔ `Work Server`: relative `/api/v1` boundary and Work OpenAPI
  status are `DISCREPANCY` until contracts converge.
- `Study` ↔ `Work` events exist as schemas but consumer wiring is not runnable.
- `DB Admin` ↔ Neon targets is a separate control plane, not a Study/Work
  business module boundary.

## Worklog graph

- [`.agents/worklog/README.md`](worklog/README.md) ⇢ contract and mandatory
  preflight.
- [`.agents/worklog/TEMPLATE.md`](worklog/TEMPLATE.md) ⇢ required fields and
  `PRIOR_WORKLOG_REVIEW`.
- [`.agents/worklog`](worklog) ⇢ canonical root.
- [`.agents/worklog/YYYY-MM-DD`](worklog) ⇢ date-based history/current entries.
- [`scripts/select-worklogs.mjs`](../scripts/select-worklogs.mjs) ⇢ exact
  `primary_task_type` selection, date/path ordering and shortage policy.
- Historical worklogs are audit records, not source-of-truth runtime evidence;
  current source, runnable tests and executable contracts take precedence.

## Maintenance rules

1. Update the manifest and this map together when a registered node, page,
   skill, workflow, contract or worklog rule changes.
2. Keep the map limited to registered canonical paths; do not add generated,
   cache, build or unregistered example nodes as runtime context.
3. Preserve `EXPECTED_BEHAVIOR` versus `CURRENT_BEHAVIOR` and mark
   `DISCREPANCY`, `UNWIRED`, `NOT_FOUND` or `CONTEXT_STALE` explicitly.
4. Run the context validator after map/registry changes. A full validation may
   still report pre-existing source drift; it must not report a broken map link
   or missing registry node.

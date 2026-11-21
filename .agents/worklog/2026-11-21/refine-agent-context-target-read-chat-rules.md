---
task_id: "2026-11-21-refine-agent-context-target-read-chat-rules"
date: "2026-11-21"
primary_task_type: "docs"
secondary_task_types: ["coding"]
project_scopes: ["mobile-work", "web-work", "server-work", "server-study", "server-ai", "db-admin"]
cross_scope_dependencies: ["Root agent router -> global context map/manifest -> target tracking, worklog read plan and chat policy -> validator"]
status: "VERIFIED"
---

# Worklog: Siết target, chat im lặng và khai báo file đọc

## LEAF_TARGET_PLAN

Each target is one separately reviewable policy or verification operation.

| Target | Single operation | Acceptance evidence |
|---|---|---|
| Định nghĩa tiêu chí target lá trong agent-control.md | Specify independent leaf/action/result and evidence rules. | Control page prohibits umbrella rows and defines leaf acceptance. |
| Định nghĩa ranh giới chat im lặng trong agent-control.md | Define the allowed exceptions to silent task execution. | Control page bans unsolicited task output and limits exceptions. |
| Định nghĩa quy tắc khai báo read-set trong agent-control.md | Define pre-read path, section, reason and append-before-read requirements. | Control page requires declared paths before file reads or searches. |
| Siết quy tắc chat im lặng trong AGENTS.md | Replace permissive status exception with explicit no-unsolicited-output rule. | Root router says no commentary/status/plan/result/final receipt absent explicit request or higher-priority need. |
| Khai báo read-set trước khi đọc trong AGENTS.md | Add the root bootstrap allowlist and ordered declaration flow. | Root router requires paths and needed sections to be recorded before content reads. |
| Đồng bộ quy tắc chat im lặng trong .agents/AGENTS.md | Mirror the same silent-execution boundary in global context. | Global guidance matches root and agent-control policy. |
| Khai báo read-set trước khi đọc trong .agents/AGENTS.md | Mirror pre-read path declaration and bounded search rules in global context. | Global guidance requires paths before reads and additions before new reads. |
| Thêm READ_PLAN bắt buộc vào worklog README | Define pre-read allowlist, bootstrap, selector and incremental path process. | Contract orders path declaration before content opening/search. |
| Thêm READ_PLAN và LEAF_TARGET_PLAN vào worklog template | Add required path ledger and one-operation plan table. | Template exposes both sections before prior-worklog review. |
| Đăng ký chính sách target và read-plan trong manifest | Register granularity, read-plan, leaf-plan and required fields. | Manifest is valid and workflow registry names the new evidence. |
| Bổ sung kiểm tra chính sách trong context validator | Enforce registered policies and worklog section order. | Validator reports policy/template mismatch. |
| Đồng bộ load flow trong context-map.md | Place read-set declaration before routed file loads and show leaf targets. | Human-readable graph matches root router. |
| Đồng bộ task flow trong project/workflows.md | Align shared task order and worklog workflow with the new policy. | Workflow no longer reads before declaration or permits status chat. |
| Đồng bộ mandatory artifact trong project/INDEX.md | Point mandatory artifact/load references to leaf targets and predeclared reads. | Cross-scope index points to canonical target and read-plan contracts. |
| Đối chiếu context validator với baseline | Compare final validator findings against the captured baseline. | No findings introduced by this task; existing baseline findings remain identified. |
| Đồng bộ thứ tự bootstrap trong context-map.md | Match the canonical load sequence to the root router. | The context map declares bootstrap reads first, then context-map/manifest/control, worklog, selector, cross-scope index and scope sources in the same order. |
| Đồng bộ common flow trong project/workflows.md | Match the common workflow to the root router. | The common flow uses the same bootstrap declaration and load order before worklog preflight and scoped reads. |
| Đối chiếu validator sau đồng bộ bootstrap flow | Run the context validator after the final load-order edits and compare findings with the captured baseline. | Final validator output has no findings introduced by these edits. |

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `node scripts/select-worklogs.mjs --type docs --limit 3`
- selector_result: `READY`; 291 available; 3 selected and read; no shortage.
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-11-21/document-server-and-script-prompts.md`
    - carry_forward: Keep `.agents/target.md` as the sole live tracker; record evidence and remove completed targets only after worklog completion.
  - path: `.agents/worklog/2026-11-21/reconcile-study-screen-completion-status.md`
    - carry_forward: Preserve source/context evidence separately and keep unrelated worktree changes intact.
  - path: `.agents/worklog/2026-11-21/refresh-study-screen-completion-percentages.md`
    - carry_forward: Target rows must be evidence-backed and removed after completion; use exact source evidence over stale context claims.
- shortage: `none`.

## READ_PLAN

This is the bounded read-set for the policy update. No other file content may be opened without first adding its path and reason here.

| Path | Purpose / allowed content | Status |
|---|---|---|
| `AGENTS.md` | Root router and mandatory workflow; supplied in the user context. | `READ_FROM_CONTEXT` |
| `.agents/AGENTS.md` | Global agent context and load-order rules. | `READ` |
| `.agents/context-map.md` | Target/chat/worklog references and context graph. | `READ` |
| `.agents/context-manifest.json` | Registry entries for target, worklog, control and validator resources. | `READ` |
| `.agents/project/INDEX.md` | Mandatory artifact references to target tracking and agent-control. | `READ` |
| `.agents/project/agent-control.md` | Target lifecycle and chat-silence policy. | `READ` |
| `.agents/project/workflows.md` | Shared task/preflight/read ordering that may duplicate the worklog contract. | `READ` |
| `.agents/worklog/README.md` | Preflight, read and worklog authoring order. | `READ` |
| `.agents/worklog/TEMPLATE.md` | Required worklog sections and target/read evidence. | `READ` |
| `.agents/target.md` | Active target table only. | `READ` |
| `scripts/validate-agent-context.mjs` | Target/worklog validation rules relevant to requested policy; validator execution uses only registered paths in the manifest and emits findings, not source contents. | `READ` |
| `scripts/select-worklogs.mjs` | Selector reads worklog metadata to return paths; selected bodies are opened separately. | `READ` |
| `apps/study-client/docs/STUDY2WORK_AGENT_CONTROL_PROMPT.md` | Active/deprecated control text that may duplicate chat or target policy. | `READ` |
| `.agents/worklog/2026-11-21/refine-agent-context-target-read-chat-rules.md` | This active worklog; read back to verify read-set and leaf-target evidence. | `READ` |
| `.agents/worklog/2026-11-21/document-server-and-script-prompts.md` | Selected prior docs task; target/worklog practice. | `READ` |
| `.agents/worklog/2026-11-21/reconcile-study-screen-completion-status.md` | Selected prior docs task; target and evidence handling. | `READ` |
| `.agents/worklog/2026-11-21/refresh-study-screen-completion-percentages.md` | Selected prior docs task; target granularity and completion handling. | `READ` |
| Exact registered paths and resource roots enumerated by `.agents/context-manifest.json` | Baseline/final validator reads are bounded by the already-read manifest; only aggregate findings enter this task's context. | `CHECKED_BY_TOOL` |
| `/tmp/study2work-agent-context-20261121-before.txt` | Baseline validator findings for final comparison. | `READ` |
| `/tmp/study2work-agent-context-20261121-after.txt` | Final validator findings for baseline comparison after context edits. | `CHECKED_BY_TOOL` |

## EXPECTED_BEHAVIOR

- Requirement: Make each live target a plan leaf representing one independently verifiable operation; suppress all unsolicited chat output during task execution; require a finite, justified file read-set before opening source/context files.
- Acceptance: Root/global/specific instructions and worklog template/contract agree; active target table remains exactly three columns; no unrelated context is loaded; validation rules match the new worklog contract.

## TARGET_UPDATES

| Target | From → to | Evidence / reason |
|---|---:|---|
| Tách target thành các mục tiêu lá có thể xác minh | `— → 0%` | Created target for updating leaf-level goal rules and context enforcement. |
| Siết quy tắc im lặng trong chat khi thực thi task | `— → 0%` | Created target for removing unsolicited task/status/final chat output from active guidance. |
| Bắt buộc khai báo read-set trước khi đọc file | `— → 0%` | Created target for a bounded, predeclared file read-set and incremental additions. |
| Đồng bộ quy tắc agent và worklog theo read-set/target mới | `— → 0%` | Created target for synchronizing the router, global/project guidance, worklog contract and validator. |
| Tách target thành các mục tiêu lá có thể xác minh | `0% → superseded` | Replaced the initial umbrella target with the independently verifiable leaf rows below; no completion progress was carried over. |
| Siết quy tắc im lặng trong chat khi thực thi task | `0% → superseded` | Replaced the initial umbrella target with canonical and mirrored silence-policy operations. |
| Bắt buộc khai báo read-set trước khi đọc file | `0% → superseded` | Replaced the initial umbrella target with canonical, router, global-context and worklog read-order operations. |
| Đồng bộ quy tắc agent và worklog theo read-set/target mới | `0% → superseded` | Replaced the initial umbrella target with file-level policy and validation operations. |
| Định nghĩa tiêu chí target lá trong agent-control.md | `— → 0%` | Decomposed the initial umbrella target into the single policy-writing operation required by this task. |
| Định nghĩa ranh giới chat im lặng trong agent-control.md | `— → 0%` | Split the canonical silence boundary into its own verifiable policy operation. |
| Định nghĩa quy tắc khai báo read-set trong agent-control.md | `— → 0%` | Split the canonical read-order rule into its own verifiable policy operation. |
| Siết quy tắc chat im lặng trong AGENTS.md | `— → 0%` | Decomposed the initial umbrella target into the root-router silence-policy edit. |
| Khai báo read-set trước khi đọc trong AGENTS.md | `— → 0%` | Split the root-router read-order edit into its own verifiable operation. |
| Đồng bộ quy tắc chat im lặng trong .agents/AGENTS.md | `— → 0%` | Decomposed the initial umbrella target into the global-context silence-policy edit. |
| Khai báo read-set trước khi đọc trong .agents/AGENTS.md | `— → 0%` | Split the global-context read-order edit into its own verifiable operation. |
| Thêm READ_PLAN bắt buộc vào worklog README | `— → 0%` | Decomposed the initial umbrella target into the worklog-contract edit. |
| Thêm READ_PLAN và LEAF_TARGET_PLAN vào worklog template | `— → 0%` | Decomposed the initial umbrella target into the required worklog-template edit. |
| Đăng ký chính sách target và read-plan trong manifest | `— → 0%` | Decomposed the initial umbrella target into the machine-readable policy registration. |
| Bổ sung kiểm tra chính sách trong context validator | `— → 0%` | Decomposed the initial umbrella target into the validator enforcement operation. |
| Đồng bộ load flow trong context-map.md | `— → 0%` | Decomposed the initial umbrella target into the human-readable load-order update. |
| Đồng bộ task flow trong project/workflows.md | `— → 0%` | Decomposed the initial umbrella target into the shared task-flow update. |
| Đồng bộ mandatory artifact trong project/INDEX.md | `— → 0%` | Added one leaf operation for the cross-scope index references discovered during the declared read. |
| Đối chiếu context validator với baseline | `— → 0%` | Added a separate leaf for final validator comparison after the context edits. |
| Định nghĩa tiêu chí target lá trong agent-control.md | `0% → 80%` | Added the one-operation/evidence definition and the matching worklog target-plan requirement. |
| Định nghĩa ranh giới chat im lặng trong agent-control.md | `0% → 80%` | Added the explicit ban on unsolicited chat output and its narrow exceptions. |
| Định nghĩa quy tắc khai báo read-set trong agent-control.md | `0% → 80%` | Added path/section/reason declaration, bounded search and append-before-read requirements. |
| Siết quy tắc chat im lặng trong AGENTS.md | `0% → 80%` | Root router now suppresses unsolicited commentary, status, plans, findings and completion messages. |
| Khai báo read-set trước khi đọc trong AGENTS.md | `0% → 80%` | Root router now lists bootstrap paths and requires incremental declaration before reading. |
| Đồng bộ quy tắc chat im lặng trong .agents/AGENTS.md | `0% → 80%` | Global guidance now uses the same silence boundary and higher-priority exception. |
| Khai báo read-set trước khi đọc trong .agents/AGENTS.md | `0% → 80%` | Global guidance now requires exact paths before reads and searches. |
| Thêm READ_PLAN bắt buộc vào worklog README | `0% → 80%` | Added bootstrap, selector, exact-path, incremental-read and targeted-range rules. |
| Thêm READ_PLAN và LEAF_TARGET_PLAN vào worklog template | `0% → 80%` | Added both mandatory sections and their path/evidence tables. |
| Đăng ký chính sách target và read-plan trong manifest | `0% → 80%` | Registered schema v5 policies, required worklog fields and workflow evidence. |
| Bổ sung kiểm tra chính sách trong context validator | `0% → 80%` | Validator now checks granularity/read-plan metadata and template section order. |
| Đồng bộ load flow trong context-map.md | `0% → 80%` | Updated the context graph to declare paths before routed reads and list leaf targets. |
| Đồng bộ task flow trong project/workflows.md | `0% → 80%` | Common flow now plans reads first and tracks leaf operations without chat updates. |
| Đồng bộ mandatory artifact trong project/INDEX.md | `0% → 80%` | Cross-scope index now points to pre-read and leaf-target requirements. |
| Đối chiếu context validator với baseline | `0% → 30%` | Captured the pre-change validator baseline; first final comparison found no new or resolved findings. |
| Định nghĩa tiêu chí target lá trong agent-control.md | `80% → 100%` | `agent-control.md` section 1 defines one operation, independent evidence and removal after evidence; the target plan and live rows match exactly. |
| Định nghĩa ranh giới chat im lặng trong agent-control.md | `80% → 100%` | `agent-control.md` section 2 lists prohibited unsolicited content and the narrow response exceptions. |
| Định nghĩa quy tắc khai báo read-set trong agent-control.md | `80% → 100%` | `agent-control.md` section 3 requires path/section/reason before reads, append-before-read and declared-path-only searches. |
| Siết quy tắc chat im lặng trong AGENTS.md | `80% → 100%` | Root section 1.1 bans unsolicited status, plan, reading summary and completion chat. |
| Khai báo read-set trước khi đọc trong AGENTS.md | `80% → 100%` | Root sections 2.1–2.2 define the bootstrap allowlist, incremental read plan and selector path order. |
| Đồng bộ quy tắc chat im lặng trong .agents/AGENTS.md | `80% → 100%` | Global context section “Quy tắc target, giao tiếp và read-set” mirrors the silent-execution boundary. |
| Khai báo read-set trước khi đọc trong .agents/AGENTS.md | `80% → 100%` | The same global section requires declared paths before reads and targeted searches. |
| Thêm READ_PLAN bắt buộc vào worklog README | `80% → 100%` | README defines bootstrap, selector, incremental path and bounded read order. |
| Thêm READ_PLAN và LEAF_TARGET_PLAN vào worklog template | `80% → 100%` | Template exposes both required tables before prior-worklog review; validator checks their order. |
| Đăng ký chính sách target và read-plan trong manifest | `80% → 100%` | Manifest registers granularity, read-plan, leaf-plan and required fields; final validator adds no finding. |
| Bổ sung kiểm tra chính sách trong context validator | `80% → 100%` | Validator checks target schema/policy, worklog metadata and section order; baseline comparison shows 0 introduced findings. |
| Đồng bộ load flow trong context-map.md | `80% → 100%` | Context map describes predeclared reads, leaf targets, selector path declaration and scoped loading. |
| Đồng bộ task flow trong project/workflows.md | `80% → 100%` | Shared workflow orders read declaration, worklog, leaf targets, focused work and silent chat. |
| Đồng bộ mandatory artifact trong project/INDEX.md | `80% → 100%` | Project index identifies READ_PLAN, LEAF_TARGET_PLAN, silent execution and three-column active rows. |
| Đối chiếu context validator với baseline | `30% → 100%` | Final comparison: 1,823 baseline and final findings, 0 introduced, 0 resolved. |
| Đồng bộ thứ tự bootstrap trong context-map.md | `— → 0%` | Final consistency readback found the context-map sequence differed from the root router order. |
| Đồng bộ common flow trong project/workflows.md | `— → 0%` | Final consistency readback found the workflow preamble did not state the same canonical order as the root router. |
| Đồng bộ thứ tự bootstrap trong context-map.md | `0% → 80%` | Context-map sequence now follows root router order; static subsequence check passes. |
| Đồng bộ common flow trong project/workflows.md | `0% → 80%` | Workflow preamble/common flow now follows root router order; static subsequence check passes. |
| Đối chiếu validator sau đồng bộ bootstrap flow | `— → 0%` | Added the required final validation operation after discovering and correcting the flow-order mismatch. |
| Đồng bộ thứ tự bootstrap trong context-map.md | `80% → 100%` | Static order check confirms context-map matches root router sequence; final validator comparison adds 0 findings. |
| Đồng bộ common flow trong project/workflows.md | `80% → 100%` | Static order check confirms common workflow matches root router sequence; final validator comparison adds 0 findings. |
| Đối chiếu validator sau đồng bộ bootstrap flow | `0% → 100%` | Final validator comparison after the load-order edits: 1,823 findings in baseline and final output; 0 introduced, 0 resolved. |

## CURRENT_BEHAVIOR

- Source/config (before this task): The tracker used the three-column schema, but target granularity was not explicitly constrained; agent guidance allowed broader chat output and did not require a declared read-set before file reads.
- Runnable tests: Not run; this is an agent-context documentation change. Context validation is the applicable executable check.
- Runtime wiring: `.agents/context-manifest.json` registers canonical context pages and `scripts/validate-agent-context.mjs` validates their structure and links.

## SOURCE_TRACE

```text
user policy -> root router -> global/project control -> predeclared worklog read-set and target leaf list -> validator
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| Current target table vs requested leaf detail | Table only exposes target name/progress; current guidance does not forbid umbrella targets or require one independently verifiable leaf per row. | `POLICY_GAP` | Add explicit leaf decomposition rules while preserving the current three-column schema. |
| Current silent-chat rule vs requested suppression | Current rule suppresses automatic progress but allows chat in broader cases; user requests no task output unless required. | `POLICY_GAP` | Narrow exceptions to explicit user question/clarification or higher-priority requirement. |
| Current worklog vs read discipline | Template has no mandatory declared file list or amendment-before-read rule. | `POLICY_GAP` | Add `READ_PLAN` and require updates before new file reads. |

## CHANGES

- Files changed: `AGENTS.md`; `.agents/AGENTS.md`; `.agents/context-map.md`; `.agents/context-manifest.json`; `.agents/project/INDEX.md`; `.agents/project/agent-control.md`; `.agents/project/workflows.md`; `.agents/target.md`; `.agents/worklog/README.md`; `.agents/worklog/TEMPLATE.md`; `scripts/validate-agent-context.mjs`; this worklog.
- CONTEXT_UPDATES: Added action-level target requirements, silent-by-default chat, mandatory predeclared read plans, manifest metadata, validator checks and a consistent bootstrap load order.
- Context pages changed: `.agents/AGENTS.md`; `.agents/context-map.md`; `.agents/project/INDEX.md`; `.agents/project/agent-control.md`; `.agents/project/workflows.md`; `.agents/worklog/README.md`; `.agents/worklog/TEMPLATE.md`; `.agents/context-manifest.json`.
- Assumptions: Explicit user requests, blocker questions that cannot be inferred, and higher-priority system/developer/tool requirements remain valid chat exceptions. Selector/validator reads are bounded machine operations declared in advance; they do not load their underlying bodies into model context.
- Target progress updates and completion evidence: see `TARGET_UPDATES`.

## VERIFICATION

| Command | Result | Status |
|---|---|---|
| `node scripts/select-worklogs.mjs --type docs --limit 3` | `READY`; 3 same-type logs selected and reviewed; no shortage. | `VERIFIED` |
| `node scripts/validate-agent-context.mjs` (baseline before edits) | Exit 1; 1,823 pre-existing findings captured in `/tmp/study2work-agent-context-20261121-before.txt`. | `BASELINE_INVALID` |
| `node scripts/validate-agent-context.mjs` (after context/worklog edits) | Exit 1; 1,823 findings, 0 introduced, 0 resolved against baseline. Existing repository context issues remain. | `BASELINE_INVALID` |
| Target/plan static check | 15 active rows, 15 planned leaves, exact name match; three-column schema and sequential numbering confirmed. | `VERIFIED` |
| Context-flow order check | Root router, context map and common workflow preserve the same bootstrap → context map → manifest/control → worklog → selector → scope order. | `VERIFIED` |

## HANDOFF

- Remaining blockers: Validator findings remain from the existing repository baseline; this task introduced no new finding and resolved no baseline finding. Affected areas are unrelated registered context/source coverage, including DB Admin and other pre-existing scope drift.
- Next owner/action: None for this task; the requested agent-context policy is implemented. Keep the final target table empty after completion evidence is recorded.

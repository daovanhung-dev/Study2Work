---
task_id: "2026-11-12-add-study-web-screen-rules-workflow"
date: "2026-11-12"
primary_task_type: "docs"
secondary_task_types: []
project_scopes: ["web-work", "server-study"]
cross_scope_dependencies: ["Study Web screen demo -> Study Server DB fixture/schema source when that screen requires persisted data"]
status: "PARTIAL"
---

# Worklog: Bổ sung rule và workflow cho Study Web screen

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `/home/daovanhung/.local/opt/node-v22.23.4/bin/node scripts/select-worklogs.mjs --type docs --limit 3`
- selector_result: `READY`; 276 worklog cùng loại; đã chọn và đọc đủ 3.
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-11-11/add-study-fe-screen-api-context.md`
    - carry_forward: Mọi task Study FE phải đọc `list_screen.md` và `list_endpoint.md`, rồi ghi screen/API scope; DD/catalog không chứng minh runtime.
  - path: `.agents/worklog/2026-11-11/list-study-api-endpoints.md`
    - carry_forward: Endpoint catalog có 103 ID và được xác định là design/DD reference; API/source/DD có các gap cần giữ thành `DISCREPANCY` hoặc `SOURCE_REQUIRED`.
  - path: `.agents/worklog/2026-11-11/load-study-server-context.md`
    - carry_forward: Tách expected DD khỏi current source; Study Server context có `CONTEXT_STALE`, nhưng task hiện tại không phụ thuộc server implementation.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Trong agent context Study Web ghi rõ feature group/screen folder structure, group route files, per-group layouts, và workflow đầy đủ để implement, demo, verify rồi sửa màn hình theo DD và ảnh minh họa.
- Canonical contract/approved DD: User request trong task này; Study screen inventory/DD package là input thiết kế, không phải bằng chứng runtime. DB fixture use is conditional on a specific screen and must follow current Study DB source/schema evidence.
- Study FE scope: screens=none; APIs=none — đây là task bổ sung context, không triển khai một màn hình/API.

## MILESTONES

| Weight | Cumulative progress when achieved | Objective / acceptance criterion | Status |
|---:|---:|---|---|
| 35% | 35% | Hoàn tất router/worklog preflight và đọc rule/source Study Web hiện tại; ghi nhận xung đột cần xử lý. | `DONE` |
| 65% | 100% | Cập nhật các trang `.agents` đã wire với folder/layout/route/workflow rules; kiểm tra registry, links, worklog và context validator. | `DONE` |

## CURRENT_BEHAVIOR

- Source/config: Trước task, context manifest đã wire `.agents/web-work/study/{AGENTS,INDEX}.md` và `.agents/web-study/{design,frontend-rules}.md`; `frontend-rules.md` mô tả `features/<domain>/<capability>` và `domain/`, trái với cấu trúc 4 folder mới. Current `apps/study-client` là Angular 22 standalone scaffold, routes rỗng, feature group folders còn placeholder (`auth`, `guest`, `system`, `student`, `mentor`, `admin`), không có screen implementation. DD catalog có 83 screen ID; endpoint catalog có 103 API rows. Ví dụ SH-02 có 8 DD Markdown, image README, clean/numbered PNG và `screen_stitch/.../code.html`; DD status ghi BLOCKED/RUNTIME NOT VERIFIED. Project DB context says checked-in Study DDL is not live-schema proof; server scope uses sync SQLAlchemy with caller-owned transaction boundaries, and source evidence must be rechecked for fixture setup/cleanup. `screen-index.md` còn dấu vết stack/path cũ; workflow mới yêu cầu coi index là locator và ghi discrepancy khi mâu thuẫn source/package.
- Runnable tests: Chưa kiểm tra; app tests không thuộc phạm vi thay đổi context.
- Runtime wiring: Task chỉ cập nhật agent context; không thêm màn hình, route, service hoặc dữ liệu.

## SOURCE_TRACE

```text
root router -> docs preflight -> Study Web context rules and source -> update registered .agents pages -> context validator
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| Proposed screen folder rules vs existing architecture | Existing frontend rules currently describe a `domain/` folder; user request specifies four screen folders: `data-access/`, `models/`, `pages/`, `ui/`. | `NEEDS_RECONCILIATION` | Apply the latest user requirement; preserve current responsibilities only where compatible, and do not add a fifth screen folder. |
| Existing role group tree | `gui/architech.md` and current placeholder directories split `auth/` and `system/`; user request groups Shared/Auth/System together before Guest/Student/Mentor/Admin. | `SOURCE_CHANGED / EXPECTED_BEHAVIOR` | Encode the requested canonical future structure in `.agents`; no app folders are changed in this documentation task. |
| Stale parent stack note | `.agents/web-work/architecture.md` says Study Web is Vue 3/Vite; current package and Angular source show Angular 22 standalone. | `DISCREPANCY / CONTEXT_STALE` | Correct the Study-specific statement in the registered parent context while preserving Work Web React context. |
| Legacy Study stack/path references in docs and validator snapshot | `apps/study-client/docs/dd_screens/screen-index.md` still contains old Vue/path references; validator compares tracked roots with the manifest source commit and reports Study source drift. | `DISCREPANCY / CONTEXT_STALE` | Keep this task scoped to `.agents`; the new screen workflow treats the index as a locator and prioritizes current source/package evidence. Do not reset the manifest source commit for all scopes. |

## CHANGES

- Files changed: `.agents/web-study/frontend-rules.md`; `.agents/web-work/study/AGENTS.md`; `.agents/web-work/study/INDEX.md`; `.agents/web-work/study/workflows/screen-implementation.md`; `.agents/web-work/architecture.md`; `.agents/web-work/AGENTS.md`; `.agents/web-work/conventions.md`; `.agents/web-work/workflows/README.md`; `.agents/context-manifest.json`; `.agents/context-map.md`; `.agents/project/workflows.md`.
- CONTEXT_UPDATES: Registered the `study-web-screen-coding` workflow and wired it into the Study Web router, common workflow table, and manifest. Added group/screen folders, per-group route/layout, reuse, event/API/data flow, full DD/image/HTML analysis, plan-before-code, test/demo, and disposable database fixture cleanup rules. Corrected active parent context from Study Vue to Study Angular while preserving Work React rules.
- Context pages changed: `.agents/web-study/frontend-rules.md`; `.agents/web-work/study/AGENTS.md`; `.agents/web-work/study/INDEX.md`; `.agents/web-work/study/workflows/screen-implementation.md`; `.agents/web-work/architecture.md`; `.agents/web-work/AGENTS.md`; `.agents/web-work/conventions.md`; `.agents/web-work/workflows/README.md`; `.agents/context-manifest.json`; `.agents/context-map.md`; `.agents/project/workflows.md`.
- Assumptions: User's `Shared / Auth / System` category maps to the shared feature group; screen folder IDs use compact names such as `SH02` corresponding to catalog ID `SH-02`.

## VERIFICATION

| Command/read | Result | Status |
|---|---|---|
| Root router, `.agents/AGENTS.md`, `.agents/context-map.md` | Confirmed docs workflow, mandatory exact-type worklog preflight, context registry ownership, and requirement to run context validator after context changes. | VERIFIED_STATIC_ONLY |
| Worklog selector and selected prior worklogs | `READY`, 3 of 276 matching docs worklogs selected and read. | VERIFIED |
| DD package, image README/PNGs, and screen_stitch reference for SH-02 | Read all eight DD sections and image README; visually compared clean/numbered images and inspected matching HTML/marker data. Clean image is blank; numbered image shows the mockup; DD marks the screen blocked/runtime not verified. | VERIFIED_STATIC_ONLY |
| `/home/daovanhung/.local/opt/node-v22.23.4/bin/node scripts/validate-agent-context.mjs` | Exit 1, `AGENT_CONTEXT_INVALID`, 83 repository-wide findings: missing DB Admin context/source, 33 orphan `create_dd_screen` resources, legacy DB Admin links/contracts, and tracked-root `CONTEXT_STALE` snapshots including Study Web. No finding names the new workflow page or reports a Study Web page/registry link error. | BASELINE_INVALID |
| `git diff --check`; JSON parse of `.agents/context-manifest.json`; targeted active-context Vue scan | Passed; manifest is valid JSON and no active Web context describes Study as Vue. Historical worklogs were left unchanged. | VERIFIED |
| Application tests/build | Not requested for context-only change. | NOT_RUN |

## HANDOFF

- Remaining blockers: Repository-wide context validator remains invalid for existing DB Admin omissions, orphan DD skill resources, legacy links/contracts, and source drift. These findings are outside this Study Web context change.
- Next owner/action: Task is complete at 100% for the requested Study Web rules/workflow. Future per-screen implementation must follow the newly registered workflow and record any DD/source discrepancy.

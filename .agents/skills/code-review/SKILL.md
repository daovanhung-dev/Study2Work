---
name: code-review
description: Perform a read-only, evidence-backed review of a requested code diff or named code path for repository-rule compliance, reuse, maintainability, and security. Use only when the user explicitly asks for code review, PR/diff review, or a code-path/module audit.
metadata:
  short-description: Read-only code review for Study2Work
---

# Code Review

Review only when the user explicitly asks for a code review, PR/diff review,
rule-compliance review, security review, or audit of a named code path/module.
Do not run this automatically after coding tasks.

This skill covers Mobile Work, Web Work, Work Server, Study Server, AI Server,
and DB Admin. Use the relevant scope and its current repository rules; do not
carry one application's architecture or conventions into another.

## Read-only boundary

- Do not edit reviewed source, tests, configuration, or documentation; do not
  format, autofix, generate code, apply patches, or implement suggested fixes.
- Do not run tests, builds, linters, or scanners. Read relevant test/config
  source and report verification gaps instead.
- Do not change the index, HEAD, branch, or PR state. Do not post review
  comments, commit, push, or dispatch another reviewer.
- Follow the repository's mandatory worklog policy. For a review task, the
  worklog is the only file write allowed and must remain an audit record; this
  does not authorize changing the reviewed code.

## Load context and resolve the target

1. Follow root `AGENTS.md`, `.agents/AGENTS.md`, and `.agents/context-map.md`.
   Classify the task as `review`; run and read the exact-type worklog preflight.
2. Resolve the named scope from `.agents/context-manifest.json`; read its
   `AGENTS.md` and `INDEX.md` when present. Load only the conventions, contracts,
   source pages, call sites, side-effect paths, and tests related to the target.
   If a declared scope page is missing, record `NOT_FOUND`, use current source
   evidence where available, and do not recreate the missing context page.
3. Prefer the explicitly requested diff or revision range. If the user names a
   base branch, compare against its merge base without checking out or moving
   repository state. Include staged, unstaged, and relevant untracked files
   when the user asks to review the current working-tree changes; state the
   included range and files in the report.
4. If there is no reviewable diff, review the path/module named by the user as
   a current-state audit. If the target or comparison range cannot be resolved,
   ask one concise clarification instead of guessing.
5. For a diff review, report a defect only when it is supported by current
   source/call-path evidence, meaningful, actionable, and introduced by that
   diff. For a path/module audit, label findings as current-state issues; do not
   claim they were introduced by a change.

## Review lenses

Read [the review checklist](references/review-checklist.md) and [the report
format](references/report-format.md). Check all four lenses, but report only
qualifying findings:

1. **Repository rules:** compare against applicable AGENTS instructions,
   approved requirements/contracts, and established scope conventions.
2. **Reuse:** check for relevant existing helpers/components and meaningful
   duplicated logic; do not recommend abstraction solely to reduce line count.
3. **Cleanliness and maintainability:** flag only concrete problems that make
   behavior harder to understand, change, or operate.
4. **Security:** trace the relevant trust boundary and access/data flow; do not
   infer a vulnerability from a pattern name without demonstrating impact.

Inspect enough surrounding code and relevant tests to confirm a finding. Keep
file/line citations minimal and, for diff reviews, make each cited range overlap
the reviewed change where possible. Continue through the complete target after
finding an issue. Do not report speculative concerns, pre-existing defects as
regressions, or style preferences that are not repository rules.

## Severity

- `P0` — sự cố nghiêm trọng, chặn phát hành hoặc làm hỏng chức năng diện rộng.
- `P1` — lỗi nghiêm trọng cần ưu tiên xử lý.
- `P2` — lỗi có ảnh hưởng rõ đến tính đúng, bảo mật hoặc khả năng bảo trì; nên sửa.
- `P3` — lỗi tác động thấp nhưng có căn cứ và đáng xử lý.

Assign severity by demonstrated impact and affected scenario, not by how easy
the fix seems. Do not create a finding just to fill a severity category.

## Final response

Write in clear, concise Vietnamese. Report the reviewed target and the four
criterion statuses, then actionable findings in severity order. Every finding
must identify whether it was caused by the diff or belongs to the current
state, exact file/line, affected scenario, impact, evidence, and a short
direction for resolution. Suggested direction is review guidance only; never
apply it.

Use `Không thấy vấn đề trong phạm vi đã review` only when the relevant evidence
was available and reviewed. Use `Chưa đủ bằng chứng` when source, contract,
scope, or comparison data prevents a reliable conclusion. If there are no
qualifying findings, say so plainly and summarize material limits, including
that tests were not run. Never describe a scoped review as proof that the whole
system is secure.

## Acceptance scenarios

- **Diff review:** every reported issue is evidenced and introduced by the
  requested diff; pre-existing concerns are not presented as regressions.
- **Path/module audit:** each issue is labeled as current-state behavior, not
  attributed to a change that was not reviewed.
- **No qualifying issues:** state that no actionable issue was found in the
  reviewed scope and provide the four criterion statuses.
- **Missing evidence:** use `Chưa đủ bằng chứng` and name the missing source,
  rule, contract, or comparison data.
- **Read-only boundary:** do not edit reviewed files or run tests; return the
  review in chat without posting PR comments.

## Official references

- OpenAI Codex read-only, defect-first sample:
  <https://github.com/openai/codex/blob/main/codex-rs/skills/src/assets/samples/review-agent/SKILL.md>
- OpenAI Plugins code reviewer prompt:
  <https://github.com/openai/plugins/blob/main/plugins/superpowers/skills/requesting-code-review/code-reviewer.md>

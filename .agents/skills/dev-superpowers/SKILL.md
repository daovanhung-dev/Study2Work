---
name: dev-superpowers
description: Guide a Study2Work task from a DD, BD, or developer description through approved scope, spec, plan, code and tests, then remind the developer to create a PR. Use for the full staged development workflow; do not use to author a DD or for a standalone code review.
---

# Dev Superpowers

Guide one task from supplied design or developer requirements to reviewed code
and tests. Apply the repository router, worklog preflight, scope pages, and
registered contracts at each stage. Keep requested behavior from BD, DD and
developer decisions separate from current source, runnable tests, and
executable configuration. A document's existence does not prove runtime
wiring. Record `DISCREPANCY`, `UNWIRED`, `NOT_FOUND`, and unresolved decisions.
Use [artifact requirements](references/artifacts.md) when authoring `SPEC.md`
or `PLAN.md`.

Mặc định trình bày phạm vi, câu hỏi cần quyết định, `SPEC.md`, `PLAN.md`,
tóm tắt phê duyệt và bàn giao bằng tiếng Việt. Giữ nguyên tên file, mã yêu cầu
và test, ký hiệu code, đường dẫn, giá trị HTTP và nhãn trạng thái. Nếu developer
yêu cầu rõ một ngôn ngữ khác, làm theo yêu cầu đó.

Ở mỗi mốc, ghi các quyết định, điểm chưa xác minh, vấn đề cần giải quyết và
phê duyệt còn chờ vào đúng artifact theo [artifact requirements](references/artifacts.md).
Nêu lại trong chat những mục còn mở, kèm hiện trạng, bằng chứng, 2-3 phương án
khả thi, hệ quả và phương án đề xuất. Cho developer chọn một phương án hoặc tự
nhập phương án khác; nếu giao diện hỏi đáp đã có ô nhập tự do thì không thêm
lựa chọn `Other` giả. Không tự chọn thay developer và không hỏi lại quyết định
đã duyệt khi revision liên quan chưa đổi.
Nếu các phương án khác nhau ở vòng đời tài nguyên hoặc luồng xử lý, giải thích
cụ thể ai tạo, lúc nào tạo, phạm vi tái sử dụng, ai đóng, lúc nào đóng, cách xử
lý khi lỗi và thay đổi cần ở caller. Dùng ví dụ ngắn khi tên phương án như
"tự động" hoặc "tường minh" chưa đủ để developer hiểu và chọn.

Keep one trace chain for every requirement: BD/DD section or explicit developer
decision -> `SPEC.md` requirement ID -> `PLAN.md` step and test-case IDs ->
changed code and executable tests -> final handoff. Before revising any artifact or code,
identify which links and downstream artifacts the change affects. Follow the
change rules in the [artifact requirements](references/artifacts.md); an approval applies to its
recorded revision, not to later material changes.

## Stage 1: intake and readiness

1. Accept one or more of: task DD path, BD/BRD path, or the developer's own task
   description. No DD is mandatory. Verify supplied paths and read all relevant
   source material, including required linked files. Record each source and
   revision; do not imply an absent DD or BD exists.
2. Trace relevant current source, callers, callees, contracts, data and external
   effects, responses, consumers, and tests. Check whether the inputs establish
   scope, behavior, authorization, data rules, acceptance criteria, and affected
   boundaries well enough to write a testable spec. When sources conflict or a
   decision is missing, mark it `NEEDS_DECISION` and ask the developer. Use a
   short multiple-choice question with consequences when there are real options;
   use a free-text question when no supported options can be offered. Never
   invent missing business, API, schema, authorization, test expectation, or
   error behavior. Use current source to explain options, not to silently
   choose an unspecified requirement.
3. Present the proposed scope, direct and downstream impact, source conflicts,
   unresolved questions, and readiness status. **Wait for explicit developer
   approval of the scope and resolved decisions before writing `SPEC.md`.** If
   requirements are still insufficient, continue asking; silence is not approval.
4. Reuse DD authoring skills only if the developer asks to create or revise a
   DD. Use `dev-reviewer` only for a separate requested review when available.

## Stage 2: spec

Create `SPEC.md` in the task's existing documentation directory. If there is no
task directory, select a task-specific location from repository conventions or
ask the developer when ambiguous. Follow the artifact requirements for scope,
acceptance criteria, evidence, affected
callers/consumers, data and contract effects, discrepancies, and open decisions.
Do not mark a spec ready for approval while a required decision remains open.
Give the developer the spec path and a concise decision list. **Wait for explicit
approval of this spec revision before planning.** Record the
approver and exact approved revision in the task worklog. A later material BD,
DD, description, scope, or contract change returns the task to spec review.

## Stage 3: plan

Create `PLAN.md` from the approved `SPEC.md`, citing its exact revision. Map
each required behavior to the smallest file and function changes, affected
callers/consumers, contract and data implications, dependency order, regression
checks, and rollback or compatibility steps where relevant. Add a test-case
matrix derived from supplied BD/DD criteria, the developer's decisions, spec
requirements, and the planned
change impact. Give each case a stable ID, scenario, expected result, test
layer/path, and linked requirement and plan-step IDs. Cover the main path plus
relevant invalid, boundary, authorization, failure, side-effect, and regression
paths; use risk and evidence to choose cases rather than a fixed count or
coverage percentage. Explicitly mark areas inspected but not yet verified.
Show any choice that changes scope or behavior. **Wait for explicit developer
approval of this plan revision before coding.** Record the approval; do not
ask again for an unchanged revision already approved in the conversation.

## Stage 4: code and tests

Before each function change, recheck its callers, callees, authorization,
validation, persistence/external effects, response and error behavior, and
affected tests against the approved plan. Implement the smallest scoped change;
avoid unrelated refactors and preserve existing contracts unless the approved
spec calls for a change. Create or update executable tests for the approved
test cases using the target scope's test conventions; include a regression case
for each confirmed bug. Map each case ID to its test path/function and actual
result. Update the correct context pages when source, contract, or conventions
change. After coding, rerun the approved test cases plus relevant existing
regression tests and the repository context validator when required; report
each case as `PASS`, `FAIL`, `NOT_RUN`, or `BLOCKED` with evidence. Review the diff
against `PLAN.md` and inspect each affected consumer. If a new impact or
material discrepancy appears, pause that dependent change and return to the
relevant approval gate. Report unresolved regression risk rather than claiming
the change cannot break anything. Audit the full input -> spec -> plan ->
code/test chain for stale revisions, missing IDs, unrun cases, and unexplained
diff lines. Resolve material gaps or report them as blockers. **Show the
completed code diff, test results, and remaining risks; wait for explicit
developer approval before the final handoff.**

When implementation reveals a plan change, record the proposed amendment and
its linked requirement IDs before changing the dependent code. Update the spec
only if requirements, scope, acceptance criteria, or contracts change. Resume
after the affected approval gate is satisfied; never rewrite an approved plan
to make an unapproved code deviation look preapproved.

## Stage 5: PR reminder

After the developer approves the code and test results, state the approved
source, spec and plan revisions and test summary, then remind them to create the PR/MR
themselves. Do not push a branch or create, approve, or merge a PR/MR as part of
this workflow. If the developer later requests one of those actions separately,
handle that request under its own authorization and repository rules.

At every stage, state the current artifact or result, revision, readiness and
approval state, remaining questions, and next action. Continue only after that
stage's explicit approval; never infer approval from a prior stage or silence.

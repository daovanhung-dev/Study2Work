# Development workflow artifacts

The developer can supply a DD, BD/BRD, a free-text task description, or a
combination. Record the exact supplied sources and their revisions. If two
sources conflict or a required behavior is absent, ask the developer and record
the explicit decision; do not choose a source silently. Keep `SPEC.md` and
`PLAN.md` in a task-specific documentation directory chosen from repository
conventions. Link to source files rather than copying them wholesale.
Record an exact artifact revision for each approval: a commit SHA if committed,
otherwise a content hash. State `PENDING` until the owner explicitly approves.
Mặc định viết phần trình bày phạm vi, nội dung `SPEC.md` và `PLAN.md` bằng
tiếng Việt, kể cả bảng, tiêu chí chấp nhận, test case và ghi chú phê duyệt.
Giữ nguyên định danh kỹ thuật và chuỗi API/code chính xác.

## Sổ quyết định, vấn đề và xác minh

Ở mỗi mốc, duy trì mục riêng cho các vấn đề ảnh hưởng tác vụ: ID ổn định, hiện
trạng và bằng chứng, artifact chịu trách nhiệm, trạng thái (`NEEDS_DECISION`,
`NOT_VERIFIED`, `PENDING_APPROVAL`, `APPROVED` hoặc trạng thái kết thúc), có chặn
bước tiếp theo hay không, phương án đề xuất và hệ quả của từng phương án, quyết
định đã chọn cùng nguồn/phê duyệt, và hành động tiếp theo. Chỉ ghi vấn đề có
bằng chứng hoặc quyết định thực sự cần thiết; không tạo câu hỏi giả cho sự thật
đã xác minh.

- Phần trình bày scope ghi quyết định về ranh giới và readiness trước SPEC.
- `SPEC.md` ghi vấn đề về yêu cầu, contract, validation, lỗi, quyền truy cập và
  những xác minh cần thiết để chốt hành vi. Quyết định bắt buộc còn mở chặn
  phê duyệt SPEC.
- `PLAN.md` ghi lựa chọn triển khai, test, tương thích, môi trường và xác minh
  còn thiếu. Liên kết đến ID trong SPEC khi có quan hệ; không sao chép cùng
  một vấn đề vào cả hai file. Quyết định bắt buộc còn mở chặn phê duyệt PLAN.
- Tại mỗi mốc phê duyệt, tóm tắt trong chat các mục còn mở và trạng thái phê
  duyệt, không buộc developer phải tự tìm trong file. Với mỗi câu hỏi có nhiều
  cách hợp lệ, đưa 2-3 lựa chọn loại trừ nhau, nêu hệ quả và đánh dấu phương
  án đề xuất; luôn cho phép developer nhập phương án riêng. Nếu dùng giao diện
  có sẵn ô nhập tự do, không thêm lựa chọn `Other`; trong chat thông thường,
  ghi rõ developer có thể trả lời bằng phương án riêng.
- Khi developer chọn phương án riêng, đánh giá tác động tới scope, SPEC, PLAN
  và revision đã duyệt trước khi tiếp tục. Không diễn giải việc im lặng hoặc
  phê duyệt ở mốc trước thành quyết định cho mục đang mở.
- Với phương án về client, connection, transaction, session hoặc tài nguyên
  tương tự, ghi rõ sự kiện tạo, phạm vi dùng chung/tái sử dụng, sự kiện đóng,
  người chịu trách nhiệm đóng, hành vi khi lỗi hoặc caller quên đóng, và tác
  động tới caller hiện có. Nếu cần, kèm ví dụ gọi ngắn cho từng phương án;
  không dùng các nhãn "tự động"/"tường minh" thay cho mô tả hành vi.

## Intake readiness record

Before `SPEC.md`, show which source files or description were supplied, the
proposed project scope, affected boundaries, missing information, and decisions.
Ask concrete multiple-choice questions when supported options exist; use
free-text questions when they do not. Record explicit approval of this scope
and the resolved decisions. If any required answer is missing, keep readiness
`BLOCKED` and do not start the spec.

## `SPEC.md` from approved inputs and current source

- Task ID; supplied BD/DD paths, revisions and statuses or the developer's
  description; approved intake decisions; scope owner; relevant contracts.
- Chosen scope and exclusions: affected app(s), endpoints/UI, database,
  integrations, and which choices the owner made.
- Expected behavior from the approved inputs versus current behavior from source and
  verified tests; label each discrepancy and missing source.
- Requirements and acceptance criteria with stable IDs, concrete inputs,
  outputs, authorization, validation, errors, and side effects.
- For each requirement ID, link the exact BD/DD section or explicit developer
  decision that supports it. Assign stable spec IDs without adding new business
  behavior when the source has no IDs.
- Impact map: changed surface, direct callers/callees, downstream consumers,
  contract or schema effects, affected tests, and evidence links. Mark unverified
  impact explicitly instead of assuming it is safe.
- Open decisions and blockers with recommended options and consequences; a
  required open decision blocks spec approval.
- Approval record: `PENDING` or `APPROVED`, approver, approved revision, and
  decision date. Approval of a previous revision does not approve new scope.

## `PLAN.md` from the approved spec

- Link and approved revision of `SPEC.md`; do not plan from an unapproved spec.
- For each requirement ID: exact file/function to change, why, the expected
  behavior after the edit, and the caller/consumer or contract it affects.
- Give each implementation step a stable ID and link it to one or more spec
  requirement IDs. Link planned verification to the same IDs.
- Order of edits and dependencies; migration, compatibility, and rollback
  handling when data or public contracts change.
- Regression map: existing behavior at risk, focused checks, integration checks
  where relevant, and how to inspect failures. Distinguish tests actually run
  from planned commands.
- Test-case matrix with stable `TC-*` IDs: linked BD/DD criterion or developer
  decision, spec requirement
  and plan step; setup/input, action, expected output/error/side effect, test
  layer, planned test path, and existing/new status. Select cases for success,
  relevant invalid/boundary/auth/failure paths, and behavior that could regress
  in callers or consumers. Explain any uncovered high-risk criterion.
- Known risks, unverified areas, and any choice that would expand the spec.
- Approval record: `PENDING` or `APPROVED`, approver, approved revision, and
  decision date.

The code stage must compare the final diff with the approved plan, rerun the
approved test cases after coding, and report each actual result before asking
the developer to approve the code and tests. A passing test suite reduces risk
but does not prove that unrelated behavior cannot regress.

## Change propagation

Keep the trace chain `BD/DD section or developer decision -> SPEC requirement -> PLAN step and TC case
-> code path/function and test path/function -> result`. Store links or exact paths beside each ID so a
reader can follow it in either direction. At each change, list the affected IDs,
artifacts, and approved revisions before editing downstream material.

| Changed item | Required reconciliation |
|---|---|
| BD, DD, or developer decision | Recheck linked spec requirements. If behavior, scope, or acceptance criteria change, revise `SPEC.md`, then affected `PLAN.md` steps, test cases and code/tests; obtain scope and spec approval before plan approval. Do not silently alter a source document to match current code. |
| `SPEC.md` | Recheck every linked plan step, test case and affected code/test. A material spec change makes the current plan stale; revise and reapprove both stages in order. |
| `PLAN.md` | Recheck its linked spec IDs and test cases. If it only changes the implementation approach, verification, or file list, keep the spec as is and reapprove the material plan revision before dependent coding. If it changes required behavior or scope, revise and reapprove the spec first. |
| Code or tests | Compare with the approved plan and test-case matrix; check affected callers/consumers. Record small implementation details in the worklog; for a material deviation, propose a plan amendment and obtain approval before dependent edits. Revise the spec first if behavior or contract changes. |

An editorial correction can keep earlier approval when it does not alter
behavior, scope, risk, or verification. Record the previous approved revision,
new revision, and reason in the worklog so the approval history remains clear.
For a material change, mark the affected artifact `PENDING` and do not rely on
its earlier approval. Before the final handoff, reconcile the final diff and
test results to test-case, plan-step and spec requirement IDs. Mark each case
`PASS`, `FAIL`, `NOT_RUN`, or `BLOCKED` with evidence; report uncovered or
unresolved links. After explicit approval of the code and test results, remind
the developer to create the PR/MR themselves; the agent does not create it.

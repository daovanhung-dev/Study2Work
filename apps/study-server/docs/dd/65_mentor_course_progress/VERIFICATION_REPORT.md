# VERIFICATION_REPORT — Study API #65

## Kết quả

- DD status: Draft — Needs Confirmation; direct catalog contract is preserved and the AC-26 response mismatch is explicit.
- Deliverables: 8 template sheets plus PLAN_RESULT.md, OPEN_QUESTIONS.md, and this report; 11 Markdown files total.
- Runtime API #65: UNWIRED / NOT_FOUND. No route, module, or focused test source was found.
- AC-26 macro-review #65–#67: VERIFIED_WITH_OPEN_QUESTIONS after DD #67 was created; see the group review below and [API #67 report](../67_mentor_student_progress/VERIFICATION_REPORT.md).
- Runtime tests: not run; this was docs-only work.

## Kiểm tra

| Check | Kết quả | Trạng thái |
|---|---|---|
| Worklog preflight | Selector returned #48, #49, #50; all three docs worklogs were read. Plan was recorded before authoring. | VERIFIED |
| Catalog/diagram | Catalog row #65 and AC-26 sequence were checked; #65 roster progress remains separate from #66 analytics and #67 student detail. | VERIFIED_STATIC_ONLY |
| Source/schema | No #65 route/module/focused test found. Legacy BIGINT and V1-PILOT UUID/versioned evidence remain separate. | VERIFIED_STATIC_ONLY |
| Manifest/front matter | Exact 11-file set; all 8 sheets carry dd_id 65 and Draft status. | VERIFIED |
| Catalog/error set | Exact method/path/auth/path parameter/no body or query/response/200; exact errors 401/403/404/500. | VERIFIED_STATIC_ONLY |
| Response/data mapping | Course and PageMeta fields are listed; candidate learner-progress fields remain separately marked DERIVED. Read-only table mapping is N/A. | VERIFIED_STATIC_ONLY |
| Template appendix | All 8 output appendices match the registered template suffix byte-for-byte; source template hashes match PLAN_RESULT.md. | VERIFIED |
| JSON/Markdown | Both JSON examples parse; local links resolve; tables have consistent widths; fences balance; trailing whitespace absent. | VERIFIED |
| git diff --check | No diagnostics. Custom checks also covered the untracked DD files. | PASS |
| AC-26 macro-review | #65 summary, #66 events and #67 selected-Student detail are distinct; shared progress formula/denominator and remaining contract/auth/schema/error questions were reconciled at document level. | VERIFIED_WITH_OPEN_QUESTIONS |
| Runtime tests | Not run; docs-only and endpoint unwired. | NOT_RUN |
| Context validator | Not applicable; no context page or manifest changed. | NOT_APPLICABLE |

## Output fingerprints — 8 sheets

~~~text
00_Cover.md        f64880a188c5f73a87772cfe6bde0a3d1663d2f86201d58cb67b980d741e08da
01_Lich_su.md      d02b84a0625d66d771c6390d50722b3486723ea654c5f6dfc61389271bb5d3fc
02_Overview.md     34f8eed88b293da26732b48be9f0a8a2550ad8afcecd5eb639388708e5b77712
03_Request.md      14156c211996dc8eb339fbff1760815609e1fb03bb565e9b4ec71ed0a639cd03
04_Response.md     db33572734e05121c964217705ebca9c6523d006970028386735c2d1b51740c1
05_Data_Mapping.md 32458ca7c4a20ccbafebcce1a786e3b397b6020fa43350dbd15cff8a850f9c87
06_Error.md        79a77b6590ec2d4cd3cafe6e318edb443f4a94181efbf929658f2f108f92f135
07_table.md        0d6763de64b59425da8cf215a35afa8a677222dedf01556834032ccf116e3320
~~~

## Remaining blockers

- Response contract Page<Course> does not represent the AC-26 learner progress dashboard; any alternative schema remains a proposal.
- Pagination inputs, Mentor identity/assignment policy, live progress schema, enrollment filtering, status/formula and empty-class semantics need owner confirmation.
- Error guideline data:null differs from the current helper default {}; future route wiring must also register the path in the design-code middleware allowlist.

Review [OPEN_QUESTIONS.md](./OPEN_QUESTIONS.md), [PLAN_RESULT.md](./PLAN_RESULT.md), and the neighboring [API #62 report](../62_mentor_course_students/VERIFICATION_REPORT.md).

## Macro-review AC-26 #65–#67 — 2026-10-24

Status: `VERIFIED_WITH_OPEN_QUESTIONS` — review tài liệu/source tĩnh sau khi DD #67 tồn tại.

- **Luồng:** Mentor mở dashboard; #65 trả class-level enrollment/progress candidate; #66 riêng course-wide learning-event candidate; UI chọn Student rồi gọi #67. Diagram không mô tả server-to-server calls.
- **Payload trực tiếp:** Cả ba catalog row đều khai báo `ApiEnvelope<Page<Course>>`, không schema nào chứa progress hoặc analytics. Đây là discrepancy nhóm; catalog được giữ nguyên trong các DD. Các PageMeta cũng không có page/size request nên chưa có pagination semantics/bounds.
- **Candidate boundary:** #65 là roster summary; #66 là event aggregate. `students_with_learning_events` đếm Student có event hợp lệ, không đồng nghĩa tổng enrollment của #65. Không dùng `lesson_progress`, `last_accessed_at`, progress snapshots hoặc `last_event_id` để thay event source #66.
- **Progress consistency:** #65 và #67 candidate dùng cùng tập lesson PUBLISHED và cùng formula floor-average; #67 chỉ thêm current state theo lesson cho Student được chọn. Candidate #67 không thêm quiz/assignment vì AC-26 không nêu chúng; API #37/AC-18 là flow khác. Tập eligible enrollment, status, duplicate progress rows, formula, rounding và empty behavior vẫn phải được duyệt.
- **Authorization/data:** Ba API yêu cầu Mentor role và course scope; #67 còn phải xác minh Student thuộc cùng roster eligibility như #65. Mentor principal binding, owner/assignment, privacy-aware 403/404 order và schema live chưa có nguồn.
- **Shared error gap:** Cả ba có direct error set 401/403/404/500. Guideline `data:null` khác helper `{}`; cả ba path chưa nằm trong middleware design-code allowlist. Cần đồng bộ khi wiring.
- **Runtime:** #65–#67 đều không có route/module/focused test source hiện tại; review này không phải runtime verification.

Xem [API #67 report](../67_mentor_student_progress/VERIFICATION_REPORT.md) và open questions của từng DD.


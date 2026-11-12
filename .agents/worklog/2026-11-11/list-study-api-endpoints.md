---
task_id: "2026-11-11-list-study-api-endpoints"
date: "2026-11-11"
primary_task_type: "docs"
secondary_task_types: []
project_scopes: ["server-study", "web-work"]
cross_scope_dependencies: ["Study Server approved API catalog/DD -> Study Client endpoint reference"]
status: "VERIFIED"
---

# Worklog: Tạo danh mục endpoint Study API

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `node scripts/select-worklogs.mjs --type docs --limit 3`
- selector_result: `READY`; 272 worklog cùng loại; đã chọn và đọc đủ 3.
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-11-11/load-study-server-context.md`
    - carry_forward: Study OpenAPI là `NOT_FOUND`/README placeholder; context ghi `CONTEXT_STALE server-study` và coverage runtime 58 path templates/69 operations tới API #98; nhiều API catalog còn ngoài runtime. DD #98 có `DISCREPANCY` với source.
  - path: `.agents/worklog/2026-11-10/load-project-context.md`
    - carry_forward: Tách approved DD/expected behavior khỏi current source; project status historical có thể lệch scope status; giữ validator baseline invalid riêng biệt.
  - path: `.agents/worklog/2026-11-09/add-study-frontend-rules.md`
    - carry_forward: Study Web đang `SKELETON_ONLY`; generic transport không chứng minh endpoint/feature runtime; tài liệu Study Web viết tiếng Việt.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Điền `apps/study-client/docs/list_endpoint.md` bằng một bảng duy nhất gồm đủ 103 API ID liên tục, sáu cột theo yêu cầu; mỗi dòng tóm tắt mục tiêu, logic 2–3 bước, input và success output. Có ghi chú envelope/lỗi chung và tuyên bố tài liệu phản ánh thiết kế/DD, không xác nhận runtime.
- Canonical contract/approved DD: `docs/lists/list_api.md` được đánh dấu `APPROVED_DESIGN_CONTRACT`; đối chiếu Overview, Request, Response và Data Mapping tương ứng trong `apps/study-server/docs/dd/`.

## CURRENT_BEHAVIOR

- Source/config: Target đã được điền bằng một bảng 103 dòng. `docs/lists/list_api.md` khai báo `APPROVED_DESIGN_CONTRACT`; đã đối chiếu 103 ID duy nhất 1–103 với DD có đủ Cover/Overview/Request/Response/Data Mapping. DD Cover bỏ trống method hoặc route ở #44, #63, #76, #94–#103; Cover thiếu API name ở #76, #94–#103; Overview thiếu Purpose ở #49–#50. Bảng dùng method/path và success I/O theo catalog, link tới Overview từng API, ghi các gap/discrepancy liên quan. Nguồn runtime/context hiện không xác nhận toàn bộ catalog đã wired.
- Runnable tests: Không chạy application tests theo phạm vi tài liệu.
- Runtime wiring: Study Web là `SKELETON_ONLY`; Study OpenAPI `NOT_FOUND`; tài liệu đã ghi rõ đây không phải xác nhận runtime.

## SOURCE_TRACE

```text
approved Study API catalog -> per-API DD Overview/Request/Response/Data Mapping -> Study Client endpoint reference
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| DD Cover method/name | Cover của #44, #63, #76, #94–#103 thiếu method hoặc route; #76 và #94–#103 còn thiếu API name; catalog có tên/route dùng được. | `DISCREPANCY` | Dùng catalog khi Cover thiếu và nêu các ID ở ghi chú. |
| DD Overview Purpose | API #49 và #50 thiếu field Purpose. | `Chưa được đặc tả` | Không suy mục tiêu từ tên hay runtime; đánh dấu trong hai dòng. |
| Response/input contract gaps | DD nêu discrepancy hoặc SOURCE_REQUIRED ở #3, #8, #18, #20–#21, #26, #65–#67, #78, #82, #87, #91–#93, #96, #98, #103. | `DISCREPANCY / SOURCE_REQUIRED` | Giữ catalog contract; ghi gap/fallback mâu thuẫn trong các dòng tương ứng. |
| API #103 response | Catalog row trả `Report`, trong khi DD Response/Data Mapping liệt kê payload `Operation` như một phương án mâu thuẫn chưa chọn. | `DISCREPANCY` | Giữ catalog `Report` làm schema theo contract và ghi conflict cạnh output. |
| Runtime wiring vs catalog | Catalog ghi `APPROVED_DESIGN_CONTRACT`; scope/worklog hiện có ghi runtime chỉ có một phần operation đến API #98, Study Web skeleton-only, OpenAPI chưa có. | `DISCREPANCY / UNWIRED / NOT_FOUND` | Ghi rõ danh mục theo thiết kế/DD; không gắn nhãn endpoint hoạt động. |

## CHANGES

- Files changed: `apps/study-client/docs/list_endpoint.md`, worklog này.
- CONTEXT_UPDATES: Không đổi source, API contract, hay context page.
- Context pages changed: None.
- Assumptions: Tóm tắt gọn bằng tiếng Việt; method/path và API ID đặt trong cột tên; schema rút gọn nhưng không đổi ý nghĩa contract.

## VERIFICATION

| Command | Result | Status |
|---|---|---|
| `node scripts/select-worklogs.mjs --type docs --limit 3` và đọc 3 log đã chọn | `READY`, đủ 3 log docs; đã ghi carry-forward facts ở `PRIOR_WORKLOG_REVIEW`. | VERIFIED |
| `list_api.md` và 103 bộ DD (`00_Cover`, `02_Overview`, `03_Request`, `04_Response`, `05_Data_Mapping`) | Đối chiếu API ID/name/route/input/output/purpose/logic; Cover/Overview gaps và response discrepancies được ghi nhận. | VERIFIED_STATIC_ONLY |
| Markdown coverage/link/schema verifier | 103 dòng ID 1–103; sáu cột; method/path duy nhất; success status/code/schema và purpose khớp source; 103 link DD và link catalog tồn tại; logic tối đa ba bước; newline cuối file, không trailing whitespace. | VERIFIED |
| `git diff --check` và `git diff --no-index --check /dev/null apps/study-client/docs/list_endpoint.md` | Chưa có whitespace error; no-index return code `1` biểu thị file mới có nội dung, không phải check error. | VERIFIED |
| `node scripts/validate-agent-context.mjs` | Exit 1 `AGENT_CONTEXT_INVALID`, 83 findings baseline: 33 DB Admin, 33 `ORPHAN_SKILL_RESOURCE`, 10 broken DB Admin context links và 7 scope snapshot stale. Không finding nào nhắc target hoặc worklog mới. | BASELINE_INVALID_UNRELATED |
| Application tests/build | Không chạy theo kế hoạch tài liệu. | NOT_RUN |

## HANDOFF

- Remaining blockers: Repo-wide context validator còn baseline invalid không liên quan đến tài liệu/worklog này; application tests không thuộc phạm vi.
- Next owner/action: Không còn việc bắt buộc cho danh mục endpoint; xử lý baseline context ở task bảo trì context riêng.

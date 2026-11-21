---
task_id: "2026-10-24-create-study-api96-dd"
date: "2026-10-24"
primary_task_type: "docs"
secondary_task_types: []
project_scopes: ["server-study"]
cross_scope_dependencies: []
status: "VERIFIED"
---

# Worklog: Tạo DD Study API #96 — Admin notification delivery status

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `deno run --allow-read scripts/select-worklogs.mjs --type docs --limit 3` (Node không có trong PATH; Deno tương thích được workflow cho phép)
- selector_result: `available=117`, `selected=3`, `status=READY`
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-10-24/create-study-api48-dd.md`
    - carry_forward: Giữ direct contract và tách expected/current; không invent schema/enum/ownership; ghi runtime là `UNWIRED` nếu thiếu route.
  - path: `.agents/worklog/2026-10-24/create-study-api49-dd.md`
    - carry_forward: Dùng các ma trận request/query/mutation/response-source; Study DD chỉ xuất Markdown; giữ `SOURCE_REQUIRED` và discrepancy của response shape.
  - path: `.agents/worklog/2026-10-24/create-study-api50-dd.md`
    - carry_forward: Không dùng DDL pilot làm nguồn cho contract BIGINT; proposals phải gắn `DERIVED`; source scan là bằng chứng code, không phải runtime proof.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Tạo DD Markdown tiếng Việt cho API #96, lập plan trước khi tạo folder DD, giữ nguyên catalog contract, đọc AC-36 và DD #92–#95, static-verify ngay sau authoring, rồi macro-review nhóm AC-36 #92–#96.
- Canonical contract: `GET /api/v1/admin/notifications/{notification_id}/status`; Bearer JWT, role Admin; path `notification_id:int64!`; không body/query; `ApiEnvelope<Notification>`; HTTP 200 `DESIGN_RESOURCE_RETRIEVED`; đúng errors 401 `DESIGN_AUTHENTICATION_REQUIRED`, 403 `DESIGN_ACCESS_DENIED`, 404 `DESIGN_RESOURCE_NOT_FOUND`, 500 `DESIGN_INTERNAL_ERROR`.
- Reusable `Notification`: `id`, `title`, `content`, `channels`, `status`, optional `read_at`, optional `scheduled_at`, `created_at`. Reusable `NotificationDelivery`: `notification_id`, `status:OperationStatus`, `queued`, `sent`, `failed`; không tự thêm các trường này vào `Notification`.
- AC-36 flow: nhánh STATUS gọi #96, sau đó diagram có bước “Đọc delivery aggregate” rồi “Reload notification management”.

## CURRENT_BEHAVIOR

- Source/config: `app/api/v1.py` không khai báo API #96; AST đối chiếu 103 catalog method/path cho thấy 12 khớp router, 91 chưa có route. Không có Admin notification module/view/test. `DESIGN_CONTRACT_PATHS` không có path Admin notifications; đây chỉ là điều kiện cần lưu ý nếu route được nối sau này.
- Runnable tests: Không chạy; task chỉ tạo/tĩnh kiểm tra tài liệu. Không có test source cho #96.
- Runtime wiring: `UNWIRED / NOT_FOUND`; source inspection không chứng minh deployment/live behavior.
- Schema: legacy BIGINT `notifications` có `id`, `user_id`, `sender_id`, `title`, `content`, `type`, `is_read`, `created_at`, không có Admin delivery aggregate. V1-PILOT UUID `notifications`/`notification_deliveries` là mô hình learner/delivery riêng; không map vào ID Admin BIGINT.

## SOURCE_TRACE

```text
Admin Bearer + notification-management permission -> GET notification_id -> load Admin Notification -> diagram requests delivery aggregate -> map only existing Notification response fields -> 200 / exact catalog errors -> reload management
```

Không có current caller/callee/DB effect cho #96 vì route chưa tồn tại. Candidate source, grain, enum, aggregate query và Admin permission đều cần nguồn được duyệt.

## PLAN BEFORE DD AUTHORING

1. Giữ nguyên method/path, Admin Bearer, `notification_id:int64!`, không body/query, `ApiEnvelope<Notification>`, HTTP 200 và đúng bốn lỗi 401/403/404/500.
2. Đọc AC-36 flow và DD #92–#95; tách response catalog khỏi bước diagram “Đọc delivery aggregate”. Không đổi `Notification` thành `NotificationDelivery`, không thêm count/channel-result fields.
3. Ghi Q1 đọc Admin Notification theo ID là `SOURCE_REQUIRED` vì chưa có approved Admin physical relation. DDL legacy chỉ là candidate một notification row; V1-PILOT UUID learner delivery không tương thích.
4. Ghi Q2 aggregate status/counts là `SOURCE_REQUIRED`: catalog có reusable `NotificationDelivery` nhưng không chỉ định API response projection, relation/grain, status tokens hay phép tổng hợp. Chỉ có thể đề xuất `DERIVED` rằng projection (nếu owner duyệt) phải nằm trong `Notification.status` hiện hữu; không tự định nghĩa quy tắc.
5. Trong Response Source Matrix, liệt kê từng field của `Notification`; chỉ `id/title/content/created_at` có candidate legacy columns, còn `channels/status/read_at/scheduled_at` thiếu mapping Admin được duyệt. Không suy `is_read` thành `status`/`read_at`.
6. Ghi mutation `N/A — READ-ONLY API`; không tạo side effect hay provider call.
7. Tạo 8 sheet roles và 3 reports trong `96_admin_notifications_status`; `07_table.md` giữ `N/A — READ-ONLY API`. Liên kết catalog, AC index/diagram, schema/DDL và DD #92–#95.
8. Static verify contract, source-status, all response fields, JSON, template appendix/front matter, local links, tables, fences, whitespace, exact file set và source-scan result. Không chạy application tests.
9. Sau khi #96 hoàn thành, macro-review toàn nhóm #92–#96; thêm `AC-36_MACRO_REVIEW.md` vào #96. Cập nhật trạng thái macro-review trong OPEN_QUESTIONS và VERIFICATION_REPORT của #92–#95 cùng worklogs; giữ các quyết định owner chưa có nguồn ở trạng thái mở.

### Count inventory checked before #96 authoring

| Measure | Current count | Basis |
|---|---:|---|
| Catalog unique method/path | 103 | 103 API rows in `docs/lists/list_api.md` and AC/API index |
| Numbered DD folders present | 95 | Static directory inventory, IDs #01–#95 |
| DD IDs missing before this task | 8 | #96–#103 |
| Full 8-sheet + 3-report packages | 83 | Static required-file shape check; 12 earlier folders have 8 sheets but no 3 reports |
| Catalog routes matching current router | 12 | AST method/path intersection with `app/api/v1.py` |
| Catalog routes without source implementation | 91 | 103 minus 12; source presence does not prove runtime for every route |
| Runtime verification boundary | 10 of 12 source-wired API IDs were previously verified; #08/#09 remain unverified after merge | `.agents/server-study/AGENTS.md` and `apis/declared-routes.md` |

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| Delivery aggregate vs response | AC-36 has aggregate-read step; catalog returns `Notification` with no count/per-channel result fields | `DISCREPANCY / SOURCE_REQUIRED` | Preserve response and ask owner for projection/source/grain |
| Admin Notification persistence | Legacy notification row is partial; no approved campaign/recipient model | `SOURCE_REQUIRED` | No executable query or full response mapping |
| Pilot delivery schema | UUID learner notification/delivery model vs int64 Admin contract | `DISCREPANCY` | Keep models separate |
| Notification enums | Channel/status/OperationStatus member values and aggregate rules absent | `SOURCE_REQUIRED` | Do not infer values or mapping |
| Admin permission | AC requires notification-management permission; Study Admin guard/policy not verified | `SOURCE_REQUIRED / UNWIRED` | Do not claim authorization implementation |
| API #93 Operation response | Catalog/diagram Notification vs tracking paragraph Operation and UUID/int64 bridge | `DISCREPANCY` | Preserve as AC-36 group issue |

## CHANGES

- Files changed: `apps/study-server/docs/dd/96_admin_notifications_status/` (8 sheets, 3 standard reports, 1 AC-36 group report); connected OPEN_QUESTIONS/VERIFICATION_REPORT updates for #92–#95; worklogs #92–#95; this worklog; `.agents/worklog/2026-10-24/refresh-study-api-dd-counts.md`.
- CONTEXT_UPDATES: None; no runtime, schema, catalog, diagram or context page change.
- Scope boundary: Study Server DD Markdown, AC-36 cross-review and count worklog only; unrelated dirty worktree changes were preserved.

## VERIFICATION

| Command/check | Result | Status |
|---|---|---|
| Worklog selector | Deno compatibility selector returned the three `docs` worklogs #48–#50; all were read. | `VERIFIED` |
| Catalog inventory | 103 unique method/path rows; #96 direct request/response/error set read. | `VERIFIED_STATIC_ONLY` |
| Router/module inventory | 12 of 103 catalog IDs have matching router declaration and module `view.py` (#01–#09, #12–#14); 91 lack the pair. | `VERIFIED_STATIC_ONLY` |
| DD inventory after #96 | 96 folders #01–#96; 7 missing (#97–#103); 84 full 8-sheet + 3-report shapes; 12 legacy folders remain core-only. | `VERIFIED_STATIC_ONLY` |
| DD #96 static checks | 12-file manifest; exact catalog/error set; all Notification fields; 8/8 template appendices; 2 JSON examples; 31 table blocks; 20 local links; no whitespace/fence/newline issues. | `PASS — STATIC` |
| AC-36 macro-review | #92–#96 reviewed; group report and connected DD/worklogs updated. | `VERIFIED_WITH_OPEN_QUESTIONS` |
| Runtime tests | Not run; docs task. | `NOT_RUN` |
| Runtime/deployment/live DB | Not checked. | `NOT_CHECKED` |

## HANDOFF

- Remaining blockers: Admin notification model/grain, delivery aggregate source/projection, enums/status rules, Admin permission and #93 Operation bridge remain owner decisions; see `AC-36_MACRO_REVIEW.md`.
- Next action: Continue at API #97. Current counts after #96 are 96 DD folders / 7 missing and 12 source-programmed APIs / 91 without a router-plus-view pair.

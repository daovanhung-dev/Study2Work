---
task_id: "2026-10-24-create-study-api92-dd"
date: "2026-10-24"
primary_task_type: "docs"
secondary_task_types: []
project_scopes: ["server-study"]
cross_scope_dependencies: []
status: "VERIFIED"
---

# Worklog: Tạo DD Study API #92 — Danh sách notification Admin

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `deno run --allow-read --allow-env scripts/select-worklogs.mjs --type docs --limit 3`
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-10-24/create-study-api48-dd.md`
    - carry_forward: Giữ catalog direct contract; tách `DERIVED` khỏi dữ kiện và không biến DD thành runtime.
  - path: `.agents/worklog/2026-10-24/create-study-api49-dd.md`
    - carry_forward: Giữ nguyên response cardinality trong catalog, nêu discrepancy khi purpose/diagram gợi ý collection hoặc tree.
  - path: `.agents/worklog/2026-10-24/create-study-api50-dd.md`
    - carry_forward: Chỉ dùng DB candidate khi có field evidence; đánh dấu `SOURCE_REQUIRED` cho persistence, access và semantics chưa có nguồn.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Tạo DD API #92 bằng tiếng Việt, lập plan trước khi tạo folder DD, rà AC-36 diagram, tham khảo các API notification đã có, kiểm tra tài liệu ngay sau khi tạo. AC-36 macro-review #92–#96 vẫn pending cho tới khi đủ nhóm.
- Catalog #92: `GET /api/v1/admin/notifications`; Bearer JWT, role Admin; query `status?:string`, `channel?:string`, `page?:int32`; success HTTP 200 `DESIGN_RESOURCE_RETRIEVED`; response trực tiếp `ApiEnvelope<Notification>`; errors chính xác: 401 `DESIGN_AUTHENTICATION_REQUIRED`, 403 `DESIGN_ACCESS_DENIED`, 503 `DESIGN_DEPENDENCY_UNAVAILABLE`, 500 `DESIGN_INTERNAL_ERROR`.
- Reusable `Notification`: `id:int64`, `title:string`, `content:string`, `channels:NotificationChannel[]`, `status:NotificationStatus`, optional `read_at:date-time`, optional `scheduled_at:date-time`, `created_at:date-time`.
- AC-36 requires Admin notification-management permission. Diagram flow: #92 query notifications, then branch to create/send #93, update #94, delete/cancel #95 or delivery status #96. It does not specify list cardinality, pagination response, filter enums or sort order.

## CURRENT_BEHAVIOR

- Source/config: Không tìm thấy API #92 route/module/test trong `apps/study-server/app` hoặc `apps/study-server/tests`. `DESIGN_CONTRACT_PATHS` không chứa `/api/v1/admin/notifications`; đây chỉ là discrepancy tích hợp có điều kiện khi route được wire.
- DB evidence: Legacy BIGINT `notifications` có `user_id`, `sender_id`, `title`, `content`, `type`, `is_read`, `created_at`; không có `channels`, `status`, `read_at`, `scheduled_at` hoặc campaign/recipient aggregate. V1-PILOT dùng UUID learner notification và `notification_deliveries` riêng; `channel/status` thuộc từng delivery, không phải `Notification.status`; không gộp hai schema và không coi là live.
- Related DDs: #43 dùng `Page<Notification>` cho Student và giữ các gap `type`/`is_read`; #63/#64 mô tả Mentor create/delivery khác Admin list. API #93 catalog response `Notification` nhưng Operation tracking summary còn gợi ý `Operation`; ghi nhận là câu hỏi nhóm, không sửa trong #92.
- Runtime wiring: `UNWIRED / NOT_FOUND`; Study shared auth hiện không có Admin guard/policy. Application tests không chạy trong task docs-only.

## SOURCE_TRACE

```text
Admin Bearer principal -> notification-management permission (AC-36) -> GET #92 và optional status/channel/page -> logical notification-list query (physical model chưa khớp đầy đủ) -> Notification contract trực tiếp hoặc Page proposal riêng -> 200/catalog errors -> Admin chọn nhánh #93–#96
```

## PLAN BEFORE DD AUTHORING

1. **Input/template/source gate:** dùng registered `createDD-markdown`; Study workflow chỉ tạo Markdown folder, không tạo ZIP. Template registry có đúng tám file. Đọc API catalog #92–#96, AC-36 index và toàn page AC36 trong `AC_04_ADMIN_MANAGEMENT.drawio`; đọc DB table guide, ERD, cả legacy Study DDL lẫn V1-PILOT notification DDL; đối chiếu DD #43, #63, #64 và current router/middleware/helper.
2. **Requirement matrix (DIRECT):** giữ GET/path, Admin Bearer, query names/types, response `ApiEnvelope<Notification>`, HTTP 200 và đúng bốn lỗi 401/403/503/500. Không thêm query/body/status/error vào contract.
3. **Request usage matrix:** Authorization xác thực Admin và notification-management permission (role/status DIRECT, concrete claim/policy SOURCE_REQUIRED); `status`/`channel` là string tùy chọn, enum/normalization chưa có; `page` int32 tùy chọn nhưng page origin/size chưa có; không có body/path.
4. **Query matrix:** giữ Q1 vật lý là `SOURCE_REQUIRED` cho complete Admin notification projection. Ghi legacy `notifications` chỉ là field candidate (`id/title/content/created_at`); không map `type→channels`, `is_read→status/read_at`, không suy `scheduled_at`. Tách V1-PILOT `notification_deliveries` (UUID, channel/status cấp delivery) và không dùng làm query runtime. Đề xuất DERIVED riêng nếu response được sửa thành `Page<Notification>`: page bắt đầu 1, fixed size 20 theo precedent #43, thứ tự `created_at DESC, id DESC`; không trình bày proposal như contract.
5. **Mutation matrix:** N/A — API #92 GET read-only, không INSERT/UPDATE/DELETE.
6. **Response source matrix:** liệt kê đủ envelope và mọi field `Notification`; xác định field candidate hoặc `SOURCE_REQUIRED` từng dòng. Giữ direct singleton-vs-list discrepancy; Page proposal không thay contract. Nêu empty result, total/page metadata, grouping campaign/recipient và filter behavior là unresolved.
7. **Error/access:** giữ 401/403/503/500 literals; permission source và error triggers chưa có. AC-36 list diagram chỉ cho thấy query DB, không chỉ ra dependency nào làm phát sinh 503; giữ code nhưng trigger SOURCE_REQUIRED. Ghi error-helper `{}` so với guideline `null` là conditional future discrepancy.
8. **Tạo package:** tạo `apps/study-server/docs/dd/92_admin_notifications_list/` gồm 8 sheet chuẩn + `PLAN_RESULT.md`, `OPEN_QUESTIONS.md`, `VERIFICATION_REPORT.md`; `07_table.md` = `N/A — READ-ONLY API`. Mọi direct/derived/source-required behavior tách rõ. Không tạo ZIP hoặc sửa runtime/schema/catalog/diagram.
9. **Kiểm tra ngay:** exact 11-file package, appendix byte parity, direct contract/error set, all Notification fields, valid JSON, local links/anchors, table widths, fences, final newline, whitespace và `git diff --check`. Cập nhật report/worklog và count inventory; app tests `NOT_RUN`.

### API requirement matrix

| Item | Contract | Evidence/status |
|---|---|---|
| Method/path | `GET /api/v1/admin/notifications` | Catalog #92 + AC-36; DIRECT |
| Actor/auth | Bearer JWT; role Admin | Catalog + diagram; DIRECT; concrete guard `SOURCE_REQUIRED` |
| Permission | notification management permission | AC-36; DIRECT requirement, policy/claim `SOURCE_REQUIRED` |
| Query | `status?:string`, `channel?:string`, `page?:int32` | Catalog; DIRECT |
| Body/path | None | Catalog; DIRECT |
| Response | `ApiEnvelope<Notification>` | Catalog + diagram; DIRECT; conflicts with list purpose |
| Success | 200 `DESIGN_RESOURCE_RETRIEVED` | Catalog + diagram; DIRECT |
| Errors | 401 `DESIGN_AUTHENTICATION_REQUIRED`; 403 `DESIGN_ACCESS_DENIED`; 503 `DESIGN_DEPENDENCY_UNAVAILABLE`; 500 `DESIGN_INTERNAL_ERROR` | Catalog + diagram; DIRECT; 503 trigger SOURCE_REQUIRED |

### Request usage matrix

| Input | Direct use | Open rule |
|---|---|---|
| Authorization | Bearer JWT; Admin role | Permission claim/policy and principal mapping `SOURCE_REQUIRED` |
| `status` | Optional string filter | Enum values, exact/case/normalization and physical mapping `SOURCE_REQUIRED` |
| `channel` | Optional string filter | `NotificationChannel` values and delivery-vs-notification semantics `SOURCE_REQUIRED` |
| `page` | Optional int32 | Page origin and size absent; do not invent in direct contract |
| Body/path | None | DIRECT |

### Query matrix

| Query | Candidate source | Candidate fields | Predicate/ordering | Status |
|---|---|---|---|---|
| Q1 | No approved complete Admin list source | Legacy BIGINT `notifications` exposes only partial fields; V1-PILOT uses incompatible UUID model | Do not specify executable SQL, filter mapping or joins | `SOURCE_REQUIRED` |
| Q1-L | Legacy `notifications` | `id,title,content,created_at` only | Per-recipient row granularity; cannot establish campaign aggregate/status/channels | Candidate only; not implementation-ready |
| Q1-P | Proposed `Page<Notification>` after contract approval | page=1, fixed size=20, `created_at DESC,id DESC` | Filter by exact status/channel only after approved field mappings | `DERIVED`; #43 precedent, not direct contract |

### Mutation matrix

| Operation | Result |
|---|---|
| INSERT/UPDATE/DELETE | N/A — read-only API |

### Response source matrix

| Response field | Candidate source | Mapping/status |
|---|---|---|
| `success`, `businessCode`, `message`, `meta`, `traceId` | Envelope convention/catalog | Preserve envelope; exact message/meta empty/null and trace propagation follow API guideline/current helper discrepancy |
| `data.id` | Legacy `notifications.id` is BIGSERIAL; pilot ID is UUID | Legacy is only an int64 candidate; live mapping unknown |
| `data.title` | Legacy `notifications.title`; pilot `notifications.title` | Candidate field in different models |
| `data.content` | Legacy `notifications.content`; pilot field is `body` | Legacy candidate; do not equate pilot body without decision |
| `data.channels[]` | Pilot `notification_deliveries.channel` only | No approved mapping; do not use legacy `type`; `SOURCE_REQUIRED` |
| `data.status` | Pilot delivery status belongs to per-channel delivery | No approved Notification-level status; `SOURCE_REQUIRED` |
| `data.read_at` | Pilot learner-owned notification only | Not a legacy field and not necessarily Admin campaign state; `SOURCE_REQUIRED` |
| `data.scheduled_at` | None in reviewed schemas | `SOURCE_REQUIRED` |
| `data.created_at` | Legacy/pilot notification `created_at` | Candidate with timezone/granularity unresolved |

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| List vs response | AC-36/API name/query imply list; catalog says `ApiEnvelope<Notification>` | `DISCREPANCY` | Keep direct contract; Page is separate DERIVED proposal |
| Notification projection | Legacy and pilot schemas each omit/alter required fields | `DISCREPANCY / SOURCE_REQUIRED` | No complete executable query/mapping |
| Recipient/campaign grain | Legacy rows are recipient-scoped; AC-36 #93 creates Notification + recipients | `SOURCE_REQUIRED` | Need decision whether #92 lists a campaign or recipient notification |
| Filter semantics | No enum definitions; delivery channel/status differ from notification resource | `SOURCE_REQUIRED` | Do not invent filter values/joins |
| Admin authorization | AC-36 permission required; no Admin guard in current Study source | `UNWIRED / SOURCE_REQUIRED` | Runtime policy not established |
| 503 trigger | Catalog includes 503; list diagram shows query only | `SOURCE_REQUIRED` | Preserve code, do not invent dependency trigger |
| #93 operation tracking | #93 row says Notification while tracking summary mentions Operation | `DISCREPANCY` | AC-36 macro question; #92 does not reconcile it |

## CHANGES

- Files changed before authoring: this plan worklog only.
- DD folder status: absent at plan time; no sheet created yet.
- CONTEXT_UPDATES: None planned; task changes documentation/worklog only.
- Runtime/schema/catalog/diagram/tests: out of scope.

## VERIFICATION

| Check | Result | Status |
|---|---|---|
| Preflight | Selected/read #48, #49, #50; no shortage | VERIFIED |
| Context registry | `createDD-markdown` and docs-dd wired to `server-study`; Study Markdown-only override read | VERIFIED_STATIC_ONLY |
| AC-36 diagram/index and AC-36 flow | Full relevant page parsed; #92 query precedes branches #93–#96; list semantics/output details absent | VERIFIED_STATIC_ONLY |
| Catalog/Notification schema | #92–#96 and reusable Notification reviewed | VERIFIED_STATIC_ONLY |
| Current route/source | No #92 marker/path/module/test; middleware allowlist does not include endpoint | VERIFIED_STATIC_ONLY |
| DB/related DDs | Legacy and pilot notification models kept separate; #43/#63/#64 reviewed | VERIFIED_STATIC_ONLY |
| DD authoring/static checks | Package, template parity, catalog, JSON, links/anchors, tables, fences, whitespace/newline and source scan rechecked in current worktree; report updated with measured results. | VERIFIED |

## HANDOFF

- Remaining blockers: Owner/source confirmation for list cardinality, campaign-vs-recipient grain, page/filter semantics, notification fields, Admin policy, 503 trigger, and #93 operation response. These remain explicitly open in DD.
- Next owner/action: After API #92 static verification, continue one API DD session at #93; keep AC-36 macro-review pending until #96 is complete.

## CURRENT SESSION — PLAN BEFORE FINAL VERIFICATION

- Trigger: The current package exists, but `VERIFICATION_REPORT.md` still labels its checks `PENDING`; the DD is not complete until those results are rerun and recorded.
- Classification: `primary_task_type: docs`; `project_scopes: [server-study]`; no cross-scope dependencies.
- Preflight: selector returned #48, #49, #50; all three selected worklogs were read. Root/global context, server-study entry/index/workflow/declared routes, manifest wiring, `createDD-markdown`, and the Markdown template were loaded.
- Plan: validate the current 11-file package against the eight registered template suffixes; check exact catalog contract/error set, all `Notification` fields, JSON, links/anchors, tables, fences, final newlines, whitespace, and read-only mapping. Re-scan source for #92 absence. Update only the #92 verification report and this worklog. Do not run app tests or author API #93 in this #92 session.

## CURRENT SESSION — VERIFIED FINALIZATION

- Files changed in this finalization: `apps/study-server/docs/dd/92_admin_notifications_list/VERIFICATION_REPORT.md` and this worklog. No sheet content, runtime, test, schema, catalog, diagram or scope context was changed.
- Static package check: exact 11-file set; 8/8 template appendix suffixes byte-identical; 8/8 front matter records contain `dd_id: 92`; output manifest hash recorded in the verification report.
- Contract/content check: catalog row #92 exact method/path/auth/query/response/HTTP/errors; all `Notification` response fields present; no undeclared 404/422 introduced.
- Markdown check: 4/4 JSON examples parse; 34 tables and 436 table lines are consistent; six fence pairs balance; 20 file/directory links and 5 anchors resolve; all files have final newlines and no trailing whitespace.
- Source/runtime boundary: source scan found no route/module/test for API #92; design middleware allowlist lacks the path. Application tests were not run; live schema/runtime not verified. AC-36 group review remains pending until #96.
- Handoff: API #92 DD is now statically verified as `Draft — Needs Confirmation`; next API DD session is #93.

## GROUP_MACRO_REVIEW

- Status: `VERIFIED_WITH_OPEN_QUESTIONS` after API #96 DD was created; document-level cross-review covers #92–#96.
- Report: `apps/study-server/docs/dd/96_admin_notifications_status/AC-36_MACRO_REVIEW.md`.
- Findings: list response/cardinality remains unresolved; #93 Notification-vs-Operation, conditional Send and ID bridge remain unresolved; #94 body/schedule are DERIVED; #95 delete/cancel and delivery-start policy are SOURCE_REQUIRED; #96 aggregate intent is not represented in its direct Notification response. Shared Admin model, grain, enums and permission remain open.
- Application tests, runtime and live schema were not checked as part of this document review.

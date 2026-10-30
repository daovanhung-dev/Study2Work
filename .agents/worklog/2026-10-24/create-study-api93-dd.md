---
task_id: "2026-10-24-create-study-api93-dd"
date: "2026-10-24"
primary_task_type: "docs"
secondary_task_types: []
project_scopes: ["server-study"]
cross_scope_dependencies: []
status: "VERIFIED"
---

# Worklog: Tạo DD Study API #93 — Admin tạo/phát notification

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `deno run --allow-read --allow-env scripts/select-worklogs.mjs --type docs --limit 3`
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-10-24/create-study-api48-dd.md`
    - carry_forward: Giữ catalog contract trực tiếp, nêu `DIRECT` và `DERIVED` riêng; không tự hoàn tất semantics còn thiếu.
  - path: `.agents/worklog/2026-10-24/create-study-api49-dd.md`
    - carry_forward: Giữ response cardinality đúng catalog; nêu discrepancy với mục đích/diagram thay vì tự sửa.
  - path: `.agents/worklog/2026-10-24/create-study-api50-dd.md`
    - carry_forward: Không dùng schema candidate làm runtime source; đánh dấu mapping không có nguồn là `SOURCE_REQUIRED`.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Yêu cầu: Tạo một DD tiếng Việt cho API #93, trước tiên lập plan trong worklog, rà AC-36 và các DD/API notification liên quan, author đúng template đã đăng ký, kiểm tra ngay sau khi tạo. Tiếp tục giữ macro-review AC-36 pending cho tới khi nhóm #92–#96 đủ DD.
- Catalog #93: `POST /api/v1/admin/notifications`; Bearer JWT, role Admin; body `recipients?:int64[]`, `segment?:AudienceSegment`, `title:string!`, `content:string!`, `channels:NotificationChannel[]!`; success HTTP 202 `DESIGN_OPERATION_ACCEPTED`; response `ApiEnvelope<Notification>`; errors chính xác: 401 `DESIGN_AUTHENTICATION_REQUIRED`, 403 `DESIGN_ACCESS_DENIED`, 422 `DESIGN_VALIDATION_ERROR`, 503 `DESIGN_DEPENDENCY_UNAVAILABLE`, 500 `DESIGN_INTERNAL_ERROR`.
- AC-36 yêu cầu Admin có notification-management permission. Diagram nhánh `CREATE/SEND`: API #93 → `INSERT Notification + recipients` → Push/Email dispatch nếu action là Send → reload management.
- Catalog reusable `Notification`: `id:int64`, `title:string`, `content:string`, `channels:NotificationChannel[]`, `status:NotificationStatus`, optional `read_at:date-time`, optional `scheduled_at:date-time`, `created_at:date-time`.

## CURRENT_BEHAVIOR

- Source: Không thấy route/module/test API #93 hoặc `/api/v1/admin/notifications` trong `apps/study-server/app` hay `apps/study-server/tests`; route chưa có trong current Study router. Trạng thái `UNWIRED / NOT_FOUND`, chỉ theo static scan.
- Authorization: Current Study source chưa có Admin notification-management guard/policy được xác minh. AC-36 là requirement, không phải bằng chứng runtime.
- Persistence: Legacy `notifications` BIGINT có `user_id`, `sender_id`, `title`, `content`, `type`, `is_read`, `created_at`; không có campaign/segment relation, `channels`, notification-level `status`, `scheduled_at` hay recipient association table. V1-PILOT dùng UUID learner notification và delivery relation khác model; không gộp vào Admin campaign.
- Contract conflict: API #93 row và AC-36 node trả `ApiEnvelope<Notification>` tại HTTP 202; phần Operation tracking của `list_api.md` nói POST Admin notification trả `data: Operation`. Generic API #18 cũng có ID mismatch: schema/diagram UUID, row khai báo `operation_id:int64`.
- Delivery semantics: Request không khai báo `action` hoặc schedule; diagram mô tả dispatch có điều kiện `Nếu action là Send`. Enum values cho `AudienceSegment`, `NotificationChannel`, `NotificationStatus` chưa có trong các nguồn đã rà.

## SOURCE_TRACE

```text
API #93 catalog row + reusable schemas
  -> AC-36 Admin permission + CREATE/SEND flow
  -> #92 Admin list and #63/#64 Mentor notification precedents
  -> legacy Study DB candidate vs separate V1-PILOT schema
  -> API #18 operation tracking conflict
  -> current Study router/tests/helper (no #93 wiring)
```

## PLAN BEFORE DD AUTHORING

1. **Input/template/source gate:** registry xác nhận `createDD-markdown` là `SOURCE_BACKED`, wired tới `server-study`/`docs-dd`; đọc skill `.agents/skills/create_dd_api/docs/dd/createDD_MARKDOWN_SKILL.md`, bộ tám template `.agents/skills/create_dd_api/docs/dd/DD_API_Template_MD/`, Study workflow và DD #92. Template manifest fingerprint lấy từ report #92: `541b6ea0c36c5781c1b62574e1aba4e2fab5fde2f949a54129a123c63b78b9c2`. Study workflow yêu cầu output Markdown folder, không ZIP.
2. **Requirement matrix — DIRECT:** giữ chính xác method/path, Bearer/Admin, năm field body và type/requiredness, `ApiEnvelope<Notification>`, HTTP 202/code và đúng năm lỗi trong catalog. Không thêm body/header/error vào direct contract.
3. **Request usage matrix:** `Authorization` cho authentication/Admin; `recipients[]` và `segment` chọn audience nhưng quy tắc mutually exclusive, segment values và ID constraints là `DERIVED`/`SOURCE_REQUIRED`; `title` và `content` là required, không đặt length limit; `channels[]` required nhưng token set và min item chưa có. Ví dụ JSON dùng giá trị minh họa có ghi rõ, không biến thành enum contract.
4. **Logical behavior proposal:** do endpoint mang tên “Tạo/phát”, diagram nhánh là `CREATE/SEND`, và request không có `action`, ghi rõ một proposal `DERIVED`: POST tạo notification và tiếp nhận yêu cầu phát ngay; lưu Notification cùng recipient associations một cách nhất quán rồi enqueue dispatch, trả 202 sau khi dependency chấp nhận; provider delivery xảy ra bất đồng bộ. Không ghi proposal như contract đã duyệt. Giữ câu hỏi mở về draft/scheduled creation, action semantics và điểm chấp nhận.
5. **Query matrix:** không có query đã được xác nhận; API #93 là create. Ghi `N/A` cho read queries runtime. Recipient/segment expansion chỉ là logical need; nguồn audience predicate và schema là `SOURCE_REQUIRED`.
6. **Mutation matrix:** hai logical writes theo diagram: M1 Notification; M2 recipient associations. Không tuyên bố physical table/column/transaction đã duyệt. Tạo `07_table.md` cho candidate `notifications` insert và một file mapping bổ sung `08_notification_recipients_insert.md`; legacy table chỉ là candidate, không có recipient table phù hợp. Mark physical target, ID strategy, atomicity, audit và rollback `SOURCE_REQUIRED`.
7. **Response source matrix:** liệt kê đầy đủ envelope và mọi `Notification` field. Mapping physical source chưa có projection hoàn chỉnh; không map `type→channels`, `is_read→status/read_at`, cũng không dùng V1-PILOT learner/delivery IDs làm Admin IDs. Giữ response shape conflict Notification vs Operation; không tự nối notification_id:int64 với operation_id:uuid.
8. **Error/access:** giữ exact direct codes/status; gán trigger direct chỉ khi có căn cứ. Mark 401/403 framework/policy mapping, 422 field-level trigger, 503 queue/provider acceptance boundary và 500 rollback/source semantics là `DERIVED` hoặc `SOURCE_REQUIRED` tùy bằng chứng.
9. **Create package:** `apps/study-server/docs/dd/93_admin_notifications_create/` với tám sheet chuẩn (`00`–`06`, `07_table.md`), supplementary recipient mapping `08_notification_recipients_insert.md`, và `PLAN_RESULT.md`, `OPEN_QUESTIONS.md`, `VERIFICATION_REPORT.md`. Status `Draft — Needs Confirmation`; không sửa catalog, schema, diagram hay runtime.
10. **Cross-API review:** liên kết #92, #18, #94–#96; ghi response/ID/action discrepancies và để AC-36 macro-review pending cho tới #96.
11. **Immediate static verification:** exact files, template appendix parity và front matter, direct request/response/error coverage, JSON parse, Markdown table widths, fence pairs, local links/anchors, final newline, trailing whitespace và `git diff --check`. Không chạy app tests cho task docs-only. Sau verify, cập nhật inventory worklog và mục kết quả ở worklog này.

### API requirement matrix

| ID | Method/path | Actor/auth | Request | Response/success | Business flow | Tables/side effects | Status |
|---|---|---|---|---|---|---|---|
| #93 | `POST /api/v1/admin/notifications` | Bearer JWT; role Admin; AC-36 notification-management permission | Body: recipients?:int64[], segment?:AudienceSegment, title:string!, content:string!, channels:NotificationChannel[]! | `ApiEnvelope<Notification>`; 202 `DESIGN_OPERATION_ACCEPTED` | Diagram inserts Notification + recipients; Push/Email nếu Send | Logical Notification + recipient associations; async dispatch proposal | Direct contract; persistence/dispatch details need confirmation |

### Request usage matrix

| Input | Source/use | Validation or branch | Query/mutation use | Gap/status |
|---|---|---|---|---|
| `Authorization` | Bearer JWT; principal actor | Missing/invalid maps to catalog 401 | Principal for Admin permission and ownership fields | Claim mapping/policy `SOURCE_REQUIRED` |
| `recipients[]` | Optional explicit audience IDs | Element constraints, non-empty, duplicate policy unspecified | Recipient association write | Exactly-one audience mode/non-empty proposal `DERIVED`; target/source `SOURCE_REQUIRED` |
| `segment` | Optional audience segment | Enum values and expansion rule unknown | Audience selection | `AudienceSegment` definition/predicate `SOURCE_REQUIRED` |
| `title` | Required notification title | Required presence direct; blank/length behavior unspecified | Notification logical insert | No length limit invented |
| `content` | Required notification content | Required presence direct; blank/length behavior unspecified | Notification logical insert | No length limit invented |
| `channels[]` | Required delivery channels | Values, empty array and duplicates unspecified | Delivery request/dispatch | Enum/provider mapping `SOURCE_REQUIRED` |
| `action` / `scheduled_at` | Not declared in request | Diagram mentions conditional Send; no payload field | Draft/scheduled vs immediate dispatch | Do not add to direct request; open decision |

### Query matrix

| Query ID | Purpose | Physical source/columns | Predicate/order/pagination | Status |
|---|---|---|---|---|
| Q1 | Expand/validate recipients or segment | No approved Admin audience relation or selector source | No SQL/predicate can be specified from current sources | `SOURCE_REQUIRED` |
| Q2 | Operation/delivery status persistence | No Study Operation store/queue producer found | No query defined for #93 response | `SOURCE_REQUIRED`; API #18 contract conflict |

### Mutation matrix

| ID | Logical operation | Candidate target | Fields | Transaction/failure | Mapping file/status |
|---|---|---|---|---|---|
| M1 | Insert Notification | Legacy `notifications` only a partial candidate | `title`, `content`, sender/audience-related fields; no direct physical mapping for channels/status/scheduled | Diagram requires create; atomicity and ID strategy unconfirmed | `07_table.md`; physical target `SOURCE_REQUIRED` |
| M2 | Insert recipient associations | No matching table; legacy `user_id` represents a single nullable recipient per row | Recipient IDs from request or expansion of segment | Logical association needed; duplicate/partial-write behavior unresolved | `08_notification_recipients_insert.md`; physical target `SOURCE_REQUIRED` |
| M3 | Enqueue send operation | External queue/provider or Operation persistence not found | Notification/audience/channel context | Proposal only; 202 acceptance boundary requires confirmation | Described in data mapping; no invented table |

### Response source matrix

| Response field | Direct type/source | Transform/null rule | Gap/status |
|---|---|---|---|
| `success` | Envelope convention | Success true on 202 | Envelope convention |
| `businessCode` | Catalog | `DESIGN_OPERATION_ACCEPTED` | `DIRECT` |
| `message` | Envelope/application | Message text unspecified | `SOURCE_REQUIRED` |
| `meta` | Envelope convention | Shape/empty value follows guideline | `SOURCE_REQUIRED` |
| `traceId` | API guideline/current trace convention | Propagated trace value | Conventional; helper wiring not present for #93 |
| `data.id` | Notification logical ID int64 | No approved Admin ID allocator/table | `SOURCE_REQUIRED` |
| `data.title` | Request `title` | Direct copy; persistence projection unknown | Logical source direct; physical source `SOURCE_REQUIRED` |
| `data.content` | Request `content` | Direct copy; persistence projection unknown | Logical source direct; physical source `SOURCE_REQUIRED` |
| `data.channels[]` | Request `channels` | No enum or approved storage mapping | `SOURCE_REQUIRED` |
| `data.status` | NotificationStatus | Initial status not defined | `SOURCE_REQUIRED` |
| `data.read_at` | Optional date-time | Usually absent for newly created campaign, but contract does not define | `DERIVED` proposal; confirm |
| `data.scheduled_at` | Optional date-time | Request has no scheduled_at; response population unknown | `SOURCE_REQUIRED` |
| `data.created_at` | Persistence clock | Timezone/precision unknown | `SOURCE_REQUIRED` |
| Operation ID | Operation schema UUID vs API18 row int64 | Not in direct Notification shape | `DISCREPANCY`; no bridge inferred |

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status/impact |
|---|---|---|
| Notification vs Operation response | API #93 row and AC-36 node say Notification; operation tracking summary says Operation | `DISCREPANCY`; preserve catalog row and expose unresolved contract |
| Action absent | Diagram says dispatch only if action=Send; request has no action/schedule field | `DISCREPANCY`; immediate-send behavior only a DERIVED proposal |
| Audience selector | Both `recipients` and `segment` are optional; no XOR/empty/duplicate rule or enum list | `SOURCE_REQUIRED`; any exactly-one rule stays DERIVED |
| Notification model | Legacy BIGINT row and V1-PILOT learner UUID schema do not satisfy Admin campaign contract | `DISCREPANCY`; no schema conflation |
| Recipient mapping | Diagram needs recipients; no compatible association table | `SOURCE_REQUIRED`; cannot implement physical insert from current schema |
| Async status IDs | #93 response Notification ID:int64, #18 operation ID schema/diagram UUID vs row int64, #96 takes notification_id:int64 | `DISCREPANCY`; client ID bridge unresolved |
| Admin authorization | AC-36 requires permission; no Study Admin guard verified | `UNWIRED / SOURCE_REQUIRED` |

## PLANNED_OUTPUT

- API folder: `apps/study-server/docs/dd/93_admin_notifications_create/`.
- Required core sheets: `00_Cover.md`, `01_Lich_su.md`, `02_Overview.md`, `03_Request.md`, `04_Response.md`, `05_Data_Mapping.md`, `06_Error.md`, `07_table.md`.
- Additional logical write mapping: `08_notification_recipients_insert.md`.
- Reports: `PLAN_RESULT.md`, `OPEN_QUESTIONS.md`, `VERIFICATION_REPORT.md`.
- Expected final count after completion: 93 DD folders; 10 IDs #94–#103 still without DD; 12 source route+view pairs remain the static programmed count.
- No app tests or source code changes.

## VERIFICATION_RESULT

- Package: 12 Markdown files; eight standard sheets, one additional recipient mapping, and three reports.
- Template: fingerprint 541b6ea0c36c5781c1b62574e1aba4e2fab5fde2f949a54129a123c63b78b9c2; all 9 sheet appendices and front matter match their template source.
- Static checks: 2/2 JSON examples parse; 30 tables / 453 table lines have consistent widths; 3 code-fence pairs balanced; 49/49 relative links and anchors resolve; all files have final newline and no trailing whitespace.
- Contract coverage: method/path, every request field, full Notification response shape, HTTP 202 and exact five error codes match the catalog; discrepancies remain explicit.
- Inventory after task: 93 DD folders, 10 missing (#94–#103), 81 complete standard report packages; 12/103 route-plus-view source pairs and 91 without.
- Source scan: API #93 route/module/test not found. Application tests/runtime not run.
- Output manifest SHA-256: 431dca80bb04bbcbb0abe3525e351b094e4ece5fcab47cd5a73756a41e3908ed.
- The count inventory worklog was updated after API #93.
- No catalog, schema, diagram, runtime, or scope context was modified; context validator not applicable.

## HANDOFF

- Next API DD: #94, PUT /api/v1/admin/notifications/{notification_id}.
- AC-36 macro-review remains pending until #96 is complete.
- No application tests were run for this docs-only task.

## GROUP_MACRO_REVIEW

- Status: `VERIFIED_WITH_OPEN_QUESTIONS` after API #96 DD was created; document-level cross-review covers #92–#96.
- Report: `apps/study-server/docs/dd/96_admin_notifications_status/AC-36_MACRO_REVIEW.md`.
- Findings: list response/cardinality remains unresolved; #93 Notification-vs-Operation, conditional Send and ID bridge remain unresolved; #94 body/schedule are DERIVED; #95 delete/cancel and delivery-start policy are SOURCE_REQUIRED; #96 aggregate intent is not represented in its direct Notification response. Shared Admin model, grain, enums and permission remain open.
- Application tests, runtime and live schema were not checked as part of this document review.

---
task_id: "2026-10-24-create-study-api79-dd"
date: "2026-10-24"
primary_task_type: "docs"
secondary_task_types: []
project_scopes: ["server-study"]
cross_scope_dependencies: []
status: "VERIFIED"
---

# Worklog: Tạo DD Study API #79

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `deno run --allow-read --allow-env scripts/select-worklogs.mjs --type docs --limit 3`
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-10-24/create-study-api48-dd.md`
    - carry_forward: AC-21 DD giữ contract trực tiếp và đánh dấu schema/assets/identity chưa có source; dùng matrices trước authoring; không suy ra live schema.
  - path: `.agents/worklog/2026-10-24/create-study-api49-dd.md`
    - carry_forward: Content tree và Content response shape có discrepancy; không đổi singular `ApiEnvelope<Content>` thành tree nếu catalog chưa sửa; ghi candidate `DERIVED` và physical mapping `SOURCE_REQUIRED`.
  - path: `.agents/worklog/2026-10-24/create-study-api50-dd.md`
    - carry_forward: AC-22 create Content và AC-33 pending queue chỉ hỗ trợ trạng thái khởi tạo như proposal; Content persistence, payload, enum, Mentor/Admin identity vẫn chưa được runtime xác nhận.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Tạo DD Markdown tiếng Việt cho API #79, lập plan trước authoring, đọc kỹ AC-33, tham khảo #78 và DD Admin detail trước, kiểm tra DD ngay sau khi tạo.
- Catalog trực tiếp: `GET /api/v1/admin/content/{content_id}`; Bearer JWT/Admin; `content_id:int64!`; không body/query; HTTP 200 `DESIGN_RESOURCE_RETRIEVED`; `ApiEnvelope<Content>`; lỗi đúng 401 `DESIGN_AUTHENTICATION_REQUIRED`, 403 `DESIGN_ACCESS_DENIED`, 404 `DESIGN_RESOURCE_NOT_FOUND`, 500 `DESIGN_INTERNAL_ERROR`.
- Diagram trực tiếp: AC-33 n5 gọi #79 sau khi chọn Content từ queue; n6 đọc `content/version/author`; tiếp theo quyết định approve/reject sang #80/#81.
- Reusable `Content`: `id`, `course_id`, `content_type`, `title`, `payload`, `status`, `parent_id?`, `order`. Schema không có version/author/review metadata.

## CURRENT_BEHAVIOR

- Source/config: Không có route `/api/v1/admin/content/{content_id}`, module `api_79_*` hoặc focused test trong Study source. Current shared auth helper chỉ cho Student; Admin route/guard chưa được wire. Middleware allowlist không chứa endpoint #79; `error_response()` mặc định `data` lỗi thành `{}` dù API guideline nêu `null`.
- DB artifacts: Legacy `DB.sql` có `courses`, `lessons`, `resources`, không có generic Content/version/author relation. V1-PILOT `content_blocks` dùng UUID, gắn `lesson_id`, có JSON block payload; `content_review_decisions` là append-only log theo `resource_version_id` UUID và `reviewer_subject_id`. `course_versions.created_by_subject_id` là tác giả phiên bản Course trong pilot; không chứng minh tác giả của Content catalog BIGINT. Live DB chưa xác minh.
- Runnable tests: Không có test API #79; không chạy application tests trong task docs-only.
- Runtime wiring: `UNWIRED / NOT_FOUND`.

## SOURCE_TRACE

```text
Admin Bearer principal -> GET detail theo content_id -> authorize Admin trước khi đọc -> Q1 logical Content lookup theo ID -> AC-33 yêu cầu đọc version/author nhưng schema/identity mapping chưa được chọn -> map exact Content response catalog -> 200 hoặc exact 401/403/404/500 -> UI quyết định #80 approve hoặc #81 reject -> #78 reload queue
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| Runtime | Không route/module/test #79; Admin guard absent | `UNWIRED / NOT_FOUND` | Tài liệu không chứng minh runtime. |
| AC-33 metadata vs catalog response | Diagram n6 đọc `content/version/author`; catalog `ApiEnvelope<Content>` và Content schema không khai báo version/author | `DISCREPANCY / SOURCE_REQUIRED` | Không thêm response fields; contract owner cần quyết định projection nếu UI phải nhận metadata. |
| Content/version/author persistence | Legacy thiếu generic Content; V1-PILOT content blocks/version IDs/subject IDs khác Content BIGINT; không có author relation trực tiếp cho logical Content | `SOURCE_REQUIRED / NOT_VERIFIED` | Chỉ lập logical query; không bịa table/join/PK. |
| Review item identity | #78 queue, #79 detail, #80/#81 action đều định danh Content bằng BIGINT path; diagram đọc version nhưng không truyền version ID | `DISCREPANCY / SOURCE_REQUIRED` | Chưa biết revision nào được xem/quyết định hoặc cách chống stale review. |
| Pending-state detail rule | #78 lọc `PENDING_REVIEW`; AC-33 không ghi #79 phải lọc lại status hay cho xem mọi trạng thái | `DERIVED / OPEN` | Đề xuất lookup theo ID, trả status hiện có; không tự phát sinh state-conflict code. |
| Admin auth/error integration | Current guard Student-only; `DESIGN_CONTRACT_PATHS` thiếu path; helper error `data={}` | `DISCREPANCY / CONDITIONAL_FUTURE_WIRING` | Khi wire cần Admin policy và mapping lỗi theo catalog/guideline. |

## PLAN BEFORE DD AUTHORING

1. Giữ nguyên `GET /api/v1/admin/content/{content_id}`, Bearer/Admin, required path `content_id:int64!`, không body/query, direct response `ApiEnvelope<Content>`, HTTP 200 `DESIGN_RESOURCE_RETRIEVED`, và chỉ bốn lỗi 401/403/404/500 đã liệt kê.
2. Theo trang AC-33 đầy đủ: #78 queue → #79 detail đọc `content/version/author` → #80 approve hoặc #81 reject có reason → #78 reload. #79 là GET read-only, không đổi status/audit/decision.
3. Dùng logical Q1 `Content.id = :content_id` làm candidate đơn giản cho lookup; giữ status trong Content response. Không thêm predicate `PENDING_REVIEW` vào #79 nếu chưa có yêu cầu trực tiếp; status recheck/stale item policy ghi `DERIVED / OPEN`.
4. Ghi rõ diagram đòi version/author nhưng direct response Content không chứa hai nhóm field. Giữ đủ tám field Content; không thêm `version`, `author`, `review_reason`, reviewer hoặc decision history vào response.
5. Tách Q2 version selector và Q3 author resolution thành logical reads `SOURCE_REQUIRED`; không viết SQL/physical join vì Content, version và Content author schema chưa được chọn. Phân biệt author với reviewer (`content_review_decisions.reviewer_subject_id`).
6. Ghi mismatch BIGINT `Content.id` so với UUID pilot `content_blocks.id`/`resource_version_id`; không đổi ID hoặc map UUID sang BIGINT. `course_versions.created_by_subject_id` chỉ mô tả tác giả course-version trong pilot, không phải source direct cho Content contract.
7. Nếu Q1 không có Content theo ID, dùng catalog 404; lỗi đọc/mapping theo catalog 500; thiếu/invalid Bearer 401; principal không Admin 403. Không thêm 409/422 hoặc state error cho non-pending item.
8. Tạo 8 template sheets + `PLAN_RESULT.md`, `OPEN_QUESTIONS.md`, `VERIFICATION_REPORT.md`; `07_table.md` ghi `N/A — READ-ONLY API`; giữ appendix 8/8 byte-identical; Study workflow Markdown-only, không ZIP.
9. Các ma trận requirement, Request Usage, Query, Mutation, Response Source được ghi dưới đây trước khi tạo DD folder. Sau authoring, kiểm exact contract/codes/fields, JSON, links/anchors, tables/fences, front matter, appendices, whitespace/fingerprints và package set.
10. AC-33 macro-review #78–#81 vẫn pending cho đến khi DD #80/#81 tồn tại; không sửa DD #78 hiện tại trước group review.

### API Requirement Matrix

| API ID | Contract item | Giá trị | Basis/status |
|---|---|---|---|
| #79 | Method/path | `GET /api/v1/admin/content/{content_id}` | Catalog; DIRECT |
| #79 | Actor/auth | Bearer JWT; Admin | Catalog + AC-33; DIRECT requirement, runtime guard absent |
| #79 | Path | `content_id:int64!` | Catalog; DIRECT |
| #79 | Body/query | Không khai báo | Catalog; DIRECT absence |
| #79 | Success | 200 `DESIGN_RESOURCE_RETRIEVED`; `ApiEnvelope<Content>` | Catalog; DIRECT |
| #79 | Error | 401/403/404/500 với exact codes của catalog | Catalog; DIRECT |
| #79 | Detail reads | `content/version/author` | AC-33 n6; DIRECT internal/read intent; schema/response projection unresolved |
| #79 | Sequence | #78 → #79 → #80 hoặc #81 → reload #78 | AC-33 nodes/edges; DIRECT |

### Request Usage Matrix

| Request item | Source/use | Query/response use | Rule/status |
|---|---|---|---|
| Authorization | Bearer JWT; Admin role | Authenticate/authorize trước Q1 | Role DIRECT; Admin claim/guard SOURCE_REQUIRED |
| `content_id` | Required path int64 | Candidate bind tới logical Content ID; map `data.id` | Type DIRECT; physical key mapping SOURCE_REQUIRED |
| Body/query | None | None | DIRECT absence |

### Query Matrix

| Query | Kind | Logical target/fields | Predicate/result | Evidence/status |
|---|---|---|---|---|
| Q1 | SELECT candidate | Content `id`, `course_id`, `content_type`, `title`, `payload`, `status`, `parent_id`, `order` | `Content.id = :content_id`; no row → catalog 404 | Logical lookup DERIVED; table/columns SOURCE_REQUIRED |
| Q2 | SELECT logical only | Selected Content version/revision referenced by AC-33 n6 | Version selection and row identity unresolved | Read intent DIRECT; schema/selector SOURCE_REQUIRED |
| Q3 | SELECT logical only | Content author identity/projection referenced by AC-33 n6 | No author identity mapping or field in Content schema | Read intent DIRECT; relation/projection SOURCE_REQUIRED |
| N/A | No count/mutation | API detail is single-resource GET | No count, INSERT, UPDATE, DELETE or audit write | DIRECT method/flow |

### Mutation Matrix

| Operation | Target | Condition | Fields/effect | Status |
|---|---|---|---|---|
| None | N/A | API #79 is GET/read-only | Does not approve/reject, change Content, write decision/audit, or mark queue read | `N/A — READ-ONLY API` |

### Response Source Matrix

| Response field | Type | Logical source | Mapping/null rule | Evidence/status |
|---|---|---|---|---|
| `success` | boolean | Envelope branch | true success, false error | DIRECT envelope convention |
| `businessCode` | string | Catalog | `DESIGN_RESOURCE_RETRIEVED` or exact catalog error code | DIRECT |
| `message` | string | Application | Safe localized branch message; exact wording unspecified | DERIVED |
| `data` | `Content` object | Q1 logical Content | One Content; no Page/list wrapper | DIRECT type; physical row SOURCE_REQUIRED |
| `data.id` | int64 | Content ID | Bind/return logical resource identifier | DIRECT field; physical mapping SOURCE_REQUIRED |
| `data.course_id` | int64 | Content | Required | DIRECT field; physical mapping SOURCE_REQUIRED |
| `data.content_type` | ContentType | Content | Preserve approved serialization | DIRECT field; members SOURCE_REQUIRED |
| `data.title` | string | Content | Preserve stored title | DIRECT field; physical mapping SOURCE_REQUIRED |
| `data.payload` | object | Content | Do not invent members/default | DIRECT field; payload schema SOURCE_REQUIRED |
| `data.status` | ContentStatus | Content | Return selected row's current status | DIRECT field; enum/storage SOURCE_REQUIRED |
| `data.parent_id` | int64? | Content | Optional; null/omit rule unresolved | DIRECT optional field; source rule SOURCE_REQUIRED |
| `data.order` | int32 | Content | Preserve sibling order; not review ordering | DIRECT field; physical mapping SOURCE_REQUIRED |
| `data.version` / `data.author` | Not in catalog schema | AC-33 n6 internal/detail read | Do not serialize until schema/contract is approved | DISCREPANCY / SOURCE_REQUIRED |
| `meta` | object | Envelope | `{}` candidate, no pagination | DIRECT envelope convention |
| `traceId` | uuid | Trace middleware | Propagate/validate or generate per current convention | Current shared convention; route absent |
| Error `data` | null per API guideline | Current response helper | Helper currently defaults missing data to `{}` | DISCREPANCY |

## CHANGES

- Files changed: 11 Markdown files under apps/study-server/docs/dd/79_admin_content_detail/; this worklog and inventory-study-api-dd-counts.md updated.
- CONTEXT_UPDATES: None; no runtime/schema/catalog/diagram changes.
- Context pages changed: None.
- Assumptions: Direct Content shape wins for serialized response; Q1 by ID is a candidate; version/author reads remain logical-only and SOURCE_REQUIRED; no status mutation or extra business code.

## VERIFICATION

| Command/check | Result | Status |
|---|---|---|
| Worklog selector/review | Deno selector chose #48/#49/#50; all three were read in full. | `VERIFIED` |
| Registry/context | Root/global/context-map/server-study/workflow/manifest and skill routing inspected; `createDD-markdown` and `docs-dd` are wired to server-study. | `VERIFIED_STATIC_ONLY` |
| Diagram/catalog | API #79 row, reusable Content, AC-33 full nodes and edges, and AC-33 index entry read. | `VERIFIED_STATIC_ONLY` |
| Related DDs | #78 queue design and #69 Admin detail/#74 Admin course detail response patterns reviewed. | `VERIFIED_STATIC_ONLY` |
| Current source/schema | No #79 route/module/test; Student-only shared guard; middleware code allowlist gap; legacy and V1-PILOT Content/version mismatch inspected; live DB not verified. | `VERIFIED_STATIC_ONLY` |
| Template/archives | Registered 8-file Markdown template read; fingerprint `3dc7fd2242dd1ed1bd9faba50aadad913a31b97ebf1392d6144bb905c5208137`; no ZIP/XLSX/7z/RAR found in scoped diagram/skill paths. | `VERIFIED_STATIC_ONLY` |
| Plan-before-authoring | Requirement, Request Usage, Query, Mutation, Response Source matrices are recorded above before DD folder creation. | `VERIFIED` |
| Static DD validation | Exact 11-file set; 8/8 appendix parity; 2 JSON examples; 28 full-package tables; 5 balanced code fences; 32 local links/16 anchors; catalog codes/fields checked; fingerprints recorded; whitespace clean. | `VERIFIED_STATIC_ONLY` |
| Application tests | Not run; docs-only. | `NOT_RUN` |

## HANDOFF

- Remaining blockers: AC-33 metadata response projection, Content/version/author persistence and version identity, Admin guard, pending/stale detail rule and error helper integration.
- Next owner/action: Continue with API #80; complete AC-33 macro-review across #78–#81 after #81 is authored.


## CURRENT RECHECK AFTER API #79 — 2026-10-24

- API #79 DD: exact 11-file Markdown package; direct ApiEnvelope<Content> is preserved; AC-33 version/author metadata discrepancy and physical schema gaps remain explicit.
- Static validation: 8/8 template appendix suffixes byte-match; 2 JSON examples parse; 26 tables, five code fences, 32 local links/16 anchors and whitespace checks pass. Template SHA-256 3dc7fd2242dd1ed1bd9faba50aadad913a31b97ebf1392d6144bb905c5208137; payload SHA-256 97e5d2e6e778d9510430c39e07c08f99178d72d9063521ea53bead36b0a3486a.
- Application tests not run; no runtime route or live DB behavior was verified. AC-33 macro-review waits for #80/#81.
- Next DD: API #80.

## POST-AUTHORING AC-33 GROUP REVIEW — 2026-10-24

- Reviewed DD #78–#81 together after API #81 was created. The review is document-level; no API contract, source, schema or diagram was changed.
- Findings retain the response-cardinality mismatch in #78; version/author metadata projection gap in #79; `APPROVED/PUBLISHED`, separate #52 publish API and audit ambiguity for #80; and #81's `REJECTED` plus reason without an explicit audit append.
- Revision identity/stale decisions, Admin guard, generic Content persistence and #53 delete/lifecycle rules remain unresolved. The queue reload consequence applies only if the same underlying row's status is changed.
- Corrected local Data Mapping anchors in #79 that did not match the headings; all local links/anchors in #78–#81 now resolve.
- Full findings: `apps/study-server/docs/dd/81_admin_content_reject/VERIFICATION_REPORT.md`.
- API #79 documentation verification is complete; application tests/runtime were not run. Next DD: API #82.

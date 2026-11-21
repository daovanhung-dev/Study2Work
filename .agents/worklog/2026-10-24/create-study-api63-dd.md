---
task_id: "2026-10-24-create-study-api63-dd"
date: "2026-10-24"
primary_task_type: "docs"
secondary_task_types: []
project_scopes: ["server-study"]
cross_scope_dependencies: []
status: "VERIFIED"
---

# Worklog: Tạo DD Study API #63 — Tạo và phát thông báo

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `deno run --allow-read scripts/select-worklogs.mjs --type docs --limit 3`
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-10-24/create-study-api48-dd.md`
    - carry_forward: Bám AC và catalog; tách DIRECT/DERIVED/SOURCE_REQUIRED; không suy physical schema từ DDL candidate.
  - path: `.agents/worklog/2026-10-24/create-study-api49-dd.md`
    - carry_forward: Bốn ma trận trước authoring; giữ nguyên contract khi lệch diagram; không gộp API khác nhau.
  - path: `.agents/worklog/2026-10-24/create-study-api50-dd.md`
    - carry_forward: DB mapping có thể ghi logical entity với physical mapping `SOURCE_REQUIRED`; mọi đề xuất lifecycle phải `DERIVED` và cần xác nhận.
- shortage: `none`
- Additional related DDs reviewed: #18 Operation, #43 notification list, #45 mark-all notifications, #62 AC-25 recipient list.

## EXPECTED_BEHAVIOR

- Requirement: Tạo DD tiếng Việt cho API #63, lập và ghi plan/ma trận trước khi tạo thư mục DD; đối chiếu toàn bộ diagram AC-25; giữ tính nhất quán với #62, #64 và operation tracking #18; kiểm tra tĩnh ngay sau authoring. Macro-review nhóm AC-25 #62–#64 thực hiện sau khi #64 DD có mặt.
- Canonical contract `docs/lists/list_api.md` row #63: `POST /api/v1/mentor/notifications`; Bearer JWT, role Mentor; body `recipients:string!`, `title:string!`, `content:int64!`, `channels:string!`; HTTP 202 `DESIGN_OPERATION_ACCEPTED`; `ApiEnvelope<Operation>`; errors đúng 401 `DESIGN_AUTHENTICATION_REQUIRED`, 403 `DESIGN_ACCESS_DENIED`, 422 `DESIGN_VALIDATION_ERROR`, 503 `DESIGN_DEPENDENCY_UNAVAILABLE`, 500 `DESIGN_INTERNAL_ERROR`.
- AC-25 direct flow: Mentor chọn course/soạn thông báo → #62 đọc active enrollments → chọn người nhận/nhập tiêu đề/nội dung → #63 → ghi Notification + recipients → Push/Email theo channel → #64 đọc delivery status. AC/API index liệt kê cả GET operation #18; diagram có node #18 nhưng node này rời, không nối bằng edge với #62–#64.

## CURRENT_BEHAVIOR

- Source/config: Không tìm thấy route `/api/v1/mentor/notifications`, module `api_63_*`, test hoặc notification delivery provider trong Study source. `DESIGN_CONTRACT_PATHS` không gồm path #63. API #63 là `UNWIRED / NOT_FOUND`; chưa có runtime để kiểm chứng.
- Database artifacts: Legacy `notifications` có BIGSERIAL id, nullable `user_id`/`sender_id`, title VARCHAR(200), content TEXT, type, is_read, created_at; không có bảng recipient riêng, channel, delivery status hoặc Operation. V1-PILOT có notification theo `learner_id UUID` và delivery rows UUID với channel `IN_APP|EMAIL`, status `QUEUED|SENT|DELIVERED|FAILED|SUPPRESSED`; model không khớp API ID int64 hoặc Push channel của AC-25. Không nguồn nào xác nhận live schema.
- Shared contract: reusable `Operation.id` là UUID, còn row API #18 khai báo `operation_id:int64`; AC-25 diagram node #18 khai báo UUID. `Operation.result` hiện là `Payment?`, không có result notification chuẩn. #63 trả Operation, trong khi #64 nhận `notification_id:int64` và trả Operation; không thấy nguồn nào cung cấp notification_id cho client từ #63.
- Related API discrepancy: catalog row #93 (Admin create/send) nhận recipients array/segment, title/content string và channels enum array, nhưng khai báo `ApiEnvelope<Notification>` dù HTTP 202; Operation tracking summary lại nói API #93 trả Operation. Không sao chép contract Admin sang Mentor.
- Runnable tests: Không chạy; docs-only; không có test API #63.

## SOURCE_TRACE

```text
Mentor + course chọn ở UI -> #62 (response Page<Course> đang lệch roster) -> chọn recipients/title/content -> POST #63 -> logical INSERT Notification + recipient rows -> dispatch Push/Email bất đồng bộ -> trả Operation/202 -> #64 đọc delivery theo notification_id:int64; API #18 operation polling là nhánh riêng chưa được nối rõ
```

## PLAN BEFORE DD AUTHORING

1. Giữ exact catalog contract #63 trong Requirement/Request/Response/Error matrices: POST/path, Bearer Mentor, đủ bốn body fields và đúng kiểu trực tiếp; HTTP 202 `DESIGN_OPERATION_ACCEPTED`; `ApiEnvelope<Operation>`; chỉ năm lỗi 401/403/422/503/500. Không đưa đề xuất hiệu chỉnh vào cột direct.
2. Bám tất cả node/edge AC-25: #63 là bước sau chọn recipients; mutation logic ghi Notification + recipients; Push/Email được chọn; #64 đọc delivery status. Ghi node operation #18 riêng vì diagram không có edge tới node này, nhưng AC/API index liệt kê nó.
3. Rà lại #62, #43, #45, #18, #50 và #93 để thống nhất các ranh giới: #62 chọn người nhận; #63 tạo/gửi; #64 đọc trạng thái gửi; #18 theo dõi job; không gộp read-state API #43–#45 hay Admin #93 vào Mentor flow.
4. Ghi discrepancy chính: diagram/UI + Notification schema nói content là text nhưng request #63 khai báo `content:int64`; body không có `course_id` nên server không thể xác thực tập recipient thuộc course đã chọn; `recipients:string` và `channels:string` chưa có encoding; Operation response không nối được với #64 `notification_id:int64` và reusable result Payment không phải NotificationDelivery.
5. Đưa khuyến nghị đơn giản dưới nhãn `DERIVED — cần duyệt`, không thay direct contract: thêm `course_id:int64`; biểu diễn recipients là danh sách ID Student duy nhất (nếu phải giữ string thì đề nghị chuỗi CSV số int64); đổi content sang `string`; quy ước channels thành danh sách tên channel từ Push/Email. Validation tối thiểu: bắt buộc không rỗng, loại recipient không thuộc active roster/course, không gửi trùng; chính sách/mã lỗi cần khớp catalog. Không gán enum member hoặc giới hạn độ dài chưa có nguồn.
6. Giữ persistence tách biệt: legacy notification là candidate theo user_id đơn lẻ, pilot notification/delivery UUID theo learner; không ghép hai model, không invent recipient table/outbox/Operation table/SQL. Mutation mapping sẽ mô tả logical Notification + recipients + async Operation, physical target `SOURCE_REQUIRED`.
7. Không đưa provider call vào transaction DB như hành vi đã duyệt. Mô tả 202 là accepted-for-processing theo contract; cơ chế durable queue/outbox, retry, partial failure, operation lifecycle và commit boundary cần thiết kế xác nhận. Không khẳng định delivery thành công ngay khi nhận 202.
8. Tạo 8 sheet template + 3 report Markdown, `07_table.md` cho logical writes với physical mapping unresolved, không ZIP/runtime/schema/catalog/diagram edits. Fingerprint/template appendix phải khớp bộ template hiện hành.
9. Static verify exact 11-file manifest, front matter 8 sheet, template fingerprints/appendix, exact request/response/error fields, JSON, link/anchor, table widths, fences, whitespace và `git diff --check`. Runtime tests `NOT_RUN`.
10. Không đóng macro-review AC-25 tại #63; ghi handoff để rà #62–#64 cùng operation #18 ngay sau khi tạo DD #64.

### API Requirement Matrix — plan gate

| API ID | Method/path | Actor/auth | Input | Success/response | Errors | Status |
|---|---|---|---|---|---|---|
| #63 | `POST /api/v1/mentor/notifications` | Bearer JWT; Mentor | `recipients:string!`, `title:string!`, `content:int64!`, `channels:string!` | HTTP 202 `DESIGN_OPERATION_ACCEPTED`; `ApiEnvelope<Operation>` | 401 `DESIGN_AUTHENTICATION_REQUIRED`; 403 `DESIGN_ACCESS_DENIED`; 422 `DESIGN_VALIDATION_ERROR`; 503 `DESIGN_DEPENDENCY_UNAVAILABLE`; 500 `DESIGN_INTERNAL_ERROR` | Catalog DIRECT; recipient scope/content/encoding/operation handoff conflicts open |

### Request Usage Matrix — plan gate

| Request item | Contract source/use | Mapping/side-effect use | Evidence/gap |
|---|---|---|---|
| Authorization | Header; authenticate Bearer and Mentor role | Sender/owner and course scope | Role DIRECT; Mentor guard/identity mapping SOURCE_REQUIRED |
| `recipients` | Required string | Resolve selected Student recipients; write recipient associations; dispatch | Type DIRECT; encoding, ID kind, dedup and course membership SOURCE_REQUIRED; CSV int64 list is DERIVED recommendation |
| `title` | Required string | Notification title | DIRECT; non-empty/length policy SOURCE_REQUIRED; legacy/pilot max 200 is only schema candidate |
| `content` | Required int64 | Notification body or content reference | DIRECT conflicts with UI text entry and Notification.content:string; correction to string DERIVED recommendation |
| `channels` | Required string | Select Push/Email work | Type DIRECT; encoding and allowed machine values SOURCE_REQUIRED; comma-separated labels is a DERIVED recommendation |
| `course_id` | Not declared | Needed to authorize selected recipients against chosen course | Do not add to direct contract; recommend as security/flow contract correction |
| `Idempotency-Key` | Shared API guideline for retryable mutation | Avoid duplicate Notification/dispatch on POST retry | Not in catalog; requiredness/storage mapping SOURCE_REQUIRED; do not silently add as direct field |

### Query / Mutation / Response Matrix — plan gate

| ID | Type/target | Purpose/fields | Status |
|---|---|---|---|
| Q1 | SELECT course + active roster | Revalidate recipient IDs within Mentor-managed selected course | No `course_id` in direct body; physical relationship/live schema absent; cannot approve query; added course_id is recommended |
| M1 | Logical INSERT Notification | title/content/sender and creation identity | Diagram DIRECT; physical target/schema conflict; SOURCE_REQUIRED |
| M2 | Logical INSERT recipient associations | Associate notification to each unique selected learner | Diagram DIRECT; no approved physical recipient table; SOURCE_REQUIRED |
| M3 | Create Operation + enqueue delivery work | 202 acceptance and asynchronous Push/Email | Response/diagram DIRECT; Operation persistence, queue and transaction SOURCE_REQUIRED |
| R1 | `ApiEnvelope<Operation>` | Envelope + Operation fields from reusable schema | Response shape DIRECT; enums/result source absent; `result?:Payment` conflicts with notification work |
| R2 | Handoff to #64 | Need `notification_id:int64` for status lookup | No #63 response mapping established; blocker for AC-25 integration |

## Source coverage captured before DD creation

- Read skill `createDD-markdown`, manifest registry entry, Study workflow, and eight-template baseline fingerprint from API #62 verification; skill boundary confirms exact templates, matrix-first, source traceability, and no invented table/field.
- Parsed every AC-25 diagram node and edge. Nodes establish n1–n10 flow; `operation_status` (#18) is present but has no connecting edge.
- Read AC/API index AC-25, API catalog rows #18/#62/#63/#64/#93, Operation/Notification/NotificationDelivery reusable schemas, Operation tracking summary and global ID convention.
- Reviewed DD #62, #18, #43, #45, #50, plus Admin #93 catalog row; checked legacy DB guide/DDL, V1-PILOT DDL, current Study router/middleware/provider/test source and API Guidelines.

## CHANGES

- Files changed: `apps/study-server/docs/dd/63_mentor_notifications_create/` (8 template sheets + 3 reports), this worklog, and `.agents/worklog/2026-10-24/inventory-study-api-dd-counts.md`.
- CONTEXT_UPDATES: None; no source/schema/catalog/diagram/context page edits.
- Context pages changed: None.
- Assumptions: Keep all suggested body parsing, field correction, course binding and operation result bridge as `DERIVED`; direct API row remains authoritative in direct-contract matrices.

## VERIFICATION

| Command/check | Result | Status |
|---|---|---|
| Worklog selector/review | Deno selector selected #48/#49/#50; all three read in full; shortage none. | `VERIFIED` |
| Context and skill registry | Root/global context, context map, Study scope/workflow, `createDD-markdown` registry entry/skill read. | `VERIFIED_STATIC_ONLY` |
| AC-25 diagram | Decoded page AC-25; all 10 sequence nodes + detached #18 node and all edges inspected. | `VERIFIED_STATIC_ONLY` |
| Catalog/API schemas | Rows #18/#62/#63/#64/#93, reusable Notification/Operation/NotificationDelivery schemas read. | `VERIFIED_STATIC_ONLY` |
| Prior DDs | #18, #43, #45, #50, #62 read for related lifecycle, schema and style evidence. | `VERIFIED_STATIC_ONLY` |
| Current source/DB | #63 route/module/provider/test absent; legacy/pilot model differences recorded; live schema not verified. | `VERIFIED_STATIC_ONLY` |
| DD manifest/template/contract/Markdown verification | 11/11 files; 8/8 front matter and template fingerprints; appendix byte match 8/8; direct body, response and five errors match; 3 JSON parsed; 40 local links resolve; 515 table rows consistent; fences/whitespace and `git diff --check` pass. | `VERIFIED_STATIC_ONLY` |
| Runtime tests | Not run: docs-only; API #63 remains `UNWIRED / NOT_FOUND`. | `NOT_RUN` |

## HANDOFF

- Remaining blockers: Direct request has no course scope, content type conflicts, recipient/channel serialization undefined, notification/recipient/operation persistence unavailable, and no response field maps to #64 notification_id.
- Next owner/action: API #64 and the AC-25 #62–#64/#18 macro-review are complete with open questions; continue at API #65.


## GROUP_MACRO_REVIEW — AC-25 after API #64

- Status: `VERIFIED_WITH_OPEN_QUESTIONS` at document level.
- Cross-API findings: #62 roster response/key is unresolved; #63 recipient/course/content/channel contract is unresolved; #63 Operation response does not supply #64 notification_id; #64 response Operation does not carry delivery summary; #18 job polling remains detached and has its own UUID/int64 and result conflicts.
- Legacy and V1-PILOT notification/delivery schemas remain alternatives; no physical query or Mentor authorization relation was approved. No direct contract was silently changed.
- Group report: `apps/study-server/docs/dd/64_mentor_notifications_status/VERIFICATION_REPORT.md`.

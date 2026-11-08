# ST-18 — Events (đặc tả xử lý)

## 1. Event index
| Event ID trong package | Source Event ID / heading | Chi tiết |
|---|---|---|
| `ST-18-EV-001` | `ST18-EV-01` / ST18-EV-01 — Mở ST-18 và đọc Assignment | See source event detail below |
| `ST-18-EV-002` | `ST18-EV-02` / ST18-EV-02 — Ánh xạ context, eligibility và thông tin read-only | See source event detail below |
| `ST-18-EV-003` | `ST18-EV-03` / ST18-EV-03 — Nhập GitHub và deployment URLs | See source event detail below |
| `ST-18-EV-004` | `ST18-EV-04` / ST18-EV-04 — Chọn và upload từng file qua #34 | See source event detail below |
| `ST-18-EV-005` | `ST18-EV-05` / ST18-EV-05 — Preview uploaded file | See source event detail below |
| `ST-18-EV-006` | `ST18-EV-06` / ST18-EV-06 — Remove selected/uploaded file | See source event detail below |
| `ST-18-EV-007` | `ST18-EV-07` / ST18-EV-07 — Sửa ghi chú/self-reflection | See source event detail below |
| `ST-18-EV-008` | `ST18-EV-08` / ST18-EV-08 — Xác nhận academic integrity | See source event detail below |
| `ST-18-EV-009` | `ST18-EV-09` / ST18-EV-09 — Lưu bản nháp / autosave indicator | See source event detail below |
| `ST-18-EV-010` | `ST18-EV-10` / ST18-EV-10 — Khôi phục bản nháp trước | See source event detail below |
| `ST-18-EV-011` | `ST18-EV-11` / ST18-EV-11 — Hủy và quay lại ST-17 | See source event detail below |
| `ST-18-EV-012` | `ST18-EV-12` / ST18-EV-12 — Submit assignment qua #35 | See source event detail below |
| `ST-18-EV-013` | `ST18-EV-13` / ST18-EV-13 — Header/footer navigation | See source event detail below |

> Event IDs trong package là alias để theo template; Source Event IDs, steps và API links giữ theo DD nguồn. Alias không chứng minh event runtime.

## 2. Chi tiết event từ DD nguồn

### Trích từ DD nguồn: D. Đặc tả events

### ST18-EV-01 — Mở ST-18 và đọc Assignment

- **Trigger/type:** route load; no dedicated marker. Input assignmentId from proposed path and Student auth context.
- **Precondition:** authenticated Student per expected screen policy; route and authorization are not current Study Web behavior.
- **Processing:** (1) read path value without inventing positivity/overflow rules; (2) decide with product whether ST-18 refetches #33 or reuses validated ST-17 state; (3) if refetch is required, send GET /api/v1/assignments/{assignment_id} with Bearer and no query/body; (4) parse only ApiEnvelope<Assignment>; (5) map fields in EV-02; (6) surface catalog errors and keep user input untouched if this is a re-entry.
- **Response/error:** catalog 200 DESIGN_RESOURCE_RETRIEVED; 401 authentication; 403 access; 404 resource; 500 internal. AC-17 deadline 409 is not in #33 catalog. No route/module/test exists.
- **Result:** enter assignment-context loading/editing only when an approved policy says it is eligible. Cache, retry, timeout and duplicate-request policy are open.

### ST18-EV-02 — Ánh xạ context, eligibility và thông tin read-only

- **Trigger/type:** #33 response mapping/render.
- **Input:** candidate Assignment{id, course_id, title, description?, due_at?, max_score} plus server access/deadline decision, if defined.
- **Processing:** (1) validate success envelope; (2) map only fields in the approved Assignment schema; (3) treat countdown as display-only and do not infer authorization from local clock; (4) keep checklist, rubric, mentor, review SLA, progress and history unsourced unless a separate approved projection is provided; (5) do not render screenshot sample values as fetched data.
- **Output:** loading → editing or server-denied/not-found/error states per future contract. Access/deadline boundary, timezone and submission-rule response are unresolved; #33 DD remains Draft.

### ST18-EV-03 — Nhập GitHub và deployment URLs

- **Trigger/type:** input/change/blur on ST18-EL-15 and ST18-EL-18.
- **Precondition:** form is editable; visual required badges do not establish approved server validation.
- **Processing:** (1) keep each field separately as in-progress UI state while the screen is open; (2) do not trim, normalize, probe URLs or claim repository validity without policy; (3) no #35 field corresponds to these URLs; (4) do not fold them into text without owner approval; (5) do not infer how values persist after API error, route leave or reload.
- **Output:** visible design state only. Requiredness, format, reachability, draft persistence and retention after errors are SOURCE_REQUIRED.

### ST18-EV-04 — Chọn và upload từng file qua #34

- **Trigger/type:** click/drop/file selection; one multipart upload per needed file per inventory/F06.
- **Request:** POST /api/v1/uploads, Authorization: Bearer, multipart/form-data parts file (binary), purpose=SUBMISSION, optional course_id:int64. API catalog does not specify count, sequence, parallelism, retry or max size.
- **Current source path:** FastAPI /uploads → create_upload → validate_current_user_request for Student/Mentor → validate_upload_policy maps Student to SUBMISSION and Mentor to LECTURE → optional enrollment/direct-course scope query → measure bytes and reset stream → provider uploads to S3-compatible storage under server-generated uploads/{UUID} → insert uploads metadata → commit → UploadAsset envelope.
- **Current source rules:** Student course_id may be omitted; if supplied, source checks an ACTIVE enrollment for current user/course. No application MIME allowlist or size cap. Missing filename becomes upload; missing Content-Type becomes application/octet-stream. Returned URL is configured public base plus storage key.
- **Success:** HTTP 201 DESIGN_RESOURCE_CREATED; data{id,name,url,content_type,size_bytes,status} with status UPLOADED. This means that file/object metadata was saved, not that the assignment submission exists.
- **Errors:** multipart File/Form parsing and malformed/missing required fields can return 422 before `create_upload`; the source tests cover malformed multipart without storage calls. Once in the view: 401 invalid/missing Bearer; 403 role/purpose or supplied course scope denial; 422 course range/purpose validation; 503 object-storage failure (source attempts best-effort delete); 500 size-measurement or DB/internal failure (rollback and best-effort object delete after an object may exist). Exact frontend progress %, upload limits, retry, and whether to send `course_id` are not decided.
- **State:** per file, selected → uploading → uploaded or failed. Do not mark the whole screen submitted here. If a later file fails, prior uploaded objects may remain; cleanup, retry, and preservation of the selected file/form values are open.

### ST18-EV-05 — Preview uploaded file

- **Trigger/type:** click/tap/keyboard on preview action.
- **Input:** candidate UploadAsset.url returned from #34; sample PNG file row alone is not authority.
- **Processing:** current #34 creates a public-base URL. Before opening/embedding it, product/security must approve access, expiry, download headers and whether URL exposure is acceptable. Do not assume a protected/signed preview or add a new endpoint.
- **Output/error:** no preview event is wired in Study Web. Behavior for an inaccessible URL, expired object or denied access is undefined until the URL/access policy is approved.

### ST18-EV-06 — Remove selected/uploaded file

- **Trigger/type:** click/tap/keyboard on remove action.
- **Processing:** remove a not-yet-uploaded local selection if such behavior is approved; for an object already stored by #34, no delete endpoint/module exists. Removing only the UI row can orphan an object and retained uploads metadata. Do not imply storage deletion or cleanup.
- **Output/errors:** UI removal semantics, confirmation, count update and server cleanup need an approved contract. A later #35 request must not reference a removed asset, but the reference format itself is unresolved.

### ST18-EV-07 — Sửa ghi chú/self-reflection

- **Trigger/type:** input/change and toolbar click in editor.
- **Input:** text string; current screenshot shows a Markdown-support note, toolbar and sample content.
- **Processing:** maintain editor content as a draft candidate; toolbar action serialization, Markdown parsing, HTML sanitization, length units, maximum length, empty/whitespace rule and any persistence are unspecified. Catalog #35 names required text:string, but does not explicitly equate it with this editor.
- **Output:** text's persistence after failure or route leave is unresolved; send under #35 only when mapping and validation are approved. No current editor exists.

### ST18-EV-08 — Xác nhận academic integrity

- **Trigger/type:** checkbox toggle by pointer or keyboard.
- **Input:** boolean checked state as shown in screenshot.
- **Processing:** no request field, policy version, consent endpoint or gating rule is declared. Do not block #35 solely from an assumed requirement and do not claim the acknowledgement is audited.
- **Output:** design-only local state until a canonical rule is provided; accessible label/state required when implemented.

### ST18-EV-09 — Lưu bản nháp / autosave indicator

- **Trigger/type:** save button click and/or draft autosave timer in design.
- **Input:** all visible form fields, uploaded file references and timestamp, but the contract defines no draft object/schema.
- **Processing:** do not call final-submit API #35 to save a draft. No draft endpoint is listed. Screenshot claims server autosave, but no autosave API, debounce, persistence, status/conflict behavior or storage source exists.
- **Output/errors:** “saved” state cannot be asserted until persistence is confirmed; define local-vs-server save, failed save, retry and page-exit behavior first. Retention of entered values after errors is unresolved.

### ST18-EV-10 — Khôi phục bản nháp trước

- **Trigger/type:** click restore action in prior draft row.
- **Input:** draft version #02 and timestamp are screenshot samples; no stable draft ID/schema supplied.
- **Processing/output:** source draft, overwrite/merge scope, attachment restoration and confirmation are undefined. Do not restore the sample text or fabricate a history API.

### ST18-EV-11 — Hủy và quay lại ST-17

- **Trigger/type:** cancel/back button, breadcrumb or browser navigation.
- **Input:** current assignmentId, unsaved local fields and possibly already-uploaded asset IDs.
- **Processing:** target route is proposed ST-17 /student/assignments/:assignmentId; no route is wired. Confirm-before-discard, draft retention and cleanup of uploaded objects are open. Do not delete objects by leaving the page.
- **Output:** when approved, return to ST-17 with assignment context. Whether to warn, persist, discard or restore the current form is unresolved; F06 does not specify API-error retention. Direct browser back behavior is not specified.

### ST18-EV-12 — Submit assignment qua #35

- **Trigger/type:** final submit click; use submitting/disabled visual state to prevent immediate duplicate clicks only after UI behavior is approved.
- **Precondition:** assignment eligibility/deadline is established by server contract; any required fields/checklist/consent are validated under approved rules; all needed uploads have completed successfully.
- **Input:** route assignment_id:int64, Student Bearer, required catalog body strings text and file refs. Catalog does not define content type, exact file-ref JSON key, encoding, asset ID/URL choice or cardinality. URLs/checklist/consent are not catalog fields.
- **Processing:** (1) collect approved text and references; (2) do not invent file_refs, JSON-string encoding, [], upload ownership claim or deduplication; (3) send one POST to /api/v1/assignments/{assignment_id}/submissions; (4) parse only the approved envelope and response; (5) mark submitted only on confirmed 201; (6) route to ST-19 using the approved ID field. Do not auto-retry an ambiguous timeout until #35 idempotency/reconciliation is defined.
- **Success/errors:** catalog success 201 DESIGN_RESOURCE_CREATED; errors 401/403/404/422/409/500 with corresponding design business codes. Exact 409 condition, access/deadline mapping, error message and duplicate/resubmit policy remain open. Candidate data.id conflicts with inventory submission_id.
- **Persistence gaps:** candidate DDL assignment_submissions.file_url is scalar; logical Submission.files[] is an array. No association table, insert/update key, transaction/lock/rollback/idempotency or orphan cleanup is established. API #35 has no source route/module/test.
- **Output:** keep entered text/URLs and show an honest failed/ambiguous state on error; distinguish it from per-file upload status. After success, hand off confirmed ID to ST-19. The inventory assigns GET #36 to ST-19; AC-17 puts GET #36 after #35 in its diagram. Keep this sequencing as an open discrepancy; do not issue #36 from ST-18 without owner approval.

### ST18-EV-13 — Header/footer navigation

- **Trigger/type:** input/change in search; pointer/keyboard activation of brand, nav/footer links, notification and profile controls.
- **Input/precondition:** search text or activated control; no destination, query API, current Student route, auth redirect or notification/profile contract is defined.
- **Processing:** code.html uses placeholder anchors plus `#/student/assignments/detail` for its fallback button and has no screen-specific navigation/event handler. Treat those as prototype text, not verified route targets. Do not call an API or construct new paths from labels.
- **Output/error:** no ST-18 navigation result is source-backed. Future route-not-found, access-denied and session-expired handling belongs to approved Study Web navigation/auth policy; keyboard, focus and accessible names must follow `.agents/web-study/design.md`.

## Trace links
- [UI Elements](01-ui-elements.md) · [API Integration](04-api-integration.md) · [Business Rules](05-business-rules.md) · [Navigation](06-navigation.md) · [Test Cases](07-test-cases.md)

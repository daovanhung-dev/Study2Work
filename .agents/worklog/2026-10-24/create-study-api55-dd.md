---
task_id: "2026-10-24-create-study-api55-dd"
date: "2026-10-24"
primary_task_type: "docs"
secondary_task_types: []
project_scopes: ["server-study"]
cross_scope_dependencies: []
status: "VERIFIED"
---

# Worklog: Tạo DD Study API #55 — Lấy bài làm và rubric Mentor

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `deno run --allow-read --allow-env scripts/select-worklogs.mjs --type docs --limit 3`
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-10-24/create-study-api48-dd.md`
    - carry_forward: Giữ exact catalog contract; các quan hệ Mentor/assignment, schema và identity chỉ là DERIVED/SOURCE_REQUIRED; dùng 8 sheets + 3 report, Markdown-only.
  - path: `.agents/worklog/2026-10-24/create-study-api49-dd.md`
    - carry_forward: Không trộn API endpoint khác nhau trong cùng AC; không dùng schema pilot UUID để map ngầm sang contract BIGINT; ghi rõ query tree chưa có nguồn.
  - path: `.agents/worklog/2026-10-24/create-study-api50-dd.md`
    - carry_forward: Đánh dấu proposal ngoài diagram là DERIVED; giữ unresolved schema, role, payload và enum; kiểm tra đủ 11 artifact và template appendix.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Tạo một API DD tiếng Việt cho API #55, lập plan trước khi tạo DD, đọc toàn bộ flow AC-23, đối chiếu DD trước và kiểm tra ngay sau khi authoring.
- Canonical contract: `GET /api/v1/mentor/submissions/{submission_id}`, Bearer JWT, role Mentor, path `submission_id:int64!`, response `ApiEnvelope<Submission>`, HTTP 200 `DESIGN_RESOURCE_RETRIEVED`, errors đúng 401/403/404/500 theo `docs/lists/list_api.md`.
- AC-23: Mentor có quyền chấm submission của course; flow chọn một submission → API #55 đọc Submission + files + rubric → nhập điểm/nhận xét → API #56 lưu grade → API #57 lưu feedback; postcondition là grade và feedback đã lưu, Student có thể nhận kết quả.
- Output: `apps/study-server/docs/dd/55_mentor_submissions_detail/`, tám sheet Markdown theo template cùng `PLAN_RESULT.md`, `OPEN_QUESTIONS.md`, `VERIFICATION_REPORT.md`; không tạo ZIP hoặc sửa runtime/schema/catalog/diagram.

## CURRENT_BEHAVIOR

- Source/config: Không có route, module hoặc test API #55 trong Study Server. Current JWT helper có `sub` số và `roles`, nhưng shared request guard chỉ cho Student. Middleware path allowlist chưa có API #55; nếu wiring trong tương lai không cập nhật, lỗi framework có thể dùng code fallback khác catalog. Current `error_response` serializes `data=None` thành `{}`, trong khi API Guidelines kỳ vọng `null`.
- Candidate schema: Legacy `infra/postgres/study-server/DB.sql` có `assignment_submissions` với `id`, `assignment_id`, `user_id`, `content`, một `file_url`, `submitted_at`, `score`, `feedback`, `status`; `assignment_id` và `user_id` cho phép NULL. DB table guide/ERD mô tả hai FK required. Đây chỉ là design candidate, live DB chưa kiểm tra.
- Rubric schema: Checked-in V1-PILOT `infra/postgres/02_study_db.sql` có `rubrics.assessment_id UUID` và `rubric_criteria`; không có liên kết source-backed giữa các bảng này với legacy `assignments`/`assignment_submissions` BIGINT. Không dùng chúng làm query API #55.
- Contract/schema gap: Reusable `Submission` có `files:UploadAsset[]`, score và feedback nhưng không có field rubric; candidate legacy có duy nhất `file_url`, không đủ metadata UploadAsset. AC-23 diagram yêu cầu đọc files + rubric.
- Runnable tests: Không có test module API #55; không chạy test trong docs-only task.
- Runtime wiring: `UNWIRED / NOT_FOUND`; không khẳng định runtime behavior hoặc live schema.

## SOURCE_TRACE

```text
GET #55 + Bearer Mentor -> parse submission_id -> candidate lookup assignment_submissions -> derive assignment/course scope -> check Mentor authorization -> map Submission -> resolve files/rubric (SOURCE_REQUIRED) -> ApiEnvelope -> UI calls #56 grade then #57 feedback
```

## PLAN BEFORE DD AUTHORING

### API Requirement Matrix

| API ID | Method/path | Actor/auth | Input | Success | Errors | Flow / status |
|---|---|---|---|---|---|---|
| #55 | `GET /api/v1/mentor/submissions/{submission_id}` | Mentor / Bearer JWT | Path `submission_id:int64!`; no body/query | HTTP 200 `DESIGN_RESOURCE_RETRIEVED`; `ApiEnvelope<Submission>` | 401 `DESIGN_AUTHENTICATION_REQUIRED`; 403 `DESIGN_ACCESS_DENIED`; 404 `DESIGN_RESOURCE_NOT_FOUND`; 500 `DESIGN_INTERNAL_ERROR` | AC-23 reads one selected submission before #56/#57; design-only, current source unwired |

### Request Usage Matrix

| Request item | Source/use | Validation | Query/response use | Gap |
|---|---|---|---|---|
| Authorization | Header | Bearer JWT; role Mentor | Principal for course permission | Mentor guard absent; numeric `sub`/`roles` shape source-backed, Mentor-specific policy DERIVED |
| `submission_id` | Required path int64 | No min/max or malformed-path behavior declared | Candidate `assignment_submissions.id`; maps to `data.id` | Invalid-path mapping not in error set |
| Body/query | None | N/A | N/A | DIRECT from catalog |

### Query Matrix

| Query | Type | Candidate source/columns | Purpose | Evidence/status |
|---|---|---|---|---|
| Q1 | SELECT | `assignment_submissions s`; LEFT JOIN `assignments a` on `a.id=s.assignment_id`; LEFT JOIN `courses c` on `c.id=a.course_id`; filter `s.id=:submission_id`; select candidate response fields and owner relation | Preserve existence, then check course permission before serializing any submission data | Legacy design candidate; joins nullable; direct-owner predicate `c.mentor_id=:mentor_id` is DERIVED from related Mentor DDs |
| Q2 | SELECT | No approved UploadAsset association/metadata relation | Resolve `files[]` | `SOURCE_REQUIRED`; do not convert `file_url` to a fabricated asset |
| Q3 | SELECT | No assignment-to-rubric relation in legacy design; V1 rubric belongs to UUID `assessment_id` | Resolve rubric named by AC-23 | `SOURCE_REQUIRED`; no cross-schema join |

### Mutation Matrix

| Operation | Target | Result |
|---|---|---|
| INSERT/UPDATE/DELETE | N/A | Read-only API; `07_table.md` will state `N/A — READ-ONLY API` |

### Response Source Matrix

| Response field | Candidate source | Mapping/null rule | Gap/status |
|---|---|---|---|
| Envelope fields | API Guidelines/current response helper | Exact catalog business code; `meta`/trace convention | Error `data:null` vs current `{}` discrepancy |
| `data.id` | `s.id` | Direct candidate | Legacy BIGINT; live DB unknown |
| `data.assignment_id` | `s.assignment_id` | Direct candidate | DDL nullable vs contract required |
| `data.user_id` | `s.user_id` | Direct candidate; do not expose additional profile fields | DDL nullable vs contract required |
| `data.content` | `s.content` | Preserve optional value | Null/omit rule open |
| `data.files[]` and nested UploadAsset fields | No approved source | No fabricated values/empty array | `SOURCE_REQUIRED` |
| `data.status` | `s.status` | Preserve candidate value | SubmissionStatus members/serialization open |
| `data.submitted_at` | `s.submitted_at` | Serialize date-time | Timestamp zone/precision open |
| `data.score` | `s.score` | Candidate NUMERIC to decimal-string | API #56 uses `int32`; max-score bounds/rounding open |
| `data.feedback` | `s.feedback` | Preserve optional value | Null/omit and Student disclosure policy open |
| Rubric | No field in reusable `Submission` | Keep exact response contract | Diagram requests rubric; contract/schema conflict |

### Plan / authoring order

1. Giữ nguyên method/path/auth/path type/success/error contract của catalog; không tự thêm query, body, response property, HTTP status hoặc business code.
2. Dùng toàn bộ node/edge AC-23 để giữ thứ tự #54 → #55 → #56 → #57; API #55 chỉ đọc, không ghi điểm/feedback.
3. Tham khảo #54, #36, #35 và #46/#47; kế thừa ranh giới Mentor ownership, file metadata, schema và grade disclosure còn mở, không âm thầm coi candidate là contract.
4. Đề xuất query đơn giản từ `assignment_submissions` qua `assignments.course_id` và `courses.mentor_id`; candidate trực tiếp sở hữu course là DERIVED. Tách 404 không có record, 403 không được quyền; hàng orphan/null quan hệ là lỗi integrity candidate 500, chờ xác nhận.
5. Không query `rubrics` từ V1-PILOT vào submission legacy: DDL đó dùng UUID và `rubrics.assessment_id`, không có relation đến assignment/submission. Không thêm `rubric` vào `ApiEnvelope<Submission>`; giữ conflict và đề xuất owner cập nhật schema contract/diagram đồng bộ.
6. Không map `file_url` thành `UploadAsset[]`, không bịa rubric, status enum, query pagination, score transformation khác decimal-string hoặc asset table.
7. Tạo Data Mapping trước khi hoàn thiện Request/Response; bao phủ mọi field, condition, query, access, error và read-only table mapping theo template.
8. Tạo `PLAN_RESULT.md` trước tám sheet; sau đó tám sheet + open questions + verification report trong đúng folder. Tất cả nội dung tiếng Việt, 8 phụ lục template giữ nguyên byte-for-byte.
9. Verify manifest, catalog codes, response field matrix, diagram order, JSON, local links, table widths, fences, Unicode/whitespace, plan/open-question coverage và `git diff --check`; cập nhật inventory sau #55. Không chạy application tests cho docs-only.
10. Giữ AC-23 macro-review #54–#57 pending đến sau khi #56 và #57 có DD; không kết luận group logic đã verified trong phiên #55.

### Blocking/open design decisions carried into DD

- Diagram rubric vs response `Submission` schema; related rubric persistence model is incompatible/unlinked.
- `files:UploadAsset[]` vs one nullable `file_url`.
- Mentor identity, ownership/assignment scope and unauthorized-resource 403/404 disclosure.
- Null/orphan FK handling and live-schema target.
- SubmissionStatus members, score type/range vs #56 `score:int32` and Assignment `max_score:decimal-string`.
- Null/omit policy, grade/feedback disclosure timing and invalid int64 path mapping.
- Error envelope `data:null` guideline vs current `{}` helper; future middleware allowlist.

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| API #55 runtime | Current router/module/test scan has no API #55 wiring | `UNWIRED / NOT_FOUND` | DD is design-only |
| API #54 → #55 handoff | AC-23 says choose one submission from #54 list; #54 catalog response is singular `Submission` | `DISCREPANCY / SOURCE_REQUIRED` | Collection response is needed to supply the #55 path ID |
| Rubric | AC-23 diagram asks to read it; `Submission` contract has no rubric field; current DDL has no legacy assignment linkage | `DISCREPANCY / SOURCE_REQUIRED` | Do not expand response silently |
| UploadAsset mapping | Contract has array; legacy candidate has only one nullable `file_url` | `SOURCE_REQUIRED` | Full file projection cannot be finalized |
| Mentor access | AC precondition requires grade permission; identity/assignment source is absent; direct owner is only candidate | `DERIVED / SOURCE_REQUIRED` | Access predicate remains confirmation item |
| Legacy vs V1-PILOT | Legacy assignment schema is BIGINT; new rubric schema is UUID and assessment-linked | `DISCREPANCY / NOT_VERIFIED` | Do not join incompatible schema artifacts |
| FK nullability | Guide/ERD required; legacy DDL nullable | `DISCREPANCY` | Orphan handling unresolved |

## CHANGES

- Files changed: `apps/study-server/docs/dd/55_mentor_submissions_detail/` (8 sheets + `PLAN_RESULT.md`, `OPEN_QUESTIONS.md`, `VERIFICATION_REPORT.md`); `.agents/worklog/2026-10-24/create-study-api55-dd.md`; `.agents/worklog/2026-10-24/inventory-study-api-dd-counts.md`.
- CONTEXT_UPDATES: None; no runtime/schema/catalog/diagram convention is being changed.
- Context pages changed: None.
- Assumptions: Direct-owner check and 403/404 separation are labeled DERIVED candidates; do not treat as approved policy.

## VERIFICATION

| Command/check | Result | Status |
|---|---|---|
| Worklog selector/review | Selected #48, #49, #50; all read; no shortage. | `VERIFIED` |
| Context and skill registry | Study server workflow and registered `createDD-markdown` skill read; registry wires resource to `server-study`; no ZIP for Study. | `VERIFIED_STATIC_ONLY` |
| Diagram coverage | Parsed all AC-23 nodes/edges and recorded four API sequence and #55 details/files/rubric node. | `VERIFIED_STATIC_ONLY` |
| Source/archive/template inventory | No API #55 folder or route/module/test; no archive or workbook in scoped docs/template source; all eight templates opened and fingerprinted. | `VERIFIED_STATIC_ONLY` |
| DD authoring | Wrote 11 Markdown files from the registered templates after recording this plan; no ZIP created. | `VERIFIED_STATIC_ONLY` |
| Custom static DD verifier | Exact 11-file manifest; 8 front matters/statuses; template appendices byte-identical; exact contract/error set; Submission/UploadAsset field coverage; valid JSON; resolved relative links; consistent table widths; closed fences; no trailing whitespace. | `VERIFIED` |
| `git diff --check` | No diagnostics. | `VERIFIED` |
| Inventory refresh | 103 catalog IDs; 55 DD folders with 8 logical core sheets; 43 full core-plus-report packs; missing DD IDs #56–#103 (48). | `VERIFIED_STATIC_ONLY` |
| Source implementation scan | Study router currently registers catalog IDs #01–#09 and #12–#14; no API #55 route/module/test. Runtime count remains 12/103 source-wired, not runtime proof. | `VERIFIED_STATIC_ONLY` |
| Runtime tests/live DB | Not run / not verified; docs-only and API unwired. | `NOT_RUN / NOT_VERIFIED` |

## HANDOFF

- Remaining blockers: Rubric contract/persistence, UploadAsset lookup, Mentor identity/assignment policy, FK nullability/live schema, score/status/disclosure semantics, malformed path and envelope discrepancies remain open.
- Next owner/action: Continue with API #56. Complete the AC-23 macro-review for #54–#57 after API #57 has a DD.

## GROUP_MACRO_REVIEW

- Trạng thái: VERIFIED_WITH_OPEN_QUESTIONS sau khi tạo DD API #57.
- Flow chung: #54 list → #55 detail/files/rubric → #56 score/status GRADED → #57 feedback → success; mỗi API giữ đúng phần read/write của mình.
- API #54 vẫn có mismatch giữa mục đích danh sách và response Submission đơn; 409 chưa có nhánh trong AC-23. Giữ contract catalog hiện tại tới khi owner quyết định.
- API #55 có gap rubric trong response; #56 nhận rubric items nhưng chưa có key, schema hoặc persistence legacy được xác nhận.
- API #56 giữ mutation score/status; #57 tách riêng feedback.
- Submission.files vẫn thiếu UploadAsset resolver. attachments của #57 không phải files học viên nộp, không dùng lại file_url; chưa có bảng hoặc field response được suy diễn.
- Mentor JWT identity, assigned-course, direct-owner candidate và quan hệ nullable/orphan còn mở.
- Error data null/object và middleware dynamic path mapping là gap wiring tương lai.
- Không chạy runtime tests hay AC-23 end-to-end; đây chỉ là macro-review tài liệu.

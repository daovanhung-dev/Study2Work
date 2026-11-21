---
task_id: "2026-10-12-create-study-api34-dd"
date: "2026-10-12"
primary_task_type: "docs"
secondary_task_types: []
project_scopes: ["server-study"]
cross_scope_dependencies: []
status: "VERIFIED"
---

# Worklog: Tạo Study API #34 DD draft

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `node scripts/select-worklogs.mjs --type docs --limit 3`
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-10-12/commit-push-study-dds.md`
    - carry_forward: Giữ nguyên các artifact đang có; task này chỉ tạo tài liệu và không commit/push.
  - path: `.agents/worklog/2026-10-12/create-study-api27-dd.md`
    - carry_forward: Draft — Needs Confirmation, có OPEN_QUESTIONS, không tạo ZIP, tách design contract khỏi runtime hiện tại.
  - path: `.agents/worklog/2026-10-12/create-study-api28-dd.md`
    - carry_forward: Bảo toàn contract và error set; không tự chốt các gap chưa có nguồn.
- shortage: `none`
- Additional recent precedent reviewed: `create-study-api29-dd.md` đến `create-study-api33-dd.md` và `review-study-api27-32-dds.md`; tiếp tục ghi rõ nguồn, giữ draft và không sửa các artifact trước.

## EXPECTED_BEHAVIOR

- Requirement: Tạo DD Markdown draft cho `POST /api/v1/uploads` theo 8 sheet canonical, kèm `PLAN_RESULT.md`, `OPEN_QUESTIONS.md`, `VERIFICATION_REPORT.md` và worklog. Không triển khai endpoint, không sửa catalog/diagram/schema/runtime và không tạo ZIP.
- Canonical contract/approved DD: API #34 trong `docs/lists/list_api.md`: Bearer JWT, role Student/Mentor; multipart gồm `file:binary!`, `purpose:UploadPurpose!`, `course_id?:int64`; HTTP 201 `DESIGN_RESOURCE_CREATED`, response `ApiEnvelope<UploadAsset>`; lỗi 401/403/422/503/500 với các mã DESIGN trong catalog.

## CURRENT_BEHAVIOR

- Source/config: Catalog và AC-17/AC-21 có contract/luồng thiết kế cho upload. Diagram mô tả Object Storage nhận file submission/media. ERD V1 và DB table notes không có bảng Uploads; footer ERD nói “Uploads lưu URL”, tạo gap chưa có mapping vật lý. Checked-in DDL không có bảng Uploads và không xác nhận live schema.
- Runnable tests: Không chạy runtime tests theo phạm vi DD-only; live DB và Object Storage không được truy vấn.
- Runtime wiring: API #34 là `UNWIRED / NOT_FOUND` trong route/module/test inventory hiện tại. API #13 là flow avatar riêng, không phải implementation contract cho API #34.

## SOURCE_TRACE

```text
Student/Mentor Bearer -> POST /api/v1/uploads multipart (approved catalog contract)
-> Object Storage write (AC-17 submission file / AC-21 lecture media)
-> ApiEnvelope<UploadAsset> HTTP 201
Current Study route/module/test: UNWIRED / NOT_FOUND
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| API #34 runtime | Current route/module/test inventory has no upload endpoint implementation. | `UNWIRED / NOT_FOUND` | DD remains design-only. |
| Purpose/status enums | Catalog names `UploadPurpose` and `UploadStatus` without enum values. | `SOURCE_REQUIRED` | Keep values and lifecycle open; do not invent allowed values. |
| File constraints and access | Catalog/ACs do not define MIME/size/signature rules, purpose-role pairs or course ownership predicates. | `SOURCE_REQUIRED` | Document questions; preserve the declared roles and 422/403 families. |
| Asset identity, URL and persistence | Catalog requires UploadAsset fields; ERD footer mentions URL storage but there is no Uploads table in ERD V1/table notes/checked-in DDL. | `DISCREPANCY / SOURCE_REQUIRED` | Do not invent an ID generator, URL policy or physical table mapping. |
| Storage failure and cleanup | Catalog allows 503 and 500; ACs do not specify provider classification, retry or orphan cleanup. | `SOURCE_REQUIRED` | Preserve both catalog branches and record cleanup/failure questions. |
| API #13 transfer | API #13 is Student avatar upload with JSON Data URL, 5 MiB limit, fixed key and 500 storage mapping. | `REFERENCE_ONLY` | Those endpoint-specific choices are excluded from API #34. |

## CHANGES

- Files changed: Added eight template sheets, `PLAN_RESULT.md`, `OPEN_QUESTIONS.md` and `VERIFICATION_REPORT.md` under `apps/study-server/docs/dd/34_uploads/`; added this worklog. Existing API #27–#33 folders and worklogs remain present and were not edited.
- CONTEXT_UPDATES: None.
- Context pages changed: None.
- Assumptions: Continue the API #27–#33 draft convention; keep unresolved decisions open; `07_table.md` records no confirmed DB mapping; no ZIP or runtime changes.

## VERIFICATION

| Command/check | Result | Status |
|---|---|---|
| `node scripts/select-worklogs.mjs --type docs --limit 3` | Selected and read `commit-push-study-dds.md`, `create-study-api27-dd.md` and `create-study-api28-dd.md`; no shortage. | `VERIFIED` |
| Source and contract review | Reviewed API #34 catalog row, API envelope/guidelines, AC/API index, AC-17/AC-21 diagrams, DB notes/ERD/DDL, API #13 reference, current route/auth/module/test inventory and canonical template. | `VERIFIED` |
| Inline Python DD validation | 11-file inventory, 8-sheet order/front matter and canonical appendices; JSON examples, links/anchors, Markdown table widths, catalog fields/error set, placeholder explanations, whitespace/conflict markers and SHA-256 fingerprints checked. | `VERIFIED` |
| `git diff --check` and untracked-file scan | Tracked diff and new DD/worklog whitespace checks are clean. | `VERIFIED` |
| Runtime tests / live DB / Object Storage | Not run or queried; API #34 is not wired and scope is documentation-only. | `NOT_RUN` |
| Context validator | Not required; no context page or manifest changed. | `NOT_REQUIRED` |

## HANDOFF

- Remaining blockers: Product/API/Architecture decisions in `OPEN_QUESTIONS.md` are needed before the DD can become Final or implementation begins; they do not block this draft.
- Next owner/action: Confirm purpose/status enums, file validation, role/course authorization, UploadAsset ID/URL and metadata persistence, provider error mapping and cleanup policy.

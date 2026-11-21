---
task_id: "2026-10-24-create-study-api48-dd"
date: "2026-10-24"
primary_task_type: "docs"
secondary_task_types: []
project_scopes: ["server-study"]
cross_scope_dependencies: []
status: "VERIFIED"
---

# Worklog: Tạo DD Study API #48

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `deno run --allow-read --allow-env scripts/select-worklogs.mjs --type docs --limit 3`
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-10-23/create-study-api41-dd.md`
    - carry_forward: Preserve catalog contract; label inferred behavior `DERIVED`; do not invent counters, columns or table relationships.
  - path: `.agents/worklog/2026-10-23/create-study-api42-dd.md`
    - carry_forward: AC-19 #39–#42 DDs were reconciled; read-only APIs use explicit N/A mutation mapping and keep response/source gaps open.
  - path: `.agents/worklog/2026-10-23/create-study-api43-dd.md`
    - carry_forward: Use requirement, request, query, mutation and response-source matrices before authoring; retain `UNWIRED`, `NOT_FOUND` and `SOURCE_REQUIRED` boundaries.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Tạo một DD tiếng Việt cho API #48, lập plan trước khi tạo DD, đọc AC-21 và DD liên quan, kiểm tra ngay sau authoring, sau đó macro-review nhóm #46–#48.
- Canonical contract/approved DD: `docs/lists/list_api.md` API #48; AC-21 index/activity diagram; reusable `Lecture`/`UploadAsset` schemas; DB guide/ERD và hai DDL hiện có; DD #46/#47/#34/#9/#26; `createDD-markdown` đã được registry wire cho `server-study`; Study workflow chỉ giao Markdown, không tạo ZIP.

## CURRENT_BEHAVIOR

- Source/config: API #48 là `GET /api/v1/mentor/lectures/{lecture_id}`, Mentor Bearer JWT, `lecture_id:int64!`, response `ApiEnvelope<Lecture>`, HTTP 200 `DESIGN_RESOURCE_RETRIEVED`, errors đúng 401/403/404/500. AC-21 nối #46 → #34/Object Storage → #47 → #48. Không có route, module hoặc test source API #48 trong Study hiện tại. Legacy `lessons` là candidate BIGINT; `resources` không đủ metadata UploadAsset. V1-PILOT là schema UUID/versioned khác; live schema chưa xác minh.
- Runnable tests: Không chạy; docs-only.
- Runtime wiring: `UNWIRED / NOT_FOUND` cho API #48. Current helper Student-only; Mentor auth/principal mapping chưa có.

## SOURCE_TRACE

```text
Mentor Bearer principal -> GET lecture theo path ID -> kiểm tra course ownership/assignment nhất quán với #46/#47 -> candidate read legacy lessons + courses -> map Lecture -> trả envelope/contract error -> UI hiển thị lecture mới
```

## PLAN BEFORE DD AUTHORING

1. Giữ nguyên method/path, Mentor Bearer auth, path `lecture_id:int64!`, không body/query, response, HTTP 200 và đúng bộ lỗi 401/403/404/500; không thêm 422/business code.
2. Đọc AC-21 flow và phân biệt AC-22 Content. API #48 là bước reload sau #47; không biến thành Content endpoint hoặc query public curriculum.
3. Candidate Q1 đọc `lessons` theo `l.id = :lecture_id`, lấy `l.course_id`, `l.name`, `l.content`, `l.sort_order`, `l.status`, và LEFT JOIN `courses` để kiểm tra course/owner. Chỉ dùng legacy DDL như candidate; tách riêng pilot UUID schema và live-schema gap.
4. Dùng cùng candidate direct-owner predicate với #46/#47 (`courses.mentor_id = principal Mentor ID`), không thêm `PUBLISHED` filter để luồng #47 tạo DRAFT vẫn reload được. Ghi assignment và JWT identity mapping là `SOURCE_REQUIRED`; missing lecture → candidate 404, inaccessible existing course → candidate 403; orphan/null parent là integrity gap cần giữ trong open question.
5. Map `id`, `course_id`, `name → title`, raw `content`, `sort_order → order`, `status` từ candidate `lessons`; không trả `video_url`. Giữ null/omit của optional `content` và enum `LessonStatus` chưa xác nhận.
6. Không bịa `assets: []`, Asset ID, metadata hay resolver. API #34 chưa có persistence/lookup; `resources` thiếu `content_type`, `size_bytes`, `status`. Đánh dấu `Lecture.assets[]` và nested fields `SOURCE_REQUIRED`, đang chặn mapping thành công đầy đủ.
7. Tạo 8 sheet theo Markdown template và 3 reports trong `48_mentor_lectures_detail`; `07_table.md` là `N/A — READ-ONLY API`. Không tạo ZIP/runtime/schema/catalog/diagram.
8. Sau authoring, kiểm tra exact contract/error set, ma trận field/column/error, JSON, template appendix/front matter, liên kết, bảng, whitespace và scope. Macro-review #46–#48 về ownership/assignment, schema, draft visibility, content/assets và error envelope; cập nhật trạng thái pending trong #46/#47 thành kết quả review, giữ câu hỏi chưa được nguồn giải đáp.

### API Requirement Matrix

| API ID | Contract item | Giá trị | Basis/status |
|---|---|---|---|
| #48 | Method/path | `GET /api/v1/mentor/lectures/{lecture_id}` | Catalog + AC-21; DIRECT |
| #48 | Actor/auth | Mentor / Bearer JWT | Catalog + AC-21; DIRECT |
| #48 | Path | `lecture_id:int64!` | Catalog + AC-21; DIRECT |
| #48 | Body/query | Không khai báo | Catalog; DIRECT |
| #48 | Success | HTTP 200 `DESIGN_RESOURCE_RETRIEVED`; `ApiEnvelope<Lecture>` | Catalog + AC-21; DIRECT |
| #48 | Error | 401 `DESIGN_AUTHENTICATION_REQUIRED` | Catalog; DIRECT |
| #48 | Error | 403 `DESIGN_ACCESS_DENIED` | Catalog; DIRECT |
| #48 | Error | 404 `DESIGN_RESOURCE_NOT_FOUND` | Catalog; DIRECT |
| #48 | Error | 500 `DESIGN_INTERNAL_ERROR` | Catalog; DIRECT |

### Request Usage Matrix

| Request item | Source/use | Query/response use | Rule/status |
|---|---|---|---|
| Authorization | Header; authenticate Bearer and Mentor role | Principal scopes course ownership check | Role DIRECT; Mentor guard and numeric/UUID identity binding unresolved |
| `lecture_id` | Path, required int64 | Q1 `lessons.id`; maps to `data.id` | Type DIRECT; malformed/overflow mapping unresolved; catalog has no 422 |
| Request body | None | None | DIRECT from catalog |
| Query parameters | None | None | DIRECT from catalog |

### Query Matrix

| Query | Type | Candidate source | Item | Predicate/rule | Evidence |
|---|---|---|---|---|---|
| Q1 | SELECT | legacy `lessons AS l` | `l.id` | `l.id = :lecture_id` | Legacy candidate; live schema unknown |
| Q1 | SELECT | legacy `lessons AS l` | `l.course_id` | Same lecture row | Nullable in legacy DDL; contract requires int64 |
| Q1 | SELECT | legacy `lessons AS l` | `l.name` | Same lecture row | Candidate mapping to title |
| Q1 | SELECT | legacy `lessons AS l` | `l.content` | Same lecture row; preserve stored text | Candidate; nullable |
| Q1 | SELECT | legacy `lessons AS l` | `l.sort_order` | Same lecture row | Candidate mapping to order |
| Q1 | SELECT | legacy `lessons AS l` | `l.status` | Same lecture row; do not filter by status | Enum members unresolved |
| Q1 | LEFT JOIN | legacy `courses AS c` | `c.id` | `c.id = l.course_id` | Candidate parent existence check |
| Q1 | SELECT | legacy `courses AS c` | `c.mentor_id` | Read owner for candidate access comparison | Candidate direct-owner source; assignment relation absent |
| Q1 | WHERE | legacy `lessons AS l` | `l.id = :lecture_id` | No row → candidate 404 | DERIVED branch using declared code |
| Q1 | CHECK | legacy `courses AS c` | `c.mentor_id = :mentor_id` | Existing course owner mismatch → candidate 403 | DERIVED; assignment support unresolved |
| Q1 | FILTER | N/A | No `PUBLISHED` predicate | Return Mentor-managed DRAFT candidate created in step #47 | DERIVED from AC-21 read-after-create flow |
| Q2 | N/A | N/A | UploadAsset lookup | No query specified until approved resolver/persistence exists | `SOURCE_REQUIRED`; no guessed query |

### Mutation Matrix

| Operation | Target | Condition | Fields | Status |
|---|---|---|---|---|
| None | N/A | API is read-only | No INSERT/UPDATE/DELETE | `N/A — READ-ONLY API` |

### Response Source Matrix

| Response field | Contract type | Candidate source | Mapping/null rule | Evidence status |
|---|---|---|---|---|
| `success` | boolean | Envelope branch | true on success, false on error | DIRECT convention |
| `businessCode` | string | Catalog | Exact branch code | DIRECT |
| `message` | string | Application message | Safe localized message; exact text unspecified | DERIVED |
| `data.id` | int64 | `lessons.id` | Direct candidate | Legacy candidate |
| `data.course_id` | int64 | `lessons.course_id` | Required; NULL is integrity gap | Legacy nullable discrepancy |
| `data.title` | string | `lessons.name` | Alias `name → title` | Candidate mapping |
| `data.content` | string? | `lessons.content` | Preserve stored text; null-versus-omit unresolved | Candidate; nullable |
| `data.assets[]` | `UploadAsset[]` | No approved source | Must not fabricate an empty array or asset records | `SOURCE_REQUIRED`; blocks full success projection |
| `data.assets[].id` | int64 | No approved source | No source/generator/lookup | `SOURCE_REQUIRED` |
| `data.assets[].name` | string | No approved source | No persistent metadata lookup | `SOURCE_REQUIRED` |
| `data.assets[].url` | uri | No approved source | Do not trust client URL | `SOURCE_REQUIRED` |
| `data.assets[].content_type` | string | No approved source | No metadata source | `SOURCE_REQUIRED` |
| `data.assets[].size_bytes` | int64 | No approved source | No metadata source | `SOURCE_REQUIRED` |
| `data.assets[].status` | UploadStatus | No approved source | Enum/lifecycle unresolved | `SOURCE_REQUIRED` |
| `data.order` | int32 | `lessons.sort_order` | Alias `sort_order → order` | Candidate mapping |
| `data.status` | LessonStatus | `lessons.status` | Return stored value; do not filter `PUBLISHED` | Enum members unresolved |
| `meta` | object | Envelope convention | `{}` candidate; error `data:null` guideline conflicts with current helper `{}` | DISCREPANCY |
| `traceId` | uuid | Request trace | Propagate current request trace | DIRECT convention |

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| API #48 runtime | No route/module/test source | `UNWIRED / NOT_FOUND` | DD remains design-only |
| Ownership | AC-21 allows owned/assigned courses; #46/#47 candidate is `courses.mentor_id`; Mentor identity binding unresolved | `DERIVED / SOURCE_REQUIRED` | Reuse one candidate rule; assigned-course support needs source |
| Schema | Legacy BIGINT lessons/resources vs pilot UUID/versioned lessons/file_objects; live schema unknown | `DISCREPANCY / NOT_VERIFIED` | Keep schemas separate |
| Assets | #47 requires refs and `Lecture.assets[]`; #34 persistence/lookup absent; legacy resources lacks required metadata | `SOURCE_REQUIRED` | Successful complete response cannot be mapped from current evidence |
| DRAFT visibility | #47 candidate default DRAFT; #9 public curriculum filters PUBLISHED; AC-21 reloads in Mentor flow | `DERIVED` | #48 must not apply public PUBLISHED filter; status enum still unresolved |
| Error envelope | API guideline expects `data:null`; current helper defaults to `{}` | `DISCREPANCY` | Keep expected/current forms explicit |

## CHANGES

- Files changed: `apps/study-server/docs/dd/48_mentor_lecture_detail/` (8 sheets + 3 reports); connected macro-review updates in DD #46/#47 and their worklogs; this worklog.
- CONTEXT_UPDATES: None planned; no source/schema/catalog/diagram changes.
- Context pages changed: None planned.
- Assumptions: Use only simple labeled `DERIVED` proposals; do not invent an asset table, ID, field, enum or error code.

## VERIFICATION

| Command/check | Result | Status |
|---|---|---|
| Worklog selector/review | Deno selector returned three `docs` worklogs; #41–#43 read in full. | `VERIFIED` |
| AC-21 diagram | Parsed all nodes/edges; confirms #46 → #34/Object Storage → #47 → #48 and Mentor owns/assigned precondition. | `VERIFIED` |
| Catalog/source/schema/prior DD | Read #48 row, Lecture/UploadAsset schema, current router/source search, legacy and pilot DDL, #46/#47/#34/#9/#26 evidence. | `VERIFIED_STATIC_ONLY` |
| Template and authoring | Eight registered Markdown templates used; all appendix suffixes match byte-for-byte; 11/11 expected files exist. | `VERIFIED` |
| Catalog and response validation | Exact GET/auth/path/response/success/error set checked; all Lecture fields and nested UploadAsset fields are listed. | `VERIFIED` |
| Static Markdown validation | Lượt đầu phát hiện trailing spaces ở metadata OPEN_QUESTIONS; đã xóa và chạy lại. JSON, local links, table widths, fences, whitespace và status markers đều pass. | `VERIFIED` |
| AC-21 macro review | Compared #46–#48 ownership/assignment, DRAFT visibility, schema split, Lecture fields, assets and envelope discrepancy; updated connected DD reports and worklogs. | `VERIFIED_WITH_OPEN_QUESTIONS` |
| Source implementation scan | No API #48 route/module/test source; `UNWIRED / NOT_FOUND`. | `VERIFIED_STATIC_ONLY` |
| Runtime tests | Not run; docs-only and API #48 is unwired. | `NOT_RUN` |
| Context validator | Not run; no `.agents/server-study` context page or registry was changed. | `NOT_APPLICABLE` |

## HANDOFF

- Remaining blockers: Asset response resolver/persistence, Mentor assignment and identity mapping, live schema, LessonStatus members, null content serialization and malformed path behavior.
- Next owner/action: Continue the one-API-per-session sequence with API #49; retain the asset resolver, assignment/identity, schema, status and null-serialization questions as blockers for future implementation approval.

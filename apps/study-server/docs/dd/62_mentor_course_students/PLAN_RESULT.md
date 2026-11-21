# PLAN_RESULT — Study API #62

## Kết quả quyết định

- API: #62 — `GET /api/v1/mentor/courses/{course_id}/students`.
- Status DD: `Draft — Needs Confirmation`.
- Scope: server-study; chỉ wire API #62, không thay đổi behavior #63/#64.
- Success payload: `ApiEnvelope<UserSummary[]>`, no pagination. Đây là fallback `DERIVED` để phục vụ AC-25 recipient picker; catalog ban đầu dùng `Page<Course>` nhưng endpoint/flow là roster và không có pagination input.
- Schema candidate: checked-in legacy BIGINT `courses`, `enrollments`, `users`; live database chưa được kiểm tra. V1-PILOT UUID model không được dùng.
- Eligibility: `enrollments.status='ACTIVE'` và `users.role='STUDENT'`; `DISTINCT` recipient, order theo `users.id ASC`.
- Access: current Mentor JWT guard + direct owner `courses.mentor_id`; thiếu course→404, owner khác→403, empty roster→200 `[]`.
- #63 `recipients:string!` encoding còn mở; #62 trả numeric UserSummary IDs, không chọn format serialize.

## Source inventory and precedence

| Ưu tiên | Source | Evidence | Quyết định/status |
|---:|---|---|---|
| 1 | AC-25 diagram | Mentor chọn course; #62 đọc active enrollments; UI chọn recipient; #63 tạo/gửi; #64 đọc trạng thái. Cùng node #62 ghi `Page<Course>`. | Internal diagram discrepancy: flow là roster nhưng payload khai báo Course page. |
| 2 | Legacy `infra/postgres/study-server/DB.sql` và current Study APIs | BIGSERIAL/BIGINT `courses`, `enrollments`, `users`; API #34 dùng `status='ACTIVE'`; #46/#49/#54 dùng numeric Mentor principal và `courses.mentor_id`. | Chọn làm local implementation candidate; DDL nullable `user_id/course_id`; live use unverified. |
| 2 | `infra/postgres/02_study_db.sql` | UUID `course_enrollments` nối `course_versions/courses` và `learner_profiles`; status `ENROLLED/IN_PROGRESS/COMPLETED`. | V1-PILOT khác schema family; không trộn vào API legacy. |
| 3 | `docs/lists/list_api.md` #62 | `Page<Course>` và error set 401/403/404/500; request chỉ có `course_id:int64!`. | Đồng bộ output sang `UserSummary[]`; giữ method/path/errors và không thêm pagination input. |
| 4 | API #49 worklog/module/DD | Endpoint list-purpose từng khai báo object singular và không có page/size; implementation đồng bộ catalog/diagram sang array phẳng. | Precedent cho collection fallback; không thay thế evidence AC-25/schema. |
| Runtime baseline | `app/api/v1.py`, middleware, mentor modules/tests | API #62 route/module/test và design-path entry vắng mặt; last connected route #61. Shared Mentor guard đã dùng bởi #46/#49/#54. | `UNWIRED / NOT_FOUND` before implementation. |

## API Requirement Matrix

| API ID | Method/path | Auth | Request | Success | Errors |
|---|---|---|---|---|---|
| #62 | `GET /api/v1/mentor/courses/{course_id}/students` | Bearer JWT; `MENTOR` | `course_id:signed-int64`; không query/body | 200 `DESIGN_RESOURCE_RETRIEVED`, `ApiEnvelope<UserSummary[]>` | 401 authentication; 403 access denied; 404 not found; 500 internal error |

## Ma trận và flow

```text
Mentor chọn course → #62 kiểm tra direct owner → đọc ACTIVE enrollments của STUDENT
→ trả UserSummary[] cho UI chọn người nhận
→ #63 tạo/gửi Notification → #64 đọc delivery status
```

| Ma trận | Kết quả |
|---|---|
| Request Usage | Bearer guard trước DB; `course_id` signed-int64; malformed/out-of-range→404; không có query/body. |
| Query | Q1 `courses.id/mentor_id` để phân biệt 404/403; Q2 `DISTINCT users.id/full_name/avatar_url` qua `enrollments`, lọc `ACTIVE`, `STUDENT`, course và Mentor owner; sort `users.id ASC`. |
| Mutation | N/A — chỉ SELECT; không commit và không gọi notification service. |
| Response Source | `data[].id/full_name/avatar_url?` từ `users`; `data=[]` khi không có recipient; `meta={}`; không PageMeta. |

## Discrepancy và remaining confirmation

| Item | Evidence/decision | Status |
|---|---|---|
| `Page<Course>` vs roster | Không map learner thành Course; đổi đồng bộ catalog, AC-25 node, DD và source sang `UserSummary[]`. | `DERIVED — OWNER CONFIRMATION PENDING` |
| Pagination | Request không có page/size; không thêm query hoặc page metadata. | `DERIVED — OWNER CONFIRMATION PENDING` |
| Schema/status | Chọn legacy BIGINT và `ACTIVE`; V1-PILOT khác biệt; runtime/live DB không được probe. | `DERIVED — LIVE SCHEMA UNVERIFIED` |
| Course scope | Dùng direct `courses.mentor_id`; assigned Mentors chưa được hỗ trợ. | `DERIVED — POLICY CONFIRMATION PENDING` |
| Recipient encoding | #63 chỉ khai báo `recipients:string!`; #62 trả numeric IDs, không xác định serialization. | `OPEN — LINKED API CONTRACT` |
| Profile privacy | Chỉ trả user ID, full name, optional avatar; không filter `users.status`. | `OPEN — PRODUCT POLICY` |

## Fingerprint template

| Template | SHA-256 |
|---|---|
| `00_Cover.md` | `fd5f568c5329d3069fbaff617a6f4ed3b5ffaf050e042c95b7c9100a05f79e63` |
| `01_Lich_su.md` | `d1cec6573433a9551812bf47552f8a44d7c533d790341941047c410e1d57771e` |
| `02_Overview.md` | `c2879c2f0e007395558dfee4167484786c5aadb3fdd63ab135ca111e7c5f8aa6` |
| `03_Request.md` | `37aaa1e9d7f3e83329e81ab38d922c9dff959284d5b7b3ae353878798dd4b7aa` |
| `04_Response.md` | `5bcb43ba5eb487302dd5d5efde4383b9f452f9fed2149f55315d64ff78a19ab8` |
| `05_Data_Mapping.md` | `11bc77bc0522d3af27b9499114991c8819046ac32bde5c1efdc841be088dcc5b` |
| `06_Error.md` | `e0160ea07fdbc74f2cafebd6ed3b21e60029662d28d67f5f6a0b4d95ba72be9b` |
| `07_table.md` | `4c9a0e037872333210aaf44ba9fbf00a0e63343a69d55250e537d2c3c5e2d356` |

## Delivery boundary

- Preserve 8 sheet files and the existing Excel source appendices; Study DD stays Markdown-only with no ZIP.
- No DB schema/migration is required for the chosen legacy tables.
- Local tests/source do not prove that `DB.sql` matches the deployed database or that API #62 is deployed.

---
title: "Data Mapping"
order: 5
dd_id: "85"
api_name: "Đổi trạng thái lesson"
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "3. Data mapping"
format: markdown
status: "Draft — Needs Confirmation"
---

# Data Mapping

## Flow xử lý data

### Mục lục

- [0. Check quyền](#step-0-check-quyen)
- [1. Nhận request](#step-1-nhan-request)
- [2. Check status proposal](#step-2-check-status-proposal)
- [3. Update và audit](#step-3-update-audit)
- [4. Check kết quả và map response](#step-4-check-ket-qua-va-map-response)
- [5. Trả response](#step-5-tra-response)
- [Requirement Matrix](#requirement-matrix)
- [Request Usage Matrix](#request-usage-matrix)
- [Query Matrix](#query-matrix)
- [Mutation Matrix](#mutation-matrix)
- [Response Source Matrix](#response-source-matrix)

<a id="step-0-check-quyen"></a>

## 0. Check quyền

- Bearer JWT xác thực qua shared `validate_current_user_request(... role="ADMIN")`.
- Thiếu/sai/hết hạn credential → 401 `DESIGN_AUTHENTICATION_REQUIRED`; thiếu ADMIN role → 403 `DESIGN_ACCESS_DENIED`.
- Guard trả numeric user ID từ JWT `sub`; view dùng ID này làm `actor_user_id` cho audit.
- AC-34 còn yêu cầu lesson-management permission riêng, nhưng current shared guard chỉ kiểm tra ADMIN role. Đây là discrepancy, không tuyên bố policy riêng đã thực thi.
- Auth chạy trước signed-int64 path parse và mọi query DB trong view. Typed body validation của FastAPI chạy trước handler/auth theo convention hiện tại.

<a id="step-1-nhan-request"></a>

## 1. Nhận request

- `lesson_id` nhận từ raw path và parse signed int64; malformed/out-of-range trả 422 `DESIGN_VALIDATION_ERROR` trước query.
- JSON body strict chỉ nhận `{status}`; không nhận query parameter hoặc metadata fields.
- `X-Trace-Id` được current middleware truyền hoặc sinh; body `status` chỉ định target theo DERIVED enum ở Step 2.

<a id="step-2-check-status-proposal"></a>

## 2. Check status proposal

- Cho phép đúng các giá trị `DRAFT`, `PUBLISHED`, `SUSPENDED`, tái dùng candidate status set của API #76 do catalog/diagram không liệt kê LessonStatus riêng.
- Body thiếu/thừa field, sai type hoặc status khác ba giá trị trên bị FastAPI/Pydantic từ chối với 422 `DESIGN_VALIDATION_ERROR`.
- Không áp transition matrix, readiness gate, moderation, enrollment/progress side effect hoặc idempotency key.
- Nếu target bằng status hiện tại, view trả Lesson hiện tại, không UPDATE và không ghi audit duplicate.

<a id="step-3-update-audit"></a>

## 3. Update và audit

### 3.1. M1 — Khóa và đọc Lesson

```sql
SELECT
    id, course_id, name AS title, content, video_url,
    sort_order AS "order", status
FROM lessons
WHERE id = :lesson_id
FOR UPDATE
```

- SQL target là legacy BIGINT `lessons` mapping dùng bởi APIs #82–#84; V1-PILOT UUID Lesson không được ghép vào flow này.
- Không có row → 404 `DESIGN_RESOURCE_NOT_FOUND`; không query lesson trước Admin authorization.
- `FOR UPDATE` giữ status cũ ổn định cho audit và nhánh same-status trong transaction.

### 3.2. M2 — Cập nhật status khi có thay đổi

```sql
UPDATE lessons
SET status = :status, updated_at = CURRENT_TIMESTAMP
WHERE id = :lesson_id
RETURNING
    id, course_id, name AS title, content, video_url,
    sort_order AS "order", status
```

- Chỉ thay `status` và `updated_at`; không sửa metadata, course relation, uploads/resources, dependencies hoặc progress.
- Returned row phải map được thành reusable API #09 `Lesson` và status phải bằng request target; nếu không, rollback rồi trả 500 `DESIGN_INTERNAL_ERROR`.
- UPDATE không trả row → 404 `DESIGN_RESOURCE_NOT_FOUND`.

### 3.3. M3 — Append audit trong cùng transaction

```sql
INSERT INTO lesson_status_audit_logs (
    lesson_id, actor_user_id, previous_status, new_status
)
VALUES (
    :lesson_id, :actor_user_id, :previous_status, :new_status
)
```

- Relation/columns được khai báo ở migration 012 theo fallback DERIVED legacy BIGINT, dựa trên patterns #76/#80.
- Chỉ ghi khi status thực sự đổi; actor là numeric subject đã qua shared ADMIN guard.
- View sở hữu transaction: status update, audit insert, response mapping rồi commit; DB/audit/mapping/commit failure rollback toàn bộ và trả safe 500.
- Migration 012 là source artifact, chưa chứng minh đã chạy trên live schema. `audit_events` pilot không dùng vì UUID resource key và Lesson schema không tương thích.

### 3.4. Query Matrix

| Query | Type | Target | Conditions/effect | Result/status |
|---|---|---|---|---|
| M1 | SELECT FOR UPDATE | Legacy `lessons` candidate | `id = :lesson_id` | Current Lesson/status; no row → 404. |
| M2 | UPDATE RETURNING | Legacy `lessons` candidate | Set target status and `updated_at` when value changes | Updated Lesson projection. |
| M3 | INSERT | `lesson_status_audit_logs` migration 012 | Actor, lesson, old/new status on actual change | Same transaction; no-op skips insert. |

### 3.5. Mutation Matrix

| Mutation | Target | Fields/effect | Value source | Status |
|---|---|---|---|---|
| M2 UPDATE | `lessons` | status, updated_at | Validated body and DB clock | DERIVED legacy mapping. |
| M3 INSERT | `lesson_status_audit_logs` | lesson_id, actor_user_id, previous_status, new_status | Locked row and validated principal | DERIVED; atomic with M2. |
| No mutation | metadata, relation, resources, progress | Preserve | N/A | Outside API #85 scope. |

<a id="step-4-check-ket-qua-va-map-response"></a>

## 4. Check kết quả và map response

- Successful changed row or no-op locked row maps through API #09 `Lesson`: id, course_id, title, content, video_url, order, status.
- `course_id` must satisfy reusable Lesson required int64; legacy NULL is not replaced with a fabricated value and produces safe 500/rollback.
- Nullable content/video_url serialize as JSON null. Audit fields are not returned in Lesson.
- Missing lesson returns 404; DB, audit, mapping or commit failure returns 500 with rollback and no raw SQL/detail.
- #85 does not filter a soft-delete marker; #86 visibility policy remains a linked open question.

<a id="step-5-tra-response"></a>

## 5. Trả response

- Success: HTTP 200, `DESIGN_RESOURCE_UPDATED`, one `ApiEnvelope<Lesson>`.
- Error set stays exactly catalog 401/403/404/422/500 codes.
- Current `error_response` returns top-level `data: null`; focused API #85 HTTP tests cover error responses.
- Successful AC-34 flow returns to API #82 list reload. No list query is added here.

## Requirement Matrix

| Requirement | Source | Status |
|---|---|---|
| PATCH path, Bearer JWT/Admin, int64 path | Catalog #85 | DIRECT |
| Lesson envelope, 200 update code, exact error set | Catalog #85 | DIRECT |
| lesson-management permission and status+audit intent | AC-34 | DIRECT intent; fine-grained permission not implemented |
| Body `{status}` and values DRAFT/PUBLISHED/SUSPENDED | Catalog/diagram omit body; API #76 precedent | DERIVED |
| Row lock, no-op, updated_at and atomic audit | Existing #76/#80 patterns and legacy schema | DERIVED |
| Migration 012 deployment/live schema | Not verified by source tests | SOURCE_REQUIRED |

## Request Usage Matrix

| Request item | Source/use | Query/response use | Rule/status |
|---|---|---|---|
| Authorization | Bearer JWT | Shared ADMIN guard and audit actor | ADMIN is current; fine-grained permission absent |
| lesson_id | Required path int64 | M1 predicate and response identity | DIRECT type; legacy key candidate |
| Body status | Strict JSON | M2 target and response status | DERIVED three-value enum; invalid input 422 |
| Query parameters | None | None | Direct absence |
| X-Trace-Id | Current middleware | Envelope trace | Current-source convention; not stored in audit row |

## Query Matrix

| Step | Type | Source/target | Purpose/status |
|---|---|---|---|
| M1 | SELECT FOR UPDATE | Legacy `lessons` | Read status and serialize changes per row |
| M2 | UPDATE RETURNING | Legacy `lessons` | Change status and updated_at only |
| M3 | INSERT | `lesson_status_audit_logs` | Append actor and old/new values atomically |
| No-op | No mutation | Locked `lessons` row | Return current Lesson and commit to release lock |

## Mutation Matrix

| Step | Target | Effect | Atomicity |
|---|---|---|---|
| M2 | `lessons` | Change status and updated_at | Same Session transaction |
| M3 | `lesson_status_audit_logs` | Record the accepted status change | Same Session transaction; skipped for no-op |

## Response Source Matrix

| Response field | Source | Transform/null rule | Status |
|---|---|---|---|
| success/businessCode | Envelope/catalog | true and `DESIGN_RESOURCE_UPDATED` | DIRECT |
| data | Lesson row | One reusable API #09 Lesson | DIRECT response shape; legacy mapping candidate |
| data.title/order | name/sort_order | Aliased by SQL | Legacy mapping used by #82–#84 |
| data.status | Returned row | Copy exact new/current value | DIRECT field; enum is DERIVED |
| meta | Envelope helper | Empty object on success | Current helper |
| traceId | Middleware | Propagate or generate UUID | Current-source convention |
---

## Phụ lục đối chiếu nguồn Excel
- Workbook nguồn: `DD_API_Template(1).xlsx`
- Sheet nguồn: `3. Data mapping`
- Dimension: `B1:BB61`
- Trạng thái: `visible`
- Số ô có dữ liệu/công thức: `63`
- Số vùng merge: `0`

<details>
<summary>Bản ghi từng ô có dữ liệu hoặc công thức</summary>

| Hàng | Ô | Giá trị nguồn | Công thức nguồn |
|---:|---|---|---|
| 2 | `B2` | Flow xử lý data |  |
| 4 | `D4` | 0. |  |
| 4 | `E4` | Check quyền |  |
| 5 | `E5` | ・ |  |
| 5 | `F5` | Thực hiện check quyền |  |
| 6 | `E6` | ・ |  |
| 6 | `F6` | Get count khi get data từ … |  |
| 7 | `G7` | Table get |  |
| 7 | `K7` | : |  |
| 8 | `G8` | Conditions |  |
| 8 | `K8` | : |  |
| 10 | `E10` | ・ |  |
| 10 | `F10` | Trường hợp giá trị get được lớn hơn 0, thực hiện các xử lý tiếp theo |  |
| 11 | `E11` | ・ |  |
| 11 | `F11` | Trường hợp giá trị get được bằng 0, trả về status 2 |  |
| 13 | `D13` | 1. |  |
| 13 | `E13` | validate data input |  |
| 14 | `F14` | refer sheet [４．Error] |  |
| 16 | `D16` | 2. |  |
| 16 | `E16` | Get thông tin… |  |
| 18 | `F18` | Table get |  |
| 18 | `K18` | Column get |  |
| 18 | `P18` | Chú thích |  |
| 18 | `U18` | Remarks |  |
| 29 | `F29` | Target table / join condition |  |
| 30 | `F30` | Target table |  |
| 30 | `N30` | Join condition |  |
| 30 | `AL30` | 結合種類 |  |
| 31 | `F31` | txn_ams_t0320 AS a |  |
| 32 | `F32` | txn_amm_v0002 AS b |  |
| 32 | `N32` | ON a . chy_typ = b . kbn_typ AND b . dmin_cd = A AND b . kbnknr_cd = 001 |  |
| 32 | `AL32` | LEFT JOIN |  |
| 33 | `F33` | txn_amm_v0002 AS c |  |
| 33 | `N33` | ON a . chy_typ = c . kbn_typ AND c . dmin_cd = A AND c . kbnknr_cd = Z02 |  |
| 33 | `AL33` | LEFT JOIN |  |
| 35 | `F35` | ・ |  |
| 35 | `G35` | Điều kiện get data |  |
| 37 | `F37` | ・ |  |
| 37 | `G37` | Điều kiện sort |  |
| 41 | `D41` | 3. |  |
| 41 | `E41` | Insert/Update thông tin … |  |
| 42 | `E42` | Update table…. |  |
| 43 | `E43` | ・ |  |
| 43 | `F43` | Items update |  |
| 44 | `F44` | ・ |  |
| 44 | `G44` | Refer sheet [xxxx] |  |
| 45 | `E45` | ・ |  |
| 45 | `F45` | Điều kiện get data |  |
| 46 | `F46` | ・ |  |
| 46 | `G46` | auth_user. id = user hiện tại theo token |  |
| 48 | `D48` | 4. |  |
| 48 | `E48` | check kết quả execute query  |  |
| 49 | `E49` | 1. Thành công |  |
| 50 | `F50` | HTTPStatus = 200 |  |
| 51 | `F51` | Trả về kết quả status = 1 |  |
| 52 | `E52` | 2. Lỗi hệ thống phát sinh |  |
| 53 | `F53` | HTTPStatus = 500 |  |
| 54 | `F54` | Trả về kết quả status = 2 |  |
| 55 | `E55` | 3. Validate lỗi |  |
| 56 | `F56` | HTTPStatus = 400 |  |
| 57 | `F57` | Trả về kết quả status = 2 |  |
| 58 | `E58` | 4. Ngoài trường hợp trên |  |
| 59 | `F59` | Trả về kết quả status = 2 |  |

</details>

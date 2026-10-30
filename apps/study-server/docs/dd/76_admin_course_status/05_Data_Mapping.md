---
title: "Data Mapping"
order: 5
dd_id: "76"
api_name: "Thay đổi trạng thái khóa học Admin"
source_sheet: "3. Data mapping"
status: "Draft — Needs Confirmation"
---

# Data Mapping

## Flow xử lý data

~~~text
Admin Bearer principal
-> validate Bearer JWT + shared ADMIN role; finer permission còn SOURCE_REQUIRED
-> validate course_id và candidate body.status
-> Q1 đọc/khóa course hiện hữu
-> M1 cập nhật status + updated_at
-> M2 insert `course_status_audit_logs` với actor/old/new nếu status đổi
-> Q2 đọc Course/UserSummary projection; same-status không UPDATE/audit
-> commit transaction
-> 200 Page<Course> singleton hoặc exact catalog errors
-> UI reload course management
~~~

# Mục lục

- [0. Check quyền](#step-0-check-quyen)
- [1. Validate data input](#step-1-validate-data-input)
- [2. Get thông tin](#step-2-get-thong-tin)
- [3. Update/audit](#step-3-update-audit)
- [4. Map response](#step-4-map-response)
- [5. Trả về response](#step-5-tra-ve-response)
- [Request Usage Matrix](#request-usage-matrix)
- [Query Matrix](#query-matrix)
- [Mutation Matrix](#mutation-matrix)
- [Response Source Matrix](#response-source-matrix)

<a id="step-0-check-quyen"></a>

## 0. Check quyền

### 0.1. Xác thực và authorization

- Runtime gọi `validate_current_user_request(..., role="ADMIN")`; đây là shared role fallback DERIVED, finer course-management permission chưa có policy source.
- Thiếu/sai token trả 401 DESIGN_AUTHENTICATION_REQUIRED.
- Principal không có ADMIN role trả 403 DESIGN_ACCESS_DENIED; finer permission enforcement chưa được implement vì SOURCE_REQUIRED.
- Shared helper kiểm tra Bearer/JWT và trả numeric user ID từ `sub`; actor mapping sang legacy users.id là DERIVED. Tenant/scope và finer permission vẫn SOURCE_REQUIRED.
- Không dùng shared Student guard trong app/utils/auth.py.

### 0.2. Thứ tự kiểm tra

- Với body hợp lệ, view xác thực trước path parsing và mọi query; FastAPI body/schema validation có thể trả 422 trước khi gọi view.
- Không dùng owner/mentor ID để thay thế Admin permission.

### 0.3. Query/check quyền

| Target table/API | Column/field | Condition/value | Remarks |
|---|---|---|---|
| Authorization header | Bearer credential | Token hợp lệ/chưa hết hạn, shared role ADMIN | DIRECT auth requirement + current shared guard. |
| JWT claims/policy | Admin role | Principal có role ADMIN | DIRECT role requirement; numeric sub comes from shared auth helper. |
| Admin policy | course-management permission | Permission được cấp | AC-32 precondition DIRECT; policy source SOURCE_REQUIRED. |

<a id="step-1-validate-data-input"></a>

## 1. Validate data input

### 1.1. course_id

- Nhận path int64! theo catalog.
- Minimum, positivity, malformed/overflow mapping chưa được nguồn xác định.
- Course ID trong legacy candidate là BIGSERIAL; V1-PILOT id là UUID, không chuyển đổi ngầm.

### 1.2. status — candidate body

- Catalog/diagram không khai báo body; {status} là DERIVED vì PATCH phải chỉ định trạng thái đích.
- Semantic target set theo catalog: draft, published, suspended.
- Runtime accepts `DRAFT`, `PUBLISHED`, `SUSPENDED`; this uppercase set is DERIVED from catalog labels + legacy/current convention, not an approved reusable enum.
- Chỉ validate target membership theo candidate set; không áp transition matrix hoặc content-readiness rule chưa có nguồn.
- Missing/unknown target and extra body fields map to 422 DESIGN_VALIDATION_ERROR through strict Pydantic request validation; field/body behavior is DERIVED.
- Same-status request is a DERIVED no-op: return current Course without timestamp update or duplicate audit append.
- Idempotency-Key chưa là direct header; API guideline retryable-mutation semantics cần quyết định.

### 1.3. Public visibility effect

- API #06 current source lọc courses.status = 'PUBLISHED'; scope context cũng mô tả API #08/#09 là published-only.
- Vì vậy candidate PUBLISHED có thể xuất hiện trong public flow; DRAFT/SUSPENDED không thỏa filter published.
- Enrollment access sau khi course chuyển SUSPENDED và readiness trước khi publish chưa được AC-32 định nghĩa.
- Không thêm query learner/enrollment/content; nhánh STATUS diagram không yêu cầu.

<a id="step-2-get-thong-tin"></a>

## 2. Get thông tin

### 2.1. Q1 — đọc và khóa course theo ID

SQL lấy từ API #76 source và legacy candidate DDL; live schema chưa xác minh.

~~~sql
SELECT status
FROM courses
WHERE id = :course_id
FOR UPDATE
~~~

- Nếu Q1 không có row: rollback và trả 404 DESIGN_RESOURCE_NOT_FOUND.
- FOR UPDATE giữ trạng thái không đổi trong khi update/audit cùng transaction.
- Không lọc PUBLISHED; Admin quản lý mọi trạng thái.

### 2.2. Q2 — response projection sau update

Q2 candidate theo legacy DDL và Course/UserSummary mapping của #74/#75.

~~~sql
SELECT
    c.id,
    c.name AS title,
    c.description,
    c.thumbnail_url,
    c.price,
    c.status,
    m.id AS mentor_id,
    m.full_name AS mentor_full_name,
    m.avatar_url AS mentor_avatar_url
FROM courses AS c
LEFT JOIN users AS m ON m.id = c.mentor_id
WHERE c.id = :course_id
~~~

- courses.name → Course.title.
- courses.status phải phản ánh target status đã được cập nhật trong transaction.
- LEFT JOIN users theo courses.mentor_id là candidate; Course.mentor required nhưng legacy mentor_id nullable.
- Không JOIN category: chưa có relation source-backed; omit optional Course.category.
- Không đọc hoặc trả email, phone, credential, course counters hoặc learner data.
- Không đọc count; Page singleton lấy từ một course hiện có.

<a id="step-3-update-audit"></a>

## 3. Update/audit

### 3.1. M1 — update trạng thái course

SQL hiện trong source, target schema là legacy DDL candidate; live schema chưa xác minh.

~~~sql
UPDATE courses
SET
    status = :status,
    updated_at = CURRENT_TIMESTAMP
WHERE id = :course_id
RETURNING id, status
~~~

- Chỉ đổi status và candidate updated_at; giữ metadata, mentor/owner và category ngoài mutation.
- Nếu M1 không trả row sau Q1, coi là cạnh tranh deletion/state drift; rollback và dùng 404 candidate.
- updated_at tồn tại trong legacy DDL; cập nhật bằng database timestamp là DERIVED.
- Không lọc theo old status vì diagram không nêu transition restriction.

### 3.2. M2 — audit event bắt buộc về mặt nghiệp vụ

- AC-32 diagram trực tiếp yêu cầu ghi audit log cùng status update.
- Legacy BIGINT IDs khớp API path và numeric JWT `sub`; V1-PILOT audit_events dùng UUID và không tương thích trực tiếp.
- Runtime fallback ghi relation `course_status_audit_logs` trong migration 010 và legacy `DB.sql`; physical mapping gồm course_id, actor_user_id, previous_status, new_status, changed_at là DERIVED.
- SQL: `INSERT INTO course_status_audit_logs(course_id, actor_user_id, previous_status, new_status) VALUES (:course_id, :actor_user_id, :previous_status, :new_status)`.
- Audit insert nằm cùng transaction với status update; lỗi insert rollback toàn bộ và trả 500 DESIGN_INTERNAL_ERROR.
- Relation/index/FK là candidate; live schema, retention and database-enforced append-only policy chưa xác minh.

### 3.3. Transaction candidate

~~~text
BEGIN
  Q1 SELECT ... FOR UPDATE
  M1 UPDATE courses.status + updated_at
  M2 INSERT course_status_audit_logs(actor, old status, new status)
  Q2 SELECT updated Course + UserSummary
COMMIT
~~~

Nếu Q1 không có course thì rollback/404. Nếu update, audit insert, projection, mapping hoặc commit lỗi thì rollback và trả 500. Same-status request bỏ qua M1/M2 nhưng đọc projection rồi commit transaction để giải phóng row lock. Study DB helpers không commit; view sở hữu transaction.

<a id="step-4-map-response"></a>

## 4. Map response

- Map Course fields theo reusable schema và Response Source Matrix.
- Bọc đúng một Course trong Page&lt;Course&gt; singleton {page:1,size:1,total:1,total_pages:1} theo #74/#75; đây là DERIVED.
- Map mentor thành UserSummary id/full_name/avatar_url; orphan/missing mentor xử lý 500 candidate, cần owner duyệt.
- Omit category do không có course-category relation source-backed.
- Serialize price decimal chính xác dạng string; legacy DDL cho phép NULL trong khi Course yêu cầu giá trị.
- Return status đã được Q1/M1/Q2 xác nhận; candidate enum/casing vẫn DERIVED.
- Không đưa audit event vào response vì catalog Course/Page không khai báo field đó.

<a id="step-5-tra-ve-response"></a>

## 5. Trả về response

- Thành công: HTTP 200 DESIGN_RESOURCE_UPDATED, envelope ApiEnvelope&lt;Page&lt;Course&gt;&gt;.
- Lỗi: giữ đúng 401/403/404/422/500 và business codes theo catalog.
- Error helper mặc định `data:null`. Middleware có template riêng `/api/v1/admin/courses/{course_id}/status`; HTTP tests xác nhận validation envelope local.
- Không thêm HTTP status hoặc business code ngoài tập API #76 khai báo.
- Sau thành công, UI reload course management theo AC-32.

## Request Usage Matrix

| Request item | Source/use | Query/response use | Rule/status |
|---|---|---|---|
| Authorization | Bearer JWT | Shared ADMIN guard and audit actor | DIRECT requirement; role guard source-backed; finer permission is SOURCE_REQUIRED; actor BIGINT mapping DERIVED |
| Idempotency-Key | Not direct in catalog | No runtime/query use until approved; may deduplicate retry/audit effects | API guideline scope and endpoint retry semantics SOURCE_REQUIRED |
| course_id | Path int64 required | Q1, M1 and Q2 predicates | DIRECT; physical legacy mapping candidate |
| Body status | Strict candidate enum | M1 target; returned in updated Course | DERIVED; runtime accepts DRAFT/PUBLISHED/SUSPENDED |
| Query | None | None | DIRECT |

## Query Matrix

| Step | Type | Source/target | Column/condition | Purpose/status |
|---|---|---|---|---|
| Q1 | SELECT FOR UPDATE | Legacy courses | status; id = :course_id | Read/lock target; source-backed SQL against legacy candidate, live schema unknown |
| M1 | UPDATE | Legacy courses | status=:status, updated_at=CURRENT_TIMESTAMP; id=:course_id | Set requested target; DERIVED candidate |
| M2 | INSERT | course_status_audit_logs | course_id, actor_user_id, previous_status, new_status | Append successful status change; physical mapping DERIVED, live schema unknown |
| Q2 | SELECT + LEFT JOIN | Legacy courses AS c, users AS m | c.id=:course_id; m.id=c.mentor_id | Updated response projection, candidate follows #74/#75 |
| None | COUNT / enrollment/content scan | N/A | N/A | Not in STATUS branch; do not add counter/policy query |

## Mutation Matrix

| Operation | Target | Condition | Fields/effect | Status |
|---|---|---|---|---|
| M1 UPDATE | Legacy courses candidate | id=:course_id | Set status; candidate set updated_at; preserve remaining course metadata | DERIVED; live schema unknown |
| M2 audit append | course_status_audit_logs | After changed status | Record course, numeric Admin user ID, previous/new status, database timestamp | Diagram intent DIRECT; physical mapping DERIVED |
| Enrollment/content mutation | None | No condition in branch | No writes or bulk updates | N/A; #77/policy sources separate |
| Transaction | Study Session | Q1→M1→M2→Q2; same-status Q1→Q2 | Commit after Course mapping; update and audit are atomic | Source implementation; fake DB tests only, live schema unknown |

## Response Source Matrix

| Response field | Contract type | Candidate source/transform | Gap/status |
|---|---|---|---|
| success | boolean | Envelope branch | true success / false error; envelope convention |
| businessCode | string | Catalog | Exact code per branch; DIRECT |
| message | string | Safe application text | Exact wording unspecified; DERIVED |
| data.items | Course[] | Q2 one updated row | One item only; singleton is DERIVED |
| data.items[0].id | int64 | courses.id | Legacy BIGSERIAL candidate |
| data.items[0].title | string | courses.name → title | Candidate mapping per #06/#74/#75 |
| data.items[0].description | string? | courses.description | Nullable; serialize null vs omit unresolved |
| data.items[0].thumbnail_url | uri? | courses.thumbnail_url | Nullable; serialize null vs omit unresolved |
| data.items[0].price | decimal-string | courses.price | Exact decimal conversion; legacy nullable but contract required |
| data.items[0].status | CourseStatus | Updated courses.status | Target value; enum members/casing unresolved |
| data.items[0].mentor.id | int64 | users.id via courses.mentor_id | Required; missing/orphan mentor rule unresolved |
| data.items[0].mentor.full_name | string | users.full_name | Required UserSummary field |
| data.items[0].mentor.avatar_url | uri? | users.avatar_url | Optional; null-vs-omit unresolved |
| data.items[0].category | Category? | No approved relation | Omit candidate; SOURCE_REQUIRED |
| data.pagination.page | int32 | Singleton Page | Fixed 1; DERIVED |
| data.pagination.size | int32 | Singleton Page | Fixed 1; DERIVED |
| data.pagination.total | int64 | Course row found | Fixed 1; DERIVED |
| data.pagination.total_pages | int32 | Singleton Page | Fixed 1; DERIVED |
| meta | object | Envelope | {} candidate; no counters in schema |
| traceId | uuid | Request trace | Shared middleware; propagate/generate |
| Error data | null by guideline | Current helper returns null by default | MATCH; local HTTP tested |
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

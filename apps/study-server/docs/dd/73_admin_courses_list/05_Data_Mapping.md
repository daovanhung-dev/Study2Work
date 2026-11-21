---
title: "Data Mapping"
order: 5
dd_id: "73"
api_name: "Lấy danh sách khóa học Admin"
source_sheet: "3. Data mapping"
status: "Draft — Needs Confirmation"
---

# Data Mapping

## Flow xử lý data

```text
Admin Bearer principal -> shared ADMIN JWT guard -> parse status/mentor/category/page -> validate query -> reject valid category before DB -> Q2 count/integrity -> Q1 page query -> map Page<Course> -> 200 or catalog error
```

# Mục lục

- [0. Check quyền](#step-0-check-quyen)
- [1. Validate data input](#step-1-validate-data-input)
- [2. Get thông tin](#step-2-get-thong-tin)
- [3. Get count](#step-3-get-count)
- [4. Check kết quả execute query](#step-4-check-ket-qua)
- [5. Map response](#step-5-map-response)
- [6. Trả về response](#step-6-tra-ve-response)
- [Request Usage Matrix](#request-usage-matrix)
- [Query Matrix](#query-matrix)
- [Mutation Matrix](#mutation-matrix)
- [Response Source Matrix](#response-source-matrix)

<a id="step-0-check-quyen"></a>

## 0. Check quyền

### 0.1. Xác thực và authorization

- Xác thực Bearer JWT và shared role `ADMIN` trước khi parse query hoặc truy vấn khóa học.
- Token thiếu/sai/không hợp lệ trả 401 `DESIGN_AUTHENTICATION_REQUIRED`.
- Principal không có role `ADMIN` trả 403 `DESIGN_ACCESS_DENIED`; course-management permission riêng chưa được kiểm tra.
- Shared JWT role guard có runtime source; course-management permission, tenant/scope policy riêng chưa có source.
- Không gọi shared Student guard của `app/utils/auth.py` cho API Admin.

### 0.2. Thứ tự truy cập

- Chỉ đọc query data sau khi authorization thành công.
- Không dùng `mentor` filter để thay thế Admin authorization; đây chỉ là filter dữ liệu.

### 0.3. Query/check quyền

| Target table/API | Column/field | Condition/value | Remarks |
|---|---|---|---|
| Authorization header | Bearer credential | Token hợp lệ/chưa hết hạn | DIRECT requirement; shared guard wired locally. |
| JWT claims/policy | Admin role | Principal có role `ADMIN` | DIRECT role; shared guard reads normalized roles. |
| Admin policy | course-management permission | Chưa kiểm tra riêng | AC-32 precondition; role-to-permission mapping `DERIVED`. |

<a id="step-1-validate-data-input"></a>

## 1. Validate data input

### 1.1. `status`

- Nhận string tùy chọn theo catalog.
- Nếu có, runtime dùng exact equality `courses.status = :status`; nếu vắng mặt thì không thêm status predicate.
- Không mặc định `PUBLISHED`, không normalize casing và không tạo enum allowlist.
- Catalog #76 ghi nhãn draft/published/suspended; current legacy/API #06 có `DRAFT`/`PUBLISHED`; casing và đầy đủ enum cần owner xác nhận.

### 1.2. `mentor`

- Nhận int64 tùy chọn.
- Nếu có, candidate predicate là `courses.mentor_id = :mentor`.
- Không thêm quy tắc positive range hoặc kiểm tra user role chưa có nguồn.

### 1.3. `category`

- Nhận int64 tùy chọn theo contract.
- Parse signed int64 theo catalog.
- Không có `courses.category_id` hoặc association table trong legacy DDL; pilot UUID model cũng không cho quan hệ category.
- Với giá trị int64 hợp lệ, runtime trả 422 `DESIGN_VALIDATION_ERROR` trước DB theo API #06 precedent. Đây là fallback `DERIVED`; category filter contract chưa được thực hiện cho tới khi relation được duyệt.
- Với kiểu hoặc miền số không hợp lệ, trả 422 field error `category`.

### 1.4. `page`

- Nhận int32 tùy chọn.
- Runtime `DERIVED`: page 1-based int32, omitted dùng 1, page < 1 hoặc > 2147483647 trả 422 `DESIGN_VALIDATION_ERROR`.
- `PageMeta.size` bắt buộc nhưng catalog không khai báo query size; proposal dùng fixed size 20 theo API #06/#68.
- Integer parse lỗi dùng HTTP/business 422; exact route đã nằm trong `DESIGN_CONTRACT_PATHS`.

### 1.5. Query không được khai báo

- Không nhận `size` hoặc `sort`.
- Không dùng keyword/search vì catalog không có trường này.

<a id="step-2-get-thong-tin"></a>

## 2. Get thông tin

### 2.1. Q1 — page query after validation

Đây là SQL runtime cục bộ trên legacy candidate DDL. Fake DB tests kiểm tra query/binds; live schema chưa xác minh.

```sql
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
WHERE (:status IS NULL OR c.status = :status)
  AND (:mentor IS NULL OR c.mentor_id = :mentor)
ORDER BY c.id ASC
LIMIT :limit OFFSET :offset
```

- `limit = 20`; `offset = (page - 1) * 20` theo implementation `DERIVED`.
- Không thêm predicate `c.status = 'PUBLISHED'` khi `status` vắng mặt.
- Nếu `category` có giá trị hợp lệ, không chạy query này; validator trả 422 trước DB.
- Chỉ chọn Course và UserSummary fields; không lấy user email/phone/credential.

### 2.2. Q1 result integrity

- `courses.mentor_id` nullable trong legacy DDL nhưng `Course.mentor` required.
- Candidate đọc mentor bằng LEFT JOIN để phát hiện missing mentor; không silently bỏ course bằng INNER JOIN.
- API #06 coi missing mentor là lỗi integrity và trả safe 500; áp dụng cho #73 là proposal cần xác nhận vì Admin có thể cần xem/sửa dữ liệu mồ côi.

### 2.3. Joins

| Base table | Joined table | Condition | Type | Purpose/status |
|---|---|---|---|---|
| `courses AS c` | `users AS m` | `m.id = c.mentor_id` | LEFT JOIN candidate | Map required `Course.mentor`; integrity check theo API #06 precedent. |
| `courses AS c` | Category relation | Chưa xác định | N/A | Không có JOIN; valid category request trả 422 `DERIVED`. |

### 2.4. WHERE

| Điều kiện | Candidate predicate | Trạng thái |
|---|---|---|
| Có `status` | `c.status = :status` | Exact-match `DERIVED`; enum/case unresolved. |
| Không có `status` | Không thêm status predicate | All-status list `DERIVED`; không lọc `PUBLISHED`. |
| Có `mentor` | `c.mentor_id = :mentor` | Direct filter + candidate physical mapping. |
| Có `category` | Không chạy query; trả 422 trước DB | Fallback `DERIVED`; relation/predicate chưa có nguồn. |
| Không có filter | Không áp dụng các optional predicate | `DERIVED`. |

### 2.5. ORDER BY và pagination

- Default order proposal: `c.id ASC` vì API không khai báo sort input.
- `page` mặc định 1; fixed size 20; `offset = (page - 1) * 20`; `LIMIT = 20`.
- Page vượt tổng vẫn trả page rỗng với tổng count; không trả 404.
- Query category hợp lệ bị reject trước cả Q1/Q2 cho tới khi relation được xác nhận.

<a id="step-3-get-count"></a>

## 3. Get count

### 3.1. Q2 — count query

```sql
SELECT
    COUNT(*) AS total,
    COUNT(*) FILTER (WHERE m.id IS NULL) AS missing_mentor_count
FROM courses AS c
LEFT JOIN users AS m ON m.id = c.mentor_id
WHERE (:status IS NULL OR c.status = :status)
  AND (:mentor IS NULL OR c.mentor_id = :mentor)
```

- Runtime gọi Q2 trước Q1; cả hai dùng cùng status/mentor predicates.
- Valid category request bị từ chối trước Q2; query không đếm khi filter không được áp dụng.
- Nếu `missing_mentor_count > 0`, runtime trả safe 500 theo API #06 precedent; Admin recovery behavior vẫn cần owner xác nhận.
- Count projection thiếu hoặc có giá trị NULL/âm trả safe 500; aggregate query phải cung cấp cả `total` và `missing_mentor_count`.

### 3.2. Page metadata

- `total = Q2.total`.
- `size = 20` theo proposal.
- `total_pages = ceil(total / 20)`.
- Nếu `total = 0`, `total_pages = 0`.

<a id="step-4-check-ket-qua"></a>

## 4. Check kết quả execute query

### 4.1. Thành công có dữ liệu

- Map từng record Q1 sau khi xác nhận Course và required mentor fields hợp lệ.
- Không trả PII ngoài `UserSummary`.

### 4.2. Thành công không có dữ liệu

- Không có row phù hợp trả 200 `DESIGN_RESOURCE_RETRIEVED` với `items=[]`.
- Page ngoài phạm vi vẫn trả 200 và giữ `total`, `total_pages` từ Q2.
- Đây là behavior `DERIVED` theo API #06 test/source precedent; catalog không khai báo 404 cho collection.

### 4.3. Lỗi query hoặc mapping

- SQLAlchemy query lỗi, count/projection lỗi, decimal/course mapping lỗi dùng 500 `DESIGN_INTERNAL_ERROR` và rollback an toàn.
- Không trả SQL, stack trace, hay thông tin credential.
- Thiếu mandatory mentor/price là candidate integrity failure; owner cần xác nhận có chặn toàn trang hay báo row-level.

### 4.4. Input validation

- Sai kiểu query hoặc page < 1 trả 422 `DESIGN_VALIDATION_ERROR`.
- Valid category trả 422 `DESIGN_VALIDATION_ERROR` trước DB theo fallback `DERIVED`; không tuyên bố đây là behavior owner-approved.

<a id="step-5-map-response"></a>

## 5. Map response

### 5.1. Map mỗi Course

- `items[].id = courses.id`.
- `items[].title = courses.name`.
- `items[].description = courses.description`.
- `items[].thumbnail_url = courses.thumbnail_url`.
- `items[].price = decimal string từ courses.price`, không qua float.
- `items[].status = courses.status` giữ nguyên stored value.
- `items[].mentor.id = users.id`.
- `items[].mentor.full_name = users.full_name`.
- `items[].mentor.avatar_url = users.avatar_url`.
- Catalog `items[].category` optional chưa có field trong reusable runtime `Course`; hiện OpenAPI/response omit field này.
- Optional description/thumbnail/avatar theo API #06 precedent serialize `null` khi source NULL; cần xác nhận contract null-vs-omit.

### 5.2. Map PageMeta

- `pagination.page = effective page`.
- `pagination.size = 20`.
- `pagination.total = Q2.total`.
- `pagination.total_pages = ceil(total/20)`, bằng 0 khi total=0.

## Request Usage Matrix

| Request field | Source | Query use | Response use | Basis/status |
|---|---|---|---|---|
| Authorization | Bearer header | Không đưa vào SQL; shared `ADMIN` check trước parse/query | Không map | Role guard source-backed; dedicated permission mapping `DERIVED`. |
| `status` | Query string | Optional `c.status = :status` trong Q1/Q2 | Không map trực tiếp | Filter DIRECT; equality DERIVED. |
| `mentor` | Query int64 | Optional `c.mentor_id = :mentor` trong Q1/Q2 | Không map trực tiếp | Filter DIRECT; legacy candidate. |
| `category` | Query int64 | Valid int64 rejected before DB; invalid value gets parse 422 | Không map trực tiếp | Filter DIRECT; current fallback `DERIVED`, relation unresolved. |
| `page` | Query int32 hoặc default | Q1 offset | `pagination.page` | Type DIRECT; default/minimum DERIVED. |
| Body | None | None | None | DIRECT. |

## Query Matrix

| Query ID | Type | Source | Selected fields | Predicate/order/page | Result/status |
|---|---|---|---|---|---|
| Q1 | SELECT | Legacy `courses AS c` LEFT JOIN `users AS m` | Course and mentor projection | Status/mentor optional; `id ASC`; bind limit 20 and offset `(page-1)*20` | Runtime local; live schema unverified. |
| ↑ | SELECT | Legacy `courses AS c` | `c.name AS title` | Same row as Q1 | Alias theo Course.title. |
| ↑ | SELECT | Legacy `courses AS c` | `c.description` | Same row as Q1 | Nullable candidate. |
| ↑ | SELECT | Legacy `courses AS c` | `c.thumbnail_url` | Same row as Q1 | Nullable candidate. |
| ↑ | SELECT | Legacy `courses AS c` | `c.price` | Same row as Q1 | Decimal-string projection candidate. |
| ↑ | SELECT | Legacy `courses AS c` | `c.status` | Optional exact status predicate | Enum/case unresolved. |
| ↑ | SELECT | Legacy `courses AS c` | `c.mentor_id` | Optional `c.mentor_id=:mentor` | Legacy mentor filter candidate. |
| Q1 | LEFT JOIN | Legacy `users AS m` | `m.id` | `m.id=c.mentor_id` | Required mentor ID projection. |
| ↑ | LEFT JOIN | Legacy `users AS m` | `m.full_name` | `m.id=c.mentor_id` | Required mentor name projection. |
| ↑ | LEFT JOIN | Legacy `users AS m` | `m.avatar_url` | `m.id=c.mentor_id` | Optional mentor avatar projection. |
| Q2 | COUNT | Legacy `courses AS c` LEFT JOIN `users AS m` | `COUNT(*)` | Same status/mentor predicates as Q1 | Candidate `PageMeta.total`. |
| ↑ | COUNT | Legacy `courses AS c` LEFT JOIN `users AS m` | `COUNT(*) FILTER (WHERE m.id IS NULL)` | Same status/mentor predicates as Q1 | Candidate mentor integrity count. |
| Q3 | Category validation | No approved relation | Không chọn column/JOIN | Signed int64 validation, then reject valid value before DB | `DERIVED` fallback 422. |

## Mutation Matrix

| Operation | Target | Condition | Fields | Status |
|---|---|---|---|---|
| None | N/A | API #73 là GET/read-only | Không INSERT/UPDATE/DELETE | `N/A — READ-ONLY API` |

## Response Source Matrix

| Response field | Type | Source/transform | Null/empty rule | Evidence status |
|---|---|---|---|---|
| `success` | boolean | Envelope branch | true success / false error | DIRECT envelope. |
| `businessCode` | string | Catalog | Exact branch code | DIRECT. |
| `message` | string | Safe application message | Text unspecified | DERIVED wording. |
| `data.items[]` | `Course[]` | Q1 rows | `[]` when empty | DIRECT type; empty behavior DERIVED. |
| `data.items[].id` | int64 | `courses.id` | Required | Legacy candidate. |
| `data.items[].title` | string | `courses.name` alias | Required | Candidate mapping; API #06 precedent. |
| `data.items[].description` | string? | `courses.description` | null when source NULL | Optional; #06 precedent. |
| `data.items[].thumbnail_url` | uri? | `courses.thumbnail_url` | null when source NULL | Optional; #06 precedent. |
| `data.items[].price` | decimal-string | `courses.price` via exact Decimal formatting | Required; NULL → candidate 500 | #06 source precedent. |
| `data.items[].status` | string | `courses.status` | Preserve source value | Runtime model uses string; enum/case incomplete. |
| `data.items[].mentor.id` | int64 | `users.id` joined on mentor_id | Required; missing mentor → candidate 500 | Legacy nullable integrity gap. |
| `data.items[].mentor.full_name` | string | `users.full_name` | Required | UserSummary candidate. |
| `data.items[].mentor.avatar_url` | uri? | `users.avatar_url` | null when source NULL | Optional; #06 precedent. |
| `data.items[].category` | Category? | Catalog optional; runtime Course model omits field | Omitted | Relation/runtime schema discrepancy. |
| `data.pagination.page` | int32 | Effective page/default 1 | 1 when omitted | Default DERIVED. |
| `data.pagination.size` | int32 | Fixed configuration | 20 | DERIVED; no request field. |
| `data.pagination.total` | int64 | Q2 count | 0 if no rows | Candidate. |
| `data.pagination.total_pages` | int32 | `ceil(total/20)` | 0 if total=0 | DERIVED. |
| `meta` | object | Envelope convention | `{}` | Current helper on success/error. |
| `traceId` | uuid | Middleware | Validated/generated | Current source convention. |

<a id="step-6-tra-ve-response"></a>

## 6. Trả về response

### 6.1. Thành công

- HTTP 200 `DESIGN_RESOURCE_RETRIEVED` với `ApiEnvelope<Page<Course>>`.
- Không có match trả page rỗng, không dùng 404.

### 6.2. Lỗi validation hoặc quyền

- Auth thiếu/sai: 401 `DESIGN_AUTHENTICATION_REQUIRED`.
- Không có `ADMIN` role: 403 `DESIGN_ACCESS_DENIED`; dedicated course-management permission chưa được kiểm tra.
- Query parse/page invalid: 422 `DESIGN_VALIDATION_ERROR`.

### 6.3. Lỗi hệ thống

- DB/query/count/mapping failure: 500 `DESIGN_INTERNAL_ERROR`.
- Response chỉ chứa safe message và trace ID; không lộ SQL/stack trace.

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

---
title: "Data Mapping"
order: 5
dd_id: "55"
api_name: "Lấy bài làm và rubric Mentor"
source_sheet: "3. Data mapping"
status: "Draft — Needs Confirmation"
---

# Data Mapping

## Flow xử lý data

~~~text
1. Nhận Authorization và raw path `submission_id`
2. Gọi shared guard `validate_current_user_request(..., role="MENTOR")` để xác thực Bearer/JWT và numeric subject
3. Parse path signed-int64; malformed/overflow -> 404 `DESIGN_RESOURCE_NOT_FOUND`
4. Q1 đọc Submission, LEFT JOIN assignment/course và LATERAL lookup UploadAsset theo URL/owner/purpose/course
5. Không có submission -> 404; quan hệ required null/orphan -> 500; course không thuộc Mentor -> 403
6. Chỉ sau khi direct-owner check đạt mới map các field reusable `Submission`
7. Rubric theo AC-23 không có field trong Submission schema và không có relation assignment được duyệt (DISCREPANCY)
8. Trả `ApiEnvelope<Submission>`; UI tiếp tục gọi #56 grade và #57 feedback
~~~

API #55 đã có route/module và TestClient coverage. Query dùng legacy DDL làm candidate target; tests thay DB bằng fake rows nên không xác minh live schema hoặc query execution trên PostgreSQL.

## Request Usage Matrix

| Request field | Source | Step | Validation | Query/response use | Gap |
|---|---|---:|---|---|---|
| Authorization | Header | 0.1 | Bearer access JWT hợp lệ; yêu cầu Mentor | Numeric subject được so với `courses.mentor_id` | Shared guard is source-backed; direct-owner policy remains DERIVED |
| `submission_id` | Path | 1.1 / 2.1 | Required signed int64; không có minimum trong catalog | `s.id`; map sang `data.id` | Current raw-path parser maps malformed/overflow to catalog 404 as DERIVED fallback |
| Request body | N/A | N/A | N/A | N/A | Catalog không khai báo body |
| Query parameters | N/A | N/A | N/A | N/A | Catalog không khai báo query |

## 0. Check quyền

### 0.1. Thực hiện check quyền

- Trích Bearer token từ `Authorization`.
- Giải mã access JWT bằng `decode_access_token`; current token contract có `sub` và `roles`.
- Chuẩn hóa `sub` thành numeric user ID theo `validate_access_claims`.
- Yêu cầu `MENTOR` có trong roles theo catalog; current shared request guard hỗ trợ role tường minh.
- Nếu token thiếu/sai/hết hạn hoặc claim không hợp lệ, trả HTTP 401 `DESIGN_AUTHENTICATION_REQUIRED`.
- Nếu token hợp lệ nhưng không có role Mentor, trả HTTP 403 `DESIGN_ACCESS_DENIED`.

### 0.2. Query/check quyền

| Target table/API | Column/Field | Condition/Value | Remarks |
|---|---|---|---|
| `assignment_submissions AS s` | `s.id` | `s.id = :submission_id` | Candidate lookup theo ID; BIGSERIAL trong legacy DDL. |
| `assignment_submissions AS s` | `s.assignment_id` | `a.id = s.assignment_id` | Candidate FK; nullable trong legacy DDL. |
| `assignments AS a` | `a.course_id` | `c.id = a.course_id` | Candidate course scope; nullable trong legacy DDL. |
| `courses AS c` | `c.mentor_id` | `c.mentor_id = :mentor_id` | Direct-owner predicate DERIVED; không chứng minh assigned Mentor. |

### 0.3. Check kết quả

- Nếu query không tìm thấy `s.id`, trả HTTP 404 `DESIGN_RESOURCE_NOT_FOUND`.
- Nếu `assignment_id`, assignment hoặc course không tồn tại trong quan hệ candidate, coi là integrity failure và trả 500 `DESIGN_INTERNAL_ERROR` theo đề xuất DERIVED; xác nhận trạng thái required/live schema còn thiếu.
- Nếu course không thuộc `mentor_id` hiện tại, candidate trả 403 `DESIGN_ACCESS_DENIED`; quy tắc mask resource tồn tại bằng 404 chưa được chốt.
- Nếu relation/ownership hợp lệ, chỉ lúc đó mới serialize field Submission cho response.
- Nếu course được phân công nhưng `courses.mentor_id` khác Mentor hiện tại, current fallback từ chối; assigned-course policy cần được bổ sung nguồn.

## 1. Validate data input

- `submission_id`: nhận một giá trị path có thể biểu diễn bằng int64 theo catalog.
- Catalog không nêu ID dương/minimum/maximum hoặc behavior cho path không parse được.
- Không thêm HTTP 400/422 hoặc business code ngoài catalog.
- Current source accepts signed int64 raw path; int64 hợp lệ nhưng không có row → 404.
- Current source maps malformed/overflow path to 404 `DESIGN_RESOURCE_NOT_FOUND` following API #48; this status mapping is DERIVED because the catalog does not specify it.

## 2. Get thông tin

### 2.1. Q1 — đọc submission, scope quyền và file metadata

Q1 đọc record theo `submission_id`, giữ left join để còn quan sát submission có FK null/orphan trong legacy DDL. Kết quả chỉ được dùng để dựng response sau khi Mentor access check đạt.

| Target table | Column get | Chú thích | Remarks |
|---|---|---|---|
| `assignment_submissions AS s` | `s.id` | Submission ID | Candidate primary key. |
| `↑` | `s.assignment_id` | Assignment ID | Required trong logical contract; DDL nullable. |
| `↑` | `s.user_id` | Student ID | Required trong logical contract; DDL nullable. |
| `↑` | `s.content` | Text bài làm | Nullable candidate. |
| `↑` | `s.file_url` | Legacy single file URL | DERIVED: match exact URL to `uploads.url` with owner, purpose and course constraints; at most one asset. |
| `↑` | `s.submitted_at` | Thời điểm nộp | TIMESTAMP; timezone chưa rõ. |
| `↑` | `s.score` | Điểm đã lưu | NUMERIC(6,2) candidate; map decimal-string chưa xác nhận format. |
| `↑` | `s.feedback` | Feedback đã lưu | Nullable candidate; Student disclosure không thuộc API Mentor này. |
| `↑` | `s.status` | Trạng thái submission | Nullable/default candidate; enum đầy đủ chưa có. |
| `assignments AS a` | `a.id` | Kiểm tra quan hệ assignment | Left join candidate vì FK có thể NULL. |
| `↑` | `a.course_id` | Course scope | Nullable trong legacy DDL. |
| `courses AS c` | `c.id` | Kiểm tra course tồn tại | Left join candidate. |
| `↑` | `c.mentor_id` | Candidate direct owner | So sánh với numeric Mentor `sub`; DERIVED. |

~~~sql
SELECT s.id, s.assignment_id, s.user_id, s.content, s.status,
       s.submitted_at, s.score, s.feedback,
       a.id AS matched_assignment_id, a.course_id,
       c.id AS matched_course_id, c.mentor_id,
       asset.id AS file_id, asset.name AS file_name, asset.url AS file_url,
       asset.content_type AS file_content_type,
       asset.size_bytes AS file_size_bytes, asset.status AS file_status
FROM assignment_submissions AS s
LEFT JOIN assignments AS a ON a.id = s.assignment_id
LEFT JOIN courses AS c ON c.id = a.course_id
LEFT JOIN LATERAL (
    SELECT u.id, u.file_name AS name, u.url, u.content_type, u.size_bytes, u.status
    FROM uploads AS u
    WHERE u.url = s.file_url
      AND u.owner_id = s.user_id
      AND u.purpose = 'SUBMISSION'
      AND u.course_id = a.course_id
    ORDER BY u.id ASC
    LIMIT 1
) AS asset ON TRUE
WHERE s.id = :submission_id
LIMIT 1;
~~~

> This matches `FIND_MENTOR_SUBMISSION` in current source. It targets the checked-in legacy DDL candidate; fake DB tests do not verify live PostgreSQL schema or execution.

### 2.2. JOIN

| Target table | Join condition | Join type |
|---|---|---|
| `assignment_submissions AS s` | N/A | BASE relation in current Q1 |
| `assignments AS a` | `a.id = s.assignment_id` | LEFT JOIN; retains null/orphan evidence |
| `courses AS c` | `c.id = a.course_id` | LEFT JOIN; retains null/orphan evidence |
| `uploads AS u` | constrained by exact URL, owner, purpose and course | LATERAL subquery; zero or one match |

### 2.3. WHERE

- `s.id = :submission_id` dùng parameter binding.
- Không đưa `user_id` từ query/body; student identity chỉ là dữ liệu của submission.
- Direct owner comparison `c.mentor_id = :mentor_id` được thực hiện trong view sau khi record được tìm thấy; đây là DERIVED fallback theo API #46 và API #54.
- Không thêm predicate `status = 'SUBMITTED'`; AC-23 không giới hạn API #55 ở submission chưa chấm và #56/#57 cần đọc bản ghi theo flow chấm.
- Không filter theo status hoặc course publication state; catalog/diagram không khai báo điều kiện này.

### 2.4. ORDER BY

N/A — Tra một submission bằng primary key candidate; không có collection/sort contract.

### Query Matrix

| Query ID | Purpose | Type | Base table/view | Alias | Columns | JOIN | WHERE | ORDER/pagination | Result/branch | Status |
|---|---|---|---|---|---|---|---|---|---|---|
| Q1 | Đọc submission, kiểm tra parent/owner và lấy tối đa một asset | SELECT | `assignment_submissions` | `s` | Submission fields, join IDs/owner và UploadAsset metadata | LEFT JOIN `assignments a`, `courses c`; LATERAL `uploads u` | `s.id = :submission_id`; constrained asset predicates | `u.id ASC LIMIT 1`; no page | No row→404; broken parent→500; owner mismatch→403; otherwise map response | Wired source; legacy DDL target candidate; live DB unverified |
| Q2 | Rubric/criteria cho assignment | N/A | Không có assignment-rubric relation được duyệt | N/A | N/A | N/A | N/A | N/A | Không query hoặc thêm field rubric vào `Submission` | `SOURCE_REQUIRED / DISCREPANCY` |

### 2.5. Xử lý access và integrity

- Nếu record không tồn tại, trả lỗi theo [06_Error.md](./06_Error.md).
- Nếu required relation ID/owner null, sai kiểu hoặc LEFT JOIN không khớp, current source trả 500 `DESIGN_INTERNAL_ERROR` as DERIVED integrity handling.
- Nếu khóa quan hệ hợp lệ nhưng Mentor không khớp direct owner, current source trả 403 `DESIGN_ACCESS_DENIED`.
- Access check diễn ra trước response mapping; không phát lộ content/file URL cho caller bị từ chối.
- 403/404 masking, assigned Mentor access và orphan policy remain `Draft — Needs Confirmation`; current source uses direct 403 and 500 integrity fallbacks.

## 3. Insert/Update thông tin

### 3.1. Target table

N/A — READ-ONLY API.

### 3.2. Conditions

N/A — Không có mutation.

### 3.3. Items update/insert

N/A — Không có mutation.

### 3.4. Parameters

| Param | Giá trị | Remarks |
|---|---|---|
| N/A | N/A | Không có query/mutation parameter cho INSERT/UPDATE. |

## 4. Check kết quả execute query

### 4.1. Thành công

- Q1 trả một record hợp lệ và direct-owner check đạt thì map `ApiEnvelope<Submission>`.
- `files[]` uses the same DERIVED constrained lookup as API #54; no match returns `[]`.
- Rubric remains SOURCE_REQUIRED because the legacy Assignment model has no approved rubric relation.

### 4.2. Lỗi hệ thống

- Query exception/mapping exception → HTTP 500 `DESIGN_INTERNAL_ERROR` theo catalog.
- Orphan/null required relation hoặc required field không thỏa logical schema → current source returns HTTP 500 with the catalog code as DERIVED integrity handling.

### 4.3. Validate lỗi

- JWT sai/thiếu → HTTP 401 `DESIGN_AUTHENTICATION_REQUIRED`.
- Không có role Mentor hoặc course owner không khớp → HTTP 403 `DESIGN_ACCESS_DENIED`.
- Catalog không khai báo 422; không thêm error branch đó.

### 4.4. Ngoài trường hợp trên

- `submission_id` hợp lệ nhưng không có submission → HTTP 404 `DESIGN_RESOURCE_NOT_FOUND`.
- Bản ghi tồn tại nhưng relation rubric/assets chưa có source không được giả thành “not found”; đó là unresolved design blocker, không có response behavior đã được duyệt.

## Response Source Matrix

| Response field | Type | Source type | Table/column hoặc generator | Data Mapping step | Transform | Null/empty/omit rule | Gap |
|---|---|---|---|---:|---|---|---|
| `success` | boolean | Envelope | Branch result | 5 | `true` success; `false` error | Always present | Shared convention |
| `businessCode` | string | Catalog | Exact catalog literal | 5 | Fixed per branch | Always present | DIRECT |
| `message` | string | Application message | Safe localized message | 5 | Branch-specific | Always present | Exact text unspecified |
| `data.id` | int64 | Legacy DDL candidate | `s.id` | 4 | Direct | Required | Live schema unknown |
| `data.assignment_id` | int64 | Legacy DDL candidate | `s.assignment_id` | 4 | Direct | Required; null is integrity issue | DDL nullable conflict |
| `data.user_id` | int64 | Legacy DDL candidate | `s.user_id` | 4 | Direct | Required; null is integrity issue | DDL nullable conflict |
| `data.content` | string? | Legacy DDL candidate | `s.content` | 4 | Preserve | Current source omits null | Contract null/omit policy open |
| `data.files[]` | UploadAsset[] | DERIVED API #54 fallback | Matched `uploads` row | Q1 | Return at most one asset | `[]` when no match | API #35 URL storage not verified |
| `data.files[].id` | int64 | Legacy DDL candidate | `uploads.id` | Q1 | Direct | Present only with match | No FK/API #35 guarantee |
| `data.files[].name` | string | Legacy DDL candidate | `uploads.file_name` | Q1 | Alias to name | Present only with match | No FK/API #35 guarantee |
| `data.files[].url` | uri | Legacy DDL candidate | `uploads.url` | Q1 | Exact match to `s.file_url` | Present only with match | No FK/API #35 guarantee |
| `data.files[].content_type` | string | Legacy DDL candidate | `uploads.content_type` | Q1 | Direct | Present only with match | No FK/API #35 guarantee |
| `data.files[].size_bytes` | int64 | Legacy DDL candidate | `uploads.size_bytes` | Q1 | Direct | Present only with match | No FK/API #35 guarantee |
| `data.files[].status` | UploadStatus | Legacy DDL candidate | `uploads.status` | Q1 | Direct | Present only with match | No FK/API #35 guarantee |
| `data.status` | SubmissionStatus | Legacy DDL candidate | `s.status` | 4 | Preserve stored value | Required; null integrity issue | Enum incomplete |
| `data.submitted_at` | date-time | Legacy DDL candidate | `s.submitted_at` | 4 | Pydantic JSON serialization | Required | Zone/precision unresolved |
| `data.score` | decimal-string? | Legacy DDL candidate | `s.score` | 4 | `str(score)` | Current source omits null | #56 uses `int32`; alignment unresolved |
| `data.feedback` | string? | Legacy DDL candidate | `s.feedback` | 4 | Preserve stored value | Current source omits null | Student disclosure policy unresolved |
| `meta` | object | Envelope | `success_response` | 5 | Empty object | `{}` when no metadata | Current source behavior |
| `traceId` | uuid | Request trace | Current trace helper | 5 | Propagate request trace | Always present | Current source behavior |

**Rubric:** Not a reusable `Submission` field. Current source does not query or return rubric until the catalog/diagram/schema discrepancy is reconciled.

## Mutation Matrix

| Mutation ID | Operation | Target table | Record condition | Fields | Value sources | Audit | Mapping file | Transaction | Failure behavior |
|---|---|---|---|---|---|---|---|---|---|
| N/A | None | N/A | Read-only endpoint | N/A | N/A | N/A | N/A | N/A | N/A — READ-ONLY API |

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

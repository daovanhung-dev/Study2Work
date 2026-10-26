---
title: "Data Mapping"
order: 5
dd_id: "34"
api_name: "Upload file"
source_sheet: "3. Data mapping"
status: "Draft — Ready for Review"
---

# Data Mapping

## Flow xử lý data

~~~text
0. Validate Bearer JWT; require Student or Mentor role.
1. FastAPI parses required file/purpose and optional int64 course_id.
2. Match SUBMISSION to Student or LECTURE to Mentor; check ACTIVE enrollment or direct course owner.
3. Measure actual bytes and choose filename/content-type fallbacks.
4. Generate uploads/<UUID>; stream file to S3-compatible Object Storage and construct public URL.
5. INSERT uploads metadata, read BIGSERIAL id and commit.
6. Return UploadAsset; on DB failure rollback and best-effort delete the object.
~~~

## Request Usage Matrix

| Request field | Source | Validate | Query/mutation usage | Response usage | Gap |
|---|---|---|---|---|---|
| Authorization | Header | Valid Bearer JWT with STUDENT or MENTOR | Principal ID is owner/enrollment query parameter | Not returned | Token/role claims are validated by shared auth helper. |
| file | Multipart file part | Required; any bytes accepted | Stream to provider; count bytes from received spool | name, content_type, size_bytes | No MIME allowlist or application size cap. |
| purpose | Multipart field | Enum SUBMISSION or LECTURE; role must match | Persist purpose | status of intended asset lifecycle | SUBMISSION is Student-only; LECTURE is Mentor-only. |
| course_id | Multipart field | Optional int64; required for LECTURE | ACTIVE enrollment for Student; direct owner lookup for Mentor | Persist nullable course_id | No positive-only constraint. |

## 0. Check quyền

- Shared `validate_current_user_request` accepts `role=("STUDENT", "MENTOR")`; existing single-role callers retain their behavior.
- Purpose policy is checked before any DB query or Object Storage side effect.
- Student SUBMISSION with no course_id requires no enrollment lookup.
- Student SUBMISSION with course_id queries `enrollments.user_id`, `course_id`, and `status = 'ACTIVE'`.
- Mentor LECTURE requires course_id and queries `courses.id` plus `courses.mentor_id = principal_id`.
- A missing matching enrollment/course-owner row returns 403; API #34 catalog does not declare 404.

## 1. Validate request

- Missing or malformed multipart field maps to 422 DESIGN_VALIDATION_ERROR.
- Unknown purpose maps to 422; valid purpose used by wrong role maps to 403 DESIGN_ACCESS_DENIED.
- Missing course_id for LECTURE maps to 422.
- course_id outside signed int64 range maps to 422; no extra positive-only rule is imposed.
- The route does not validate MIME, file extension, content signature, size cap or filename path.
- Filename uses `file.filename or "upload"`; Content-Type uses `file.content_type or "application/octet-stream"`.
- The size is measured by seeking to end of the received spool, reading its byte position, and rewinding it before storage.

## 2. Permission queries

| Query ID | Purpose | Base table | Predicate | Result | Failure |
|---|---|---|---|---|---|
| Q1 | Student course enrollment | enrollments | `user_id = :student_id AND course_id = :course_id AND status = 'ACTIVE'` | One matching row | No row → 403; DB error → 500. |
| Q2 | Mentor direct owner | courses | `id = :course_id AND mentor_id = :mentor_id` | One matching row | No row → 403; DB error → 500. |

## 3. Object Storage mutation

| Step | Operation | Target | Values | Failure behavior |
|---|---|---|---|---|
| 3.1 | Generate key | Server | `uploads/{uuid4()}` | Key is not accepted from request. |
| 3.2 | Upload stream | S3-compatible bucket | File stream and `ContentType` | 503 DESIGN_DEPENDENCY_UNAVAILABLE; rollback and best-effort delete. |
| 3.3 | Construct URL | Application | `OBJECT_STORAGE_PUBLIC_BASE_URL.rstrip('/') + '/' + storage_key` | Invalid/missing storage config maps to 503. |

## 4. Metadata mutation

| Mutation ID | Operation | Table | Fields | Source | Transaction and failure |
|---|---|---|---|---|---|
| M1 | INSERT | uploads | owner_id | JWT subject | Same transaction as other metadata. |
| M1 | INSERT | uploads | purpose | Validated purpose enum | Fixed values SUBMISSION/LECTURE. |
| M1 | INSERT | uploads | course_id | Multipart field or NULL | Student may omit; Mentor may not. |
| M1 | INSERT | uploads | storage_key | Server-generated UUID key | Unique key also identifies object cleanup. |
| M1 | INSERT | uploads | file_name | Multipart filename or `upload` | Stored as received; never used as object key. |
| M1 | INSERT | uploads | url | Public URL from storage configuration | Stored and returned. |
| M1 | INSERT | uploads | content_type | Part Content-Type or octet-stream fallback | No allowlist/sniffing. |
| M1 | INSERT | uploads | size_bytes | Measured received bytes | Zero is allowed. |
| M1 | INSERT | uploads | status | Constant `UPLOADED` | DB default and CHECK agree with the only current status. |
| M1 | INSERT | uploads | id | BIGSERIAL | Returned from INSERT; commit failure rolls back and triggers best-effort object delete. |

## 5. Error and response mapping

- Storage write/configuration failure returns 503 DESIGN_DEPENDENCY_UNAVAILABLE.
- Course access/purpose authorization failure returns 403 DESIGN_ACCESS_DENIED.
- Multipart/type/int64 validation failure returns 422 DESIGN_VALIDATION_ERROR.
- DB query, INSERT, or commit failure returns 500 DESIGN_INTERNAL_ERROR after rollback and best-effort object deletion when an object key was attempted.
- Success returns the committed ID and persisted UploadAsset metadata with 201 DESIGN_RESOURCE_CREATED.
- API #47 later resolves IDs from uploads and must filter same Mentor, purpose LECTURE, and same course; no API #47 runtime is wired by this task.

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

---
title: "Data Mapping"
order: 5
dd_id: "57"
api_name: "Lưu feedback bài nộp Mentor"
source_sheet: "3. Data mapping"
status: "Draft — Needs Confirmation"
---

# Data Mapping

## Flow xử lý data

~~~text
Mentor Bearer JWT
-> nhận submission_id, feedback_text và attachments theo wire fallback
-> shared MENTOR guard, sau đó khóa submission và kiểm tra direct course owner
-> UPDATE chỉ assignment_submissions.feedback; attachments nhận opaque nhưng không lưu/echo
-> resolve files[] bằng API #54 DERIVED lookup, validate Submission response rồi commit
-> lỗi query/quyền/mapping/commit rollback; trả 200 DESIGN_RESOURCE_UPDATED hoặc lỗi catalog trong 06_Error.md
-> AC-23 UI báo lưu feedback thành công
~~~

API #57 có runtime source và TestClient coverage. Các bảng/cột trong ma trận vẫn là legacy DDL candidates; source/test không xác nhận live schema hoặc migration.

## Request Usage Matrix

| Request field | Source | Step | Validation/use | Query or response use | Gap/status |
|---|---|---:|---|---|---|
| Authorization | Header Authorization | 0.1 | Bearer JWT và role Mentor theo catalog | Numeric subject for direct-owner candidate | Shared MENTOR guard is source-backed; direct-owner policy remains DERIVED |
| submission_id | Path | 1, 2.1 | Required signed int64; malformed/overflow => 422 | Khóa candidate assignment_submissions.id | Runtime checked; schema live chưa xác minh |
| feedback_text | Body fallback | 1, 3.1 | Required strict string; no trim/length/non-empty rule | `assignment_submissions.feedback` | Wire spelling DERIVED from catalog descriptor |
| attachments | Body | 1, 3.1 | Required strict string; opaque, unparsed | Không dùng trong SQL/response | Target/format remain SOURCE_REQUIRED |
| Content-Type | Header | 1 | application/json | Body parser | Route được đăng ký |
| X-Trace-Id | Header theo API Guidelines | 0, 5 | Optional UUID propagation | Envelope traceId và response header | Shared convention; route được đăng ký |
| Request body extras | Body | 1 | Không có field bổ sung trong catalog | N/A | Không thêm field |

## 0. Check quyền

### 0.1. Thực hiện check quyền

- Catalog yêu cầu Bearer JWT và role Mentor.
- AC-23 precondition yêu cầu Mentor có quyền chấm submission thuộc course.
- Shared Study guard requires explicit MENTOR role and returns the numeric subject before database access.
- Runtime direct-owner rule is `courses.mentor_id = authenticated Mentor ID`; this remains DERIVED and does not prove assigned-Mentor support.
- Không thêm rule submission phải có status GRADED khi API được gọi trực tiếp; diagram chỉ đặt #57 sau #56 trong UI flow.

### 0.2. Query/check quyền

| Target table/API | Column/Field | Condition/Value | Remarks |
|---|---|---|---|
| assignment_submissions AS s | s.id | s.id = :submission_id | Candidate existence lookup; DDL ID is BIGSERIAL. |
| assignment_submissions AS s | s.assignment_id | s.assignment_id = assignments.id | Candidate relation; DDL FK is nullable. |
| assignments AS a | a.course_id | a.course_id = courses.id | Candidate relation; DDL FK is nullable. |
| courses AS c | c.mentor_id | c.mentor_id = :mentor_id | DERIVED direct-owner candidate; Mentor ID source mapping unresolved. |

### 0.3. Check kết quả

- Bearer thiếu/không hợp lệ: theo catalog 401 DESIGN_AUTHENTICATION_REQUIRED.
- Actor không phải Mentor hoặc không có quyền trên course: 403 DESIGN_ACCESS_DENIED.
- Không tìm thấy submission: candidate 404 DESIGN_RESOURCE_NOT_FOUND.
- Submission tồn tại nhưng required assignment/course/owner relation null/orphan: safe 500 DESIGN_INTERNAL_ERROR.
- Submission thuộc course của Mentor khác: 403; không áp dụng mask thành 404.

## 1. Validate data input

- submission_id phải đáp ứng signed int64; malformed/overflow trả 422 DESIGN_VALIDATION_ERROR, ID không tìm thấy trả 404.
- feedback text phải là string theo catalog; không tự đặt giới hạn, trim, non-empty hay định dạng.
- attachments phải là string theo catalog; nhận opaque string nhưng không parse/lưu/echo; encoding và storage target SOURCE_REQUIRED.
- Catalog không định nghĩa field-level error codes, độ dài, mảng asset hay format URL; không thêm các quy tắc đó.

## 2. Get thông tin

### 2.1. Candidate Q1 — đọc submission và course scope

| Target table | Column get | Chú thích | Remarks |
|---|---|---|---|
| assignment_submissions AS s | s.id | Submission ID | Candidate từ legacy DDL. |
| ↑ | s.assignment_id | Assignment relation | Nullable trong DDL; ERD/table guide thể hiện required. |
| ↑ | s.user_id | Student ID | Cần cho Submission response; không lấy từ request. |
| ↑ | s.content | Nội dung bài làm | Nullable candidate. |
| ↑ | s.file_url | URL file học viên nộp | API #54 uses a DERIVED constrained lookup; API #35 must persist the matching URL. |
| ↑ | s.submitted_at | Thời điểm nộp | TIMESTAMP candidate; timezone policy mở. |
| ↑ | s.score | Điểm do #56 lưu | NUMERIC(6,2) candidate; giữ giá trị, không tính lại. |
| ↑ | s.feedback | Feedback hiện tại | Nullable candidate; dùng để phản hồi sau mutation. |
| ↑ | s.status | Trạng thái submission | Ghi nhận trạng thái; không ép GRADED precondition cho direct call. |
| assignments AS a | a.id | Assignment ID | Candidate join target. |
| ↑ | a.course_id | Course ID | Nullable relation candidate. |
| courses AS c | c.id | Course ID | Candidate authorization context. |
| ↑ | c.mentor_id | Direct owner ID | DERIVED access candidate. |

### 2.2. JOIN

| Target table | Join condition | Join type |
|---|---|---|
| assignment_submissions AS s | N/A | BASE candidate |
| assignments AS a | a.id = s.assignment_id | LEFT JOIN candidate to retain nullable/orphan row evidence |
| courses AS c | c.id = a.course_id | LEFT JOIN candidate to retain nullable/orphan row evidence |

DDL nullable references differ from required relationships in the guide/ERD. Join and orphan behavior must be confirmed against the chosen live schema.

### 2.3. WHERE

- Candidate identity filter: s.id = :submission_id.
- Candidate direct-owner access check: c.mentor_id = :mentor_id.
- Do not infer assigned-Mentor joins or a principal claim name.
- Do not add status = GRADED to API #57's direct request predicate.
- If the selected row has null/orphan assignment/course links, return/error behavior remains SOURCE_REQUIRED.

### 2.4. ORDER BY

- N/A — Candidate query addresses one submission by primary key.

## Query Matrix

| Query ID | Purpose | Type | Candidate target | Candidate fields/condition | Status |
|---|---|---|---|---|---|
| Q1 | Read submission and derive Mentor course scope | SELECT | assignment_submissions s, assignments a, courses c | s.id plus candidate relation/owner fields described above | DERIVED schema candidate; access identity unresolved |

## 3. Insert/Update thông tin

### 3.1. Target table

- assignment_submissions — legacy candidate only.

### 3.2. Conditions

- Candidate row key: assignment_submissions.id = :submission_id.
- Candidate authorization scope: the submission resolves through assignment to a course whose courses.mentor_id equals the authenticated Mentor ID.
- View locks the row; UPDATE repeats the direct-owner predicate. Broken parent/owner projections return safe 500; live relation integrity remains unverified.

### 3.3. Items update/insert

- Runtime UPDATE changes assignment_submissions.feedback only; see [07_assignment_submissions_feedback_update.md](./07_assignment_submissions_feedback_update.md). Repeated calls overwrite the single nullable field as a DERIVED fallback.
- attachments has no approved target column/table/relation; do not claim it is saved.
- Diagram also says INSERT/UPDATE; no history INSERT is implemented because no history target/relation is source-backed.

### 3.4. Parameters

| Param | Giá trị | Remarks |
|---|---|---|
| submission_id | Path submission_id | Required int64 descriptor. |
| mentor_id | Numeric subject from shared MENTOR guard | Direct-owner check is DERIVED; assigned-Mentor policy remains SOURCE_REQUIRED. |
| feedback_text | Required request wire fallback | Maps to feedback as DERIVED; exact wire key still needs owner approval. |
| attachments | Request attachments | Required strict string; accepted opaquely and unused because no persistence binding is approved. |

### Mutation Matrix

| Mutation ID | Operation | Target | Condition | Fields | Status |
|---|---|---|---|---|---|
| M1 | UPDATE fallback | assignment_submissions | Locked row and direct-owner predicate | feedback = feedback_text | Implemented; mutation is DERIVED; live schema/owner approval unresolved |
| M2 | Store feedback attachments | Not used | No approved attachment relation | N/A | No table or column invented; input is accepted but not persisted |
| M3 | INSERT feedback history | Not used | No history relation exists | N/A | Repeated call overwrites one field as DERIVED fallback |

## 4. Check kết quả execute query

### 4.1. Thành công

- UPDATE affects the locked submission after direct-owner check, and repeats owner predicate in SQL.
- Read/map the Submission envelope according to [04_Response.md](./04_Response.md).
- Preserve score and status established by earlier workflow; API #57 does not update them.
- Full success projection uses API #54's DERIVED files lookup; API #35 URL compatibility and feedback attachment handling remain unresolved.

### 4.2. Lỗi hệ thống

- Query/mapping/commit failure maps only to 500 DESIGN_INTERNAL_ERROR and rolls back the caller-owned transaction.
- Do not expose SQL, tokens, attachment URLs, raw provider responses or stack traces.

### 4.3. Validate lỗi

- Invalid required path/body shape maps only to 422 DESIGN_VALIDATION_ERROR.
- Do not add a length, URL, array or non-empty condition without a source.

### Response Source Matrix

| Response field | Contract type | Candidate source | Mapping/null rule | Evidence status |
|---|---|---|---|---|
| success | boolean | Envelope branch | true on success; false on error | DIRECT envelope |
| businessCode | string | Catalog | Exact success/error code by branch | DIRECT |
| message | string | Application | Safe localized message; exact wording unspecified | DERIVED |
| data.id | int64 | assignment_submissions.id | Direct candidate | Legacy DDL candidate |
| data.assignment_id | int64 | assignment_submissions.assignment_id | Direct candidate | Nullable DDL discrepancy |
| data.user_id | int64 | assignment_submissions.user_id | Direct candidate | Nullable DDL discrepancy |
| data.content | string? | assignment_submissions.content | Preserve optional stored value | Nullable candidate; null/omit unresolved |
| data.files[] | UploadAsset[] | API #54 constrained uploads lookup (DERIVED) | Match file_url by URL, owner, purpose and course; keep feedback attachments separate | API #35 URL persistence and reusable resolver remain open |
| data.files[].id | int64 | uploads candidate via API #54 (DERIVED) | Match by URL, owner, purpose and course | API #35 compatibility remains open |
| data.files[].name | string | uploads metadata via API #54 (DERIVED) | Use matched UploadAsset metadata | API #35 compatibility remains open |
| data.files[].url | uri | uploads.url via API #54 (DERIVED) | Exact match to file_url with owner/purpose/course checks | API #35 compatibility remains open |
| data.files[].content_type | string | uploads metadata via API #54 (DERIVED) | Use matched UploadAsset metadata | API #35 compatibility remains open |
| data.files[].size_bytes | int64 | uploads metadata via API #54 (DERIVED) | Use matched UploadAsset metadata | API #35 compatibility remains open |
| data.files[].status | UploadStatus | uploads.status via API #54 (DERIVED) | Preserve matched status | Enum/lifecycle unresolved |
| data.status | SubmissionStatus | assignment_submissions.status | Preserve stored value, including prior #56 candidate GRADED | Candidate; enum members unresolved |
| data.submitted_at | date-time | assignment_submissions.submitted_at | Serialize timestamp | Candidate; timezone behavior unresolved |
| data.score | decimal-string? | assignment_submissions.score | Preserve prior score value; no recalc | NUMERIC-to-string conversion needs #56 decision |
| data.feedback | string? | assignment_submissions.feedback | Candidate value after update | DERIVED column mapping; nullable |
| meta | object | Shared envelope | Empty object candidate | DIRECT envelope shape; no pagination |
| traceId | uuid | Request trace | Propagate request trace | API Guidelines convention |

## 5. Trả về response

### 5.1. Thành công

- HTTPStatus = 200.
- businessCode = DESIGN_RESOURCE_UPDATED.
- Return ApiEnvelope<Submission> exactly; do not add feedback attachments, rubric or pagination fields.
- Populate data.feedback from the saved value when the candidate mapping is approved; other Submission fields follow their candidate sources.
- Keep error data null per API Guidelines and current helper behavior.

### 5.2. Business error

- Keep only the catalog 401, 403, 404 and 422 branches.
- Do not add 409 for repeat feedback or state conflict; the catalog does not declare it.

### 5.3. System error

- HTTPStatus = 500.
- businessCode = DESIGN_INTERNAL_ERROR.
- Return a safe message without internal/provider details.

---

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

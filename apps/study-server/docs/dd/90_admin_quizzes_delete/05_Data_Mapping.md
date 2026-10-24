---
title: "Data Mapping"
order: 5
dd_id: "90"
api_name: "Xóa quiz"
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "3. Data mapping"
format: markdown
status: "Draft — Needs Confirmation"
---

# Data Mapping

## Flow xử lý data

<a id="step-0-check-quyen"></a>

## Step 0 — Check quyền

### 0.1 Xác thực và authorize

- Đọc Bearer JWT từ `Authorization`.
- Xác thực token và kiểm tra role `Admin`.
- Kiểm tra `quiz-management permission` theo AC-35.
- Hoàn tất authorization trước khi kiểm tra quiz tồn tại hoặc attempt history.
- Current Study chỉ có Student guard; Admin guard/policy là `SOURCE_REQUIRED`.

### 0.2 Quyền

| Target table/API | Column/Field | Condition/Value | Remarks |
|---|---|---|---|
| Admin authorization policy | role | Admin | Catalog yêu cầu role; runtime guard chưa có. |
| AC-35 permission | quiz management | Allowed | Permission intent DIRECT; physical claim/permission source SOURCE_REQUIRED. |

### 0.3 Check kết quả

- Nếu xác thực/role thất bại: HTTP 401 `DESIGN_AUTHENTICATION_REQUIRED`.
- Nếu role hợp lệ nhưng permission bị từ chối: HTTP 403 `DESIGN_ACCESS_DENIED`.
- Nếu authorization thành công: tiếp tục Step 1.

<a id="step-1-nhan-request"></a>

## Step 1 — Nhận request

- Đọc `quiz_id` từ path; kiểu trực tiếp là `int64`.
- Không đọc body hoặc query parameter.
- Không tự thêm minimum/positive rule.
- Path parse/validation fail ánh xạ catalog 422 `DESIGN_VALIDATION_ERROR`; chính xác rule cần framework/source xác nhận.

<a id="step-2-tim-quiz"></a>

## Step 2 — Tìm quiz

### 2.1 Candidate lookup Q1

| Target table | Column get | Chú thích | Remarks |
|---|---|---|---|
| Legacy `quizzes AS q` | `q.id` | Quiz ID | Candidate BIGINT primary key; live schema chưa xác minh. |
| ↑ | `q.status` | Current lifecycle state | VARCHAR(20) candidate; enum chưa canonical. |
| ↑ | `q.updated_at` | Existing update timestamp | Candidate timestamp source for soft-delete only; semantic mapping needs approval. |

**WHERE**

- `q.id = :quiz_id`.

### 2.2 Check result

- Nếu không có quiz row: HTTP 404 `DESIGN_RESOURCE_NOT_FOUND`.
- Nếu `q.status = 'DELETED'`: proposal DERIVED là không ghi lại, dùng `q.updated_at` candidate làm timestamp ổn định và trả success Step 5.
- Nếu có quiz row chưa tombstone: tiếp tục Step 3.
- Idempotent repeat-delete behavior cần owner xác nhận.

## Step 3 — Kiểm tra attempt history

### 3.1 Candidate existence query Q2

| Candidate relation | Condition | Purpose | Status |
|---|---|---|---|
| Legacy `quiz_attempts AS qa` | `qa.quiz_id = :quiz_id` | Xác định quiz có ít nhất một attempt hay không | AC-35 intent DIRECT; legacy relation candidate, live schema chưa xác minh. |
| Attempt status | Không lọc theo `qa.status` | Tính cả attempt đang làm, đã nộp hoặc trạng thái khác | DERIVED từ “đã có attempts”; enum đầy đủ chưa được định nghĩa. |

- Query Q2 chỉ cần `EXISTS`; không tải danh sách attempts hoặc answers.
- Nếu có ít nhất một attempt: đi tới Step 4A.
- Nếu không có attempt: đi tới Step 4B.
- Kiểm tra và mutation phải thuộc cùng transaction candidate; lock/isolation/race với API #29 cần được chốt.

<a id="step-4a-soft-delete"></a>

## Step 4A — Có attempts: soft delete

### 4A.1 Candidate logical operation

- Giữ nguyên `quiz_questions`, `quiz_choices`, `quiz_attempts` và `quiz_answers`.
- Nếu quiz chưa tombstone, đề xuất UPDATE `quizzes.status = 'DELETED'` để quiz không còn được coi là hoạt động.
- Đề xuất cập nhật `quizzes.updated_at` cùng thời điểm xóa; map `DeleteResult.deleted_at` từ giá trị này nếu owner chấp thuận.
- Nếu quiz đã tombstone, proposal là no-op và giữ nguyên `updated_at` để DELETE lặp lại không đổi thời điểm xóa.
- `DELETED` không phải status enum đã xác minh; legacy DDL chỉ cho biết cột `VARCHAR(20)`.
- Thao tác map ở [07_quizzes_soft_delete.md](./07_quizzes_soft_delete.md).

### 4A.2 Cross-API behavior cần đồng bộ

- API #29 phải từ chối tạo attempt mới cho quiz đã bị xóa; predicate quiz-open và status value hiện chưa chốt.
- API #30–#32 phải tiếp tục thao tác/đọc attempt đã có theo quyền Student; không xóa answer history.
- API #87 list, #89 update và #91 statistics phải được thống nhất về visibility sau xóa trong macro-review #87–#91.

<a id="step-4b-khong-co-attempts-candidate-hard-delete"></a>

## Step 4B — Không có attempts: candidate hard delete

### 4B.1 Transaction candidate

- Bắt đầu một transaction bao phủ Q1, Q2 và cả ba DELETE để tránh partial delete.
- Isolation/row locking và phối hợp với API #29 là `SOURCE_REQUIRED`; không thêm HTTP 409 ngoài catalog.
- DDL legacy không khai báo ON DELETE CASCADE trong chuỗi quiz; xóa theo thứ tự child → parent.

### 4B.2 Xóa choices — M2

- DELETE rows trong `quiz_choices` có `question_id` thuộc các `quiz_questions` với `quiz_id = :quiz_id`.
- Không xóa lựa chọn riêng lẻ ngoài phạm vi target quiz.
- Mapping: [08_quiz_choices_delete.md](./08_quiz_choices_delete.md).

### 4B.3 Xóa questions — M3

- DELETE rows trong `quiz_questions` với `quiz_id = :quiz_id`.
- Mapping: [09_quiz_questions_delete.md](./09_quiz_questions_delete.md).

### 4B.4 Xóa quiz — M4

- DELETE row trong `quizzes` với `id = :quiz_id`.
- Chỉ chạy sau khi M2 và M3 thành công.
- Mapping: [10_quizzes_delete.md](./10_quizzes_delete.md).

### 4B.5 Commit/rollback

- Nếu toàn bộ mutation thành công: COMMIT rồi dựng `DeleteResult`.
- Nếu bất kỳ mutation nào lỗi: ROLLBACK toàn transaction rồi trả HTTP 500 `DESIGN_INTERNAL_ERROR`.
- Nhánh hard delete là proposal DERIVED; owner phải xác nhận vì diagram chỉ nêu rõ soft delete khi có attempts.

## Step 5 — Map response và trả kết quả

### 5.1 Success mapping

- `data.id = quiz_id` đã xác minh tồn tại trước mutation.
- `data.status = "deleted"` theo reusable `DeleteResult`.
- `data.deleted_at` là required nhưng chưa có physical source. Candidate soft-delete source là `quizzes.updated_at`; candidate hard-delete source là operation timestamp được capture trong transaction.
- Không trả attempt/answer rows hoặc quiz/question payload.
- Trả HTTP 200 `DESIGN_RESOURCE_DELETED` với `ApiEnvelope<DeleteResult>`.

### 5.2 Error mapping

- 401 → `DESIGN_AUTHENTICATION_REQUIRED`.
- 403 → `DESIGN_ACCESS_DENIED`.
- 404 → `DESIGN_RESOURCE_NOT_FOUND`.
- 422 → `DESIGN_VALIDATION_ERROR` cho request validation; trigger cụ thể SOURCE_REQUIRED.
- 500 → `DESIGN_INTERNAL_ERROR` cho lỗi query, mutation, transaction hoặc mapping.
- Không thêm 409 hoặc business code mới.
- Error envelope `data:null` theo API Guidelines; current helper trả `{}` nếu không truyền data.

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

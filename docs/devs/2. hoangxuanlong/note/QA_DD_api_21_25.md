# Q&A – Mâu thuẫn và điểm chưa rõ trong DD API #21–#25

- Phạm vi: `apps/study-server/docs/dd/21_users_me_progress` … `25_lessons_progress`
- Ngày rà soát: 2026-10-23
- Trạng thái DD hiện tại: tất cả đều là `Draft — Needs Confirmation`, phần lớn quy tắc nghiệp vụ ghi `SOURCE_REQUIRED`.
- Cột "Mức độ": **Mâu thuẫn** = DD tự mâu thuẫn hoặc mâu thuẫn với code/DB; **Chưa rõ** = DD chưa chốt; **Rủi ro** = DD chưa chốt và code đang tự chọn một hướng.
- Cột "Trả lời" để trống cho người quyết định điền.

---

## A. API #21 – `GET /users/me/progress`

| ID | Mức độ | Câu hỏi | Căn cứ trong DD / code | Trả lời |
|---|---|---|---|---|
| Q-21-01 | Mâu thuẫn | Response của API tên "Lấy tiến độ tổng hợp" nhưng catalog khai báo `ApiEnvelope<UserProfile>`. Cần trả **profile người dùng** hay **dữ liệu tiến độ**? | `05_Data_Mapping.md` ghi "Progress aggregate does not have a declared matching schema". Code hiện chỉ `SELECT` từ bảng `users` và trả `UserProfile`. | |
| Q-21-02 | Chưa rõ | Query selector `course_id list hoặc aggregate?:string` có tên field, cách truyền list (`course_id=1,2` hay `course_id=1&course_id=2`), kiểu, optionality như thế nào? | `03_Request.md` giữ nguyên chuỗi gốc của catalog. Route hiện nhận `course_id: str` và `aggregate: str`, nhưng view bỏ qua cả hai. | |
| Q-21-03 | Chưa rõ | Giá trị hợp lệ và ý nghĩa của `aggregate` là gì? Công thức tổng hợp (mẫu số, làm tròn, bao gồm bài nào) là gì? | `05_Data_Mapping.md` mục 2.4: "formula, denominator, inclusion/exclusion, rounding: SOURCE_REQUIRED". | |
| Q-21-04 | Chưa rõ | Khi user chưa ghi danh hoặc chưa có tiến độ thì trả gì (mảng rỗng, 0%, hay 404)? | `05_Data_Mapping.md` mục 3: "empty progress and no-enrollment result remain SOURCE_REQUIRED". | |
| Q-21-05 | Chưa rõ | Bộ lọc có xét `enrollments.status`, `courses.status`, `lessons.status` không? | `05_Data_Mapping.md` mục 2.3: "Enrollment status, Course status, Lesson status và visibility filters chưa xác định". | |
| Q-21-06 | Mâu thuẫn | `UserProfile` trong DD có field `bio`, nhưng bảng `users` trong `DB.sql` không có cột `bio`. Bỏ `bio` khỏi contract hay thêm cột? | `05_Data_Mapping.md` bảng Response Source Matrix. Model code `UserProfile` hiện không có `bio`. | |
| Q-21-07 | Chưa rõ | Catalog không liệt kê 422 cho API này. Nếu `course_id` sai kiểu thì trả 422 hay bỏ qua? | `05_Data_Mapping.md` mục 1.1: "Không tự đặt enum, default, range ... 422 condition". | |
| Q-21-08 | Chưa rõ | Có chặn user có `users.status` khác `ACTIVE` không? Có kiểm tra `refresh_tokens` (đã thu hồi) không? | DD chỉ nhắc "Bearer JWT + role Student". | |

## B. API #22 – `GET /lessons/{lesson_id}/access`

| ID | Mức độ | Câu hỏi | Căn cứ trong DD / code | Trả lời |
|---|---|---|---|---|
| Q-22-01 | Rủi ro | Trạng thái enrollment nào được coi là "có quyền học"? Code đang tự chọn `ACTIVE` và `COMPLETED`. | `05_Data_Mapping.md` mục 2.3: "Enrollment status values and the status eligible for access are SOURCE_REQUIRED"; mục 0.2: "do not infer active-state rule". Code: `FIND_ACTIVE_ENROLLMENT` trong `query.py`. | |
| Q-22-02 | Chưa rõ | Prerequisite (bài tiên quyết) được lưu và đánh giá thế nào? Hiện code không kiểm tra prerequisite. | AC-14 nhắc prerequisite, DD ghi "model/rule SOURCE_REQUIRED". | |
| Q-22-03 | Chưa rõ | Khi từ chối (403), "lý do" nằm ở field nào của response (`message`, `errors[]`, `meta`)? Code hiện trả message cố định `Access denied to this lesson.` | AC-14: "HTTP 403 + lý do". `05_Data_Mapping.md` mục 5.2: "response field/message location remains unresolved". | |
| Q-22-04 | Chưa rõ | Khi nào trả 404: lesson không tồn tại, lesson chưa PUBLISHED, khóa chưa PUBLISHED, hay `course_id` null? Code hiện chỉ trả 404 khi lesson không có hoặc `course_id` null. | `05_Data_Mapping.md` mục 2.3: "missing resource/visibility condition is SOURCE_REQUIRED". | |
| Q-22-05 | Chưa rõ | `lesson_id` không hợp lệ (<= 0, không phải số) trả 404 hay 422? Code hiện trả 404 cho `<= 0`; chuỗi không phải số bị FastAPI trả 422 theo format mặc định (route khai báo `lesson_id: int`). | `03_Request.md`: Min/Max là `SOURCE_REQUIRED`. | |

## C. API #23 – `POST /lessons/{lesson_id}/start`

| ID | Mức độ | Câu hỏi | Căn cứ trong DD / code | Trả lời |
|---|---|---|---|---|
| Q-23-01 | Mâu thuẫn | DD mô tả "UPSERT" nhưng đồng thời cấm chọn conflict target vì DDL không có unique `(user_id, lesson_id)`. Có thêm unique constraint và dùng `INSERT ... ON CONFLICT` không? Hiện code dùng `SELECT` rồi `INSERT`/`UPDATE`, nên có thể bị trùng bản ghi khi 2 request chạy song song. | `05_Data_Mapping.md` mục 2.3 và `07_table.md`. | |
| Q-23-02 | Chưa rõ | Khi row đã tồn tại và đang `COMPLETED`, gọi `start` có đặt lại về `IN_PROGRESS` không? Code hiện giữ nguyên `COMPLETED`. | `07_table.md`: "existing-state transition/preservation is unresolved". | |
| Q-23-03 | Chưa rõ | Có ghi `last_accessed_at` khi start không? Có đặt `progress_percent = 0` khi insert không? | `07_table.md`: "không được so đồ ... là giá trị cần cập nhật; không tự đặt hoặc reset". (Sau khi sửa code theo DD thì hai cột này không còn được ghi; cần xác nhận lại.) | |
| Q-23-04 | Chưa rõ | Trả `201` cả khi row đã tồn tại (chỉ cập nhật) có đúng không, hay nên là `200`? | Catalog chỉ nêu 201 `DESIGN_RESOURCE_CREATED`. | |
| Q-23-05 | Rủi ro | API #23 có phải tự kiểm tra enrollment khi gọi trực tiếp không, hay tin vào việc client đã gọi API #22? Code hiện tự kiểm tra. | `05_Data_Mapping.md` mục 0.1: "direct-call entitlement check chưa được định nghĩa". | |
| Q-23-06 | Chưa rõ | Điều kiện trả 422 là gì? Code hiện không trả 422 mà trả 404 khi `lesson_id <= 0`. | `06_Error.md` hàng 4: "Catalog không định nghĩa validation condition". | |
| Q-23-07 | Chưa rõ | Atomicity: ghi tiến độ và dựng response phải cùng transaction không? Khi lỗi thì rollback thế nào? | `05_Data_Mapping.md` mục 4.5: "transaction boundary ... chưa có nguồn". | |

## D. API #24 – `GET /lessons/{lesson_id}`

| ID | Mức độ | Câu hỏi | Căn cứ trong DD / code | Trả lời |
|---|---|---|---|---|
| Q-24-01 | Chưa rõ | "Kiểm tra publish status" (AC-15) áp dụng cho bảng nào: `lessons.status`, `courses.status`, hay cả hai? Code hiện kiểm tra cả hai. | `05_Data_Mapping.md` mục 0.2 và 2.3. | |
| Q-24-02 | Chưa rõ | Khi chưa publish thì trả 403 hay 404? Code hiện trả 404. | `05_Data_Mapping.md` mục 2.3: "how unpublished content maps to 403 versus 404". | |
| Q-24-03 | Rủi ro | Trạng thái enrollment hợp lệ cho API này là gì? Code đang chọn `ACTIVE`, `COMPLETED`. | Cùng vấn đề với Q-22-01. | |
| Q-24-04 | Chưa rõ | Có áp dụng kiểm tra prerequisite không? | `05_Data_Mapping.md` mục 0.2. | |
| Q-24-05 | Chưa rõ | Catalog không có 422 cho API này. Nếu `lesson_id` không hợp lệ thì trả gì? | `05_Data_Mapping.md` mục 1. | |

## E. API #25 – `PATCH /lessons/{lesson_id}/progress`

| ID | Mức độ | Câu hỏi | Căn cứ trong DD / code | Trả lời |
|---|---|---|---|---|
| Q-25-01 | Mâu thuẫn | DD cấm thêm rule `position >= 0`, `0 <= percent <= 100`, nhưng kiểu `percent` trong DB là `SMALLINT`. Giá trị ngoài khoảng `SMALLINT` (ví dụ 100000) sẽ gây lỗi DB (500). Có chốt range cho `percent` và `position` không? Code hiện tự thêm range và trả 422. | `05_Data_Mapping.md` mục 1 (ghi chú dưới bảng), `06_Error.md` hàng 4. | |
| Q-25-02 | Mâu thuẫn | `position` là bắt buộc trong request nhưng ERD/DDL không có cột lưu `position`. Thêm cột (tên, kiểu, đơn vị giây hay ms) hay chỉ nhận mà không lưu? | `05_Data_Mapping.md` mục 3.3: "no physical column is present". | |
| Q-25-03 | Chưa rõ | Có ràng buộc giữa `percent` và `completed` không (ví dụ `completed=true` thì `percent=100`)? | `05_Data_Mapping.md` mục 1 ghi chú: "Không thêm coupling". | |
| Q-25-04 | Chưa rõ | Khi row đang `COMPLETED` mà client gửi `completed=false` hoặc `percent` thấp hơn (request đến sai thứ tự), có cho tiến độ lùi hoặc hạ trạng thái không? Code hiện cho phép. | `05_Data_Mapping.md` mục 3.3: "behavior for an existing COMPLETED row or out-of-order request is SOURCE_REQUIRED". | |
| Q-25-05 | Chưa rõ | **Course aggregate** (AC-14 "UPDATE lesson progress + course aggregate") lưu ở bảng nào, công thức ra sao? Code hiện chưa cập nhật aggregate nào. | `05_Data_Mapping.md` Q3/M2: "SOURCE_REQUIRED, không chỉ định nguồn/đích/công thức". | |
| Q-25-06 | Chưa rõ | Có ghi `last_accessed_at` và `completed_at` không? Nếu có thì quy tắc là gì (`completed_at` giữ giá trị đầu tiên hay ghi đè)? Code hiện ghi cả hai. | `05_Data_Mapping.md` mục 3.3: "timestamp policy SOURCE_REQUIRED". | |
| Q-25-07 | Chưa rõ | Nếu chưa có row tiến độ thì PATCH tạo mới (upsert) hay trả 404? Code hiện tạo mới. | `05_Data_Mapping.md` mục 3.2: "Whether mutation requires an existing row or creates one is not fully specified". | |
| Q-25-08 | Rủi ro | Cùng vấn đề race condition và unique `(user_id, lesson_id)` như Q-23-01. | `05_Data_Mapping.md` mục 2.3. | |
| Q-25-09 | Rủi ro | Trạng thái enrollment hợp lệ, kiểm tra publish của lesson/course, và 403 vs 404 cho API này. | `05_Data_Mapping.md` mục 0.3: "Không xác định ... enrollment, prerequisite, ownership hoặc publish state thế nào". | |
| Q-25-10 | Chưa rõ | Atomicity khi cập nhật tiến độ và aggregate: nếu một bước lỗi thì xử lý ra sao? | `05_Data_Mapping.md` mục 4.6. | |

## F. Điểm chung cho cả 5 API

| ID | Mức độ | Câu hỏi | Căn cứ | Trả lời |
|---|---|---|---|---|
| Q-ALL-01 | Mâu thuẫn | DD ghi các API là `UNWIRED / NOT_FOUND` nhưng code đã được wired trong `app/api/v1.py`. DD cần cập nhật trạng thái sau khi chốt. | Mục "Overview" / "Assumptions" của từng DD. | |
| Q-ALL-02 | Chưa rõ | Chỉ role `STUDENT` được gọi? Mentor/Admin xem thử bài học thì xử lý thế nào (hiện nhận 403)? | `auth.py` yêu cầu `STUDENT`; DD ghi "role Student". | |
| Q-ALL-03 | Chưa rõ | Message lỗi (`message`) chuẩn của từng nhánh là gì? | DD: "message catalog chưa có". | |
| Q-ALL-04 | Chưa rõ | Có cần chặn user có `users.status` khác `ACTIVE` không? | DD không đề cập. | |
| Q-ALL-05 | Chưa rõ | Cột `status` kiểu `VARCHAR(20)` không có CHECK. Danh sách giá trị hợp lệ của `lesson_progress.status`, `enrollments.status`, `lessons.status`, `courses.status` là gì? | `DB.sql`; DD ghi "enum values unspecified". | |
| Q-ALL-06 | Chưa rõ | Các bảng thiếu index (`lesson_progress(user_id, lesson_id)`, `enrollments(user_id, course_id)`, `lessons(course_id)`) và thiếu `updated_at` cho `lesson_progress` có nằm trong phạm vi DB design không? | `DB.sql` (không nằm trong DD của 5 API). | |

---

## Các lỗi code đã phát hiện nhưng DD không đề cập (tạm chưa sửa)

Các mục này theo yêu cầu **chưa sửa** cho tới khi DD được bổ sung.

1. `except:` trần trong tất cả view (nên dùng `except Exception:`).
2. `model_validate(...)` nằm trong khối `try` của transaction ở #23 và #25.
3. `execute_query` được import nhưng không dùng trong #23 `view.py`.
4. `FIND_ACTIVE_ENROLLMENT` ở #22 lấy thêm cột `e.status` nhưng không dùng.
5. Số `lesson_id` vượt `BIGINT` có thể gây lỗi DB (500).
6. Race condition khi insert `lesson_progress` (xem Q-23-01).
7. Không có kiểm tra `PUBLISHED` ở #22, #23, #25 (xem Q-22-04, Q-24-01).
8. Tiến độ có thể lùi và mất trạng thái `COMPLETED` ở #25 (xem Q-25-04).
9. Không kiểm tra `users.status` (xem Q-ALL-04).
10. `TIMESTAMP` không timezone trong `lesson_progress`, so với `TIMESTAMPTZ` trong `refresh_tokens`.


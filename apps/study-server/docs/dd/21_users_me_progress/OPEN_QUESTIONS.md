# OPEN_QUESTIONS

Các câu hỏi dưới đây chặn việc chuyển API #21 DD sang Ready/Final hoặc dùng làm implementation contract. Bản Draft giữ nguyên contract hiện có và không tự chọn câu trả lời.

## Q-21-01 — Query selector có grammar và kiểu dữ liệu nào?

<a id="q-21-01"></a>

**Bằng chứng**

- API #21 trong [list_api.md](../../../../../docs/lists/list_api.md) ghi query nguyên văn: course_id list hoặc aggregate?:string.
- AC-13 và AC-18 lặp lại cùng khai báo trong [AC_02_STUDENT_LEARNING.drawio](../../diagrams/AC_UNICA/AC_02_STUDENT_LEARNING.drawio).

**Vấn đề**

- Không rõ đây là field course_id dạng list, field aggregate dạng string optional, hai lựa chọn mutually exclusive, hay một grammar khác.
- Không có serialization format của list ID, allowed values, default hoặc validation rule.

**Ảnh hưởng**

- Không chốt được parameter rows, URL example, parsing, validation, SQL predicate hoặc boundary test.

**Cần quyết định**

- API owner chốt field names, cardinality/serialization, type, optionality, allowed values và semantics; cập nhật canonical catalog/diagram trước khi DD lên Ready.

## Q-21-02 — Aggregate progress gồm dữ liệu nào và tính ra sao?

<a id="q-21-02"></a>

**Bằng chứng**

- AC-18 mô tả API #21 “Aggregate progress theo user”.
- AC-18 gọi API #37 riêng sau khi chọn course; node API #37 mô tả “Aggregate lesson + quiz + assignment progress”.
- DB design có lesson_progress.status, progress_percent, completed_at; API #21/#37 query hiện ở trạng thái DESIGN_ONLY.

**Vấn đề**

- Chưa rõ API #21 chỉ aggregate lesson_progress hay còn gồm quiz/assignment, phạm vi khóa học nào được tính, denominator, completed rule, rounding hoặc cách xử lý dữ liệu chưa có.
- Không có công thức hoặc expected aggregate example trong nguồn.

**Ảnh hưởng**

- Không thể thiết kế SELECT/GROUP BY, xác nhận kết quả tiến độ hoặc viết expected-value test.

**Cần quyết định**

- Chốt nguồn progress, phạm vi, công thức, trạng thái hoàn tất, rounding và các ví dụ đầu vào/đầu ra. Giữ API #37 là endpoint chi tiết riêng theo diagram trừ khi canonical contract được cập nhật.

## Q-21-03 — Response data là UserProfile hay progress schema?

<a id="q-21-03"></a>

**Bằng chứng**

- Catalog khai báo ApiEnvelope<UserProfile>; reusable UserProfile không có field progress.
- AC-13 yêu cầu client ghép Course + progress và hiển thị % hoàn thành.
- AC-18 yêu cầu render dashboard + biểu đồ tiến độ nhưng không định nghĩa progress payload.

**Vấn đề**

- Response type hiện tại không mô tả aggregate progress hoặc merge key; chưa có schema tương ứng và chưa có null/empty semantics.

**Ảnh hưởng**

- Không chốt được response fields, data mapping, success example, course merge hoặc dashboard rendering contract.

**Cần quyết định**

- API owner xác nhận schema trả về và cập nhật catalog/diagram. Đến khi đó giữ ApiEnvelope<UserProfile> trong tài liệu, đánh dấu discrepancy và không thêm field.

## Q-21-04 — Current-user identity được gắn vào query thế nào?

<a id="q-21-04"></a>

**Bằng chứng**

- Endpoint dùng /me, contract yêu cầu Bearer JWT và role Student.
- Current [auth.py](../../../app/utils/auth.py) parse JWT sub thành user ID số dương; DB design liên kết lesson_progress.user_id tới users.id.
- API #21 chưa có route/query runtime để xác nhận binding.

**Vấn đề**

- Chưa có endpoint-specific source xác định identity guard, bind parameter, hay behavior nếu token resolve tới user không còn tồn tại.

**Ảnh hưởng**

- Không thể khẳng định query predicate hoặc authorization behavior đã chạy; không thể chứng minh isolation giữa các user.

**Cần quyết định**

- Xác nhận dùng shared Student guard và bind authenticated user ID vào progress ownership predicate; xác nhận behavior khi identity không resolve.

## Q-21-05 — Empty progress/no enrollment trả wire shape nào?

<a id="q-21-05"></a>

**Bằng chứng**

- AC-13 có nhánh UI empty state khi không có khóa học sau khi client ghép kết quả API #20 và API #21.
- API #21 hiện khai báo ApiEnvelope<UserProfile>, không định nghĩa collection hay empty result shape.

**Vấn đề**

- Chưa rõ API trả UserProfile rỗng/không có progress, collection rỗng theo schema khác, hay response thành công với một shape khác.
- Chưa rõ phân biệt user không có enrollment với user có course nhưng chưa có lesson progress.

**Ảnh hưởng**

- Client không thể xác định empty state hoặc phân biệt “chưa bắt đầu học” với “không có khóa học”.

**Cần quyết định**

- Chốt success wire shape cho từng trường hợp; đồng bộ schema với Q-21-03 và quy tắc ghép client của AC-13.

---

## Điều kiện đóng các câu hỏi

- Cập nhật nguồn canonical trước khi đổi trạng thái DD sang Ready/Final.
- Sau khi contract được xác nhận, cập nhật request/response/mapping/error cases và test scenarios liên quan.
- Không dùng suy luận từ API #37 hoặc current shared auth helper để tự đóng các quyết định trên.

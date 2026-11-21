# OPEN_QUESTIONS

Các câu hỏi dưới đây chặn việc chuyển API #20 DD sang Ready/Final hoặc dùng làm contract triển khai. Bản Draft giữ response type và query inputs đang có trong catalog, không tự chọn câu trả lời.

## Q-20-01 — Response là UserProfile hay danh sách Course?

<a id="q-20-01"></a>

**Bằng chứng**

- API #20 trong [list_api.md](../../../../../docs/lists/list_api.md) khai báo ApiEnvelope<UserProfile>.
- AC-13 trong [AC_02_STUDENT_LEARNING.drawio](../../diagrams/AC_UNICA/AC_02_STUDENT_LEARNING.drawio) gọi API #20 để nạp Enrollment + Course và hiển thị danh sách khóa học.
- AC-13 gọi API #21 riêng để lấy progress rồi ghép Course + progress tại client.

**Vấn đề**

- Type UserProfile không mô tả collection Course; catalog chưa định nghĩa schema payload Course cho API #20.

**Ảnh hưởng**

- Không thể chốt response fields, query projection, empty collection representation hoặc JSON course-list example.
- Không thể kết luận endpoint đáp ứng AC-13 chỉ từ response type hiện tại.

**Cần quyết định**

- API owner xác nhận payload danh sách và cập nhật nguồn canonical nếu cần. Đến khi có quyết định, giữ nguyên ApiEnvelope<UserProfile> trong DD và đánh dấu discrepancy; không đổi sang Page<Course> hoặc thêm progress.

## Q-20-02 — status lọc trạng thái nào?

<a id="q-20-02"></a>

**Bằng chứng**

- Catalog khai báo query status là optional string.
- DB design có enrollments.status và courses.status; enum đầy đủ không được khai báo trong API #20 row.

**Vấn đề**

- Chưa biết filter áp dụng trên Enrollment hay Course, enum hợp lệ, case sensitivity, default hoặc cách xử lý giá trị không hợp lệ.

**Ảnh hưởng**

- Không thể chốt query predicate, request validation, 422 condition hoặc test case cho filter.

**Cần quyết định**

- Xác nhận target column, giá trị hợp lệ, semantics và hành vi khi status bị bỏ qua hoặc không hợp lệ.

## Q-20-03 — page pagination được định nghĩa ra sao?

<a id="q-20-03"></a>

**Bằng chứng**

- Catalog chỉ khai báo page:int32?.
- API schemas có PageMeta và Page<T> dùng ở một số endpoint; API #20 hiện khai báo UserProfile, không khai báo Page hoặc PageMeta.

**Vấn đề**

- Chưa có page base, page size/default, max, ordering ổn định, total-count policy hoặc meta response mapping.

**Ảnh hưởng**

- Không thể chốt LIMIT/OFFSET, thứ tự kết quả, tính tái lập giữa các trang hoặc pagination metadata.

**Cần quyết định**

- Xác nhận semantics của page và các pagination fields cần trả; cập nhật catalog contract trước khi DD lên Ready.

## Q-20-04 — Kết quả không có khóa học có wire shape nào?

<a id="q-20-04"></a>

**Bằng chứng**

- AC-13 diagram yêu cầu UI hiển thị empty state nếu không có khóa học.
- API #20 response type hiện là UserProfile.

**Vấn đề**

- Diagram xác định hành vi UI, không xác định API trả collection rỗng, null, envelope khác hay một status khác.

**Ảnh hưởng**

- Client/backend không thể thống nhất điều kiện empty state từ wire response.

**Cần quyết định**

- Chốt success response khi không có enrollment và cập nhật payload schema theo quyết định ở Q-20-01.

## Q-20-05 — JWT subject map sang Enrollment.user_id thế nào?

<a id="q-20-05"></a>

**Bằng chứng**

- Endpoint /users/me/courses và actor Student biểu thị dữ liệu của user hiện tại.
- Current [auth.py](../../../app/utils/auth.py) parse JWT sub là số dương thành user ID và yêu cầu role STUDENT.
- DB design liên kết enrollments.user_id tới users.id.
- API #20 chưa có route/query runtime để xác nhận binding này.

**Vấn đề**

- Chưa có API #20 source xác định chính xác identity guard, cách truyền user ID vào query, hoặc behavior nếu token hợp lệ nhưng user/enrollment không còn tồn tại.

**Ảnh hưởng**

- Không thể tuyên bố predicate e.user_id = JWT sub đã chạy; ownership scope chỉ có thể ghi là candidate/derived trong Draft.

**Cần quyết định**

- Xác nhận API #20 dùng shared Student guard và ánh xạ user ID parse từ JWT sub vào enrollments.user_id; xác định behavior khi identity không resolve.

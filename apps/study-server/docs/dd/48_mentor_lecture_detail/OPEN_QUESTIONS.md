# Open Questions — API #48 Tải lecture của Mentor

**Trạng thái DD:** Draft — Needs Confirmation
**Endpoint:** GET /api/v1/mentor/lectures/{lecture_id}

Các quyết định dưới đây chưa có nguồn đủ để chuyển candidate thành implementation contract. Giữ nguyên catalog; không tạo field, bảng, enum hoặc business code để lấp chỗ trống.

## Q-48-01 — Nguồn assets và resolver

**Bằng chứng**

- Lecture yêu cầu assets:UploadAsset[]; UploadAsset có id, name, url, content_type, size_bytes, status.
- API #47 nhận asset refs:string! nhưng chưa định nghĩa wire key, định dạng hoặc lookup.
- API #34 chưa xác định ID generation, metadata persistence hay lookup.
- Legacy resources thiếu content_type, size_bytes và UploadStatus; V1-PILOT file_objects dùng UUID và mô hình khác.

**Cần xác nhận**

1. Asset refs trong #47 tham chiếu ID nào và format ra sao?
2. API #34 lưu metadata vào nguồn nào để #47/#48 resolve UploadAsset?
3. Resource/UploadAsset có quan hệ vật lý nào; URL là public hay signed?
4. Lecture không có asset thì biểu diễn assets=[] có được contract cho phép không?

**Ảnh hưởng:** Không thể dựng đầy đủ success response; đây là blocker cho response mapping của #48.

## Q-48-02 — Course ownership, phân công và Mentor identity

**Bằng chứng**

- AC-21 cho phép Mentor sở hữu hoặc được phân công course.
- #46/#47/#48 dùng candidate legacy courses.mentor_id; chưa có relation assignment trong artifacts legacy.
- Current Study auth helper chỉ có Student guard; Mentor principal có thể khác numeric users.id theo V1-PILOT.

**Cần xác nhận**

1. Relation nào biểu diễn course được phân công cho Mentor?
2. JWT subject của Mentor là numeric users.id hay UUID subject?
3. Có dùng cùng một authorization helper/predicate cho #46, #47 và #48 không?

**Ảnh hưởng:** Query ownership, 403 behavior và việc AC-21 hỗ trợ course được phân công.

## Q-48-03 — Schema đích và quan hệ Lecture/Course

**Bằng chứng**

- Legacy DB.sql dùng BIGINT lessons/course_id và cho phép course_id NULL; DB table guide mô tả course_id bắt buộc.
- V1-PILOT dùng UUID lessons theo chapter/course_version, không có cùng projection course_id/name/sort_order/status.
- Live schema chưa được xác minh.

**Cần xác nhận**

1. API #48 sẽ chạy trên legacy schema hay V1-PILOT schema?
2. Quan hệ từ lecture đến course trong schema đích là gì?
3. Nếu row lecture thiếu parent course hoặc course_id NULL, xử lý 500 hay 404?

**Ảnh hưởng:** Query, identifier type, parent authorization và projection course_id bắt buộc.

## Q-48-04 — Content nullable và cách serialize

**Bằng chứng**

- Lecture.content là optional string.
- Legacy lessons.content là TEXT NULL.
- API #47 gửi content:int64! và đã ghi discrepancy/decimal-string candidate.

**Cần xác nhận**

1. Khi lessons.content NULL, JSON omit content hay trả content:null?
2. content từ #47 là body text được biểu diễn số hay ID tham chiếu Content?

**Ảnh hưởng:** Tính ổn định response và mapping create → reload.

## Q-48-05 — LessonStatus và đọc DRAFT

**Bằng chứng**

- Legacy lessons.status có default DRAFT; catalog không liệt kê member của LessonStatus.
- API #47 candidate dùng default DRAFT.
- AC-21 gọi #48 ngay sau #47; API #9 public curriculum lọc PUBLISHED nhưng khác role/workflow.

**Cần xác nhận**

1. LessonStatus có những member nào và DRAFT có hợp lệ cho Lecture không?
2. Mentor được phép đọc Lecture DRAFT bằng #48 không?

**Ảnh hưởng:** Enum serialization và khả năng hoàn tất AC-21 read-after-create.

## Q-48-06 — Path parse failure

**Bằng chứng**

- lecture_id:int64! là path parameter bắt buộc.
- Catalog #48 chỉ liệt kê 401/403/404/500; không khai báo 422.

**Cần xác nhận**

1. Giá trị không phải int64 hoặc overflow được gateway/framework xử lý ra sao?
2. Có cần cập nhật catalog nếu API muốn trả validation error không?

**Ảnh hưởng:** Không thể thêm 422 vào DD nếu chưa sửa contract nguồn.

## Q-48-07 — Error envelope

**Bằng chứng**

- API Guidelines yêu cầu data:null ở error response.
- Current app/core/responses.py dùng {} khi data=None.
- API #48 chưa có runtime.

**Cần xác nhận**

1. Envelope expected cho endpoint mới theo guideline hay helper cần thay đổi?
2. Việc sửa helper có nằm ngoài scope Study API #48 không?

**Ảnh hưởng:** Expected contract và current helper representation khác nhau.

## Quyết định cần có trước khi DD chuyển Final

Ưu tiên chốt asset persistence/resolver; Mentor identity và assignment; schema đích; content semantics/null behavior; LessonStatus/DRAFT policy; malformed path contract; error envelope. Đến khi có các nguồn này, giữ trạng thái Draft — Needs Confirmation.

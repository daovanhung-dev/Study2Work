# Open Questions — API #47 Tạo lecture

Trạng thái: Draft — Needs Confirmation. Các câu hỏi dưới đây cần được giải quyết trước khi DD được coi là implementation-ready.

| ID | Câu hỏi | Bằng chứng hiện có | Ảnh hưởng | Trạng thái |
|---|---|---|---|---|
| Q1 | content:int64 là nội dung chữ được biểu diễn số, hay ID tham chiếu tới Content khác? | Catalog request int64; Lecture schema string?; legacy lessons.content TEXT; AC-21 ghi INSERT Lecture/Content; không có bảng contents trong legacy ERD/DDL. | Request parsing, storage và data.content response. | DISCREPANCY / SOURCE_REQUIRED |
| Q2 | asset refs dùng wire key nào và chuỗi có định dạng gì? | Catalog/diagram chỉ ghi asset refs:string!; không có delimiter/JSON/array semantics. | Request validation, parsing, duplicate handling và response assets. | SOURCE_REQUIRED |
| Q3 | API #34 sinh UploadAsset.id như thế nào và metadata được lưu/tra ở đâu? | API #34 DD không có DB write; legacy schema không có uploads; resources thiếu content_type, size_bytes, UploadStatus. | API #47 không thể tạo Lecture.assets[] đầy đủ hoặc xác minh asset thuộc uploader/course. | SOURCE_REQUIRED |
| Q4 | Asset refs có được lưu thành resources rows không, hay chỉ tham chiếu Object Storage/file registry? | Legacy resources có lesson_id, name, resource_type, url; API #34 persistence chưa xác định; V1-PILOT file_objects dùng UUID/schema khác. | Có/không có resources mutation, transaction, delete/cleanup và response mapping. | SOURCE_REQUIRED |
| Q5 | Mentor “được phân công” course được xác định bởi relation nào? | AC-21 gồm owns/assigned; API #46 candidate dùng courses.mentor_id; không có assignment table trong legacy ERD/DDL. | Q1 permission, 403 và candidate Mentor scope. | SOURCE_REQUIRED |
| Q6 | JWT Mentor principal là numeric users.id hay UUID subject; Mentor guard nào chuẩn? | API #46 nêu conflict; current Study helper có Student guard; V1-PILOT dùng UUID owner subject. | Ownership query, authz và schema binding. | DISCREPANCY |
| Q7 | Schema nào là target runtime: legacy BIGINT hay V1-PILOT UUID/versioned? | Hai DDL có cấu trúc lessons/courses khác nhau; database context nói live schema chưa verify. | ID types, table/columns, FK, defaults và migration. | NOT_VERIFIED |
| Q8 | LessonStatus gồm những giá trị nào và DRAFT có hợp lệ cho lecture mới không? | Legacy lessons.status default DRAFT; catalog không khai enum member list; pilot dùng versioned statuses. | INSERT default, response status và API #48 reload. | SOURCE_REQUIRED |
| Q9 | API #47 có yêu cầu course ở trạng thái cụ thể hoặc lecture tạo ra có publish state nào không? | AC-21 là Mentor create flow; catalog không có status input; #48 candidate đọc lại mà không lọc PUBLISHED; API #9 public read lọc PUBLISHED nhưng khác actor/flow. | Có thêm predicate/validation hay không; LessonStatus và quyền đọc draft vẫn cần xác nhận. | DERIVED / NEEDS_CONFIRMATION |
| Q10 | Response content khi DB value NULL phải omit hay trả null? | Lecture.content là optional; legacy column nullable; envelope schema không nói optional-field serialization. | JSON response stability. | SOURCE_REQUIRED |
| Q11 | created_at/updated_at phải serialize với timezone nào khi legacy cột là TIMESTAMP? | Legacy DDL yêu cầu timestamp nhưng không chỉ rõ timezone/default; API contract dùng date-time. | Timestamp correctness và round trip. | SOURCE_REQUIRED |
| Q12 | Error envelope dùng data:null theo guidelines hay data:{} theo current helper? | API guidelines yêu cầu null; app/core/responses.py default {}. | Expected response behavior chung. | DISCREPANCY |

## Candidate handling trong bản draft

- Legacy lessons là một candidate mapping, không xác nhận live schema.
- Candidate courses.mentor_id = current Mentor ID kế thừa hướng của API #46 nhưng không xử lý course assigned.
- content decimal-string conversion, title max 200, asset_refs wire key và default DRAFT đều cần xác nhận.
- Không tạo bảng/cột, không chuyển upload thành resource, không giả định mọi lecture là PUBLISHED.
- Không thêm error code ngoài 401/403/404/422/500 của catalog.


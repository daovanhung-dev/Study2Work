# Open Questions — Study API #34 Upload file

**Trạng thái DD:** Draft — Needs Confirmation
**Endpoint:** POST /api/v1/uploads

Các câu hỏi dưới đây giữ nguyên phần contract, nghiệp vụ và storage policy chưa được API catalog hoặc AC-17/AC-21 xác nhận. Không tự chốt các nội dung này trong draft.

## Q-34-01 — UploadPurpose values và role-purpose pairing

**Bằng chứng**

- API catalog khai báo purpose:UploadPurpose! nhưng không có định nghĩa enum.
- AC-17 dùng endpoint trong luồng Student nộp assignment.
- AC-21 dùng endpoint trong luồng Mentor đăng lecture/media.

**Cần xác nhận**

1. Những giá trị nào thuộc UploadPurpose?
2. Mỗi purpose cho phép Student, Mentor hay cả hai?
3. Purpose nào yêu cầu course_id, và purpose nào không dùng course context?

**Ảnh hưởng:** Request validation, authorization, storage metadata/key và cách downstream APIs liên kết asset.

## Q-34-02 — File validation và filename policy

**Bằng chứng**

- Catalog chỉ định file:binary!; không có allowlist MIME, giới hạn byte, extension hoặc signature rule.
- AC-17/AC-21 chỉ mô tả chọn file rồi lưu vào Object Storage.
- API #13 có quy tắc ảnh riêng cho avatar, không phải quy tắc chung cho API #34.

**Cần xác nhận**

1. MIME/file formats nào được chấp nhận theo từng purpose?
2. Giới hạn request/file size và cách đo byte là gì?
3. Có sniffing chữ ký, antivirus/content scanning hoặc từ chối filename/path nguy hiểm không?
4. Có giữ nguyên filename, chuẩn hóa hay tạo tên lưu trữ riêng?

**Ảnh hưởng:** Request contract, 422 cases, storage metadata và security requirements.

## Q-34-03 — Course ownership và uploader authorization

**Bằng chứng**

- Catalog cho phép Student và Mentor; course_id là optional.
- AC-21 có bước chọn course và đọc course ownership/assignment trước khi gọi upload.
- AC-17 yêu cầu Student được phép nộp, nhưng upload step không xác định predicate hoặc binding tới assignment/course.

**Cần xác nhận**

1. Khi nào course_id bắt buộc và API #34 kiểm tra course tồn tại/ownership ra sao?
2. Student được upload vào phạm vi nào; có cần enrolled hoặc assignment còn hạn không?
3. API #34 xác thực quyền theo purpose hay để API tạo submission/lecture chịu trách nhiệm?

**Ảnh hưởng:** Course query, 403 behavior, role-purpose scope và chống gắn file sang resource không được phép.

## Q-34-04 — UploadAsset identity, status và metadata persistence

**Bằng chứng**

- Catalog yêu cầu UploadAsset{id, name, url, content_type, size_bytes, status}.
- Catalog không định nghĩa UploadStatus hoặc nguồn/generator của asset ID và các field metadata.
- ERD footer ghi “Uploads lưu URL” nhưng không có Uploads entity/table; DB_UNICA_TABLES.md nói logical uploads không nằm trong 16 bảng ERD V1.
- Checked-in DB.sql không có Uploads table; live schema chưa được xác minh.

**Cần xác nhận**

1. Asset ID được tạo từ nguồn nào?
2. UploadStatus có giá trị và lifecycle nào?
3. name, content_type, size_bytes lấy từ client metadata hay được server/storage xác định?
4. Asset metadata có cần persistence không; nếu có, canonical table/schema nào chứa nó?

**Ảnh hưởng:** Response mapping, downstream reference, retry/deduplication và DB design.

## Q-34-05 — Object Storage URL, failure và cleanup

**Bằng chứng**

- AC-17/AC-21 chỉ nói Object Storage lưu file/media; không nêu provider, bucket, key hoặc URL policy.
- Catalog cho phép 503 DESIGN_DEPENDENCY_UNAVAILABLE và 500 DESIGN_INTERNAL_ERROR.
- API #13 là flow avatar riêng; nó dùng public URL/fixed key và trả 500 khi storage lỗi. Những lựa chọn đó không định nghĩa API #34.

**Cần xác nhận**

1. Response url là public URL hay signed URL; nếu signed thì thời hạn và quyền tải là gì?
2. Object key, overwrite/collision, retention và delete policy là gì?
3. Provider failure nào trả 503, failure nào trả 500?
4. Có timeout/retry/idempotency nào không; xử lý object mồ côi khi API nộp submission/lecture tiếp theo thất bại ra sao?

**Ảnh hưởng:** Storage security, response validity, operational reliability, 503/500 mapping và lifecycle chi phí.

## Quyết định cần có trước khi chuyển DD sang Final

Các câu hỏi về enum, file constraints, ownership, metadata persistence và URL/access policy cần được Product/API/Architecture owner xác nhận trước khi đánh dấu DD Final hoặc triển khai endpoint.

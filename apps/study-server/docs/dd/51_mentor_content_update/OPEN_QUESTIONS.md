# Open Questions — API #51 Cập nhật nội dung Mentor

**Trạng thái DD:** Draft — Needs Confirmation
**Endpoint:** `PUT /api/v1/mentor/content/{content_id}`

## Q-51-01 — Request body có field nào và semantics gì?

**Bằng chứng**

- Catalog #51 và AC-22 PUT node chỉ khai báo `path{content_id:int64!}`.
- API #51 local runtime dùng strict full replacement `{content_type, title, payload}`, tái sử dụng API #50.

**Cần xác nhận**

- Ba field này có phải contract chính thức và đều bắt buộc không?
- `content_type` có enum members nào; có cho đổi type của Content không?
- `title` có trim/length constraints; payload có subtype schemas nào?

**Ảnh hưởng:** Request/OpenAPI validation hiện là `DERIVED`; cần cập nhật catalog sau khi xác nhận.

## Q-51-02 — Snapshot schema và version numbering có được duyệt không?

**Bằng chứng**

- AC-22 yêu cầu `UPDATE Content + version`; migration 007 thêm `content_versions` dạng legacy BIGINT snapshot.
- Snapshot trước update được ghi với `version_no=MAX+1`; current `contents` row được xem là version kế tiếp implicit.
- Live schema và migration deployment chưa được probe.

**Cần xác nhận**

- `content_versions` có phải physical model chuẩn; current version có cần row/pointer rõ ràng không?
- Có cần backfill lịch sử hoặc khởi tạo version khi API #50 tạo Content không?
- Snapshot cần retention, immutable policy, khóa/index bổ sung nào không?

**Ảnh hưởng:** Migration 007 và query/API #51 là `DERIVED` fallback; không chứng minh production schema.

## Q-51-03 — Update có luôn đưa Content vào `PENDING_REVIEW` không?

**Bằng chứng**

- AC-33 queue đọc `PENDING_REVIEW`; API #50 cũng khởi tạo state đó.
- API #51 local runtime đặt current `contents.status=PENDING_REVIEW` sau mỗi PUT.
- AC-22 không định nghĩa transition và API #52 sở hữu publish/unpublish.

**Cần xác nhận**

- Update khi Content đang `PUBLISHED` có được thay current projection ngay không?
- Có cần giữ bản published làm active pointer đến khi Admin duyệt không?
- Admin approval `APPROVED/PUBLISHED` có tự publish hay phải gọi API #52?

**Ảnh hưởng:** Snapshot giữ dữ liệu cũ nhưng API #51 không bảo đảm public reader tiếp tục serve bản published cũ; #52/AC-33 chưa có revision selector.

## Q-51-04 — Ai là tác giả của revision và dữ liệu lịch sử cũ?

**Bằng chứng**

- AC-33 reviewer đọc author; legacy `contents` không có author/created_by field.
- Migration 007 có `archived_by`, là Mentor thực hiện update kế tiếp, không phải tác giả gốc.

**Cần xác nhận**

- Cần lưu `authored_by` cho revision mới ở đâu?
- Với Content cũ không có author, cho phép unknown/null hay cần backfill từ nguồn khác?
- `archived_at` ghi thời điểm snapshot, không phải thời điểm version ban đầu được tạo.

**Ảnh hưởng:** Không dùng `archived_by` để thỏa yêu cầu author của AC-33.

## Q-51-05 — Authorization dùng direct owner hay assigned Mentor?

**Bằng chứng**

- Catalog yêu cầu role Mentor; AC-22 yêu cầu quyền quản lý course.
- API #49 và API #51 current source dùng numeric JWT subject so với `courses.mentor_id`.

**Cần xác nhận**

- Có hỗ trợ co-owner/assigned Mentor không?
- JWT subject và `courses.mentor_id` có chung identity namespace không?
- 404/403 enumeration policy có cần đổi không?

**Ảnh hưởng:** Direct-owner là fallback từ API #49, không bao quát assignment.

## Q-51-06 — No-op update, concurrency và revision policy là gì?

**Bằng chứng**

- API #51 khóa row Content trong transaction nên các PUT qua endpoint này được serialize.
- Mỗi PUT hiện tạo snapshot dù body có giống dữ liệu hiện tại; catalog không có 409 hoặc version token.

**Cần xác nhận**

- Body không đổi có cần tạo snapshot và đẩy `PENDING_REVIEW` không?
- Có cần optimistic concurrency/version precondition không?
- API #52 và Admin review có phải khóa cùng row/revision theo cùng thứ tự không?

**Ảnh hưởng:** Không thêm 409; hiện chưa quy định chống lost update giữa #51 với các thao tác lifecycle khác.

## Q-51-07 — Lịch sử Content khi soft delete được giữ thế nào?

**Bằng chứng**

- API #53 DD đề xuất soft delete qua `contents.deleted_at`; migration 007 không cascade snapshot history.
- #53 retention/history policy còn Draft.

**Cần xác nhận**

- Snapshot có được giữ vĩnh viễn sau soft delete không?
- Có cần xóa/anonymize khi xóa user hoặc course không?

**Ảnh hưởng:** Foreign keys hiện ngăn hard-delete referenced Content/Course/User nếu snapshot còn tồn tại.

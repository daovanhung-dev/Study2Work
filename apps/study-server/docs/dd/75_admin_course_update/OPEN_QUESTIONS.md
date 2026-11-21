# Câu hỏi còn mở — API #75

Trạng thái tài liệu: `Draft — Needs Confirmation`. API #75 đã được wire local theo các fallback bên dưới. Đây là quyết định triển khai `DERIVED`, không phải approval sản phẩm hoặc bằng chứng schema live.

1. **Request body:** Catalog và AC-32 chỉ khai báo `course_id`; runtime hiện dùng `title`, `description`, `thumbnail_url`, `price`. Owner có duyệt bộ field này không?
2. **PUT semantics:** Runtime yêu cầu đủ cả bốn field và từ chối field lạ. Đây có phải full-replacement contract mong muốn không?
3. **Null/omission:** Runtime cho phép `description` và `thumbnail_url` là `null` để xóa; không cho omission. Có cần đổi semantics này không?
4. **Title validation:** Runtime giữ nguyên whitespace, không áp nonblank rule và giới hạn 200 ký tự theo legacy DDL candidate. Có rule khác được duyệt không?
5. **Thumbnail URL:** Runtime nhận string hoặc null, không kiểm tra URI scheme/host/length. Chính sách URL nào cần áp dụng?
6. **Price:** Runtime chỉ nhận decimal string, không exponent/rounding, scale tối đa 2 và 10 chữ số nguyên theo legacy `NUMERIC(12,2)`; cho phép số âm vì DDL không có CHECK. Precision/range/minimum nào được duyệt?
7. **Admin authorization:** Runtime dùng shared JWT role `ADMIN`. Claim/policy riêng cho “course-management permission” có được yêu cầu không?
8. **Schema/persistence:** Runtime nhắm legacy BIGINT `courses`; V1-PILOT dùng UUID/versioned `courses`. Schema nào đang được triển khai thật và live migration state là gì?
9. **Response owner/category:** `Course.mentor` và `price` bắt buộc nhưng legacy DDL cho phép null ở FK/price. Runtime trả 500 cho projection thiếu; có orphan/null policy khác không? Category tiếp tục omit đến khi có relation được duyệt?
10. **Response cardinality:** Runtime trả `Page<Course>` singleton 1/1/1/1 như #74. Catalog có cần chuyển sang resource đơn không?
11. **Status/audit boundary:** Xác nhận API #75 giữ nguyên `status`/`mentor_id` và không ghi audit; AC-32 giao status/audit cho #76.
12. **Timestamp/transaction:** Runtime đặt `updated_at=CURRENT_TIMESTAMP`, đọc lại projection cùng Session, commit sau mapping hợp lệ và rollback query/projection/commit failures. Có transaction/audit policy khác không?
13. **Counters/deleted target:** API #74 diagram nhắc counters nhưng Course response không có field; #77 soft-delete policy/visibility cũng chưa xác định. Không có counters query hoặc deleted filter trong #75.

## Ranh giới proposal

- Body, full-replacement/null behavior, numeric limits, legacy table mapping, singleton Page và transaction sequence là `DERIVED`.
- Shared role `ADMIN` là guard hiện có; dedicated course-management permission chưa có source.
- Không thay đổi API catalog, AC-32 diagram, schema artifact, API #76/#77 hay live database trong task này.

# Plan and Result — API #92 Lấy notification list

## Kế hoạch trước khi tạo DD

1. Giữ nguyên method/path/auth/query/response/status/error literals của catalog #92.
2. Đọc AC-36 diagram/index, legacy và V1-PILOT notification schemas; tách chúng, không tuyên bố live schema.
3. Tham khảo #43 về notification projection/pagination và #63/#64 về create/delivery tracking; không chuyển Student ownership hoặc Operation semantics sang #92.
4. Viết requirement, request-usage, query, mutation và response-source matrices; giữ `ApiEnvelope<Notification>` trực tiếp và chỉ đặt Page làm proposal `DERIVED`.
5. Tạo 8 sheet template cùng 3 report Markdown; read-only mapping là `N/A`; không sửa runtime/schema/catalog/diagram.
6. Rà exact contract, nội dung, examples, template appendix, link/anchor, bảng, fence, whitespace và file set ngay sau authoring.

## Kết quả

- Đã tạo 8 sheet template và 3 report tại `92_admin_notifications_list/`.
- Contract trực tiếp giữ singleton `ApiEnvelope<Notification>`; list/page semantics và fixed-size pagination được ghi riêng là proposal hoặc câu hỏi mở.
- Legacy BIGINT và V1-PILOT UUID được mô tả tách biệt; không có query/schema hoàn chỉnh để khẳng định implementation.
- AC-36 macro-review chưa hoàn tất; tiếp tục sau khi có #93–#96.
- Kiểm tra tĩnh chi tiết và kết quả cuối cùng nằm trong [VERIFICATION_REPORT.md](./VERIFICATION_REPORT.md).

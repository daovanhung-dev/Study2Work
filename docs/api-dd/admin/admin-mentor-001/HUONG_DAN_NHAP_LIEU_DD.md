# Huong dan cap nhat DD - ADMIN-MENTOR-001

## Cach dung

1. Đọc `README.md` để nắm endpoint, module và status.
2. Đọc `01_Overview/Overview.md` để kiểm tra source trace, actor, permission, ownership/scope và Open Questions.
3. Cập nhật `03_Request/Request.md` và `04_Response/Response.md` nếu BA/PO hoặc Tech Lead chốt contract chi tiết.
4. Cập nhật `05_DataMapping/DataMapping.md` khi có data design, repository, transaction hoặc async behavior rõ hơn.
5. Cập nhật `06_Error/Error.md` để giữ business code và safe message ổn định.
6. Append `02_History/History.md`; không sửa/xóa row lịch sử cũ.
7. Cập nhật `API_DD_CHECKLIST.md`, `docs/checklists/API.md` và worklog khi status thay đổi.

## Quy tac

- Giữ code, endpoint, field, enum, table và businessCode bằng English/camelCase/snake_case như contract.
- Mô tả nghiệp vụ có thể viết tiếng Việt để team review.
- Nếu thiếu source, ghi `OPEN_QUESTION`; không tự chuyển sang `APPROVED`.
- Không thêm scope employer/recruitment/job/CV/interview vào DD này.

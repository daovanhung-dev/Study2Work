# Plan Result — API #82 Lấy danh sách lesson

## Kết quả

Đã tạo DD Markdown theo 8 sheet đã đăng ký và 3 report chuẩn của workflow Study. Authoring dùng catalog API #82, reusable `Lesson`, AC-34 diagram/index, legacy/V1-PILOT schema artifacts và source Study hiện hành.

## Quyết định giữ lại

- Giữ `ApiEnvelope<Lesson>` cùng đúng status/error codes như contract trực tiếp.
- Ghi `ApiEnvelope<Lesson[]>` là phương án DERIVED do list intent, cần owner xác nhận; không đổi sang Page vì contract không khai báo pagination.
- Không tạo mapping cho `type`; đánh dấu SOURCE_REQUIRED.
- Legacy lessons chỉ là physical mapping candidate; không khẳng định live schema. Giữ discrepancy `course_id` nullable so với reusable Lesson required.
- Ghi Admin guard, LessonStatus values/casing, query validation và error `data` convention là các gap cần xử lý trước runtime integration.

## Phạm vi

Chỉ tạo tài liệu DD #82 và worklog liên quan. Không sửa router, module, tests, database, catalog, diagram hoặc context pages. AC-34 macro-review chờ đến khi #86 DD có mặt.

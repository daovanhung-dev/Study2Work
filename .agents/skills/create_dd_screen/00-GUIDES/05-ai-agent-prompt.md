# Prompt mẫu cho Codex / AI Agent tạo DD screen

Dán prompt sau vào Agent và thay các tham số trong dấu `[...]`:

```text
Nhiệm vụ: Tạo/hoàn thiện DD cho [SCREEN_ID] - [SCREEN_NAME] tại [OUTPUT_PATH].

Trước khi viết:
1) Đọc README.md, 00-GUIDES/03-dd-conventions.md và 01-TEMPLATES/SCREEN_ID/.
2) Khảo sát TOÀN BỘ ngữ cảnh cần thiết trong repo: router, screen component, shared UI,
   stores/state, services/API, DTO/types, auth, business logic, tests, screen liên quan.
3) Đọc [PATH_TO_UI_REFERENCE] và hai ảnh thiết kế (nếu có).
4) Đối chiếu API bằng OpenAPI, endpoint code hoặc schema, tuyệt đối không tự bịa contract.
5) Liệt kê những dữ kiện có bằng chứng (path + symbol) và những điểm CẦN_XÁC_NHẬN.

Output bắt buộc:
- 8 file: 00-overview.md, 01-ui-elements.md, 02-events.md, 03-data-flow.md,
  04-api-integration.md, 05-business-rules.md, 06-navigation.md, 07-test-cases.md.
- images/screen-clean.png và images/screen-numbered.png nếu có ảnh nguồn hợp lệ.
- Số marker trên ảnh phải ánh xạ 1–1 với Element ID.
- Event chi tiết theo: Trigger → Guard → Input Source → Validate → Logic → API
  → Mapping → State/UI → Navigation → Exceptions → Tests.
- Mọi mô tả dẫn ID và Markdown link tương đối chính xác, không copy trùng contract.
- Link chéo đến screen liên quan; không thay đổi code app nếu chưa được yêu cầu.

Trước khi kết thúc:
- Tự kiểm tra test coverage cho tất cả event, rule chính, loading/empty/error/auth.
- Chạy 03-TOOLS/validate_dd.py trên folder đã tạo.
- Báo cáo file tạo/sửa, link, quyết định đã xác minh và điểm còn CẦN_XÁC_NHẬN.
```

> Nếu ảnh nguồn không có sẵn, Agent phải ghi rõ thiếu ảnh, **không tự dựng ảnh rồi gọi là thiết kế thật**.

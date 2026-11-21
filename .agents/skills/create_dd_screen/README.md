# DD Screen Kit — Bộ template đặc tả thiết kế chi tiết màn hình

**Phiên bản:** 1.0 · **Ngôn ngữ:** Tiếng Việt · **Định dạng:** Markdown + PNG + Python 3

Bộ tài liệu giúp Product/BA/Designer/Frontend/Backend/QA và AI Agent (ví dụ Codex) thống nhất đặc tả trước khi lập trình. Mỗi screen có 8 file Markdown và 2 ảnh (ảnh gốc + ảnh đánh số phần tử).

> **QUAN TRỌNG:** Hai screen minh họa SH-01 và SH-02 dùng **nghiệp vụ, route, API và dữ liệu GIẢ ĐỊNH** để trình bày cách viết DD. Chúng **không phải đặc tả đã được kiểm chứng** từ repository Study2Work. Phải đối chiếu source code, UI thực tế và API/OpenAPI trước khi sử dụng để triển khai.

## Cấu trúc

```text
DD-Screen-Kit/
├── README.md
├── 00-GUIDES/
│   ├── 01-quick-start.md            # Bắt đầu nhanh
│   ├── 02-create-new-screen.md     # Hướng dẫn tạo DD screen từng bước
│   ├── 03-dd-conventions.md        # Tiêu chuẩn đặt ID, viết DD, tránh trùng lặp
│   ├── 04-review-checklist.md      # Tiêu chí nghiệm thu
│   └── 05-ai-agent-prompt.md       # Prompt làm việc với Codex / Agent
├── 01-TEMPLATES/
│   └── SCREEN_ID/                   # 8 template .md + images/README.md
├── 02-EXAMPLES/
│   ├── screen-index.md             # Danh mục & quan hệ screen
│   ├── SH-01-CourseList/           # DD mẫu hoàn thiện: danh sách khóa học
│   └── SH-02-CourseDetail/         # DD mẫu hoàn thiện: chi tiết khóa học
└── 03-TOOLS/
    ├── create_screen.py            # Sinh bộ DD mới từ templates
    └── validate_dd.py             # Kiểm tra cấu trúc và liên kết cơ bản
```

## Đọc theo thứ tự

1. `00-GUIDES/01-quick-start.md` — bắt đầu trong vài phút.
2. `02-EXAMPLES/SH-01-CourseList/` — đọc màn danh sách, bắt đầu từ `00-overview.md`.
3. `02-EXAMPLES/SH-02-CourseDetail/` — đọc màn chi tiết, theo liên kết từ SH-01.
4. `00-GUIDES/02-create-new-screen.md` — quy trình tạo màn mới, lấy dữ liệu từ source thực tế.
5. Dùng `03-TOOLS/create_screen.py` rồi `03-TOOLS/validate_dd.py`.

## Quy tắc nền tảng

- Viết **đúng theo nguồn chứng cứ**: screenshot/thiết kế, source code, API schema, nghiệp vụ đã xác nhận. Không tự bịa API hoặc giả định đã là sự thật.
- `02-events.md` là trung tâm trình tự xử lý, nhưng chỉ **tham chiếu ID** tới API, business rule và data mapping thay vì copy lại mọi thứ.
- Mã phần tử xuất hiện trong ảnh `screen-numbered.png` phải ánh xạ 1–1 với `01-ui-elements.md`.
- UI hiện trạng (ảnh clean) là một state tham khảo; mô tả đầy đủ cả loading, empty, error, disabled, unauthorized.
- Khi chưa rõ, đánh dấu `CẦN_XÁC_NHẬN` và ghi câu hỏi, người phụ trách, nguồn cần kiểm tra. Không che giấu sự không chắc chắn.

## Tám file và trách nhiệm

| File | Trả lời câu hỏi |
|---|---|
| `00-overview.md` | Screen nhằm mục đích gì, điều kiện vào là gì? |
| `01-ui-elements.md` | Có những phần tử nào, thuộc tính và state ra sao? |
| `02-events.md` | Tương tác hoặc lifecycle dẫn tới các bước xử lý nào? |
| `03-data-flow.md` | Dữ liệu đi từ đâu, biến đổi và lưu state như thế nào? |
| `04-api-integration.md` | Giao tiếp Backend dùng contract nào? |
| `05-business-rules.md` | Quy tắc và điều kiện nghiệp vụ bắt buộc là gì? |
| `06-navigation.md` | Vào/ra màn hình và mang theo tham số gì? |
| `07-test-cases.md` | Kiểm tra chức năng/ngoại lệ bằng kịch bản gì? |

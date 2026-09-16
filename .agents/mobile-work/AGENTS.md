# Mobile Work context router

```text
CONTEXT_STATUS: SOURCE_BACKED
scope: apps/work-client/mobile/
```

Hai source root là `flutter_business/` và `flutter_student/`. Kiến trúc, dependency
và convention đã được ghi nhận trong các page cùng thư mục; vẫn phải kiểm tra
exact source khi task thay đổi module cụ thể.

Progressive load:

1. `architecture.md`, `conventions.md`, `dependencies.md`.
2. `modules/README.md` và `workflows/README.md` để chọn nơi bổ sung context.
3. Exact `pubspec.yaml`, entrypoint, feature/controller/model/view và tests của
   task; không đọc cả hai app nếu task chỉ chạm một app.

Không tự điền Supabase/API/schema/navigation convention từ tên file.

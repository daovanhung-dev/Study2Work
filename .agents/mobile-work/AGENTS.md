# Mobile Work context router

```text
CONTEXT_STATUS: SKELETON_ONLY
scope: apps/work-client/mobile/
```

Theo yêu cầu hiện tại, không deep-load hoặc mô tả kiến trúc/module mobile. Hai
source root nhìn thấy là `flutter_business/` và `flutter_student/`; mọi thông tin
chi tiết phải được kiểm tra trong task mobile cụ thể.

Progressive load:

1. `architecture.md`, `conventions.md`, `dependencies.md`.
2. `modules/README.md` và `workflows/README.md` để chọn nơi bổ sung context.
3. Exact `pubspec.yaml`, entrypoint, feature/controller/model/view và tests của
   task; không đọc cả hai app nếu task chỉ chạm một app.

Không tự điền Supabase/API/schema/navigation convention từ tên file.

# Mobile Work context router

```text
CONTEXT_STATUS: SOURCE_BACKED
scope: apps/work-client/mobile/
```

Hai source root là `flutter_business/` và `flutter_student/`. Đây là hai Flutter
app độc lập, không phải một package Dart dùng chung. Kiến trúc, dependency,
module và workflow đã được ghi nhận trong các page cùng thư mục; vẫn phải kiểm
tra exact source khi task thay đổi module cụ thể.

Canonical page graph: `INDEX.md`.

Progressive load:

1. `../project/design.md`, `architecture.md`, `conventions.md`,
   `dependencies.md`.
2. `modules/README.md` và `workflows/README.md` để xác định feature, side effect
   và test liên quan.
3. Exact `pubspec.yaml`, entrypoint, feature/controller/model/view và tests của
   task; không đọc cả hai app nếu task chỉ chạm một app.

Với task authoring hoặc review DD cho Flutter/mobile module, load
`create-dd-from-bd-mobile` từ skill registry. Skill này tạo DD từ BD/BRD và
source evidence; không triển khai runtime code. Không dùng `createDD-markdown`
cho Mobile module DD vì skill đó thuộc boundary Web/API.

Không tự điền Supabase/API/schema/navigation convention từ tên file. Tên helper
chứa `Supabase` là compatibility naming; phải kiểm tra implementation trước khi
kết luận backend.

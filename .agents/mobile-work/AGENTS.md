# Mobile Work context router

```text
CONTEXT_STATUS: SOURCE_BACKED
scope: apps/work-client/mobile/
```

Hai source root là `flutter_business/` và `flutter_student/`. Đây là hai Flutter
app độc lập, không phải một package Dart dùng chung. Kiến trúc, dependency,
module, file inventory và workflow đã được ghi nhận trong các page cùng thư
mục; vẫn phải kiểm tra exact source khi task thay đổi module cụ thể.

Canonical page graph: `INDEX.md`.

Progressive load:

1. `INDEX.md` và `file-inventory.md` để xác định đúng app, file và status wiring.
2. `../project/design.md`, `architecture.md`, `conventions.md`,
   `dependencies.md`.
3. `modules/README.md`, `data-flow.md` và `workflows/README.md` để xác định
   feature, side effect và test liên quan.
4. Chọn đúng `flutter-student.md` hoặc `flutter-business.md`, sau đó đọc exact
   `pubspec.yaml`, entrypoint, feature/controller/model/view và tests; không đọc
   cả hai app nếu task chỉ chạm một app.

Tracked source boundary: inventory bao phủ 210 file Git-tracked trong hai app;
`build/`, `.dart_tool/`, cache và generated artifacts không được ghi vào agent
context. Mỗi file runtime phải được phân biệt giữa `WIRED`, `UNWIRED`,
`LEGACY`, `PLACEHOLDER` và UI-only behavior theo import/route evidence.

Với task authoring hoặc review DD cho Flutter/mobile module, load
`create-dd-from-bd-mobile` từ skill registry. Skill này tạo DD từ BD/BRD và
source evidence; không triển khai runtime code. Không dùng `createDD-markdown`
cho Mobile module DD vì skill đó thuộc boundary Web/API.

Không tự điền Supabase/API/schema/navigation convention từ tên file. Tên helper
chứa `Supabase` là compatibility naming; phải kiểm tra implementation trước khi
kết luận backend.

# Mobile Work context router

```text
CONTEXT_STATUS: SOURCE_BACKED
scope: apps/work-client/mobile/
```

Đây là một Flutter project tại `apps/work-client/mobile/` với hai Android
flavor `student` và `business`. Source role-specific đang nằm dưới
`lib/features/student/legacy/` và `lib/features/business/legacy/` trong giai
đoạn chuyển tiếp; app/core/shared mới là boundary dùng chung.

Canonical page graph: `INDEX.md`.

Progressive load:

1. `INDEX.md` và `file-inventory.md` để xác định đúng flavor, file và status wiring.
2. `../project/design.md`, `architecture.md`, `conventions.md`,
   `dependencies.md`.
3. `modules/README.md`, `data-flow.md` và `workflows/README.md` để xác định
   feature, side effect và test liên quan.
4. Chọn đúng `flutter-student.md` hoặc `flutter-business.md`, sau đó đọc exact
   `pubspec.yaml`, flavor config, entrypoint, feature/controller/model/view và
   tests; chỉ đọc role còn lại khi task chạm shared boundary.

Tracked source boundary: một root Flutter project chứa app/core/shared,
role-specific migration source, Android flavor resources và tests;
`build/`, `.dart_tool/`, cache và generated artifacts không được ghi vào agent
context. Mỗi file runtime phải được phân biệt giữa `WIRED`, `UNWIRED`,
`LEGACY`, `PLACEHOLDER` và UI-only behavior theo import/route evidence.

Với task authoring hoặc review DD cho Flutter/mobile module, load
`create-dd-from-bd-mobile` từ skill registry. Skill này tạo DD từ BD/BRD và
source evidence; không triển khai runtime code. Không dùng `createDD-markdown`
cho Mobile module DD vì skill đó thuộc boundary Web/API.

Package Dart hiện tại là `study2work_mobile`; không dùng lại `work_server` cho
source mới. Không tự điền Supabase/API/schema/navigation convention từ tên file. Tên helper
chứa `Supabase` là compatibility naming; phải kiểm tra implementation trước khi
kết luận backend.
